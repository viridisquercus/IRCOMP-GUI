# Web client

Planned React/TypeScript client for Prepare, Review and Export. No client build
or application exists yet. Add `package.json`, a resolved lockfile and executable
build/check commands with the first runnable slice in S6. The selected stack is
React/TypeScript/Vite, with a FastAPI service and SQLite persistence.

Keep state in the shared reducer/Context presentation model, outside view files.
Controlled views display draft strings and dispatch intent; feature controllers
call the API asynchronously. Accepted domain truth belongs to server workspace
sessions; explicit Save persists the complete study in SQLite. Keep newer typed
text when a delayed response arrives. See the [state contract](../docs/architecture/domain-model.md)
and [API operation inventory](../docs/architecture/api.md).

Planned feature allocation is in the [architecture overview](../docs/architecture/overview.md).
Use shared components only where multiple concrete consumers exist. No disabled
Run button or artificial scientific progress state belongs in the initial GUI.
