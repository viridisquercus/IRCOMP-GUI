"""State and exchange acceptance. Project owner: Lukáš Dubšík; review pending."""

from __future__ import annotations

import ast
import base64
import hashlib
import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

import pytest
from fastapi.testclient import TestClient
from httpx import Client
from pydantic import TypeAdapter, ValidationError

from ircomp_gui.adapters.exchange import Exchange
from ircomp_gui.adapters.resources import load_catalogue, resource_path
from ircomp_gui.adapters.sqlite import SQLiteRepository
from ircomp_gui.api.app import create_app
from ircomp_gui.application.commands import Command
from ircomp_gui.application.export import ExportService
from ircomp_gui.application.imports import ImportService
from ircomp_gui.application.workspace import Session, WorkspaceService
from ircomp_gui.domain.errors import DomainError
from ircomp_gui.domain.models import (
    CandidateKey,
    DraftBuffers,
    RequestSnapshot,
    TargetDraft,
)
from ircomp_gui.domain.rules import active_revision
from ircomp_gui.domain.serialization import decode_base64, parse_json

ADAPTER: TypeAdapter[Command] = TypeAdapter(Command)


@dataclass
class Stack:
    workspace: WorkspaceService
    imports: ImportService
    exports: ExportService
    repository: SQLiteRepository
    exchange: Exchange
    session: Session


@pytest.fixture
def stack(tmp_path: Path) -> Stack:
    catalogue = load_catalogue()
    exchange = Exchange(catalogue)
    repository = SQLiteRepository(tmp_path / "workspace.sqlite3", catalogue, exchange)
    workspace = WorkspaceService(repository, catalogue)
    imports = ImportService(workspace, exchange)
    exports = ExportService(workspace, exchange)
    request = cast(
        "RequestSnapshot",
        exchange.decode(
            resource_path("examples/request-valid.json").read_bytes(), "request"
        ),
    )
    return Stack(
        workspace,
        imports,
        exports,
        repository,
        exchange,
        workspace.import_request(request),
    )


def command(
    stack: Stack, value: dict[str, Any], buffers: DraftBuffers | None = None
) -> Session:
    session = stack.session
    return stack.workspace.command(
        session.workspace_id,
        session.version,
        buffers or session.study.draft_buffers,
        ADAPTER.validate_python(value),
    )


def evidence_raw(*, bundle_id: str | None = None) -> bytes:
    raw = resource_path("examples/evidence-valid.json").read_bytes()
    if bundle_id is None:
        return raw
    value = json.loads(raw)
    value["bundle_id"] = bundle_id
    return json.dumps(value).encode()


def preview(stack: Stack, raw: bytes) -> dict[str, Any]:
    session = stack.session
    return stack.imports.preview(
        "evidence",
        base64.b64encode(raw).decode(),
        session.workspace_id,
        session.version,
        session.study.active_revision_id,
    )


def attach(stack: Stack, raw: bytes | None = None) -> None:
    result = preview(stack, raw or evidence_raw())
    _ = stack.imports.attach(
        stack.session.workspace_id,
        stack.session.version,
        stack.session.study.draft_buffers,
        result["preview_id"],
    )


def save(stack: Stack, buffers: DraftBuffers | None = None) -> None:
    session = stack.session
    _ = stack.workspace.save(
        session.workspace_id,
        session.version,
        session.base_saved_version,
        buffers or session.study.draft_buffers,
    )


def target_draft(stack: Stack, **changes: str) -> TargetDraft:
    target = active_revision(stack.session.study).targets[0]
    return TargetDraft.model_validate(
        {
            "target_id": target.target_id,
            "label": stack.session.study.target_labels[target.target_id],
            "contig": target.contig,
            "start": str(target.start),
            "end": str(target.end),
            "strand": target.strand,
            **changes,
        }
    )


