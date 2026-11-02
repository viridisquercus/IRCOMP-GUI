"""Strict local data contracts. Project owner: Lukáš Dubšík; review pending."""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue

Id = Annotated[
    str,
    Field(pattern=r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"),
]
Label = Annotated[str, Field(min_length=1, max_length=200, pattern=r"\S")]
Text = Annotated[str, Field(max_length=200)]
Coordinate = Annotated[int, Field(ge=0, le=9007199254740991)]
Disposition = Literal[
    "undecided", "include_for_review", "exclude", "needs_clarification"
]


class Value(BaseModel):
    """Reject coercions and unknown fields at every model boundary."""

    model_config = ConfigDict(
        strict=True, extra="forbid", frozen=True, allow_inf_nan=False
    )


class Diagnostic(Value):
    """A source-local, field-addressable diagnostic."""

    code: str
    severity: Literal["error", "warning", "info"] = "error"
    location: str | None = None
    message: str


class Target(Value):
    """An accession-qualified, zero-based half-open interval."""

    target_id: Id
    contig: Label
    start: Coordinate
    end: Coordinate
    strand: Literal["+", "-", "."]


class Revision(Value):
    """Immutable analysis context; labels are separate cosmetic state."""

    revision_id: Id
    reference_id: Label
    profile_id: Label
    coordinate_system: Literal["0-based-half-open"] = "0-based-half-open"
    targets: Annotated[list[Target], Field(max_length=50)]


class RequestSnapshot(Value):
    """Local exchange, not an IRCOMP normalized specification."""

    kind: Literal["request"] = "request"
    format_version: Literal["1.0"] = "1.0"
    study_id: Id
    request_id: Id
    title: Label
    revision: Revision
    target_labels: dict[Id, Label]


class Metric(Value):
    """A source observation with explicit availability and interpretation metadata."""

    name: Label
    model: Text | None
    unit: Text | None
    scale: Text | None
    direction: Literal["higher", "lower", "not_ordered"] | None
    availability: Literal["present", "not_supplied", "unsupported", "failed", "unknown"]
    value: float | int | None


class CandidateKey(Value):
    """Bundle-scoped candidate identity, never inferred from a label."""

    bundle_id: Id
    candidate_id: Annotated[
        str,
        Field(min_length=1, max_length=100, pattern=r"^[A-Za-z0-9][A-Za-z0-9_.:-]*$"),
    ]


class Candidate(Value):
    """Immutable evidence with lossless original records retained separately."""

    candidate_id: Annotated[
        str,
        Field(min_length=1, max_length=100, pattern=r"^[A-Za-z0-9][A-Za-z0-9_.:-]*$"),
    ]
    target_id: Id
    label: Label
    metrics: Annotated[list[Metric], Field(max_length=20)]
    raw_record: dict[str, JsonValue]


class Source(Value):
    """Declared external producer; importing does not verify its execution."""

    name: Label
    version: Label
    uri: Annotated[str, Field(max_length=2000)] | None


class Dependency(Value):
    """External dependency declaration; never automatically fetched."""

    uri: Annotated[str, Field(min_length=1, max_length=2000)]
    description: Annotated[str, Field(min_length=1, max_length=1000)]


class EvidenceBundle(Value):
    """An immutable, exactly contextualized local evidence file."""

    kind: Literal["evidence"] = "evidence"
    format_version: Literal["1.0"] = "1.0"
    bundle_id: Id
    request_id: Id
    context: Revision
    category: Literal["synthetic", "computational_prediction"]
    source: Source
    candidates: Annotated[list[Candidate], Field(max_length=200)]
    dependencies: Annotated[list[Dependency], Field(max_length=100)]


class EvidenceFile(Value):
    """Original bytes and measured identity, separate from review decisions."""

    bundle: EvidenceBundle
    sha256: Annotated[str, Field(pattern=r"^[a-f0-9]{64}$")]
    content_base64: str


class Membership(Value):
    """One collection-specific decision over an immutable candidate."""

    candidate: CandidateKey
    disposition: Disposition
    rationale: Annotated[str, Field(max_length=4000)]
    evidence_refs: Annotated[list[CandidateKey], Field(max_length=100)]


class Collection(Value):
    """An explicitly revision-scoped many-to-many review collection."""

    collection_id: Id
    revision_id: Id
    name: Label
    memberships: Annotated[list[Membership], Field(max_length=1000)]


class TargetDraft(Value):
    """Unapplied strings; invalid values remain recoverable."""

    target_id: Id | None
    label: Text
    contig: Text
    start: Text
    end: Text
    strand: Text


class DecisionDraft(Value):
    """Unapplied review buffer stored independently from accepted decisions."""

    collection_id: Id
    candidate: CandidateKey
    disposition: Disposition
    rationale: Annotated[str, Field(max_length=4000)]
    evidence_refs: Annotated[list[CandidateKey], Field(max_length=100)]


class DraftBuffers(Value):
    """At most one editor buffer per substantive module."""

    target: TargetDraft | None = None
    decision: DecisionDraft | None = None


class Study(Value):
    """The local aggregate saved atomically; no compiler products are synthesized."""

    study_id: Id
    request_id: Id
    title: Label
    active_revision_id: Id
    revisions: Annotated[list[Revision], Field(min_length=1, max_length=200)]
    target_labels: dict[Id, Label]
    evidence: Annotated[list[EvidenceFile], Field(max_length=10)]
    collections: Annotated[list[Collection], Field(max_length=20)]
    draft_buffers: DraftBuffers
