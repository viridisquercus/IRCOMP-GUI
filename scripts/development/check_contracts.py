"""Check S5 structural artifacts and retained source bytes."""

from __future__ import annotations

import base64
import hashlib
import json
from pathlib import Path
from typing import Any, cast

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2] / "contracts"


def read_object(path: Path) -> dict[str, Any]:
    """Read a contract artifact expected to contain an object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected object: {path.name}")
    return cast("dict[str, Any]", value)


def check_cases(validator: Draft202012Validator) -> int:
    """Check declared structural outcomes and raw files inside review fixtures."""
    cases = json.loads((ROOT / "cases.json").read_text(encoding="utf-8"))
    for case in cases:
        document = read_object(ROOT / "examples" / case["file"])
        valid = validator.is_valid(document)
        if valid != case["schema_valid"]:
            raise ValueError(f"Unexpected schema outcome: {case['file']}")
        if document["kind"] == "review" and valid:
            for evidence_file in document["evidence_files"]:
                raw = base64.b64decode(evidence_file["content_base64"], validate=True)
                if hashlib.sha256(raw).hexdigest() != evidence_file["sha256"]:
                    raise ValueError("Embedded evidence hash does not match")
                evidence = json.loads(raw)
                validator.validate(evidence)
                if evidence["bundle_id"] != evidence_file["bundle_id"]:
                    raise ValueError("Embedded bundle ID does not match")
                original = (ROOT / "examples" / "evidence-valid.json").read_bytes()
                if raw != original:
                    raise ValueError("Review fixture changed the original source bytes")
    return len(cases)


def check_catalogue() -> int:
    """Recompute the pinned chromosome subset from the retained NCBI report."""
    catalogue = read_object(ROOT / "catalogue.json")
    reference = next(
        item
        for item in catalogue["references"]
        if item["reference_id"] == "grch38-p14-primary-v1"
    )
    report = (ROOT / "references" / "grch38-p14-assembly-report.txt").read_bytes()
    if hashlib.sha256(report).hexdigest() != reference["provenance"]["sha256"]:
        raise ValueError("Reference report hash does not match catalogue provenance")
    expected = []
    for line in report.decode("utf-8").splitlines():
        if line.startswith("#"):
            continue
        fields = line.split("\t")
        if fields[1] == "assembled-molecule" and fields[3] == "Chromosome":
            expected.append(
                {
                    "accession": fields[6],
                    "label": f"chr{fields[2]}",
                    "length": int(fields[8]),
                }
            )
    if len(expected) != 24 or expected != reference["contigs"]:
        raise ValueError("Catalogue differs from the declared 24-chromosome subset")
    return len(expected)


def main() -> None:
    """Verify only the artifact checks documented in the contracts README."""
    schema = read_object(ROOT / "exchange.schema.json")
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    cases = check_cases(validator)
    contigs = check_catalogue()
    print(f"Schema valid; {cases} fixture outcomes; embedded source bytes verified.")
    print(f"NCBI source hash and {contigs} chromosome records verified.")
    print("Runtime semantics, HTTP, persistence and browser behavior: not tested.")


if __name__ == "__main__":
    main()
