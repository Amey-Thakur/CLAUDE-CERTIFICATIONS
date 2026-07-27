# Cheat sheet: Associate – Foundations

Everything worth holding in your head the hour before the exam, on one page. Facts come from the [official exam guide](exam-guide.pdf); the rules of thumb are the maintainer's, distilled from the official rationales.

## The exam

| | |
| --- | --- |
| Code | CCAO-F |
| Items | 60, multiple choice and multiple response |
| Time | 120 minutes, about 2 minutes per item |
| Pass | 720 of 1,000, scaled |
| Fee | 99 USD before partner discount |
| Valid | 12 months, free renewal assessment |

## Where the marks are

```text
Output Evaluation and Validation      21%  ████████████████████
Workflow Integration and Design       16%  ███████████████
Governance, Risk, Responsible Use     15%  ██████████████
Prompting and Task Execution          14%  █████████████
Product and Model Selection           12%  ███████████
Configuration and Knowledge Mgmt      12%  ███████████
Troubleshooting and Optimization      10%  █████████
```

Evaluating output is worth half again as much as writing prompts. Study accordingly.

## If you remember nothing else

1. **Verify anything specific and consequential.** Citations, numbers, dates, and section references are where models fabricate. Confidence is not evidence.
2. **Self-reported confidence proves nothing.** Asking the model how sure it is never validates a claim.
3. **Omission counts as failure.** A summary that drops a material caveat is wrong even though every word in it is true. Read the source, not just the output.
4. **Anonymize, then analyze.** Strip regulated identifiers before upload. Purpose, seniority of the requester, and "tell it to ignore that column" are not controls.
5. **Match the model to the task.** Fast and cheap for routine volume, capable for genuine reasoning. Defaulting to the largest model is a wrong answer; so is using the smallest for hard work.
6. **Structure beats intensifiers.** Role, audience, sections, constraints, and an example fix bad output. "Be detailed and thorough" does not.
7. **Decompose compound requests.** Ask for the categorized list, then the top three, then the actions. One vague mega-prompt yields vague output.
8. **Projects hold what repeats.** Durable instructions and knowledge live in the Project; per-message specifics live in the prompt.
9. **Project knowledge is maintained by you.** Stale uploaded documents produce confidently outdated answers. Replace, do not accumulate.
10. **Diagnose the change.** When quality drops, ask what changed (new knowledge, new sources, new prompt) before rewriting anything.
11. **Escalate integrations.** Connecting Claude to internal systems is Developer and Architect territory. Knowing that boundary is tested.
12. **Answer the business question.** "Can Claude do X?" is answered with a division of labor: what it drafts, what humans judge, and where the review step sits.

## Judgment patterns the exam rewards

| Situation | Right instinct |
| --- | --- |
| Output bound for a customer, executive, or regulator | Verify claims, then human review |
| High volume, low complexity | Cheaper, faster model |
| Sensitive data in the input | Remove or pseudonymize first |
| Same task every month | Project with instructions and knowledge |
| Output format keeps missing | State the format explicitly, with an example |
| Something worked and now does not | Find the change before changing anything |

## Exam day

- ID name must match your registration exactly
- Closed book. No notes, no documentation, no translation tools, no second monitor
- Answer everything; unanswered scores zero. Flag and return rather than stalling
- Multiple response items say how many to pick. Read that line first
- Two minutes per item is the budget

## Traps

- The longest option is not the safest one; the exam rewards the option that meets the stated constraint
- "Do nothing" and "abandon the task" are almost always wrong when a compliant path exists
- Adding a disclaimer does not make inaccurate content acceptable
- A larger model is not a fix for a governance, format, or process problem

---

[Study guide](README.md) · [Notes](notes.md) · [Practice questions](practice-questions.md) · [Mock exam](mock-exam.md) · [Repository index](../README.md)
