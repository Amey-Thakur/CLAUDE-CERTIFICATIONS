# Mock exam 2: Architect – Foundations

A second timed practice exam in the official style, with fifteen questions that appear nowhere else in this repository. Take it after [mock exam 1](mock-exam-1.md) and the [practice questions](practice-questions.md), when you want a fresh measure rather than a review. Original questions written against the public [blueprint](README.md#skills-measured); not items from the live exam, which is covered by a non-disclosure agreement.

**How to take it.** 15 questions, 30 minutes, closed book: no notes, no documentation, no Claude. The real exam frames its items inside published scenarios; this mock samples the same judgment across all of them. Score yourself with the [key](#answer-key) and the [readiness table](#interpreting-your-score) afterwards.

> [!TIP]
> Stuck on a question afterwards? The [prompts for studying with Claude](../guide/prompts.md) include one for working through a question you got wrong, and one for drilling a whole domain.

---

## Questions

**1.** A pipeline has four steps whose order never varies and whose outputs are each checkable. What should it be?

- A. An agent that plans each run
- B. Four agents, one per step
- C. A deterministic workflow with model calls at defined points
- D. A single prompt covering all four steps

**2.** What is the principal cost of introducing a subagent?

- A. It loses the context the parent held unless the handoff carries it explicitly
- B. It requires a larger model
- C. It cannot use tools
- D. It doubles token cost in every case

**3.** An autonomous step would modify production data. What does the architecture require?

- A. A more capable model
- B. A longer system prompt describing caution
- C. A retry policy
- D. A checkpoint where a person authorises the action, or a reversible mechanism

**4.** What most helps diagnose an agentic failure after the fact?

- A. The final output alone
- B. A trace of each step's inputs, tool calls, and outputs
- C. The total token count
- D. The model version

**5.** Where should repository-wide conventions for Claude Code live?

- A. In each developer's local configuration
- B. In a CLAUDE.md committed to the repository
- C. In the team's chat channel
- D. In the CI configuration only

**6.** Which task is best suited to headless Claude Code in CI?

- A. Exploratory debugging of an unfamiliar failure
- B. Designing a new module's architecture
- C. Pair programming with a developer
- D. A repeatable, well-specified check that runs on every pull request

**7.** What is a hook for?

- A. Running a deterministic action at a defined point, independently of the model
- B. Storing reusable instructions
- C. Holding project context
- D. Selecting the model

**8.** A pipeline needs output that always conforms to a fixed shape. What is the correct mechanism?

- A. Requesting the shape in the prompt and parsing the result
- B. Post-processing prose with regular expressions
- C. Declaring the shape as a schema the model must satisfy, and validating on receipt
- D. Lowering the temperature

**9.** How should a schema handle a value the source may not contain?

- A. Omit the field silently
- B. Supply a plausible default
- C. Return an empty string in all cases
- D. Define an explicit representation for absence

**10.** Extraction succeeds on typical inputs and fails on unusual ones. What is the most effective response?

- A. Raise the temperature
- B. Use a larger model
- C. Add examples covering the unusual formats and state what to return when a field is missing
- D. Ask the model to be careful with unusual inputs

**11.** What is the clearest sign that a tool surface needs redesign rather than better prompting?

- A. It exposes more than five tools
- B. The model repeatedly selects a tool that cannot satisfy the request
- C. The tools are implemented in different services
- D. The tools return large payloads

**12.** How should a tool that deletes records be constrained?

- A. By enforcing authorisation and scope outside the model
- B. By a description warning the model to use it carefully
- C. By requiring more parameters
- D. By declaring it last among the tools

**13.** An MCP integration exposes an entire database through one general query tool. What is the architectural concern?

- A. The model's authority is unbounded, and least privilege cannot be applied
- B. It will be slow
- C. It uses too many tokens
- D. It cannot return structured output

**14.** Quality degrades steadily through a long agentic run. What is the most likely cause?

- A. The model version changed mid-run
- B. Accumulated context has diluted the material that matters
- C. The temperature is too low
- D. The tools have become slower

**15.** What must happen for state to survive a compaction boundary?

- A. Nothing, the model retains what matters
- B. The context window must be enlarged
- C. The decisions and constraints that must persist are written into an explicit carried-forward summary
- D. The run must restart

---

## Answer key

| # | Answer | Domain | Why |
| --- | --- | --- | --- |
| 1 | C | Agentic Architecture | A known fixed order is encoded rather than rediscovered, which is cheaper and testable per step. Runtime planning (A, B) adds nondeterminism, and one prompt (D) removes the checkpoints |
| 2 | A | Agentic Architecture | Delegation buys isolation and pays in context, which is why handoffs must be explicit. A subagent does not require a larger model (B), can use tools (C), and cost varies with the work (D) |
| 3 | D | Agentic Architecture | Irreversible external effects need an authorisation boundary or reversibility, enforced outside the model. Capability (A), instruction (B), and retries (C) do not bound the consequence |
| 4 | B | Agentic Architecture | A per-step trace reconstructs a nondeterministic run, which is what diagnosis needs. The final output (A), token totals (C), and version (D) do not show where it diverged |
| 5 | B | Claude Code Configuration & Workflows | Committed project memory is shared, versioned, and reviewed with the code. Local configuration (A) does not propagate, chat (C) is not read as context, and CI (D) covers automation rather than interactive work |
| 6 | D | Claude Code Configuration & Workflows | Headless execution suits bounded, repeatable work that runs unattended. Exploration (A), design (B), and pairing (C) all depend on a person in the loop |
| 7 | A | Claude Code Configuration & Workflows | Hooks execute as code at fixed points, which is how a guarantee is enforced. Instructions (B) and context (C) belong in project memory, and model choice (D) is configuration |
| 8 | C | Prompt Engineering & Structured Output | A declared schema makes the shape a contract rather than a request, and validation closes the loop. Prompt requests (A), text parsing (B), and temperature (D) leave the shape to chance |
| 9 | D | Prompt Engineering & Structured Output | Absence must be representable so a genuine gap is distinguishable from a failure. Silent omission (A) is ambiguous, a plausible default (B) fabricates, and an empty string (C) conflates absence with an empty value |
| 10 | C | Prompt Engineering & Structured Output | The unusual cases fail because they were never specified, and examples plus a missing-value rule specify them. Temperature (A) adds variance, model size (B) is not aimed at the gap, and exhortation (D) is not specification |
| 11 | B | Tool Design & MCP Integration | Repeated wrong selection indicates the tools are not distinguishable from their descriptions, which is a design fault. Tool count (A) and implementation topology (C) are not faults, and payload size (D) is a separate problem |
| 12 | A | Tool Design & MCP Integration | Destructive capability is bounded by the surrounding system, since a description is a request rather than a control. Extra parameters (C) and ordering (D) do not limit authority |
| 13 | A | Tool Design & MCP Integration | A single unrestricted tool removes the ability to scope what the model may reach. Speed (B) and tokens (C) are secondary, and structured output (D) is achievable either way |
| 14 | B | Context Management & Reliability | Progressive degradation over a long run is the signature of context accumulation. Versions do not change mid-run (A), low temperature (C) reduces variety rather than quality, and tool latency (D) does not affect correctness |
| 15 | C | Context Management & Reliability | Compaction is lossy, so persistence must be deliberate. Relying on recall (A) is unreliable, a larger window (B) only moves the boundary, and restarting (D) discards the work |

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

Written by the maintainer for self-assessment. [Study guide](README.md) · [Study notes](notes.md) · [Mock 1](mock-exam-1.md) · [Mock 3](mock-exam-3.md) · [Practice questions](practice-questions.md) · [Repository index](../README.md)
