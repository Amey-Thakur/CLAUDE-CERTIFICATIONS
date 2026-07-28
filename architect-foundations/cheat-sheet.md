# Cheat sheet: Architect – Foundations

Everything worth holding in your head the hour before the exam, on one page. Facts come from the [official exam guide](exam-guide.pdf); the rules of thumb are the maintainer's, distilled from the official rationales.

![Claude Certified Architect – Foundations cheat sheet: exam facts, domain weights, and the rules that decide questions](../.github/assets/cheat-sheet-architect-foundations.png)

Save or share the card above; the full sheet follows.

## The exam

| | |
| --- | --- |
| Code | CCAR-F |
| Items | 60, framed by 4 scenarios drawn from a published bank of 6 |
| Time | 120 minutes, about 2 minutes per item |
| Pass | 720 of 1,000, scaled |
| Fee | 125 USD before partner discount, raised from 99 on June 30, 2026 |
| Valid | 12 months, free renewal assessment |

## Where the marks are

```text
Agentic Architecture & Orchestration   27%  ██████████████████████████
Claude Code Configuration & Workflows  20%  ███████████████████
Prompt Engineering & Structured Output 20%  ███████████████████
Tool Design & MCP Integration          18%  █████████████████
Context Management & Reliability       15%  ██████████████
```

## The six scenarios, four of which you will see

| Scenario | Rehearse |
| --- | --- |
| Support resolution agent (MCP tools, 80% first-contact target) | Loop termination, escalation triggers, tool scoping, structured errors |
| Claude Code for a dev team | CLAUDE.md hierarchy, path-scoped rules, plan mode, commands and skills |
| Multi-agent research with cited reports | Coordinator and subagent handoffs, provenance, error propagation |
| Developer productivity tooling | Built-in tool selection, MCP integration, large-codebase context |
| Claude Code in CI/CD | Headless invocation, JSON output, review criteria, false positives |
| Structured data extraction | JSON schema design, validation retry, batch processing, confidence |

## If you remember nothing else

1. **Agent loops need engineered termination.** Iteration caps, repeated-call detection, and an escalation path. Token budget is not a stopping condition.
2. **Escalate on policy gaps and lack of progress.** Not on turn count, order age, or customer tone.
3. **Structured errors with a category and a retryable flag.** An agent can only recover from a failure it can interpret. Use the isError flag.
4. **Tool descriptions are the selection mechanism.** Differentiate similar tools precisely, or consolidate them.
5. **Enforce hard limits in the tool layer.** Policy caps belong in code or hooks, never in a request to the model.
6. **CLAUDE.md hierarchy: user, project, directory.** Conditional conventions go in `.claude/rules/` with path scoping so context is spent only where relevant.
7. **Plan mode is a review gate.** Use it when a human should approve the approach, not universally.
8. **CI means headless.** `-p` or `--print`, `--output-format json`, `--json-schema`. Never scrape a transcript.
9. **False positives are cured by explicit criteria.** State what to flag, what to ignore, the severity bar, and give examples.
10. **Subagents return distilled findings, not raw documents.** Bulk stays at the edge; that is the point of delegation.
11. **Provenance must survive handoffs.** Carry claim and source together or citations drift from claims.
12. **Errors propagate with context** so the coordinator can retry, exclude with a noted gap, or abort.
13. **Nullable for legitimate absence.** Required-everything forces fabrication; optional-everything hides real misses.
14. **Validate, then retry with the validation error.** Feed the model what was wrong.
15. **Measure on a labeled sample of everything.** Accuracy computed only on records that passed validation is a biased number.

## Appendix items worth knowing cold

`stop_reason` values, PostToolUse hooks, `allowedTools`, the Task tool for subagents, `.mcp.json` with environment expansion, `isError`, `.claude/skills/SKILL.md` frontmatter (`context: fork`, `allowed-tools`, `argument-hint`), `/memory`, `/compact`, `--resume`, `fork_session`, the Explore subagent, `tool_choice`, Message Batches (50% saving, 24-hour window, `custom_id`, no multi-turn tool calling), lost-in-the-middle effects, scratchpad files, confidence calibration.

## Working the clock

60 items across 4 scenarios in 120 minutes. The scenarios each carry a block of questions, so pace by block rather than by item.

- **Read each scenario once, carefully, before its questions.** Two minutes spent understanding the system saves more than it costs, because every question in the block leans on it.
- **First pass, about 70 minutes.** Work each block in order. Flag anything needing more than 90 seconds.
- **Second pass, about 30 minutes.** Return to the flags with the whole scenario now familiar.
- **Last 20 minutes.** Re-read multiple-response items and confirm selection counts.

## Reading a question the way it is written

Because you know the six scenarios in advance, you can walk in already knowing what each one is about to test. Use that: when the block opens, recall the primary domains listed for that scenario and expect the questions to sit there.

Within a question, find the constraint (reliability, cost, context limits, safety, maintainability) and eliminate everything that does not address it. The winning option almost always removes a structural weakness; the distractors add capacity, add supervision, or ask the model to be careful.

## The morning of

- Run the system test again on the exam machine, even if it passed last week
- Close everything on the shutdown list before check-in, including the Claude desktop app
- ID ready, room clear, desk clear, second monitor unplugged
- Check-in takes longer than you expect; start early
- 135 minutes of seat time; eat first

## If you blank

Move on within the block and come back. Scenario questions are mutually reinforcing: a later question in the same block often clarifies what an earlier one was asking.

## Exam day logistics

- ID name must match your registration exactly
- Closed book. No notes, no documentation, no translation tools
- Answer everything; unanswered scores zero
- Read the scenario once carefully, then answer its questions against that context
- If you attempted this exam before June 30, 2026 and did not pass, that attempt was cleared: no waiting period

---

[Study guide](README.md) · [Notes](notes.md) · [Practice questions](practice-questions.md) · [Mock exam](mock-exam.md) · [Repository index](../README.md)
