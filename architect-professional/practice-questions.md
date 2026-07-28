# Practice questions: Architect – Professional

Thirty-five original practice questions written for this repository against the public [exam blueprint](README.md#skills-measured), in the official item style. They are unofficial practice aids, not items from the live exam, which is covered by a non-disclosure agreement. Coverage follows the domain weights. For unlimited practice, use [Practice with Claude](../guide/practice.md).

**1. Integration.** An internal agent for account managers can read CRM records, draft emails, update opportunities, and delete contacts. Account managers only ever read records and draft emails through it. Under least privilege, what is the right change?

- A. Log every update and deletion for later audit
- D. Remove the update and delete capabilities from the agent's configuration entirely
- B. Add a confirmation dialog before updates and deletions
- C. Restrict deletions to business hours

<details><summary>Answer and rationale</summary>

**D.** Least privilege removes capabilities the role does not need, eliminating the attack and error surface rather than monitoring it. Logging (A) and confirmations (B) are compensating controls around a privilege that should not exist, and scheduling (C) narrows the window without closing it.

</details>

**2. Integration.** After a nightly document refresh, your RAG assistant's answers turned confident but wrong. Model version, prompts, and latency are unchanged. Where do you look first?

- B. The model, which may have degraded overnight
- A. The retrieval and indexing layer: whether the refresh broke the index, changed chunking, or introduced mismatched embeddings
- C. The system prompt wording
- D. The temperature setting

<details><summary>Answer and rationale</summary>

**A.** The only thing that changed is the document pipeline, and confident-but-wrong is the signature of plausible-but-irrelevant retrieved context. The pinned model (B), unchanged prompt (C), and sampling (D) do not correlate with the refresh.

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
- C. Two simple components: a retrieval-augmented answer service for policy questions, and a templated generation workflow for letters, each evaluated on its own metrics
- B. One agent with all tools and a routing prompt
- D. A single fine-tuned model for both

<details><summary>Answer and rationale</summary>

**C.** Two well-understood problems with different shapes deserve the two cheapest reliable structures, independently testable and governable. Shared document-ness (A) is not an architectural argument, one agent with everything (B) couples unrelated risk profiles, and fine-tuning (D) is the most expensive path to problems retrieval and templates already solve.

</details>

**5. Solution Design.** Your architecture review board asks why you chose a deterministic workflow over an autonomous agent for claims intake. Which justification reflects the tested decision framework?

- A. Agents are a newer pattern and less proven in general
- D. The intake path is fully known in advance, so deterministic orchestration is cheaper, auditable, and reliable; autonomy earns its complexity only where the model must choose the path
- B. Workflows always outperform agents
- C. The team lacked time to build an agent

<details><summary>Answer and rationale</summary>

**D.** The framework is structural fit: known path, deterministic orchestration; open-ended path, agent. Novelty (A) and universal claims (B) are not engineering arguments, and resourcing (C) justifies a schedule, not an architecture.

</details>

**6. Evaluation, Testing & Optimization.** Legal review quality is subjective, and your team disagrees about whether the assistant's clause summaries are "good." What makes evaluation tractable?

- B. Ship and count complaints
- A. Define a rubric with the failure modes that matter, build a labeled evaluation set with counsel, and combine rubric-based model grading with periodic human review
- C. Exact string match against one reference summary per clause
- D. Grade outputs by length

<details><summary>Answer and rationale</summary>

**A.** Subjective quality becomes measurable through rubrics, labeled sets, and mixed methodology with humans anchoring the judgment. Complaint-counting (B) measures too late, exact match (C) fails every valid paraphrase, and length (D) measures nothing.

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
- C. A de-identification layer that strips or tokenizes PHI before the API call, re-associating results locally, with logging and periodic audits of the boundary
- B. A system prompt instructing the model to forget PHI
- D. Blocking free-text queries entirely

<details><summary>Answer and rationale</summary>

**C.** Compliance boundaries are enforced by architecture: PHI is removed before it crosses, and the control is auditable. Trust (A) is not a control, model instructions (B) act after the data already crossed, and a hard block (D) fails the stated business need that a compliant design can meet.

</details>

**9. Stakeholder Communication & Lifecycle Management.** Your Claude solution's executive sponsor asks for "99.9% accuracy or we cancel." Accuracy on the task plateaus near 92% with human review catching the rest. What is the architect's correct move?

- A. Promise 99.9% and hope model upgrades close the gap
- D. Reframe the target around the end-to-end process: the system plus confidence-routed human review achieves the business outcome, with measured rates, costs, and the tradeoff curve made explicit
- B. Decline to discuss numbers with non-engineers
- C. Quietly redefine accuracy so the number reads higher

<details><summary>Answer and rationale</summary>

**D.** Managing expectations with explicit, honest tradeoffs is scored material at this level: the deliverable is the business outcome of the whole pipeline, not a raw model metric. Overpromising (A), stonewalling (B), and metric games (C) each destroy the trust the role exists to build.

</details>

**10. Developer Productivity & Operational Enablement.** Three teams configure Claude Code independently: conventions drift, and new engineers take days to become productive. What is the enablement fix?

- B. Mandate that engineers memorize the conventions
- A. Ship a shared baseline: version-controlled team configuration, common skills and commands, and an onboarding path, with team-specific rules layered on top
- C. Prohibit Claude Code until conventions settle
- D. Let each engineer keep personal settings only

<details><summary>Answer and rationale</summary>

**A.** Team-level enablement means shared, versioned configuration with local extension, which is what makes tooling productive at organizational scale. Memorization (B) does not configure anything, prohibition (C) discards the productivity the domain exists to deliver, and personal-only settings (D) is the drift you started with.

</details>

**11. Integration.** A customer requires that no request data leave their AWS account. Which deployment satisfies the constraint?

- A. The Claude API with a signed data processing agreement
- B. Claude through Amazon Bedrock within the customer's own account and region
- C. The Claude API with request logging disabled
- D. Any deployment, provided the data is encrypted in transit

<details><summary>Answer and rationale</summary>

**B.** A residency constraint of this kind is met by running within the customer's own cloud boundary, which is what Bedrock provides. A contractual agreement (A), disabled logging (C), and transport encryption (D) all still involve the data leaving the account.

</details>

**12. Integration.** An enterprise standardised on Google Cloud and requires identity, billing, and audit to run through existing controls. What follows?

- A. Deploy on Bedrock for feature parity
- C. Deploy through Vertex AI so the platform's identity, billing, and audit apply
- B. Use the Claude API and replicate the controls
- D. Let each team choose its own path

<details><summary>Answer and rationale</summary>

**C.** Aligning with the platform the enterprise already governs is what makes existing controls apply without duplication. A different cloud (A) creates a second control plane, replication (B) is expensive and drifts, and per-team choice (D) removes governance.

</details>

**13. Integration.** A design places Claude behind an internal service that every application calls. What is the principal benefit?

- A. It reduces token cost
- D. Authentication, rate limiting, logging, and model routing are enforced in one place
- B. It removes the need for evaluation
- C. It guarantees lower latency

<details><summary>Answer and rationale</summary>

**D.** A single integration point is where cross-cutting concerns can be applied consistently and changed once. It does not reduce token cost (A) or remove the need to evaluate (B), and an extra hop generally adds latency (C).

</details>

**14. Integration.** A legacy system can only call synchronous endpoints with a two-second timeout, but the task needs long reasoning. What is the appropriate design?

- B. Force the model to answer within two seconds
- A. Accept the request, return an identifier immediately, and deliver the result asynchronously
- C. Increase the legacy timeout
- D. Use the smallest model available

<details><summary>Answer and rationale</summary>

**A.** Decoupling submission from delivery lets the constraint and the workload coexist without degrading either. Truncating the reasoning (B, D) sacrifices the task, and changing the legacy system (C) is usually the constraint rather than an option.

</details>

**15. Integration.** What is the most important consideration when a solution must run across two clouds?

- A. Using identical prompts in both
- B. Establishing which behaviours must be identical and evaluating for those on each platform
- C. Choosing the cheaper platform for both
- D. Deploying to whichever region is nearest

<details><summary>Answer and rationale</summary>

**B.** Cross-platform equivalence is a requirement to be defined and then verified, not assumed. Identical prompts (A) do not guarantee identical behaviour, and cost (C) and proximity (D) do not address consistency.

</details>

**16. Solution Design.** A stakeholder asks for an autonomous agent to handle an end-to-end financial approval process. What should the architect establish first?

- A. Which model to use
- C. Which decisions carry accountability and must remain with a person
- B. The expected token cost
- D. Whether the agent can be built in the available time

<details><summary>Answer and rationale</summary>

**C.** Where accountability sits determines the shape of the solution and what may be automated at all. Model choice (A), cost (B), and schedule (D) are all downstream of that boundary.

</details>

**17. Solution Design.** Two designs meet the functional requirement. One is simpler and slightly less capable. What should decide?

- A. The more capable design, since capability is the point
- D. Whether the extra capability is needed by a stated requirement, weighed against the cost of complexity
- B. The design the team finds more interesting
- C. The design with more components, for future flexibility

<details><summary>Answer and rationale</summary>

**D.** Complexity is a cost paid continuously in operation and maintenance, so it must be bought by a real requirement. Capability for its own sake (A), preference (B), and speculative flexibility (C) all pay that cost without justification.

</details>

**18. Solution Design.** A proposed architecture depends on the model behaving correctly for a control that regulation requires. What is the correct judgment?

- B. Acceptable if evaluation shows high accuracy
- A. Unacceptable: a required control must be enforced deterministically outside the model
- C. Acceptable with a disclaimer to the regulator
- D. Acceptable if a larger model is used

<details><summary>Answer and rationale</summary>

**A.** A regulatory control needs a guarantee, and probabilistic behaviour cannot supply one however high the measured accuracy. Accuracy (B), disclosure (C), and model size (D) do not convert a tendency into a guarantee.

</details>

**19. Solution Design.** What is the clearest sign that a solution has been over-engineered?

- A. It uses more than one model
- B. Components exist that no stated requirement depends on
- C. It has an evaluation suite
- D. It includes a human approval step

<details><summary>Answer and rationale</summary>

**B.** Unjustified components are the definition of over-engineering and are the parts that will rot. Multiple models (A), evaluation (C), and approval steps (D) are all defensible when a requirement calls for them.

</details>

**20. Evaluation, Testing & Optimization.** What must exist before a solution can be said to be ready for production?

- A. A demonstration that impressed stakeholders
- C. A defined success criterion and measured performance against representative data
- B. Agreement from the engineering team
- D. A completed cost estimate

<details><summary>Answer and rationale</summary>

**C.** Readiness is a measured claim against a stated bar, which is what distinguishes it from an impression. Demonstrations (A), consensus (B), and cost (D) do not establish whether the system works.

</details>

**21. Evaluation, Testing & Optimization.** An evaluation set is drawn entirely from cases the system already handles well. What is the consequence?

- A. It gives a reliable measure of quality
- D. It overstates performance and hides the failure modes that matter
- B. It is acceptable if it is large enough
- C. It only matters for regulated systems

<details><summary>Answer and rationale</summary>

**D.** An unrepresentative set measures the wrong distribution, and size cannot correct a biased sample. It is not reliable (A), scale does not fix bias (B), and the problem is universal rather than sector-specific (C).

</details>

**22. Evaluation, Testing & Optimization.** A prompt change improves the target metric but degrades an unmeasured behaviour. How is this best prevented?

- B. Changing one thing at a time
- A. Maintaining a regression suite that covers behaviours the system must not lose
- C. Reviewing changes more carefully
- D. Limiting how often prompts change

<details><summary>Answer and rationale</summary>

**A.** Silent regressions are caught by explicitly testing what must not break. Single changes (B) and careful review (C) reduce risk without detecting it, and slowing change (D) does not make it safe.

</details>

**23. Evaluation, Testing & Optimization.** What should trigger re-evaluation of a deployed solution?

- A. Only a reported incident
- B. A change to the model, the prompt, the data distribution, or the requirement
- C. A fixed annual schedule
- D. A change in cost

<details><summary>Answer and rationale</summary>

**B.** Any change to the things that determine behaviour invalidates prior measurement. Waiting for incidents (A) detects late, a fixed schedule (C) is unrelated to actual change, and cost (D) does not affect correctness.

</details>

**24. Governance, Safety & Risk Management.** How should an architect treat a request to log full prompts and responses for audit?

- A. Implement it, since audit requirements take precedence
- C. Establish what the audit actually requires, since prompts and responses may contain personal or confidential data
- B. Refuse, since logging creates risk
- D. Log responses only

<details><summary>Answer and rationale</summary>

**C.** Audit and data protection are both real constraints, and the design must satisfy the audit purpose without retaining more than is warranted. Blanket implementation (A) and blanket refusal (B) ignore one side, and a partial rule (D) is arbitrary without knowing the requirement.

</details>

**25. Governance, Safety & Risk Management.** What is the correct treatment of content retrieved from an untrusted source before it reaches the model?

- A. It is safe once scanned for known attack strings
- D. It is untrusted data throughout, and the model's authority must be bounded regardless of its content
- B. It is safe if the model is instructed to disregard instructions within it
- C. It is safe if it comes over an encrypted channel

<details><summary>Answer and rationale</summary>

**D.** The durable control is that the model cannot exceed its permissions whatever the content persuades it to attempt. String scanning (A) and prompt instructions (B) are bypassable, and transport security (C) says nothing about the content.

</details>

**26. Governance, Safety & Risk Management.** Who is accountable for a wrong decision produced by an automated Claude workflow?

- B. The model provider
- A. The organisation that deployed the workflow
- C. The engineer who wrote the prompt
- D. Nobody, since the output was automated

<details><summary>Answer and rationale</summary>

**A.** Deploying an automated decision means owning its outcomes, which is why the boundaries of automation are an architectural decision. The provider (B) supplies a capability, individual authorship (C) does not transfer organisational responsibility, and automation does not remove accountability (D).

</details>

**27. Stakeholder Communication & Lifecycle Management.** An executive sponsor asks for a single number showing how good the solution is. What is the right response?

- A. Provide the headline accuracy figure
- B. Provide the measure that matches the decision they face, with its limits stated
- C. Explain that quality cannot be summarised
- D. Provide the model's benchmark score

<details><summary>Answer and rationale</summary>

**B.** A useful metric is one tied to the decision at hand and honest about what it does not cover. A bare accuracy figure (A) and a benchmark score (D) can mislead, and refusing to summarise (C) fails the sponsor.

</details>

**28. Stakeholder Communication & Lifecycle Management.** A pilot succeeded with ten users and the business wants to roll out to two thousand. What should the architect raise first?

- A. The cost of additional licences
- C. Which assumptions held at ten users and may not hold at two thousand
- B. The need for a larger model
- D. The training schedule

<details><summary>Answer and rationale</summary>

**C.** Scale invalidates assumptions about inputs, support, and edge cases, and naming those is the architect's contribution. Licences (A), model size (B), and training (D) are downstream of knowing what breaks.

</details>

**29. Stakeholder Communication & Lifecycle Management.** What most reduces the risk that a delivered solution decays after handover?

- A. Full documentation at delivery
- D. A named owner with a defined routine for evaluation, monitoring, and update
- B. A longer warranty period
- C. Training every user

<details><summary>Answer and rationale</summary>

**D.** Decay is prevented by ongoing ownership and a routine, not by artefacts produced once. Documentation (A) and training (C) age, and a warranty (B) covers defects rather than drift.

</details>

**30. Claude Models, Prompting & Context Engineering.** How should an architect choose a model for a solution with several different tasks?

- B. One model for everything, for simplicity
- A. Match each task to the smallest model that meets its requirement, and evaluate the choices
- C. The largest model for everything, for safety
- D. The newest model for everything

<details><summary>Answer and rationale</summary>

**A.** Different tasks have different requirements, and matching each keeps cost proportionate while evidence supports the choice. Uniform choices (B, C, D) optimise for convenience rather than fit.

</details>

**31. Claude Models, Prompting & Context Engineering.** What is the correct treatment of the context window in a production design?

- A. A capacity to fill as fully as possible
- B. A budget to allocate deliberately between instructions, retrieved material, and working state
- C. A limit that only matters for long documents
- D. A setting to raise when quality drops

<details><summary>Answer and rationale</summary>

**B.** Context is a scarce resource whose allocation determines quality, so it is designed rather than consumed. Filling it (A) invites dilution, it matters well beyond long documents (C), and enlarging it (D) does not fix an allocation problem.

</details>

**32. Claude Models, Prompting & Context Engineering.** A solution's prompts are maintained by three teams and have diverged. What is the appropriate remedy?

- A. Appoint one team to own all prompting
- C. Version the prompts as artefacts with defined ownership, review, and evaluation on change
- B. Freeze the prompts
- D. Move all prompts into the system prompt

<details><summary>Answer and rationale</summary>

**C.** Prompts that determine production behaviour deserve the same lifecycle as code. Centralising ownership (A) may not fit the organisation, freezing (B) blocks improvement, and relocation (D) does not address governance.

</details>

**33. Developer Productivity & Operational Enablement.** An organisation wants consistent Claude Code practice across many repositories. What is the most durable approach?

- A. A written policy circulated by email
- D. Committed project memory and shared skills in each repository, reviewed like code
- B. A one-off training session
- C. Requiring approval for each use

<details><summary>Answer and rationale</summary>

**D.** Conventions travel when they live in the repository and are reviewed with the work. Policies (A) and training (B) fade, and per-use approval (C) creates friction without conveying practice.

</details>

**34. Developer Productivity & Operational Enablement.** What is the most useful measure of whether a developer enablement programme is working?

- B. The number of people trained
- A. Change in the outcomes the tooling was adopted to improve
- C. Licence utilisation
- D. The volume of tool calls

<details><summary>Answer and rationale</summary>

**A.** Enablement is justified by the outcome it moves, which is what should be measured. Attendance (B), utilisation (C), and activity (D) measure uptake rather than benefit.

</details>

**35. Developer Productivity & Operational Enablement.** A team reports that Claude Code helps with new code but hurts on a legacy service. What should the architect investigate?

- A. Whether the team needs more training
- B. Whether the legacy service lacks the committed context and conventions the model needs
- C. Whether a larger model would help
- D. Whether the legacy service should be rewritten

<details><summary>Answer and rationale</summary>

**B.** A difference between codebases usually reflects a difference in the context available in each. Training (A) does not supply repository context, a larger model (C) cannot infer undocumented conventions, and a rewrite (D) is a disproportionate response to a diagnosis not yet made.

</details>

---

These questions are the maintainer's original work for self-assessment. [Study guide](README.md) · [Study notes](notes.md) · [Mock exam](mock-exam.md) · [Repository index](../README.md)
