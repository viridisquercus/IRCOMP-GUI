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
| Implementation order and acceptance criteria | [S6 plan](docs/architecture/s6-acceptance.md) |
| Conventions and verification | [Development](docs/development/README.md) |
| Course milestones and remaining work | [ITU checklist](docs/tasks/itu-phase-i.md) |

## Development layout

- `src/ircomp_gui/`: Python application package; service/model implementation
  belongs here, outside visual components.
- `web/`: planned React/TypeScript client; implementation boundary documented,
  runtime dependencies and application code pending S6.
- `contracts/`: versioned exchange schema, catalogue and labelled fixtures.
- `tests/`: verification strategy; runtime suites added with behavior.
- `docs/`: research, architecture decisions, development notes and task records.

The Python package has no runtime dependencies yet. `pyproject.toml` defines the
package and initial quality settings. There is deliberately no command that
pretends to launch an unfinished application.

## Relationship to IRCOMP

[IRCOMP](https://github.com/viridisquercus/IRCOMP) owns the scientific/compiler
work. This repository owns the course GUI and its local application model.
Prepare is the initial editor of a restricted subset of IRCOMP user intent.
Future formal-specification/YAML integration goes through a versioned adapter and
IRCOMP-owned accepted contracts; missing goals, policies and cartridge semantics
are recorded in the [gap register](docs/architecture/ircomp-integration.md).
Importing evidence does not assert that this application executed or verified
the external analysis. Synthetic examples must remain labelled.
