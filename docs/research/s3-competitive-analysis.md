# S3 — Competitive analysis

Date: 2026-11-01

Status: Working comparison complete; mapping to primary research pending S2 interviews.

## Scope and method

Compare four existing applications against the proposed request-preparation and
evidence-review workflow: **CRISPOR, CHOPCHOP, Benchling and Galaxy**. Four products
cover the chosen two-person equivalent workload. Each analysis records three
advantages, three disadvantages and a consequence for the design.

CRISPOR and CHOPCHOP are direct domain alternatives. Benchling is an integrated
laboratory workspace. Galaxy is a partial workflow/provenance alternative, not a
specialist guide-review application. IGV remains a supplementary inspection
reference; it overlaps less with editable preparation and review than Benchling.

The comparison uses public interface inspection and official documentation. It
is an expert review, not a user study or a scientific benchmark. No private
sequence data were submitted, new accounts created, or computational analyses
executed. There are no measured task times, error rates or numerical usability
scores. An unavailable feature in the inspected route is not evidence that the
entire product lacks it.

Evidence levels:

- **O — observed:** visible in the inspected public interface.
- **D — documented:** described in official instructions, not executed here.
- **I — inference:** likely interaction consequence for this project's scope.

The [inspection register](evidence/s3/README.md) records surfaces, screenshots,
versions where visible, and the limits of each inspection. Screenshots document
particular states; they do not demonstrate a completed workflow.

## Needs used for comparison

The identifiers preserve the [S2 desk-research](s2-desk-research.md) mapping.
They remain provisional until checked against real workflow interviews.

| ID | Human/process need | Comparison question |
| --- | --- | --- |
| N1 | Understand the origin and meaning of an observation | Can a reviewer distinguish source/model/context? |
| N2 | Recognize the exact target and reference | Is identity visible at the point of input and review? |
| N3 | Distinguish absent evidence from an unfavorable result | Are score availability and execution state unambiguous? |
| N4 | Correct an input problem without losing work | Does the route expose the relevant setting and a correction path? |
| N5 | Recover the context of an earlier review | What is saved, versioned and associated with output? |
| N6 | Hand over an understandable review | What can be exported or shared, and with which dependencies? |
| N7 | Fit existing work without unnecessary transfer | How many objects, contexts and manual transfers are involved? |
| N8 | Preserve reasons for a review decision | Where can rationale live? This need has weak direct evidence so far. |

## 1. CRISPOR

