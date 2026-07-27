# Practice questions: Architect – Foundations

Ten original practice questions written for this repository against the public [exam blueprint](README.md#skills-measured), framed inside the [six published scenarios](README.md#the-six-exam-scenarios) the way the real exam frames its items. They are unofficial practice aids, not items from the live exam, which is covered by a non-disclosure agreement. For unlimited practice, use [Practice with Claude](../guide/practice.md) or the repository's built-in exam coach skill.

**1. Support resolution agent, Agentic Architecture.** Your support agent resolves most tickets but sometimes loops indefinitely, re-calling lookup_order on the same order. What is the correct structural fix?

- A. Raise max_tokens so the loop has room to finish
- B. Add explicit loop-termination conditions: cap tool iterations, detect repeated identical calls, and route to escalate_to_human when progress stalls
- C. Remove the lookup_order tool
- D. Lower the temperature

<details><summary>Answer and rationale</summary>

**B.** Agent loops need engineered termination: iteration budgets, repeated-call detection, and an escalation path when the agent cannot progress. Token budget (A) delays the symptom, removing a needed tool (C) breaks resolution, and temperature (D) does not bound iteration.

</details>

**2. Support resolution agent, Tool Design.** process_refund currently accepts any amount. Support policy caps agent-initiated refunds at $200; larger refunds need a human. Where does that rule belong?

- A. In the system prompt, phrased firmly
- B. Enforced in the tool layer: the tool rejects amounts over the cap with a structured error, and a hook or the tool itself routes larger cases to escalation
- C. In the model's reasoning, since it reads the policy
- D. In quarterly staff training

<details><summary>Answer and rationale</summary>

**B.** Hard policy limits are enforced deterministically at the tool boundary, not requested of the model. Prompt phrasing (A) and model reasoning (C) are probabilistic where the requirement is absolute, and training (D) does not constrain the agent at all.

</details>

**3. Multi-agent research, Agentic Architecture.** Your coordinator delegates to search, analysis, and report subagents. Final reports cite sources that do not support their claims, though each subagent behaves sensibly alone. What is the most likely architectural cause?

- A. The report subagent's model is too small
- B. Provenance is lost at handoffs: findings and their sources are not passed together in a structured form, so the report writer pairs claims with citations by guesswork
- C. The web is unreliable
- D. Too many subagents are running in parallel

<details><summary>Answer and rationale</summary>

**B.** In multi-agent pipelines, provenance survives only if the handoff format carries claim and source together. That failure mode produces exactly this symptom while every stage looks locally fine. Model size (A), source quality (C), and parallelism (D) do not explain correct facts paired with wrong citations.

</details>

**4. Multi-agent research, Context Management.** The analysis subagent returns 30,000-token document dumps to the coordinator, which then fails on context limits. What is the right fix?

- A. Give the coordinator a bigger context window
- B. Have subagents return structured extracts, findings with citations and confidence, while full documents stay in the subagent's context or a scratchpad file
- C. Have the coordinator drop the oldest messages silently
- D. Run the analysis twice and keep the shorter answer

<details><summary>Answer and rationale</summary>

**B.** Context isolation is the point of subagent delegation: raw bulk stays at the edge, distilled results travel. A larger window (A) postpones the failure, silent dropping (C) loses arbitrary information, and rerunning (D) changes nothing structural.

</details>

**5. Claude Code for development, Configuration.** Your monorepo has frontend and backend directories with different conventions, and one team-wide rule about commit style. Where does each piece of configuration belong?

- A. Everything in one root CLAUDE.md
- B. The commit rule in the project-level CLAUDE.md; the per-area conventions in path-scoped rules under .claude/rules/ that load only when matching files are touched
- C. Each engineer's personal user-level CLAUDE.md
- D. A wiki page linked from the README

<details><summary>Answer and rationale</summary>

**B.** The hierarchy exists for exactly this: shared rules at project scope, conditional conventions path-scoped so context is spent only where relevant. One root file (A) loads everything everywhere, personal files (C) diverge per engineer, and a wiki (D) never reaches the model.

</details>

**6. Claude Code in CI, Workflows.** Your CI job runs Claude Code to review pull requests, and the pipeline must parse the results mechanically. Which invocation is correct?

- A. Interactive mode with a human copying the output into CI
- B. Non-interactive mode with -p, with --output-format json and a schema so the review arrives as machine-readable, validated output
- C. Plan mode, which is safer for automation
- D. A shell script that greps the human-readable transcript

<details><summary>Answer and rationale</summary>

**B.** Headless CI use is what -p with JSON output and a schema is for: deterministic invocation, parseable results. A human in the loop (A) is not CI, plan mode (C) is a review gate for interactive work rather than an output format, and grepping prose (D) breaks on the first wording change.

</details>

**7. Claude Code in CI, Prompt Engineering.** The automated reviewer flags dozens of trivial style nits per pull request, and engineers have started ignoring it. Which change addresses the false-positive problem the way the blueprint suggests?

- A. Run the review twice and post only findings that appear both times
- B. Define explicit review criteria in the prompt: what to flag, what to ignore, and a severity bar, with a few worked examples of in-scope and out-of-scope findings
- C. Cap the reviewer at three findings per pull request
- D. Route all findings to a channel nobody reads

<details><summary>Answer and rationale</summary>

**B.** Precision comes from explicit criteria and few-shot examples that draw the boundary between signal and noise. Double-running (A) filters randomness but not systematic nit-picking, an arbitrary cap (C) drops real findings on bad days, and (D) is surrender.

</details>

**8. Structured data extraction, Structured Output.** Invoices sometimes lack a purchase-order number, and your extraction schema must handle that honestly while catching real misses. What is the right schema design?

- A. Make every field required so nothing is missed
- B. Make purchase_order nullable, so absence is recorded as null, and validate that it is present whenever the document type requires it
- C. Make everything optional to avoid validation errors
- D. Have the model invent a plausible number when one is missing

<details><summary>Answer and rationale</summary>

**B.** Schema design encodes reality: genuinely optional data is nullable, and conditional requirements are validated downstream. All-required (A) forces fabrication or failure on legitimate documents, all-optional (C) blinds you to true misses, and invention (D) is data corruption.

</details>

**9. Structured data extraction, Reliability.** Your pipeline reports 98% field accuracy, measured on the documents the schema validated cleanly. An auditor calls the number misleading. Why?

- A. Accuracy should be measured only on the hardest documents
- B. Validation-clean documents are a biased sample: the honest measure comes from a labeled sample drawn across all documents, including ones that failed or barely passed validation
- C. 98% is below industry standard
- D. Field accuracy is not a real metric

<details><summary>Answer and rationale</summary>

**B.** Measuring only where the system already succeeded inflates the estimate; calibration requires a labeled sample representative of the full input stream. Hardest-only (A) biases in the opposite direction, the standard claim (C) is invented, and (D) is false.

</details>

**10. Developer productivity agent, Tool Design.** Your codebase-exploration agent has get_file_contents, read_source, and fetch_file tools that all read files, and it frequently picks poorly among them. What is the correct fix?

- A. Add a fourth, better file-reading tool
- B. Consolidate to one file-reading tool, or give the survivors sharply differentiated descriptions that state exactly when each applies
- C. Fine-tune the model on the tool list
- D. Randomize which tool the harness dispatches

<details><summary>Answer and rationale</summary>

**B.** Tool selection runs on descriptions; overlapping tools with vague descriptions produce dithering. Consolidation or sharp differentiation is the documented cure. Adding overlap (A) worsens it, fine-tuning (C) is disproportionate, and randomization (D) institutionalizes the confusion.

</details>

---

These questions are the maintainer's original work for self-assessment. [Study guide](README.md) · [Study notes](notes.md) · [Repository index](../README.md)
