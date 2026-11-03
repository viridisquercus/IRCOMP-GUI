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

## S9 final verification — 2 November 2026

**Technical checks pass. The current deliverables are not ready for assessed
submission.** Baseline: `986aebf8af4153a14c31b5375448fd39e415335b`.
This verification increment changes two owner/review comments and these two
records only; no application behavior or report binary is changed.
The checks above were run on 2 November; commit and package finalization resumed
on 3 November 2026 after an approval-service usage limit interrupted the commit.

### Checks run

| Check | Observed result |
| --- | --- |
| Backend | 33 pytest cases pass; existing Starlette/HTTPX deprecation warning remains |
| Contracts | Schema, nine fixture outcomes, original evidence bytes, NCBI hash and 24 chromosome records pass |
| Python quality | Ruff lint/format pass; Pyright zero errors and warnings |
| Client | Strict TypeScript/Vite production build and Prettier pass |
| Browser | All seven Chromium workflows pass against an isolated SQLite test service |
| Archive | Baseline ZIP has 86 files; CRCs, SHA-256 and every byte match recorded Git commit; no unsafe paths or excluded runtime assets |
| Documentation | All 65 local Markdown file links resolve before this record; links rechecked after editing |
| Report | Fresh DOCX render has the same text as the delivered PDF on all 20 pages; rendered pages are pixel-identical to the inspected S8 render |
| Identification | All 34 DOCX heading paragraphs name Lukáš Dubšík; login/lab remain intentional placeholders |
| Source labels | Two missing labels corrected; all 42 Python/TypeScript/TSX/CSS/HTML source files carry the owner name and pending-review qualification |

The report remains an unencrypted, 20-page US Letter PDF with six embedded
figures in the editable DOCX. All-page visual overview and exact comparison to
the previously inspected render found no new layout defect. The 33 contents
entries, captions and readable author labels are retained. There are 13 explicit
TODO occurrences in PDF text, concerning known unfinished submission work.

Report SHA-256 values (unchanged by S9):

- PDF: `cfa7636f30ccb62aaa10940048802117767db04ceb828462c26fb5ec11ffb112`
- DOCX: `dcbfe85140ad982e665d43817b2a133e35bd6dcc1bb6bfe2018b637c3022c21a`

Fresh dependency installation from extracted sources was verified in S8. S9
reran the engineering suite against identical implementation and dependency
files; a second dependency download was not needed. After the comment fixes,
Python lint/format, the client build and formatting are checked again. The final
ZIP is regenerated and checked against its exact commit; only the two labelled
source files and the verification/submission records differ from the S8 package.

### Phase I requirements audit

The supplied assignment, report template and research guide are the requirements
baseline; the deadline comes from the supplied Moodle assignment detail.

| Requirement | Evidence and status |
| --- | --- |
| Real user research and human/process needs | **Pending:** report 1.2 has no completed sessions; 1.3 labels secondary-source hypotheses honestly |
| Two competitor analyses per member; three pros/cons each | Four analyses, each with three pros and three cons, in report 2; mapping to actual research remains pending |
| UI wireframes, rationale, scenarios and navigation | Five editable SVGs; report 3 includes diagrams, figures, state-changing scenarios and recovery |
| Complete local model/API and working key GUI | Prepare edits context/targets; Review changes M:N membership and decisions; Save, Undo and export work within documented scope |
| Separate model, reactive state and asynchronous web communication | Domain/application import-boundary test passes; shared reducer/controller and fetch transport sit outside feature views; React updates without page reload |
| Architecture, state, module APIs and source ownership | Report 4–5 plus retained architecture docs; owner labels exist, actual attribution is unresolved |
| Report PDF and source ZIP | Present and structurally valid; actual-login filenames and completed report still required |
| AI rules and understanding | **Unresolved:** larger AI-generated contributions conflict with the supplied restriction absent an accepted exception; owner labels and passing tests do not resolve this |
| Checkpoint demonstration | Pending regular lab slot in week starting 9 November 2026; both modules, shared state, error recovery, persistence and API must be demonstrated |

No real interviews, usability study, live genomic run, new third-party product
inspection or Moodle upload was performed during S9. Scientific execution and
IRCOMP integration remain outside the implemented local scope. The final
acceptance decision belongs to the course staff; this record reports observable
checks and unresolved requirements rather than awarding a grade.
