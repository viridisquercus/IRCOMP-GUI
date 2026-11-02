# S6 implementation and acceptance plan

Status: declared local model/API operations and connected Prepare/Review/Export
implemented. [S6 verification](../development/s6-verification.md) records observed
backend/browser checks and their limits. The original acceptance criteria below
remain the implementation contract, not an exhaustive claim about all inputs.

The [IRCOMP integration boundaries](ircomp-integration.md) apply throughout:
local validation remains local, source evidence is immutable and no compiler is
required to use the workspace. Future YAML/compiler/graph acceptance criteria are
tracked separately there; they do not add runtime features to this S6 checklist.

## Implementation sequence

1. Lock the runtime/build tools; implement catalogue, domain types, diagnostics,
   revision/interval rules and a headless service test. Add actual author headers
   according to the course rules after reviewing source ownership.
2. Implement sessions, create/open/rename/duplicate, SQLite Save, Undo and version
   conflicts. Connect Prepare end-to-end, including invalid strings and reopen.
3. Implement request round-trip, exact-byte evidence preview and atomic attachment,
   immutable observations, collection/member/decision operations. Connect Review.
4. Implement saved snapshot exports and download preview identity. Connect Export,
   error/loading/empty states and keyboard focus; run complete acceptance checks.
5. Review operation inventory against actual routes/OpenAPI and report actual
   source files. Package source only after checks pass. S2 interviews remain a
   separate outstanding course requirement.

## Observable acceptance criteria

| ID | Scope | Input / action | Required observation |
| --- | --- | --- | --- |
| A01 | Domain/API | New study, rename, duplicate | Fresh identities on duplication; no copied evidence or decisions |
| A02 | Prepare | Add/update/remove target | Correct new revision; old revisions intact; invalid Apply has no accepted effect |
| A03 | Prepare | Label-only edit / identical Apply | No scientific revision; relevant views still update |
| A04 | Domain | Zero, negative, boolean, fractional, overflowing/out-of-bounds coordinates | Exact diagnostics; zero start valid; end-exclusive semantics |
| A05 | Domain/API | Reference/profile change with invalid replacement target | Whole operation rejected; original context unchanged |
| A06 | Persistence/GUI | Save an invalid input buffer, reopen | Accepted target unchanged; exact draft string restored and labelled unapplied |
| A07 | Domain/GUI | Remove target/collection/member, Undo | Exact prior working state restored; evidence not deleted by review removal |
| A08 | Persistence | Induce write failure / second-tab stale Save | Durable snapshot unchanged; working edits retained; no false Saved state |
| A09 | Exchange/API | Export request, import in clean database | Supported fields and IDs preserved; conflict cannot overwrite existing study |
| B01 | Exchange | Valid evidence + empty evidence | Both parse; empty means no records supplied, not a successful negative search |
| B02 | Exchange/API | Malformed/duplicate-key/oversize/future-version input | Rejected before acceptance; all previous state byte-equivalent |
| B03 | Domain/API | Same bundle ID same bytes / changed bytes | No duplicate vs explicit collision, respectively |
| B04 | Domain | Schema-valid reference/context mismatch | Attachment blocked; expected/received context shown |
| B05 | Domain/GUI | Change target, then review old evidence | Old revision remains visible; evidence cannot attach to new revision |
| B06 | Review | Candidate in two collections; edit one decision | Other collection decision unchanged; details/counts/export update reactively |
| B07 | Review | Create/rename/remove collections; add/remove members | Every operation works; missing membership removal is safe no-op |
| B08 | Evidence | Present score zero; absent/unsupported/failed/unknown score | Five meanings remain distinct; no synthetic zero or aggregate confidence |
| B09 | Domain/API | Dangling candidate/supporting ref or wrong-revision membership | Rejected atomically; source record unchanged |
| B10 | Concurrency | Change workspace after import preview | Stale preview rejected; fresh preview required |
| E01 | Export | Undecided, clarification, blank rationale, empty collection | Exact unresolved count; draft status; no biological approval label |
| E02 | Export | Select subset of collections | Complete source byte closure with valid hashes; other collections absent |
| E03 | Export/API | Save again after export preview | Existing download bytes/hash unchanged; new preview uses new saved version |
| E04 | Export | Dirty editor, export last saved | Explicit saved identity and omitted-draft notice; no unsaved values leak in |
| E05 | Persistence | Corrupt stored bytes / unsupported storage version | Load fails safely without rewriting data |
| U01 | GUI | Type during Save; delayed response | Newer typed characters remain dirty and visible |
| U02 | GUI | Keyboard-only correction → review → Save → export | Labels/focus/error links usable; relevant panels update without page reload |
| U03 | API/service | Run operations headlessly | Same domain results as GUI; no component/DOM dependency |

Runtime tests assert preserved state, source bytes and observable interactions.
The S5 checker still covers structural artifacts only. Actual semantic/HTTP/SQLite
and browser evidence is linked in the verification record; future integration
features and primary user validation are outside those observed checks.

## Demonstration path

Create two targets → correct invalid interval → Save → request export → compatible
synthetic import → create a collection and decide with rationale → reject mismatch
→ revise target and inspect old evidence → Save/reopen → draft review export.
Use synthetic labels throughout. The checkpoint is three minutes plus the live
architecture/GUI demonstration; rehearse timing separately after implementation.
