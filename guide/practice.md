# Practice with Claude

There is no official practice exam, and the [exam NDA](policies.md#confidentiality) forbids sharing real questions. What remains, and works well, is generating your own practice from the published blueprints using Claude itself. The questions Claude produces are practice aids in the official style, not leaked items, which keeps this method both effective and clean.

The fastest way to test yourself is the [practice engine](quiz.md): a shuffled, timed, scored exam drawn from all 100 questions, in the browser or from a terminal. It reorders questions and options on every run, so nothing can be memorised by position.

Start with the written sets. Each certification folder contains ten practice questions with answers and rationales shown inline ([Associate](../associate-foundations/practice-questions.md), [Developer](../developer-foundations/practice-questions.md), [Architect Foundations](../architect-foundations/practice-questions.md), [Architect Professional](../architect-professional/practice-questions.md)), plus a timed mock exam with domains hidden, an answer key at the end, and a score-interpretation table ([Associate](../associate-foundations/mock-exam.md), [Developer](../developer-foundations/mock-exam.md), [Architect Foundations](../architect-foundations/mock-exam.md), [Architect Professional](../architect-professional/mock-exam.md)). Take the practice set to learn, then the mock exam under timed conditions to measure.

The fastest route: this repository ships the coach as a built-in [Claude skill](https://github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS/blob/main/.claude/skills/exam-coach/SKILL.md). Clone the repository, open Claude Code inside it, and say "quiz me for the Developer exam". The skill reads the blueprints and exam guides in place and runs the whole coaching loop, including domain-weighted quizzes, drills, and a timed-style mock exam with a score-report-style breakdown. The prompts below do the same anywhere else Claude runs.

Setup that makes every prompt below better: create a Claude Project, upload the [exam guide PDF](../guide/official-sources.md) for your certification as knowledge, and set the Project instructions to "You are an exam coach for the {certification name} exam. Ground everything in the attached exam guide. Never invent facts about the exam itself."

## Blueprint quiz generator

Paste a domain's objectives from your certification's study page, then:

```text
Using the attached exam guide, write 10 practice questions for the domain
"{domain name}". Match the official style: scenario-based multiple choice,
four options, exactly one best answer, distractors that are plausible but
fail the stated constraint. Mix in two multiple-response items that state
how many responses to select.

Ask me the questions one at a time. After each answer, tell me whether I
was right, then explain why each wrong option is wrong, the way the
official sample rationales do. Track my score by objective and show the
breakdown at the end.
```

## Weak-domain drill

After a practice round, or after a real attempt using the percent-correct breakdown from your score report:

```text
My weakest areas are: {list domains or objectives with your scores}.
Build me a focused drill: for each weak objective, first explain the
concept in three sentences with a concrete example, then ask me two
scenario questions about it. Escalate difficulty if I answer correctly,
and re-explain from a different angle if I answer wrongly twice.
```

## Architect Foundations scenario rehearsal

Unique to [Architect – Foundations](../architect-foundations/README.md): the six scenarios are published, and four appear per sitting. Rehearse each one:

```text
The exam scenario is: {paste one of the six scenarios from the study page,
including its primary domains}. Generate 8 practice questions that this
scenario would plausibly frame, drawing only on its primary domains.
Include at least one question each about tool design, error handling, and
escalation. Quiz me one at a time with rationales.
```

## Rationale coach

The official sample rationales reward a specific skill: identifying which option addresses the stated constraint and why the others fail. Train it directly:

```text
Give me one scenario question at a time from the attached exam guide's
domains. I will answer AND explain my elimination reasoning for each
option. Grade both my answer and my reasoning: tell me where my
elimination logic differed from the strongest justification.
```

## Rules of engagement

- Generated questions calibrate your knowledge against the blueprint. They are not exam items, and treating any set of questions as "the real ones" is both a policy violation and a bad strategy, since the item bank is confidential and rotates.
- The blueprint is the boundary: if Claude drifts into topics outside the domains, pull it back. The official guide states that anything outside the blueprint is not on the exam.
- Verify anything surprising against the [official documentation](resources.md#documentation). A practice question is a study aid, not a source of truth.
- Do not post generated questions to the exam's discussion forums presented as real content, and never post real content anywhere. The [discussion rules](https://github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS/blob/main/.github/CONTRIBUTING.md#discussions) apply.

---

This page is the repository's recommendation. [Repository index](../README.md)
