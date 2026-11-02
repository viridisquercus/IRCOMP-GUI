<!-- Working scope retained from S1; S2/S3 contain subsequent refinements. -->

# ITU S1 project scope and design recommendation

Prepared 31 October 2026. This is a planning and consultation document, not the submitted ITU design report, completed user research, or institutional approval. S1 means Submission Task 1 in this chat, not IRCOMP sprint S01. The agreed solo arrangement is taken as given. Two modules, two research users and four competitor analyses follow the student's chosen two-person-equivalent workload, not a newly verified instructor rule.

## Architectural follow-up — 2 November 2026

The bounded ITU scope below is retained. [ADR-0003](../architecture/decisions/ADR-0003-ircomp-specification-boundary.md)
and the [integration gap register](../architecture/ircomp-integration.md) clarify
the future role as an editor/viewer of IRCOMP specifications. Prepare currently
represents a restricted subset of intent; the local request format is separate
from IRCOMP's normalized request and workflow IR. Goals, constraints, control
policies, YAML editing and compiler operations remain explicitly deferred, with
conversion/acceptance gates. This follow-up does not claim interoperability or
expand the November 6 implementation scope.

## Recommended project

**CRISPR Study Workspace — preparation of analysis requests and review of computational evidence.**

Czech working title: **Pracovní prostředí pro přípravu CRISPR analýz a revizi výpočetních výsledků**.

The application helps a computational researcher prepare an explicitly identified CRISPR analysis request, associate compatible evidence with that request, and create a justified review selection without losing the original evidence or confusing predictions with experimental results. It is a local, single-user application with two substantive GUI modules: request preparation and evidence review. It does not require an operational IRCOMP compiler to be useful.

The concept is selected for alignment with the current IRCOMP MWP-A direction, meaningful interaction for ITU, future reuse, and the 6 November deadline. User needs below are hypotheses until the required interviews validate or change them.

## Source findings that determine the design

1. ITU requires more than presentation of results: each authored GUI task must actively change model state; all relevant components must update reactively. Research, competitor analysis, explicit authorship, working application logic/API and key GUI screens are required in Phase I.
2. Downloaded genomic proposals are inconsistent. The May-header proposal concerns a CRISPR cartridge and new off-target enumerator; another revised March proposal substitutes Cas12a-specific prioritization. They are historical context, not a sound basis for silently choosing current scope.
3. The current repository architecture explicitly identifies learning guide v11.1 as the planning basis. Its protected genomic scope is pre-experiment SpCas9–NGG evidence with pinned GRCh38/reference identity, lossless source records and disagreement reporting. New algorithms, AI, observed outcomes and broad deployment are not core dependencies.
4. Guide v11.1 identifies the operator as a bioinformatician or computationally capable research assistant, and the experimental biologist as beneficiary/domain reviewer. This determines the initial audience.
5. Guide bonus B6 is a compact read-only local review UI. That is insufficient on its own for ITU. The proposed ITU work extends it with editable requests and separately persisted review decisions; this is a new scoped course deliverable, not proof that the thesis roadmap has been amended or a gate passed.
6. At inspected main revision `67ec115814f46d45fa6a84bef1c860f58bffb6f3`, `src/ircomp/engine.py` is a placeholder. The architecture and I/O contract explicitly distinguish specified design from implemented behavior. This inspection does not establish the contents of all branches or unpublished local work.
7. The I/O contract is a proposed logical interface, not a frozen runtime API. SCRUM-155, specifying normalized outputs, is still To Do in the inspected record. Therefore the ITU app needs an explicit versioned local exchange format and a future mapping to accepted IRCOMP contracts; it cannot claim compatibility with a nonexistent released API.
8. The repository's dual-project agreement is a proposal awaiting supervisor decisions and distinguishes a FIT bachelor's thesis from the MUNI Final Project. It does not authorize ITU reuse. The design remains useful while reuse terms are resolved separately.

## Why this concept

| Alternative | ITU value | Thesis fit and delivery risk | Decision |
| --- | --- | --- | --- |
| Read-only scientific report viewer | Insufficient active data manipulation | Closest to B6, but weak course compliance | Add request editing and review decisions |
| Generic draggable workflow graph editor | Strong interactions | Requires a large editing/validation surface and prematurely couples to unfinished compiler contracts | Defer |
| Full guide-design and off-target web service | Potentially strong | Requires scientific backend execution and semantic validation before the GUI can be demonstrated | Too much for the deadline |
| New Cas12a model demonstration | Possible UI scope | Follows an older proposal rather than current protected MWP-A | Do not make a dependency |
| Request preparation plus evidence review | Two coherent, persistent workflows | Useful independently and reusable around the future compiler | Recommended |

