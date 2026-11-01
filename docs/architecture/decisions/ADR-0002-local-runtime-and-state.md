# ADR-0002: Local web runtime, working copies and saved snapshots

Status: Selected for initial implementation

Date: 2026-11-01

## Context

Two editable workflows must work by Phase I, while the thesis compiler API remains
unreleased. Explicit Save and Undo in S4 require a distinction between typed text,
accepted working data and persisted data. Backend database complexity is not an
ITU scoring objective.

## Decision

- React + strict TypeScript, built with Vite; native asynchronous `fetch`.
- Reducer + Context for one shared presentation model. Feature controllers and
  selectors are separate modules. No additional state library initially.
- Python >=3.12 + FastAPI with strict request models; domain dataclasses and
  services independent of the HTTP framework. Uvicorn runs one process/worker.
- A server-side `WorkspaceSession` holds a working copy per opened tab. An opaque
  workspace ID and increasing version protect commands against stale state.
- Explicit Save atomically stores one versioned study JSON document in SQLite
  through stdlib `sqlite3`. Raw evidence bytes are embedded as base64 within that
  document, with digests. No ORM, distributed cache or separate blob filesystem.
- One-step Undo restores the previous accepted working snapshot; Save clears Undo.
- Local single-user operation on `127.0.0.1`. Production serves client assets and
  API from one origin. Development uses Vite's proxy to `/api`; no wildcard CORS.
  Check Host and browser Origin against the configured loopback origin; changing
  routes require JSON content type and reject foreign browser origins. No login UI.
- SQLite file location is configurable; default
  `~/.local/share/ircomp-gui/workspace.sqlite3`. It is never inside tracked source.

Dependency versions and native lockfiles are selected and verified when creating
the first runnable slice in S6. This ADR selects tools, not untested version pins.

## Alternatives and consequences

| Alternative | Reason not selected |
| --- | --- |
| Qt desktop | Viable, but switches away from the already selected web interaction design |
| All domain logic in browser | Makes later Python integration and headless domain reuse less direct |
| Auto-persist every edit | Conflicts with S4 explicit Save and makes invalid draft handling less clear |
| Normalized SQL schema for every observation | Adds migrations and joins without a demonstrated query need |
| Server session persisted after each command | Duplicates Save semantics; unnecessary for this bounded local app |
| Direct dependency on IRCOMP | Couples delivery to unfinished scientific contracts |

A crash can lose unsaved accepted edits and unsaved typed text. The interface must
state this plainly and warn before closing dirty work. Explicit Save can preserve
invalid editor strings separately from valid accepted domain data. No crash-safe
autosave is promised. Multiple tabs can open the same saved study; compare-and-save
prevents silent overwrites. The second tab must resolve a conflict explicitly.

Full snapshots and raw files are acceptable under the bounded limits in the
exchange specification. If measured scale later exceeds them, revisit storage
rather than silently increasing payloads. No real-time collaboration is implied.

## Technical references

Consulted 1 November 2026:

- [React reducer and Context](https://react.dev/learn/scaling-up-with-reducer-and-context):
  shared state update logic and propagation; the domain remains in Python.
- [FastAPI guide](https://fastapi.tiangolo.com/tutorial/): typed HTTP boundary,
  response models and application testing.
- [Python 3.12 sqlite3](https://docs.python.org/3.12/library/sqlite3.html): local
  persistence, explicit transaction behavior and bound SQL parameters.
- [JSON Schema 2020-12](https://json-schema.org/draft/2020-12): structural exchange
  constraints; cross-object and scientific checks require domain validation.
