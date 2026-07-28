---
description: Sit a full timed mock exam under realistic conditions, scored like the real report
argument-hint: [certification] [question count, default 15]
---

Run a timed mock exam for the certification in `$ARGUMENTS`. Default to 15 questions unless a count is given. If no certification was named, ask and stop until answered.

## Prepare

1. Read the certification's `README.md` for domain weights and, for Architect Foundations, the six published scenarios.
2. Read `question-bank.json` and draw that exam's questions, weighted by domain so the paper mirrors the real blueprint.
3. Shuffle both the question order and the options within each question.

## Conditions

State the rules before starting: closed book, no notes, no documentation, roughly two minutes per question, and every question answered because unanswered items score zero. Note the wall-clock time when the candidate begins.

For Architect Foundations, group the questions under scenarios the way the real exam does, drawing from the six published ones.

## Run

Present one question at a time. Give no feedback of any kind until the exam is over: no hints, no confirmation, no reactions. Accept "flag" to mark a question for review and revisit flagged items at the end before scoring.

## Report

1. Raw score and percentage, and elapsed time against the 2-minutes-per-question budget
2. The readiness band from the certification's `mock-exam-1.md`
3. A per-domain table of correct against asked, with each domain's exam weight
4. A full review of every missed question: the question, the correct option, the option chosen, and why the chosen one fails
5. The two domains to study next, chosen by error rate weighted by exam weight

Finish with the standing caveat: this is a study aid, and the real exam reports a scaled score from 100 to 1,000 with 720 to pass.
