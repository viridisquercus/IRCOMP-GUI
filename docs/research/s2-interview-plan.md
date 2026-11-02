# S2 — Interview kit and hypothesis checks

Prepared 1 November 2026. This is a plan, not a record of completed research. Read alongside [desk research](s2-desk-research.md) and [current project scope](../report/phase-i.md).

## Recruit for relevant behavior

For the chosen two-person equivalent workload, interview two real people separately. Prefer one computational researcher who recently prepared/reviewed relevant genomic or CRISPR outputs, and one researcher involved in interpreting or receiving such results. If the second is only a recipient, explicitly distinguish that role from the operator. Do not describe a general software student as a domain user without relevant experience.

A participant with adjacent genomics experience can reveal transferable workflow issues; record the domain difference and do not turn their account into CRISPR-specific evidence. Ask about a recent concrete task and an artifact they can comfortably show. No sensitive dataset is needed: a sanitized example, blank structure or narrated walkthrough can suffice.

## 35–45 minute session

### Opening — 3 minutes

Explain that the purpose is to understand their current work, not test their expertise. Ask permission to take notes and separately obtain consent for recording if used. Explain how their identity and artifacts will be handled. Do not promise anonymity if the actual report will identify them; use participant codes where possible.

### Recent task and context — 7 minutes

1. “Tell me about the most recent analysis where you prepared inputs or reviewed candidate results. What question were you trying to answer?”
2. “What did you receive at the beginning, and what did someone need from you at the end?”
3. “Which steps did you do yourself, and which were done by somebody else?”

Record role, frequency, approximate task size, tools and collaborators. Do not introduce the proposed app yet.

### Walkthrough — 12 minutes

4. “Could you walk me through that task using the files or screens you normally use?”
5. “How did you establish which reference, target or annotation these data describe?”
6. “What information did you copy between tools? What did you have to enter again?”
7. “How could you tell the output belonged to this particular input or version?”

Observe actual labels, filenames, conventions, scripts and notes. Distinguish behavior observed on screen from what the participant remembers. Ask “what happened next?” before suggesting possible problems.

### Decisions and difficult cases — 10 minutes

8. “How did you decide what to keep or investigate further? Can you show one example?”
9. “Was anything confusing or unexpected? What did you do then?” If there was no incident, accept that answer.
10. “When a value is absent or results differ, how do you work out what that means?” Ask only if relevant to their workflow; do not assume multi-tool comparison.
11. “Where did you record the reason for the decision? Would someone else be able to recover it?”
12. “What was the most expensive part in time or repeated work? What already works well?”

Probe with concrete follow-ups: last occurrence, actual consequence, workaround, who helped, and what artifact remains. Never convert a guess about frequency into a measured frequency.

### Handover and concept check — 5–10 minutes

13. “What do you send onward? What does the recipient need to open or interpret it?”
14. “If you reopened this in a month, how would you know which version to use?”
15. Only now show a brief neutral concept: an editor for explicit requests and a view of imported evidence with saved review decisions. “Where, if anywhere, would this fit? What would it duplicate? What extra work would it create?”
16. “Which single part of your actual task would you want improved first?”

Concept reactions are weaker than demonstrated behavior. Record them separately. Do not ask “Would clear provenance be useful?” or “Would you use our easy-to-use app?”

## Hypotheses and ways to disprove them

| Hypothesis from desk research | Evidence to seek | Disconfirming evidence and design response |
| --- | --- | --- |
| H1: source/context interpretation causes review friction | A recent conflicting/unclear output and the steps used to resolve it | One trusted source with adequate labels: simplify comparison UI |
| H2: explicit identity checks save rework | A mismatch, uncertainty, manual checking step or accepted automatic check | Existing pipeline guarantees identity: import its manifest, avoid re-entering metadata |
| H3: an interval-first editor fits the operator | Participant shows where exact intervals come from | They begin only with genes and cannot establish intervals: reconsider entry boundary or recruit the actual computational preparer |
| H4: version associations need a visible UI | Participant struggles to identify the current request/output pair | Existing naming/versioning is sufficient: keep associations internal and presentation minimal |
| H5: candidate-level rationale and collections matter | Examples of alternative selections and recorded reasons | Decisions are whole-target or recorded elsewhere: change granularity or export into existing record |
| H6: a new GUI reduces total effort | Existing multi-step task has a clear point of avoidable work | Conversion and metadata entry outweigh benefit: narrow integration or revise concept |
| H7: a portable review package helps a recipient | Actual handover missing needed context | Recipient wants a specific existing format: prioritize that format rather than a new report system |

## Notes template — make one copy per participant

- Participant code, date, duration, interviewer:
- Role and relevant experience (self-reported):
- Consent and permitted artifact/quotation use:
- Concrete recent task and desired outcome:
- Tools/files and step sequence:
- Observed behavior, with note timestamp or artifact reference:
- Reported behavior not directly observed:
- Problem/obstacle and actual consequence:
- Existing workaround and what works well:
- Exact quote, only if accurately recorded and permitted:
- Researcher interpretation, clearly separated:
- Hypotheses supported, contradicted or still unknown:
- Proposed requirement and why the evidence supports it:
- Limitations of the session:

Do not prefill findings or quotes from the desk research. Keep participant evidence codes such as P01-O01 (observation) and P01-R01 (reported account) distinct from E01–E16 public sources.

## Synthesis after both sessions

Build a compact traceability table: participant evidence → concrete human/process need → proposed requirement → design location → later test scenario. Retain conflicting needs and negative findings. One incident supports the existence of an issue for that person, not a statement that all researchers face it. Two similar accounts are useful corroboration, not statistical prevalence.

Compare results with desk hypotheses. Label each confirmed for this participant, contradicted, partly supported, or untested. Update the S1 scope before freezing the model/API and screens. Do not solve a late disagreement by promising an entirely new scientific pipeline.

For the ITU report, TODO: write the actual recruitment/method/context, participants' relevant roles, observed/reported needs, limitations and resulting design decisions, with required author identification. Desk sources remain labelled secondary research. Attach only consented supporting material. Keep the interview records separate from later Phase II usability test results.

Completion check: two real sessions under the chosen workload; accurate notes; evidence-linked needs; explicit contradictions; justified design changes; no fabricated participant details; and sufficient time before the 6 November 2026 submission for those changes to matter.
