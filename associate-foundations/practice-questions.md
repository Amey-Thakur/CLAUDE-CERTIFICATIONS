# Practice questions: Associate – Foundations

Thirty-five original practice questions written for this repository against the public [exam blueprint](README.md#skills-measured), in the official item style: scenario-based, one best answer, distractors that fail the stated constraint. They are unofficial practice aids, not items from the live exam, which is covered by a non-disclosure agreement. Coverage follows the domain weights. For unlimited practice, use [Practice with Claude](../guide/practice.md).

**1. Output Evaluation and Validation.** Claude summarizes a vendor contract for you and states that the termination clause requires 60 days' notice, citing section 14.2. You are about to send the summary to your legal team. What should you do first?

- B. Send it, since Claude cited a specific section
- A. Check section 14.2 of the contract and confirm the notice period before sending
- C. Ask Claude how confident it is and send if the confidence is high
- D. Rephrase the summary in more formal language, then send

<details><summary>Answer and rationale</summary>

**A.** Specific-looking citations can be fabricated, and material bound for legal review requires verification against the source document. A specific citation is not evidence of accuracy (B), self-reported confidence is not a reliability signal (C), and rewording does nothing about correctness (D).

</details>

**2. Output Evaluation and Validation.** You ask Claude to draft a competitive analysis, and the output presents market share figures for three competitors without sources. The figures look plausible. What is the appropriate handling?

- A. Include the figures, since plausibility is sufficient for internal documents
- C. Delete the figures and note that no market data was available
- B. Verify each figure against a market research source and keep only what checks out, with citations
- D. Ask Claude to regenerate until the numbers stabilize across runs

<details><summary>Answer and rationale</summary>

**B.** Unsourced quantitative claims are a classic hallucination surface; the professional move is verification against an authoritative source, keeping what survives. Plausibility is not accuracy (A), deleting everything discards genuinely verifiable material (C), and consistency across regenerations does not establish truth (D).

</details>

**3. Prompting and Task Execution.** You need Claude to produce a quarterly report from meeting notes, a spreadsheet summary, and last quarter's report. The first attempt misses the required structure and tone. What is the most effective next step?

- A. Retry the identical prompt, since outputs vary between runs
- C. Rewrite the prompt to state the role, the required sections in order, the tone, and attach last quarter's report as a format example
- B. Switch to the most capable model and resend the same prompt
- D. Break the work into forty single-sentence prompts

<details><summary>Answer and rationale</summary>

**C.** Structure, explicit constraints, and an example of the target format are the most effective fixes for a formatting and tone miss. Re-rolling (A) leaves the deficiency in place, a larger model does not learn unstated requirements (B), and over-fragmentation destroys coherence (D).

</details>

**4. Prompting and Task Execution.** A colleague's prompt asks Claude to "analyze our customer feedback and fix the problems." The output is generic. Which revision best applies task decomposition?

- A. Add "be specific and detailed" to the prompt
- D. Ask first for a categorized list of complaint themes with counts, then for the top three by frequency, then for a proposed action per theme
- B. Ask the same question three times and merge the answers
- C. Paste more feedback into the same prompt

<details><summary>Answer and rationale</summary>

**D.** Decomposition turns a vague compound request into a sequence of verifiable steps, each with a concrete output. Vague intensifiers (A) do not add structure, repetition (B) multiplies the vagueness, and more input without more structure (C) usually worsens focus.

</details>

**5. Product and Model Selection.** Your team drafts hundreds of short, routine customer replies daily, and cost and speed matter more than nuance. Occasionally a complex escalation needs careful reasoning. What is the sound model strategy?

- A. Use the most capable model for everything to maximize quality
- B. Use the fastest, lowest-cost model for routine replies and switch to a more capable model for the complex escalations
- C. Use the fastest model for everything, including escalations
- D. Alternate models randomly to balance the load

<details><summary>Answer and rationale</summary>

**A** wastes cost and latency budget on routine work; **C** underserves exactly the cases that need depth; **D** matches nothing to anything. **B** aligns model choice with task requirements in both directions, which is the tested judgment.

</details>

**6. Workflow Integration and Solution Design.** Your monthly close process involves collecting figures, drafting a variance commentary, and formatting a board pack. You want Claude to help durably, not just once. What is the strongest approach?

- B. Paste everything into a fresh chat each month and ask for the pack
- A. Create a Project with the commentary conventions and prior packs as knowledge, plus instructions for the structure, and run each close inside it
- C. Ask Claude to do the whole close autonomously, including pulling the figures
- D. Use Claude only for spellchecking the final pack

<details><summary>Answer and rationale</summary>

**A.** Durable, repeated workflows belong in a Project where instructions and knowledge persist and improve. Re-pasting monthly (B) rebuilds context by hand every time, full autonomy over financial figures without review (C) ignores appropriate-use judgment, and spellchecking (D) forfeits the actual value.

</details>

**7. Workflow Integration and Solution Design.** A department head asks you whether Claude could "handle our customer onboarding." What is the right first move?

- A. Say yes and start building immediately
- B. Map the onboarding steps, identify which involve drafting, summarizing, or lookup that Claude does well, and which need human judgment or system access it does not have
- C. Say no, since onboarding involves customer data
- D. Forward the question to Anthropic support

<details><summary>Answer and rationale</summary>

**B.** The Associate's core skill is translating a business ask into a realistic division of labor: where Claude adds value, where humans stay, and what the limits are. Unqualified yes (A) and unqualified no (C) both skip the analysis, and support (D) does not know your process.

</details>

**8. Configuration and Knowledge Management.** Your team's Project answers policy questions from an uploaded handbook. HR publishes a new handbook version. What must happen for the Project to stay trustworthy?

- A. Nothing; Claude will find the new version on its own
- C. Replace the outdated handbook in the Project knowledge and spot-check answers against the new version
- B. Add the new handbook alongside the old one so both are available
- D. Tell users to mention the new version in every prompt

<details><summary>Answer and rationale</summary>

**C.** Project knowledge is maintained, not self-updating; stale sources are a quality defect the configurer owns. Claude does not fetch your internal documents on its own (A), keeping both versions invites contradictory answers (B), and pushing the burden onto every user (D) is not maintenance.

</details>

**9. Governance, Risk, and Responsible Use.** You want Claude to analyze churn patterns in an export that includes customer names, emails, and account numbers. Company policy forbids sharing personal data with external tools. What is the correct action?

- A. Upload the file, since churn analysis is an internal purpose
- B. Upload it but instruct Claude to ignore the personal columns
- D. Remove or pseudonymize the identifying columns first, then upload and analyze
- C. Abandon the analysis

<details><summary>Answer and rationale</summary>

**D.** Make the task compliant, then do it: the identifiers are not needed for pattern analysis. Purpose does not override policy (A), an instruction to ignore data is not a control because the data still left the boundary (B), and abandoning the work (C) is unnecessary when anonymization enables it.

</details>

**10. Troubleshooting and Optimization.** A prompt that worked well for weeks now produces off-target answers after your team added many new documents to the Project. What is the best first diagnostic?

- B. Rewrite the prompt from scratch
- A. Check whether the newly added knowledge is diluting or contradicting the sources the answers should draw from
- C. Switch to a larger model
- D. Delete the Project and start over

<details><summary>Answer and rationale</summary>

**A.** The change that coincided with the regression is the first suspect: new knowledge can crowd out or conflict with the relevant sources. Rewriting the prompt (B), upgrading the model (C), or rebuilding everything (D) all treat symptoms before diagnosing the actual change.

</details>

**11. Output Evaluation and Validation.** Claude produces a competitor comparison table where one row is marked “data unavailable” and the rest are filled in. A colleague asks you to delete the empty row so the table looks complete. What is the right response?

- A. Delete the row, since an incomplete table undermines confidence
- B. Keep the row and its label, because the gap is itself a finding the reader needs
- C. Fill the row with a reasonable estimate and mark it as approximate
- D. Ask Claude to search harder until every row is populated

<details><summary>Answer and rationale</summary>

**B.** A declared gap is information: it tells the reader where the analysis is thin. Deleting it (A) hides a limitation, an unmarked estimate (C) manufactures data, and pressing the model to fill the cell (D) invites fabrication rather than retrieval.

</details>

**12. Output Evaluation and Validation.** Two runs of the same prompt give different figures for the same metric. Which conclusion is supported?

- A. The higher figure is more likely correct because the model found more evidence
- C. Neither figure is established, and the metric must be checked against the source
- B. The figures should be averaged to reduce variance
- D. The prompt is fine and the model needs a longer context window

<details><summary>Answer and rationale</summary>

**C.** Disagreement between runs shows the figure is not grounded in a reliable source, so neither is established. Preferring the larger number (A) is arbitrary, averaging (B) treats two unverified numbers as measurements, and context length (D) is unrelated to whether the figure is true.

</details>

**13. Output Evaluation and Validation.** You ask Claude to extract every payment term from a 40-page contract. The output lists four terms, cleanly formatted. What is the first check?

- A. Confirm the formatting is consistent across the four entries
- D. Read the contract's payment sections to confirm no term was omitted
- B. Ask Claude whether it found all of them
- C. Run it again at a higher temperature to surface more terms

<details><summary>Answer and rationale</summary>

**D.** Extraction fails by omission more often than by error, and a tidy output gives no signal about completeness. Formatting (A) is cosmetic, self-report (B) is not evidence, and temperature (C) changes phrasing rather than recall.

</details>

**14. Output Evaluation and Validation.** A summary you commissioned states a conclusion that contradicts your own reading of the source. What should you do?

- B. Defer to the summary, since the model read the whole document
- C. Defer to your reading and treat the summary as wrong
- A. Locate the passage the conclusion rests on and compare it against both readings
- D. Ask a colleague which of the two sounds more plausible

<details><summary>Answer and rationale</summary>

**A.** The disagreement is resolvable by returning to the passage in question, which settles it on evidence. Deferring either way (B, C) decides without checking, and canvassing opinion (D) substitutes plausibility for the source.

</details>

**15. Output Evaluation and Validation.** Claude produces a well-argued recommendation with no citations, on a topic where you have no expertise. What is the appropriate use of it?

- A. Adopt it, since the reasoning is internally consistent
- B. Treat it as a hypothesis to test against sources before acting
- C. Discard it, because unsourced output has no value
- D. Ask for citations and adopt whatever comes back

<details><summary>Answer and rationale</summary>

**B.** Unsourced reasoning is a starting point, useful for structuring an enquiry but not for deciding. Internal consistency is not accuracy (A), the reasoning may still be useful (C), and citations produced on demand need the same verification as the claim (D).

</details>

**16. Workflow Integration and Solution Design.** A team wants Claude to draft weekly customer health summaries from support tickets, CRM notes, and usage data. Which design detail matters most for the output to stay useful over months?

- A. Choosing the largest available model
- C. Defining what a health summary must contain and keeping that definition in one place the team maintains
- B. Running the summary daily instead of weekly
- D. Letting each team member write their own prompt

<details><summary>Answer and rationale</summary>

**C.** A stable, maintained definition of the deliverable is what keeps output consistent as people and inputs change. Model size (A) does not fix an undefined task, higher frequency (B) multiplies an unclear output, and per-person prompts (D) guarantee drift.

</details>

**17. Workflow Integration and Solution Design.** Which task in a monthly reporting process is the weakest candidate for delegation to Claude?

- A. Drafting the narrative summary from agreed figures
- B. Reformatting last month's report into the new template
- D. Deciding which underperforming account to escalate to the executive team
- C. Extracting the top five variances from a spreadsheet export

<details><summary>Answer and rationale</summary>

**D.** The escalation decision carries accountability and depends on relationships and context the model does not hold. Drafting (A), reformatting (B), and extraction (C) are all bounded tasks with checkable output.

</details>

**18. Workflow Integration and Solution Design.** A process works well for one analyst and poorly for three others using the same prompt. What is the most likely cause?

- B. The other three need a more capable model
- A. The prompt relies on context the first analyst supplies without noticing
- C. The task is unsuitable for Claude
- D. The other three are using shorter inputs

<details><summary>Answer and rationale</summary>

**A.** One person succeeding with the same prompt usually means they are contributing unstated context, such as knowing which file to attach or what good looks like. A model change (B) does not supply missing context, the task clearly works (C), and input length (D) is a symptom rather than a cause.

</details>

**19. Workflow Integration and Solution Design.** When is it appropriate to keep a human approval step in an otherwise automated Claude workflow?

- A. Always, since automation is inherently risky
- B. When the action is hard to reverse or carries external consequences
- C. Only while the workflow is new, then remove it
- D. Never, because approval steps defeat the purpose of automation

<details><summary>Answer and rationale</summary>

**B.** Approval earns its cost where a mistake is expensive or hard to undo. Blanket approval (A) and blanket removal (D) both ignore the specific risk, and a time-based rule (C) removes the check regardless of what the action does.

</details>

**20. Governance, Risk, and Responsible Use.** A colleague proposes pasting a customer list into a prompt to draft personalised outreach. What is the correct handling?

- A. Proceed, since the prompt is not stored anywhere permanent
- C. Remove or replace identifying details before drafting, and reattach them afterwards
- B. Ask Claude to keep the names confidential
- D. Proceed but delete the conversation afterwards

<details><summary>Answer and rationale</summary>

**C.** Working on anonymised data and reattaching identifiers afterwards achieves the task without exposing the personal data. Assumptions about storage (A) are not a control, an instruction to the model (B) is not a safeguard, and deleting afterwards (D) does not undo the disclosure.

</details>

**21. Governance, Risk, and Responsible Use.** Which statement about instructing a model not to do something is accurate?

- A. An instruction in the prompt is an enforceable control
- D. An instruction shapes behaviour but does not guarantee it, so controls belong outside the prompt
- B. Instructions are enforceable if placed in a system prompt
- C. Instructions are enforceable if repeated several times

<details><summary>Answer and rationale</summary>

**D.** Prompt instructions influence behaviour and are not guarantees, so anything that must hold is enforced in the surrounding system. Placement (B) and repetition (C) change the strength of the steer, not its nature, and treating it as enforcement (A) is the error the question tests.

</details>

**22. Governance, Risk, and Responsible Use.** A regulated report drafted with Claude is about to be filed. What is the reviewer accountable for?

- B. Confirming that Claude was used according to policy
- A. The accuracy and compliance of the filed document, regardless of how it was drafted
- C. Confirming the prompt included the relevant regulations
- D. Recording which model version produced the draft

<details><summary>Answer and rationale</summary>

**A.** Accountability sits with the person who files, and the tool used does not transfer it. Policy compliance (B), prompt content (C), and version records (D) are all reasonable practices that do not replace responsibility for the document.

</details>

**23. Governance, Risk, and Responsible Use.** When is disclosing that AI assisted a piece of work most clearly warranted?

- A. Whenever any AI tool touched the work at any stage
- B. When the audience's judgment of the work depends on how it was produced
- C. Only when the output is published externally
- D. Only when a written policy requires it

<details><summary>Answer and rationale</summary>

**B.** Disclosure matters where provenance would change how a reader weighs the work. A universal rule (A) makes the signal meaningless, and confining it to external publication (C) or written policy (D) misses internal cases where it genuinely matters.

</details>

**24. Prompting and Task Execution.** A prompt produces output that is accurate but consistently too long. What is the most reliable fix?

- A. Add “be concise” to the prompt
- C. State the limit in concrete terms, such as a word count or a number of bullet points
- B. Ask for a summary of the output afterwards
- D. Use a smaller model

<details><summary>Answer and rationale</summary>

**C.** Concrete limits are checkable and reproducible in a way that adjectives are not. “Be concise” (A) is interpreted differently each run, summarising afterwards (B) adds a step and a second failure point, and a smaller model (D) trades accuracy for brevity.

</details>

**25. Prompting and Task Execution.** You need output in a specific structure every time so it can be pasted into a template. What is the most effective technique?

- A. Describing the structure in prose at the end of the prompt
- D. Providing a filled example of the exact structure you want
- B. Asking for the output to be well organised
- C. Requesting the output twice and taking the better one

<details><summary>Answer and rationale</summary>

**D.** An example specifies the target unambiguously and is the strongest available signal for format. Prose description (A) leaves room for interpretation, a vague request (B) leaves more, and generating twice (C) does not define the target at all.

</details>

**26. Prompting and Task Execution.** A long prompt with many rules produces output that follows some rules and ignores others. What should you try first?

- B. Repeating the ignored rules in capitals
- A. Separating the task into stages so each output is checked before the next
- C. Moving all the rules to the top of the prompt
- D. Adding a rule that says all rules must be followed

<details><summary>Answer and rationale</summary>

**A.** Splitting the work reduces how much must hold at once and gives a checkpoint between stages. Emphasis (B), ordering (C), and a meta-rule (D) all leave the same load in a single step.

</details>

**27. Prompting and Task Execution.** Which detail most improves a prompt asking Claude to review a document?

- A. Stating that the review should be thorough
- B. Stating what the review is for and what would count as a problem
- C. Attaching several similar documents for comparison
- D. Asking for the review as a numbered list

<details><summary>Answer and rationale</summary>

**B.** Purpose and criteria tell the model what to look for, which is what a review depends on. Thoroughness (A) is unmeasurable, extra documents (C) add noise without criteria, and formatting (D) shapes presentation rather than substance.

</details>

**28. Product and Model Selection.** A task involves reading a 200-page report once and answering a single question. Which consideration should lead the choice?

- A. The cheapest model available, since the task runs once
- C. Whether the model can hold and reason over the whole document reliably
- B. Whether the model supports the fastest response time
- D. Whether the task can be split across several small models

<details><summary>Answer and rationale</summary>

**C.** The binding constraint is reliable comprehension across a long document, which is what the choice must satisfy. Cost (A) and speed (B) matter only among models that can do the task, and splitting (D) risks losing the cross-document reasoning the question needs.

</details>

**29. Product and Model Selection.** When does working in a Claude project make more sense than an API integration?

- D. When the work is exploratory and done by people rather than systems
- A. When the volume is high and predictable
- B. When the output must be inserted into another system automatically
- C. When the task must run on a schedule

<details><summary>Answer and rationale</summary>

**D.** Projects suit human, iterative work where the context is curated and reused by people. High volume (A), programmatic handoff (B), and scheduling (C) all describe system integration, which is what the API is for.

</details>

**30. Product and Model Selection.** A team asks whether to move to a larger model because outputs are inconsistent. What should be established first?

- B. The cost difference between the two models
- A. Whether the inconsistency comes from the prompt and the inputs rather than the model
- C. Whether the larger model is available in their region
- D. How much faster the current model is

<details><summary>Answer and rationale</summary>

**A.** Inconsistency usually traces to an underspecified task or variable inputs, which a larger model does not fix. Cost (B), availability (C), and speed (D) are inputs to a decision that has not yet been shown to be the right one.

</details>

**31. Configuration and Knowledge Management.** What belongs in a project's knowledge rather than in individual prompts?

- A. The specific question being asked today
- B. Material that every conversation in the project should be able to draw on
- C. The preferred output length for one report
- D. A one-off document being reviewed this week

<details><summary>Answer and rationale</summary>

**B.** Project knowledge holds what recurs, so each conversation starts from the same base. Today's question (A), a single formatting preference (C), and a one-off document (D) all belong in the prompt that needs them.

</details>

**32. Configuration and Knowledge Management.** A project's answers have grown vaguer as more documents were added. What is the likely cause?

- A. The model version changed
- C. The knowledge now holds overlapping or outdated material competing with the right sources
- B. The project has too few documents to ground answers
- D. The prompts have become too specific

<details><summary>Answer and rationale</summary>

**C.** Accumulated, unmaintained knowledge dilutes retrieval, and the symptom is exactly this drift toward vagueness. A version change (A) is unrelated to what was added, and both too few documents (B) and overly specific prompts (D) contradict the described trend.

</details>

**33. Configuration and Knowledge Management.** How should project knowledge be treated as the underlying material changes?

- A. It updates automatically from the source systems
- D. It must be maintained deliberately, because it does not update itself
- B. It only needs review when answers are visibly wrong
- C. It should be rebuilt from scratch each quarter

<details><summary>Answer and rationale</summary>

**D.** Project knowledge is a curated copy and stays as accurate as the person maintaining it. It does not sync (A), waiting for visible errors (B) means acting after the damage, and periodic rebuilds (C) are wasteful and still unscheduled against real change.

</details>

**34. Troubleshooting and Optimization.** A workflow that has run reliably for months begins returning off-target output. What is the first diagnostic step?

- B. Rewrite the prompt from scratch
- A. Establish what changed: the inputs, the configuration, or the knowledge
- C. Switch to a different model
- D. Increase the amount of context supplied

<details><summary>Answer and rationale</summary>

**A.** A working system that degrades points to a change, and identifying it is faster and safer than rebuilding. Rewriting (B), switching models (C), and adding context (D) all alter the system before the cause is known.

</details>

**35. Troubleshooting and Optimization.** Output quality is acceptable but the process takes too long to be worth using. What should be examined first?

- A. Whether a faster model would meet the quality bar
- B. Whether the slow part is the model or the human steps around it
- C. Whether the prompt can be shortened
- D. Whether the task should be abandoned

<details><summary>Answer and rationale</summary>

**B.** Locating the actual delay comes before optimising anything, and in practice the surrounding steps often dominate. Changing the model (A) or the prompt (C) assumes the model is the bottleneck, and abandoning (D) discards a process that already produces acceptable output.

</details>

---

These questions are the maintainer's original work for self-assessment. [Study guide](README.md) · [Study notes](notes.md) · [Mock exam](mock-exam-1.md) · [Repository index](../README.md)
