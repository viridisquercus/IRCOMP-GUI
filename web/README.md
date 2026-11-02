# Web client

React/TypeScript/Vite client with Prepare, Review and Export. The Python service
owns accepted data and SQLite persistence. State, selectors and asynchronous
controllers live in `src/app/`; visual feature modules render controlled values
and dispatch intent. No scientific execution or compiler dependency is included.

## Build and run

With the Python environment installed from the repository root:

```sh
npm ci
npm run build
```

Then run `.venv/bin/ircomp-gui` from the repository root and open
[the local workspace](http://127.0.0.1:8000). The service serves `web/dist` and its
API from the same origin. For development, run the Python service and `npm run dev`
separately; Vite proxies `/api` to port 8000.

`npm run typecheck` checks strict TypeScript. `npm run format:check` checks the
client style. `npx playwright install chromium` installs the browser used by
`npm test`; build first. Tests start their own server on port 8765 with a fresh
SQLite database in the OS temporary directory. They never use the normal study
database. Browser artifacts stay in ignored `test-results/`.

See [development instructions](../docs/development/README.md), the
[state contract](../docs/architecture/domain-model.md) and
[API inventory](../docs/architecture/api.md). Synthetic fixtures are visibly
labelled and retain their fixed request context; the app does not patch them to
pretend compatibility with arbitrary studies.
