# Practice questions: Associate – Foundations

Ten original practice questions written for this repository against the public [exam blueprint](README.md#skills-measured), in the official item style: scenario-based, one best answer, distractors that fail the stated constraint. They are unofficial practice aids, not items from the live exam, which is covered by a non-disclosure agreement. Coverage follows the domain weights. For unlimited practice, use [Practice with Claude](../guide/practice.md).

**1. Output Evaluation and Validation.** Claude summarizes a vendor contract for you and states that the termination clause requires 60 days' notice, citing section 14.2. You are about to send the summary to your legal team. What should you do first?

- A. Send it, since Claude cited a specific section
- B. Check section 14.2 of the contract and confirm the notice period before sending
- C. Ask Claude how confident it is and send if the confidence is high
- D. Rephrase the summary in more formal language, then send

<details><summary>Answer and rationale</summary>

**B.** Specific-looking citations can be fabricated, and material bound for legal review requires verification against the source document. A specific citation is not evidence of accuracy (A), self-reported confidence is not a reliability signal (C), and rewording does nothing about correctness (D).

</details>

**2. Output Evaluation and Validation.** You ask Claude to draft a competitive analysis, and the output presents market share figures for three competitors without sources. The figures look plausible. What is the appropriate handling?

- A. Include the figures, since plausibility is sufficient for internal documents
- B. Delete the figures and note that no market data was available
- C. Verify each figure against a market research source and keep only what checks out, with citations
- D. Ask Claude to regenerate until the numbers stabilize across runs

<details><summary>Answer and rationale</summary>

**C.** Unsourced quantitative claims are a classic hallucination surface; the professional move is verification against an authoritative source, keeping what survives. Plausibility is not accuracy (A), deleting everything discards genuinely verifiable material (B), and consistency across regenerations does not establish truth (D).

</details>

**3. Prompting and Task Execution.** You need Claude to produce a quarterly report from meeting notes, a spreadsheet summary, and last quarter's report. The first attempt misses the required structure and tone. What is the most effective next step?

- A. Retry the identical prompt, since outputs vary between runs
- B. Rewrite the prompt to state the role, the required sections in order, the tone, and attach last quarter's report as a format example
- C. Switch to the most capable model and resend the same prompt
- D. Break the work into forty single-sentence prompts

<details><summary>Answer and rationale</summary>

**B.** Structure, explicit constraints, and an example of the target format are the most effective fixes for a formatting and tone miss. Re-rolling (A) leaves the deficiency in place, a larger model does not learn unstated requirements (C), and over-fragmentation destroys coherence (D).

</details>

**4. Prompting and Task Execution.** A colleague's prompt asks Claude to "analyze our customer feedback and fix the problems." The output is generic. Which revision best applies task decomposition?

- A. Add "be specific and detailed" to the prompt
- B. Ask first for a categorized list of complaint themes with counts, then for the top three by frequency, then for a proposed action per theme
- C. Ask the same question three times and merge the answers
- D. Paste more feedback into the same prompt

<details><summary>Answer and rationale</summary>

**B.** Decomposition turns a vague compound request into a sequence of verifiable steps, each with a concrete output. Vague intensifiers (A) do not add structure, repetition (C) multiplies the vagueness, and more input without more structure (D) usually worsens focus.

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

- A. Paste everything into a fresh chat each month and ask for the pack
- B. Create a Project with the commentary conventions and prior packs as knowledge, plus instructions for the structure, and run each close inside it
- C. Ask Claude to do the whole close autonomously, including pulling the figures
- D. Use Claude only for spellchecking the final pack

<details><summary>Answer and rationale</summary>

**B.** Durable, repeated workflows belong in a Project where instructions and knowledge persist and improve. Re-pasting monthly (A) rebuilds context by hand every time, full autonomy over financial figures without review (C) ignores appropriate-use judgment, and spellchecking (D) forfeits the actual value.

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
- B. Replace the outdated handbook in the Project knowledge and spot-check answers against the new version
- C. Add the new handbook alongside the old one so both are available
- D. Tell users to mention the new version in every prompt

<details><summary>Answer and rationale</summary>

**B.** Project knowledge is maintained, not self-updating; stale sources are a quality defect the configurer owns. Claude does not fetch your internal documents on its own (A), keeping both versions invites contradictory answers (C), and pushing the burden onto every user (D) is not maintenance.

</details>

**9. Governance, Risk, and Responsible Use.** You want Claude to analyze churn patterns in an export that includes customer names, emails, and account numbers. Company policy forbids sharing personal data with external tools. What is the correct action?

- A. Upload the file, since churn analysis is an internal purpose
- B. Upload it but instruct Claude to ignore the personal columns
- C. Remove or pseudonymize the identifying columns first, then upload and analyze
- D. Abandon the analysis

<details><summary>Answer and rationale</summary>

**C.** Make the task compliant, then do it: the identifiers are not needed for pattern analysis. Purpose does not override policy (A), an instruction to ignore data is not a control because the data still left the boundary (B), and abandoning the work (D) is unnecessary when anonymization enables it.

</details>

**10. Troubleshooting and Optimization.** A prompt that worked well for weeks now produces off-target answers after your team added many new documents to the Project. What is the best first diagnostic?

- A. Rewrite the prompt from scratch
- B. Check whether the newly added knowledge is diluting or contradicting the sources the answers should draw from
- C. Switch to a larger model
- D. Delete the Project and start over

<details><summary>Answer and rationale</summary>

**B.** The change that coincided with the regression is the first suspect: new knowledge can crowd out or conflict with the relevant sources. Rewriting the prompt (A), upgrading the model (C), or rebuilding everything (D) all treat symptoms before diagnosing the actual change.

</details>

---

These questions are the maintainer's original work for self-assessment. [Study guide](README.md) · [Study notes](notes.md) · [Repository index](../README.md)
