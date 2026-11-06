# IRCOMP-GUI

Local CRISPR Study Workspace for preparing analysis requests and reviewing
imported computational evidence. Prepare edits reference context and interval
targets. Review manages candidate collections, dispositions and reasons. Export
produces a saved request or review package.

## Run

Python >=3.12 and Node >=20.19 are required. From the repository root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip install --no-build-isolation --no-deps -e .
npm --prefix web ci
npm --prefix web run build
.venv/bin/ircomp-gui
```

Open [127.0.0.1:8000](http://127.0.0.1:8000). **Inspect sample request** opens
labelled synthetic data. Interactive API documentation is at `/docs`; the schema
is at `/openapi.json`. Use `--port 8001` for another port. For client development,
run the service on port 8000 and `npm --prefix web run dev` on port 5173.

## Local data

**Apply** accepts an edit; **Save study** writes accepted values and separate
unapplied editor text to `~/.local/share/ircomp-gui/workspace.sqlite3`.
`IRCOMP_GUI_DATABASE` selects another SQLite file. **Undo** restores one unsaved
accepted action. Restarting the service loses unsaved sessions and previews.

Use one server process and one browser tab per study. A local lock serializes
operations and SQLite saves one complete snapshot. There is no multi-tab conflict
resolution: the latest explicit Save replaces the saved study. The save counter
labels snapshots; request revision IDs identify the context of evidence.
After a connection error, refresh working state and inspect accepted changes
before retrying. `IRCOMP_GUI_WEB` can select a separately built client directory.

## Source and documentation

- `src/ircomp_gui/domain`: values and rules.
- `src/ircomp_gui/application`: Prepare/Review/Save/import/export services.
- `src/ircomp_gui/adapters` and `api`: SQLite, JSON and HTTP.
- `web/src`: React views, shared reducer, selectors and controller.
- [Architecture and API](docs/architecture.md).
- [Exchange schema, catalogue and examples](contracts/README.md).
- [Wireframes](docs/design/README.md), [report](docs/report/README.md),
  [submission checklist](docs/submission.md).

Research notes, the future IRCOMP mapping and historical checks are in the
[IRCOMP Confluence GUI section](https://viridisquercusnova.atlassian.net/wiki/spaces/IRCOMP/pages/29360129).
Code, executable contracts and build configuration remain here. The application
runs without Confluence or an installed IRCOMP compiler. YAML editing, compilation,
execution and biological validation are outside this version.

The draft/code were prepared with AI assistance; simplifying the implementation
does not change that provenance. Actual contribution and acceptability under the
course rules remain to review. Real interviews and report identification fields
are still pending. External dependencies retain their own licences.
