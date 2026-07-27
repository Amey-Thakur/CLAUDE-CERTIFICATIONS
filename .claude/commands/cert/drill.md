---
description: Drill one weak domain with escalating questions and immediate rationales
argument-hint: [certification] [domain, for example "Tool Design"]
---

Drill the domain named in `$ARGUMENTS` for the given certification. If either is missing, ask for it and stop until answered.

## Prepare

1. Read the certification's `README.md` and locate the domain, its weight, and its objectives.
2. Read the certification's `notes.md` for the maintainer's summary of that domain.
3. Read `question-bank.json` and filter to that exam and domain.

## Run

Teach and test in alternation:

1. Explain the domain's core judgment in three or four sentences, using the notes as the frame.
2. Ask a question from the bank for that domain, options shuffled.
3. After each answer, say whether it was right, then explain why every wrong option is wrong, in the style of the official rationales: name the constraint the correct option satisfies and the reason each distractor fails it.
4. Escalate difficulty after two consecutive correct answers. After two misses on the same objective, re-teach that objective from a different angle with a concrete example before continuing.

When the bank's questions for the domain are exhausted, write new ones against the same objectives rather than repeating.

## Close

Summarize which objectives within the domain are solid and which still need work, and recommend either another drill or `/cert:mock` if the domain now looks steady.
