# Application and HTTP API

Status: local model/API implemented, prefix `/api/v1`; browser integration
verification in progress. Runtime OpenAPI is available at `/openapi.json`.
This is the operation inventory for S6, including less visible operations from S1.
FastAPI generates the request/command interface from strict runtime models.
This document records operation semantics alongside that generated interface.

All operations here are local workspace services. In particular, local
`validate_request` is not IRCOMP's compiler-side operation of the same logical
name. Compiler invocation, YAML conversion and graph editing are absent from this
API version. The [integration boundary](ircomp-integration.md) specifies future
ownership, source-labelled diagnostics and conversion failures; extending runtime
routes/types requires a separate accepted interface change.


## Types and common behavior

IDs are UUID strings unless explicitly bundle-local candidate IDs. JSON object
fields are closed, numbers finite, and booleans are not integers. Optional fields
are explicitly nullable or have a stated default; reject other unknown fields.
No silent conversion of HTTP body types. File import uses exact base64 bytes,
not a browser-parsed/re-serialized JSON object.

`CandidateKey = {bundle_id: UUID, candidate_id: string}`.
`Diagnostic = {code: string, severity: "error"|"warning"|"info",
location: string|null, message: string}`; location is a JSON Pointer into the
logical input or null. UI focus mapping uses the pointer/code, not English text.

`DraftBuffers = {target: TargetDraft|null, decision: DecisionDraft|null}` as in
[domain model](domain-model.md). DecisionDraft additionally carries
`evidence_refs: CandidateKey[]`. DraftBuffers are included with every changing
workspace command and Save so the server can retain/Undo the corresponding input.
On successful Apply/remove, the relevant submitted buffer is cleared by the
service; other buffers survive. Failed operations leave client buffers intact.

`WorkspaceView = {workspace_id, version, base_saved_version, dirty, can_undo,
study, diagnostics}`. Study serializes `study_id`, `request_id`, `title`,
`active_revision_id`, `revisions: Revision[]`, `target_labels: {UUID: string}`,
`evidence: {bundle: EvidenceBundle, sha256: string}[]`,
`collections: Collection[]`, `draft_buffers: DraftBuffers`. Revision,
EvidenceBundle and Collection have the exact shapes in the exchange schema.
Raw file bytes are kept server-side and omitted from this view.
`dirty` compares the working snapshot to the last saved snapshot; the client ORs
this with unsent draft changes. Diagnostics/readiness are derived, not persisted
as proof of previous validation.

Every successful changing operation returns the complete WorkspaceView. Controllers
replace the accepted mirror, preserve newer client draft generations and publish
`workspaceReceived` to the reducer. State events remain local React actions;
there is no WebSocket event bus or background scientific progress.

## HTTP routes

All bodies below are JSON. `w` denotes a workspace UUID. Success status is 200
unless listed otherwise. Mutating service operations are atomic under a session
lock. Request file parsing/preview never changes a study.

| Route | Body / service method | Response |
| --- | --- | --- |
| GET `/catalogue` | `get_catalogue()` | Reference and profile catalogue, limits and supported format versions |
| GET `/studies` | `list_studies()` | `{studies: [{study_id,title,saved_version,updated_at}]}` from durable data |
| POST `/workspaces` | Discriminated sources below; `create/open/duplicate/import_request` | 201 WorkspaceView |
| GET `/workspaces/{w}` | `get_workspace(w)` | WorkspaceView |
| DELETE `/workspaces/{w}` | `{expected_version, discard: true}`; `close_workspace` | 204; closes session/previews only, never deletes saved study |
| POST `/workspaces/{w}/commands` | `{expected_version, draft_buffers, command}`; dispatch below | WorkspaceView |
| POST `/workspaces/{w}/validate` | `{revision_id, target_draft: TargetDraft|null}`; `validate_request` | `{workspace_version,revision_id,export_ready,checks,diagnostics}`; draft problems reported separately |
| POST `/workspaces/{w}/save` | `{expected_version, expected_saved_version, draft_buffers}`; `save_workspace` | WorkspaceView after durable commit |
| POST `/workspaces/{w}/undo` | `{expected_version}`; `undo` | WorkspaceView; restores submitted draft buffers too |
| POST `/imports` | ImportPreviewInput below; `preview_import` | 201 ImportPreview, including blocked previews |
| DELETE `/imports/{preview_id}` | `cancel_import` | 204; unknown/already-cancelled preview also 204 |
| POST `/exports` | ExportSelection below; `prepare_export` | 201 ExportPreview with immutable download identity |
| GET `/exports/{export_id}/file` | `download_export` | Exact previewed bytes, `application/json`, attachment filename |

POST `/workspaces` bodies are a closed union:

