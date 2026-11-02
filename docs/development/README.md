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

The S5 artifact checker is `python scripts/development/check_contracts.py`
(requires `jsonschema`). It verifies schema/fixture outcomes, embedded source
bytes and the pinned reference catalogue. It is not a runtime test suite.
Downloaded provenance files use an explicit Git attribute to preserve exact
bytes; verify their digests from a Git archive as well as the working tree.

## Next implementation checkpoint

1. Use the [S5 specification](../architecture/overview.md) as the implementation
   contract; refine needs separately through the two pending S2 sessions.
2. Lock and verify the selected React/TypeScript/Vite and Python/FastAPI toolchain.
3. Implement request creation/edit/save/reopen end-to-end, then evidence review.
4. Implement the complete operation inventory, persistence and export rules.
5. Verify the [S6 acceptance criteria](../architecture/s6-acceptance.md) before
   claiming the Phase I code requirement complete.

## Version control and design artifacts

Follow [working changes](../../CONTRIBUTING.md) for logical commits and publication.
[S4 wireframes](../design/README.md) are generated design artifacts, not the runtime client.