Public form inspected at [CRISPOR](https://crispor.gi.ucsc.edu/), displaying
Version 5.2. Result interactions were assessed through the
[official manual](https://github.com/maximilianh/crisporWebsite/blob/master/manual/manual.md).

### Advantages

| ID | Finding and evidence | Need | Design lesson |
| --- | --- | --- | --- |
| CR-P1 | O: Three numbered input groups expose target, genome and PAM together. | N2, N7 | Keep essential context visible in one preparation view. |
| CR-P2 | D: Annotated sequence and guide-table links connect spatial context with individual records. | N1, N2 | Selection should update an adjacent evidence detail view. |
| CR-P3 | D: Downloadable result pages/spreadsheets support retention outside the live result page. | N5, N6 | Include a portable review export. |

### Disadvantages for this workflow

| ID | Finding and evidence | Need | Design lesson |
| --- | --- | --- | --- |
| CR-C1 | D/I: Remembered genome selection can carry an earlier context into a new request. | N2, N4 | Show inherited settings explicitly before accepting input. |
| CR-C2 | O/I: Main form specifies one sequence below 2,300 bp; batch work uses a separate route. | N7 | Keep the planned small target collection in one workspace. |
| CR-C3 | D/I: Long-term retention requires a deliberate download rather than reliance on a bookmarked result. | N5, N6 | Make persistence and export state visible. |

### Interpretation

Borrow the compact input sequence and linked details. Do not reproduce the
scientific engine or claim that every batch task is unsupported. Saved review
decisions are a proposed IRCOMP-GUI extension; their absence across CRISPOR has
not been established by this limited inspection.

## 2. CHOPCHOP

Public [input form](https://chopchop.cbu.uib.no/) and expanded Options inspected.
Score and persistence behavior comes from the
[official instructions](https://chopchop.cbu.uib.no/instructions).

### Advantages

| ID | Finding and evidence | Need | Design lesson |
| --- | --- | --- | --- |
| CH-P1 | O: Target, organism, tool family and purpose appear in one compact row. | N2, N7 | Summarize the full request context together. |
| CH-P2 | O: Advanced controls are behind Options with General/Cas9/Primers tabs. | N7 | Use progressive disclosure for infrequent settings. |
| CH-P3 | O: Target entry advertises identifiers or coordinates, with a separate pasted-sequence route. | N2, N7 | Investigate the operator's actual starting artifact before fixing input design. |

### Disadvantages for this workflow

| ID | Finding and evidence | Need | Design lesson |
| --- | --- | --- | --- |
| CH-C1 | D/I: Advanced options can persist across mode changes; instructions recommend resetting them. | N2, N4 | Make effective settings and context changes explicit. |
| CH-C2 | D/I: Some unsupported score settings produce zero; G20 separately uses a binary value. | N1, N3 | Preserve raw values and explicitly label their interpretation. |
| CH-C3 | O/I: Expanded settings expose many biological choices and defaults at once. | N4, N7 | Restrict the first version to one supported profile with clear explanations. |

### Interpretation

The compact initial view is a useful pattern, but hiding controls must not hide
effective context. The third disadvantage is an expert inference about cognitive
load, not a measured failure. No retained-settings or scoring experiment was
executed. Unsupported and zero remain separate concepts in the proposed model.

## 3. Benchling

Documentation-based review of the official
[CRISPR workflow](https://help.benchling.com/hc/en-us/articles/9684226093197-CRISPR-Knockouts),
updated 2024-09-26. No authenticated application session was inspected.

### Advantages

| ID | Finding and evidence | Need | Design lesson |
| --- | --- | --- | --- |
| BE-P1 | D: Imported sequence, analysis and saved results live within an organized workspace. | N5, N7 | Keep related request and evidence objects together. |
| BE-P2 | D: Split Workspace and guide selection connect table records to sequence context. | N1, N2 | Link selection and details through shared state. |
| BE-P3 | D: All or selected guides can be exported for a notebook or spreadsheet. | N6, N7 | Support a deliberate selection and a useful handover. |

### Disadvantages for this workflow

| ID | Finding and evidence | Need | Design lesson |
| --- | --- | --- | --- |
| BE-C1 | D/I: The documented route assumes an account and an existing Benchling workspace. | N7 | A standalone local review should not require remote onboarding. |
| BE-C2 | D/I: Preparation crosses import, parameter and analysis contexts. | N2, N7 | Retain a visible request summary through transitions. |
| BE-C3 | D/I: The taught notebook transfer involves exporting TSV, creating table headings and pasting. | N6, N8 | Preview a package that retains evidence and rationale together. |

### Interpretation

These limitations concern the documented route, not all available Benchling
features. The integrated workflow is strong counterevidence to building another
generic guide organizer. Whether a separate IRCOMP interface reduces effort must
be tested with an actual workflow, including conversion into its exchange format.

## 4. Galaxy

Public [Galaxy Europe](https://usegalaxy.eu/) workspace inspected without login.
History operations and version handling were checked in the official
[history tutorial](https://training.galaxyproject.org/training-material/topics/galaxy-interface/tutorials/history/tutorial.html)
and [workflow tutorial](https://training.galaxyproject.org/training-material/topics/galaxy-interface/tutorials/workflow-editor/tutorial.html).

### Advantages

| ID | Finding and evidence | Need | Design lesson |
| --- | --- | --- | --- |
| GA-P1 | D: Histories group work and support tags and longer annotations. | N5, N8 | Preserve context and human explanations alongside evidence. |
| GA-P2 | D: Workflow versions can be revisited and individual tool versions selected. | N5 | Keep input/evidence version associations explicit. |
| GA-P3 | D: History archives and sharing provide routes for handover. | N6 | Export more than a screenshot or a transient selection. |

### Disadvantages for this workflow

| ID | Finding and evidence | Need | Design lesson |
| --- | --- | --- | --- |
| GA-C1 | O/I: A large tool catalog and general analysis navigation precede the narrow review task. | N7 | Offer task-specific Prepare and Review destinations. |
| GA-C2 | D/I: Workflow attributes, tool versions and history controls occupy different contexts. | N2, N5 | Keep the relevant request/evidence identity visible without opening several views. |
| GA-C3 | O: Anonymous session disables creating, switching and renaming histories with login explanations. | N5, N7 | Make local persistence usable without an account. |

### Interpretation

Galaxy already addresses provenance and organization; these are not novel
concepts. Its broader scope is useful for execution but larger than the present
application needs. The login observation applies to the inspected public server,
not every Galaxy deployment. No missing CRISPR tool or broken workflow is inferred.

## Comparative synthesis

This is a comparison of emphasis and inspected evidence, not a universal ranking.
“Not assessed” must not be converted into “unsupported.”

| Criterion | CRISPOR | CHOPCHOP | Benchling | Galaxy |
| --- | --- | --- | --- | --- |
| Preparation pattern | Three input groups | Compact row + advanced tabs | Sequence import → parameters → analysis | Tool/workflow selection + inputs |
| Most useful pattern | Linked evidence detail | Progressive disclosure | Related objects in one workspace | History and version context |
| Main cost for this scope | Separate main/batch routes | Many effective settings | Workspace onboarding and transfer | General-platform navigation |
| Persistence/handover evidence | Manual documents downloads | Not assessed end-to-end | Documented saved analysis/export | Documented histories/archive/share |
| Candidate-specific rationale | Not established | Not established | Notebook route; exact decision semantics untested | General annotations; exact candidate semantics untested |
| Inspection strength | Public input + manual | Public input/options + instructions | Official documented workflow | Public shell + official tutorials |

### Decisions for IRCOMP-GUI

1. **Prepare:** a persistent context strip and a small editable target list.
   CR-P1 and CH-P1 support visibility; CR-C1 and CH-C1 motivate explicit effective
   settings. Full reference details remain inspectable without crowding every row.
2. **Review:** list selection updates evidence details and the editable review
   panel. CR-P2 and BE-P2 motivate linked views, not a full genome browser.
3. **Interpretation:** keep source metrics separate; show unavailable or unknown
   status in text. CH-C2 motivates a state distinction, not heuristic rewriting
   of imported zeros.
4. **Persistence:** save requests, evidence identities and decisions. GA-P1/GA-P2
   motivate traceability; the initial UI needs a clear current/older-context
   distinction rather than a workflow editor or branch graph.
5. **Export:** preview contents and unresolved items before creating a review
   package. CR-C3 and BE-C3 motivate an explicit handover; GA-P3 demonstrates that
   richer portable state already has precedents.
6. **Scope:** retain one default review collection and a documented import
   boundary. Additional collection workflows need interview support. Product
   value must include the cost of preparing an import, not just viewing it.

These decisions are interaction proposals. The application does not inherit the
scientific capabilities of the products whose interface patterns informed it.

## Review TODO

- [ ] Replace provisional need mappings with evidence from the two S2 sessions;
      retain contradictions and remove unsupported assumptions.
- [ ] Inspect a consented or synthetic authenticated Benchling workflow if it is
      part of a participant's actual work; verify whether the documented transfer
      cost still applies to that route.
- [ ] Capture representative result/recovery states if needed for the report;
      current screenshots show input/options/workspace/documentation only.
- [ ] Check the final report's author-labelled headings and citation format.
- [ ] Write the assessed comparison in the final report after reviewing these
      working notes. Do not describe expert inspection as participant testing.

The four-product, three-pro/three-con comparison is present. Final linkage to
observed user needs remains dependent on S2 primary research.
