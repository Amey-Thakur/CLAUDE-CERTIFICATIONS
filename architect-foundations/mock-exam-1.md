# Mock exam 1: Architect – Foundations

A timed practice exam in the official style: scenario-framed, domains hidden, answers at the end. Unlike the [practice questions](practice-questions.md), this measures readiness rather than teaching. Original questions written against the public [blueprint](README.md#skills-measured) and the [six published scenarios](README.md#the-six-exam-scenarios); not items from the live exam, which is covered by a non-disclosure agreement.

**How to take it.** 15 questions, 30 minutes, closed book: no notes, no documentation, no Claude. The real exam presents 4 scenarios drawn from the published 6; this mock samples across all of them. Score yourself with the [key](#answer-key) and the [readiness table](#interpreting-your-score) afterwards.

---

## Scenario A: customer support resolution agent

An Agent SDK agent handles returns, billing disputes, and account issues through MCP tools: get_customer, lookup_order, process_refund, escalate_to_human.

**1.** The agent occasionally answers billing questions using an order it looked up three turns earlier for a different customer. What is the architectural fix?

- A. Increase the context window
- B. Scope each conversation's context to one customer and clear or isolate prior lookups when the subject changes
- C. Remove the lookup_order tool
- D. Instruct the model to be careful about customer identity

**2.** process_refund fails intermittently because the billing backend times out. What should the tool return so the agent can behave sensibly?

- A. An empty string
- B. A message asking the user to try later
- C. A structured error with a category and a retryable flag, so the agent can retry or escalate deliberately
- D. The exception stack trace

**3.** Which condition should route a ticket to escalate_to_human rather than continue autonomous resolution?

- A. The customer writes in a language the agent supports
- B. The order is more than thirty days old
- C. The conversation exceeds five turns
- D. The request falls outside documented policy, or the agent cannot make progress after a bounded number of attempts

**4.** The agent sometimes calls get_customer when it should call lookup_order. What is the most effective change?

- A. Rewrite both tool descriptions so each states precisely when it applies and how it differs from the other
- B. Reorder the tools in the configuration
- C. Merge them into one tool with a mode flag
- D. Increase the model's temperature

## Scenario B: Claude Code for a development team

A team uses Claude Code across a monorepo for generation, refactoring, and review.

**5.** Backend conventions should apply only when backend files are touched. Where do they belong?

- A. In the root CLAUDE.md so they are always available
- B. In a path-scoped rule under .claude/rules/ with frontmatter matching backend paths
- C. In each engineer's user-level configuration
- D. In the repository wiki

**6.** When is plan mode the appropriate choice over direct execution?

- A. For every change, since planning is always safer
- B. Only when the model is unfamiliar with the language
- C. When the change is large or risky enough that a human should review the approach before edits are made
- D. When the context window is nearly full

**7.** A repeated multi-step review procedure should be available to the whole team as a single invocation. What is the right mechanism?

- A. A shared document describing the steps
- B. A longer CLAUDE.md
- C. A saved chat transcript
- D. A custom slash command or skill committed to the repository

## Scenario C: multi-agent research system

A coordinator delegates to search, analysis, synthesis, and report subagents that produce cited reports.

**8.** Subagents return full source documents to the coordinator, which then exceeds its context limit. What is the correct design change?

- A. Have subagents return structured findings with citations while raw sources stay at the edge or in a scratchpad
- B. Give the coordinator a larger model
- C. Reduce the number of subagents to one
- D. Truncate each document to its first page

**9.** Final reports attribute claims to the wrong sources even though each subagent is individually accurate. What is the likely cause?

- A. The synthesis model is too small
- B. The handoff format does not carry claim and source together, so provenance is lost between stages
- C. The search subagent returns too many results
- D. Reports are generated before analysis completes

**10.** A subagent fails permanently on one source. What should the coordinator receive?

- A. Nothing, so the report proceeds
- B. A silent retry loop until it succeeds
- C. A propagated error with enough context to decide between retry, exclusion with a noted gap, or abort
- D. A generic failure flag with no detail

## Scenario D: Claude Code in CI/CD

Claude Code runs automated review on pull requests and posts feedback.

**11.** The reviewer must emit results a pipeline can parse. Which invocation is correct?

- A. Interactive session with output redirected to a log
- B. Plan mode with an approval step
- C. A cron job that emails the transcript
- D. Non-interactive print mode with JSON output and a schema

**12.** Reviews flag many low-value style nits and engineers now ignore them. Which change addresses this?

- A. Define explicit review criteria and a severity bar in the prompt, with examples of in-scope and out-of-scope findings
- B. Post findings to a separate channel
- C. Run the review only on large pull requests
- D. Cap output at five findings

## Scenario E: structured data extraction

Documents are parsed into validated records for downstream systems.

**13.** Some invoices legitimately lack a delivery date. How should the schema express this?

- A. Make the field required and let extraction fail
- B. Make the field nullable so absence is recorded explicitly, with conditional validation where the document type requires it
- C. Omit the field from the schema
- D. Default it to today's date

**14.** Which loop gives the most reliable extraction output?

- A. Generate, then manually review every record
- B. Generate three times and take the majority
- C. Enforce a JSON schema through tool use, validate, and on failure retry with the validation error provided to the model
- D. Generate with temperature zero and accept the result

**15.** Your team reports 97% accuracy measured only on records that passed validation. Why is that number misleading?

- A. Accuracy should be measured per field, not per record
- B. 97% is too low to report
- C. Validation and accuracy are unrelated
- D. It excludes the failures, so it measures where the system already succeeded rather than the true rate across all documents

---

## Answer key

| # | Answer | Domain | Why |
| :---: | --- | --- | --- |
| 1 | B | Context Management & Reliability | Cross-customer contamination is a context-scoping defect, not a window-size problem |
| 2 | C | Tool Design & MCP Integration | Structured errors with categories and retryable flags are what let an agent recover deliberately |
| 3 | D | Context Management & Reliability | Policy gaps and lack of progress are the documented escalation triggers; turn counts and order age are not |
| 4 | A | Tool Design & MCP Integration | Tool selection runs on descriptions, so differentiation is the fix for confusion between similar tools |
| 5 | B | Claude Code Configuration & Workflows | Path-scoped rules load conditionally, which is exactly the stated requirement |
| 6 | C | Claude Code Configuration & Workflows | Plan mode is a human review gate for approach, warranted by risk rather than universally |
| 7 | D | Claude Code Configuration & Workflows | Repeatable team procedures belong in committed commands or skills, not prose |
| 8 | A | Context Management & Reliability | Delegation exists to keep bulk at the edge and move distilled results |
| 9 | B | Context Management & Reliability | Provenance survives handoffs only when the format carries claim and source together |
| 10 | C | Context Management & Reliability | Errors must propagate with enough context for the coordinator to choose a recovery path |
| 11 | D | Claude Code Configuration & Workflows | CI requires non-interactive invocation with structured, schema-validated output |
| 12 | A | Prompt Engineering & Structured Output | Precision comes from explicit criteria and examples that draw the signal boundary |
| 13 | B | Prompt Engineering & Structured Output | Nullable fields record legitimate absence; required fields force fabrication or failure |
| 14 | C | Prompt Engineering & Structured Output | Schema enforcement plus a validation-retry loop is the reliability pattern the guide describes |
| 15 | D | Context Management & Reliability | Measuring only validated records is a biased sample; calibration needs coverage of all documents |

## Interpreting your score

| Raw score | Reading |
| --- | --- |
| 13 to 15 | Comfortable. Review misses, reread the six scenarios, and book the exam |
| 10 to 12 | Close. Work the weak domains, then do the guide's own preparation exercises |
| 7 to 9 | More study needed. Build an Agent SDK agent and configure Claude Code on a real project before testing |
| 6 or fewer | Start from the exam guide, including its appendix of named technologies |

This scale is a study aid, not a predictor. The real exam reports a scaled score from 100 to 1,000 with 720 to pass.

Tally misses by domain; two or more in one domain marks your next study target, as the real score report's percent-correct breakdown would.

---

Written by the maintainer for self-assessment. [Study guide](README.md) · [Study notes](notes.md) · [Mock 2](mock-exam-2.md) · [Mock 3](mock-exam-3.md) · [Practice questions](practice-questions.md) · [Repository index](../README.md)
