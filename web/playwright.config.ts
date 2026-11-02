// Project owner: Lukáš Dubšík; implementation review pending.
import { defineConfig } from "@playwright/test";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";

export default defineConfig({
  testDir: "./e2e",
  workers: 1,
  fullyParallel: false,
  timeout: 30000,
  use: {
    baseURL: "http://127.0.0.1:8765",
    viewport: { width: 1440, height: 1100 },
    trace: "retain-on-failure",
  },
  webServer: {
    command: `${resolve("../.venv/bin/python")} -m ircomp_gui --port 8765`,
    url: "http://127.0.0.1:8765/api/v1/catalogue",
    env: {
      IRCOMP_GUI_DATABASE: join(
        tmpdir(),
        `ircomp-gui-e2e-${process.pid}.sqlite3`,
      ),
    },
    reuseExistingServer: false,
  },
});
