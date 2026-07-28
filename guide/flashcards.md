# Flashcards

Every fact, weight, rule, and term in this repository as a deck of 110 cards. Turn them here, or take the file and study them anywhere.

<div id="deck" class="quiz">
  <noscript>The interactive deck needs JavaScript. Every card is written out further down this page.</noscript>
</div>

## Take the deck with you

[flashcards.tsv](../flashcards.tsv) imports directly into Anki, Quizlet, or RemNote: three tab-separated columns, front, back, and tags, so you can study one certification or one topic at a time.

```text
https://github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS/raw/main/flashcards.tsv
```

> [!TIP]
> In Anki, choose File, then Import, select the file, set the field separator to Tab, and map the third column to Tags. Filter by a tag such as `developer-foundations` or `policy` to drill one area.

![A card, front face](../.github/assets/flashcard-front.png)

![The same card turned over](../.github/assets/flashcard-back.png)

## Every card in writing

The full deck below, for reading, printing, or checking one fact quickly. It is generated from the same source as the rest of the documentation, so it cannot drift out of date.

## Exam facts

| Front | Back |
| --- | --- |
| Associate – Foundations: exam code | CCAO-F |
| Associate – Foundations: how many items | 60 items |
| Associate – Foundations: list fee before partner discount | $99 |
| Associate – Foundations: who is it for | Consultants, sellers, and delivery leads |
| Developer – Foundations: exam code | CCDV-F |
| Developer – Foundations: how many items | 53 items |
| Developer – Foundations: list fee before partner discount | $125 |
| Developer – Foundations: who is it for | Engineers building on the Claude platform |
| Architect – Foundations: exam code | CCAR-F |
| Architect – Foundations: how many items | 60 items |
| Architect – Foundations: list fee before partner discount | $125 |
| Architect – Foundations: who is it for | Architects building production systems |
| Architect – Professional: exam code | CCAR-P |
| Architect – Professional: how many items | 63 items |
| Architect – Professional: list fee before partner discount | $175 |
| Architect – Professional: who is it for | Architects governing systems at scale |
| Passing score on every Claude certification exam | 720 on a scaled range of 100 to 1,000 |
| Time limit on every Claude certification exam | 120 minutes, with about 135 minutes of total seat time |
| Who delivers the exams | Pearson VUE, online proctored through OnVUE or at a test centre |
| Where does the digital badge come from | Credly, by email after a pass |
| Which exam does not count toward partner tier eligibility | Claude Certified Associate |
| Partner tier discounts on exam fees | Select, Preferred, and Global Premier partners receive 50% off, applied at checkout |
| How many scenarios does Architect Foundations present, and from how many | Four, drawn from a published bank of six |
| Where can you take the official courses without a partner account | The public Anthropic Academy; every course is free there |

## Blueprints and weights

| Front | Back |
| --- | --- |
| Associate – Foundations: heaviest domain and its weight | Output evaluation at 21% |
| Associate – Foundations: lightest domain and its weight | Troubleshooting at 10% |
| Associate – Foundations: domains in weight order | Output evaluation 21% → Workflow integration 16% → Governance and risk 15% → Prompting 14% → Product and model choice 12% → Configuration 12% → Troubleshooting 10% |
| Developer – Foundations: heaviest domain and its weight | Applications and integration at 33.1% |
| Developer – Foundations: lightest domain and its weight | Eval, testing, and debugging at 2.6% |
| Developer – Foundations: domains in weight order | Applications and integration 33.1% → Model selection and optimization 16.8% → Agents and workflows 14.7% → Prompt and context engineering 11.0% → Tools and MCPs 10.6% → Security and safety 8.1% → Claude Code 3.1% → Eval, testing, and debugging 2.6% |
| Architect – Foundations: heaviest domain and its weight | Agentic architecture at 27% |
| Architect – Foundations: lightest domain and its weight | Context and reliability at 15% |
| Architect – Foundations: domains in weight order | Agentic architecture 27% → Claude Code workflows 20% → Prompting, structured output 20% → Tool design and MCP 18% → Context and reliability 15% |
| Architect – Professional: heaviest domain and its weight | Integration at 19% |
| Architect – Professional: lightest domain and its weight | Developer enablement at 7% |
| Architect – Professional: domains in weight order | Integration 19% → Solution design 17% → Evaluation and testing 16% → Governance and risk 14% → Stakeholders, lifecycle 14% → Models and prompting 13% → Developer enablement 7% |

