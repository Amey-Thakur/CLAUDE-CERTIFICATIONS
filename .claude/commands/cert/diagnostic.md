---
description: Find your weak domains before you start studying, with a short blueprint-weighted assessment
argument-hint: [associate | developer | architect-foundations | architect-professional]
---

Run a diagnostic assessment for the certification named in `$ARGUMENTS`. If no certification was given, ask which of the four they are preparing for and stop until they answer.

## Prepare

1. Read that certification's `README.md` for the blueprint: domains, weights, objectives.
2. Read `question-bank.json` at the repository root and select that exam's questions.

## Run

Ask 12 questions drawn across every domain, allocated by blueprint weight so heavy domains get more items. Shuffle the option order for each question. Present one question at a time and wait for an answer before continuing. Do not reveal whether an answer was right until the end: this is a measurement, not a lesson.

If the bank has fewer questions than a domain's allocation needs, write additional ones in the same style, grounded strictly in that domain's published objectives.

## Report

Produce a readiness profile:

- Overall score, and how it maps to the readiness bands in the certification's `mock-exam-1.md`
- A table of every domain: questions asked, correct, and the domain's exam weight
- Weak domains, ranked by the product of error rate and exam weight, so the ranking reflects what will actually cost marks
- For each weak domain, the two or three specific objectives from the blueprint that the missed questions map to

Close by recommending the next step: `/cert:drill` for a weak domain, or `/cert:prep-plan` if several domains are weak.
