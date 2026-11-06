# IRCOMP-GUI

### Name: Lukas (Viridis) Dubsik
### Login: xdubsil00
### Project: IRCOMP
### School-Project: ITU-1

## Overview

IRCOMP-GUI is a local application for preparing CRISPR analysis requests and
reviewing imported results. It is the first GUI prototype for IRCOMP and the
project for ITU. The application uses Python for its data and operations, with
React and TypeScript for the interface.

The application is divided into **Prepare**, **Review** and **Export**. Prepare
sets the reference and interval targets. Review adds candidates to collections
and stores decisions about them. Export writes a request or a review package
from the saved study. No CRISPR computation is performed by this application.

## Temporary checklist

Phase I files are due in Moodle on **6 November 2026 at 23:59**. The checkpoint
presentation is in the regular lab slot in the week starting **9 November 2026**.
This is the working list of remaining actions; remove it after completing them.

- [ ] Fill in the regular lab day and time: **________________**.
- [ ] Conduct and record P01/P02. Add the participant role, relevant experience,
  date, duration, setting, consent, recent task and materials used. Keep observed
  steps separate from recollection and opinion.
- [ ] Evaluate the sessions: record needs, conflicting findings and existing
  solutions that work. Link N1-N8 to the actual P01/P02 findings and update the
  competitor comparisons, interface design, task scenarios and priorities.
- [ ] Review the [contribution record](ai-audit.md) against the course rules for
  larger generated sections. Record a course-staff exception only if granted.
- [ ] Update the [report text](docs/report/phase-i.md) and editable document with
  the findings and lab details. Export the PDF and check every page, contents
  entry, figure and author heading.
- [ ] After the final edits, run `make check` and affected browser scenarios with
  `make test`, commit the changes and run `make pack` from the clean checkout.
- [ ] Upload `00_xdubsil00_navrh.pdf` and `00_xdubsil00_source.zip` under the personal
  Moodle account and confirm that Moodle records the submission.
- [ ] Prepare the checkpoint demonstration: both modules, an interval correction,
  compatible and mismatching evidence, a collection decision, Save/reopen, Undo
  and export. Explain shared state, the model/API boundary and the source code.
- [ ] Attend the checkpoint presentation in the regular lab slot.

## Installation and execution

Python 3.12 or newer and Node 20.19 or newer are required. The checked environment
uses Python 3.14.6, Node 20.20.2 and npm 10.8.2 on Linux.

From the project directory, run:

```sh
make install
make build
make run
```

This creates `.venv`, installs the Python package and downloads the web
dependencies. The application is then available at
[http://127.0.0.1:8000](http://127.0.0.1:8000). To select another port, use
`.venv/bin/ircomp-gui --port 8001`.

The same installation can be done without Make:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip install --no-build-isolation --no-deps -e .
npm --prefix web ci
npm --prefix web run build
.venv/bin/ircomp-gui
```

For frontend development, start the Python service on port 8000 and run
`npm --prefix web run dev`. Vite starts on port 5173 and forwards API calls to
Python. The HTTP documentation is at `/docs`, and the generated API schema is
at `/openapi.json`.

## Using the application

### Prepare

To try the application, press **Inspect sample request**, then **Open request**.
The example is synthetic and already contains an interval target. Alternatively,
create a study through **New / Open / Rename / Duplicate**.

Select a target to edit it, or use **Add target** for a new one. Coordinates use
zero-based, end-exclusive intervals: start 100 and end 200 describe 100 bases.
**Apply target** checks the input and changes the request. An edit to coordinates
creates a new request revision; changing the label alone keeps the same revision.

**Check request** lists the local checks. The application checks known reference
identifiers and chromosome lengths. It does not check a FASTA file or calculate
biological suitability.

### Review

The Review view displays evidence from the selected request revision. Import an
evidence file or inspect the synthetic example. Check the preview before
attaching it. A file with a different request or revision is refused.

Select a candidate and add it to a collection. Its disposition, reason and
supporting references are stored in that collection. The same candidate can
belong to more than one collection, with a different decision in each one.
Original scores stay unchanged. A score of zero is different from a value that
was not supplied.

### Save and export

**Apply** changes the working study. **Save study** stores it in SQLite, together
with any unapplied editor text. **Undo** restores one accepted unsaved change.
After saving, the Undo copy is cleared.

Export uses saved data. Select a request or review package, inspect the preview,
then download the JSON file. Unfinished decisions produce a draft review package.
The review package includes the original evidence bytes and their checksums.
Unapplied editor text is kept for recovery but is excluded from export.

## Implementation

The Python code is under `src/ircomp_gui`. `domain` defines the data and checks,
`application` handles operations, `adapters` reads and writes data, and `api`
connects these functions to HTTP. The React components are under `web/src`.
The reducer stores shared client state; visual components dispatch changes to it.

[Architecture](docs/architecture.md) describes the classes and API.
[File formats](contracts/README.md) describes the JSON exchange.
[Wireframes](docs/design/README.md) and the [design report](docs/report/README.md)
contain the interface design. Longer research notes and future integration work
are in [IRCOMP Confluence](https://viridisquercusnova.atlassian.net/wiki/spaces/IRCOMP/pages/29360129).

## Code checks

The runtime stays small, but code checks are kept strict. To install and run them:

```sh
make install-dev
make check
```

This runs Ruff linting and formatting checks, strict Pyright, strict TypeScript
and Prettier, including the Cypress source and test runner. Use `make format` to
apply formatting. Python uses typed functions,
four spaces and double quotes. TypeScript uses two spaces and double quotes.
The configuration is in `pyproject.toml`, `web/tsconfig.json` and
`web/.prettierrc.json`.

## Browser tests

Run `make test` after installation. It builds the client, starts a separate local
server and runs 11 Cypress scenarios against a temporary SQLite database. Your
saved studies are not used. The server and temporary database are removed when
the run finishes.

The tests cover editing, draft recovery, Undo, imports, collection decisions,
review downloads and failed or delayed requests. Use
`npm --prefix web run test:e2e:open` after building to work in the Cypress window.
See [testing](docs/testing.md) for the scenarios and failure simulation.

## Local storage and limitations

Saved studies are stored in `~/.local/share/ircomp-gui/workspace.sqlite3`.
`IRCOMP_GUI_DATABASE` selects another database; `IRCOMP_GUI_WEB` selects an already
built client directory. Restarting the service loses unsaved working copies and
previews. Browser reload can reconnect while the same service is running, but
unsubmitted typing has no guaranteed recovery.

Use one process and one browser tab per study. A local lock orders operations,
and SQLite saves a complete study in one transaction. There is no multi-tab
merge: the latest explicit Save wins. After a connection error, use **Refresh
working state** and check what was accepted before repeating the operation.

YAML editing, the IRCOMP compiler, workflow graphs and scientific execution are
future work. The local JSON format is not the IRCOMP specification language.
The remaining Phase I work is listed in the temporary checklist above.

## Libraries and source information

The application uses FastAPI, Pydantic, Uvicorn, jsonschema, React and Vite.
Hatchling and editables are used for Python installation. External dependencies
retain their licences. The catalogue includes NCBI reference metadata and keeps
its original source report and checksum.

Code and documentation were developed with substantial AI assistance, including
core functionality. The [contribution record](ai-audit.md) describes its scope.
