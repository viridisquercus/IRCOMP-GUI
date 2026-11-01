# ITU S2 — Desk research for CRISPR Study Workspace

Research date: 1 November 2026. Status: secondary research and provisional design recommendations; no interviews or usability sessions have been conducted for this memo.

Companion: [S1 design](s1-scope.md). Interview materials: [S2 interview kit](s2-interview-plan.md).

## 1. Decision supported by this research

Continue with the two-module concept from S1: **prepare an explicit analysis request, then review imported computational evidence and record decisions**. Narrow the product proposition to helping a computational researcher establish what an output means, whether it belongs to this request, and what remains unresolved before handing it onward.

The strongest support is for context, score interpretation and recoverable validation. The evidence does not establish demand for another general CRISPR design platform, elaborate review collections, a workflow graph editor, or a universal ranking algorithm. The prospective user must still demonstrate a task this application improves over their existing tools.

Working problem statement, to test rather than present as an interview finding:

> When preparing or reviewing a small CRISPR analysis, a computational researcher needs to keep target identity, analysis settings and source evidence together, understand incompatibilities, and communicate a justified review decision without reconstructing the context manually.

This research supports a bounded interface around the thesis, not new scientific claims. It does not establish biological efficacy, validate a scoring model, or demonstrate that IRCOMP execution exists.

## 2. Method, coverage and limits

Research coverage included public discussions on Reddit (r/labrats and r/bioinformatics), GitHub issues, Galaxy Help and archived Galaxy/Biostar discussions; checked official CRISPOR, CHOPCHOP, Benchling, Galaxy, UCSC and IGV documentation; and consulted original research papers. Search themes included conflicting guide scores, annotation uncertainty, reference/coordinate mismatch, local installation failures, analysis organization, provenance, handover and satisfaction with existing tools.

Representative queries included `CRISPR guide scores different Benchling IDT CHOPCHOP`, `site:biostars.org CRISPOR CHOPCHOP scores different`, `site:help.galaxyproject.org history reproduce parameters`, and `site:reddit.com/r/bioinformatics CRISPR workflow tools`. Biostars-targeted searches yielded adjacent material, including Galaxy archives; this is not a comprehensive survey of Biostars. Some Reddit results were inaccessible or only available as search excerpts and were excluded from the main evidence set. No private messaging groups were accessed and nobody was contacted.

The register below retains **16 public sources**: seven community/issue threads, six official documentation pages, and three research papers. The current thesis context comes from the earlier S1 inspection, not a new claim that its implementation has advanced. Search results were followed to relevant source passages where retained; unrelated recommended posts on Reddit pages were not treated as part of the thread.

Evidence labels:

- **Reported:** an author describes their own experience. It establishes a reported incident, not independently observed behavior.
- **Documented:** a tool author documents a behavior or convention. It does not establish how often users struggle with it.
- **Research:** a published study supplies technical context within its tested conditions.
- **Inference:** the proposed need, explanation or design response. It still needs validation with the intended users.

Confidence concerns the existence of a problem or documented behavior, not its prevalence. Forum participants are self-selected, roles are not verified, difficult cases are overrepresented, and several discussions concern other genomic tasks. Threads are not independent interview participants. Upvotes are not prevalence measures. Older reports do not establish current defects. Relative Reddit dates and crawl dates were inconsistent in some retrieved views; exact dates are left unverified rather than reconstructed from those labels.

## 3. Evidence register

All links were accessed during this research on 1 November 2026. Summaries are paraphrases; detailed design proposals elsewhere are design inferences.

