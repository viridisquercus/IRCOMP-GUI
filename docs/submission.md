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
| S8 source package | Cleaned source tree; archive verification recorded below |
| S9 final verification | TODO after research/report/authorship edits |
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
- [ ] Review actual attribution, source ownership headers and course AI rules.
- [ ] Re-export and visually inspect the final report PDF.
- [ ] Regenerate the ZIP from the final reviewed commit; verify source contents.
- [ ] Upload both required files personally and verify the Moodle submission state.
- [ ] Demonstrate both modules, reactive updates, error recovery, persistence and API.

All Phase I parts and the demonstration are required. The supplied Moodle text
states 0 points for missing required work/demonstration and a five-point late
penalty. Preparing an archive does not satisfy the remaining research or upload.
