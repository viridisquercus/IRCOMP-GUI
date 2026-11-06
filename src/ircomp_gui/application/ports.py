"""Application persistence boundary. Project owner: Lukáš Dubšík; review pending."""

from collections.abc import Mapping
from typing import Protocol

from ircomp_gui.domain.models import (
    EvidenceBundle,
    EvidenceFile,
    RequestSnapshot,
    Study,
    Value,
)


class SavedStudy(Value):
    """One verified saved snapshot."""

    study: Study
    saved_version: int
    updated_at: str


class StudySummary(Value):
    """Study selector metadata from durable data."""

    study_id: str
    title: str
    saved_version: int
    updated_at: str


class Repository(Protocol):
    """Storage operations owned by the application, not the HTTP layer."""

    def list(self) -> list[StudySummary]:
        """Return saved study summaries."""
        ...

    def load(self, study_id: str) -> SavedStudy:
        """Load and verify one saved aggregate."""
        ...

    def save(self, study: Study) -> int:
        """Save one snapshot atomically and return its save counter."""
        ...

    def identity_exists(self, study_id: str, request_id: str) -> str | None:
        """Return a colliding durable study ID if either identity exists."""
        ...


class ExchangePort(Protocol):
    """Versioned local exchange boundary owned by application use cases."""

    def decode(self, raw: bytes, kind: str) -> RequestSnapshot | EvidenceBundle:
        """Decode a supported request/evidence file without accepted side effects."""
        ...

    def verify_sources(self, study: Study) -> None:
        """Require matching original bytes, hashes and parsed observations."""
        ...

    def evidence_file(self, raw: bytes, bundle: EvidenceBundle) -> EvidenceFile:
        """Retain complete original evidence bytes and measured provenance."""
        ...

    def validate_document(self, document: Mapping[str, object]) -> None:
        """Require a generated document to match the supported exchange schema."""
        ...
