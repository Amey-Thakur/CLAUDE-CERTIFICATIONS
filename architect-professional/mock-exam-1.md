# Mock exam 1: Architect – Professional

A timed practice exam in the official style. Unlike the [practice questions](practice-questions.md), the domains are hidden and the answers sit at the end, so this measures readiness rather than teaching. Original questions written against the public [blueprint](README.md#skills-measured); not items from the live exam, which is covered by a non-disclosure agreement.

**How to take it.** 15 questions, 30 minutes, closed book: no notes, no documentation, no Claude. Several questions test judgment about stakeholders and governance, which carry real weight on this exam. Score yourself with the [key](#answer-key) and the [readiness table](#interpreting-your-score) afterwards.

---

## Questions

**1.** A retailer wants Claude to answer product questions from a 40,000-document catalog that changes daily. Which architecture fits?

- A. Fine-tune a model on the catalog nightly
- B. Load the catalog into the system prompt
- C. Retrieval over an index refreshed as the catalog changes, with the model answering from retrieved context
- D. An autonomous agent that browses the public website

**2.** After a re-index, your retrieval system returns semantically similar but commercially wrong products. Which investigation comes first?

- A. The generation prompt
- B. The model version
- C. The user interface
- D. Chunking and embedding configuration, and whether the index was rebuilt consistently

**3.** An agent used by 300 employees exposes 45 tools across eight systems. Selection quality is degrading. What is the architectural response?

- A. Scope toolsets per task or role, with progressive discovery for the rest
- B. Shorten all tool descriptions
- C. Merge tools into a few multi-mode tools
- D. Replace the agent with a larger model

**4.** Which evaluation design best fits a summarization feature where quality is subjective?

- A. Exact match against reference summaries
- B. A rubric covering the failure modes that matter, applied by model graders and periodically audited by humans on a labeled set
- C. Average output length compared to references
- D. User thumbs-up counts alone

**5.** Before a prompt change reaches all users, what is the disciplined sequence?

- A. Ship it and monitor complaints
- B. Team vote followed by rollout
- C. Regression evaluation, then a controlled A/B against the current prompt on predefined metrics, then rollout
- D. Rollout with a feedback form

**6.** A hospital system requires that protected health information never reach the model provider, while clinicians need free-text search. Which design satisfies both?

- A. A policy instructing clinicians not to type identifiers
- B. A system prompt instructing the model to disregard PHI
- C. Restricting the feature to structured queries only
- D. A de-identification layer that removes or tokenizes PHI before the call, with local re-association and auditing

**7.** Which is the correct application of human-in-the-loop review at scale?

- A. Route by confidence and consequence, so low-confidence and high-impact cases reach humans while routine cases flow through
- B. Review every output regardless of risk
- C. Review a fixed 10% sample chosen at random
- D. Review only what users complain about

**8.** An executive sponsor demands a single accuracy number for a system whose performance varies sharply by document type. What does a competent architect present?

- A. The highest observed number
- B. Performance broken out by document type with the aggregate, the measurement method, and what the business outcome is after human review
- C. A refusal to quantify
- D. An average weighted to look favorable

**9.** Your design must satisfy GDPR for EU customer data. Which requirement most directly shapes the architecture?

- A. Response latency targets
- B. The choice of programming language
- C. Data minimization, purpose limitation, and the ability to delete personal data on request
- D. The number of model providers

**10.** Which is the correct reason to prefer a workflow over an agent for a document intake process?

- A. Workflows are always more accurate
- B. Agents cannot process documents
- C. Workflows use less context
- D. The processing path is known in advance, so deterministic orchestration is cheaper, testable, and auditable

**11.** An application sends an identical 12,000-token policy preamble on every request. Which optimization addresses both latency and cost?

- A. Ordering the static preamble first and enabling prompt caching
- B. Splitting the preamble across two requests
- C. Summarizing the preamble with the model at request time
- D. Moving the preamble into a few-shot block

**12.** What belongs in an architecture decision record for a Claude system?

- A. The final design only
- B. The decision, the alternatives considered, the tradeoffs, and the constraints that drove the choice
- C. The team members involved
- D. The implementation timeline

**13.** Observability for a production agent should capture which of the following to make incidents diagnosable?

- A. Final outputs only
- B. Aggregate latency metrics only
- C. Traces of tool calls, retrieved context, and decision points alongside outputs
- D. User feedback only

**14.** A partner team wants to adopt your Claude Code setup. What makes adoption durable rather than a one-time handoff?

- A. A recorded walkthrough
- B. A shared chat channel
- C. Individual coaching sessions
- D. Version-controlled shared configuration, common skills and commands, and an onboarding path that new engineers follow

**15.** Which change best reduces risk in an agent that can both read and modify production records?

- A. Separating read and write capabilities, granting write access only where the role requires it, and gating writes behind explicit approval
- B. Logging modifications for later review
- C. Requiring a longer system prompt about caution
- D. Running the agent during business hours only

---

## Answer key

| # | Answer | Domain | Why |
| :---: | --- | --- | --- |
| 1 | C | Solution Design & Architecture | Frequently changing knowledge belongs in retrieval, not in weights or a context window |
| 2 | D | Integration | Degradation following a re-index points at chunking, embeddings, and index consistency |
| 3 | A | Integration | At large tool counts, scoping and progressive discovery preserve selection quality |
| 4 | B | Evaluation, Testing & Optimization | Subjective quality becomes measurable through rubrics, labeled sets, and mixed methodology |
| 5 | C | Evaluation, Testing & Optimization | Prompt changes are production changes: regression first, then a controlled comparison |
| 6 | D | Governance, Safety & Risk Management | Compliance boundaries are enforced architecturally before data crosses, and audited |
| 7 | A | Governance, Safety & Risk Management | Confidence and consequence routing makes human review affordable and effective |
| 8 | B | Stakeholder Communication & Lifecycle Management | Honest segmentation plus method and end-to-end outcome is what earns and keeps trust |
| 9 | C | Governance, Safety & Risk Management | GDPR drives minimization, purpose limitation, and erasure, all of which shape design |
| 10 | D | Solution Design & Architecture | Known path, deterministic orchestration; autonomy earns its complexity only when the path is not known |
| 11 | A | Claude Models, Prompting & Context Engineering | A stable cached prefix cuts time-to-first-token and per-request cost together |
| 12 | B | Stakeholder Communication & Lifecycle Management | A decision record captures alternatives and tradeoffs, not just the outcome |
| 13 | C | Evaluation, Testing & Optimization | Without traces of tool calls and retrieved context, failures cannot be localized to a layer |
| 14 | D | Developer Productivity & Operational Enablement | Shared, versioned configuration with an onboarding path is what makes adoption stick |
| 15 | A | Integration | Least privilege plus approval gates on writes reduces the surface rather than monitoring it |

## Interpreting your score

| Raw score | Reading |
| --- | --- |
| 13 to 15 | Comfortable. Review misses and book the exam |
| 10 to 12 | Close. Target weak domains, and do not neglect governance and stakeholder material, which together are 28% of the real exam |
| 7 to 9 | More study needed. Build or dissect an end-to-end system with retrieval, evaluation, and observability |
| 6 or fewer | Start from the exam guide and the engineering articles in [official resources](../guide/resources.md) |

This scale is a study aid, not a predictor. The real exam reports a scaled score from 100 to 1,000 with 720 to pass.

Tally misses by domain; two or more in one domain marks your next study target, as the real score report's percent-correct breakdown would.

---

Written by the maintainer for self-assessment. [Study guide](README.md) · [Study notes](notes.md) · [Mock 2](mock-exam-2.md) · [Mock 3](mock-exam-3.md) · [Practice questions](practice-questions.md) · [Repository index](../README.md)
