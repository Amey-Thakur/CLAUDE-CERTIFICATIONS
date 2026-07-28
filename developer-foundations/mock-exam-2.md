# Mock exam 2: Developer – Foundations

A second timed practice exam in the official style, with fifteen questions that appear nowhere else in this repository. Take it after [mock exam 1](mock-exam.md) and the [practice questions](practice-questions.md), when you want a fresh measure rather than a review. Original questions written against the public [blueprint](README.md#skills-measured); not items from the live exam, which is covered by a non-disclosure agreement.

**How to take it.** 15 questions, 30 minutes, closed book: no notes, no documentation, no Claude. Several questions turn on cost and latency trade-offs, which carry real weight on this paper. Score yourself with the [key](#answer-key) and the [readiness table](#interpreting-your-score) afterwards.

> [!TIP]
> Stuck on a question afterwards? The [prompts for studying with Claude](../guide/prompts.md) include one for working through a question you got wrong, and one for drilling a whole domain.

---

## Questions

**1.** A service sends the same 8,000-token system prompt on every request and cost is dominated by input tokens. What is the first change to evaluate?

- A. Rewriting the system prompt to be shorter
- B. Switching to a cheaper model
- C. Caching the stable prefix so it is not reprocessed on every call
- D. Reducing the number of requests

**2.** An endpoint must return within 500 ms but the model needs longer for a good answer. What is the appropriate pattern?

- A. Return an acknowledgement immediately and deliver the result through a callback or poll
- B. Truncate the model's output
- C. Use the smallest model regardless of quality
- D. Increase the timeout on the client

**3.** What does a stop reason indicating the maximum token limit tell you?

- A. The input was too long
- B. The request was malformed
- C. The model refused the request
- D. The output was cut off before the model finished

**4.** A tool result returns 50,000 tokens of JSON, most of it unused. What is the right fix?

- A. Raise the model's context limit
- B. Change the tool to return only the fields the task needs
- C. Summarise the JSON with a second model call
- D. Call the tool less frequently

**5.** Which condition warrants a retry with backoff rather than surfacing an error?

- A. The request contained an invalid parameter
- B. The service returned a rate limit or a transient server error
- C. The model returned an answer you disagree with
- D. The response exceeded the expected length

**6.** A workload runs nightly over 50,000 records with no interactive requirement. Which choice reduces cost most?

- A. Streaming each request
- B. Using the largest model for accuracy
- C. Increasing concurrency against the standard endpoint
- D. Submitting the work as a batch

**7.** Accuracy on a simple extraction task is identical between a small and a large model. What should be deployed?

- A. The small model, since it meets the requirement at lower cost
- B. The large model, in case inputs change
- C. Both, alternating between them
- D. The newest model available

**8.** A task requires the model to plan across many interacting constraints and revise as it goes. What does this argue for?

- A. The smallest model, to keep cost down
- B. Splitting the task across several small models
- C. A more capable model, since the work is reasoning-heavy
- D. A longer prompt with the same model

**9.** An agent is given ten tools, three of which overlap in purpose. What is the likely consequence?

- A. Faster execution, since more options are available
- B. Lower token cost
- C. Better error handling
- D. More frequent wrong tool selection

**10.** What should terminate an agent loop?

- A. A fixed wall-clock timeout only
- B. The model deciding it is finished
- C. An explicit success condition, with a step ceiling as a backstop
- D. Running out of context

**11.** Where should a stable instruction that must apply to every turn be placed?

- A. At the end of the latest user message
- B. In the system prompt
- C. Repeated in each user message
- D. In a tool description

**12.** Which change most improves output that is correct but inconsistently formatted?

- A. Providing an example of the exact output required
- B. Raising the temperature
- C. Asking for the output to be neat
- D. Using a larger model

**13.** What is the most important property of a tool description?

- A. It states what the tool does, when to use it, and what each parameter means
- B. It is short
- C. It lists the implementation language
- D. It matches the function name exactly

**14.** Content retrieved from an external site contains instructions aimed at the model. What is the correct defence?

- A. Instruct the model in the system prompt to ignore such content
- B. Treat retrieved content as untrusted data and bound the model's permissions outside the prompt
- C. Scan for known injection phrases and block them
- D. Use a model with a larger context window

**15.** A prompt change improved results on the five examples you tested. What should happen before it reaches production?

- A. Ship it, since all five improved
- B. Ask the model to compare the two prompts
- C. Evaluate it against a held-out set that reflects real inputs, on defined criteria
- D. Ship it to a small percentage of traffic and watch error rates

---

## Answer key

| # | Answer | Domain | Why |
| --- | --- | --- | --- |
| 1 | C | Applications and Integration | A large unchanging prefix repeated per call is what caching addresses, without losing any instruction. Shortening (A) sacrifices capability, a cheaper model (B) trades quality, and fewer requests (D) changes the product |
| 2 | A | Applications and Integration | Decoupling acceptance from completion satisfies the latency contract without degrading the answer. Truncation (B) and a minimal model (C) sacrifice the result, and the timeout (D) is the stated constraint |
| 3 | D | Applications and Integration | That stop reason reports that generation hit the output ceiling. An oversized input (A) fails before generation, and neither a malformed request (B) nor a refusal (C) produces this reason |
| 4 | B | Applications and Integration | Tools should return what the task requires, which preserves context for reasoning. A larger window (A) delays the problem, a second call (C) adds cost and failure surface, and calling less often (D) does not change the payload |
| 5 | B | Applications and Integration | Rate limits and transient server errors are the recoverable class. An invalid parameter (A) will fail identically, and disagreement (C) or length (D) are not transport failures |
| 6 | D | Model Selection and Optimization | Large, uniform, latency-tolerant work is exactly the batch case, and it is materially cheaper. Streaming (A) serves interactive use, the largest model (B) raises cost, and concurrency (C) does not change unit price |
| 7 | A | Model Selection and Optimization | Where the requirement is met, the cheaper option is correct, and changing inputs are handled by re-evaluating. Insurance against hypothetical change (B), alternation (C), and recency (D) all spend without benefit |
| 8 | C | Model Selection and Optimization | Multi-step reasoning under interacting constraints is where capability differences show. A small model (A) and splitting (B) both fragment the reasoning, and prompt length (D) does not add capability |
| 9 | D | Agents and Workflows | Overlapping tools make selection ambiguous, which is where agents go wrong. Overlap does not improve speed (A), reduce cost (B), or help error handling (C) |
| 10 | C | Agents and Workflows | A defined success condition ends the loop correctly, and the ceiling bounds the failure case. A timeout alone (A) does not recognise success, the model's own judgment (B) is not a guarantee, and exhausting context (D) is a failure rather than a termination |
| 11 | B | Prompt and Context Engineering | The system prompt is designed for persistent framing across the exchange. Placing it in user turns (A, C) mixes configuration with input, and tool descriptions (D) govern tool selection |
| 12 | A | Prompt and Context Engineering | An example defines the target unambiguously, which is what formatting consistency needs. Higher temperature (B) increases variance, a vague adjective (C) does not specify, and a larger model (D) does not know your format |
| 13 | A | Tools and MCPs | The description is the model's only basis for choosing and calling the tool correctly. Brevity (B) is secondary to clarity, and implementation detail (C) and naming (D) do not guide selection |
| 14 | B | Security and Safety | The durable control is that the model cannot exceed its granted permissions regardless of what the content says. Prompt instructions (A) and phrase filters (C) are bypassable, and context size (D) is irrelevant |
| 15 | C | Eval, Testing, and Debugging | Five hand-picked cases cannot separate a real gain from noise, which is what an evaluation set settles. Self-comparison (B) is not measurement, and shipping first (A, D) makes users the test |

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

Written by the maintainer for self-assessment. [Study guide](README.md) · [Study notes](notes.md) · [Mock 1](mock-exam.md) · [Mock 3](mock-exam-3.md) · [Practice questions](practice-questions.md) · [Repository index](../README.md)
