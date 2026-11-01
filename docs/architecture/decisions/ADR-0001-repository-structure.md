# ADR-0001: Repository structure and implementation boundaries

Status: Selected for the initial scaffold

Date: 2026-11-01

## Context

IRCOMP-GUI is a separate repository with a Python application boundary and a
planned web client. The sibling IRCOMP repository uses `src/`, focused `docs/`
areas, numbered ADRs, typed Python and directories populated by concrete work.
The course application needs its own runtime and data model without copying the
compiler's environment stack or claiming an implemented integration.

## Decision

Keep root Python packaging, `src/ircomp_gui`, a `web` client boundary, `tests`, and
research/architecture/development/task documentation. Create deeper runtime
packages with their first implementation, not as an empty directory tree.

Adapt the sibling's four-space Python indentation, double quotes, 88-column
formatting, Google-style public docstrings and strict typing. Prefer `pathlib`,
explicit types and domain-specific errors. Frontend conventions are provisional:
strict TypeScript, two-space indentation, double quotes and feature-oriented files.
Pin actual frontend tooling when the first runnable slice is implemented.

Research notes distinguish observations, source claims and interpretation. They
use neutral project documentation and review TODOs, not conversational handoffs.
Historical standalone notes are incorporated as working records with corrected
repository links. No interview, test, author approval or scientific result is
created by changing prose style.

## Alternatives

| Option | Assessment |
| --- | --- |
| Separate GUI repository with focused client and Python package | Selected: independent course delivery and clear future adapter |
| Add GUI directly to IRCOMP | More coupling to the scientific work and its unfinished contracts |
| Generate a large monorepo skeleton and all tools immediately | Premature dependencies and empty abstractions before UI/model design |

## Consequences

The first implementation must make a complete vertical operation work across
client, service and persistence. No copied Conda locks, Docker stack, CI badges or
placeholder success endpoints. Tool versions and CI become authoritative when
selected and verified in this repository.
