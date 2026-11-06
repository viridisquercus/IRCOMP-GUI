# UI design

Prepare edits a small target list against an explicit reference/profile. Review
places immutable observations beside collection-specific decisions. Export previews
an identified saved request or review package. Shared context and save state remain
visible through navigation; changes propagate from the shared model.

| Editable SVG | Purpose |
| --- | --- |
| [Prepare](wireframes/01-prepare.svg) | Interval editor, target list and scoped checks |
| [Prepare error](wireframes/02-prepare-error.svg) | Invalid draft and field-focused correction |
| [Review](wireframes/03-review.svg) | Source evidence separate from editable judgement |
| [Import mismatch](wireframes/04-import-mismatch.svg) | Expected/received identity before atomic acceptance |
| [Export](wireframes/05-export.svg) | Saved context, unresolved decisions and draft status |

These are the initial design sources, not live application captures. All shown
candidate data are synthetic. Edit the SVG directly in a vector or text editor.
The report contains the rationale and interaction scenarios in chapter 3, with
readable figure excerpts. Exact runtime state and validation rules are in the
[architecture](../architecture.md).

Ordinary edits use inline panels; diagnostics focus the relevant field. Text
accompanies status colors, native controls have labels, and narrow layouts stack
regions. A typed draft is separate from an accepted value. Historical evidence
retains its revision, and source scores are never combined into a universal score.

The [real interviews](https://viridisquercusnova.atlassian.net/wiki/spaces/IRCOMP/pages/29425665) must still validate interval
entry, candidate-level decisions and collection granularity. Engineering checks do not establish measured usability.
