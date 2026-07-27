# Contributing

This repository's single job is to keep an accurate, well-organized picture of the Claude certification program. The most valuable contributions are corrections: a price that changed, a moved page, a new exam guide version, a dead link.

## Reporting

- Broken link or factual error: [open an issue](https://github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS/issues/new/choose) with the page and the correction. If you can cite the official source, include it.
- Questions about the exams themselves belong in [Discussions](https://github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS/discussions), not issues.

## Pull requests

1. Keep facts and recommendations separate, as the existing pages do. A fact needs an official source; a recommendation needs to be labeled as one.
2. Match the house style: formal, plain prose; sentence case headings; no emojis; no decorative badges; no marketing language; lowercase kebab-case file names; alt text on every image.
3. Summaries of official text must be rewritten in your own words. Do not paste blocks of Anthropic's pages into markdown; the mirrored PDFs carry the official wording.
4. If you touch a volatile fact, update the "facts last verified" footer date of that page and add a line to CHANGELOG.md.
5. CI must pass: markdown lint, spell check, and link check run on every pull request. Run the link checker locally with `lychee .` if you want a faster loop.
6. Refreshing mirrored PDFs: run `python scripts/update_resources.py`, commit the changed files, and update the last-checked date in pdfs/README.md.

## Discussions

Discussions exist so candidates can help each other: preparation approaches, how the domains felt relative to their weights, scheduling and proctoring logistics, renewal experiences.

Ground rules:

1. **Never post real exam content.** Every candidate accepts a non-disclosure agreement covering questions, answer options, and scenarios, and it explicitly extends to study groups and online forums. Posts that share or solicit live exam content will be removed. Discussing the published blueprints, the official sample questions, and general topic difficulty is fine.
2. Answer from experience, cite official sources for facts, and say which exam and date your experience refers to, since the program changes.
3. Be respectful. The [code of conduct](CODE_OF_CONDUCT.md) applies everywhere in this repository.

Suggested threads if you are unsure where to post: the pinned welcome thread for orientation, one thread per certification for preparation questions, and the exam experience thread for post-exam reflections (within NDA limits).

## Scope

In scope: the four Claude certifications, their official documents, the Academy courses that prepare for them, and the registration and policy machinery around them. Out of scope: general Claude usage tutorials, API guides unrelated to certification, and third-party courseware promotion. Braindumps and any material that violates the exam NDA are rejected outright.