def test_cosmetic_edit_revision_change_and_undo(stack: Stack) -> None:
    session = stack.session
    original_revision = session.study.active_revision_id
    target = active_revision(session.study).targets[0]
    _ = command(
        stack,
        {"type": "rename_target", "target_id": target.target_id, "label": "Renamed"},
    )
    assert session.study.active_revision_id == original_revision
    count = len(session.study.revisions)
    draft = target_draft(stack, end="250")
    _ = command(stack, {"type": "apply_target", "draft": draft.model_dump()})
    assert len(session.study.revisions) == count + 1
    assert session.study.revisions[-2].targets[0].end == 200
    _ = stack.workspace.undo(session.workspace_id, session.version)
    assert session.study.active_revision_id == original_revision
    assert active_revision(session.study).targets[0].end == 200
    with pytest.raises(DomainError, match="no unsaved accepted"):
        _ = stack.workspace.undo(session.workspace_id, session.version)


@pytest.mark.parametrize(
    "value", ["", "-1", "1.5", "1e2", " 10", "١٢", "9007199254740992"]
)
def test_invalid_coordinates_preserve_state(stack: Stack, value: str) -> None:
    before = stack.session.study.model_dump_json()
    version = stack.session.version
    with pytest.raises((DomainError, ValidationError)):
        _ = command(
            stack,
            {
                "type": "apply_target",
                "draft": target_draft(stack, start=value).model_dump(),
            },
        )
    assert stack.session.study.model_dump_json() == before
    assert stack.session.version == version


def test_zero_start_and_bounds(stack: Stack) -> None:
    _ = command(
        stack,
        {
            "type": "apply_target",
            "draft": target_draft(stack, start="0", end="10000").model_dump(),
        },
    )
    assert active_revision(stack.session.study).targets[0].start == 0
    with pytest.raises(DomainError, match="end-exclusive"):
        _ = command(
            stack,
            {
                "type": "apply_target",
                "draft": target_draft(stack, end="10001").model_dump(),
            },
        )


def test_invalid_saved_draft_reopens_without_changing_accepted_target(
    stack: Stack,
) -> None:
    draft = target_draft(stack, end="")
    save(stack, DraftBuffers(target=draft))
    opened = stack.workspace.open(stack.session.study.study_id)
    assert opened.study.draft_buffers.target == draft
    assert active_revision(opened.study).targets[0].end == 200
    assert opened.previous is None
    assert not stack.workspace.view(opened)["dirty"]
    duplicated = stack.workspace.duplicate(opened.workspace_id, opened.version, "Copy")
    assert duplicated.study.request_id != opened.study.request_id
    assert (
        active_revision(duplicated.study).targets[0].target_id
        != active_revision(opened.study).targets[0].target_id
    )
    assert duplicated.study.draft_buffers == DraftBuffers()
    assert duplicated.study.evidence == []


def test_context_replacement_is_atomic_and_explicit(stack: Stack) -> None:
    target = active_revision(stack.session.study).targets[0]
    before = stack.session.study
    with pytest.raises(DomainError):
        _ = command(
            stack,
            {
                "type": "set_context",
                "reference_id": "grch38-p14-primary-v1",
                "profile_id": "spcas9-ngg-preexperiment-v1",
                "targets": [target.model_dump()],
            },
        )
    assert stack.session.study == before
    _ = command(
        stack,
        {
            "type": "set_context",
            "reference_id": "grch38-p14-primary-v1",
            "profile_id": "spcas9-ngg-preexperiment-v1",
            "targets": [{**target.model_dump(), "contig": "NC_000001.11"}],
        },
    )
    assert active_revision(stack.session.study).reference_id == "grch38-p14-primary-v1"


def test_two_tab_save_conflict_and_failed_storage_keep_work(
    stack: Stack, tmp_path: Path
) -> None:
    save(stack)
    other = stack.workspace.open(stack.session.study.study_id)
    _ = command(stack, {"type": "rename_study", "title": "First tab"})
    save(stack)
    with pytest.raises(DomainError) as failure:
        _ = stack.workspace.save(
            other.workspace_id, other.version, other.base_saved_version, DraftBuffers()
        )
    assert failure.value.code == "SAVE_CONFLICT"
    assert other.study.title != "First tab"
    _ = command(stack, {"type": "rename_study", "title": "Keep this unsaved title"})
    path = stack.repository.path
    stack.repository.path = tmp_path / "absent-directory" / "database.sqlite3"
    before = stack.session.study
    version = stack.session.version
    with pytest.raises(DomainError) as failure:
        save(stack)
    assert failure.value.code == "PERSISTENCE_UNAVAILABLE"
    assert stack.session.study == before and stack.session.version == version
    stack.repository.path = path
    assert stack.repository.load(before.study_id).study.title == "First tab"


