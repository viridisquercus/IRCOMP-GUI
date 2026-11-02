# Local exchange, persistence and IRCOMP boundary

Status: local `1.0` exchange/persistence implemented and checked in S6;
no released compiler compatibility claim. See [verification](../verification.md).
See [schemas and fixtures](../../contracts/README.md) for exact structural fields.

## References and profiles

The checked-in [catalogue](../../contracts/catalogue.json) fixes two references:

- `demo-reference-v1`: synthetic `demo_contig`, length 10,000. It is not GRCh38.
- `grch38-p14-primary-v1`: assembly `GCF_000001405.40`, NCBI GRCh38.p14
  **24 nuclear assembled chromosomes only**, keyed by versioned RefSeq accessions.
  No mitochondrial, alternate, patch or unplaced sequences in this UI subset.
  This subset is explicit; it is not a claim to support every GRCh38 contig.

Lengths/accessions were extracted from the NCBI assembly report on 1 November
2026. The catalogue records source URL and SHA-256 of the retrieved report.
No FASTA was downloaded or checked. Bounds checks attest to catalogue metadata,
not agreement with any external FASTA file. Display accession with optional human
chromosome label, but accept only the accession in the exchange format.

Profiles are `demo-spcas9-ngg-v1` (demo reference only) and
`spcas9-ngg-preexperiment-v1` (GRCh38 subset only). Both declare SpCas9 / NGG and
pre-experiment intent; neither executes an algorithm or asserts biological safety.
Synthetic evidence may reference either context and stays labelled synthetic.
`computational_prediction` evidence is allowed only with the real reference/profile;
its external execution claims remain unverified by this application.

## Files and identity

All exchange files are UTF-8 JSON, exact `format_version: "1.0"`; schema uses
JSON Schema 2020-12. Reject unknown versions and unknown envelope fields. A local
version change is independent of database schema, package version and IRCOMP
contract version. No implicit migration or interpretation of a future version.

| Kind / suffix | Contents | Acceptance |
| --- | --- | --- |
| `request` / `.request.json` | Study/request IDs, title, one exact revision, target-label map | Preview, then open as a new unsaved study; identity conflict never overwrites |
| `evidence` / `.evidence.json` | Bundle ID, request ID, exact revision context, category, source, candidates, dependencies | Preview and attach to one selected retained revision |
| `review` / `.review.json` | Request snapshot, selected collections, source saved version, raw evidence files with hashes, status and unresolved count | Downloadable handover; review-package reimport is outside initial scope |

Request import/export round trip preserves supported values and IDs. It is not a
full workspace backup: other revisions, reviews and unapplied drafts are absent.
A request file must have at least one valid target. Import creates one retained
revision; request export may select any valid saved revision.

Exact evidence compatibility requires request ID plus deep equality of the
revision object: revision UUID, reference/profile IDs, convention and target IDs
with intervals/strands. Compare targets by UUID, ignoring array order. Labels are
not context. Unknown or missing context is rejected, not repaired. A historical
revision is acceptable only if explicitly selected at preview time.

Original file bytes are retained without normalization, hashed with SHA-256.
A bundle UUID already attached with the same digest and identical bytes is a
no-op; a different byte sequence using that UUID is a collision, even if only
formatting changed. A producer must use a new bundle UUID for changed output.
Re-parsing raw bytes must reproduce the stored bundle; raw fields never become
editable review fields. Raw record values may contain arbitrary JSON but are
rendered as escaped text and never used as executable input or fetched links.

## Review export closure

1. Select saved version, one revision and one or more collections belonging to it.
2. Include the exact request snapshot and all selected collections/memberships.
3. Include complete original bytes for each bundle referenced by a membership or
   its supporting evidence refs. Include all bundles for the revision when the
   selected collections have no memberships, so an empty-evidence handover remains
   explainable. Deduplicate by bundle UUID; no source record is truncated.
4. Store each as `{bundle_id, sha256, content_base64}`. The bundle's embedded
   dependencies list survives unchanged; no URL/path is fetched. The GUI summary
   counts their unique `(uri, description)` pairs and calls them external.
5. Recompute unresolved count: each undecided/needs-clarification membership,
   each other disposition with blank rationale, plus each empty selected
   collection contributes one. A membership contributes at most one.
6. Status `draft` iff unresolved count > 0, otherwise `reviewed`. Always display
   “Review bookkeeping complete; scientific conclusions not verified” for reviewed.
