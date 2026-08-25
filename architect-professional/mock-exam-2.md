# Mock exam 2: Architect – Professional

A second timed practice exam in the official style, with fifteen questions that appear nowhere else in this repository. Take it after [mock exam 1](mock-exam-1.md) and the [practice questions](practice-questions.md), when you want a fresh measure rather than a review. Original questions written against the public [blueprint](README.md#skills-measured); not items from the live exam, which is covered by a non-disclosure agreement.

**How to take it.** 15 questions, 30 minutes, closed book: no notes, no documentation, no Claude. Several questions test judgment about governance and stakeholders, which carry real weight on this exam. Score yourself with the [key](#answer-key) and the [readiness table](#interpreting-your-score) afterwards.

> [!TIP]
> Stuck on a question afterwards? The [prompts for studying with Claude](../guide/prompts.md) include one for working through a question you got wrong, and one for drilling a whole domain.

---

## Questions

**1.** A client requires that inference run inside their own AWS account. What does this determine?

- A. The model family only
- B. That a data processing agreement is sufficient
- C. Deployment through Amazon Bedrock in the client's account and region
- D. That request logging must be disabled

**2.** An enterprise standardised on Google Cloud wants identity and audit handled by existing controls. What follows?

- A. Deploy through Vertex AI so the platform's identity, billing, and audit apply
- B. Use the Claude API and rebuild the controls
- C. Use Bedrock for feature parity
- D. Let each team decide

**3.** What is the main architectural benefit of routing all model traffic through one internal service?

- A. Lower token prices
- B. It removes the need for evaluation
- C. It guarantees lower latency
- D. Authentication, rate limiting, logging, and routing are applied consistently in one place

**4.** Two designs both satisfy the requirement; one is materially simpler. What decides?

- A. The more capable design, since headroom is valuable
- B. Whether any stated requirement needs the extra capability, against the ongoing cost of complexity
- C. Whichever the team prefers to build
- D. The one with more components, for flexibility

**5.** A required compliance control depends on the model behaving correctly. What is the correct judgment?

- A. Acceptable if measured accuracy is very high
- B. Not acceptable: a required control must be enforced deterministically outside the model
- C. Acceptable with a documented residual risk
- D. Acceptable if a larger model is used

**6.** Where should the boundary of automation be drawn in a solution that makes customer-affecting decisions?

- A. Wherever the model performs well in testing
- B. As far as the budget allows
- C. At whatever the client requests
- D. Where accountability for the decision sits, keeping those decisions with a person

**7.** What must exist before a solution is declared production-ready?

- A. A defined success criterion and measured performance against representative data
- B. A successful demonstration
- C. Sign-off from the engineering team
- D. A completed cost model

**8.** An evaluation set contains only cases the system already handles. What is the effect?

- A. It provides a reliable quality measure
- B. It is fine if it is large
- C. It overstates performance and conceals the failures that matter
- D. It matters only in regulated contexts

**9.** How should a request to log every prompt and response for audit be handled?

- A. Implement it, since audit takes precedence
- B. Decline, because logging creates risk
- C. Log responses but not prompts
- D. Establish what the audit requires, because prompts and responses may contain personal or confidential data

**10.** Who is accountable when an automated Claude workflow produces a harmful decision?

- A. The model provider
- B. The engineer who wrote the prompt
- C. The organization that deployed it
- D. No one, because the decision was automated

**11.** A sponsor asks for one number that shows whether the solution is working. What is the right response?

- A. Give the headline accuracy figure
- B. Give the measure tied to the decision they face, and state what it does not cover
- C. Explain that this cannot be reduced to a number
- D. Give the model's benchmark score

**12.** A ten-user pilot is about to expand to two thousand users. What should the architect raise first?

- A. Which assumptions held at ten users and may not hold at two thousand
- B. License cost
- C. Whether a larger model is needed
- D. The training rollout plan

**13.** How should a model be chosen for a solution containing several distinct tasks?

- A. Match each task to the smallest model meeting its requirement, and evaluate the choices
- B. One model everywhere, for simplicity
- C. The largest model everywhere, for safety
- D. The newest model everywhere

**14.** How should the context window be treated in a production design?

- A. As capacity to fill as completely as possible
- B. As a budget allocated deliberately between instructions, retrieved material, and working state
- C. As a concern only for long documents
- D. As a setting to increase whenever quality drops

**15.** An organization wants consistent Claude Code practice across dozens of repositories. What is most durable?

- A. A policy document circulated once
- B. A single training session
- C. Committed project memory and shared skills in each repository, reviewed like code
- D. Requiring approval for every use

---

## Answer key

| # | Answer | Domain | Why |
| :---: | --- | --- | --- |
| 1 | C | Integration | Running inside the client's own cloud boundary is what the requirement describes. A contract (B) and logging settings (D) do not keep the data in the account, and the model family (A) is a separate choice |
| 2 | A | Integration | Aligning with the governed platform makes existing controls apply without duplication. Rebuilding (B) drifts, a different cloud (C) creates a second control plane, and per-team choice (D) removes governance |
| 3 | D | Integration | A single integration point is where cross-cutting concerns are enforced and changed once. It does not change unit price (A), remove evaluation (B), or reduce latency (C) |
| 4 | B | Solution Design & Architecture | Complexity is paid for continuously, so it must be bought by a real requirement. Headroom (A), preference (C), and speculative flexibility (D) pay that cost without justification |
| 5 | B | Solution Design & Architecture | A control that must hold needs a guarantee, which probabilistic behavior cannot supply. High accuracy (A), documentation (C), and model size (D) do not convert a tendency into a guarantee |
| 6 | D | Solution Design & Architecture | Accountability determines what may be automated at all, and that boundary is an architectural decision. Test performance (A), budget (B), and unexamined requests (C) do not address responsibility |
| 7 | A | Evaluation, Testing & Optimization | Readiness is a measured claim against a stated bar. A demonstration (B), consensus (C), and cost (D) do not establish whether it works |
| 8 | C | Evaluation, Testing & Optimization | An unrepresentative sample measures the wrong distribution, and size does not correct bias. It is not reliable (A), scale does not fix it (B), and the problem is general (D) |
| 9 | D | Governance, Safety & Risk Management | Audit and data protection are both real, and the design must serve the audit purpose without retaining more than warranted. Blanket action (A) or refusal (B) ignores one side, and an arbitrary split (C) is unjustified |
| 10 | C | Governance, Safety & Risk Management | Deploying an automated decision means owning its outcomes. The provider (A) supplies a capability, individual authorship (B) does not transfer organizational responsibility, and automation does not remove accountability (D) |
| 11 | B | Stakeholder Communication & Lifecycle Management | A useful metric matches the decision and is honest about its limits. A bare accuracy figure (A) and a benchmark (D) can mislead, and refusing (C) fails the sponsor |
| 12 | A | Stakeholder Communication & Lifecycle Management | Scale invalidates assumptions about inputs, support, and edge cases, and surfacing those is the architect's contribution. Cost (B), model size (C), and training (D) follow from knowing what breaks |
| 13 | A | Claude Models, Prompting & Context Engineering | Different tasks have different requirements, and matching each keeps cost proportionate on evidence. Uniform choices (B, C, D) optimise for convenience rather than fit |
| 14 | B | Claude Models, Prompting & Context Engineering | Context is scarce and its allocation drives quality, so it is designed. Filling it (A) dilutes, it matters beyond long documents (C), and enlarging it (D) does not fix allocation |
| 15 | C | Developer Productivity & Operational Enablement | Conventions persist when they live in the repository and are reviewed with the work. Policies (A) and training (B) fade, and per-use approval (D) adds friction without conveying practice |

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
