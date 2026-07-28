# Mock exam: Associate – Foundations

A timed practice exam in the official style. Unlike the [practice questions](practice-questions.md), the domains are hidden and the answers sit at the end, so this measures readiness rather than teaching. Original questions written against the public [blueprint](README.md#skills-measured); not items from the live exam, which is covered by a non-disclosure agreement.

**How to take it.** 15 questions, 30 minutes, closed book: no notes, no documentation, no Claude. Answer every question, since unanswered items score zero. Flag anything you are unsure of and return to it. Score yourself with the [key](#answer-key) and the [readiness table](#interpreting-your-score) afterwards.

---

## Questions

**1.** A colleague shares a Claude-drafted policy summary that reads well and cites three internal documents by name. What is the appropriate review step before it circulates to the whole department?

- A. Circulate it, since the named sources demonstrate grounding
- C. Confirm each named document exists and says what the summary claims
- B. Ask Claude to double-check its own work and circulate if it agrees
- D. Add a disclaimer that the summary was AI-generated and circulate

**2.** You need a first draft of a stakeholder update from a long project log. Which prompt is most likely to produce a usable draft on the first attempt?

- A. "Summarize this project log."
- D. "You are writing a weekly update for non-technical executives. From the log, produce: status in one line, three progress items, two risks with owners, and next week's focus. Keep it under 200 words."
- B. "Write something good about this project log for my boss."
- C. "Summarize this project log. Be detailed and thorough and professional."

**3.** A workflow drafts hundreds of routine appointment confirmations each day. Latency and cost dominate; the language is formulaic. Which choice fits?

- B. The most capable model, for consistency
- A. A fast, low-cost model, reserving a more capable one for exceptions
- C. Whichever model is newest
- D. Alternate between models to spread cost

**4.** Your team's Project answers questions from a product manual. Users report confident answers about a feature that was removed last quarter. What is the most likely cause?

- A. The model needs retraining
- B. The Project's knowledge still contains the outdated manual
- C. Users are asking the questions wrong
- D. The context window is too small

**5.** Legal asks you to analyze a spreadsheet of support tickets containing customer names and email addresses. Your organization prohibits sending personal data to external tools. What do you do?

- A. Upload it, since legal requested the analysis
- C. Strip or pseudonymize the personal columns, then analyze what remains
- B. Upload it and ask Claude to disregard the personal columns
- D. Tell legal the analysis is not possible

**6.** Claude produces a five-paragraph answer when you needed three bullet points, twice in a row. What is the most effective adjustment?

- A. Ask again and hope for variation
- D. State the format explicitly, including the number of bullets and their maximum length
- B. Switch to a more capable model
- C. Manually reformat each response

**7.** Which of these is the strongest signal that a Claude-generated claim needs verification before use?

- B. The answer is long
- A. The claim is a specific number, date, or citation that would matter if wrong
- C. The answer was produced quickly
- D. The answer uses technical vocabulary

**8.** A manager wants to know whether Claude can "replace our weekly reporting process." What is the most useful response?

- A. Yes, automation is what AI is for
- B. A breakdown of which reporting steps Claude can draft or summarize, which need human judgment or system access, and what the review step would be
- C. No, reporting requires human oversight
- D. A recommendation to hire a consultant

**9.** You are configuring a Project that several colleagues will use for consistent client communications. What belongs in the Project instructions rather than in each individual prompt?

- A. The specific client's name for today's message
- C. The house tone, required disclaimers, and the standard structure of a client message
- B. Today's date
- D. The colleague's personal writing preferences

**10.** A summary Claude produced omits a material caveat that appears in the source document. What does this failure mode illustrate?

- A. Hallucination through fabricated detail
- D. Omission, which requires reading the source rather than only reviewing the output
- B. A context window limit
- C. A prompt injection attack

**11.** Your prompt worked well last month and now returns weaker results after your team added twelve documents to the Project's knowledge. What is the first thing to investigate?

- B. Whether the model changed
- A. Whether the new documents are diluting or contradicting the sources the answers should use
- C. Whether colleagues are using different browsers
- D. Whether the prompt should be longer

**12.** For which task is a Project with persistent instructions and knowledge clearly better than a one-off chat?

- A. Asking for a synonym
- B. A monthly report that follows the same structure and draws on the same reference documents
- C. Checking a single fact
- D. Rewriting one email

**13.** Which practice best reduces the risk of sharing an inaccurate Claude output with a customer?

- A. Reading the output for tone before sending
- C. Verifying the claims that would cause harm if wrong, then having a second person review customer-facing material
- B. Sending it with a note that AI assisted
- D. Using the largest available model

**14.** You want Claude to help redesign a slow approval process rather than just speed up its current steps. Which prompt direction fits that goal?

- A. "Make our approval process faster."
- D. "Here are the current approval steps and where delays occur. Propose two redesigns: one that keeps the current structure and one that reorders or removes steps, with the tradeoffs of each."
- B. "Automate our approvals."
- C. "What do other companies do for approvals?"

**15.** Which situation most clearly calls for escalating to a technical colleague rather than solving it yourself?

- B. A prompt that needs better structure
- A. A request to connect Claude directly to the company's internal order database through an integration
- C. An output with the wrong tone
- D. A Project that needs its knowledge updated

---

## Answer key

| # | Answer | Domain | Why |
| --- | --- | --- | --- |
| 1 | C | Output Evaluation and Validation | Named sources can be fabricated; verification against the actual documents is the diligence step. Self-checking (B) is not independent evidence, and a disclaimer (D) does not make content correct |
| 2 | D | Prompting and Task Execution | Role, audience, explicit structure, and length constraints are what turn a vague request into a usable draft. Intensifiers like "detailed and thorough" (C) add no structure |
| 3 | A | Product and Model Selection | Match the model tier to the work: fast and cheap for formulaic volume, capable for exceptions |
| 4 | B | Configuration and Knowledge Management | Project knowledge is maintained by you; stale documents produce confidently outdated answers |
| 5 | C | Governance, Risk, and Responsible Use | Make the task compliant, then do it. A requester's seniority does not override policy, and instructing the model to ignore data does not un-send it |
| 6 | D | Prompting and Task Execution | Format failures are fixed by stating the format, not by re-rolling or upgrading the model |
| 7 | A | Output Evaluation and Validation | Specific, consequential details are the highest-risk surface for fabrication. Length, speed, and vocabulary carry no accuracy signal |
| 8 | B | Workflow Integration and Solution Design | The valued skill is a realistic division of labor with a review step, not a yes or a no |
| 9 | C | Configuration and Knowledge Management | Durable, shared conventions belong in instructions; per-message specifics belong in the prompt |
| 10 | D | Output Evaluation and Validation | Omission is as damaging as fabrication and is only visible if you read the source, not just the output |
| 11 | A | Troubleshooting and Optimization | Diagnose the change that coincided with the regression before rewriting anything |
| 12 | B | Workflow Integration and Solution Design | Repeated work with stable context and structure is exactly what Projects are for |
| 13 | C | Output Evaluation and Validation | Verification of consequential claims plus human review for customer-facing material. Model size is not a control |
| 14 | D | Workflow Integration and Solution Design | Process redesign requires giving Claude the current steps, the pain points, and asking for alternatives with tradeoffs |
| 15 | A | Governance, Risk, and Responsible Use | System integrations belong to the Developer and Architect scope; recognizing that boundary is an Associate competency |

## Interpreting your score

| Raw score | Reading |
| --- | --- |
| 13 to 15 | Comfortable. Review anything you missed and book the exam |
| 10 to 12 | Close. Work the domains where you lost points, then retake this and the [practice questions](practice-questions.md) |
| 7 to 9 | More study needed. Return to the [study guide](README.md), [notes](notes.md), and the prep courses before testing |
| 6 or fewer | Start from the blueprint and the official exam guide; you are not yet reading questions the way the exam intends |

This scale is a study aid, not a predictor. The real exam reports a scaled score from 100 to 1,000 with 720 to pass, and it draws from a much larger item pool.

Tally your misses by domain using the key above; two or more misses in one domain marks it as your next study target, exactly as the real score report's percent-correct breakdown would.

---

Written by the maintainer for self-assessment. [Study guide](README.md) · [Study notes](notes.md) · [Practice questions](practice-questions.md) · [Repository index](../README.md)
