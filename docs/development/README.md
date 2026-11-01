# Development

Status: scaffold; runtime toolchain installation pending first implementation.

## Conventions

Python follows the IRCOMP conventions adapted in `pyproject.toml`: typed public
signatures, four spaces, double quotes, LF, Google-style docstrings and strict
type checking. Avoid copying unrelated environment policies or host-specific
settings. Version declarations belong in native configuration; resolved dependency
locks are added with the actual toolchain, not copied from another project.

Documentation uses stable relative links, evidence dates, concise status labels,
and actionable TODOs. Source behavior, design interpretation and implemented
behavior remain separate. Research artifacts belong under `docs/research`;
decisions belong under `docs/architecture/decisions`.

## Verification

For documentation/scaffold changes: parse TOML, compile Python syntax without
writing tracked artifacts, resolve relative document links, and inspect the diff
for unintended files. No runtime test pass is claimed while no runtime exists.

With the development tools installed, use `ruff check .`, `ruff format --check .`
and `pyright`. Their configurations are present; the initial scaffold does not
pin or install these developer tools. Select reproducible versions when creating
the first development environment and record the lock and execution evidence.

Add tests for domain invariants, import failure atomicity, persistence and API
behavior with implementation. Frontend testing should verify interactions and
error recovery rather than mirror component markup. See [test strategy](../../tests/README.md).

## Next implementation checkpoint

1. Resolve S4 preparation/review flows and complete S2 primary research.
2. Freeze a minimal model/API/exchange contract for S5.
3. Select and lock the Python HTTP and frontend build tools.
4. Implement request creation/edit/save/reopen end-to-end, then evidence review.
5. Verify all declared model/API functions before the Phase I submission.
