# Cheat sheet: Associate – Foundations

Everything worth holding in your head the hour before the exam, on one page. Facts come from the [official exam guide](exam-guide.pdf); the rules of thumb are the maintainer's, distilled from the official rationales.

[![Claude Certified Associate – Foundations cheat sheet: exam facts, domain weights, and the rules that decide questions](../.github/assets/cheat-sheet-associate-foundations.png)](../.github/assets/cheat-sheet-associate-foundations.png "View this cheat sheet at full size")

Save or share the card above; the full sheet follows.

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

## Working the clock

60 items in 120 minutes is two minutes each, and you will not need two minutes for most of them. My approach:

- **First pass, about 70 minutes.** Answer everything you know. If an item needs more than 90 seconds of thought, choose your best option, flag it, and move. An unanswered item scores zero; a flagged guess is a free option to change your mind.
- **Second pass, about 30 minutes.** Only the flagged ones. You will find that several are now obvious, because later items remind you of the framing.
- **Last 20 minutes.** Re-read the multiple-response items specifically. They are where careless marks are lost, because it is easy to select two when the item says three.

## Reading a question the way it is written

Every scenario names a constraint: cost, privacy, speed, policy, or scale. Find that constraint first, then eliminate every option that does not address it. Two options usually survive; the better one is the one that changes the system rather than compensating around it.

When two options both look right, ask which one a careful professional would defend in front of the person who owns the risk. That is nearly always the intended answer.

## The morning of

- Run the system test again on the exam machine, even if it passed last week
- Close everything on the shutdown list before check-in, not during it
- Have the ID ready, room clear, desk clear, second monitor unplugged
- Check-in takes longer than you expect; start the process early
- Eat something. 135 minutes of seat time is longer than it sounds

## If you blank

Skip it and keep moving. The blueprint is finite and the items are independent; one hard question costs one mark, and stalling on it costs five. Come back in the second pass and the answer is often obvious.

## Exam day logistics

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

Facts last verified against the official sources on 2026-09-01. [Study guide](README.md) · [Notes](notes.md) · [Practice questions](practice-questions.md) · [Mock exam](mock-exam-1.md) · [Repository index](../README.md)