def test_evidence_duplicate_collision_stale_preview_and_original_bytes(
    stack: Stack,
) -> None:
    raw = evidence_raw()
    attach(stack, raw)
    assert stack.session.study.evidence[0].bundle.candidates[0].metrics[0].value == 0
    assert stack.session.study.evidence[0].bundle.candidates[0].metrics[1].value is None
    assert base64.b64decode(stack.session.study.evidence[0].content_base64) == raw
    version = stack.session.version
    duplicate = preview(stack, raw)
    assert duplicate["status"] == "duplicate"
    _ = stack.imports.attach(
        stack.session.workspace_id, version, DraftBuffers(), duplicate["preview_id"]
    )
    assert stack.session.version == version
    collision = preview(stack, raw + b"\n")
    assert collision["status"] == "blocked"
    assert collision["diagnostics"][0]["code"] == "BUNDLE_ID_COLLISION"
    stack.imports.cancel(collision["preview_id"])
    ready = preview(stack, evidence_raw(bundle_id=stack.workspace.new_id()))
    _ = command(stack, {"type": "rename_study", "title": "Changed after preview"})
    before = stack.session.study
    with pytest.raises(DomainError) as failure:
        _ = stack.imports.attach(
            stack.session.workspace_id,
            stack.session.version,
            DraftBuffers(),
            ready["preview_id"],
        )
    assert failure.value.code == "PREVIEW_STALE"
    assert stack.session.study == before


def test_old_evidence_retains_context_and_empty_bundle_is_valid(stack: Stack) -> None:
    attach(stack)
    old = stack.session.study.active_revision_id
    _ = command(
        stack,
        {"type": "apply_target", "draft": target_draft(stack, end="220").model_dump()},
    )
    assert stack.session.study.evidence[0].bundle.context.revision_id == old
    assert preview(stack, evidence_raw())["status"] == "blocked"
    empty = resource_path("examples/evidence-empty.json").read_bytes()
    result = stack.imports.preview(
        "evidence",
        base64.b64encode(empty).decode(),
        stack.session.workspace_id,
        stack.session.version,
        old,
    )
    assert result["status"] == "ready" and result["summary"]["candidate_count"] == 0
    _ = stack.imports.attach(
        stack.session.workspace_id,
        stack.session.version,
        DraftBuffers(),
        result["preview_id"],
    )
    assert len(stack.session.study.evidence) == 2


def test_collection_specific_decisions_source_closure_and_frozen_export(
    stack: Stack,
) -> None:
    attach(stack)
    first_bundle = stack.session.study.evidence[0].bundle
    key = CandidateKey(bundle_id=first_bundle.bundle_id, candidate_id="demo-A")
    first = stack.session.study.collections[0]
    _ = command(
        stack,
        {
            "type": "add_member",
            "collection_id": first.collection_id,
            "candidate": key.model_dump(),
        },
    )
    _ = command(
        stack,
        {
            "type": "create_collection",
            "revision_id": first.revision_id,
            "name": "Other review",
        },
    )
    second = stack.session.study.collections[-1]
    _ = command(
        stack,
        {
            "type": "add_member",
            "collection_id": second.collection_id,
            "candidate": key.model_dump(),
        },
    )
    _ = command(
        stack,
        {
            "type": "set_decision",
            "collection_id": first.collection_id,
            "candidate": key.model_dump(),
            "disposition": "include_for_review",
            "rationale": "Needs an independent domain review.",
            "evidence_refs": [],
        },
    )
    assert stack.session.study.collections[-1].memberships[0].disposition == "undecided"
    save(stack)
    result = stack.exports.prepare(
        stack.session.study.study_id,
        stack.session.base_saved_version,
        first.revision_id,
        "review",
        [first.collection_id],
    )
    assert result["review_status"] == "reviewed" and result["unresolved_count"] == 0
    raw = stack.exports.download(result["export_id"]).raw
    document = json.loads(raw)
    assert len(document["collections"]) == 1
    assert (
        base64.b64decode(document["evidence_files"][0]["content_base64"])
        == evidence_raw()
    )
    assert hashlib.sha256(raw).hexdigest() == result["sha256"]
    _ = command(
        stack,
        {
            "type": "set_decision",
            "collection_id": first.collection_id,
            "candidate": key.model_dump(),
            "disposition": "needs_clarification",
            "rationale": "",
            "evidence_refs": [],
        },
    )
    save(stack)
    assert stack.exports.download(result["export_id"]).raw == raw
    draft = stack.exports.prepare(
        stack.session.study.study_id,
        stack.session.base_saved_version,
        first.revision_id,
        "review",
        [first.collection_id, second.collection_id],
    )
    assert draft["review_status"] == "draft" and draft["unresolved_count"] == 2
    _ = command(
        stack, {"type": "remove_collection", "collection_id": first.collection_id}
    )
    assert len(stack.session.study.evidence) == 1
    _ = stack.workspace.undo(stack.session.workspace_id, stack.session.version)
    assert any(
        item.collection_id == first.collection_id
        for item in stack.session.study.collections
    )


