"""Bounded local JSON exchange. Project owner: Lukáš Dubšík; review pending."""

from __future__ import annotations

import base64
import binascii
import hashlib
import json
import math
from collections.abc import Iterator, Mapping
from typing import Protocol, cast

from jsonschema import Draft202012Validator, FormatChecker
from pydantic import JsonValue, ValidationError

from ircomp_gui.domain.catalogue import Catalogue, resource_path
from ircomp_gui.domain.errors import DomainError
from ircomp_gui.domain.models import (
    EvidenceBundle,
    EvidenceFile,
    RequestSnapshot,
    Study,
)
from ircomp_gui.domain.rules import validate_bundle, validate_revision

MAX_FILE = 1024 * 1024
MAX_DOCUMENT = 20 * 1024 * 1024


def _pairs(pairs: list[tuple[str, JsonValue]]) -> dict[str, JsonValue]:
    result: dict[str, JsonValue] = {}
    for key, value in pairs:
        if key in result:
            raise DomainError("DUPLICATE_KEY", "JSON contains a duplicate object key.")
        result[key] = value
    return result


def _nonfinite(value: str) -> None:
    raise DomainError("SCHEMA_INVALID", "Nonfinite numbers are not supported.")


def parse_json(raw: bytes, *, limit: int = MAX_FILE) -> dict[str, JsonValue]:
    """Decode one bounded, finite, duplicate-free object with bounded nesting."""
    if len(raw) > limit:
        raise DomainError("LIMIT_EXCEEDED", "Input exceeds the supported byte limit.")
    try:
        document = json.loads(
            raw.decode("utf-8"), object_pairs_hook=_pairs, parse_constant=_nonfinite
        )
    except (ValueError, UnicodeError, RecursionError) as error:
        raise DomainError(
            "MALFORMED_JSON", "Choose a valid UTF-8 JSON object."
        ) from error
    if not isinstance(document, dict):
        raise DomainError("SCHEMA_INVALID", "The file must contain a JSON object.")
    stack: list[tuple[JsonValue, int]] = [(document, 1)]
    while stack:
        value, depth = stack.pop()
        if depth > 32:
            raise DomainError("LIMIT_EXCEEDED", "JSON nesting exceeds 32 levels.")
        if isinstance(value, dict):
            stack.extend((child, depth + 1) for child in value.values())
        elif isinstance(value, list):
            stack.extend((child, depth + 1) for child in value)
        elif isinstance(value, float) and not math.isfinite(value):
            raise DomainError("SCHEMA_INVALID", "Nonfinite numbers are not supported.")
    return cast("dict[str, JsonValue]", document)


def decode_base64(content: str) -> bytes:
    """Bound encoded data before decoding it; reject invalid base64."""
    if len(content) > 4 * ((MAX_FILE + 2) // 3):
        raise DomainError("LIMIT_EXCEEDED", "Import files must be at most 1 MiB.")
    try:
        raw = base64.b64decode(content, validate=True)
    except (binascii.Error, ValueError) as error:
        raise DomainError("INVALID_BASE64", "File encoding is invalid.") from error
    if len(raw) > MAX_FILE:
        raise DomainError("LIMIT_EXCEEDED", "Import files must be at most 1 MiB.")
    return raw


def encode_json(document: Mapping[str, object]) -> bytes:
    """Create reproducible finite JSON, checking its final byte size."""
    raw = (
        json.dumps(document, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    ).encode("utf-8")
    if len(raw) > MAX_DOCUMENT:
        raise DomainError("LIMIT_EXCEEDED", "The resulting document exceeds 20 MiB.")
    return raw


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
