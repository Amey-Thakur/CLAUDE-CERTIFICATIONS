# Mock exam 3: Associate – Foundations

The third and final timed practice exam, with fifteen more questions that appear nowhere else in this repository. Save it for the week you intend to book: taken cold, after the [first](mock-exam-1.md) and [second](mock-exam-2.md) mocks, it is the closest thing here to a readiness check. Original questions written against the public [blueprint](README.md#skills-measured); not items from the live exam, which is covered by a non-disclosure agreement.

**How to take it.** 15 questions, 30 minutes, closed book: no notes, no documentation, no Claude. Answer every question, since unanswered items score zero. Flag anything you are unsure of and return to it. Score yourself with the [key](#answer-key) and the [readiness table](#interpreting-your-score) afterwards.

> [!TIP]
> Stuck on a question afterwards? The [prompts for studying with Claude](../guide/prompts.md) include one for working through a question you got wrong, and one for drilling a whole domain.

---

## Questions

**1.** A summary cites a statistic that turns out to be correct. Does that validate the rest of the summary?

- A. Yes, one verified claim indicates the whole is reliable
- B. Yes, if the statistic was the hardest claim
- C. No, each material claim needs its own check
- D. Only if the source was named

**2.** Claude declines to answer part of a request and explains why. How should this be read?

- A. As information about a limit or a policy that is worth understanding before proceeding
- B. As a failure that should be worked around
- C. As a sign the prompt was too long
- D. As a reason to switch models

**3.** You need to know whether a long report supports a specific conclusion. What is the most reliable approach?

- A. Ask for a summary and read that
- B. Ask whether the report supports the conclusion
- C. Ask for a confidence score
- D. Ask for the passages that bear on the conclusion, then read those passages yourself

**4.** A manual process takes four hours and produces a document nobody reads. What should happen before automating it?

- A. Automate it, since four hours is significant
- B. Establish whether the document is needed at all
- C. Automate it and measure adoption afterwards
- D. Split it across more people

**5.** Which sequencing is correct when introducing Claude to a recurring team process?

- A. Automate the whole process, then refine
- B. Start with the step that is bounded and checkable, prove it, then extend
- C. Start with the hardest step, since it has most value
- D. Let each person adopt it however they prefer

**6.** A policy forbids sending customer data to external services. A colleague asks Claude to summarise a customer email. What applies?

- A. Nothing, because summarising is not sending
- B. The policy only if the customer is named
- C. Nothing, because the output stays internal
- D. The policy, since the email is customer data

**7.** What is the correct response to a request that a model output be presented as human-written to a customer?

- A. Decline to misrepresent it, and raise the disclosure question with whoever owns the relationship
- B. Comply, since the customer cares about quality not provenance
- C. Comply if the output was heavily edited
- D. Comply and record the decision internally

**8.** A prompt asks for a recommendation and gets a balanced discussion instead. What is the most likely cause?

- A. The model is incapable of recommending
- B. The temperature is too high
- C. The prompt did not state that a single recommendation with a reason was required
- D. The input was too short

**9.** What is the most effective way to get output pitched at the right level for a specific audience?

- A. Ask for it to be clear
- B. Ask for a shorter response
- C. Ask for simpler words
- D. Name the audience and what they already know

**10.** A colleague uses the largest model for every task including formatting. What should you point out?

- A. Nothing, capability is never wasted
- B. That the largest model is less accurate on simple tasks
- C. That matching the model to the work saves cost without losing anything on simple tasks
- D. That formatting should be done manually

**11.** When does the choice of interface matter more than the choice of model?

- A. Never, the model determines the outcome
- B. When the obstacle is how people supply context and act on output, not the quality of the answer
- C. Only for very large teams
- D. Only when cost is constrained

**12.** What is the risk of adding a document to project knowledge without removing the version it replaces?

- A. Both versions can be drawn on, producing answers that mix current and superseded material
- B. Storage cost
- C. Slower responses
- D. The project will refuse to answer

**13.** Which is the better test of whether something belongs in project knowledge?

- A. Whether every conversation in the project would benefit from it
- B. Whether it is long enough to be worth uploading
- C. Whether it was recently created
- D. Whether it is confidential

**14.** A previously reliable prompt now returns shorter answers than before. What is worth checking first?

- A. Whether the model is deprecated
- B. Whether the input or the instructions changed, including anything added to the project
- C. Whether the network is slow
- D. Whether the account has hit a limit

**15.** Someone reports that Claude is wrong about a fact that it stated correctly last week. What is the most useful first question?

- A. Which model did you use
- B. How long was the conversation
- C. What exactly did you ask, and what did it reply
- D. Have you tried again

---

## Answer key

| # | Answer | Domain | Why |
| --- | --- | --- | --- |
| 1 | C | Output Evaluation and Validation | Verification does not generalise from one claim to the others. Treating it as a proxy for the whole (A, B) is the error tested, and naming a source (D) does not verify the remaining claims |
| 2 | A | Output Evaluation and Validation | A refusal with a reason is a signal about the task, not an obstacle to route around. Working around it (B) ignores the reason, and neither prompt length (C) nor model choice (D) is indicated |
| 3 | D | Output Evaluation and Validation | Retrieving the evidence and reading it keeps the judgment with you. A summary (A) and a direct verdict (B) hand the judgment to the model, and a confidence score (C) is not evidence |
| 4 | B | Workflow Integration and Solution Design | Automating unnecessary work makes waste faster. Proceeding regardless (A, C) skips the question, and redistributing it (D) does not address whether it is needed |
| 5 | B | Workflow Integration and Solution Design | A bounded first step produces evidence and trust cheaply. Full automation first (A) risks everything at once, the hardest step (C) is the least likely to succeed early, and uncoordinated adoption (D) produces drift |
| 6 | D | Governance, Risk, and Responsible Use | Submitting the content is the act the policy governs. Framing it as summarising (A) or by where the output goes (C) misreads the policy, and it is not limited to named individuals (B) |
| 7 | A | Governance, Risk, and Responsible Use | Actively misrepresenting provenance is the issue, and it belongs to the person accountable for the relationship. Editing (C) and internal records (D) do not make the representation true, and quality (B) is not the point |
| 8 | C | Prompting and Task Execution | Output shape follows the instruction, and no decision was requested. Incapability (A) is not the issue, and neither temperature (B) nor input length (D) determines whether a recommendation is given |
| 9 | D | Prompting and Task Execution | Naming the reader and their prior knowledge is what calibrates level. Clarity (A), length (B), and vocabulary (C) are consequences rather than the instruction |
| 10 | C | Product and Model Selection | Fit-to-task is the principle, and simple work does not benefit from extra capability. Capability is not free (A), larger models are not less accurate on simple tasks (B), and manual work (D) is not the alternative |
| 11 | B | Product and Model Selection | Where adoption or context-supply is the bottleneck, interface dominates. Treating the model as decisive (A) misses that, and neither team size (C) nor cost (D) defines the case |
| 12 | A | Configuration and Knowledge Management | Superseded material remains retrievable and contradicts the current version. Storage (B) and speed (C) are minor, and the project does not refuse (D) |
| 13 | A | Configuration and Knowledge Management | Recurrence across conversations is what distinguishes shared knowledge from prompt content. Length (B), recency (C), and sensitivity (D) are unrelated to that test |
| 14 | B | Troubleshooting and Optimization | A behavioral change points to a change in inputs or configuration. Deprecation (A), network (C), and limits (D) produce errors rather than shorter answers |
| 15 | C | Troubleshooting and Optimization | The exact exchange is what makes the claim examinable. Model (A), length (B), and retrying (D) may matter later but none of them establishes what happened |

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
