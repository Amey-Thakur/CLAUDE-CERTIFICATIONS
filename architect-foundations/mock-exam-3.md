# Mock exam 3: Architect – Foundations

The third and final timed practice exam, with fifteen more questions that appear nowhere else in this repository. Save it for the week you intend to book: taken cold, after the [first](mock-exam.md) and [second](mock-exam-2.md) mocks, it is the closest thing here to a readiness check. Original questions written against the public [blueprint](README.md#skills-measured); not items from the live exam, which is covered by a non-disclosure agreement.

**How to take it.** 15 questions, 30 minutes, closed book: no notes, no documentation, no Claude. The real exam frames its items inside published scenarios; this mock samples the same judgment across all of them. Score yourself with the [key](#answer-key) and the [readiness table](#interpreting-your-score) afterwards.

> [!TIP]
> Stuck on a question afterwards? The [prompts for studying with Claude](../guide/prompts.md) include one for working through a question you got wrong, and one for drilling a whole domain.

---

## Questions

**1.** An agentic design calls the same expensive tool repeatedly with identical arguments. What does this indicate?

- A. Healthy retry behaviour
- B. The tool is too fast
- C. The agent is not retaining or reusing the result, which points at the state design
- D. The model is too capable

**2.** What determines whether two lines of work belong in separate subagents?

- A. Whether each needs context the other would pollute
- B. Their combined length
- C. Whether they use different tools
- D. Whether they can run in parallel

**3.** Which design most reduces the cost of a wrong autonomous decision?

- A. A larger model
- B. A longer prompt
- C. More tools
- D. Making the action reversible, or gating it behind confirmation

**4.** A CLAUDE.md has grown to several thousand lines. What is the likely effect?

- A. Better results, because more context is available
- B. The instructions that matter compete with material that no longer applies
- C. No effect, since it is read once
- D. Faster responses

**5.** What should be true of a skill before it is committed to a shared repository?

- A. It is long enough to be useful
- B. It encodes a procedure the team genuinely repeats, and it is reviewable
- C. It is written by the most senior engineer
- D. It covers every edge case

**6.** Why is committed configuration preferable to per-developer configuration for team conventions?

- A. It is faster to load
- B. It uses less context
- C. It cannot be overridden
- D. It is versioned, reviewed, and applies to everyone including automation

**7.** A schema-validated response fails validation once in every few hundred calls. What is the correct handling?

- A. Define a fallback path: retry, then fail explicitly rather than passing invalid data on
- B. Ignore it, since the rate is low
- C. Disable validation to avoid the failures
- D. Increase the output token limit

**8.** What is the advantage of validating structured output at the boundary rather than downstream?

- A. It is cheaper
- B. It removes the need for a schema
- C. The failure is caught where it can still be retried or rejected, before it contaminates later steps
- D. It improves model accuracy

**9.** A structured extraction must record where in the source each value came from. What does this require?

- A. A larger model
- B. A longer prompt
- C. A second extraction pass
- D. The schema to include a provenance field the model must populate

**10.** Two tools do nearly the same thing with different names. What is the architectural fault?

- A. Duplication of code
- B. Higher latency
- C. The model has no reliable basis for choosing between them
- D. Increased token cost

**11.** What should a tool do when given arguments it cannot satisfy?

- A. Return the closest result it can
- B. Return a clear error stating what was wrong, so the model can correct the call
- C. Return an empty result
- D. Raise an exception that terminates the run

**12.** An MCP tool exposes a write operation that the use case never needs. What should happen?

- A. Remove it, because unused authority is unnecessary risk
- B. Leave it, since it may be useful later
- C. Document that it should not be used
- D. Rename it to discourage use

**13.** What is the earliest reliable signal that context management has failed in a long run?

- A. The agent begins repeating work or contradicting earlier decisions
- B. The run takes longer than expected
- C. Token cost rises
- D. A tool returns an error

**14.** Why is a defined success criterion necessary for a reliable agentic system?

- A. It reduces token cost
- B. Without it there is no way to tell completion from failure, so the system cannot stop correctly or be measured
- C. It makes the prompt shorter
- D. It is required by the platform

**15.** A reliability requirement says wrong output must never reach the user unnoticed. What does the design need?

- A. A more capable model
- B. More examples in the prompt
- C. A detection step with a defined action when it fires
- D. A longer context window

---

## Answer key

| # | Answer | Domain | Why |
| --- | --- | --- | --- |
| 1 | C | Agentic Architecture | Repeating an identical call means the prior result is not available to the agent, which is a state problem. It is not retry behaviour (A), and neither tool speed (B) nor capability (D) explains it |
| 2 | A | Agentic Architecture | Context isolation is the reason subagents exist. Length (B), tool difference (C), and parallelism (D) can all be handled within one context |
| 3 | D | Agentic Architecture | Reversibility and gating bound the consequence, which is what the risk is. Capability (A), prompt length (B), and tools (C) affect the chance of error rather than its cost |
| 4 | B | Claude Code Configuration & Workflows | Project memory is context and dilutes like any other. More is not automatically better (A), it is not free (C), and it does not speed anything up (D) |
| 5 | B | Claude Code Configuration & Workflows | A shared skill is justified by genuine repetition and must be reviewable like code. Length (A), authorship (C), and exhaustiveness (D) do not establish that |
| 6 | D | Claude Code Configuration & Workflows | Shared, reviewed, versioned context is what makes a convention hold across people and CI. Speed (A) and context size (B) are not the reason, and it can still be overridden locally (C) |
| 7 | A | Prompt Engineering & Structured Output | A rare failure still needs a defined path, and silently passing invalid data is the outcome to prevent. Ignoring it (B) and disabling validation (C) do exactly that, and the token limit (D) is not the cause |
| 8 | C | Prompt Engineering & Structured Output | Catching at the boundary contains the fault. It is not primarily a cost question (A), the schema is what makes it possible (B), and it does not change the model's accuracy (D) |
| 9 | D | Prompt Engineering & Structured Output | Anything the output must carry has to be part of the declared shape. Model size (A) and prompt length (B) do not create a field, and a second pass (C) is unnecessary if the schema asks for it |
| 10 | C | Tool Design & MCP Integration | Ambiguity at the point of selection is the fault, because the model chooses from descriptions. Code duplication (A), latency (B), and cost (D) are secondary consequences |
| 11 | B | Tool Design & MCP Integration | An informative error keeps the model able to adapt. A closest-guess (A) and an empty result (C) are silently wrong, and terminating (D) discards a recoverable run |
| 12 | A | Tool Design & MCP Integration | Authority that is not needed should not be granted. Retaining it for possible future use (B), documenting (C), or renaming (D) all leave the capability reachable |
| 13 | A | Context Management & Reliability | Repetition and self-contradiction are the behavioural signature of lost state. Duration (B) and cost (C) rise for many reasons, and a tool error (D) is unrelated |
| 14 | B | Context Management & Reliability | Termination and measurement both depend on a definition of done. Cost (A), prompt length (C), and platform requirements (D) are not the reason |
| 15 | C | Context Management & Reliability | Preventing silent error requires detection plus a response. Capability (A), examples (B), and context (D) improve the average case without catching the bad one |

## Interpreting your score

| Score | Reading |
| --- | --- |
| 13 to 15 | Comfortable. Review anything you missed and book the exam |
| 10 to 12 | Close. Work the domains where you lost points, then revisit the [study notes](notes.md) |
| 7 to 9 | More study needed. Return to the [study guide](README.md) and the prep courses before testing |
| 6 or fewer | Start from the blueprint and the official exam guide; you are not yet reading questions the way the exam intends |

This scale is a study aid, not a predictor. The real exam reports a scaled score from 100 to 1,000 with 720 to pass, and it draws from a much larger item pool.

Tally your misses by domain using the key above; two or more misses in one domain marks it as your next study target, exactly as the real score report's percent-correct breakdown would.

---

Written by the maintainer for self-assessment. [Study guide](README.md) · [Study notes](notes.md) · [Mock 1](mock-exam.md) · [Mock 2](mock-exam-2.md) · [Practice questions](practice-questions.md) · [Repository index](../README.md)
