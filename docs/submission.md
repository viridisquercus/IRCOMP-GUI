# ITU Phase I submission

Deadline: **6 November 2026, 23:59**, Moodle. Checkpoint presentation: the regular
lab slot in the week beginning **9 November 2026**; exact day/time still to fill in.
Solo participation is agreed; the chosen scope corresponds to two members.

| Work | State |
| --- | --- |
| S1 scope; S3 comparison; S4 interface | In the report, with editable SVG wireframes |
| S2 real-user research | Desk research and interview plan retained; two sessions pending |
| S5 architecture; S6 model/API/GUI | Implemented; contracts and verification retained |
| S7 report | Editable DOCX/PDF draft; research, login/lab and attribution review pending |
| S8 source package | Prepared and checked from a fresh extraction; login placeholder retained |
| S9 final verification | Technical checks pass; submission readiness blocked by research, identification and AI/authorship conditions |
| S10 upload | TODO upload and confirm actual Moodle status |

## Build the source archive

From a clean, committed repository root:

```sh
mkdir -p submission
git archive --format=zip --prefix=IRCOMP-GUI/ \
  --output=submission/00_DOPLNIT_LOGIN_source.zip HEAD
sha256sum submission/00_DOPLNIT_LOGIN_source.zip
git rev-parse HEAD
```

Replace `DOPLNIT_LOGIN` with the actual FIT login before upload. The report PDF is
submitted separately as `00_<login>_navrh.pdf`. `.gitattributes` excludes the report
binary output directory from `git archive`; code, tests, locks, schema/examples,
reference provenance and essential documentation remain included. Git internals,
local databases, installed dependencies and build/cache output are not tracked
archive inputs. Generated ZIP/checksum records stay in ignored `submission/`.

The ZIP is a snapshot of the recorded commit, not a live view of later edits.
After changing submitted code/docs, commit and regenerate it; check CRCs, file
inventory and clean installation again as appropriate. The generated
`submission/manifest.json` records the archive commit, bytes, files and SHA-256.

## Final review

- [ ] Complete the two actual interviews; update the research-to-design mapping.
- [ ] Fill the report login and lab slot and verify required author headings.
- [ ] Resolve the larger AI-generated contribution against the course rules; review
  actual attribution and understanding. Owner labels alone do not establish compliance.
- [ ] Re-export and visually inspect the final report PDF.
- [ ] Regenerate the ZIP from the final reviewed commit; verify source contents.
- [ ] Upload both required files personally and verify the Moodle submission state.
- [ ] Demonstrate both modules, reactive updates, error recovery, persistence and API.

All Phase I parts and the demonstration are required. The supplied Moodle text
states 0 points for missing required work/demonstration and a five-point late
penalty. Preparing an archive does not satisfy the remaining research or upload.

## S8 package check

The cleanup source commit `bc8fe0d` passed a fresh Python environment install,
33 backend cases, clean `npm ci`/build, formatting and seven Chromium workflows
from its extracted archive. The final source ZIP is regenerated after recording
these results; subsequent changes are documentation only. CRCs, the final file
inventory and exclusions are checked again. Exact revision, byte count and hash
are in `submission/manifest.json` and the adjacent `.zip.sha256` file.

The package contains 86 files with a common `IRCOMP-GUI/` root. The login remains
intentionally unfilled, matching the report. This package is prepared for review;
S9 technical verification is recorded below; S10 and primary research remain pending.

## S9 verdict — 2 November 2026

**Technical verification: PASS. Submission readiness: BLOCKED.**

The backend, seven browser workflows, client build, static checks, report render
and archive audit pass. Two missing owner/review labels were added to the package
initializer and HTML entry point. These labels retain the pending-review status.
The archive is refreshed from the commit containing this record; exact revision,
size and checksum remain in the generated manifest. See [verification](verification.md#s9-final-verification--2-november-2026).

Before S10:

1. Complete the planned P01/P02 sessions and trace real findings into needs,
   competitor comparisons and design. Two sessions are the voluntarily chosen
   scope; the assignment says at least one real user per actual team member.
2. Fill the login and regular lab slot; rename both submitted files. These fields
   were intentionally left editable, not inferred.
3. Resolve acceptability of the larger AI-generated contribution with the course
   staff. The supplied assignment permits consultation/small fragments but
   prohibits larger generated sections. Attribution or understanding alone does
   not override that restriction; no exception is documented here.
4. Update both report representations, export and inspect the final PDF, then
   commit, regenerate and verify the ZIP. Repeat affected checks after changes.
5. Upload the PDF and ZIP under the student's own Moodle account by
   **6 November 2026, 23:59** and confirm the actual submission status.

The report's page 18 final-review TODO stays valid while these conditions remain
unresolved. The checkpoint demonstration is still required in the regular lab
slot in the week beginning 9 November; this audit is not that presentation.
