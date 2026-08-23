<div align="center">

<a href="https://amey-thakur.github.io/CLAUDE-CERTIFICATIONS/" title="Open the website"><img src=".github/assets/logos/claude-symbol.svg" alt="Claude symbol, links to the website" width="80"></a>

# Claude Certifications

**One place to prepare for every Anthropic Claude certification.**

Official exam guides, blueprints, policies, courses, and study notes,
collected and organized so you can spend your time studying, not searching.

[Website](https://amey-thakur.github.io/CLAUDE-CERTIFICATIONS/) · [Certifications](#the-certifications) · [Start here](#start-here) · [Program guide](guide/README.md) · [Credentials](#credentials-behind-this-guide) · [Discussions](https://github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS/discussions)

**[Download the companion (PDF)](claude-certifications-companion.pdf)** · the whole guide in one printable file

[![Checks](https://github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS/actions/workflows/checks.yml/badge.svg)](https://github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS/actions/workflows/checks.yml)
[![Release](https://img.shields.io/github/v/release/Amey-Thakur/CLAUDE-CERTIFICATIONS?label=release&color=c15f3c)](https://github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS/releases/latest)
[![Curated by](https://img.shields.io/badge/curated%20by-Amey%20Thakur-0969DA)](https://github.com/Amey-Thakur)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

<a href=".github/assets/roadmap.png" title="View the certification roadmap at full size"><img src=".github/assets/roadmap.png" alt="Claude certification roadmap: all four certifications with exam codes, fees, item counts, domain weights, and the courses that prepare for each" width="100%"></a>

</div>

---

Built and maintained by [Amey Thakur](https://github.com/Amey-Thakur) after completing the program's curriculum. This is a community resource, not an official Anthropic repository: the official program lives on [Anthropic Partner Academy](https://anthropic-partners.skilljar.com/), and exams are delivered by [Pearson VUE](https://www.pearsonvue.com/us/en/anthropic.html).

> [!NOTE]
> I worked through every course and collected all of this while preparing myself. None of it required anything you do not already have: the official material is free, the blueprints tell you exactly what is tested, and the rest is steady work. I put it in one place so your time goes into learning rather than looking. If it helps you get certified, it did its job.
>
> Amey Thakur

## The certifications

Each certification has its own folder containing the study guide, the official exam guide PDF, the maintainer's study notes, and original practice questions.

| Certification | Questions | Fee | Study guide | Exam guide | Notes | Practice | Mocks | Cheat sheet |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Associate – Foundations | 60 | $99 | [Guide](associate-foundations/README.md) | [PDF](associate-foundations/exam-guide.pdf) | [Notes](associate-foundations/notes.md) | [Questions](associate-foundations/practice-questions.md) | [1](associate-foundations/mock-exam-1.md) · [2](associate-foundations/mock-exam-2.md) · [3](associate-foundations/mock-exam-3.md) | [Sheet](associate-foundations/cheat-sheet.md) |
| Developer – Foundations | 53 | $125 | [Guide](developer-foundations/README.md) | [PDF](developer-foundations/exam-guide.pdf) | [Notes](developer-foundations/notes.md) | [Questions](developer-foundations/practice-questions.md) | [1](developer-foundations/mock-exam-1.md) · [2](developer-foundations/mock-exam-2.md) · [3](developer-foundations/mock-exam-3.md) | [Sheet](developer-foundations/cheat-sheet.md) |
| Architect – Foundations | 60 | $125 | [Guide](architect-foundations/README.md) | [PDF](architect-foundations/exam-guide.pdf) | [Notes](architect-foundations/notes.md) | [Questions](architect-foundations/practice-questions.md) | [1](architect-foundations/mock-exam-1.md) · [2](architect-foundations/mock-exam-2.md) · [3](architect-foundations/mock-exam-3.md) | [Sheet](architect-foundations/cheat-sheet.md) |
| Architect – Professional | 63 | $175 | [Guide](architect-professional/README.md) | [PDF](architect-professional/exam-guide.pdf) | [Notes](architect-professional/notes.md) | [Questions](architect-professional/practice-questions.md) | [1](architect-professional/mock-exam-1.md) · [2](architect-professional/mock-exam-2.md) · [3](architect-professional/mock-exam-3.md) | [Sheet](architect-professional/cheat-sheet.md) |

Every exam: 120 minutes, closed book, proctored by Pearson VUE online or at a test center, passing score 720 of 1,000, credential valid 12 months with free renewal, badge via Credly. Fees are list prices in USD; partner tiers receive automatic discounts. Registration requires a Claude Partner Network company email.

> [!TIP]
> Every course in the program is free on the public [Anthropic Academy](https://anthropic.skilljar.com/), no partner account needed. Only the proctored exams require Claude Partner Network membership, so you can learn the whole syllabus before deciding whether to certify.
>
> Prefer one file? The whole guide is a printable companion: [claude-certifications-companion.pdf](claude-certifications-companion.pdf), thirty-three pages in five parts: choose your exam, know it, prepare, sit it, and keep going.

## Start here

```mermaid
flowchart TD
    Q{What do you do?}
    Q -->|Advise customers and run engagements| A[Associate - Foundations]
    Q -->|Build with the API, Claude Code, or MCP| D[Developer - Foundations]
    Q -->|Design solutions end to end| RF[Architect - Foundations]
    RF -. then .-> RP[Architect - Professional]
```

1. **Pick your exam.** Advising customers: [Associate](associate-foundations/README.md). Building with the API, Claude Code, or MCP: [Developer](developer-foundations/README.md). Designing solutions end to end: [Architect Foundations](architect-foundations/README.md), then [Architect Professional](architect-professional/README.md). Unsure: [how the certifications connect](guide/learning-paths.md).
2. **Study.** Read your exam's study guide and notes, then the [study strategy](guide/study-strategy.md) for a working plan, the [22 official courses](guide/courses.md) with [per-course notes](guide/course-notes.md) and [official resources](guide/resources.md) that teach the material, and the [practice engine](guide/quiz.md) to test yourself: a shuffled, timed, scored exam drawn from 320 original questions. Clone the repository and open Claude Code inside it, and the built-in [exam coach skill](.claude/skills/exam-coach/SKILL.md) quizzes you directly from the blueprints.
3. **Book and sit.** The [registration guide](guide/registration.md) covers everything from partner email issues to the proctoring network allowlist. Policies on retakes, validity, and appeals are in [policies](guide/policies.md), and quick answers in the [FAQ](guide/faq.md).

## Flashcards

Every fact, domain weight, rule, and glossary term in this repository, as a deck of 110 cards. Turn them in the browser on the [flashcards page](https://amey-thakur.github.io/CLAUDE-CERTIFICATIONS/guide/flashcards.html), filtered by exam or by topic, or take [flashcards.tsv](flashcards.tsv) and import the whole deck into Anki, Quizlet, or RemNote.

<a href=".github/assets/flashcard-front.png" title="View this flashcard at full size"><img src=".github/assets/flashcard-front.png" alt="A flashcard asking which domain carries the most weight on the Developer Foundations exam" width="49%"></a> <a href=".github/assets/flashcard-back.png" title="View this flashcard at full size"><img src=".github/assets/flashcard-back.png" alt="The same flashcard turned over, showing applications and integration at 33 percent of the paper" width="49%"></a>

## Credentials behind this guide

All **22 Anthropic Academy courses** in the certification program, completed and independently verifiable. **19** were also issued as a digital completion badge on [Claude Academy](https://academy.claude.com), Anthropic's own domain, and every one of the 22 carries a Skilljar verification record with its completion date.

This is here so you can check the material rather than trust it. Every claim in this repository traces to an official source; these show the curriculum behind it was worked through rather than summarized from the outside.

<div align="center">

<table>
<tr>
<td align="center" width="25%">
<a href="https://academy.claude.com/verify/13103f134da7befe9615ec2adfc8c50e" title="Verify Claude 101 on Claude Academy"><img src="certificates/badges/claude-101.png" width="100%" alt="Claude Academy completion badge for Claude 101, issued to Amey Thakur"></a>
<br><b>Claude 101</b>
<br><sub><a href="https://academy.claude.com/verify/13103f134da7befe9615ec2adfc8c50e">Verify</a></sub>
</td>
<td align="center" width="25%">
<a href="https://academy.claude.com/verify/c916ad7d1190ea2447bb2fcf3809ef16" title="Verify Claude Platform 101 on Claude Academy"><img src="certificates/badges/claude-platform-101.png" width="100%" alt="Claude Academy completion badge for Claude Platform 101, issued to Amey Thakur"></a>
<br><b>Claude Platform 101</b>
<br><sub><a href="https://academy.claude.com/verify/c916ad7d1190ea2447bb2fcf3809ef16">Verify</a></sub>
</td>
<td align="center" width="25%">
<a href="https://academy.claude.com/verify/47482157d8dbc48e39d22aaa49d6d9b1" title="Verify Claude Code 101 on Claude Academy"><img src="certificates/badges/claude-code-101.png" width="100%" alt="Claude Academy completion badge for Claude Code 101, issued to Amey Thakur"></a>
<br><b>Claude Code 101</b>
<br><sub><a href="https://academy.claude.com/verify/47482157d8dbc48e39d22aaa49d6d9b1">Verify</a></sub>
</td>
<td align="center" width="25%">
<a href="https://academy.claude.com/verify/7f0839f0576b57f38658e8784e4c9a83" title="Verify Claude Code in Action on Claude Academy"><img src="certificates/badges/claude-code-in-action.png" width="100%" alt="Claude Academy completion badge for Claude Code in Action, issued to Amey Thakur"></a>
<br><b>Claude Code in Action</b>
<br><sub><a href="https://academy.claude.com/verify/7f0839f0576b57f38658e8784e4c9a83">Verify</a></sub>
</td>
</tr>
<tr>
<td align="center" width="25%">
<a href="https://academy.claude.com/verify/f6a1826e7f9054f5e41bf340a402fe58" title="Verify Building with the Claude API on Claude Academy"><img src="certificates/badges/building-with-the-claude-api.png" width="100%" alt="Claude Academy completion badge for Building with the Claude API, issued to Amey Thakur"></a>
<br><b>Building with the Claude API</b>
<br><sub><a href="https://academy.claude.com/verify/f6a1826e7f9054f5e41bf340a402fe58">Verify</a></sub>
</td>
<td align="center" width="25%">
<a href="https://academy.claude.com/verify/0377c528acb2ecff93695ef9a9b56369" title="Verify Introduction to Model Context Protocol on Claude Academy"><img src="certificates/badges/introduction-to-model-context-protocol.png" width="100%" alt="Claude Academy completion badge for Introduction to Model Context Protocol, issued to Amey Thakur"></a>
<br><b>Introduction to Model Context Protocol</b>
<br><sub><a href="https://academy.claude.com/verify/0377c528acb2ecff93695ef9a9b56369">Verify</a></sub>
</td>
<td align="center" width="25%">
<a href="https://academy.claude.com/verify/f7904c762c678c6e136bc866545a47e4" title="Verify Model Context Protocol: Advanced Topics on Claude Academy"><img src="certificates/badges/model-context-protocol-advanced-topics.png" width="100%" alt="Claude Academy completion badge for Model Context Protocol: Advanced Topics, issued to Amey Thakur"></a>
<br><b>Model Context Protocol: Advanced Topics</b>
<br><sub><a href="https://academy.claude.com/verify/f7904c762c678c6e136bc866545a47e4">Verify</a></sub>
</td>
<td align="center" width="25%">
<a href="https://academy.claude.com/verify/707d8089647cf8c2a99e833811ef8411" title="Verify AI Fluency: Framework &amp;amp; Foundations on Claude Academy"><img src="certificates/badges/ai-fluency-framework-and-foundations.png" width="100%" alt="Claude Academy completion badge for AI Fluency: Framework &amp;amp; Foundations, issued to Amey Thakur"></a>
<br><b>AI Fluency: Framework &amp;amp; Foundations</b>
<br><sub><a href="https://academy.claude.com/verify/707d8089647cf8c2a99e833811ef8411">Verify</a></sub>
</td>
</tr>
</table>

**[See all 22 certificates and 19 badges](certificates/README.md)**

</div>

| Track | Courses | Academy badges | What it covers |
| --- | ---: | ---: | --- |
| [Claude platform](certificates/README.md#claude-platform) | 5 | 5 | Claude 101, the platform, Claude Code, and Cowork |
| [Developer and integration](certificates/README.md#developer-and-integration) | 5 | 3 | The API, Model Context Protocol, and building agents |
| [Deployment platforms](certificates/README.md#deployment-platforms) | 2 | 2 | Claude on Amazon Bedrock and Google Cloud Vertex AI |
| [AI Fluency](certificates/README.md#ai-fluency) | 10 | 9 | The framework, and its versions for builders, educators, students, nonprofits and small businesses |

> [!NOTE]
> **A course certificate is not a certification credential, and this section claims only the first.** The 22 courses above are free, self-paced, and open to anyone on the public [Anthropic Academy](https://anthropic.skilljar.com/). The four certifications are separate: each requires a proctored Pearson VUE exam, a passing score of 720 of 1,000, and Claude Partner Network membership to register, and each is issued as a Credly badge that is valid for 12 months. The two are verified on different systems and should never be presented as the same thing.

## What is where

| Folder | Contents |
| --- | --- |
| [associate-foundations](associate-foundations/) · [developer-foundations](developer-foundations/) · [architect-foundations](architect-foundations/) · [architect-professional](architect-professional/) | One folder per certification: study guide, official exam guide PDF, study notes, practice questions |
| [guide](guide/) | Program-wide pages: learning paths, study strategy, official resources, practice, registration, policies, FAQ, and glossary, plus the official policy PDFs and their [provenance](guide/official-sources.md) |
| [certificates](certificates/) | The maintainer's 22 Anthropic Academy course certificates, with previews and verification links |
| [.github](.github/) | Repository housekeeping: CI, templates, logo assets, and the [script](.github/scripts/update_resources.py) that keeps mirrored PDFs current |

## Questions and community

Ask questions, share how your exam went, and compare preparation notes in [Discussions](https://github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS/discussions). Found a broken link or an outdated fact? [Open an issue](https://github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS/issues/new/choose).

> [!IMPORTANT]
> Every candidate accepts a non-disclosure agreement covering exam questions, answer options, and scenarios. It forbids publishing or posting that content anywhere, which includes forums like this one. Never post or request real exam content here. Blueprints, official sample questions, and the practice material in this repository are all fair game.

Preparing someone else? The [share kit](guide/share.md) has the links, ready-to-use copy, and images.

Contributions that keep facts current are welcome; see [CONTRIBUTING.md](.github/CONTRIBUTING.md).

---

<div align="center">

<a href="https://www.anthropic.com" title="Anthropic">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/logos/anthropic-wordmark-dark.svg">
  <img src=".github/assets/logos/anthropic-wordmark.svg" alt="Anthropic" width="160">
</picture>
</a>

<sub>Not affiliated with or endorsed by Anthropic. Claude and Anthropic are trademarks of Anthropic PBC.<br>
Repository text is <a href="LICENSE">MIT licensed</a>; mirrored documents and logo artwork keep their own provenance
(<a href="guide/official-sources.md">sources</a>, <a href=".github/assets/logos/README.md">logos</a>).</sub>

<sub>Facts last verified against the official sources on 2026-08-22.</sub>

</div>
