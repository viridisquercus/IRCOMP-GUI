# S7 report verification

Date: 2026-11-02. Result: rendered review draft, not a completed submission.

| Check | Observed result |
| --- | --- |
| Source basis | Supplied ITU assignment, template and research guide; S1–S6 notes; inspected implementation at `9364e16` |
| Report structure | Project identification/theme and all five template subject areas, with references as chapter 6 |
| Contents | 33 entries checked against the actual PDF locations; 20 pages |
| Figures | Six inline figures: navigation, three S4 excerpts, architecture and an actual S6 excerpt; synthetic data identified |
| Visual review | All 20 pages inspected; no clipped text, table overlap, missing Czech glyphs or disconnected captions |
| Text bounds | PDF character bounds remain inside the expected body area; footer separate |
| Author labels | Project owner present in every title/section heading; actual attribution review remains open |
| Template fidelity | Original template SHA-256 unchanged; styles, numbering, fonts, theme, settings and root relationships preserved byte for byte |
| Page geometry | One US Letter portrait section with one-inch margins; a page-number footer added |
| Source placeholders | Login/lab visibly fillable, no unexpanded template tokens in PDF |
| Research honesty | No invented P01/P02 data, dates, quotations, findings, task times or usability results |
| Scope honesty | Local JSON/validation distinguished from IRCOMP language/compiler and biological verification |
| Builder | Ruff lint and formatter pass; optional dependencies isolated from runtime |
| Final-mode guard | `--strict` rejects the current TODOs with an error before creating output |

The [build record](output/build-record.json) contains hashes for the text,
metadata, external template and delivered DOCX/PDF. The latest render changed
only the contents page and the Prepare excerpt from the preceding reviewed
version; the other page PNGs were byte-identical. Those two pages were inspected
again. PNGs and trial renders remain outside Git.

S6's 33 backend cases and seven Chromium workflows are cited as previously
observed results, not rerun or newly claimed for S7. This task changes report
materials and tooling only. Document checks do not complete S9 or replace a
final clean installation from the actual S8 archive.

## Remaining release conditions

- [ ] Real S2 sessions and evidence-linked revisions to chapters 1–3.
- [ ] Login and lab metadata, then corresponding output filenames.
- [ ] Actual authorship/source-header and course AI-use review.
- [ ] Regenerate and inspect final artifacts after those edits.
- [ ] Actual S8 archive, S9 verification and S10 Moodle upload.

The review draft is usable for editing and technical review now. Its presence
does not satisfy the missing primary research or prove course-policy compliance.
