# Mock exam 2: Associate – Foundations

A second timed practice exam in the official style, with fifteen questions that appear nowhere else in this repository. Take it after [mock exam 1](mock-exam-1.md) and the [practice questions](practice-questions.md), when you want a fresh measure rather than a review. Original questions written against the public [blueprint](README.md#skills-measured); not items from the live exam, which is covered by a non-disclosure agreement.

**How to take it.** 15 questions, 30 minutes, closed book: no notes, no documentation, no Claude. Answer every question, since unanswered items score zero. Flag anything you are unsure of and return to it. Score yourself with the [key](#answer-key) and the [readiness table](#interpreting-your-score) afterwards.

> [!TIP]
> Stuck on a question afterwards? The [prompts for studying with Claude](../guide/prompts.md) include one for working through a question you got wrong, and one for drilling a whole domain.

---

## Questions

**1.** Claude returns a policy answer that matches your expectation exactly, with no citation. What does the match tell you?

- A. The answer is confirmed, since it agrees with your understanding
- B. The answer is probably correct but should be reworded
- C. Nothing about accuracy, because agreement with an expectation is not evidence
- D. The model has read the policy document

**2.** A colleague asks Claude to check its own earlier answer, and it confirms the answer. How much weight does the confirmation carry?

- A. None on its own, because the check is not independent of the thing being checked
- B. Substantial, because the model reviewed its own reasoning
- C. Substantial if the confirmation is detailed
- D. It depends on the model used

**3.** A report drafted with Claude contains one figure you cannot verify from any available source. What is the appropriate handling before circulation?

- A. Circulate it with a general disclaimer about AI assistance
- B. Keep the figure and mark it as an estimate
- C. Ask Claude to provide a source and keep whatever it returns
- D. Remove the figure and note that it could not be verified

**4.** Which of these is the strongest candidate to hand to Claude in a monthly close process?

- A. Approving the final journal entries
- B. Drafting the variance commentary from figures that are already agreed
- C. Deciding which variances require investigation
- D. Signing off the reconciliation

**5.** A workflow produces good output but nobody uses it. What should be examined first?

- A. Whether the model should be upgraded
- B. Whether the output arrives where the work actually happens, in a form people can act on
- C. Whether the prompt is long enough
- D. Whether more people need training

**6.** A team wants to paste anonymised customer feedback into Claude for theme analysis. What remains a risk after names are removed?

- A. Nothing, since anonymisation removes the risk entirely
- B. The model may store the text permanently
- C. Theme analysis is unreliable on anonymised data
- D. Free text can still identify people through specific details, so review before sending is still needed

**7.** Who should decide whether a Claude-assisted output is fit to send to a customer?

- A. The person accountable for the customer relationship
- B. Whoever wrote the prompt
- C. The model, if asked to assess its own output
- D. Nobody, if the workflow was approved in advance

**8.** A prompt works well until the input document is much longer than usual, when quality drops. What is the most likely explanation?

- A. The model became less capable
- B. The prompt is too short
- C. The relevant material is now competing with far more surrounding text
- D. Longer documents always produce worse output

**9.** You want the same analysis applied to fifty documents with consistent output. What matters most?

- A. Using the largest model available
- B. Processing the documents in one conversation
- C. Reviewing only a sample of the outputs
- D. Fixing the prompt and the required output structure, and applying both unchanged to every document

**10.** A task must return an answer within a second for an interactive interface, and the work is simple classification. What follows?

- A. Use the most capable model to be safe
- B. Batch the requests
- C. Use the smallest model that meets the accuracy requirement, since latency is the binding constraint
- D. Increase the context supplied

**11.** What is the correct reading of a model's published benchmark score when choosing for a specific business task?

- A. It predicts performance on your task
- B. It is a general signal that does not substitute for evaluating on your own task
- C. It is irrelevant
- D. It determines the price you should expect to pay

**12.** Two teams keep separate copies of the same reference documents in their own projects. What is the main risk?

- A. The copies drift apart, and the two teams begin answering the same question differently
- B. Higher storage cost
- C. Slower responses
- D. The model becomes confused between projects

**13.** What is the right first step when setting up a project for a recurring task?

- A. Decide what the task needs to know every time, and add only that
- B. Upload every document the team owns
- C. Write the longest possible instruction
- D. Add documents as questions come up, without review

**14.** A user reports that Claude gave a wrong answer, but you cannot reproduce it. What is the most useful next step?

- A. Assume the user made an error
- B. Obtain the exact prompt, inputs, and configuration they used
- C. Increase the model size for everyone
- D. Add a warning to the interface

**15.** Output quality varies between runs of an identical prompt on identical input. What does this indicate?

- A. The system is broken
- B. The temperature must be zero for all tasks
- C. Some variation is expected, and the task needs constraints tight enough that the variation does not matter
- D. The input must be shortened

---

## Answer key

| # | Answer | Domain | Why |
| --- | --- | --- | --- |
| 1 | C | Output Evaluation and Validation | Agreement with what you already believed is the easiest error to miss, since nothing prompts a check. Neither confirmation (A), rewording (B), nor an assumption about retrieval (D) establishes that the claim is true |
| 2 | A | Output Evaluation and Validation | Self-review is not an independent source and cannot establish correctness. Detail (C) and model choice (D) do not make a self-check independent |
| 3 | D | Output Evaluation and Validation | An unverifiable claim should not be presented as fact, and a labeled gap is honest. A blanket disclaimer (A) does not address the specific figure, an unfounded estimate (B) misrepresents it, and a citation produced on demand (C) needs the same verification |
| 4 | B | Workflow Integration and Solution Design | Drafting from agreed inputs is bounded and checkable. Approval (A), sign-off (D), and the decision about what to investigate (C) all carry accountability |
| 5 | B | Workflow Integration and Solution Design | Adoption usually fails on fit with the existing process rather than on output quality. Model (A) and prompt length (C) address quality that is already acceptable, and training (D) treats a symptom |
| 6 | D | Governance, Risk, and Responsible Use | Removing names does not remove identifying detail from free text, which is why a review step remains. Treating anonymisation as complete (A) is the error tested, and neither storage assumptions (B) nor reliability (C) is the governance issue here |
| 7 | A | Governance, Risk, and Responsible Use | Accountability for the outgoing communication decides the question. Prompt authorship (B) is incidental, self-assessment (C) is not independent, and prior approval of a workflow (D) does not review this instance |
| 8 | C | Prompting and Task Execution | Dilution across a much longer input is the usual cause of this pattern. The model has not changed (A), prompt length (B) is not the variable that changed, and length alone is not determinative (D) |
| 9 | D | Prompting and Task Execution | Consistency across a set comes from holding the instruction and the output shape constant. Model size (A) does not create consistency, one long conversation (B) invites drift, and sampling (C) is a review policy rather than a design |
| 10 | C | Product and Model Selection | With a hard latency requirement and a simple task, the smallest sufficient model is the fit. The most capable model (A) spends latency for accuracy that is not needed, batching (B) breaks interactivity, and more context (D) adds cost and time |
| 11 | B | Product and Model Selection | Benchmarks indicate general capability and cannot stand in for measurement on the actual task. Treating them as predictive (A) or irrelevant (C) are both wrong, and they do not set price (D) |
| 12 | A | Configuration and Knowledge Management | Duplicated knowledge diverges as each copy is maintained separately, producing inconsistent answers. Storage (B) and speed (C) are minor, and projects do not leak into one another (D) |
| 13 | A | Configuration and Knowledge Management | A deliberate, minimal base keeps retrieval sharp and is maintainable. Uploading everything (B) and accumulating without review (D) both dilute, and instruction length (C) is not the question |
| 14 | B | Troubleshooting and Optimization | Reproduction depends on the exact conditions, and gathering them is the only way to diagnose. Dismissing the report (A) discards the signal, and a model change (C) or a warning (D) acts before the cause is known |
| 15 | C | Troubleshooting and Optimization | Generation is not deterministic, so the design must tolerate variation within acceptable bounds. Treating it as breakage (A) misreads normal behavior, a universal temperature rule (B) is too blunt, and input length (D) is unrelated |

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
