# S6 verification record

Date: 2026-11-02. Local editing/review runtime; no IRCOMP compiler, scientific run,
primary research session or measured user-usability result is asserted here.

## Observed checks

| Check | Result / scope |
| --- | --- |
| Python acceptance | 33 passed: headless domain/services, SQLite save/reopen/conflicts/corruption, parser/import/export, HTTP boundary and inward dependency enforcement |
| Strict typing | Pyright: zero errors/warnings |
| Python style | Ruff lint and formatter checks pass |
| Exchange artifacts | Schema + nine structural fixture expectations, original evidence bytes, NCBI source hash and 24 chromosome records pass |
| Client | Strict TypeScript and Vite production build pass; Prettier checks pass |
| Chromium | Seven complete browser workflows pass against the built client and real local API |
| Source reproducibility | `npm ci` + production build from a clean Git archive |
| Backend packaging | sdist → wheel build; independently installed wheel resolves catalogue/schema/examples and responds through its HTTP API |
| Visual review | Prepare, Review and Export screenshots inspected; no clipped controls in the tested layouts |

One upstream Starlette TestClient warning reports its deprecated HTTPX integration.
HTTP tests run successfully with the pinned toolchain; this is not a runtime
application error. No warning filter suppresses it.

## Browser workflow coverage

1. Open sample through actual request preview, inspect checks, import evidence,
   distinguish numeric zero from absence, add membership, record rationale, Save,
   export a draft package, verify downloaded source hash and reopen decisions.
2. Save an invalid draft without changing accepted values; reload it; type during
   a delayed Save and verify newer text remains visible and unsaved.
3. Keyboard entry/focus; explicit reference/context replacement; no horizontal
   page overflow at the tested 390 px viewport.
4. Import arbitrary fresh request/bundle identities; maintain independent decisions
   for one candidate in two collections; rename/remove membership/Undo; revise a
   target, reject old evidence for the new revision and recover the old review.
5. Link an invalid-interval diagnostic to its field; correct it; simulate a failed
   Save and verify retained values and successful retry.
6. Lose a command response after server acceptance; prevent replay until refresh,
   retain typed text and reconcile with the one accepted target.
7. Export the last saved request after accepting a newer unsaved revision; verify
   the download contains saved values and the working copy stays unsaved.

The tests use synthetic examples or explicitly generated synthetic test fixtures,
never real genomic results. Source observations remain immutable. The UI does not
rewrite fixture request IDs to force compatibility. Basic text/action contrast was
checked (body on white 11.79:1, muted text on background 4.74:1, white/teal 6.61:1);
this is not a complete accessibility audit or cross-browser certification.

## Coverage against the S5 acceptance matrix

[S6 criteria](../architecture/s6-acceptance.md) remain the specification. The
following describes exercised behavior rather than claiming exhaustive input coverage.

| Criteria | Evidence |
| --- | --- |
| A01–A03 | Creation/rename/duplication; add/update/remove, cosmetic/no-op revision behavior; Undo |
| A04–A05 | Invalid coordinate strings, safe range/bounds/zero and explicit atomic reference changes; strict HTTP models |
| A06–A09 | Saved draft strings, recovery, failed/stale Save and request round trip/identity collisions |
| B01–B05 | Empty/invalid/oversized inputs, duplicate/collision/stale previews, compatibility and retained historical evidence |
| B06–B10 | Collection-specific decisions, create/rename/remove/member operations, all five metric availability states, dangling/supporting references and stale previews |
| E01–E03 | Draft bookkeeping, selected collection/source closure, original byte hashes and frozen export downloads |
| E04–E05 | Last-saved export excludes unsaved revisions; stored version/digest corruption rejected without repair |
| U01–U03 | Delayed-save typing, representative keyboard/focus paths and headless use of the same services |

Tests live in [test_workspace.py](../../tests/test_workspace.py) and
[workspace.spec.ts](../../web/e2e/workspace.spec.ts). Exact commands and installation
steps are in [Development](README.md).

## Runtime screenshots

All three show synthetic data from an automated Chromium session.

- [Prepare](screenshots/s6-prepare.png): accepted interval, shared context and checks.
- [Review](screenshots/s6-review.png): immutable observations and a separate decision.
- [Export](screenshots/s6-export.png): identified draft package and download metadata.

## Limits and remaining work

This record does not establish crash/power-loss durability, every assistive
technology, other browser/OS support, biological validity or scientific reference
sequence availability. Browser reload and server restart have different recovery
limits; see [Development](README.md). Local capacity limits remain deliberate.

S2's two primary sessions, report/authorship review, final source archive and Moodle
upload remain outstanding. S6 completes the declared local API/model and connected
GUI foundation; it does not complete all course submission tasks. Future YAML,
compiler and graph operations remain under [ADR-0003](../architecture/decisions/ADR-0003-ircomp-specification-boundary.md).
