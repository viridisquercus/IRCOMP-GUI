# IRCOMP-GUI

Local CRISPR Study Workspace for preparing analysis requests and reviewing imported
computational evidence. **Prepare** edits reference/profile context and interval
targets. **Review** records collection membership, dispositions and rationale over
immutable evidence. **Export** produces identified saved snapshots.

The local model/API and key React GUI are implemented. Primary interviews and the
final submission review remain pending. Scientific execution, YAML editing and
the IRCOMP compiler adapter are outside this version.

## Install and run

Tested on Linux with Python 3.14.6, Node 20.20.2 and npm 10.8.2. The package requires
Python >=3.12 and Node >=20.19; other environments have not been verified.
From the repository root, or the extracted `IRCOMP-GUI` archive directory:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.lock
.venv/bin/python -m pip install --no-build-isolation --no-deps -e .
npm --prefix web ci
npm --prefix web run build
.venv/bin/ircomp-gui
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000), then choose **Inspect sample
request** for the labelled synthetic example. The Python service serves both
`web/dist` and `/api/v1`. Interactive API documentation is at `/docs`, generated
OpenAPI at `/openapi.json`. Select another port with `--port 8001`.

For frontend development, run the service on port 8000 and
`npm --prefix web run dev`; Vite uses port 5173 and proxies `/api`.
Run only one Python worker: working sessions and previews are process-local.
Installation downloads the pinned dependencies; no credentials or environment
files are needed. `requirements-dev.lock` pins the Python development environment;
`web/package-lock.json` pins the client. External libraries retain their licences.

## Data and recovery

Explicit **Save** persists accepted data and separate unapplied editor buffers in
`~/.local/share/ircomp-gui/workspace.sqlite3`. `IRCOMP_GUI_DATABASE` selects a
different SQLite file. A server restart loses unsaved sessions and previews.
Browser reload may reconnect to a live session; unsubmitted typing has no
guaranteed recovery. Opening a saved study creates a separate working copy;
version checks prevent it silently overwriting a newer Save.

`IRCOMP_GUI_WEB` selects an already built client directory. An editable source
install finds `web/dist` automatically; a standalone backend wheel contains
contracts/examples but needs separately supplied web assets.

## Verify

```sh
.venv/bin/python scripts/development/check_contracts.py
.venv/bin/pytest -q
.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/pyright
npm --prefix web run build
npm --prefix web run format:check
npm --prefix web exec -- playwright install chromium
npm --prefix web test
```

Browser tests use a separate service on port 8765 and temporary SQLite data.
Failure traces stay in ignored `web/test-results`. They do not touch normal saved
studies. See [verification](docs/verification.md) for outcomes and limits.

## Documentation

| Subject | Record |
| --- | --- |
| GUI structure and editable wireframes | [Design](docs/design/README.md) |
| Layers and shared state | [Architecture](docs/architecture/overview.md) |
| Data and transitions | [Domain model](docs/architecture/domain-model.md) |
| Operations, HTTP and errors | [API](docs/architecture/api.md) |
| Exact exchange, provenance and persistence | [Exchange](docs/architecture/exchange-and-persistence.md), [contracts](contracts/README.md) |
| Future thesis integration and missing capabilities | [IRCOMP boundary](docs/architecture/ircomp-integration.md) |
| Research sources and pending real sessions | [Desk research](docs/research/s2-desk-research.md), [interview plan](docs/research/s2-interview-plan.md) |
| Phase I report and fill-in fields | [Report](docs/report/README.md) |
| Source archive and remaining submission work | [Submission](docs/submission.md) |

Source layout: `src/ircomp_gui` owns Python domain/services/adapters/HTTP; `web/src`
owns views, shared state and controllers; `contracts` owns local exchange examples
and reference metadata; `tests` and `web/e2e` exercise the implementation.

## Development conventions

Python uses typed signatures, four spaces, double quotes, LF, Google-style
docstrings and strict Pyright. Frozen Pydantic value models express local data
contracts; domain/application modules import neither FastAPI nor concrete SQLite
adapters. TypeScript uses strict types, two spaces, double quotes and Prettier.
State, selectors, transport and controllers stay outside visual feature modules.

Keep commits focused and recoverable. Check the diff and appropriate verification
before committing; publish completed increments to origin without rewriting shared
history. Keep research assumptions, implemented behavior and observed tests distinct.
