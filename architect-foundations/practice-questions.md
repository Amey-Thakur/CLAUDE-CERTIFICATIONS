# Practice questions: Architect – Foundations

Thirty-five original practice questions written for this repository against the public [exam blueprint](README.md#skills-measured), framed inside the [six published scenarios](README.md#the-six-exam-scenarios) the way the real exam frames its items. They are unofficial practice aids, not items from the live exam, which is covered by a non-disclosure agreement. For unlimited practice, use [Practice with Claude](../guide/practice.md) or the repository's built-in exam coach skill.

**1. Support resolution agent, Agentic Architecture.** Your support agent resolves most tickets but sometimes loops indefinitely, re-calling lookup_order on the same order. What is the correct structural fix?

- A. Raise max_tokens so the loop has room to finish
- C. Add explicit loop-termination conditions: cap tool iterations, detect repeated identical calls, and route to escalate_to_human when progress stalls
- B. Remove the lookup_order tool
- D. Lower the temperature

<details><summary>Answer and rationale</summary>

**C.** Agent loops need engineered termination: iteration budgets, repeated-call detection, and an escalation path when the agent cannot progress. Token budget (A) delays the symptom, removing a needed tool (B) breaks resolution, and temperature (D) does not bound iteration.

</details>

**2. Support resolution agent, Tool Design.** process_refund currently accepts any amount. Support policy caps agent-initiated refunds at $200; larger refunds need a human. Where does that rule belong?

- A. In the system prompt, phrased firmly
- D. Enforced in the tool layer: the tool rejects amounts over the cap with a structured error, and a hook or the tool itself routes larger cases to escalation
- B. In the model's reasoning, since it reads the policy
- C. In quarterly staff training

<details><summary>Answer and rationale</summary>

**D.** Hard policy limits are enforced deterministically at the tool boundary, not requested of the model. Prompt phrasing (A) and model reasoning (B) are probabilistic where the requirement is absolute, and training (C) does not constrain the agent at all.

</details>

**3. Multi-agent research, Agentic Architecture.** Your coordinator delegates to search, analysis, and report subagents. Final reports cite sources that do not support their claims, though each subagent behaves sensibly alone. What is the most likely architectural cause?

- B. The report subagent's model is too small
- A. Provenance is lost at handoffs: findings and their sources are not passed together in a structured form, so the report writer pairs claims with citations by guesswork
- C. The web is unreliable
- D. Too many subagents are running in parallel

<details><summary>Answer and rationale</summary>

**A.** In multi-agent pipelines, provenance survives only if the handoff format carries claim and source together. That failure mode produces exactly this symptom while every stage looks locally fine. Model size (B), source quality (C), and parallelism (D) do not explain correct facts paired with wrong citations.

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
- C. The commit rule in the project-level CLAUDE.md; the per-area conventions in path-scoped rules under .claude/rules/ that load only when matching files are touched
- B. Each engineer's personal user-level CLAUDE.md
- D. A wiki page linked from the README

<details><summary>Answer and rationale</summary>

**C.** The hierarchy exists for exactly this: shared rules at project scope, conditional conventions path-scoped so context is spent only where relevant. One root file (A) loads everything everywhere, personal files (B) diverge per engineer, and a wiki (D) never reaches the model.

</details>

**6. Claude Code in CI, Workflows.** Your CI job runs Claude Code to review pull requests, and the pipeline must parse the results mechanically. Which invocation is correct?

- A. Interactive mode with a human copying the output into CI
- D. Non-interactive mode with -p, with --output-format json and a schema so the review arrives as machine-readable, validated output
- B. Plan mode, which is safer for automation
- C. A shell script that greps the human-readable transcript

<details><summary>Answer and rationale</summary>

**D.** Headless CI use is what -p with JSON output and a schema is for: deterministic invocation, parseable results. A human in the loop (A) is not CI, plan mode (B) is a review gate for interactive work rather than an output format, and grepping prose (C) breaks on the first wording change.

</details>

**7. Claude Code in CI, Prompt Engineering.** The automated reviewer flags dozens of trivial style nits per pull request, and engineers have started ignoring it. Which change addresses the false-positive problem the way the blueprint suggests?

- B. Run the review twice and post only findings that appear both times
- A. Define explicit review criteria in the prompt: what to flag, what to ignore, and a severity bar, with a few worked examples of in-scope and out-of-scope findings
- C. Cap the reviewer at three findings per pull request
- D. Route all findings to a channel nobody reads

<details><summary>Answer and rationale</summary>

**A.** Precision comes from explicit criteria and few-shot examples that draw the boundary between signal and noise. Double-running (B) filters randomness but not systematic nit-picking, an arbitrary cap (C) drops real findings on bad days, and (D) is surrender.

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
- C. Validation-clean documents are a biased sample: the honest measure comes from a labeled sample drawn across all documents, including ones that failed or barely passed validation
- B. 98% is below industry standard
- D. Field accuracy is not a real metric

<details><summary>Answer and rationale</summary>

**C.** Measuring only where the system already succeeded inflates the estimate; calibration requires a labeled sample representative of the full input stream. Hardest-only (A) biases in the opposite direction, the standard claim (B) is invented, and (D) is false.

</details>

**10. Developer productivity agent, Tool Design.** Your codebase-exploration agent has get_file_contents, read_source, and fetch_file tools that all read files, and it frequently picks poorly among them. What is the correct fix?

- A. Add a fourth, better file-reading tool
- D. Consolidate to one file-reading tool, or give the survivors sharply differentiated descriptions that state exactly when each applies
- B. Fine-tune the model on the tool list
- C. Randomize which tool the harness dispatches

<details><summary>Answer and rationale</summary>

**D.** Tool selection runs on descriptions; overlapping tools with vague descriptions produce dithering. Consolidation or sharp differentiation is the documented cure. Adding overlap (A) worsens it, fine-tuning (B) is disproportionate, and randomization (C) institutionalizes the confusion.

</details>

**11. Agentic Architecture.** A support workflow resolves tickets by looking up an account, checking entitlement, and drafting a reply, always in that order. Which architecture is correct?

- B. A single agent that decides each step at runtime
- A. A deterministic pipeline that calls the model at each defined step
- C. Three agents that negotiate the order between them
- D. One prompt containing all three steps

<details><summary>Answer and rationale</summary>

**A.** A known, fixed sequence should be encoded rather than rediscovered on every run, which makes it cheaper, faster, and testable step by step. Runtime decisions (B, C) add nondeterminism for no gain, and one prompt (D) removes the checkpoints between steps.

</details>

**12. Agentic Architecture.** What is the strongest justification for splitting work across subagents?

- A. The task has many steps
- B. Separate lines of work each need their own context, and mixing them degrades both
- C. Subagents are faster than a single agent
- D. The output must be assembled from several sections

<details><summary>Answer and rationale</summary>

**B.** Subagents exist to isolate context, so the case for them is contamination between concerns rather than volume. Step count (A) and sectioned output (D) suit a workflow, and delegation usually adds latency rather than removing it (C).

</details>

**13. Agentic Architecture.** An agent loops between two tools without converging. What is the most appropriate first control?

- A. Increase the context window so it can see more history
- C. Impose a step ceiling and define the terminating condition explicitly
- B. Switch to a larger model
- D. Remove one of the two tools

<details><summary>Answer and rationale</summary>

**C.** Non-termination is bounded by an explicit stop condition and a hard ceiling, which contains cost and makes the failure visible. More context (A) and a larger model (B) do not guarantee convergence, and removing a tool (D) may break the task.

</details>

**14. Agentic Architecture.** Which property most increases the operational risk of an agentic design?

- A. It calls more than one model
- D. It takes irreversible actions without a checkpoint
- B. It produces structured output
- C. It runs longer than a minute

<details><summary>Answer and rationale</summary>

**D.** Reversibility governs the cost of being wrong, which is the dominant risk in autonomous execution. Multiple models (A), structure (B), and duration (C) affect cost and complexity rather than blast radius.

</details>

**15. Agentic Architecture.** How should an agentic system handle a step whose result it cannot verify?

- B. Proceed, since the model is usually right
- A. Surface the unverifiable step for human confirmation before acting on it
- C. Retry the step until two runs agree
- D. Log the step and continue

<details><summary>Answer and rationale</summary>

**A.** An unverifiable result is exactly where human judgment belongs, before it is acted upon. Assuming correctness (B) and logging without stopping (D) both act on unchecked output, and agreement across runs (C) establishes consistency rather than truth.

</details>

**16. Agentic Architecture.** A team proposes an agent for a task where every input is well formed and every rule is known. What should the architect recommend?

- A. An agent, for future flexibility
- B. A deterministic implementation, reserving model calls for the genuinely ambiguous parts
- C. An agent with a low step limit
- D. A multi-agent design for separation of concerns

<details><summary>Answer and rationale</summary>

**B.** Known rules over well-formed input are code, and using a model there buys nondeterminism at a price. Speculative flexibility (A), a constrained agent (C), and multiple agents (D) all keep the cost without the need.

</details>

**17. Agentic Architecture.** What most improves the debuggability of an agentic system in production?

- A. Reducing the number of tools
- C. Recording the inputs, tool calls, and outputs of each step as a trace
- B. Using a single model for every step
- D. Increasing the step limit

<details><summary>Answer and rationale</summary>

**C.** A per-step trace is what makes a nondeterministic run reconstructable after the fact. Fewer tools (A) and one model (B) simplify without explaining, and a higher ceiling (D) makes failures longer rather than clearer.

</details>

**18. Claude Code Configuration & Workflows.** Where should conventions that apply to everyone working in a repository be recorded?

- A. In each developer's personal settings
- D. In a CLAUDE.md committed to the repository
- B. In the pull request template
- C. In a pinned chat message

<details><summary>Answer and rationale</summary>

**D.** Committed project memory is versioned, reviewable, and shared, which is what a team convention requires. Personal settings (A) do not propagate, and templates (B) and messages (C) are not read as working context.

</details>

**19. Claude Code Configuration & Workflows.** What distinguishes work suited to headless mode?

- B. It is complex and needs close supervision
- A. It is well defined and repeatable, so it can run unattended in automation
- C. It requires many tools
- D. It produces a long output

<details><summary>Answer and rationale</summary>

**A.** Headless execution suits bounded, repeatable work where no one is watching. Supervision (B) argues for interactive use, and tool count (C) and output length (D) do not determine suitability.

</details>

**20. Claude Code Configuration & Workflows.** A skill and a subagent could both address a need. What decides between them?

- A. Skills are always preferable
- B. Whether the need is reusable know-how or an isolated line of work with its own context
- C. Whether the task is long
- D. Whether the repository already has a CLAUDE.md

<details><summary>Answer and rationale</summary>

**B.** The two solve different problems: a skill packages reusable procedure, a subagent isolates context. A blanket preference (A), duration (C), and existing files (D) do not address that distinction.

</details>

**21. Claude Code Configuration & Workflows.** What is the correct use of a hook in a Claude Code workflow?

- A. To hold instructions the model should follow
- C. To enforce a deterministic action at a defined point, independently of the model
- B. To store project context
- D. To define which model is used

<details><summary>Answer and rationale</summary>

**C.** Hooks run as code at fixed points, so they enforce rather than request. Instructions (A) and context (B) belong in project memory, and model choice (D) is configuration.

</details>

**22. Claude Code Configuration & Workflows.** Claude Code performs well for one engineer and inconsistently across the team. What is the most likely cause?

- A. The others need more capable machines
- D. The working conventions live in one person's local setup rather than in the repository
- B. The repository is too large
- C. The others are using different terminals

<details><summary>Answer and rationale</summary>

**D.** Context that is not committed does not travel, which produces exactly this asymmetry. Hardware (A), repository size (B), and terminal choice (C) do not explain a difference in output quality.

</details>

**23. Prompt Engineering & Structured Output.** A pipeline requires output that always validates against a schema. What is the correct approach?

- B. Ask for the schema in the prompt and validate afterwards
- A. Declare the schema as a tool the model must call, and validate on receipt
- C. Ask for JSON and repair malformed output in code
- D. Use a lower temperature

<details><summary>Answer and rationale</summary>

**A.** A declared schema makes the structure part of the contract rather than a request, and validation on receipt closes the loop. Prompt requests (B), downstream repair (C), and temperature (D) all leave the shape to chance.

</details>

**24. Prompt Engineering & Structured Output.** Extraction is accurate for common cases and fails on rare formats. What is the most effective response?

- A. Raise the temperature to encourage flexibility
- B. Add examples covering the rare formats and define what to return when a field is absent
- C. Switch to a larger model
- D. Ask the model to try harder on unusual inputs

<details><summary>Answer and rationale</summary>

**B.** Rare cases fail because they are unspecified, and examples plus an explicit absent-field rule specify them. Temperature (A) adds variance, a larger model (C) is not aimed at the gap, and exhortation (D) is not a specification.

</details>

**25. Prompt Engineering & Structured Output.** What should a schema define for a field the source document may not contain?

- A. Nothing, since the model will omit it
- C. An explicit representation for absence, so a missing value is distinguishable from an unfilled one
- B. A default value that looks plausible
- D. A free-text field for notes

<details><summary>Answer and rationale</summary>

**C.** Absence must be representable, or downstream code cannot tell a genuine gap from a failure. Silent omission (A) is ambiguous, plausible defaults (B) fabricate data, and a notes field (D) does not make the state machine-readable.

</details>

**26. Prompt Engineering & Structured Output.** Which practice most improves consistency across a long-running structured extraction job?

- A. Randomising the order of documents
- D. Fixing the prompt, the schema, and the model version, and recording them with the output
- B. Increasing the output token limit
- C. Running each document twice

<details><summary>Answer and rationale</summary>

**D.** Consistency requires that the things that shape output are pinned and recorded, so results remain comparable and reproducible. Ordering (A) is irrelevant, the token cap (B) affects length, and duplicate runs (C) measure variance without removing it.

</details>

**27. Prompt Engineering & Structured Output.** A prompt mixes the instruction, the data, and the output format in continuous prose. What is the first improvement?

- B. Shorten it
- A. Separate the sections so the instruction, the input, and the required format are distinguishable
- C. Move it into the system prompt
- D. Add emphasis to the format requirement

<details><summary>Answer and rationale</summary>

**A.** Structure lets the model tell instruction from data, which is the most common source of confusion in long prompts. Shortening (B) may remove needed detail, relocation (C) does not clarify, and emphasis (D) does not separate.

</details>

**28. Tool Design & MCP Integration.** What is the strongest indicator that a tool surface needs redesign?

- A. It contains more than ten tools
- B. The model regularly selects a tool that cannot accomplish the request
- C. The tools return JSON
- D. The tools are implemented across several services

<details><summary>Answer and rationale</summary>

**B.** Repeated wrong selection is evidence that the tools are not distinguishable from their descriptions, which is a design fault. Tool count (A), return format (C), and implementation topology (D) are not themselves problems.

</details>

**29. Tool Design & MCP Integration.** How should a tool that performs an irreversible action be designed?

- A. With a description warning the model to be careful
- C. So that authorisation and confirmation are enforced outside the model
- B. So that it requires more parameters
- D. So that it is declared last

<details><summary>Answer and rationale</summary>

**C.** Irreversibility is controlled by the surrounding system, because a prompt-level warning is a request rather than a guarantee. Extra parameters (B) and ordering (D) do not constrain authority.

</details>

**30. Tool Design & MCP Integration.** A tool returns a large payload that consumes most of the context window. What is the right change?

- A. Increase the context window
- D. Return only what the task needs, with a way to request more detail
- B. Summarise the payload with a second model call
- C. Call the tool less often

<details><summary>Answer and rationale</summary>

**D.** Tools should return task-relevant results rather than everything available, which keeps context for reasoning. A larger window (A) postpones the problem, a second call (B) adds cost and a failure point, and calling less often (C) does not change the payload.

</details>

**31. Tool Design & MCP Integration.** What belongs in a tool's description?

- B. The implementation language and framework
- A. What the tool does, when to use it, and what its parameters mean
- C. The service level agreement
- D. The name of the team that owns it

<details><summary>Answer and rationale</summary>

**A.** The description is the model's selection guide, so it must answer purpose, applicability, and parameters. Implementation detail (B), service levels (C), and ownership (D) are irrelevant to the choice.

</details>

**32. Context Management & Reliability.** A long agentic run degrades in quality as it proceeds. What is the most likely cause?

- A. The model version changed mid-run
- B. Context has accumulated until relevant material competes with stale material
- C. The temperature was set too low
- D. The tools became slower

<details><summary>Answer and rationale</summary>

**B.** Progressive degradation over a long run is the signature of context accumulation and drift. Versions do not change mid-run (A), low temperature (C) reduces variety rather than quality, and tool latency (D) does not affect correctness.

</details>

**33. Context Management & Reliability.** What is the right way to carry state across a compaction boundary?

- A. Rely on the model to remember what mattered
- C. Write the decisions and constraints that must persist into an explicit summary that is carried forward
- B. Increase the context window so compaction is never needed
- D. Restart the task after compaction

<details><summary>Answer and rationale</summary>

**C.** Persistence must be deliberate, because compaction is lossy by design. Relying on recall (A) is unreliable, a larger window (B) only delays the boundary, and restarting (D) discards the work.

</details>

**34. Context Management & Reliability.** Which measure most improves reliability for a workflow that must not silently produce wrong output?

- A. A larger model
- D. A validation step that can reject output and trigger a defined fallback
- B. A longer prompt
- C. More examples in the prompt

<details><summary>Answer and rationale</summary>

**D.** Reliability against silent failure requires detection and a defined response, which is what validation with a fallback provides. Model size (A), prompt length (B), and examples (C) improve the average case without catching the bad one.

</details>

**35. Context Management & Reliability.** What should be measured to know whether a production agentic system is healthy?

- B. Total tokens consumed
- A. Task success against a defined criterion, plus the rate and shape of failures
- C. Average response time
- D. The number of tool calls per run

<details><summary>Answer and rationale</summary>

**A.** Health is defined by whether the system accomplishes the task and how it fails when it does not. Tokens (B), latency (C), and call counts (D) are cost and behaviour signals that say nothing about correctness.

</details>

---

These questions are the maintainer's original work for self-assessment. [Study guide](README.md) · [Study notes](notes.md) · [Mock exam](mock-exam-1.md) · [Repository index](../README.md)