## Users and needs to investigate

Primary operator: a bioinformatician, computational biology student, or research assistant who prepares analyses and checks their inputs and outputs. Secondary participant: an experimental researcher who reviews candidate evidence and communicates decisions.

Hypotheses to investigate, not interview findings:

- Users need to know exactly which reference and target a result describes.
- Users need to correct missing or incompatible input without losing their work.
- Users need to associate outputs with the right version of a request.
- Users need to compare source evidence without treating different scores as interchangeable.
- Users need to preserve why a candidate was included, excluded or left unresolved.
- Users need to hand over a selection and its limitations without manually reconstructing provenance.

Research should inspect a recent concrete workflow: what files/tools were used, how identities were checked, how choices were recorded and where rework occurred. Do not ask respondents to endorse this proposed UI. Recruit two relevant people; do not substitute developer opinion for either interview. The Jira interview-summary task is not evidence of completed interviews. Existing research may be reused only if its actual scope, consent and academic use allow that reuse.

## Module A — Prepare and revise a study request

**User goal:** express what is to be analysed and establish that the declared inputs are coherent before handing the request to a pipeline.

The central object is a versioned study request containing reference identity, a small collection of targets and the declared supported analysis policy. Start with explicit interval targets; defer gene-symbol resolution because the thesis requires pinned nomenclature, annotation and transcript-selection policies for that feature.

Minimum interactions:

1. Create, rename, duplicate and reopen a study request.
2. Add, edit and remove interval targets, with explicit reference, contig, coordinate convention and strand where relevant. Show coordinate labels beside inputs; do not rely on a hidden convention.
3. Bind targets to an available reference manifest and a supported analysis profile. The initial profile is constrained to the selected MWP-A scope; unsupported choices receive a clear unsupported result, not a guessed conversion.
4. Validate locally supported structural and identity rules. Show a problem list whose entries focus the offending target/field.
5. Correct the request and see the problem count, target summary, validity and export readiness update together.
6. Export an identified request snapshot, then reimport it without losing supported meaning.

Persisted changes include target membership, target data, reference/profile associations and request revisions. These are substantive application state changes. Merely changing the displayed filter does not count.

Validation is scoped. A syntactically valid interval or matching manifest is not proof of biological suitability. If reference sequence, annotation or semantic policy has not been checked, the GUI must not report that check as passed. Validate supported contigs/bounds against the actual bundled manifest; a reference label alone is not verification.

Changing an analysis-relevant input creates a new request revision. Evidence associated with an older revision remains accessible with that identity and is not silently relabelled as current. Cosmetic title changes need not invalidate scientific context; document which fields do.

## Module B — Review evidence and record decisions

**User goal:** assemble an explainable review selection from computational evidence while retaining its origin and limitations.

Minimum interactions:

1. Import an evidence bundle in one documented local exchange format and inspect its source, reference identity, request context and evidence category.
2. Attach a compatible bundle to a specific target/request revision. Reject or isolate incompatible attachments with an actionable reason.
3. Inspect a candidate alongside its source-specific observations and any recorded disagreement. Selecting a record updates the detail panel and summary together.
4. Create named review collections and add/remove candidates. A candidate can belong to multiple collections; a collection can contain many candidates.
5. Set a collection-specific disposition: undecided, include for further review, exclude, or needs clarification. Record a reason and references to supporting evidence. These are research-review decisions, not biological safety approvals.
6. Revise a decision and preserve its source association; support a reversible last action or equivalent recovery.
7. Save/reopen the workspace and export a review package containing selected candidates, decisions, reasons, evidence identities and unresolved issues.

Imported observations remain immutable. Reviewer notes and decisions are a separate layer. A source value of zero is different from an absent value. Scores remain labelled by source/model/version, with scale/direction when supplied. No automatic average or universal confidence percentage is created from unrelated scores.

The UI may group records across sources only using declared identity rules. Ambiguous records remain unmatched; the app must not infer equivalence from a matching display name. A full biological normalization engine is outside this course scope.

Imported synthetic examples are visibly labelled as synthetic. Importing a bundle means the app received data; it does not mean the app observed or verified the claimed external run. Real external evidence must retain actual source files/identities. Evidence-import and review functionality must operate on arbitrary valid input within the declared format, not just a hardcoded demonstration.

## Screen structure and interaction design

Use one application shell with **Prepare**, **Review**, and **Export** destinations. Prepare and Review are the two substantive modules. Export is a shared final view, not a third module commitment.

