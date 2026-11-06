# Architecture and local API

The GUI has two editable modules, Prepare and Review, sharing one workspace.
React components display controlled inputs and dispatch intent to the controller.
The controller calls FastAPI with asynchronous fetch; the shared reducer replaces
accepted state from the response and updates dependent panels without reloading.
Python services own the study and rules. They do not import FastAPI or SQLite.

```text
React views -> controller + shared reducer -> fetch / FastAPI
                                            -> application services
                                            -> domain values and rules
                                            -> repository / exchange ports
                                               SQLite / JSON adapters
```

## State

- `Study`: request identity, retained request revisions, target labels, original
  evidence, review collections and separate editor buffers.
- `Revision`: reference, profile, coordinate convention and interval targets.
  Analytical edits create a revision; cosmetic labels do not. Old evidence keeps
  its original context and cannot silently become evidence for a new revision.
- `Session`: one working study, its last saved snapshot and one Undo snapshot.
  A single process-local reentrant lock serializes operations.
- React state mirrors accepted data and keeps navigation and typed text separate.
  A small editor counter preserves newer typing while an earlier Save returns.
  DOM attributes are not the accepted data model.

SQLite keeps one complete study per row. Save uses an ordinary transaction;
there is no expected-version protocol or multi-tab merge. The last explicit Save
wins. The database keeps its existing layout, so older saved studies still load.
The incrementing save counter identifies an export and is not a concurrency lock.
The version marker in stored JSON identifies its format, not a working session.

## HTTP

Routes below are under `/api/v1`. Detailed request/response types are generated
from `api/requests.py` at `/docs` and `/openapi.json`.

| Route | Purpose / body |
| --- | --- |
| GET `/catalogue`, `/studies` | Supported metadata and saved study list |
| POST `/workspaces` | Open source `new`, `saved`, `duplicate` or `request_import` |
| GET `/workspaces/{id}` | Current working snapshot |
| DELETE `/workspaces/{id}` | `{discard: true}`; close working copy, keep saved data |
| POST `/workspaces/{id}/commands` | `{draft_buffers, command}`; typed Prepare/Review operation |
| POST `/workspaces/{id}/save` | `{draft_buffers}`; save the complete study |
| POST `/workspaces/{id}/undo` | Restore the last accepted unsaved action |
| POST `/workspaces/{id}/validate` | `{revision_id, target_draft}`; local checks only |
| POST `/imports` | Base64 request/evidence bytes; evidence also names workspace and revision |
| DELETE `/imports/{id}` | Discard an import preview |
| POST `/exports` | `{study_id, revision_id, kind, collection_ids}` from saved data |
| GET `/exports/{id}/file` | Exact previewed JSON bytes |
| GET `/examples/{name}` | One of four labelled synthetic examples |

Prepare commands rename a study/target, apply/remove a target or explicitly
replace reference/profile context. Review commands attach evidence, create/rename/
remove collections, add/remove members and set a member's disposition, reason and
supporting references. Candidate identity combines bundle and candidate IDs.
One candidate can belong to several collections with independent decisions.

Input errors return `{error: {code, message, diagnostics}}`. Field diagnostics
include a location. Failed edits preserve accepted state; failed Save preserves
working edits. After a lost response, use Refresh before retrying. Imports check
schema and request context again at attachment. A duplicate bundle with identical
bytes is harmless; the same ID with different bytes is rejected.

Exports freeze bytes for later download and include the save counter and selected
request revision. Review packages preserve original evidence bytes and digests.
A complete review means bookkeeping is complete, not scientific validation.
Use one local worker and one tab per study; this is a standalone application.

## Future IRCOMP integration

[Integration mapping and F01–F10 gates](https://viridisquercusnova.atlassian.net/wiki/spaces/IRCOMP/pages/29392897)
remain planning, not an implemented adapter. IRCOMP owns the specification
language, goals/constraints, cartridge semantics, compiler and execution policy.
The GUI owns local editing and review. The local JSON format is not an IRCOMP
normalized request. Any future adapter must preserve supported meaning and return
diagnostics for unsupported constructs instead of silently dropping them.
