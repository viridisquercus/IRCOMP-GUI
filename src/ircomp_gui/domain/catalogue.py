"""Pinned reference metadata. Project owner: Lukáš Dubšík; review pending."""

from __future__ import annotations

from typing import Annotated

from pydantic import Field, JsonValue

from ircomp_gui.domain.errors import DomainError
from ircomp_gui.domain.models import Value


class Contig(Value):
    """Metadata only; sequence content is not verified."""

    accession: str
    label: str
    length: Annotated[int, Field(gt=0)]


class Reference(Value):
    """Explicit supported subset and source provenance."""

    reference_id: str
    category: str
    assembly: str | None
    contigs: list[Contig]
    provenance: dict[str, JsonValue] | None


class Profile(Value):
    """Declared intent, not a compiler policy or a scientific result."""

    profile_id: str
    reference_ids: list[str]
    nuclease: str
    pam: str
    intent: str


class Catalogue(Value):
    """The shipped, versioned catalogue used for local checks."""

    catalogue_version: str
    references: list[Reference]
    profiles: list[Profile]

    def reference(self, reference_id: str) -> Reference:
        """Resolve exact identity without inferring aliases."""
        for item in self.references:
            if item.reference_id == reference_id:
                return item
        raise DomainError(
            "REFERENCE_UNSUPPORTED",
            "Choose an exact supported reference.",
            "/reference_id",
        )

    def profile(self, profile_id: str, reference_id: str) -> Profile:
        """Resolve the exact supported reference/profile binding."""
        for item in self.profiles:
            if item.profile_id == profile_id and reference_id in item.reference_ids:
                return item
        raise DomainError(
            "PROFILE_UNSUPPORTED",
            "The profile is not supported for this reference.",
            "/profile_id",
        )
