# Cheat sheet: Developer – Foundations

Everything worth holding in your head the hour before the exam, on one page. Facts come from the [official exam guide](exam-guide.pdf); the rules of thumb are the maintainer's, distilled from the official rationales.

[![Claude Certified Developer – Foundations cheat sheet: exam facts, domain weights, and the rules that decide questions](../.github/assets/cheat-sheet-developer-foundations.png)](../.github/assets/cheat-sheet-developer-foundations.png "View this cheat sheet at full size")

Save or share the card above; the full sheet follows.

## The exam

| | |
| --- | --- |
| Code | CCDV-F |
| Items | 53, multiple choice and multiple response |
| Time | 120 minutes, about 2 minutes per item |
| Pass | 720 of 1,000, scaled |
| Fee | 125 USD before partner discount |
| Valid | 12 months, free renewal assessment |

## Where the marks are

```text
Applications and Integration        33.1%  ████████████████████████████████
Model Selection and Optimization    16.8%  ████████████████
Agents and Workflows                14.7%  ██████████████
Prompt and Context Engineering      11.0%  ███████████
Tools and MCPs                      10.6%  ██████████
Security and Safety                  8.1%  ████████
Claude Code                          3.1%  ███
Eval, Testing, and Debugging         2.6%  ██
```

One domain is a third of the paper. Claude Code and Eval together are under 6%, so do not over-prepare them because they feel familiar.

## If you remember nothing else

1. **stop_reason drives the loop.** `tool_use` means execute the tool, append the result, call again. `end_turn` means done.
2. **Batches for latency-tolerant volume.** 50% of the cost, 24-hour window, `custom_id` correlation, no multi-turn tool calling inside a batch.
3. **Cache the stable prefix.** Static system prompt and policy first, variable content last, caching on. Cuts latency and cost together.
4. **Enforce structure, then validate, then retry with the error.** Tool use plus JSON schema. Never trust the model to emit valid JSON because you asked firmly.
5. **Known path, workflow. Unknown path, agent.** Autonomy earns its complexity only when the model must choose the route.
6. **Subagents isolate context.** Delegation keeps verbose intermediate work out of the parent window.
7. **Pin model versions in production.** Upgrades then become evaluated changes rather than overnight surprises.
8. **Injection is defeated structurally.** Separate untrusted content from instructions and deny it access to consequential tools. Not by asking the model to ignore it, not by a bigger model.
9. **Least privilege on tools.** A capability the agent does not hold cannot be misused. Removal beats confirmation dialogs and logging.
10. **MCP server for reuse across applications.** Custom tool for one app, Skill for instructions, built-ins for file and shell basics.
11. **Tool descriptions are the selection mechanism.** Overlapping, vague descriptions cause wrong tool choices. Differentiate or consolidate.
12. **Context hygiene beats a bigger window.** Prune tool output, compact history, isolate subtasks. A larger window delays the same failure at higher cost.
13. **Few-shot fixes format and edge cases.** More instructions do not.
14. **Traces localize the fault.** Correct reasoning over wrong documents is a retrieval defect, not a model defect.

## Decisions the exam keeps testing

| Requirement | Answer |
| --- | --- |
| Cheap bulk work, results tomorrow | Message Batches API |
| Same long preamble every call | Reorder for a stable prefix, enable caching |
| Output must be machine-parseable | Tool use with JSON schema plus validation retry |
| Capability shared by several apps | MCP server |
| Agent must never do X | Do not give it the tool |
| Fixed five-step process | Workflow, model used inside it |
| Long session degrading | Prune, compact, delegate |

## Working the clock

53 items in 120 minutes is a comfortable pace, slightly over two minutes each. My approach:

- **First pass, about 65 minutes.** Answer what you know. Code-shaped questions read slowly; do not let one long snippet eat five minutes. Flag and move.
- **Second pass, about 35 minutes.** Work the flags. API mechanics questions in particular tend to resolve once you have seen several: the exam is internally consistent about what it considers good practice.
- **Last 20 minutes.** Re-read every multiple-response item and confirm the number of selections.

## Reading a question the way it is written

Each scenario states a constraint: cost, latency, reliability, security, or maintainability. Identify it in the first sentence, then eliminate. The pattern across almost every item is the same: the correct option changes the structure of the system, and the distractors adjust a parameter, add a bigger model, or ask the model nicely.

Specifically, be suspicious of any option containing "increase max_tokens", "raise temperature", "use a larger model", or "add an instruction to the prompt" when the problem is correctness, cost, format, or security. Those are the exam's standard wrong answers.

## The morning of

- Run the system test again on the exam machine, even if it passed last week
- Close everything on the shutdown list before check-in, including the Claude desktop app
- ID ready, room clear, desk clear, second monitor unplugged
- Check-in takes longer than you expect; start early
- 135 minutes of seat time; eat first

## If you blank

Skip and keep moving. One hard item costs one mark; stalling costs several. On this exam in particular, later items often jog the concept you needed for an earlier one.

## Exam day logistics

- ID name must match your registration exactly
- Closed book. No notes, no documentation, no translation tools
- Answer everything; unanswered scores zero
- Multiple response items say how many to pick
- Roughly 2 minutes per item; flag and return rather than stalling

## Traps

- The most capable model is rarely the right answer to a cost or latency question
- Temperature is almost never the fix for a correctness, format, or security problem
- Try or catch that silently swallows failures is never the sturdy pattern
- Prompt wording is not a security control, and confirmation dialogs are not least privilege

---

Facts last verified against the official sources on 2026-08-31. [Study guide](README.md) · [Notes](notes.md) · [Practice questions](practice-questions.md) · [Mock exam](mock-exam-1.md) · [Repository index](../README.md)