| ID | Source and date | Evidence retained | Limit and relevance |
| --- | --- | --- | --- |
| E01 | [r/labrats: variable ON/OFF scores](https://www.reddit.com/r/labrats/comments/tlaqhf/why_are_onoff_target_scores_so_variable_from/) — exact post date unverified | Author reports very different evaluations for the same sequences in Benchling, IDT and CHOPCHOP, and uncertainty about which to trust. | Direct CRISPR interpretation problem; settings were not audited. Replies do not establish the correct biological explanation. |
| E02 | [r/labrats: CRISPRi guides and conflicting annotations](https://www.reddit.com/r/labrats/comments/rxoy4y/issues_designing_crispri_guides_w_idtbroad_tools/) — exact date unverified | Author cannot reconcile promoter/TSS annotations, reports conflicting Broad/IDT evaluations and limited local help. Discussion initially confuses the intended modality. | CRISPRi is outside our initial scope. Transfers to visible task/annotation context, not a requirement to support CRISPRi or proof of a tool bug. |
| E03 | [CRISPOR issue 69](https://github.com/maximilianh/crisporWebsite/issues/69) — 7 August 2024 | Initial index failure after installation. Final author reply identifies `h38` instead of `hg38`; correcting the identifier allowed execution. | Resolved in conversation despite issue remaining open. Supports early identifier checks and useful errors, not claims of broken installation. |
| E04 | [Galaxy Help: VCF annotation](https://help.galaxyproject.org/t/help-with-vcf-annotation/11407) — 4–10 January 2024 | Missing annotations and confusing errors led to support discussion; author confirmed chromosome naming mismatch and successful annotation after correction. | VCF workflow, not CRISPR. Strong concrete transfer case for checking compatible identifiers. Does not justify automatic renaming in every case. |
| E05 | [r/labrats: useful laboratory tools](https://www.reddit.com/r/labrats/comments/1es2n2a/are_there_any_free_online_tools_you_use_in_the_lab/) — exact date unverified | Commenters value Benchling's integrated sequence import, annotations and saved designs; one describes having most needed tools together. | Positive counterevidence. Historical personal experience, not a current pricing or completeness audit. |
| E06 | [r/bioinformatics: organizing code and analyses](https://www.reddit.com/r/bioinformatics/comments/1sgk92b/how_do_you_organize_bioinformatics_code_and/) — exact date unverified | Author reports unsaved commands, working and failed code mixed together, and multiple similar analysis versions under deadline pressure. | General computational work, not evidence of a specific CRISPR review process. Supports investigating context recovery. |
| E07 | [r/bioinformatics: tools and workflows](https://www.reddit.com/r/bioinformatics/comments/1wrgw0r/what_tools_and_software_do_you_use_in_your/) — exact date unverified | Author describes preferring terminal tools and keyboard interaction, finding full IDEs distracting. Other participants also describe established scripting workflows. | Counterevidence to assuming computational researchers want a GUI. Not representative of all bioinformaticians. |
| E08 | [CRISPOR manual](https://github.com/maximilianh/crisporWebsite/blob/master/manual/manual.md) — mutable documentation | Documents retained genome choice, reference-related warnings, cases where sequence context prevents scoring, and downloadable output for archival. | Documentation inspected, not a live task benchmark. Version-specific recommendations are not treated as universal current biological advice. |
| E09 | [CHOPCHOP instructions](https://chopchop.cbu.uib.no/instructions) — mutable documentation | Documents zeros under some unsupported scoring settings, G20 as a binary feature, and advanced options that can persist when the targeting mode changes. | These are distinct cases. A zero must not automatically become “missing”; source context determines interpretation. |
| E10 | [Galaxy: understanding input errors](https://training.galaxyproject.org/training-material/faqs/galaxy/troubleshooting_input_problem.html) — mutable documentation | Distinguishes input format, parameter, reference and content problems; apparently successful inputs may still be empty. | General workflow guidance. Does not prove the proposed validator can perform every check. |
| E11 | [UCSC coordinate FAQ](https://genome.ucsc.edu/FAQ/FAQtracks.html#tracks1) — mutable documentation | Describes the difference between database/BED coordinates and displayed position coordinates. | Convention evidence, not an incident sample. Do not generalize a single convention to all formats. |
| E12 | [IGV sessions](https://igv.org/doc/desktop/UserGuide/sessions/) — mutable documentation | Saved sessions restore viewing state, but recipients also need access to referenced data files. Autosave is supported. | Existing solution and portability constraint; a saved session is not necessarily a self-contained data package. |
| E13 | [Benchling CRISPR worksheet](https://help.benchling.com/hc/en-us/articles/9684226093197-CRISPR-Knockouts) — page updated 26 September 2024 | Documents importing a target, scoring guides, saving analysis and exporting sequences to a notebook. | Confirms overlap with the proposed workflow. Documentation does not establish usability or current account entitlements. |
| E14 | [Bradford & Perrin: benchmark of guide design methods](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1007274) — 29 August 2019 | Study of 18 tools found variation in candidate sets and limited agreement under its tested datasets and versions. | Historical benchmark, not a current leaderboard or proof of optimal consensus aggregation. |
| E15 | [Khan et al.: genomic workflow provenance](https://pmc.ncbi.nlm.nih.gov/articles/PMC5508699/) — 2017 | Case study across three workflow approaches found implicit assumptions and incomplete requirements hindered reproduction. | Technical rationale for explicit context; not a study of this application's users or proof that a GUI solves reproducibility. |
| E16 | [Hoberecht et al.: crisprVerse](https://www.nature.com/articles/s41467-022-34320-7) — 2 November 2022 | Presents an R/Bioconductor ecosystem integrating guide design, annotations and scoring. | Counterevidence to claiming integration is new or absent. Not an interaction evaluation of the proposed ITU application. |

Excluded from core findings: promotional posts advertising new tools; commercial comparison/SEO pages; inaccessible search-only reports; broad HDR, screening, crop and sequencing-analysis feature requests that would expand the agreed scope; unresolved historical bugs where a causal conclusion would be speculative. Exclusion means insufficient relevance or evidence for this design, not that a reported problem is false.

## 4. Findings and design implications

### F1 — Users can interpret disagreement as a question of whom to trust

E01 directly reports this problem; E02 supplies a related but differently scoped example. E14 shows that differing outputs existed under controlled historical comparisons. These sources do not establish that any particular tool is right for the target user's task.

**Proposed need N1:** identify the source and meaning of an observation before using it in a decision.

For the UI, retain separate source/model-labelled columns; reveal units or scale and direction only when known. Provide the original source record and explain any transformation. Permit “cannot compare from available metadata.” Do not show a universal confidence percentage, average unlike scores, or infer consensus from a large number of sources. A shared sequence is not enough to establish shared context.

Interview uncertainty: does the intended operator actually compare outputs, or consistently use one approved pipeline? If the latter, multi-source comparison can be a secondary detail view rather than the main screen.

### F2 — Target identity includes more than a friendly name

E02 concerns annotation ambiguity. E03 and E04 provide concrete resolved naming incidents. E11 establishes that visible coordinates require a declared convention. Together they justify investigating identity handling without implying every disagreement is a naming error.

**Proposed need N2:** recognize the exact reference and target represented by input and output, and correct incompatible identity without losing work.

Use controlled choices for known reference profiles; display the full accession/version in details and a concise unambiguous summary in the main view. Label interval conventions at entry and export. A diagnostic should identify the offending field, supplied value, expected identifier and next action. An alias suggestion is not proof of equivalence. Do not silently strip chromosome prefixes, convert assembly coordinates, or choose a transcript.

The interval-first S1 design reduces implementation ambiguity but may impose work on researchers who start with gene symbols. That is an unresolved usability tradeoff. Interviews must establish where intervals come from and whether the intended computational operator can supply them reliably.

### F3 — Missing, unsupported, failed and zero are different states

E09 documents why numeric appearance alone can mislead; E08 describes a different reason scores may be unavailable. E10 warns that an apparently successful step can yield empty content.

**Proposed need N3:** distinguish absent evidence from an unfavorable observation and distinguish successful import from successful analysis.

Our proposed representation is a raw value plus declared availability/interpretation metadata. Unknown interpretation stays unknown. Preserve a source's raw zero; annotate unsupported status only when the source metadata or validated adapter supports that interpretation. Use textual labels as well as color. An empty valid bundle should say “No candidate records supplied,” with execution status separately shown if known; it must not imply that a completed search found no candidates.

This is a correctness requirement for our display even if users never report a zero/missing mistake. Whether the proposed labels are understandable needs observation.

### F4 — Troubleshooting should lead back to a repairable input

E03's final reply changes the story from possible installation difficulty to a known input typo. E04 similarly resolves a misleading failure through context checking. E10 supplies a broader diagnostic taxonomy.

**Proposed need N4:** know what can be corrected now and what remains outside the application's checks.

Separate structural checks, declared identity compatibility, missing metadata and unperformed scientific checks. Link diagnostics to fields; retain valid edits after failure; offer technical details on demand. Where the app has only an identifier, it can verify membership in a manifest but cannot assert that an external file contains the correct genome. No “biologically validated” badge follows from parsing a JSON file.

A good demonstration is a user repairing a reference mismatch while the target list and summary update. A generic red “invalid” banner is not enough.

### F5 — Recovering context may matter more than managing more objects

E06 reports confusion between versions and successful/failed work. E15 offers a technical rationale for explicit assumptions. Neither demonstrates demand for the exact revision UI or many-to-many collections.

**Proposed need N5:** return to a prior review and identify which inputs and evidence supported it.

Preserve request snapshots and evidence associations internally. Show the current context and explain when evidence belongs to an earlier request. Keep ordinary saving separate from scientific-context changes. Renaming a study should not make evidence stale; changing a target or reference should trigger the documented compatibility rules. Full branch/merge history is unnecessary for the course scope.

Open question: users may already solve this adequately with dated folders, notebooks or version control. The interview must inspect those artifacts before deciding the amount of new UI.

### F6 — Handover requires usable content, not merely an export button

E08 recommends archival downloads. E12 demonstrates the distinction between saved state and accessible underlying data. These support a portability question, not proven demand for a new report format.

**Proposed need N6:** let another person understand a review without needing the author's memory or inaccessible local files.

Proposed export: identified request snapshot, source manifest, included evidence records, review dispositions/reasons, unresolved issues, and an explicit list of external dependencies. Preview what is included. A CSV alone may be useful for the lab's next step but can omit context; a machine-readable package alone may be hard for a collaborator to read. Ask to see an actual handover before choosing the minimal combination.

Do not claim that such a package reproduces computation unless the actual execution requirements and inputs are present and tested. For ITU it can reproduce the saved review state.

### F7 — Existing tools and habits may already be good enough

E05 and E13 challenge a generic “researchers need somewhere to save guides” premise. E07 challenges the assumption that a GUI is inherently more usable for a computational operator. E16 demonstrates existing integrated scientific tooling.

**Proposed need N7:** fit into existing work with less transfer effort than the benefit provided.

The application should concentrate on IRCOMP-oriented request preparation and evidence interpretation. It should not replace the laboratory notebook, recreate a genome browser, or require users to retype data already in files. A documented local interchange format is a feasible course boundary, but conversion into it is a real adoption cost. It must be counted in the workflow, not hidden outside the usability test.

If interviews show that conversion is more work than review, prioritize one actually used import path or revise the concept. Do not promise many native tool parsers on the current deadline.

### F8 — Review rationale is plausible, but remains the least demonstrated central need

The sources establish uncertainty and provenance concerns more strongly than candidate-level rationale capture. There is no retained direct evidence that the intended users need named collections with separate decisions for each membership.

**Proposed need N8, low confidence:** preserve why an item was retained, excluded or left unresolved.

Keep editable review decisions as a coherent second ITU module, but treat the organization scheme as a design hypothesis. Start the UI with one default review collection and reveal additional collections when needed. Avoid an elaborate approval vocabulary. A decision is a reviewer's choice for further consideration, not a biological guarantee.

Interview discriminator: ask for a recent selection and how reasons were recorded. If decisions are made only at whole-target level, candidate-level decisions may be the wrong granularity.

## 5. Provisional user and workflow model

These are role assumptions, not invented personas with demographic details.

| Role | Likely task to investigate | Evidence gap |
| --- | --- | --- |
| Computational operator | Prepare explicit inputs, inspect outputs, diagnose mismatches, hand off results | Actual tools, frequency, batch size, input format and tolerance for GUI use |
| Experimental collaborator/reviewer | Understand a selection and its unresolved limitations | Whether this person uses the app directly or only receives an export |
| Future self revisiting work | Recover the context of an earlier review | Whether existing folders/notebooks already solve the problem adequately |

Provisional journey: receive a question → establish target/reference context → prepare request → obtain external computational evidence → check compatibility → inspect observations → record a review decision → hand over/revisit. The ITU app covers preparation and review; external computation is a boundary, not a fake implemented step.

Potential failure points to observe: copying an ambiguous identifier, omitting annotation context, retaining an old setting, attaching output to the wrong request, treating an absent score as poor performance, losing the reason for a choice, or exporting a package whose referenced files are unavailable. These are interview prompts and test hypotheses, not a claim that one observed participant experienced this entire journey.

## 6. Priority and changes to S1

Priority reflects evidence, potential interpretation consequences, thesis fit and delivery cost. It is not a numerical user-importance score.

| Priority | Proposed requirement | Trace | What would change the decision? |
| --- | --- | --- | --- |
| Core | Visible exact target/reference/profile context | N2; E02–E04, E11 | Presentation depth can change; identity must remain explicit |
| Core | Scoped validation with correction paths and preserved edits | N4; E03, E04, E10 | Actual input artifacts determine which diagnostics matter first |
| Core | Source-specific values and explicit missing/unsupported states | N1, N3; E01, E08, E09, E14 | A single-source workflow simplifies layout, not truthfulness |
| Core | Honest evidence category: example/imported, execution not verified where applicable | N3; S1 thesis constraints | Actual execution support would add a separately evidenced state |
| Core, simple UI | Persistent requests, evidence associations and review decisions | N5, N8; E06, E15 plus ITU active-editing need | Interviews determine decision granularity and visible history |
| Next | Portable review export with dependency list | N6; E08, E12 | Recipient's real next step determines format |
| Validate first | Multiple named collections, comparison presets, elaborate revision browser | N8; weak direct support | Concrete examples of alternate shortlists or repeated review justify them |
| Defer | Broad gene resolution, new scoring/consensus, live execution, workflow canvas, collaboration accounts | No adequate justification for bounded ITU scope | Requires deliberate scope change and independent scientific/engineering work |

Recommended S1 refinements:

1. Make context and diagnostics the main preparation story; don't make the number of CRUD objects the product proposition.
2. Give Review one default collection so it works immediately. Retain substantive editable membership and decisions; keep additional collection management secondary.
3. Show evidence source, meaning and uncertainty before decorative aggregate summaries.
4. Keep revision associations in the model; expose a simple “evidence belongs to request revision X” explanation rather than a Git-like history UI.
5. Add **Benchling** to the comparison shortlist. If choosing exactly four systems for S3, prefer CRISPOR, CHOPCHOP, Benchling and Galaxy. IGV remains a useful supplementary pattern for inspection/session portability. Confirm the final set against interview workflows.
6. Test the interval-only entry assumption early. The easiest implementation is not automatically the user's easiest starting point.
7. Count file conversion and metadata entry as user effort. A successful import demonstration alone does not establish an efficient workflow.

These recommendations supplement S1; the original file remains intact so the reasoning is traceable. They do not change the agreed thesis scope or certify permission to reuse assessed work.

## 7. Proposed scenarios for later design and testing

Use small, clearly synthetic fixtures. The scenarios are test plans, not reported results or biological guidance.

| Scenario | Expected application behavior | Observation to collect later |
| --- | --- | --- |
| A supported request contains a mistyped contig/reference identifier | Field-specific problem; correction retains other targets | Does the participant find and repair the issue without guessing? |
| A bundle declares a different reference from the selected request | Explain the mismatch and prevent attaching it as compatible; preserve original data | Can the participant explain why changing a label is not necessarily a repair? |
| Two sources provide differently defined metrics for an explicitly matched record | Keep metrics separate, preserve raw observations, expose metadata | Does the participant mistakenly interpret a combined confidence score that does not exist? |
| One record has numeric zero; another lacks a value | Show different states, including unknown meaning when appropriate | Can the participant explain the difference without being taught first? |
| Analysis-relevant request data changes after review | New context; older evidence stays bound to its original snapshot | Can the participant identify which review is current? |
| A review decision is changed accidentally | Recover the previous choice and rationale | Can the participant recover without recreating the review? |
| A review is reopened and exported | Preserve decisions and context; preview included content and dependencies | Can another person understand what was selected and what remains unresolved? |

For Phase I, these are useful functional acceptance cases for the implemented scope. For Phase II, observe real participants completing tasks and record help requests, interpretation errors, completion and recovery. No completion percentages or time targets are asserted before a baseline exists.

## 8. What is established, and what remains open

Established by the retained evidence: people report score/annotation confusion; reference naming can produce concrete failures; score availability and coordinate conventions require context; existing tools already address substantial parts of the workflow; some computational users prefer scripts and terminals.

Not established: how common each problem is among the intended users; whether the app saves time; how many targets are typical; whether users compare tools; whether candidate-level collections are useful; whether intervals are a viable entry point; desired export formats; willingness to enter metadata; willingness to adopt a separate application.

The next research step should be two concrete workflow walkthroughs, not a vote on the feature list. A strong negative result is valuable: “our existing notebook already handles this” should narrow or change the app rather than be reframed as hidden demand.

## 9. Course status and responsible use of this memo

The supplied ITU assignment (supplied course material) requires an interview or observation with at least one real user per team member. Forum authors are secondary sources, not interview respondents. The chosen two-person equivalent workload includes two real participants. The research guide (supplied course material) recommends 30–45 minutes per research meeting.

**S2 desk research is prepared; S2 primary research remains pending.** This memo can guide recruitment, questioning, comparison and design. It must not be labelled as two interviews or copied into the report as observed user findings. The course explicitly allows AI consultation/search while restricting generation of large project sections; this is a research aid to inspect and use critically, not a finished assessed research chapter.

The supplied Moodle deadline remains **6 November 2026, 23:59**. Schedule the real research early enough for findings to affect the submitted design. The checklist in the companion interview kit explains how to turn actual evidence into the final research section without inventing missing results.
