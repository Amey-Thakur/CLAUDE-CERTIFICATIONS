# Mock exam 3: Developer – Foundations

The third and final timed practice exam, with fifteen more questions that appear nowhere else in this repository. Save it for the week you intend to book: taken cold, after the [first](mock-exam-1.md) and [second](mock-exam-2.md) mocks, it is the closest thing here to a readiness check. Original questions written against the public [blueprint](README.md#skills-measured); not items from the live exam, which is covered by a non-disclosure agreement.

**How to take it.** 15 questions, 30 minutes, closed book: no notes, no documentation, no Claude. Several questions turn on cost and latency trade-offs, which carry real weight on this paper. Score yourself with the [key](#answer-key) and the [readiness table](#interpreting-your-score) afterwards.

> [!TIP]
> Stuck on a question afterwards? The [prompts for studying with Claude](../guide/prompts.md) include one for working through a question you got wrong, and one for drilling a whole domain.

---

## Questions

**1.** A request fails with an authentication error after working for months. What is the most likely cause?

- A. A transient service fault
- B. The prompt became too long
- C. A credential that expired, was rotated, or lost its permissions
- D. The model was deprecated

**2.** What is the purpose of correlating a request identifier through an integration?

- A. It lets a specific response be traced back to the request that produced it
- B. It reduces token cost
- C. It improves model accuracy
- D. It is required by the API

**3.** An integration must handle a response that stops early because the model called a tool. What does the application do next?

- A. Treat it as an error and retry
- B. Return the partial text to the user
- C. Increase the output token limit
- D. Execute the tool and return its result so the model can continue

**4.** Which is the strongest reason to put a queue between an application and the model?

- A. It makes responses more accurate
- B. It absorbs bursts so load stays within rate limits without dropping work
- C. It reduces the token count
- D. It removes the need for retries

**5.** A response arrives well-formed but semantically wrong for the input. Where should investigation start?

- A. The transport layer
- B. The prompt and the exact context supplied for that input
- C. The rate limit configuration
- D. The output token limit

**6.** What is the practical consequence of choosing a model with a much larger context window than the task needs?

- A. Better accuracy on every task
- B. Fewer rate limit errors
- C. More reliable structured output
- D. Cost and latency that the task does not require

**7.** How should a team decide when to move a task to a smaller model?

- A. When measurement shows the smaller model meets the task's stated quality bar
- B. When the budget is exceeded
- C. When the task becomes high volume
- D. When latency becomes a complaint

**8.** A long-running agent needs to keep a decision it made twenty steps ago. What is the correct mechanism?

- A. Rely on the context window retaining it
- B. Increase the temperature
- C. Write it into an explicit state that is carried forward regardless of compaction
- D. Restart the agent periodically

**9.** What distinguishes a workflow from an agent in practice?

- A. Workflows are shorter
- B. Agents cannot use tools
- C. Workflows cannot call the model
- D. In a workflow the control flow is fixed in advance; in an agent the model chooses the next step

**10.** A prompt contains an instruction that contradicts an example in the same prompt. What is the likely outcome?

- A. The instruction always wins
- B. The example always wins
- C. Behavior becomes unpredictable between the two
- D. The request is rejected

**11.** What is the effect of placing the most important instruction in the middle of a very long prompt?

- A. None, position is irrelevant
- B. It is more likely to be overlooked than if it were at a boundary
- C. It is followed more closely
- D. It causes an error

**12.** When should a tool return an identifier rather than the full object?

- A. When the object is large and the model only needs it to make a subsequent call
- B. Never, the model needs the full object
- C. Always, to reduce cost
- D. Only for write operations

**13.** An MCP server is added and the agent's success rate falls. What should be checked first?

- A. Whether the new tools overlap with existing ones and have distinguishable descriptions
- B. The server's uptime
- C. The model version
- D. The network latency

**14.** A model output will be rendered directly into a web page. What must the application do?

- A. Nothing, model output is safe
- B. Treat the output as untrusted and escape or sanitise it before rendering
- C. Ask the model not to produce markup
- D. Use a larger model

**15.** What does a regression suite protect against that a one-off evaluation does not?

- A. Slow responses
- B. Rate limits
- C. A change that improves the target behavior while quietly breaking another
- D. Cost increases

---

## Answer key

| # | Answer | Domain | Why |
| --- | --- | --- | --- |
| 1 | C | Applications and Integration | Authentication failures point at the credential rather than the payload. A transient fault (A) presents differently, and neither prompt length (B) nor deprecation (D) produces an auth error |
| 2 | A | Applications and Integration | Correlation exists for traceability, which is what debugging asynchronous or batched work depends on. It does not affect cost (B) or accuracy (C), and it is a design practice rather than a requirement (D) |
| 3 | D | Applications and Integration | A tool-use stop is a handoff, and the loop continues once the result is returned. Retrying (A) repeats the request, returning partial text (B) discards the work, and the token limit (C) is unrelated |
| 4 | B | Applications and Integration | A queue smooths demand against a rate-limited dependency. It does not change accuracy (A) or token counts (C), and retries remain necessary (D) |
| 5 | B | Applications and Integration | A well-formed but wrong answer points at what the model was told, not how it was delivered. Transport (A), limits (C), and output caps (D) produce failures of delivery rather than of meaning |
| 6 | D | Model Selection and Optimization | Unused capacity is paid for in cost and time. A larger window does not itself improve accuracy (A), reduce rate limiting (B), or make structure more reliable (C) |
| 7 | A | Model Selection and Optimization | The decision is evidence-led against a defined bar. Budget (B), volume (C), and latency (D) create pressure to look, but they do not establish that quality holds |
| 8 | C | Agents and Workflows | Durable state must be explicit, because context is finite and compaction is lossy. Relying on the window (A) fails at length, temperature (B) is unrelated, and restarting (D) loses the decision |
| 9 | D | Agents and Workflows | Who decides the next step is the distinction that matters. Length (A) is incidental, agents do use tools (B), and workflows do call the model (C) |
| 10 | C | Prompt and Context Engineering | Contradictory signals produce inconsistent behavior rather than a defined precedence. Neither the instruction (A) nor the example (B) reliably wins, and the request is not rejected (D) |
| 11 | B | Prompt and Context Engineering | Material at the edges of a long input is attended to more reliably than material buried in the middle. Position is not neutral (A) or advantageous here (C), and it does not error (D) |
| 12 | A | Tools and MCPs | Returning a handle keeps context free when the payload is only needed for a later call. Always returning everything (B) or nothing (C) ignores the task, and the rule is not about writes (D) |
| 13 | A | Tools and MCPs | A new tool surface most often degrades selection through overlap and unclear descriptions. Uptime (B) and latency (D) present as errors or slowness, and the model did not change (C) |
| 14 | B | Security and Safety | Anything rendered into a page is escaped regardless of source, since output can be influenced by input. Assuming safety (A) and instructing the model (C) are not controls, and model size (D) is irrelevant |
| 15 | C | Eval, Testing, and Debugging | Regressions are silent by definition and are caught by continuously testing what must not break. Latency (A), limits (B), and cost (D) are operational signals rather than correctness |

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

Written by the maintainer for self-assessment. [Study guide](README.md) · [Study notes](notes.md) · [Mock 1](mock-exam-1.md) · [Mock 2](mock-exam-2.md) · [Practice questions](practice-questions.md) · [Repository index](../README.md)