7. Encode JSON and freeze it with filename, length and digest for preview/download.

The JSON package is the single handover artifact; its top-level status, counts and
embedded provenance are the human-readable summary. No ZIP creation/extraction
or separate HTML-report dependency is needed. External raw data may still be
required to reproduce an external analysis; embedded evidence is not a complete
scientific run directory. Request export makes no execution/RunRecord claim.

## Limits and validation layers

Limits are contract choices for the local teaching application, not measured
performance results: 1 MiB decoded per import file; nesting depth 32; 50 targets,
200 candidates per bundle, 20 metrics per candidate, 10 bundles, 20 collections,
1,000 memberships across a study, 200 revisions, 20 MiB serialized saved snapshot
or generated review package. Metric numbers must be finite and JSON integers
used as coordinates must fit JavaScript's safe integer range. Exact message/body
limits are checked before buffering an unbounded request. Base64 overhead is
accounted for separately. Exports are checked against their final encoded size.

Validate in order: transport/byte limit → UTF-8/duplicate keys/depth/finite values →
version/schema → catalogue/intervals/unique IDs/references → selected context →
state limits → atomic acceptance. Schema alone cannot enforce uniqueness by ID,
end > start, contig bounds, cross-file references, raw-byte hashes or completeness
counts. S6 must implement all these semantic checks, not equate a schema pass
with an import ready for attachment.

## Durable storage

One SQLite table keeps the saved aggregate together:

```sql
CREATE TABLE studies (
    study_id TEXT PRIMARY KEY,
    request_id TEXT NOT NULL UNIQUE,
    saved_version INTEGER NOT NULL CHECK (saved_version > 0),
    title TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    document_json TEXT NOT NULL
);
```

Use `PRAGMA user_version = 1` for this database layout. Stored document:
`{storage_version: 1, study: Study}` with Study as in the API, except evidence entries
also include `content_base64`. Top-level row metadata must agree with the document.
UUID and reference integrity is domain-validated before Save and after Load. The
request revision graph is stored as retained snapshots, not mutable SQL rows.
No claim of SQL enforcing domain relationships is made.

Save under the workspace lock: capture accepted state + submitted drafts, validate
storage invariants/limits, begin explicit transaction, insert if expected saved
version is 0 or update with `WHERE study_id = ? AND saved_version = ?`; require
exactly one changed row, commit, then advance session versions and clear Undo.
Bind all SQL values as parameters. Uniqueness violation or zero changed rows means
conflict; rollback on all failures. Set transaction behavior explicitly rather
than relying on Python sqlite3 defaults. An exception before commit leaves the
previous saved row intact. Do not mark the client Saved before commit succeeds.

Reopen verifies storage version, envelope, digests, references and row metadata.
Unsupported/corrupt data produces an error without rewriting it. Future migrations
require a backup and explicit migration tests; no initial migration framework.
Single-row transactions avoid half-saved evidence/decisions. All bounded source
bytes are in the row, so no filesystem/SQLite two-phase commit is required.

## Future compiler mapping

[integration contract and gap register](ircomp-integration.md) define the complete
mapping obligations. The local exchange is a workspace/request format; it is not
IRCOMP's normalized specification, canonical IR, backend bundle or execution record.
The main IRCOMP repository owns its request schema and YAML semantics.

Current intervals/reference metadata are only part of possible `known_inputs`.
Exact cartridge version, explicit goals/deliverables, general constraints and AI
control are missing. A local profile must not silently supply these. A future
adapter either converts the complete supported specification with provenance or
returns blocking diagnostics. Unsupported constructs cannot disappear in a GUI
import/edit/export round trip. No compiler schema is duplicated here.

Future IRCOMP-compatible YAML is a distinct export kind, gated by an accepted
compiler schema/parser and mapping tests. Local `.request.json` and `.review.json`
remain unchanged. No `RunRecord`, planner status or scientific execution success
is synthesized; the compiler must perform its own authoritative validation.

Sources: [IRCOMP I/O design](https://github.com/viridisquercus/IRCOMP/blob/main/docs/architecture/contracts/input-output-error-contract.md),
[NCBI GRCh38.p14 assembly report](https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.40_GRCh38.p14/GCF_000001405.40_GRCh38.p14_assembly_report.txt).
The latter was retrieved directly; the catalogue records the inspected content hash.