## The rules that decide questions

| Front | Back |
| --- | --- |
| Associate – Foundations: Verify anything specific and consequential. Why? | Confidence is not evidence. |
| Associate – Foundations: Omission fails too. Why? | Read the source, not only the output. |
| Associate – Foundations: Anonymize, then analyze. Why? | Instructions are not a control. |
| Associate – Foundations: finish the rule: Match the model to the ... | Match the model to the task in both directions. |
| Associate – Foundations: finish the rule: Structure beats intensifiers: ... | Structure beats intensifiers: role, sections, constraints, example. |
| Associate – Foundations: finish the rule: Projects hold what repeats; ... | Projects hold what repeats; prompts hold what changes. |
| Associate – Foundations: finish the rule: Project knowledge is maintained by you, ... | Project knowledge is maintained by you, not self-updating. |
| Associate – Foundations: finish the rule: Diagnose what changed ... | Diagnose what changed before rewriting anything. |
| Associate – Foundations: finish the rule: Escalate system integrations to ... | Escalate system integrations to Developer and Architect scope. |
| Developer – Foundations: finish the rule: stop_reason drives the loop: ... | stop_reason drives the loop: tool_use executes, end_turn finishes. |
| Developer – Foundations: finish the rule: Batches for latency-tolerant volume: ... | Batches for latency-tolerant volume: half cost, 24-hour window. |
| Developer – Foundations: Stable prefix first, then cache it. Why? | Cuts latency and cost together. |
| Developer – Foundations: finish the rule: Enforce a schema, ... | Enforce a schema, validate, retry with the validation error. |
| Developer – Foundations: Known path is a workflow. Why? | Unknown path earns an agent. |
| Developer – Foundations: finish the rule: Subagents exist to isolate context, ... | Subagents exist to isolate context, not to add horsepower. |
| Developer – Foundations: finish the rule: Pin model versions; ... | Pin model versions; upgrades become evaluated changes. |
| Developer – Foundations: finish the rule: Injection is defeated structurally, ... | Injection is defeated structurally, never by asking politely. |
| Developer – Foundations: finish the rule: A tool the agent does not ... | A tool the agent does not hold cannot be misused. |
| Architect – Foundations: finish the rule: Agent loops need engineered termination, ... | Agent loops need engineered termination, not a token budget. |
| Architect – Foundations: finish the rule: Escalate on policy gaps ... | Escalate on policy gaps and lack of progress. |
| Architect – Foundations: finish the rule: Structured errors: ... | Structured errors: a category and a retryable flag. |
| Architect – Foundations: Tool descriptions are the selection mechanism. Why? | Differentiate them. |
| Architect – Foundations: finish the rule: Hard limits belong in the tool layer, ... | Hard limits belong in the tool layer, never in a prompt. |
| Architect – Foundations: finish the rule: CLAUDE.md hierarchy, ... | CLAUDE.md hierarchy, with path-scoped rules for conditional context. |
| Architect – Foundations: finish the rule: CI means headless: ... | CI means headless: print mode, JSON output, a schema. |
| Architect – Foundations: finish the rule: Subagents return findings; ... | Subagents return findings; raw documents stay at the edge. |
| Architect – Foundations: finish the rule: Provenance must survive ... | Provenance must survive every handoff. |
| Architect – Professional: finish the rule: Climb the pattern ladder only when ... | Climb the pattern ladder only when the rung below cannot hold. |
| Architect – Professional: finish the rule: Least privilege means removal, ... | Least privilege means removal, not monitoring. |
| Architect – Professional: finish the rule: Retrieval degradation after a data change ... | Retrieval degradation after a data change is an index problem. |
| Architect – Professional: finish the rule: Subjective quality is measured with ... | Subjective quality is measured with rubrics and labeled sets. |
| Architect – Professional: finish the rule: Prompt changes are production changes: ... | Prompt changes are production changes: regression, then A/B. |
| Architect – Professional: finish the rule: Compliance is enforced before ... | Compliance is enforced before data crosses the boundary. |
| Architect – Professional: finish the rule: Route human review by ... | Route human review by confidence and consequence. |
| Architect – Professional: finish the rule: Present segmented, ... | Present segmented, honest numbers, never a flattering average. |
| Architect – Professional: finish the rule: Observability captures traces, ... | Observability captures traces, not just outputs. |