- `{source: "new", title}`: default demo reference/profile and empty target list.
- `{source: "saved", study_id}`: read durable data, create a fresh session/version.
- `{source: "duplicate", workspace_id, expected_version, title}`: copy active
  request as specified in the model. Existing workspace remains unchanged.
- `{source: "request_import", preview_id}`: accept a ready request preview into
  a new unsaved session, preserving exported study/request/revision/target IDs.

If imported study ID already exists durably, return `IDENTITY_EXISTS` with its
study ID; offer Open existing or explicit Duplicate after opening it. If the same
request ID exists under another study ID, reject `IDENTITY_CONFLICT`. Never merge
or overwrite a saved study through import. Concurrent unsaved imports may exist
as separate sessions; first Save wins and the other receives a version conflict.

## Module A — Prepare commands

`command` has `type` plus exactly the payload fields shown. Services return a new
snapshot or diagnostics; components contain no accepted-state mutation rules.

| Type / service method | Payload | Domain effect / GUI consumers |
| --- | --- | --- |
| `rename_study` / `rename_study` | `title` | Cosmetic; shell and study list after Save |
| `apply_target` / `apply_target` | `draft: TargetDraft` | Null target ID adds; existing ID edits; parse/validate complete target set, new revision only for analysis change; list, problem panel, context strip |
| `remove_target` / `remove_target` | `target_id` | New active revision without target; retain historical evidence/labels; list and export readiness |
| `set_context` / `set_context` | `reference_id, profile_id, targets: Target[]` | Atomic new context + complete replacement intervals; exact same target ID set as active revision; no implicit conversion; context strip and diagnostics |
| `rename_target` / `rename_target` | `target_id, label` | Cosmetic label map; list/details; no new revision |

`apply_target` uses the submitted draft's label as well as interval fields. If
only label changes it behaves as `rename_target`. A completely unchanged command
is a no-op. The service clears the applied draft on success; clearing a non-null
buffer is itself a workspace change even if analysis data is unchanged.
`set_context` cannot add/remove targets, so IDs remain traceable. Add/remove are
separate intents. Active target removal is confirmed using its visible label. `apply_target` and
`remove_target` address active targets only; `rename_target` may rename any target
retained in the study, including a historical one.

Validation response `checks` is an array of
`{name, status: "passed"|"failed"|"not_performed", message}`. Required local
checks and explicitly unperformed scientific checks are listed in the model.
Selecting an older revision changes client navigation only; all edits target the
active revision. Export accepts an explicit saved revision ID.

## Module B — Review commands

| Type / service method | Payload | Domain effect / GUI consumers |
| --- | --- | --- |
| `attach_evidence` / `attach_evidence` | `preview_id` | Revalidate exact context under lock; store bytes/parsed bundle and default collection if needed; evidence list, candidate panel and summaries |
| `create_collection` / `create_collection` | `revision_id, name` | Fresh UUID, empty membership; collection navigation and export selection |
| `rename_collection` / `rename_collection` | `collection_id, name` | Collection name only; selection and export summary |
| `remove_collection` / `remove_collection` | `collection_id` | Remove membership/decisions with collection; evidence unchanged; confirm name/count |
| `add_member` / `add_member` | `collection_id, candidate: CandidateKey` | Add undecided membership, or no-op if already present; many-to-many relation |
| `remove_member` / `remove_member` | `collection_id, candidate: CandidateKey` | Remove membership and decision only; missing membership is no-op |
| `set_decision` / `set_decision` | `collection_id, candidate: CandidateKey, disposition, rationale, evidence_refs: CandidateKey[]` | Membership must exist; update review layer; detail, row status and unresolved count |

Collection names need not be globally unique; IDs select them. All candidate and
supporting references must resolve to attached evidence for the collection's
revision. Missing/broken references fail; a blank rationale produces incomplete
state, not an invalid import. Decisions are never written into raw evidence. `set_decision` clears the submitted
decision draft after acceptance, preserving any newer client draft generation.

### Import preview/accept

`ImportPreviewInput` is one of:

- `{kind: "request", content_base64}`.
- `{kind: "evidence", workspace_id, expected_version, revision_id,
  content_base64}`. Revision may be active or retained historical context.

`ImportPreview = {preview_id, kind, status, diagnostics, summary}` where status is
`ready`, `blocked` or `duplicate`. Summary contains available request/revision/
reference/profile/category/bundle IDs and candidate counts, using null where
parsing failed. Include expected/received context for mismatches; never display
untrusted filenames/HTML as markup. Whole-file malformed JSON still gets a blocked
preview if transport/base64/size parsing succeeded. Transport failures return the
common error envelope.

