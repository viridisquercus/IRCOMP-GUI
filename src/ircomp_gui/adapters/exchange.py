"""Bounded local JSON exchange. Project owner: Lukáš Dubšík; review pending."""

from __future__ import annotations

import base64
import hashlib
import json
from collections.abc import Iterator, Mapping
from typing import Protocol, cast

from jsonschema import Draft202012Validator, FormatChecker
from pydantic import ValidationError

from ircomp_gui.adapters.resources import resource_path
from ircomp_gui.domain.catalogue import Catalogue
from ircomp_gui.domain.errors import DomainError
from ircomp_gui.domain.models import (
    EvidenceBundle,
    EvidenceFile,
    RequestSnapshot,
    Study,
)
from ircomp_gui.domain.rules import validate_bundle, validate_revision
from ircomp_gui.domain.serialization import decode_base64, parse_json


class SchemaValidator(Protocol):
    """Narrow typed surface around jsonschema's dynamically overloaded validator."""

    def iter_errors(self, instance: object) -> Iterator[object]:
        """Yield structural violations."""
        ...

    def validate(self, instance: object) -> None:
        """Reject a structurally invalid generated document."""
        ...


class Exchange:
    """Own wire parsing and measured byte identities, not scientific semantics."""

    def __init__(self, catalogue: Catalogue) -> None:
        self.catalogue = catalogue
        schema = json.loads(
            resource_path("exchange.schema.json").read_text(encoding="utf-8")
        )
        self.validator = cast(
            "SchemaValidator",
            Draft202012Validator(schema, format_checker=FormatChecker()),
        )

    def decode(self, raw: bytes, kind: str) -> RequestSnapshot | EvidenceBundle:
        """Require both the structural schema and local semantic rules."""
        document = parse_json(raw)
        if document.get("format_version") != "1.0":
            raise DomainError(
                "VERSION_UNSUPPORTED", "Only local exchange version 1.0 is supported."
            )
        if document.get("kind") != kind:
            raise DomainError("SCHEMA_INVALID", f"Choose a {kind} file.")
        errors = list(self.validator.iter_errors(document))
        if errors:
            raise DomainError(
                "SCHEMA_INVALID", "The file does not match the local exchange schema."
            )
        try:
            if kind == "request":
                request = RequestSnapshot.model_validate(document)
                validate_revision(
                    request.revision, self.catalogue, require_targets=True
                )
                if set(request.target_labels) != {
                    target.target_id for target in request.revision.targets
                }:
                    raise DomainError(
                        "DANGLING_REFERENCE",
                        "Request labels must cover its target identities exactly.",
                    )
                return request
            bundle = EvidenceBundle.model_validate(document)
            validate_bundle(bundle, self.catalogue)
            return bundle
        except ValidationError as error:
            raise DomainError(
                "SCHEMA_INVALID", "The file contains unsupported field values."
            ) from error

    def verify_sources(self, study: Study) -> None:
        """Check original bytes, hashes and parsed contents on save/load."""
        for item in study.evidence:
            raw = decode_base64(item.content_base64)
            decoded = self.decode(raw, "evidence")
            if decoded != item.bundle or hashlib.sha256(raw).hexdigest() != item.sha256:
                raise DomainError(
                    "SCHEMA_INVALID",
                    "Stored evidence bytes, digest or parsed contents disagree.",
                )

    def evidence_file(self, raw: bytes, bundle: EvidenceBundle) -> EvidenceFile:
        """Preserve exact source bytes; no reserialization of imported evidence."""
        return EvidenceFile(
            bundle=bundle,
            sha256=hashlib.sha256(raw).hexdigest(),
            content_base64=base64.b64encode(raw).decode("ascii"),
        )

    def validate_document(self, document: Mapping[str, object]) -> None:
        """Validate a generated local exchange document through the adapter port."""
        self.validator.validate(document)
