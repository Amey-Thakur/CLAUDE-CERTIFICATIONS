# Practice questions: Architect – Professional

Ten original practice questions written for this repository against the public [exam blueprint](README.md#skills-measured), in the official item style. They are unofficial practice aids, not items from the live exam, which is covered by a non-disclosure agreement. Coverage follows the domain weights. For unlimited practice, use [Practice with Claude](../guide/practice.md).

**1. Integration.** An internal agent for account managers can read CRM records, draft emails, update opportunities, and delete contacts. Account managers only ever read records and draft emails through it. Under least privilege, what is the right change?

- A. Log every update and deletion for later audit
- B. Remove the update and delete capabilities from the agent's configuration entirely
- C. Add a confirmation dialog before updates and deletions
- D. Restrict deletions to business hours

<details><summary>Answer and rationale</summary>

**B.** Least privilege removes capabilities the role does not need, eliminating the attack and error surface rather than monitoring it. Logging (A) and confirmations (C) are compensating controls around a privilege that should not exist, and scheduling (D) narrows the window without closing it.

</details>

**2. Integration.** After a nightly document refresh, your RAG assistant's answers turned confident but wrong. Model version, prompts, and latency are unchanged. Where do you look first?

- A. The model, which may have degraded overnight
- B. The retrieval and indexing layer: whether the refresh broke the index, changed chunking, or introduced mismatched embeddings
- C. The system prompt wording
- D. The temperature setting

<details><summary>Answer and rationale</summary>

**B.** The only thing that changed is the document pipeline, and confident-but-wrong is the signature of plausible-but-irrelevant retrieved context. The pinned model (A), unchanged prompt (C), and sampling (D) do not correlate with the refresh.

</details>

**3. Integration.** Your platform will expose forty internal capabilities to agents across many teams. Loading all forty tool definitions into every agent's context is bloating prompts and degrading tool selection. What is the architectural remedy?

- A. Shorter tool descriptions across the board
- B. Progressive discovery: agents load a small task-relevant toolset, with search or namespacing to pull in others when needed
- C. One mega-tool with a mode parameter selecting among forty behaviors
- D. Limit the platform to ten capabilities

<details><summary>Answer and rationale</summary>

**B.** At large tool counts, progressive discovery beats monolithic context: each agent sees what its task needs. Uniformly terser descriptions (A) trade selection quality for tokens, a mode-switch mega-tool (C) hides forty behaviors from the selection mechanism entirely, and capping the platform (D) sacrifices the requirement.

</details>

**4. Solution Design.** A bank wants a system that answers loan officers' policy questions with citations, and separately drafts decline letters from structured decision data. A vendor proposes one autonomous multi-agent system for both. What is the sounder architecture?

- A. The proposed multi-agent system, since both tasks involve documents
- B. Two simple components: a retrieval-augmented answer service for policy questions, and a templated generation workflow for letters, each evaluated on its own metrics
- C. One agent with all tools and a routing prompt
- D. A single fine-tuned model for both

<details><summary>Answer and rationale</summary>

**B.** Two well-understood problems with different shapes deserve the two cheapest reliable structures, independently testable and governable. Shared document-ness (A) is not an architectural argument, one agent with everything (C) couples unrelated risk profiles, and fine-tuning (D) is the most expensive path to problems retrieval and templates already solve.

</details>

**5. Solution Design.** Your architecture review board asks why you chose a deterministic workflow over an autonomous agent for claims intake. Which justification reflects the tested decision framework?

- A. Agents are a newer pattern and less proven in general
- B. The intake path is fully known in advance, so deterministic orchestration is cheaper, auditable, and reliable; autonomy earns its complexity only where the model must choose the path
- C. Workflows always outperform agents
- D. The team lacked time to build an agent

<details><summary>Answer and rationale</summary>

**B.** The framework is structural fit: known path, deterministic orchestration; open-ended path, agent. Novelty (A) and universal claims (C) are not engineering arguments, and resourcing (D) justifies a schedule, not an architecture.

</details>

**6. Evaluation, Testing & Optimization.** Legal review quality is subjective, and your team disagrees about whether the assistant's clause summaries are "good." What makes evaluation tractable?

- A. Ship and count complaints
- B. Define a rubric with the failure modes that matter, build a labeled evaluation set with counsel, and combine rubric-based model grading with periodic human review
- C. Exact string match against one reference summary per clause
- D. Grade outputs by length

<details><summary>Answer and rationale</summary>

**B.** Subjective quality becomes measurable through rubrics, labeled sets, and mixed methodology with humans anchoring the judgment. Complaint-counting (A) measures too late, exact match (C) fails every valid paraphrase, and length (D) measures nothing.

</details>

**7. Evaluation, Testing & Optimization.** A prompt change looks better in demos. Before rolling it to all users, what is the disciplined path?

- A. Roll it out; demos are representative
- B. Run it against the regression evaluation set, then A/B it against the current prompt on real traffic with predefined metrics before full rollout
- C. Ask the team to vote
- D. Roll out to everyone with a feedback banner

<details><summary>Answer and rationale</summary>

**B.** Changes to prompts are production changes: regression evaluation catches breakage, and an A/B on defined metrics establishes improvement before exposure. Demos (A) and votes (C) are anecdotes, and full rollout with a banner (D) is the experiment without the control.

</details>

**8. Governance, Safety & Risk Management.** A healthcare client requires that no protected health information reach the model provider, while clinicians want free-text queries about patients. Which design meets both?

- A. Trust clinicians to avoid typing identifiers
- B. A de-identification layer that strips or tokenizes PHI before the API call, re-associating results locally, with logging and periodic audits of the boundary
- C. A system prompt instructing the model to forget PHI
- D. Blocking free-text queries entirely

<details><summary>Answer and rationale</summary>

**B.** Compliance boundaries are enforced by architecture: PHI is removed before it crosses, and the control is auditable. Trust (A) is not a control, model instructions (C) act after the data already crossed, and a hard block (D) fails the stated business need that a compliant design can meet.

</details>

**9. Stakeholder Communication & Lifecycle Management.** Your Claude solution's executive sponsor asks for "99.9% accuracy or we cancel." Accuracy on the task plateaus near 92% with human review catching the rest. What is the architect's correct move?

- A. Promise 99.9% and hope model upgrades close the gap
- B. Reframe the target around the end-to-end process: the system plus confidence-routed human review achieves the business outcome, with measured rates, costs, and the tradeoff curve made explicit
- C. Decline to discuss numbers with non-engineers
- D. Quietly redefine accuracy so the number reads higher

<details><summary>Answer and rationale</summary>

**B.** Managing expectations with explicit, honest tradeoffs is scored material at this level: the deliverable is the business outcome of the whole pipeline, not a raw model metric. Overpromising (A), stonewalling (C), and metric games (D) each destroy the trust the role exists to build.

</details>

**10. Developer Productivity & Operational Enablement.** Three teams configure Claude Code independently: conventions drift, and new engineers take days to become productive. What is the enablement fix?

- A. Mandate that engineers memorize the conventions
- B. Ship a shared baseline: version-controlled team configuration, common skills and commands, and an onboarding path, with team-specific rules layered on top
- C. Prohibit Claude Code until conventions settle
- D. Let each engineer keep personal settings only

<details><summary>Answer and rationale</summary>

**B.** Team-level enablement means shared, versioned configuration with local extension, which is what makes tooling productive at organizational scale. Memorization (A) does not configure anything, prohibition (C) discards the productivity the domain exists to deliver, and personal-only settings (D) is the drift you started with.

</details>

---

These questions are the maintainer's original work for self-assessment. [Study guide](README.md) · [Study notes](notes.md) · [Mock exam](mock-exam.md) · [Repository index](../README.md)