def test_request_round_trip_identity_and_corrupt_storage(
    stack: Stack, tmp_path: Path
) -> None:
    save(stack)
    result = stack.exports.prepare(
        stack.session.study.study_id,
        1,
        stack.session.study.active_revision_id,
        "request",
        [],
    )
    request = cast(
        "RequestSnapshot",
        stack.exchange.decode(
            stack.exports.download(result["export_id"]).raw, "request"
        ),
    )
    repository = SQLiteRepository(
        tmp_path / "different.sqlite3", stack.workspace.catalogue, stack.exchange
    )
    other = WorkspaceService(repository, stack.workspace.catalogue)
    imported = other.import_request(request)
    assert imported.study.request_id == stack.session.study.request_id
    assert active_revision(imported.study) == active_revision(stack.session.study)
    with pytest.raises(DomainError) as failure:
        _ = stack.workspace.import_request(request)
    assert failure.value.code == "IDENTITY_EXISTS"
    with sqlite3.connect(stack.repository.path) as connection:
        _ = connection.execute(
            "UPDATE studies SET document_json = ?",
            ('{"storage_version": 99, "study": {}}',),
        )
    with pytest.raises(DomainError):
        _ = stack.repository.load(stack.session.study.study_id)
    with sqlite3.connect(stack.repository.path) as connection:
        assert (
            "99"
            in connection.execute("SELECT document_json FROM studies").fetchone()[0]
        )


@pytest.mark.parametrize(
    "raw, code",
    [
        (b'{"x":1,"x":2}', "DUPLICATE_KEY"),
        (b'{"x":NaN}', "SCHEMA_INVALID"),
        (b'{"x":1e999}', "SCHEMA_INVALID"),
        (b"[]", "SCHEMA_INVALID"),
        (b"bad", "MALFORMED_JSON"),
        (b'{"x":' * 33 + b"0" + b"}" * 33, "LIMIT_EXCEEDED"),
    ],
)
def test_parser_rejects_unsafe_or_ambiguous_input(raw: bytes, code: str) -> None:
    with pytest.raises(DomainError) as failure:
        _ = parse_json(raw)
    assert failure.value.code == code


def test_import_byte_limit_and_schema_valid_semantic_failures(stack: Stack) -> None:
    with pytest.raises(DomainError):
        _ = decode_base64(base64.b64encode(b"x" * 1048577).decode())
    for name in [
        "request-invalid-interval.json",
        "evidence-context-mismatch.json",
        "evidence-invalid-missing-value.json",
        "evidence-unsupported-version.json",
    ]:
        raw = resource_path(f"examples/{name}").read_bytes()
        with pytest.raises(DomainError):
            _ = stack.exchange.decode(
                raw, "request" if name.startswith("request") else "evidence"
            )


