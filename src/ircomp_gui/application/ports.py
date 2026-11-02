"""Application persistence boundary. Project owner: Lukáš Dubšík; review pending."""

from typing import Protocol

from ircomp_gui.domain.models import Study, Value


class SavedStudy(Value):
    """One verified durable version."""

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

    def save(self, study: Study, expected_saved_version: int) -> int:
        """Atomically compare and save, or preserve the preceding version."""
        ...

    def identity_exists(self, study_id: str, request_id: str) -> str | None:
        """Return a colliding durable study ID if either identity exists."""
        ...
