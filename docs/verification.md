# Verification

Local Prepare/Review/Export application; all examples and test candidates are
synthetic. These are engineering checks, not user interviews or biological results.

## Recorded runtime checks

| Check | Result recorded 2 November 2026 |
| --- | --- |
| Python acceptance | 33 pytest cases: domain/services, SQLite, import/export, HTTP and inward dependencies |
| Strict typing/style | Pyright zero errors/warnings; Ruff lint/format pass |
| Client | Strict TypeScript, Vite build and Prettier checks pass |
| Browser | Seven Chromium workflows against the real local service |
| Contracts | Schema, nine structural fixture expectations, original bytes and 24 chromosome provenance records |
| Packaging | Clean source build; sdist/wheel resource resolution and HTTP checks |

Browser workflows cover request import, evidence attachment, decisions, Save and
reopen, invalid draft preservation, delayed Save, keyboard/focus, two collections,
historical context, failed Save, lost command response and last-saved export.
The tested narrow viewport is 390 px. Basic text/action contrast was checked;
this is not a full accessibility audit or cross-browser certification.

One upstream Starlette TestClient warning concerns deprecated HTTPX integration;
tests pass without filtering it. Commands are in the root [README](../README.md).

## Report

The report preserves the supplied template's US Letter page size, one-inch
margins and typography. Its embedded figures distinguish initial wireframes from
implemented synthetic-data examples. Text and binary reports must agree after
editing. Primary research and authorship review remain explicit TODOs.

## Source package

S8 package checks and the exact archive revision/checksum are tracked in
[submission](submission.md) and the generated `submission` directory.
No command check proves biological validity, every input case, crash/power-loss
durability, real-user usability or compliance with unresolved course conditions.
Future YAML/compiler/graph gates remain in the
[integration record](architecture/ircomp-integration.md).

## S8 cleanup and extracted-source checks

Verified again on 2 November 2026 after cleanup:

- 33 backend cases, seven Chromium workflows, strict typing, lint/format and
  contract/provenance checks pass in the working repository.
- A Git source archive from cleanup commit `bc8fe0d` was extracted into a new
  temporary directory. A fresh virtual environment installed
  `requirements-dev.lock` and the project with the documented commands.
- The extracted source passed all 33 backend cases and all seven Chromium
  workflows. Fresh `npm ci`, TypeScript/Vite build and Prettier checks pass.
- ZIP CRCs and required source/lock/provenance entries pass. Report outputs,
  Git metadata, installed dependencies, caches, databases and loose raster assets
  are absent from the source ZIP.
- All retained Markdown links resolve locally. Removed paths are absent from
  retained documentation and report text.
- The updated report retains 20 pages, 33 contents entries and six embedded
  figures. Changed pages were visually checked; other pages match the previously
  inspected render. Body bounds and preserved package parts pass.

Only this verification record and the submission record change after the tested
cleanup commit. The delivered ZIP is regenerated from the final committed tree;
its manifest records that final revision and SHA-256. No additional runtime or
browser assertions were removed; only decorative screenshot capture was deleted.
