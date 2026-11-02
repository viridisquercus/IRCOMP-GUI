"""Working copies and explicit save. Project owner: Lukáš Dubšík; review pending."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from threading import RLock
from typing import Any
from uuid import uuid4

from ircomp_gui.application.commands import (
    ApplyTarget,
    AttachEvidence,
    Command,
    RemoveTarget,
    RenameStudy,
    RenameTarget,
    SetContext,
)
from ircomp_gui.application.ports import Repository
from ircomp_gui.application.prepare import PrepareService
from ircomp_gui.application.review import ReviewService
from ircomp_gui.domain.catalogue import Catalogue
from ircomp_gui.domain.errors import DomainError
from ircomp_gui.domain.models import (
    Diagnostic,
    DraftBuffers,
    RequestSnapshot,
    Revision,
    Study,
    TargetDraft,
)
from ircomp_gui.domain.rules import (
    active_revision,
    parse_target,
    request_diagnostics,
    revision_by_id,
    validate_revision,
    validate_study,
)


@dataclass
class Session:
    """A process-local working copy; accepted and durable versions are distinct."""

    workspace_id: str
    study: Study
    base_saved_version: int = 0
    version: int = 1
    saved: Study | None = None
    previous: Study | None = None


def new_uuid() -> str:
    """Generate a fresh opaque identity for each new object/revision."""
    return str(uuid4())


class WorkspaceService:
    """Own working state with serialized operations and replace-on-success semantics."""

    def __init__(
        self,
        repository: Repository,
        catalogue: Catalogue,
        new_id: Callable[[], str] = new_uuid,
    ) -> None:
        self.repository = repository
        self.catalogue = catalogue
        self.new_id = new_id
        self.sessions: dict[str, Session] = {}
        self.lock = RLock()
        self.prepare = PrepareService(catalogue, new_id)
        self.review = ReviewService(new_id)

    def get(self, workspace_id: str, expected_version: int | None = None) -> Session:
        """Resolve a session and reject stale changes before evaluating commands."""
        session = self.sessions.get(workspace_id)
        if session is None:
            raise DomainError(
                "SESSION_EXPIRED",
                (
                    "This working session is unavailable. Reopen the saved study;"
                    " unsaved changes may be lost."
                ),
            )
        if expected_version is not None and expected_version != session.version:
            raise DomainError(
                "WORKSPACE_CONFLICT",
                "The working copy changed. Refresh its state before retrying.",
            )
        return session

    def view(self, session: Session) -> dict[str, Any]:
        """Project public state without original byte payloads."""
        return {
            "workspace_id": session.workspace_id,
            "version": session.version,
            "base_saved_version": session.base_saved_version,
            "dirty": session.study != session.saved,
            "can_undo": session.previous is not None,
            "study": session.study.model_dump(
                mode="json", exclude={"evidence": {"__all__": {"content_base64"}}}
            ),
            "diagnostics": [
                item.model_dump()
                for item in request_diagnostics(
                    session.study, active_revision(session.study), self.catalogue
                )
            ],
        }

    def _register(self, study: Study, saved_version: int = 0) -> Session:
        validate_study(study, self.catalogue)
        session = Session(
            workspace_id=self.new_id(),
            study=study,
            base_saved_version=saved_version,
            saved=study if saved_version else None,
        )
        self.sessions[session.workspace_id] = session
        return session

    def create(self, title: str) -> Session:
        """Create an unsaved, empty study with explicitly synthetic defaults."""
        with self.lock:
            revision = Revision(
                revision_id=self.new_id(),
                reference_id="demo-reference-v1",
                profile_id="demo-spcas9-ngg-v1",
                targets=[],
            )
            study = Study(
                study_id=self.new_id(),
                request_id=self.new_id(),
                title=title,
                active_revision_id=revision.revision_id,
                revisions=[revision],
                target_labels={},
                evidence=[],
                collections=[],
                draft_buffers=DraftBuffers(),
            )
            return self._register(study)

    def open(self, study_id: str) -> Session:
        """Open a separate working copy, preserving saved unapplied draft strings."""
        with self.lock:
            saved = self.repository.load(study_id)
            return self._register(saved.study, saved.saved_version)

    def import_request(self, request: RequestSnapshot) -> Session:
        """Preserve imported identities without overwriting any saved study."""
        with self.lock:
            collision = self.repository.identity_exists(
                request.study_id, request.request_id
            )
            if collision:
                code = (
                    "IDENTITY_EXISTS"
                    if collision == request.study_id
                    else "IDENTITY_CONFLICT"
                )
                raise DomainError(
                    code,
                    f"Identity already belongs to study {collision}. "
                    "Open it or duplicate its request.",
                )
            study = Study(
                study_id=request.study_id,
                request_id=request.request_id,
                title=request.title,
                active_revision_id=request.revision.revision_id,
                revisions=[request.revision],
                target_labels=request.target_labels,
                evidence=[],
                collections=[],
                draft_buffers=DraftBuffers(),
            )
            return self._register(study)

    def duplicate(
        self, workspace_id: str, expected_version: int, title: str
    ) -> Session:
        """Copy active intent with fresh identities and no evidence or drafts."""
        with self.lock:
            source = self.get(workspace_id, expected_version).study
            revision = active_revision(source)
            replacements = {
                target.target_id: self.new_id() for target in revision.targets
            }
            copied = revision.model_copy(
                update={
                    "revision_id": self.new_id(),
                    "targets": [
                        target.model_copy(
                            update={"target_id": replacements[target.target_id]}
                        )
                        for target in revision.targets
                    ],
                }
            )
            study = Study(
                study_id=self.new_id(),
                request_id=self.new_id(),
                title=title,
                active_revision_id=copied.revision_id,
                revisions=[copied],
                target_labels={
                    replacements[target.target_id]: source.target_labels[
                        target.target_id
                    ]
                    for target in revision.targets
                },
                evidence=[],
                collections=[],
                draft_buffers=DraftBuffers(),
            )
            return self._register(study)

    def accept(self, session: Session, changed: Study, previous: Study) -> Session:
        """Validate the entire replacement before touching accepted state or Undo."""
        changed = Study.model_validate(changed.model_dump())
        validate_study(changed, self.catalogue)
        if changed != session.study:
            session.previous = previous
            session.study = changed
            session.version += 1
        return session

    def command(
        self,
        workspace_id: str,
        expected_version: int,
        buffers: DraftBuffers,
        command: Command,
    ) -> Session:
        """Execute a typed local command; attachment is coordinated by ImportService."""
        with self.lock:
            session = self.get(workspace_id, expected_version)
            previous = session.study.model_copy(update={"draft_buffers": buffers})
            validate_study(previous, self.catalogue)
            if isinstance(command, AttachEvidence):
                raise DomainError(
                    "SCHEMA_INVALID", "Attachment requires an owned evidence preview."
                )
            if isinstance(
                command,
                (RenameStudy, ApplyTarget, RemoveTarget, RenameTarget, SetContext),
            ):
                changed = self.prepare.apply(previous, command)
            else:
                changed = self.review.apply(previous, command)
            return self.accept(session, changed, previous)

    def save(
        self,
        workspace_id: str,
        expected_version: int,
        expected_saved_version: int,
        buffers: DraftBuffers,
    ) -> Session:
        """Publish Saved only after the compare-and-save transaction commits."""
        with self.lock:
            session = self.get(workspace_id, expected_version)
            if session.base_saved_version != expected_saved_version:
                raise DomainError(
                    "SAVE_CONFLICT",
                    "The saved version no longer matches this working copy.",
                )
            proposed = session.study.model_copy(update={"draft_buffers": buffers})
            version = self.repository.save(proposed, expected_saved_version)
            session.study = proposed
            session.saved = proposed
            session.base_saved_version = version
            session.version += 1
            session.previous = None
            return session

    def undo(self, workspace_id: str, expected_version: int) -> Session:
        """Restore one unsaved accepted action without inventing another revision."""
        with self.lock:
            session = self.get(workspace_id, expected_version)
            if session.previous is None:
                raise DomainError(
                    "UNDO_UNAVAILABLE", "There is no unsaved accepted action to undo."
                )
            session.study = session.previous
            session.previous = None
            session.version += 1
            return session

    def validate(
        self,
        workspace_id: str,
        revision_id: str,
        target_draft: TargetDraft | None = None,
    ) -> dict[str, Any]:
        """Report local checks and explicitly unperformed scientific checks."""
        with self.lock:
            session = self.get(workspace_id)
            revision = revision_by_id(session.study, revision_id)
            diagnostics = request_diagnostics(session.study, revision, self.catalogue)
            draft_diagnostics: list[Diagnostic] = []
            if target_draft is not None:
                try:
                    target = parse_target(
                        target_draft, target_draft.target_id or self.new_id()
                    )
                    validate_revision(
                        revision.model_copy(update={"targets": [target]}),
                        self.catalogue,
                    )
                except DomainError as error:
                    draft_diagnostics = error.diagnostics
            checks = [
                {
                    "name": "Local request structure and catalogue bounds",
                    "status": "failed" if diagnostics else "passed",
                    "message": (
                        "Local checks only; no biological or compiler acceptance is "
                        "implied."
                    ),
                }
            ]
            for name in [
                "Reference sequence availability/checksum",
                "Sequence extraction",
                "PAM inspection",
                "Off-target search",
                "Biological suitability",
                "IRCOMP specification and controller validation",
            ]:
                checks.append(
                    {
                        "name": name,
                        "status": "not_performed",
                        "message": "Not performed by this local workspace.",
                    }
                )
            return {
                "workspace_version": session.version,
                "revision_id": revision_id,
                "export_ready": not diagnostics,
                "checks": checks,
                "diagnostics": [item.model_dump() for item in diagnostics],
                "draft_diagnostics": [item.model_dump() for item in draft_diagnostics],
            }
