# ITU Phase I

Submission: **2026-11-06 23:59**, Moodle assignment deadline supplied in course
access. Presentation: regular team lab in the week beginning **2026-11-09**;
exact slot remains to be recorded. Solo participation is agreed; workload is
planned as a two-person equivalent.

| Task | Status | Record |
| --- | --- | --- |
| S1: bounded topic and modules | Working scope prepared | [Scope](../research/s1-scope.md) |
| S2: user research | Desk research prepared; two real sessions pending | [Research](../research/s2-desk-research.md), [plan](../research/s2-interview-plan.md) |
| S3: four existing applications | Comparison prepared; final primary-need mapping pending | [Comparison](../research/s3-competitive-analysis.md) |
| S4: UI design | Initial specification and five wireframes prepared; interview validation pending | [Design](../design/README.md) |
| S5: architecture/contracts | Specification prepared; schema/fixture and provenance checks pass | [Architecture](../architecture/overview.md), [contracts](../../contracts/README.md) |
| S6: all model/API operations and key GUI | Implemented locally; 33 backend and seven Chromium workflows pass | [Criteria](../architecture/s6-acceptance.md), [verification](../development/s6-verification.md) |
| S7: design report | Review draft rendered and checked; research and authorship pending | [Report text, DOCX and PDF](../report/README.md) |
| S8: source archive | TODO | Create the actual ZIP and verify contents |
| S9: final verification | TODO | Research, attribution, reproducibility and final PDF/ZIP |
| S10: Moodle upload | TODO | Upload and verify actual submission state |

Submission filenames from the assignment: `00_<login>_navrh.pdf` and
`00_<login>_source.zip`. Report sections require author identification. All
required parts and the checkpoint demonstration matter; late upload incurs the
specified five-point penalty. This checklist does not replace the course files.

## Future integration tracking

[ADR-0003](../architecture/decisions/ADR-0003-ircomp-specification-boundary.md) and
the [gap register](../architecture/ircomp-integration.md) record ownership, mapping
limitations and future acceptance gates. Documentation alignment is complete;
YAML/specification editing, compiler calls and workflow graphs are unimplemented
and outside the current ITU milestone. Revisit the register before adding any
compiler adapter or changing request semantics. S6 continues with the local API.

## Source material

Supplied course documents: “ITU – Zadání a pokyny k projektu”, “ITU – Fáze I
Design report (šablona)”, and “ITU – Průvodce uživatelským výzkumem a testováním
použitelnosti”. Institutional documents remain outside the repository. Working
notes are preparation material, not a completed assessed report. TODO: review
final text, attribution and the course AI-use rules before submission.
