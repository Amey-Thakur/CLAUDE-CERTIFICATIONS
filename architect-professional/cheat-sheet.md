# Cheat sheet: Architect – Professional

Everything worth holding in your head the hour before the exam, on one page. Facts come from the [official exam guide](exam-guide.pdf); the rules of thumb are the maintainer's, distilled from the official rationales.

[![Claude Certified Architect – Professional cheat sheet: exam facts, domain weights, and the rules that decide questions](../.github/assets/cheat-sheet-architect-professional.png)](../.github/assets/cheat-sheet-architect-professional.png "View this cheat sheet at full size")

Save or share the card above; the full sheet follows.

## The exam

| | |
| --- | --- |
| Code | CCAR-P |
| Items | 63, multiple choice and multiple response |
| Time | 120 minutes, about 2 minutes per item |
| Pass | 720 of 1,000, scaled |
| Fee | 175 USD before partner discount |
| Valid | 12 months, free renewal assessment |
| Prerequisite | None. Foundations is not required and does not upgrade into this |

## Where the marks are

```text
Integration                                19%  ██████████████████
Solution Design & Architecture             17%  ████████████████
Evaluation, Testing & Optimization         16%  ███████████████
Governance, Safety & Risk Management       14%  █████████████
Stakeholder Communication & Lifecycle      14%  █████████████
Claude Models, Prompting & Context         13%  ████████████
Developer Productivity & Enablement         7%  ███████
```

Governance and stakeholder communication are 28% combined. Technical candidates lose marks there, not in integration.

## If you remember nothing else

1. **Climb the ladder only when forced.** Plain call, then augmented with retrieval and tools, then workflow, then agent, then multi-agent. Justify every rung.
2. **Least privilege means removal.** Take the capability away. Logging, confirmation prompts, and business-hours limits are compensating controls, not fixes.
3. **RAG degradation after a data change is a retrieval defect.** Look at chunking, embeddings, and index consistency before prompts or models.
4. **Frequently changing knowledge belongs in retrieval,** never in weights and never pasted into a system prompt.
5. **At high tool counts, scope per role and discover progressively.** Do not shorten descriptions and do not build a mega-tool.
6. **Subjective quality is measured with rubrics.** Define failure modes, build a labeled set, use model graders audited by humans. Exact match and length measure nothing.
7. **Prompt changes are production changes.** Regression suite, then A/B on predefined metrics, then rollout.
8. **Compliance is enforced before the boundary.** De-identify or tokenize ahead of the call, re-associate locally, audit the boundary. Instructions to the model act too late.
9. **Route human review by confidence and consequence.** Reviewing everything does not scale; reviewing nothing is negligent; random sampling misses the risky cases.
10. **Observability captures traces, not just outputs.** Tool calls, retrieved context, and decision points, or incidents cannot be localized.
11. **Order static content first and cache it.** The one optimization that improves latency and cost together.
12. **Present segmented, honest numbers.** Break performance out by case type, state the method, and give the end-to-end outcome including human review. Never a single flattering average.
13. **Decision records carry alternatives and tradeoffs,** not just the chosen design.
14. **Enablement is versioned and shared.** Team configuration, common skills and commands, and an onboarding path.

## Regulations in one line each

| | |
| --- | --- |
| GDPR | Personal data of EU persons: minimization, purpose limitation, erasure on request |
| HIPAA | US protected health information: de-identify before it leaves the boundary |
| FedRAMP | US federal cloud deployments: authorized environments and controls |

## Working the clock

63 items in 120 minutes, just under two minutes each, and the scenarios are longer than on the Foundations exams.

- **First pass, about 75 minutes.** Answer what you know and flag the rest. Design questions with several defensible options are the ones to flag; they reward a second look more than any other type.
- **Second pass, about 30 minutes.** Work the flags. By then you will have absorbed what this exam considers good architecture, and the previously ambiguous items usually resolve.
- **Last 15 minutes.** Re-read multiple-response items and confirm selection counts.

## Reading a question the way it is written

At this level, most options are defensible and only one is best. Two questions resolve nearly every item:

1. **What constraint does the scenario actually state?** Cost, latency, compliance, scale, auditability, or stakeholder trust. The best option addresses that one, not the others.
2. **Which option would survive a design review?** The exam consistently prefers the choice that removes a risk over the choice that monitors it, and the choice that is measurable over the choice that is merely reasonable.

Expect governance and stakeholder items to feel softer than the technical ones. They are not easier and they are 28% of the paper: answer them with the same rigour, choosing the option that is honest, segmented, and defensible rather than the one that sounds reassuring.

## The morning of

- Run the system test again on the exam machine, even if it passed last week
- Close everything on the shutdown list before check-in, including the Claude desktop app
- ID ready, room clear, desk clear, second monitor unplugged
- Check-in takes longer than you expect; start early
- 135 minutes of seat time; eat first

## If you blank

Skip and return. Long scenarios reward a second reading with fresh eyes far more than they reward staring.

## Exam day logistics

- ID name must match your registration exactly
- Closed book. No notes, no documentation, no translation tools
- Answer everything; unanswered scores zero
- Expect scenario questions where several options are defensible: pick the one that satisfies the stated constraint
- Roughly 2 minutes per item; flag and return rather than stalling

## Traps

- More agents, more tools, and bigger models are rarely the answer to a design question
- A refusal to quantify is as wrong as an inflated number; segmentation is the professional answer
- Fine-tuning is the expensive answer to problems retrieval and templates already solve
- Monitoring a dangerous capability is not the same as removing it

---

Facts last verified against the official sources on 2026-08-29. [Study guide](README.md) · [Notes](notes.md) · [Practice questions](practice-questions.md) · [Mock exam](mock-exam-1.md) · [Repository index](../README.md)