A preview is immutable process memory, owned by its workspace for evidence, with
its creation version and bytes. Accept requires the same workspace version as
preview creation; on intervening changes return `PREVIEW_STALE` and preview again.
Previews live until cancellation, acceptance, workspace close or server restart.
Keep at most five pending previews globally; reject additional ones with
`LIMIT_EXCEEDED` and offer cancellation. Accepted previews are consumed. Duplicate
same-ID/same-byte evidence returns an unchanged snapshot on acceptance (and consumes
the preview); same-ID/different-bytes is blocked. No partial attachment.

### Export selection/preview/download

`ExportSelection = {study_id, saved_version, revision_id, kind,
collection_ids}` where kind is `request` or `review`; collection_ids is an empty
array for request and a nonempty unique UUID array for review. Use only a durable
snapshot whose saved version exactly matches; stale selection fails. All selected
collections must belong to that revision. Review needs at least one attached
bundle for that revision, including a valid empty bundle.

`ExportPreview = {export_id, filename, sha256, byte_length, study_id,
saved_version, revision_id, kind, review_status, target_count, candidate_count,
collection_count, unresolved_count, dependency_count}`. review_status is null for
request, otherwise `draft` or `reviewed`. `reviewed` means review bookkeeping is
complete, not approved biological evidence. The preview freezes bytes in memory;
a later Save cannot change an existing download. Retain at most five exports
(FIFO eviction); missing/evicted export returns `PREVIEW_EXPIRED`, regenerate it.
Server restart also requires regeneration. Download errors do not mutate a study.

When the editor is dirty, explicitly Save/Apply or choose **Export last saved**.
Show the selected saved version; do not silently drop unsaved work. A saved draft
buffer does not enter exports and must be disclosed as excluded in the GUI.

## Failure contract

`{error: {code, message, diagnostics: Diagnostic[]}, workspace_version: int|null}`.
No source bytes, host paths or stack traces in public errors. Invalid JSON and
validation errors are normalized to this envelope at the HTTP adapter.

| HTTP | Codes | Recovery |
| --- | --- | --- |
| 400 | `MALFORMED_JSON`, `DUPLICATE_KEY`, `INVALID_BASE64` | Correct input; no accepted change |
| 404 | `NOT_FOUND`, `SESSION_EXPIRED`, `PREVIEW_EXPIRED` | Reopen durable study / recreate preview |
| 409 | `WORKSPACE_CONFLICT`, `SAVE_CONFLICT`, `PREVIEW_STALE`, `IDENTITY_EXISTS`, `IDENTITY_CONFLICT`, `BUNDLE_ID_COLLISION`, `UNDO_UNAVAILABLE` | Refresh/repreview or explicit conflict choice; preserve working state |
| 413 | `LIMIT_EXCEEDED` | Explain supported limit and reduce input |
| 422 | `SCHEMA_INVALID`, `VERSION_UNSUPPORTED`, `REFERENCE_UNSUPPORTED`, `PROFILE_UNSUPPORTED`, `CONTEXT_MISMATCH`, `INTERVAL_INVALID`, `DANGLING_REFERENCE`, `EXPORT_NOT_READY` | Field/context diagnostics; fix actual source |
| 503 | `PERSISTENCE_UNAVAILABLE` | Retain work and Retry Save |
| 500 | `INTERNAL_ERROR` | Correlated server log, retain visible state; no success claim |

Browser-origin rejection uses HTTP 403 `ORIGIN_REJECTED`. Missing or wrong route
fields use `SCHEMA_INVALID`. Imported files also fail on nonfinite numbers,
duplicate JSON keys and unsupported format version before any acceptance.

## Public service interfaces

`WorkspaceService`: create, open, list, get, duplicate, close, save, undo.
`PrepareService`: rename_study, apply_target, remove_target, set_context,
rename_target, validate_request, preview_request, accept_request.
`ReviewService`: preview_evidence, attach_evidence, create/rename/remove_collection,
add/remove_member, set_decision.
`ExportService`: prepare_export, download_export.

Repository port: `list()`, `load(study_id)`,
`save(study, expected_saved_version) -> saved_version`.
Exchange port: `decode_request(bytes)`, `decode_evidence(bytes)`,
`encode_request(snapshot) -> bytes`, `encode_review(snapshot, collection_ids) -> bytes`.
Inject UUID generation/clock at the application boundary for deterministic tests.
These interfaces can be called without HTTP or React; they are owned here, not
asserted to be the compiler's interface.

## Runtime support route

GET `/examples/{name}` downloads one of four bounded, labelled source fixtures
(request, compatible evidence, empty evidence or mismatched evidence). It does not
generate scientific results or rewrite their fixed request context.
