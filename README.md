# IRCOMP-GUI

Local workspace for preparing explicit CRISPR analysis requests and reviewing
imported computational evidence. The ITU project focuses on editable request
data, explainable validation, evidence context and persistent review decisions.

**Status:** research and repository scaffold. No runnable GUI, HTTP service,
scientific execution or released IRCOMP adapter is implemented yet.

## Project notes

| Area | Entry point |
| --- | --- |
| Scope and two application modules | [S1 scope](docs/research/s1-scope.md) |
| User problems and source evidence | [S2 desk research](docs/research/s2-desk-research.md) |
| Pending primary research | [Interview plan](docs/research/s2-interview-plan.md) |
| Existing applications and design lessons | [S3 comparison](docs/research/s3-competitive-analysis.md) |
| UI design and wireframes | [S4 design](docs/design/README.md) |
| Runtime boundaries and repository ownership | [Architecture](docs/architecture/overview.md) |
| Conventions and verification | [Development](docs/development/README.md) |
| Course milestones and remaining work | [ITU checklist](docs/tasks/itu-phase-i.md) |

## Development layout

- `src/ircomp_gui/`: Python application package; service/model implementation
  belongs here, outside visual components.
- `web/`: planned React/TypeScript client; implementation boundary documented,
  dependencies and application code pending UI design.
- `tests/`: verification strategy; suites added with behavior.
- `docs/`: research, architecture decisions, development notes and task records.

The Python package has no runtime dependencies yet. `pyproject.toml` defines the
package and initial quality settings. There is deliberately no command that
pretends to launch an unfinished application.

## Relationship to IRCOMP

[IRCOMP](https://github.com/viridisquercus/IRCOMP) owns the scientific/compiler
work. This repository owns the course GUI and its local application model.
Future integration goes through an explicit adapter and accepted contracts.
Importing evidence does not assert that this application executed or verified
the external analysis. Synthetic examples must remain labelled.
