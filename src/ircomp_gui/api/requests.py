"""HTTP request contracts. Project owner: Lukáš Dubšík; review pending."""

from typing import Annotated, Literal

from pydantic import Field

from ircomp_gui.application.commands import Command
from ircomp_gui.domain.models import DraftBuffers, Id, Label, TargetDraft, Value

Version = Annotated[int, Field(ge=1)]
SavedVersion = Annotated[int, Field(ge=0)]


class NewWorkspace(Value):
    """Create an independently usable local request."""

    source: Literal["new"]
    title: Label


class SavedWorkspace(Value):
    """Open a durable study in a separate session."""

    source: Literal["saved"]
    study_id: Id


class DuplicateWorkspace(Value):
    """Duplicate only the active request."""

    source: Literal["duplicate"]
    workspace_id: Id
    expected_version: Version
    title: Label


class ImportedWorkspace(Value):
    """Accept a ready request preview."""

    source: Literal["request_import"]
    preview_id: Id


CreateInput = Annotated[
    NewWorkspace | SavedWorkspace | DuplicateWorkspace | ImportedWorkspace,
    Field(discriminator="source"),
]


class CommandInput(Value):
    """A version-checked accepted-state operation and current editor buffers."""

    expected_version: Version
    draft_buffers: DraftBuffers
    command: Command


class SaveInput(Value):
    """Explicit Save with both concurrency boundaries."""

    expected_version: Version
    expected_saved_version: SavedVersion
    draft_buffers: DraftBuffers


class VersionInput(Value):
    """Check a session version before Undo."""

    expected_version: Version


class CloseInput(VersionInput):
    """Explicit confirmation of working-copy discard."""

    discard: Literal[True]


class ValidateInput(Value):
    """Local validation only, including a separate unapplied editor buffer."""

    revision_id: Id
    target_draft: TargetDraft | None


class RequestImport(Value):
    """Exact request bytes, base64 encoded for JSON transport."""

    kind: Literal["request"]
    content_base64: Annotated[str, Field(max_length=1398104)]


class EvidenceImport(Value):
    """Exact evidence bytes and explicitly selected request context."""

    kind: Literal["evidence"]
    content_base64: Annotated[str, Field(max_length=1398104)]
    workspace_id: Id
    expected_version: Version
    revision_id: Id


ImportInput = Annotated[RequestImport | EvidenceImport, Field(discriminator="kind")]


class ExportInput(Value):
    """Freeze bytes from one explicitly selected durable revision."""

    study_id: Id
    saved_version: Version
    revision_id: Id
    kind: Literal["request", "review"]
    collection_ids: Annotated[list[Id], Field(max_length=20)]
