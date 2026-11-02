# ITU Phase I report

S7 review draft, 2 November 2026. The report follows the supplied Phase I template
and describes the implemented local application at `9364e16`. It has 20 pages,
six figures, both module/API descriptions and a source responsibility inventory.
S2 primary research, final authorship review and S8–S10 remain outstanding.

## Files and editing

- [Report text](phase-i.md): canonical Czech text, with deliberate page boundaries.
- [Identification](metadata.json): fill in `login` and `lab`; keep the real author.
- [Editable document](output/00_DOPLNIT_LOGIN_navrh.docx).
- [Rendered PDF](output/00_DOPLNIT_LOGIN_navrh.pdf).
- [Build record](output/build-record.json): source/template hashes and TODO lines.
- [Verification](verification.md): rendering and structural checks for this version.

`DOPLNIT_LOGIN` is intentionally a filename placeholder, not an actual FIT login.
The first page also leaves the lab slot for completion. Rebuild after editing the
Markdown or metadata. Direct Word edits are possible, but must be transferred
back to the canonical text before rebuilding, or they will be overwritten.
The PDF is a review export; it is not ready for Moodle while research is pending.

## Content coverage

| Template requirement | Report location | Remaining review |
| --- | --- | --- |
| Identification and project theme | First page | Fill login/lab; confirm final scope |
| Actual research method and respondents | 1.1–1.2 | Two real sessions, context, consent and accurate notes |
| Human/process needs | 1.3–1.4 | Replace provisional mappings with participant evidence; retain contradictions |
| Four applications, three pros/cons each | 2.1–2.6 | Remap to real findings; preserve inspection limits |
| UI reasoning, data, operations, navigation | 3.1 | Reconsider interval entry and collection granularity after interviews |
| Separate module designs and scenarios | 3.2.1–3.2.2 | Review the full wireframes in `docs/design/wireframes` |
| Export and recovery | 3.3 | Verify the final selected workflow |
| Architecture diagram and state ownership | 4.1 | Explain the dependency direction and accepted/draft state |
| Per-module data/API/GUI connections | 4.2.1–4.2.2 | Explain operations from the actual code |
| Shared routes, Save and errors | 4.3 | Check against the packaged version |
| Local exchange and thesis boundary | 4.4 | No compiler/YAML/scientific execution claim |
| Functional code and source allocation | 5.1–5.2 | Review real attribution and source headers; create ZIP in S8 |
| Installation and remaining submission work | 5.3 | S8 source archive, S9 verification and S10 upload |

## Research and authorship review

The text was prepared with AI assistance from the recorded project materials and
source. Author names in the headings identify the responsible project owner;
they do not establish independent student authorship of generated text or code.
The supplied ITU rules allow consultation and small fragments, prohibit generation
of larger project sections, and require detailed understanding of submitted work.
This working draft does not establish compliance with those rules. Review the
assistance actually used and prepare the final assessed text with accurate
attribution and in accordance with the course conditions.

- [ ] Conduct and record P01 and P02 without substituting forum posts.
- [ ] Update needs, comparison, scope and interactions from the actual findings.
- [ ] Replace the pending-research statements only once the work is done.
- [ ] Fill login and lab metadata.
- [ ] Check the actual contribution and course AI-use conditions.
- [ ] Review report headings and source ownership comments; do not mass-convert
      `review pending` into an authorship claim without checking the work.
- [ ] Rebuild and inspect the PDF after final content changes.
- [ ] Complete S8–S10 separately; this directory is not an uploaded submission.

## Rebuild

The institutional template stays outside Git. The builder requires the exact
supplied file and checks its SHA-256 before editing a copy. It preserves source
styles, numbering, theme, font table, settings and root relationships byte for
byte. Added figures/footer and body content are the editable package parts.
Page size remains US Letter with one-inch margins, as in the supplied template.

Optional report dependencies are separate from application dependencies:

```sh
python3 -m venv /tmp/ircomp-report-venv
/tmp/ircomp-report-venv/bin/python -m pip install -r scripts/report/requirements.txt
/tmp/ircomp-report-venv/bin/python scripts/report/build.py \
  --template "$HOME/Downloads/ITU – Fáze I Design report (šablona).docx" \
  --output docs/report/output
```

`--font` can select a DejaVu Sans TTF if it is not at the Linux default path.
The normal build accepts explicit TODOs. Add `--strict` before final packaging to
reject unresolved TODOs; passing that guard does not prove the truth of the text
or replace manual review. The script emits DOCX and a build record, not a PDF.

Export the DOCX to PDF using Word or LibreOffice, keeping the same stem. When
working in Codex, resolve its bundled document runtime and use its packaged
`render_docx.py` with `--emit_pdf`; use the bundled LibreOffice, not the desktop
installation. Inspect every page image, compare the 20 planned pages and contents
entries, and check captions, table wrapping, Czech glyphs and page footers.
Changes to text can invalidate the deliberately planned pagination and contents;
adjust page boundaries and repeat rendering before delivery.

The build has no scientific network activity. It reads retained wireframes and
screenshots, crops labelled excerpts and creates native diagrams. It neither
modifies the source application nor contacts interview participants.
