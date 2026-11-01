# Web client

Planned React/TypeScript client for Prepare, Review and Export. No client build
or application exists yet. Add `package.json`, a resolved lockfile and executable
build/check commands with the first runnable slice after S4.

Keep accepted request/review state outside visual components. Feature views may
own transient form buffers and focus; domain truth and persistence belong to the
Python service. Async transport must expose loading, error and unsaved states.

Planned feature allocation is in the [architecture overview](../docs/architecture/overview.md).
Use shared components only where multiple concrete consumers exist. No disabled
Run button or artificial scientific progress state belongs in the initial GUI.
