# Architecture overview

Status: Planned application boundaries; scaffold only.

## Application responsibilities

Prepare edits requests and targets. Review imports evidence and stores a separate
layer of collection membership, decisions and rationale. Export produces an
identified request/review snapshot. Scientific computation remains external.

The planned local web implementation uses React/TypeScript and asynchronous HTTP
calls to Python application services. SQLite is the initial persistence proposal.
No server framework, frontend dependency lock or scientific adapter has been
selected by installing packages at this stage.

## Dependency direction

```text
web views → client application state → HTTP transport
                                       ↓
                              application use cases
                                       ↓
                                 domain model
                                       ↑
                         persistence / evidence adapters
```

HTTP handlers translate requests and errors; they do not own domain rules.
Application services coordinate operations and persistence. Domain code must not
import a UI framework, HTTP framework or database driver. Adapters implement
interfaces owned by the application boundary. Accepted source observations remain
immutable; reviewer decisions are separate state.

| Planned location | Responsibility | Create with |
| --- | --- | --- |
| `src/ircomp_gui/domain/` | Request/target identity, review rules, diagnostics | First implemented model and unit tests |
| `src/ircomp_gui/application/` | Use cases and persistence ports | First complete edit/save operation |
| `src/ircomp_gui/adapters/` | SQLite, local exchange parser, future IRCOMP mapping | Concrete format/storage contract |
| `src/ircomp_gui/api/` | HTTP boundary and error translation | Selected framework and first route |
| `web/src/features/prepare/` | Target/request editing interaction | S4 preparation design |
| `web/src/features/review/` | Evidence inspection and editable decisions | S4 review design |
| `web/src/shared/` | Shared state/transport/accessibility primitives | Actual shared consumers |

These are allocation rules, not existing implementations. Avoid empty layer
packages and speculative abstractions. The selected structure is recorded in
[ADR-0001](decisions/ADR-0001-repository-structure.md).

## Invariants to preserve

- Matching display labels do not establish scientific identity.
- Missing, unsupported, failed and numeric zero are distinct.
- A source score remains associated with its source/model/context.
- An analysis-relevant request change does not relabel old evidence as current.
- Validation reports only checks actually performed.
- Save failures retain visible unsaved state and permit recovery.
- Import/export operates on arbitrary supported input, not hardcoded demo IDs.

TODO: freeze the minimal local exchange format after S4/S5; document compatibility
rules, error categories and persistence transactions before implementing imports.
