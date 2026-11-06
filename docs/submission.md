# ITU Phase I submission

Due **6 November 2026, 23:59**, in Moodle. Checkpoint presentation: the regular lab
slot in the week beginning **9 November 2026**; exact day/time to fill in.
Solo participation is agreed; two modules and two planned interviews are the
chosen scope. The assignment requires at least one real user per actual member.

## Before upload

- [ ] Complete P01/P02 and update needs, competitor comparisons and design from
  actual findings. The report currently contains clearly labelled placeholders.
- [ ] Fill login/lab and use `00_<login>_navrh.pdf` and `00_<login>_source.zip`.
- [ ] Resolve actual authorship and the course restriction on larger AI-generated
  contributions. Cleanup does not change the provenance of the existing draft/code.
- [ ] Review both report representations and export/inspect the final PDF.
- [ ] Run the app, edit a target, attach compatible evidence, record a decision,
  Save/reopen, Undo an unsaved edit and inspect request/review exports.
- [ ] Commit the final changes and regenerate the source ZIP below.
- [ ] Upload PDF and ZIP personally and confirm the Moodle submission state.

## Package

From a clean committed checkout:

```sh
mkdir -p submission
git archive --format=zip --prefix=IRCOMP-GUI/ \
  --output=submission/00_DOPLNIT_LOGIN_source.zip HEAD
sha256sum submission/00_DOPLNIT_LOGIN_source.zip
```

Replace the login placeholder before upload. The report is submitted separately;
`.gitattributes` excludes its binary outputs from the source ZIP. Source, schemas,
examples, reference provenance and setup files stay included. Installed packages,
SQLite databases and build output are ignored. Rebuild the ZIP after source edits.

The repository contains the standalone application and required report/design
sources. Longer research notes, integration plans and earlier verification records
are in [IRCOMP Confluence](https://viridisquercusnova.atlassian.net/wiki/spaces/IRCOMP/pages/29360129).
Earlier automated results describe their exact old Git revision, not this cleanup.

The checkpoint must demonstrate both editable modules, reactive shared state,
input correction, persistence and API separation. All Phase I parts and the
presentation are required; the supplied Moodle text states zero points for missing
required work/demonstration and a five-point late penalty. No Moodle upload is
recorded here.