def test_http_contract_strict_types_origins_and_full_workflow(tmp_path: Path) -> None:
    app = create_app(tmp_path / "http.sqlite3")
    with cast("Client", TestClient(app, base_url="http://127.0.0.1:8000")) as client:
        assert client.get("/api/v1/catalogue").status_code == 200
        assert client.get("/openapi.json").status_code == 200
        denied = client.post(
            "/api/v1/workspaces",
            json={"source": "new", "title": "No"},
            headers={"Origin": "https://foreign.example"},
        )
        assert denied.status_code == 403
        malformed = client.post(
            "/api/v1/workspaces",
            content='{"source":"new","source":"saved"}',
            headers={"Content-Type": "application/json"},
        )
        assert (
            malformed.status_code == 400
            and malformed.json()["error"]["code"] == "DUPLICATE_KEY"
        )
        raw = resource_path("examples/request-valid.json").read_bytes()
        inspected = client.post(
            "/api/v1/imports",
            json={"kind": "request", "content_base64": base64.b64encode(raw).decode()},
        )
        assert inspected.status_code == 201
        opened = client.post(
            "/api/v1/workspaces",
            json={
                "source": "request_import",
                "preview_id": inspected.json()["preview_id"],
            },
        )
        assert opened.status_code == 201
        workspace = opened.json()
        route = f"/api/v1/workspaces/{workspace['workspace_id']}"
        invalid = client.post(
            route + "/save",
            json={
                "expected_version": True,
                "expected_saved_version": 0,
                "draft_buffers": {"target": None, "decision": None},
            },
        )
        assert invalid.status_code == 422
        saved = client.post(
            route + "/save",
            json={
                "expected_version": workspace["version"],
                "expected_saved_version": 0,
                "draft_buffers": {"target": None, "decision": None},
            },
        )
        assert saved.status_code == 200
        workspace = saved.json()
        check = client.post(
            route + "/validate",
            json={
                "revision_id": workspace["study"]["active_revision_id"],
                "target_draft": None,
            },
        )
        assert check.json()["export_ready"] is True
        assert any(item["status"] == "not_performed" for item in check.json()["checks"])
        evidence = client.post(
            "/api/v1/imports",
            json={
                "kind": "evidence",
                "content_base64": base64.b64encode(evidence_raw()).decode(),
                "workspace_id": workspace["workspace_id"],
                "expected_version": workspace["version"],
                "revision_id": workspace["study"]["active_revision_id"],
            },
        )
        attached = client.post(
            route + "/commands",
            json={
                "expected_version": workspace["version"],
                "draft_buffers": {"target": None, "decision": None},
                "command": {
                    "type": "attach_evidence",
                    "preview_id": evidence.json()["preview_id"],
                },
            },
        )
        assert attached.status_code == 200
        assert "content_base64" not in attached.json()["study"]["evidence"][0]
        closed = client.request(
            "DELETE",
            route,
            json={"expected_version": attached.json()["version"], "discard": True},
        )
        assert closed.status_code == 204
        assert client.get(route).status_code == 404
        assert len(client.get("/api/v1/studies").json()["studies"]) == 1


def test_target_add_remove_drafts_and_noop_identity(stack: Stack) -> None:
    draft = TargetDraft(
        target_id=None,
        label="Second target",
        contig="demo_contig",
        start="300",
        end="450",
        strand=".",
    )
    _ = command(stack, {"type": "apply_target", "draft": draft.model_dump()})
    targets = active_revision(stack.session.study).targets
    assert len(targets) == 2
    added = next(target for target in targets if target.start == 300)
    version = stack.session.version
    same = TargetDraft(
        target_id=added.target_id,
        label="Second target",
        contig=added.contig,
        start="300",
        end="450",
        strand=".",
    )
    _ = command(stack, {"type": "apply_target", "draft": same.model_dump()})
    assert stack.session.version == version
    _ = command(
        stack,
        {"type": "remove_target", "target_id": added.target_id},
        DraftBuffers(target=same),
    )
    assert stack.session.study.draft_buffers.target is None
    assert len(active_revision(stack.session.study).targets) == 1
    _ = stack.workspace.undo(stack.session.workspace_id, stack.session.version)
    assert len(active_revision(stack.session.study).targets) == 2
    assert stack.session.study.draft_buffers.target == same


