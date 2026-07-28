# Mock exam 3: Architect – Professional

The third and final timed practice exam, with fifteen more questions that appear nowhere else in this repository. Save it for the week you intend to book: taken cold, after the [first](mock-exam-1.md) and [second](mock-exam-2.md) mocks, it is the closest thing here to a readiness check. Original questions written against the public [blueprint](README.md#skills-measured); not items from the live exam, which is covered by a non-disclosure agreement.

**How to take it.** 15 questions, 30 minutes, closed book: no notes, no documentation, no Claude. Several questions test judgment about governance and stakeholders, which carry real weight on this exam. Score yourself with the [key](#answer-key) and the [readiness table](#interpreting-your-score) afterwards.

> [!TIP]
> Stuck on a question afterwards? The [prompts for studying with Claude](../guide/prompts.md) include one for working through a question you got wrong, and one for drilling a whole domain.

---

## Questions

**1.** A client will not accept a solution whose behavior cannot be explained to their auditor. What does this constrain?

- A. The model family only
- B. The cost model
- C. The architecture, which must make decisions traceable and the controls inspectable
- D. The deployment region

**2.** What is the main risk of building directly against a single cloud's model service with no abstraction?

- A. Moving later becomes expensive, because the coupling reaches into application code
- B. Higher token cost
- C. Lower accuracy
- D. Slower responses

**3.** A solution must serve users in two regions with different data residency rules. What follows?

- A. One deployment in the cheaper region
- B. A single deployment with encryption in transit
- C. Whichever region has the lowest latency
- D. Separate deployments whose data stays within each region's boundary

**4.** A requirement is stated as make it as accurate as possible. What should the architect do?

- A. Choose the largest model and optimise from there
- B. Establish the accuracy the use case actually needs and what an error costs
- C. Build the most complex design the budget allows
- D. Defer the question until after the pilot

**5.** Two components each work correctly but the system fails intermittently at their boundary. What does this suggest?

- A. One component needs a larger model
- B. The contract between them is underspecified, particularly for edge and error cases
- C. The system needs more components
- D. The failure is transient and can be retried

**6.** A design proposes storing every model interaction indefinitely. What should the architect raise?

- A. Nothing, retention is always safer
- B. That storage is expensive
- C. That it will slow the system
- D. Why the data is needed, for how long, and what obligations retention creates

**7.** How should a solution handle the case where the model is confident and wrong?

- A. Design so that consequential outputs are verified against something independent of the model
- B. Trust the confidence signal
- C. Ask the model to double-check
- D. Use two models and take the agreement

**8.** An evaluation shows 94% accuracy. What else must be known before this is actionable?

- A. The model version only
- B. The token cost of the evaluation
- C. What the 6% look like, and what each failure costs
- D. How long the evaluation took

**9.** What should happen when a model version is updated beneath a production solution?

- A. Nothing, versions are compatible
- B. Increase monitoring for a week
- C. Roll back automatically if complaints rise
- D. Re-run the evaluation suite before the change reaches production traffic

**10.** A stakeholder asks why the solution cannot simply be fully automated. What is the most useful answer?

- A. That the technology is not ready
- B. That automation is always risky
- C. Which specific decisions carry accountability or are unverifiable, and what automating them would risk
- D. That the budget does not allow it

**11.** What should be handed over with a solution so it survives its first year?

- A. The source code
- B. The evaluation suite, the criteria, the owner, and the routine for re-checking
- C. A recorded demonstration
- D. A list of prompts used

**12.** A team reports the solution has become worse, but nothing was deployed. What is the most likely explanation?

- A. The inputs or the surrounding usage changed
- B. The model degraded on its own
- C. The prompts wore out
- D. The evaluation was wrong originally

**13.** How should prompts that determine production behavior be managed?

- A. Versioned, owned, reviewed, and evaluated on change, like code
- B. Edited in place when someone notices a problem
- C. Kept in a shared document for easy editing
- D. Frozen after launch

**14.** An organization asks how to measure whether Claude Code is worth the license cost. What should be measured?

- A. Number of tool invocations
- B. Change in the delivery outcomes the tooling was adopted to improve
- C. Number of users onboarded
- D. Hours spent in the tool

**15.** What most often blocks a team from getting good results from Claude Code on an existing codebase?

- A. The size of the repository
- B. The programming language
- C. The absence of committed context describing the conventions and structure
- D. The number of contributors

---

## Answer key

| # | Answer | Domain | Why |
| --- | --- | --- | --- |
| 1 | C | Integration | Auditability is an architectural property covering tracing and inspectable controls. Model family (A), cost (B), and region (D) do not by themselves make behavior explicable |
| 2 | A | Integration | Coupling determines the cost of change, which is the architectural concern. Cost (B), accuracy (C), and latency (D) are not consequences of the coupling itself |
| 3 | D | Integration | Residency is satisfied by keeping the data within each boundary. A single deployment (A, B) moves data across it, and latency (C) does not address the rule |
| 4 | B | Solution Design | An unbounded requirement cannot be designed against or verified, so it must be made concrete. Defaulting to maximum capability (A, C) spends without a target, and deferring (D) leaves the design unanchored |
| 5 | B | Solution Design | Boundary failures between correct components point at the contract. Capability (A) and more components (C) do not define the interface, and retrying (D) hides it |
| 6 | D | Governance, Safety & Risk Management | Retention creates obligations and risk, so purpose and duration must justify it. Treating retention as free of risk (A) is the error, and cost (B) and speed (C) are minor by comparison |
| 7 | A | Governance, Safety & Risk Management | Independence is what catches confident error. Confidence (B) is not evidence, self-checking (C) is not independent, and two models can agree and both be wrong (D) |
| 8 | C | Evaluation, Testing & Optimization | A headline rate is only meaningful alongside the shape and cost of the failures. Version (A), cost (B), and duration (D) do not describe the risk |
| 9 | D | Evaluation, Testing & Optimization | A change to the thing that determines behavior invalidates prior measurement. Assuming compatibility (A) is unsafe, and monitoring (B) or reacting to complaints (C) detects after users are affected |
| 10 | C | Stakeholder Communication & Lifecycle Management | A specific, reasoned boundary is actionable and can be revisited. Generic claims about readiness (A) or risk (B) are not, and budget (D) is not the reason |
| 11 | B | Stakeholder Communication & Lifecycle Management | Continuity depends on being able to measure and maintain, with someone responsible. Code (A), a demonstration (C), and prompts (D) are artefacts without the means to verify them |
| 12 | A | Claude Models, Prompting & Context Engineering | Behavior changes with what is fed to it, and distribution drift is the usual cause. Models do not degrade unprompted (B), prompts do not wear out (C), and the original evaluation is not the first suspect (D) |
| 13 | A | Claude Models, Prompting & Context Engineering | Anything that determines production behavior needs the lifecycle of code. Ad hoc edits (B) and open documents (C) invite unreviewed change, and freezing (D) blocks improvement |
| 14 | B | Developer Productivity & Operational Enablement | Value is the outcome moved, not the activity generated. Invocations (A), onboarding (C), and time in tool (D) measure usage rather than benefit |
| 15 | C | Developer Productivity & Operational Enablement | Missing project context is the usual cause, and it is the one the team can fix. Size (A), language (B), and contributor count (D) do not by themselves prevent good results |

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