Prepare layout: target list on the left, inline target/request editor in the centre, linked diagnostics and request summary on the right. Persistent header shows current request revision and save state. Keep reference identity visible while editing target data.

Review layout: target/evidence navigation on the left, candidate evidence comparison in the centre, review collection and rationale panel on the right. A persistent context strip shows the request revision, source bundle and whether the evidence is example data or imported output. Table rows may be used for comparisons, but editing and reasoning happen inline rather than through a succession of pop-up forms.

Export layout: preview of exactly which request version, collections, decisions and sources will be included. Unresolved items remain visible. Exporting a review draft must not silently label it complete.

Keyboard navigation, labelled controls, text explanations alongside status colours, visible save failures and a way to recover a mistaken action are part of usable completion. A large genome browser, complex canvas editor and elaborate animations are not needed.

## Architecture and proposed implementation choice

Recommended default: a local React/TypeScript client with a small Python service and local persistence. Python matches the current IRCOMP repository direction. This is a design recommendation, not a mandated toolkit or claim that a service already exists. Desktop Qt is a viable alternative if it is substantially faster for the author; choose one before implementation.

For the web option, asynchronous HTTP calls satisfy ITU's communication requirement; use a shared model/view-model state layer and update relevant components without reloading the page. Domain validation and persistence live outside visual components. Transient input buffers, focus and panel selection may be UI state, but accepted scientific context and decisions must not be stored only in DOM fields.

Four main aggregate types are sufficient:

| Aggregate | Responsibility |
| --- | --- |
| StudyRequest | Identity, versioned analysis context, targets and profile/reference bindings |
| EvidenceBundle | Immutable imported source observations, manifest and declared request/reference context |
| ReviewCollection | Named set of candidate references associated with one request context |
| ReviewDecision | Membership, disposition, rationale and evidence links; review history as needed |

Identifiers and revisions connect them. A lightweight SQLite store or carefully written versioned local files can persist them; a large backend database is unnecessary. Pick one persistence mechanism rather than implementing both.

Logical application services to implement completely for the declared scope: create/update/duplicate request, add/update/remove target, validate/export/import request, import/attach evidence, create/update collection, add/remove candidate, set/revise decision, save/load workspace, and export review package. These are proposed application operations, not names of existing IRCOMP endpoints.

Keep the future IRCOMP boundary behind an adapter. The initial app performs real local editing, checks, import/export and review without a planner. Later, accepted compiler requests and actual pipeline evidence can pass through that adapter. Do not claim a request export is canonical IR or an execution bundle. Do not create a RunRecord for an operation that was never executed.

## What must work by Phase I

By **6 November 2026 at 23:59**, all declared model/service operations above must work, with key UI paths in both modules connected. Phase I cannot leave all of Module B as static artwork.

Minimum working demonstration:

1. Create a request and add two targets.
2. Enter an invalid supported field; navigate from its diagnostic to the field and correct it.
3. Export and reopen the request with the same supported meaning.
4. Import a labelled evidence example and attach it to the matching request revision.
5. Attempt an incompatible attachment and receive an honest rejection without losing the last valid state.
6. Create a review collection, add candidates, change a disposition and save a reason.
7. Show the list, evidence detail and collection summary update from shared state.
8. Change analysis-relevant request context; show older evidence and decisions retain their original context.
9. Close/reopen the workspace and recover decisions.
10. Export the review package with exact source references and clear example-data status.

Use at least a valid fixture, an incompatible-reference fixture, and an incomplete-evidence fixture. These fixtures exercise app behavior; they do not establish scientific findings. A tiny honest dataset is preferable to fabricated genome-wide analysis.

Phase II completes all declared screens, handles loading/empty/error states, improves interactions based on the checkpoint, and conducts real-user usability testing. Source/result parsing breadth, compiler execution and new scientific computations should remain outside scope unless there is demonstrated capacity and a deliberate change to the project definition.

## Research and comparison follow-through

S1 defines a concept. S2 must test whether users actually need it. The following four systems are candidates for the required comparison, not four completed competitor analyses:

| System | Comparison question |
| --- | --- |
| CRISPOR | How are candidate evidence, source scores and exports presented? |
| CHOPCHOP | How are target/mode input, advanced settings, incompatibility and result meaning communicated? |
| Galaxy | How do users associate inputs, parameters, workflow versions and outputs? |
| IGV | How is genomic reference/context preserved during evidence inspection? |

