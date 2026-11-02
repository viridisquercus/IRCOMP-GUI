// Project owner: Lukáš Dubšík; implementation review pending.
import { test, expect, type Page } from "@playwright/test";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import type { Workspace } from "../src/shared/types";

async function start(page: Page) {
  await page.goto("/");
  await page.getByRole("button", { name: "Inspect sample request" }).click();
  await expect(
    page.getByRole("region", { name: "Import preview" }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Open request", exact: true }).click();
  await expect(
    page.getByRole("heading", { name: "Make the request explicit." }),
  ).toBeVisible();
}

async function save(page: Page) {
  await page.getByRole("button", { name: "Save study", exact: true }).click();
  await expect(page.locator(".save-status")).toContainText("Saved");
}

async function review(page: Page) {
  await page.getByRole("button", { name: "02 Review" }).click();
  await page.getByRole("button", { name: "Inspect synthetic example" }).click();
  await page
    .getByRole("button", { name: "Attach evidence", exact: true })
    .click();
  await expect(
    page.getByRole("heading", { name: "Synthetic candidate A" }),
  ).toBeVisible();
}

test("prepare, import, decide, save, reopen and download exact draft", async ({
  page,
}) => {
  await start(page);
  await page.getByRole("button", { name: /Demo target A/ }).click();
  await page.getByRole("button", { name: "Check request" }).click();
  await expect(
    page.getByText("IRCOMP specification and controller validation", {
      exact: false,
    }),
  ).toBeVisible();
  await review(page);
  await expect(page.locator(".metric-value")).toHaveText("0");
  await expect(page.locator(".metric-missing")).toHaveText("not supplied");
  await page
    .getByRole("button", { name: "Add to collection", exact: true })
    .click();
  await page
    .getByLabel("Disposition", { exact: true })
    .selectOption("needs_clarification");
  await page
    .getByLabel("Rationale", { exact: true })
    .fill("Independent expert review is pending.");
  await page
    .getByRole("button", { name: "Apply decision", exact: true })
    .click();
  await expect(
    page.getByText("1 members · 1 unresolved", { exact: true }),
  ).toBeVisible();
  await save(page);
  await page.getByRole("button", { name: "03 Export" }).click();
  await page.getByText("Review / evidence package", { exact: true }).click();
  await page.getByRole("checkbox", { name: /Review collection/ }).check();
  await page.getByRole("button", { name: "Preview saved export" }).click();
  await expect(
    page.getByRole("heading", { name: "Draft review", exact: true }),
  ).toBeVisible();
  const downloading = page.waitForEvent("download");
  await page.getByRole("link", { name: "Download draft review" }).click();
  const downloaded = await downloading;
  const raw = await readFile((await downloaded.path())!);
  const document = JSON.parse(raw.toString());
  expect(document.review_status).toBe("draft");
  expect(document.collections[0].memberships[0].rationale).toBe(
    "Independent expert review is pending.",
  );
  const source = Buffer.from(
    document.evidence_files[0].content_base64,
    "base64",
  );
  expect(createHash("sha256").update(source).digest("hex")).toBe(
    document.evidence_files[0].sha256,
  );
  const before = await page.evaluate(() =>
    sessionStorage.getItem("ircomp.workspace"),
  );
  const current = await page.request.get(`/api/v1/workspaces/${before}`);
  const workspace = (await current.json()) as Workspace;
  await page
    .getByText("New / Open / Rename / Duplicate", { exact: true })
    .click();
  await page.getByRole("button", { name: "Close working copy" }).click();
  await page
    .getByRole("button", { name: /Synthetic example — no scientific result/ })
    .click();
  await page.getByRole("button", { name: "02 Review" }).click();
  await expect(page.getByLabel("Rationale", { exact: true })).toHaveValue(
    "Independent expert review is pending.",
  );
  expect(workspace.study.evidence[0].bundle.category).toBe("synthetic");
});

test("invalid input survives save and delayed save cannot erase newer typing", async ({
  page,
}) => {
  // Use a fresh lineage because the preceding test saved the fixed example IDs.
  await page.goto("/");
  await page
    .getByText("New / Open / Rename / Duplicate", { exact: true })
    .click();
  await page.getByLabel("New study title").fill("Draft recovery browser check");
  await page.getByRole("button", { name: "Create study", exact: true }).click();
  await page.getByRole("button", { name: "+ Add target", exact: true }).click();
  await page
    .getByLabel("Target label", { exact: true })
    .fill("Editable interval");
  await page.getByLabel("Start (0-based)").fill("100");
  await page.getByLabel("End (exclusive)", { exact: true }).fill("200");
  await page.getByRole("button", { name: "Apply target", exact: true }).click();
  await page.getByLabel("End (exclusive)", { exact: true }).fill("");
  await save(page);
  await page.reload();
  await expect(page.getByLabel("End (exclusive)", { exact: true })).toHaveValue(
    "",
  );
  const id = await page.evaluate(() =>
    sessionStorage.getItem("ircomp.workspace"),
  );
  const accepted = (await (
    await page.request.get(`/api/v1/workspaces/${id}`)
  ).json()) as Workspace;
  expect(accepted.study.revisions.at(-1)!.targets[0].end).toBe(200);
  let release!: () => void;
  let committed!: () => void;
  const wait = new Promise<void>((resolve) => {
    release = resolve;
  });
  const saved = new Promise<void>((resolve) => {
    committed = resolve;
  });
  await page.route("**/save", async (route) => {
    const response = await route.fetch();
    committed();
    await wait;
    await route.fulfill({ response });
  });
  await page.getByRole("button", { name: "Save study", exact: true }).click();
  await saved;
  await page.getByLabel("End (exclusive)", { exact: true }).fill("250");
  release();
  await expect(page.getByLabel("End (exclusive)", { exact: true })).toHaveValue(
    "250",
  );
  await expect(page.locator(".save-status")).toContainText("Unsaved");
});

test("keyboard editing, explicit context change and narrow layout", async ({
  page,
}) => {
  await page.goto("/");
  await page
    .getByText("New / Open / Rename / Duplicate", { exact: true })
    .click();
  await page.getByLabel("New study title").fill("Keyboard and bounds");
  await page.getByRole("button", { name: "Create study", exact: true }).click();
  await page.getByRole("button", { name: "+ Add target", exact: true }).click();
  await page.getByLabel("Target label", { exact: true }).focus();
  await page.keyboard.type("Target by keyboard");
  await page.keyboard.press("Tab");
  await expect(
    page.getByLabel("Contig accession", { exact: true }),
  ).toBeFocused();
  await page.keyboard.press("Tab");
  await page.keyboard.type("0");
  await page.keyboard.press("Tab");
  await page.keyboard.type("75");
  await page.getByRole("button", { name: "Apply target", exact: true }).click();
  await expect(
    page.getByRole("button", { name: /Target by keyboard/ }),
  ).toBeVisible();
  await page
    .getByText("Change reference or analysis profile", { exact: true })
    .click();
  await page
    .getByLabel("Supported reference")
    .selectOption("grch38-p14-primary-v1");
  await page.getByLabel("Replacement contig").selectOption("NC_000001.11");
  await page.getByRole("button", { name: "Apply context change" }).click();
  await expect(page.locator(".context-strip")).toContainText(
    "grch38-p14-primary-v1",
  );
  await page.setViewportSize({ width: 390, height: 844 });
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
  ).toBe(true);
  await save(page);
});

async function arbitrarySample(page: Page) {
  await page.goto("/");
  const request = await (
    await page.request.get("/api/v1/examples/request-valid.json")
  ).json();
  const evidence = await (
    await page.request.get("/api/v1/examples/evidence-valid.json")
  ).json();
  const oldTarget = request.revision.targets[0].target_id;
  const targetId = crypto.randomUUID();
  request.study_id = crypto.randomUUID();
  request.request_id = crypto.randomUUID();
  request.revision.revision_id = crypto.randomUUID();
  request.revision.targets[0].target_id = targetId;
  request.target_labels = { [targetId]: "Arbitrary imported target" };
  request.title = `Imported study ${request.study_id.slice(0, 8)}`;
  evidence.bundle_id = crypto.randomUUID();
  evidence.request_id = request.request_id;
  evidence.context = request.revision;
  evidence.candidates = evidence.candidates.map(
    (item: { target_id: string }) => ({
      ...item,
      target_id: item.target_id === oldTarget ? targetId : item.target_id,
    }),
  );
  await page
    .getByText("New / Open / Rename / Duplicate", { exact: true })
    .click();
  await page.getByLabel("Import request file").setInputFiles({
    name: "request.request.json",
    mimeType: "application/json",
    buffer: Buffer.from(JSON.stringify(request)),
  });
  await page.getByRole("button", { name: "Open request", exact: true }).click();
  await page.getByRole("button", { name: "02 Review" }).click();
  await page.getByLabel("Import evidence file").setInputFiles({
    name: "evidence.evidence.json",
    mimeType: "application/json",
    buffer: Buffer.from(JSON.stringify(evidence)),
  });
  await page
    .getByRole("button", { name: "Attach evidence", exact: true })
    .click();
  await expect(
    page.getByRole("heading", { name: "Synthetic candidate A" }),
  ).toBeVisible();
  return { request, evidence };
}

test("arbitrary imports, independent collections, removal and historical evidence", async ({
  page,
}) => {
  const { request, evidence } = await arbitrarySample(page);
  await page
    .getByRole("button", { name: "Add to collection", exact: true })
    .click();
  await page
    .getByLabel("Disposition", { exact: true })
    .selectOption("include_for_review");
  await page
    .getByLabel("Rationale", { exact: true })
    .fill("Keep for independent review.");
  await page
    .getByRole("button", { name: "Apply decision", exact: true })
    .click();
  await page.getByText("Manage collections", { exact: true }).click();
  await page
    .getByLabel("Collection name", { exact: true })
    .fill("Second selection");
  await page
    .getByRole("button", { name: "Create collection", exact: true })
    .click();
  await expect(
    page.getByLabel("Review collection", { exact: true }),
  ).toContainText("Second selection");
  await page
    .getByLabel("Review collection", { exact: true })
    .selectOption({ label: "Second selection" });
  await page
    .getByRole("button", { name: "Add to collection", exact: true })
    .click();
  await expect(page.getByLabel("Disposition", { exact: true })).toHaveValue(
    "undecided",
  );
  await page
    .getByLabel("Collection name", { exact: true })
    .fill("Independent selection");
  await page
    .getByRole("button", { name: "Rename collection", exact: true })
    .click();
  await expect(
    page.getByLabel("Review collection", { exact: true }),
  ).toContainText("Independent selection");
  page.once("dialog", (dialog) => dialog.accept());
  await page
    .getByRole("button", { name: "Remove from collection", exact: true })
    .click();
  await expect(
    page.getByRole("button", { name: "Add to collection", exact: true }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Undo", exact: true }).click();
  await expect(page.getByLabel("Disposition", { exact: true })).toHaveValue(
    "undecided",
  );
  await page
    .getByLabel("Review collection", { exact: true })
    .selectOption({ label: "Review collection" });
  await expect(page.getByLabel("Disposition", { exact: true })).toHaveValue(
    "include_for_review",
  );
  await page.getByRole("button", { name: "01 Prepare" }).click();
  await page.getByRole("button", { name: /Arbitrary imported target/ }).click();
  await page.getByLabel("End (exclusive)", { exact: true }).fill("240");
  await page.getByRole("button", { name: "Apply target", exact: true }).click();
  await page.getByRole("button", { name: "02 Review" }).click();
  await expect(
    page.getByRole("heading", {
      name: "No evidence attached to this revision",
    }),
  ).toBeVisible();
  await page.getByLabel("Import evidence file").setInputFiles({
    name: "older.evidence.json",
    mimeType: "application/json",
    buffer: Buffer.from(JSON.stringify(evidence)),
  });
  await expect(
    page.getByRole("button", { name: "Attach evidence", exact: true }),
  ).toBeDisabled();
  await expect(page.locator(".import-preview")).toContainText(
    "CONTEXT_MISMATCH",
  );
  await page.getByRole("button", { name: "Cancel import" }).click();
  await page
    .getByLabel("Request revision")
    .selectOption(request.revision.revision_id);
  await expect(page.getByLabel("Rationale", { exact: true })).toHaveValue(
    "Keep for independent review.",
  );
  await save(page);
});

test("invalid interval diagnostics focus the field and failed save retains the edit", async ({
  page,
}) => {
  await page.goto("/");
  await page
    .getByText("New / Open / Rename / Duplicate", { exact: true })
    .click();
  await page.getByLabel("New study title").fill("Failure and correction check");
  await page.getByRole("button", { name: "Create study", exact: true }).click();
  await page.getByRole("button", { name: "+ Add target", exact: true }).click();
  await page
    .getByLabel("Target label", { exact: true })
    .fill("Interval to correct");
  await page.getByLabel("Start (0-based)").fill("200");
  await page.getByLabel("End (exclusive)", { exact: true }).fill("100");
  await expect(
    page.getByRole("button", { name: "Apply target", exact: true }),
  ).toBeDisabled();
  await page.getByRole("button", { name: /Require 0 ≤ start < end/ }).click();
  await expect(
    page.getByLabel("End (exclusive)", { exact: true }),
  ).toBeFocused();
  await page.getByLabel("End (exclusive)", { exact: true }).fill("250");
  await page.getByRole("button", { name: "Apply target", exact: true }).click();
  await page.route("**/save", (route) =>
    route.fulfill({
      status: 503,
      contentType: "application/json",
      body: JSON.stringify({
        error: {
          code: "PERSISTENCE_UNAVAILABLE",
          message: "Storage is temporarily unavailable.",
          diagnostics: [],
        },
        workspace_version: null,
      }),
    }),
  );
  await page.getByRole("button", { name: "Save study", exact: true }).click();
  await expect(page.getByRole("alert")).toContainText(
    "Storage is temporarily unavailable",
  );
  await expect(page.locator(".save-status")).toHaveText("Save failed");
  await expect(page.getByLabel("End (exclusive)", { exact: true })).toHaveValue(
    "250",
  );
  await page.unroute("**/save");
  await save(page);
});

test("lost command response requires reconciliation before another mutation", async ({
  page,
}) => {
  await page.goto("/");
  await page
    .getByText("New / Open / Rename / Duplicate", { exact: true })
    .click();
  await page.getByLabel("New study title").fill("Lost response check");
  await page.getByRole("button", { name: "Create study", exact: true }).click();
  await page.getByRole("button", { name: "+ Add target", exact: true }).click();
  await page
    .getByLabel("Target label", { exact: true })
    .fill("One accepted target");
  await page.getByLabel("Start (0-based)").fill("100");
  await page.getByLabel("End (exclusive)", { exact: true }).fill("200");
  let calls = 0;
  await page.route("**/commands", async (route) => {
    calls += 1;
    await route.fetch();
    await route.abort("failed");
  });
  await page.getByRole("button", { name: "Apply target", exact: true }).click();
  await expect(page.getByRole("alert")).toContainText(
    "local service is unavailable",
  );
  await page.getByLabel("End (exclusive)", { exact: true }).fill("250");
  await page.getByRole("button", { name: "Apply target", exact: true }).click();
  await expect(page.getByRole("alert")).toContainText(
    "Refresh working state before changing",
  );
  expect(calls).toBe(1);
  await page.unroute("**/commands");
  await page
    .getByRole("button", { name: "Refresh working state", exact: true })
    .click();
  await expect(page.locator(".context-strip")).toContainText(
    "1 accepted targets",
  );
  await expect(page.getByLabel("End (exclusive)", { exact: true })).toHaveValue(
    "250",
  );
  await page
    .getByRole("button", { name: "Discard edits", exact: true })
    .click();
  await page.getByRole("button", { name: /01 One accepted target/ }).click();
  await expect(page.getByLabel("End (exclusive)", { exact: true })).toHaveValue(
    "200",
  );
  await save(page);
});

test("last saved export excludes an accepted but unsaved request revision", async ({
  page,
}) => {
  await page.goto("/");
  await page
    .getByText("New / Open / Rename / Duplicate", { exact: true })
    .click();
  await page.getByLabel("New study title").fill("Saved snapshot check");
  await page.getByRole("button", { name: "Create study", exact: true }).click();
  await page.getByRole("button", { name: "+ Add target", exact: true }).click();
  await page.getByLabel("Target label", { exact: true }).fill("Saved interval");
  await page.getByLabel("Start (0-based)").fill("10");
  await page.getByLabel("End (exclusive)", { exact: true }).fill("20");
  await page.getByRole("button", { name: "Apply target", exact: true }).click();
  await save(page);
  await page.getByLabel("End (exclusive)", { exact: true }).fill("30");
  await page.getByRole("button", { name: "Apply target", exact: true }).click();
  await page.getByRole("button", { name: "03 Export" }).click();
  await page
    .getByRole("button", { name: "Export last saved", exact: true })
    .click();
  await expect(
    page.getByRole("heading", { name: "Request snapshot", exact: true }),
  ).toBeVisible();
  const waiting = page.waitForEvent("download");
  await page.getByRole("link", { name: /Download snapshot/ }).click();
  const downloaded = await waiting;
  const document = JSON.parse(
    (await readFile((await downloaded.path())!)).toString(),
  );
  expect(document.revision.targets[0].end).toBe(20);
  await expect(page.locator(".save-status")).toContainText("Unsaved changes");
});
