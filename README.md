# IRCOMP-GUI

Local workspace for preparing explicit CRISPR analysis requests and reviewing
imported computational evidence. The ITU project focuses on editable request
data, explainable validation, evidence context and persistent review decisions.

**Status:** local model/API and connected React GUI implemented; backend and
Chromium acceptance checks pass. Primary interviews remain pending.
Scientific execution and the future IRCOMP adapter are outside this runtime.

## Project notes

| Area | Entry point |
| --- | --- |
| Scope and two application modules | [S1 scope](docs/research/s1-scope.md) |
| User problems and source evidence | [S2 desk research](docs/research/s2-desk-research.md) |
| Pending primary research | [Interview plan](docs/research/s2-interview-plan.md) |
| Existing applications and design lessons | [S3 comparison](docs/research/s3-competitive-analysis.md) |
| UI design and wireframes | [S4 design](docs/design/README.md) |
| Architecture, state and complete operation specification | [S5 architecture](docs/architecture/overview.md) |
| Exchange schemas and example files | [Contracts](contracts/README.md) |
| IRCOMP specification ownership and missing integration capabilities | [Integration and gaps](docs/architecture/ircomp-integration.md) |
| Implementation criteria and observed checks | [S6 criteria](docs/architecture/s6-acceptance.md), [verification](docs/development/s6-verification.md) |
| Phase I report draft and fill-in fields | [S7 report](docs/report/README.md) |
| Conventions and verification | [Development](docs/development/README.md) |
| Course milestones and remaining work | [ITU checklist](docs/tasks/itu-phase-i.md) |

## Development layout

- `src/ircomp_gui/`: Python application package; service/model implementation
  belongs here, outside visual components.
- `web/`: connected React/TypeScript views, state/controllers, native lock and browser tests.
- `contracts/`: versioned exchange schema, catalogue and labelled fixtures.
- `tests/`: headless model/service, persistence, exchange and HTTP acceptance tests.
- `docs/`: research, architecture decisions, development notes and task records.

## Run locally

After setup, run `.venv/bin/ircomp-gui` from the repository root and open
[http://127.0.0.1:8000](http://127.0.0.1:8000).

For a new clone, follow the [installation and verification commands](docs/development/README.md).
The interface supports explicit Save/Undo, request round trips, atomic evidence
imports, collection-specific decisions and identified saved-snapshot exports.
Synthetic examples remain visibly labelled. Saved studies use local SQLite;
unsaved sessions remain in process memory.

## Relationship to IRCOMP

[IRCOMP](https://github.com/viridisquercus/IRCOMP) owns the scientific/compiler
work. This repository owns the course GUI and its local application model.
Prepare is the initial editor of a restricted subset of IRCOMP user intent.
Future formal-specification/YAML integration goes through a versioned adapter and
IRCOMP-owned accepted contracts; missing goals, policies and cartridge semantics
are recorded in the [gap register](docs/architecture/ircomp-integration.md).
Importing evidence does not assert that this application executed or verified
the external analysis. Synthetic examples must remain labelled.
