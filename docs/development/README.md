# Development

Status: S6 local model/API and React client implemented. See the
[verification record](s6-verification.md) for observed checks and their limits.
IRCOMP compiler integration and primary user research remain separate work.

## Install from source

Tested environment: Linux, CPython 3.14.6, Node 20.20.2 and npm 10.8.2.
The package targets Python >=3.12; Vite requires Node >=20.19. The recorded run did
not test other Python versions, operating systems or browsers.

From the repository root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.lock
.venv/bin/python -m pip install --no-build-isolation --no-deps -e .
npm --prefix web ci
npm --prefix web run build
.venv/bin/ircomp-gui
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000). The one-process Python service
serves the built client and API. Runtime OpenAPI is at `/openapi.json`; interactive
API documentation is at `/docs`. A different local port can be selected with
`--port 8001`.

For frontend development, leave the Python service on port 8000 and run
`npm --prefix web run dev`. Vite serves the client on port 5173 and proxies `/api`.
Do not enable multiple Uvicorn workers: unsaved workspaces/previews are process-local.

`requirements-dev.lock` pins the complete observed Python runtime/development
environment, excluding the editable project itself. Runtime dependencies are also
pinned in `pyproject.toml`; `web/package-lock.json` is the native frontend lock.
No environment files or credentials are needed.

## Persistence and recovery

Default database: `~/.local/share/ircomp-gui/workspace.sqlite3`.
`IRCOMP_GUI_DATABASE` selects a different SQLite file; `IRCOMP_GUI_WEB` can select
an already built client directory. Normal use from this editable source checkout
finds `web/dist` automatically. A standalone backend wheel includes its schema,
catalogue and source examples, but not built web assets; supply `IRCOMP_GUI_WEB`
when serving a separately installed wheel.

Explicit Save persists accepted data and separate unapplied editor buffers. A
server restart loses unsaved working sessions and previews. Browser reload can
reconnect to the session ID in session storage; typing since the last submitted
buffer is not guaranteed to survive. Open saved study creates another working
copy; stale durable versions cannot overwrite a newer Save. Unsaved conflict
resolution offers explicit reopen or request-only duplication.

## Verification commands

```sh
.venv/bin/python scripts/development/check_contracts.py
.venv/bin/pytest -q
.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/pyright
npm --prefix web run build
npm --prefix web run format:check
cd web
npx playwright install chromium
npm test
```

Browser tests start a separate server on port 8765 and use a fresh database under
the OS temporary directory. They do not touch normal saved studies. Failed traces
and screenshots go to ignored `web/test-results/`; three selected synthetic-data
screenshots are retained in the verification record.

For packaging, `.venv/bin/python -m build --no-isolation` builds an sdist and wheel
using the installed build tools. The source install above must be complete first.
The standalone contract checker covers structural artifacts/provenance only;
pytest and Playwright exercise runtime behavior. Downloaded reference provenance
uses Git attributes to retain exact bytes and its recorded hash.

## Conventions and next work

Python: typed signatures, four spaces, double quotes, LF, Google-style docstrings,
strict Pyright. Strict frozen Pydantic value models provide shared structural
validation; domain rules/services import neither FastAPI nor SQLite. The mutable
session coordinator uses a dataclass and serialized replace-on-success operations.
TypeScript: strict types, two spaces, double quotes and Prettier. State, selectors,
transport and controllers are outside visual feature modules.

Follow [working changes](../../CONTRIBUTING.md) for recoverable commits and
publication. Research, intended design and implemented/tested behavior remain
explicitly distinguished. Before assessed packaging, review source ownership,
required author labels and the actual report text. The
[S6 matrix](../architecture/s6-acceptance.md) links the original contract to this
implementation; [IRCOMP integration gates](../architecture/ircomp-integration.md)
remain deferred. User sessions, final report, submission packaging and presentation
preparation are still tracked in the [course checklist](../tasks/itu-phase-i.md).
