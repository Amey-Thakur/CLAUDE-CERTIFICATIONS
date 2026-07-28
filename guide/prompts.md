# Prompts for studying with Claude

Every prompt on this page is ready to use. Copy one with the button on the right of the block, paste it into Claude, and fill in the part in braces. They are written to make Claude behave like a tutor who knows the blueprint rather than a search box.

> [!IMPORTANT]
> Never paste real exam questions, answer options, or scenario wording into any of these. Every candidate signs a non-disclosure agreement. Use the blueprint, the official exam guides, and the practice material here, all of which are published.
>
> Working in the terminal instead? Clone the repository, open Claude Code inside it, and the built-in [exam coach skill](https://github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS/blob/main/.claude/skills/exam-coach/SKILL.md) does all of this from the blueprints directly, with six slash commands.

## Find out where you stand

Run this first. It produces a ranked list of what to study, which is more useful than working through the syllabus in order.

```text
You are helping me prepare for the {Claude Certified Architect – Foundations} exam.

Here is the published blueprint with the weight of each domain:
{paste the domain table from the exam's study guide}

Ask me one question at a time, twelve in total, spread across the domains in
proportion to their weight. Scenario-based, one best answer, four options.
Do not tell me the answer until I have committed to one.

After all twelve, give me:
- A score per domain
- The two domains where I am weakest, in weight order
- What specifically I misunderstood, not just which questions I missed
- What to study first, and why that order
```

## Drill one domain

Use this after the diagnostic, on the domain that carries the most weight among your weak ones.

```text
I am preparing for the {Claude Certified Developer – Foundations} exam and I am
weak on {Applications and integration}, which is {33}% of the paper.

Drill me on it. Ten scenario questions, one at a time, increasing in difficulty.
Each must have one clearly best answer and three distractors that fail a stated
constraint, the way the real items are written.

After each answer, tell me the rule the question was testing in one sentence,
whether or not I got it right. At the end, list the rules I did not know.
```

## Understand a question you got wrong

The most valuable prompt on this page. Use it on questions from the practice sets here.

```text
I got this practice question wrong.

Question: {paste the question and its four options from this repository}
I chose: {your answer}
The correct answer is: {the correct answer}

Do not just restate the rationale. Tell me:
- What rule or principle the question is actually testing
- Why the option I chose is attractive, and what constraint it fails
- What would have to change in the scenario for my answer to become correct
- Two other situations where the same rule decides the answer
```

## Turn the blueprint into a study plan

```text
I am sitting the {Claude Certified Associate – Foundations} exam on {date}.
I can study {5} hours a week.

Here is the blueprint with domain weights:
{paste the domain table from the exam's study guide}

Here is my diagnostic result:
{paste the per-domain scores from the diagnostic prompt above}

Build me a week-by-week plan that allocates time by weight and by weakness, not
evenly. For each week, state what I will study, what I will build or practice,
and the check that tells me the week worked. Keep it realistic for the hours I
have, and say what to drop if I fall behind.
```

## Explain a concept the way the exam tests it

```text
Explain {prompt caching} as the {Claude Certified Developer – Foundations} exam
would test it.

I do not want a general explanation. I want:
- The decision the exam expects me to make about it
- The conditions under which it is the right answer
- The conditions under which it is the wrong answer, and what is right instead
- The distractor a question writer would use to tempt me
```

## Rehearse an Architect scenario

For the Architect Foundations exam, whose items are framed inside six published scenarios.

```text
Here is one of the published exam scenarios:
{paste one of the six scenarios from the study guide, with its primary domains}

Play the role of the customer's technical lead. I am the architect. Interview me
about how I would design this, pushing on the decisions the scenario's primary
domains cover.

Challenge weak reasoning rather than accepting it. When I finish, tell me which
of my decisions would not survive the exam's standard, and why.
```

## Interpret a real score report

For a failed attempt, where the report gives percent-correct by domain.

```text
I sat the {Claude Certified Architect – Professional} exam and did not pass.

My scaled score: {680} of 1,000, with 720 to pass.
Percent correct by domain:
{paste the per-domain breakdown from the score report}

Here are the domain weights:
{paste the domain table from the exam's study guide}

Work out where the points actually went, weighting each domain by its share of
the paper. Tell me the smallest set of domains that would close the gap, roughly
how much study each needs, and whether I should retake at the earliest permitted
date or wait. Do not be encouraging at the expense of being accurate.
```

## Check something you have written

```text
I wrote this summary of {how retakes and credential renewal work} for my own
notes:

{paste your notes}

Here is the official source:
{paste the relevant section of the exam policy PDF, or link it}

Check my summary against the source line by line. List anything I have stated
that the source does not support, anything material I have left out, and
anything I have subtly changed. Do not soften the corrections.
```

## Build something, which the guides ask for

Every official exam guide recommends building. This turns that into a scoped task.

```text
I am preparing for the {Claude Certified Developer – Foundations} exam.

Propose three small projects I could build in a weekend that would force me to
use the parts of the platform this exam actually tests. For each one, say which
domains it exercises, what I would have to get right for it to work, and what
about it would still leave me unprepared.

Then help me build the one that covers the most weight.
```

---

Facts drawn from the official Anthropic exam guides. [Practice engine](quiz.md) · [Practice questions](practice.md) · [Repository index](../README.md)
