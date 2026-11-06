# ITU Phase I submission

### Name: Lukas (Viridis) Dubsik
### Login: xdubsil00
### Project: IRCOMP
### School-Project: ITU-1

The supplied Moodle assignment gives **6 November 2026, 23:59** as the deadline.
The checkpoint presentation is in the regular lab slot in the week starting
**9 November 2026**. The exact lab day/time still needs to be filled in.
Solo participation is agreed; two modules and two planned interviews are the
chosen scope. The assignment requires one real user per actual team member.

## Current work

- [x] Prepare and Review both change application data.
- [x] Shared state, Save/Undo and JSON import/export are implemented.
- [x] Strict Python/client checks and formatting are configured.
- [x] Eleven Cypress scenarios pass with a temporary database; see [testing](testing.md).
- [x] The English report describes the data, GUI, architecture and API.
- [ ] Complete P01/P02 with actual participants.
- [ ] Update needs, competitor comparisons and design using those findings.
- [ ] Fill the regular lab day/time in the report.
- [ ] Review actual contribution and the course restriction on larger generated
  sections. Code and documentation were developed with AI assistance.
- [ ] Check the final report and regenerate the archive after the last changes.
- [ ] Upload personally and confirm the Moodle submission status.

## Creating the archive

Use `make pack` from a clean, committed checkout. It creates
`submission/00_xdubsil00_source.zip`. This is a snapshot of the current Git commit,
so commit any changes that should be included before packaging.

The report PDF is submitted separately as `00_xdubsil00_navrh.pdf`. The required
`_navrh` filename is kept even though the content is in English. Report binaries
are excluded from the source ZIP by `.gitattributes`. Source, schemas, examples,
reference metadata, installation files and essential documentation are included.
Installed packages, databases and build output are excluded.

## Before the presentation

Run the application and demonstrate a target edit, an invalid interval and its
correction, compatible and mismatching evidence, a collection decision,
Save/reopen, one Undo action and a saved export. Explain the shared state and how
the GUI calls the model through the HTTP interface.

All Phase I parts and the presentation are required. The supplied Moodle text
states zero points for missing required work/demonstration and a five-point late
penalty. No completed Moodle upload is recorded here.

Longer research notes, future compiler integration and earlier engineering records
are in [IRCOMP Confluence](https://viridisquercusnova.atlassian.net/wiki/spaces/IRCOMP/pages/29360129).
Historical results belong to the Git revisions named in those records.
