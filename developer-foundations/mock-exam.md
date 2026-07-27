# Mock exam: Developer – Foundations

A timed practice exam in the official style. Unlike the [practice questions](practice-questions.md), the domains are hidden and the answers sit at the end, so this measures readiness rather than teaching. Original questions written against the public [blueprint](README.md#skills-measured); not items from the live exam, which is covered by a non-disclosure agreement.

**How to take it.** 15 questions, 30 minutes, closed book: no notes, no documentation, no Claude. Answer every question, since unanswered items score zero. Question weighting follows the blueprint, so Applications and Integration dominates. Score yourself with the [key](#answer-key) and the [readiness table](#interpreting-your-score) afterwards.

---

## Questions

**1.** Your service makes a Messages API call and the response carries stop_reason "end_turn" with a tool_use block absent. What does your loop do?

- A. Execute the last requested tool again
- B. Treat the turn as complete and return the content to the caller
- C. Re-send the request with higher max_tokens
- D. Append an empty tool result and continue the loop

**2.** A nightly job enriches 200,000 product descriptions. Results are consumed the next morning. Which design minimizes cost?

- A. Synchronous calls fanned out across many workers
- B. The Message Batches API with results collected within its processing window
- C. Synchronous calls with a smaller model and reduced max_tokens
- D. One request containing all descriptions

**3.** Which change makes a repeated 10,000-token system prompt cheaper and faster without losing content?

- A. Moving the prompt to the end of the request
- B. Placing the stable prompt first and enabling prompt caching so the prefix is reused
- C. Compressing the prompt text with abbreviations
- D. Sending the prompt only on the first request of a session

**4.** Your extraction endpoint occasionally receives JSON with a missing required field, and downstream code throws. What is the sturdiest production pattern?

- A. Wrap the parse in a try block and return an empty object on failure
- B. Enforce a schema through tool use, validate the parsed result, and retry once with the validation error appended
- C. Instruct the model more firmly in the system prompt
- D. Post-process with a regular expression that inserts missing fields

**5.** A teammate proposes an autonomous agent for a pipeline whose five steps are identical for every input. What is the strongest technical objection?

- A. Agents are unsupported in production
- B. A known, fixed path does not need model-chosen control flow; deterministic orchestration is cheaper, testable, and auditable
- C. Agents cannot call tools reliably
- D. The pipeline would need a larger context window

**6.** Which is the correct use of a subagent in an agent system?

- A. To run the same prompt twice for consensus
- B. To isolate a self-contained subtask so its verbose intermediate context does not fill the parent's window
- C. To bypass rate limits
- D. To provide a fallback if the main model is unavailable

**7.** An agent that summarizes user-submitted URLs must never be able to trigger a refund. Where is that guaranteed?

- A. In the system prompt, stated clearly
- B. By not granting the agent the refund tool, and enforcing that with tool configuration or hooks
- C. By instructing the model to confirm before refunds
- D. By using a model known for instruction following

**8.** Your team pins model versions in production. What is the primary reason?

- A. Pinned models are cheaper
- B. Model updates can change behavior, so upgrades become deliberate, evaluated changes rather than surprises
- C. Pinning increases the context window
- D. Pinning is required by the API

**9.** Which describes the correct relationship between an MCP server and the applications that use it?

- A. Each application embeds its own copy of the server code
- B. The server exposes tools and resources that multiple clients connect to, maintained independently of any one application
- C. The server replaces the Messages API
- D. The server must run in the same process as the model

**10.** A long-running assistant begins contradicting itself and forgetting recent constraints. Inspection shows the context is nearly full of verbose tool outputs. What is the correct remedy?

- A. Increase temperature to encourage variety
- B. Prune and summarize tool outputs, compact history, and isolate subtasks so the working context stays lean
- C. Repeat the system prompt after every turn
- D. Reduce max_tokens on each response

**11.** When is few-shot prompting the right tool?

- A. When the model needs more factual knowledge
- B. When output format or edge-case handling is inconsistent and examples can demonstrate the target behavior
- C. When latency must be reduced
- D. When the context window is too small

**12.** A page retrieved by your agent contains hidden text instructing it to reveal its system prompt. Which mitigation actually works?

- A. Asking the model in the system prompt to ignore such instructions
- B. Treating retrieved content as untrusted data, separating it from instructions, and gating sensitive capabilities behind guardrails
- C. Raising temperature so behavior is less predictable
- D. Filtering pages that contain the word "ignore"

**13.** Which statement about the Message Batches API is correct?

- A. It supports multi-turn tool calling within a batch
- B. It processes large asynchronous workloads at reduced cost within a processing window, correlating requests by custom_id
- C. It guarantees sub-second latency
- D. It requires a dedicated endpoint per request

**14.** Your CI pipeline runs Claude Code non-interactively and must parse its output. Which invocation fits?

- A. Interactive mode with output piped to a file
- B. The print flag with a JSON output format and a schema, so results are machine-readable and validated
- C. Plan mode with a human approver
- D. A wrapper that screen-scrapes the terminal

**15.** Traces show your assistant reasons correctly over the documents it receives, but frequently receives documents unrelated to the question. Where is the defect?

- A. The model, which should be upgraded
- B. The retrieval layer that selects the documents
- C. The system prompt, which needs stronger accuracy language
- D. The output parser

---

## Answer key

| # | Answer | Domain | Why |
| --- | --- | --- | --- |
| 1 | B | Agents and Workflows | "end_turn" means the model has finished; "tool_use" is the signal to execute a tool and continue the loop |
| 2 | B | Applications and Integration | Latency-tolerant bulk work is the Batches API's purpose: roughly half the cost within a 24-hour window |
| 3 | B | Applications and Integration | Caching reuses a stable prefix, cutting time-to-first-token and per-request cost. Position matters: stable content first |
| 4 | B | Prompt and Context Engineering | Schema enforcement plus a validation-retry loop treats model output as untrusted input and lets the model self-correct |
| 5 | B | Agents and Workflows | Autonomy is justified when the path is unknown. A fixed path belongs in deterministic code that can be tested |
| 6 | B | Agents and Workflows | Subagents delegate and isolate context; that isolation is their main architectural value |
| 7 | B | Security and Safety | Capability the agent does not hold cannot be misused. Prompts and confirmations are not enforcement |
| 8 | B | Model Selection and Optimization | Pinning makes model behavior a controlled dependency so upgrades pass through evaluation |
| 9 | B | Tools and MCPs | An MCP server is a reusable, independently maintained capability that multiple clients share |
| 10 | B | Prompt and Context Engineering | Context drift and bloat are managed by pruning, compaction, and isolation |
| 11 | B | Prompt and Context Engineering | Few-shot examples fix format and edge-case behavior far better than more instructions |
| 12 | B | Security and Safety | Injection defense is structural: separate untrusted content and apply least privilege to consequential tools |
| 13 | B | Applications and Integration | Reduced cost, asynchronous window, custom_id correlation, and no multi-turn tool calling inside a batch |
| 14 | B | Claude Code | Headless CI use means non-interactive invocation with structured, schema-validated output |
| 15 | B | Eval, Testing, and Debugging | Traces localize the fault to the integration layer: correct reasoning over wrong inputs is a retrieval defect |

## Interpreting your score

| Raw score | Reading |
| --- | --- |
| 13 to 15 | Comfortable. Review misses and book the exam |
| 10 to 12 | Close. Target the domains where you lost points, especially anything in Applications and Integration, which is a third of the real exam |
| 7 to 9 | More study needed. Build something that exercises the API, a tool, and structured output, then return |
| 6 or fewer | Start from the blueprint and the official exam guide, then the prep path |

This scale is a study aid, not a predictor. The real exam reports a scaled score from 100 to 1,000 with 720 to pass.

Tally misses by domain; two or more in one domain marks your next study target, as the real score report's percent-correct breakdown would.

---

Written by the maintainer for self-assessment. [Study guide](README.md) · [Study notes](notes.md) · [Practice questions](practice-questions.md) · [Repository index](../README.md)
