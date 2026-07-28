# Practice engine

A shuffled, timed, scored practice exam drawn from the repository's bank of 100 questions across the four certifications. Every run samples different questions and reorders the options, so nothing can be memorised by position. Answers and rationales appear after you finish, with a per-domain breakdown in the style of the real score report.

The questions are original, written against the public blueprints. They are not items from the live exam, which is covered by a [non-disclosure agreement](policies.md#confidentiality).

<div id="quiz-app" class="quiz">
  <noscript>The interactive engine needs JavaScript. Use the command line runner below, or read the written <a href="../associate-foundations/practice-questions.md">practice questions</a> and <a href="../associate-foundations/mock-exam.md">mock exams</a>.</noscript>
</div>

## On the command line

The same engine runs in a terminal, which is useful for repeated drilling:

```bash
git clone https://github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS.git
cd CLAUDE-CERTIFICATIONS
python .github/scripts/mock_exam.py --exam developer-foundations --count 15
```

Useful flags: `--domain "Tool Design"` to drill one domain, `--review` to see each answer as you go, `--count 25` for a longer sitting, and `--seed 7` to reproduce a run exactly. It needs only Python 3, no packages.

## How the bank works

The questions live in the markdown pages, which stay readable and reviewable: the [practice questions](practice.md) and mock exams in each certification folder. A build script parses those pages into `question-bank.json`, which both the browser engine and the command line runner consume, so no question is ever written twice and the prose and the data cannot drift apart.

```bash
python .github/scripts/build_question_bank.py --check
```

Contributions of new questions go into the markdown, not the JSON. See [contributing](https://github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS/blob/main/.github/CONTRIBUTING.md).

---

This page is the repository's own practice tooling. [Repository index](../README.md)
