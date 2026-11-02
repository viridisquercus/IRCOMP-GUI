# Local exchange contracts

Version: `1.0`, implemented local exchange contract. No released IRCOMP compiler
API is implied. The local GUI service is now implemented; its [runtime checks](../docs/verification.md)
are separate from structural artifact validation.

| File | Role |
| --- | --- |
| [exchange.schema.json](exchange.schema.json) | Closed request/evidence/review JSON envelopes; shared definitions |
| [catalogue.json](catalogue.json) | Exact supported reference metadata and profile bindings |
| [cases.json](cases.json) | Fixture schema expectations and later semantic acceptance expectations |
| [examples/](examples/) | Small labelled synthetic examples and intentional negative cases |
| [NCBI report](references/grch38-p14-assembly-report.txt) | Retrieved source for the 24 nuclear chromosome identifiers/bounds |

The schema `$id` is a stable identifier, not a promise that a website serves it.
All `$ref` values are local; checking these artifacts requires no network fetch.
Use a Draft 2020-12 validator with format checking enabled, including UUIDs.
Runtime-generated object IDs use canonical lowercase UUID spelling; use that
spelling in local exchange files. JSON Schema is only the structural layer; apply the
[semantic and transaction rules](../docs/architecture/exchange-and-persistence.md)
and [domain invariants](../docs/architecture/domain-model.md) before acceptance.

`evidence-context-mismatch.json` and `request-invalid-interval.json` intentionally
pass the schema. They must fail domain acceptance. Conversely, an empty candidate
list is valid and makes no assertion that a scientific search was run.
`evidence-valid.json` distinguishes a supplied zero from a missing score.
`review-draft.json` embeds its exact original bytes and digest, with an unresolved
review decision. All evidence examples are synthetic, never genomic results.

Request labels must exactly cover the exported revision's target IDs. A study may
retain more labels for historical targets; export projects only the chosen IDs.
Bundle candidate IDs must be unique within their bundle. Review package references,
raw-byte integrity, complete source closure and unresolved counts are semantic
obligations not fully expressible by this schema.

The reference catalogue is metadata only. The checked-in NCBI source report records
more sequences than the supported subset; extraction is limited to rows marked
`assembled-molecule` and location type `Chromosome`. No aliases, mitochondria,
patches or alternate loci are silently enabled. See provenance URL/hash in the
catalogue. Do not interpret matching metadata as sequence-content verification.

## Future formal-language integration

These schemas describe local workspace exchange only. IRCOMP owns the future
normalized specification schema and YAML language semantics. Do not add placeholder
compiler fields or treat local `format_version` as IRCOMP `contract_version`.
Supported YAML/GUI round trips must eventually preserve specification meaning;
unsupported constructs require diagnostics rather than lossy subset export.
See [the gap register and integration gates](../docs/architecture/ircomp-integration.md).
Current schema files and fixture meanings are unchanged by that architectural decision.

## Artifact verification

From the repository root, with `jsonschema` available:

```sh
python scripts/development/check_contracts.py
```

This checks schema validity, positive/negative fixture structural expectations,
embedded raw evidence hashes, and catalogue extraction against the recorded source
report. It does **not** run application semantics, HTTP handlers, SQLite saves or a
browser. See [runtime verification](../docs/verification.md) for those checks.
The installed `requirements-dev.lock` environment includes the checker dependencies.