## Policies and scoring

| Front | Back |
| --- | --- |
| How long is a Claude credential valid | 12 months from the date it is earned |
| What does on-time renewal involve | A free, open-book, non-proctored assessment on Anthropic Partner Academy, retakable as often as needed |
| What happens if a credential lapses | You must pass the full exam again at full fee |
| Retake waiting periods after failed attempts | 14 days after the first, 30 after the second, 90 after the third |
| Maximum attempts per exam per rolling 12 months | Four |
| Free cancellation or reschedule window | At least 24 hours before the appointment; inside that, the fee is forfeited |
| How is the exam scored, in one phrase | Criterion-referenced: against a fixed standard, not against other candidates |
| What does the score report show beyond pass or fail | The scaled score and percent-correct per domain |
| Is there an official practice exam | No. The previous platform's was retired in the Pearson migration; the exam guides' sample questions are the only official items |
| What is the authoritative scope of an exam | The blueprint in its official exam guide; anything outside it is not tested |
| Are the exams open book | No. No notes, documentation, translation tools, or AI assistants |
| Who may currently sit these exams | People at Claude Partner Network organizations, registering with a recognised company email |
| How long do partner email domain record changes take | 7 to 10 days, so resolve them before you plan to sit |
| What does the exam NDA cover | Questions, answer options, and scenarios, explicitly including study groups and online forums |

## Glossary

| Front | Back |
| --- | --- |
| Glossary: Blueprint | The exam content outline in each exam guide: the domains measured, their weights, and the objectives items are written against. The authoritative scope of the exam |
| Glossary: Domain weight | The approximate share of scored items drawn from a domain, for example 33.1% for the Developer exam's Applications and integration domain |
| Glossary: Task statement | A numbered capability within a domain, used in the Architect Foundations guide, that items are written against |
| Glossary: MQC | Minimally qualified candidate: the profile of the weakest examinee who should still pass, which the passing standard is calibrated to |
| Glossary: Criterion-referenced | Scored against a fixed standard rather than against other candidates. There is no curve |
| Glossary: Scaled score | The reported score on a 100 to 1,000 range, equated so results are comparable across exam forms of slightly different difficulty |
| Glossary: Cut score | The passing threshold: 720 scaled, for all four exams |
| Glossary: Item | An exam question. Multiple-choice items have one best answer; multiple-response items state how many responses to select |
| Glossary: Scenario-based exam | The Architect Foundations format: 4 scenarios drawn from a published bank of 6, each framing a set of items |
| Glossary: Exam form | A specific assembled version of an exam; forms vary slightly, which scaled scoring corrects for |
| Glossary: NDA | The non-disclosure agreement accepted before the exam starts: exam content may not be shared, reproduced, or discussed, including in study groups and forums |
| Glossary: Pearson VUE | The company that delivers the exams, online and at test centers, since June 30, 2026 |
| Glossary: OnVUE | Pearson's online proctoring application, run on your own computer under remote supervision |
| Glossary: Test center | A physical Pearson location with provided equipment, the alternative to online proctoring |
| Glossary: Credly | The digital badging platform that issues the shareable credential after a pass |
| Glossary: CPN | The Claude Partner Network, whose member organizations are eligible for certification |
| Glossary: Partner tier | An organization's CPN level: Registered pays list price; Select, Preferred, and Global Premier receive 50% off exams |
| Glossary: Prep path | The curated course sequence on Partner Academy for a specific certification |
| Glossary: Exam guide | The official PDF for each certification: blueprint, sample questions, policies, and scoring. The single most important study document |
| Glossary: Renewal assessment | The free, open-book, non-proctored assessment on Partner Academy that extends a credential 12 months when passed before expiry |
| Glossary: Lapse | Letting a credential expire without renewing; regaining it requires the full exam at full fee |
| Glossary: Appeal | A formal challenge to a certification decision or result, filed with Pearson within 14 days |
| Glossary: Question report | Flagging a possibly faulty item to Pearson; separate from an appeal and never counted against you |
| Glossary: Accommodations | Testing adjustments for documented needs, requested through Pearson and approved before scheduling |

---

Facts drawn from the official Anthropic exam guides. [Repository index](../README.md)