These cover different parts of the workflow; describe them as partial alternatives where appropriate. For each, personally inspect the relevant interaction and record three advantages and three disadvantages against actual research needs, with screenshots/examples. Do not invent missing features or infer usability from marketing claims. CLI libraries important to the thesis remain scientific baselines but are less informative than graphical tools for the ITU interaction comparison.

Suggested later usability scenarios: prepare a request from supplied information; diagnose an incompatible reference; identify the source of a displayed observation; build a review selection with reasons; recover a decision; explain why older evidence is not current after an input change. Measure independent completion, errors, help requests and interpretation mistakes. No user results are asserted here.

## Limits, reuse and completion status

This design deliberately excludes algorithm development, AI planning, Snakemake/HPC job control, live genome-wide search, multi-organism support, HDR/amplicon design, observed editing outcomes and hosted accounts. Those are outside the bounded application, not unfinished promises hidden behind mocked controls.

The reusable result is the request editor, evidence import boundary, context/identity presentation, review-decision model, and usability evidence. It does not by itself establish FIT compiler correctness, MUNI semantic conformance, biological efficacy or permission to submit identical work for multiple assessments.

ITU's document permits AI consultation but restricts generating large project sections. This memo supports discussion and decision-making; it must not be represented as completed primary research or copied as a completed assessed report. TODO: make and understand the final design and follow the course's authorship rules.

**S1 status: a complete recommended scope has been prepared.** It remains a working proposal to refine through actual research. Supervisor/course reuse permission, accepted biological contracts, actual implementation, and S2 onward are not marked complete.

## Sources inspected

- ITU project assignment (supplied course material), Phase I template (supplied course material), and research guide (supplied course material); recorded Moodle assignment excerpt establishes the exact deadline.
- Historical downloaded proposals: `genetic-proposal.pdf`, `genetic-1.pdf`, and related variants; historical `IRCOMP_spec.txt`. These do not override current planning.
- [Guide v11.1](https://github.com/viridisquercus/IRCOMP/blob/67ec115814f46d45fa6a84bef1c860f58bffb6f3/docs/tasks/IRCOMP_learning_guide_v11_1.html): governing decisions, MWP quality bar, claim reconciliation, S01-T02, S07-T03, S09/S12 tasks, comparison set and B6. Relevant scope and contract sections inspected; unrelated learning resources are outside this review.
- [Current architecture](https://github.com/viridisquercus/IRCOMP/blob/67ec115814f46d45fa6a84bef1c860f58bffb6f3/docs/architecture/overview.md), [I/O contract draft](https://github.com/viridisquercus/IRCOMP/blob/67ec115814f46d45fa6a84bef1c860f58bffb6f3/docs/architecture/contracts/input-output-error-contract.md), and [engine placeholder](https://github.com/viridisquercus/IRCOMP/blob/67ec115814f46d45fa6a84bef1c860f58bffb6f3/src/ircomp/engine.py).
- [Dual-project agreement draft](https://github.com/viridisquercus/IRCOMP/blob/67ec115814f46d45fa6a84bef1c860f58bffb6f3/docs/research/dual-thesis-agreement.md).
- [Confluence product overview](https://viridisquercusnova.atlassian.net/wiki/spaces/IRCOMP/pages/13271041), [system architecture](https://viridisquercusnova.atlassian.net/wiki/spaces/IRCOMP/pages/13434891), and [May scope proposal](https://viridisquercusnova.atlassian.net/wiki/spaces/IRCOMP/pages/21331979). These describe proposed/planned capability, not demonstrated execution.
- [SCRUM-117 interview synthesis](https://viridisquercusnova.atlassian.net/browse/SCRUM-117), [SCRUM-155 output contract](https://viridisquercusnova.atlassian.net/browse/SCRUM-155), [SCRUM-84 claim-map reconciliation](https://viridisquercusnova.atlassian.net/browse/SCRUM-84). Issue state is a limited work-state observation, not independent verification.
- [CHOPCHOP instructions](https://chopchop.cbu.uib.no/instructions), [Galaxy workflow tutorial](https://training.galaxyproject.org/training-material/topics/galaxy-interface/tutorials/workflow-editor/tutorial.html), [IGV documentation](https://igv.org/doc/desktop/). The initial S1 review did not retrieve the CRISPOR manual; S3 subsequently inspected the public form and official repository manual.

## Subsequent review

[S2](s2-desk-research.md) narrows the priorities; [S3](s3-competitive-analysis.md) compares CRISPOR, CHOPCHOP, Benchling and Galaxy. Benchling replaces IGV in the main four-product comparison. The original design remains a traceable starting point, not an implemented feature inventory.