def test_supporting_reference_closure_and_dangling_rejection(stack: Stack) -> None:
    attach(stack)
    first = stack.session.study.evidence[0].bundle
    second_id = stack.workspace.new_id()
    attach(stack, evidence_raw(bundle_id=second_id))
    collection = stack.session.study.collections[0]
    key = {"bundle_id": first.bundle_id, "candidate_id": "demo-A"}
    _ = command(
        stack,
        {
            "type": "add_member",
            "collection_id": collection.collection_id,
            "candidate": key,
        },
    )
    before = stack.session.study
    with pytest.raises(DomainError):
        _ = command(
            stack,
            {
                "type": "set_decision",
                "collection_id": collection.collection_id,
                "candidate": key,
                "disposition": "exclude",
                "rationale": "Example",
                "evidence_refs": [{"bundle_id": second_id, "candidate_id": "missing"}],
            },
        )
    assert stack.session.study == before
    _ = command(
        stack,
        {
            "type": "set_decision",
            "collection_id": collection.collection_id,
            "candidate": key,
            "disposition": "exclude",
            "rationale": "Conflicting source requires separate follow-up.",
            "evidence_refs": [{"bundle_id": second_id, "candidate_id": "demo-A"}],
        },
    )
    save(stack)
    result = stack.exports.prepare(
        before.study_id,
        stack.session.base_saved_version,
        collection.revision_id,
        "review",
        [collection.collection_id],
    )
    exported = json.loads(stack.exports.download(result["export_id"]).raw)
    assert {item["bundle_id"] for item in exported["evidence_files"]} == {
        first.bundle_id,
        second_id,
    }
    _ = command(
        stack,
        {
            "type": "rename_collection",
            "collection_id": collection.collection_id,
            "name": "Renamed review",
        },
    )
    assert stack.session.study.collections[0].name == "Renamed review"
    _ = command(
        stack,
        {
            "type": "remove_member",
            "collection_id": collection.collection_id,
            "candidate": key,
        },
    )
    assert stack.session.study.collections[0].memberships == []
    version = stack.session.version
    _ = command(
        stack,
        {
            "type": "remove_member",
            "collection_id": collection.collection_id,
            "candidate": key,
        },
    )
    assert stack.session.version == version
    assert len(stack.session.study.evidence) == 2


def test_missing_metric_states_and_invalid_preview_metadata(stack: Stack) -> None:
    document = json.loads(evidence_raw())
    for state in ["unsupported", "failed", "unknown"]:
        document["candidates"][0]["metrics"].append(
            {
                "name": state,
                "model": None,
                "unit": None,
                "scale": None,
                "direction": None,
                "availability": state,
                "value": None,
            }
        )
    attach(stack, json.dumps(document).encode())
    assert [
        item.availability
        for item in stack.session.study.evidence[0].bundle.candidates[0].metrics
    ] == ["present", "not_supplied", "unsupported", "failed", "unknown"]
    document["context"]["reference_id"] = {"invalid": "object"}
    result = preview(stack, json.dumps(document).encode())
    assert result["status"] == "blocked"
    assert result["summary"]["received_context"] is None


def test_preview_limits_and_empty_review_export(stack: Stack) -> None:
    for _ in range(5):
        _ = preview(stack, evidence_raw())
    with pytest.raises(DomainError) as failure:
        _ = preview(stack, evidence_raw())
    assert failure.value.code == "LIMIT_EXCEEDED"
    for preview_id in list(stack.imports.previews):
        stack.imports.cancel(preview_id)
    attach(stack, resource_path("examples/evidence-empty.json").read_bytes())
    collection = stack.session.study.collections[0]
    save(stack)
    result = stack.exports.prepare(
        stack.session.study.study_id,
        1,
        collection.revision_id,
        "review",
        [collection.collection_id],
    )
    assert result["candidate_count"] == 0 and result["unresolved_count"] == 1
    document = json.loads(stack.exports.download(result["export_id"]).raw)
    assert len(document["evidence_files"]) == 1
    for _ in range(5):
        _ = stack.exports.prepare(
            stack.session.study.study_id, 1, collection.revision_id, "request", []
        )
    with pytest.raises(DomainError) as failure:
        _ = stack.exports.download(result["export_id"])
    assert failure.value.code == "PREVIEW_EXPIRED"


def test_corrupt_source_digest_and_collection_limit_preserve_state(
    stack: Stack,
) -> None:
    attach(stack)
    save(stack)
    for index in range(19):
        _ = command(
            stack,
            {
                "type": "create_collection",
                "revision_id": stack.session.study.active_revision_id,
                "name": f"Collection {index}",
            },
        )
    before = stack.session.study
    with pytest.raises(DomainError) as failure:
        _ = command(
            stack,
            {
                "type": "create_collection",
                "revision_id": stack.session.study.active_revision_id,
                "name": "Over the limit",
            },
        )
    assert failure.value.code == "LIMIT_EXCEEDED" and stack.session.study == before
    with sqlite3.connect(stack.repository.path) as connection:
        row = connection.execute("SELECT document_json FROM studies").fetchone()
        document = json.loads(row[0])
        document["study"]["evidence"][0]["sha256"] = "0" * 64
        _ = connection.execute(
            "UPDATE studies SET document_json = ?", (json.dumps(document),)
        )
    with pytest.raises(DomainError, match="disagree"):
        _ = stack.repository.load(stack.session.study.study_id)


def test_stale_workspace_and_wrong_revision_membership_rejected(stack: Stack) -> None:
    attach(stack)
    old = stack.session.study.active_revision_id
    version = stack.session.version
    _ = command(
        stack,
        {"type": "apply_target", "draft": target_draft(stack, end="230").model_dump()},
    )
    with pytest.raises(DomainError) as failure:
        _ = stack.workspace.undo(stack.session.workspace_id, version)
    assert failure.value.code == "WORKSPACE_CONFLICT"
    _ = command(
        stack,
        {
            "type": "create_collection",
            "revision_id": stack.session.study.active_revision_id,
            "name": "New context",
        },
    )
    new_collection = stack.session.study.collections[-1]
    with pytest.raises(DomainError):
        _ = command(
            stack,
            {
                "type": "add_member",
                "collection_id": new_collection.collection_id,
                "candidate": {
                    "bundle_id": stack.session.study.evidence[0].bundle.bundle_id,
                    "candidate_id": "demo-A",
                },
            },
        )
    assert stack.session.study.evidence[0].bundle.context.revision_id == old


@pytest.mark.parametrize("version", [0, 1])
def test_unsupported_database_layout_is_not_repaired(
    tmp_path: Path, version: int
) -> None:
    path = tmp_path / "unsupported.sqlite3"
    with sqlite3.connect(path) as connection:
        if version == 0:
            _ = connection.execute("CREATE TABLE unrelated (message TEXT)")
            _ = connection.execute("INSERT INTO unrelated VALUES ('keep me')")
        else:
            _ = connection.execute("PRAGMA user_version = 1")
    before = path.read_bytes()
    catalogue = load_catalogue()
    with pytest.raises(DomainError) as failure:
        _ = SQLiteRepository(path, catalogue, Exchange(catalogue))
    assert failure.value.code == "SCHEMA_INVALID"
    assert path.read_bytes() == before


def test_domain_and_application_keep_inward_dependencies() -> None:
    source = Path(__file__).resolve().parents[1] / "src/ircomp_gui"
    forbidden = (
        "fastapi",
        "starlette",
        "sqlite3",
        "ircomp_gui.adapters",
        "ircomp_gui.api",
    )
    for layer in ["domain", "application"]:
        for path in (source / layer).glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            modules: list[str] = []
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module:
                    modules.append(node.module)
                elif isinstance(node, ast.Import):
                    modules.extend(alias.name for alias in node.names)
            assert not any(name.startswith(forbidden) for name in modules), path.name
            if layer == "domain":
                assert not any(
                    name.startswith("ircomp_gui.application") for name in modules
                )
