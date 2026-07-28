# Maintenance guide

How this repository stays current. Written for maintainers and anyone submitting substantial pull requests.

## What must be kept true

The repository's value is that its facts match the official program. The volatile facts, and where they live:

| Fact | Lives in | Official source |
| --- | --- | --- |
| Prices, discounts, question counts | README, all four certification pages, FAQ | [Certifications page](https://anthropic-partners.skilljar.com/page/partner-certifications), exam guides |
| Exam guide versions and blueprints | Certification pages, mirrored PDFs | Exam guide PDFs on the certifications page |
| Policies: retakes, validity, renewal | guide/policies.md, guide/faq.md | [Policies page](https://anthropic-partners.skilljar.com/page/policies-certifications), policy PDFs |
| Course catalog and prep paths | guide/learning-paths.md | [All courses](https://anthropic-partners.skilljar.com/page/all-courses), [prep courses](https://anthropic-partners.skilljar.com/page/claude-certification-exam-prep-courses) |
| OnVUE requirements | guide/registration.md | [Setup page](https://anthropic-partners.skilljar.com/page/computer-and-network-setup) |

Every documentation page carries a "facts last verified" date in its footer. Update that date only after actually re-checking the page's facts against the sources above.

## Routine

**Weekly, automated.** The link-check workflow runs on a schedule and flags dead links. Treat a newly dead official link as a signal that Anthropic moved or changed something, not just as a link to fix.

**Monthly, manual.** Run the resource updater and review what changed:

```bash
python .github/scripts/update_resources.py
```

The script re-downloads every mirrored official PDF, verifies each file is a valid PDF, and reports which files changed by hash. If an exam guide changed, diff the exam facts (version, item counts, domains, weights, fees) against the matching documentation page, update the page, update its footer date, and note the change in the next release.

**When Anthropic announces changes.** Program changes have historically landed as dated cutovers (the June 30, 2026 Pearson migration; the August 31, 2026 Global Premier discount expiry). Dated facts like these are written into the pages deliberately so that stale ones are findable: search the docs for the current year to audit them.

## Regenerating the derived files

Most of what this repository ships is generated from a source somewhere else in it, so edit the source and rebuild rather than editing the output. Every script is standard library only.

`build_images.py` holds `CERTS`, the exam facts every other script and image is built from. Change an exam fact there, not in the outputs.

| Command | Reads | Writes |
| --- | --- | --- |
| `python .github/scripts/build_question_bank.py` | the practice and mock markdown in each exam folder | `question-bank.json` |
| `python .github/scripts/build_tracker.py` | `CERTS` | `.github/assets/tracker.json` |
| `python .github/scripts/build_flashcards.py` | `CERTS` and [glossary.md](glossary.md) | `flashcards.tsv`, `guide/flashcards.md`, `.github/assets/flashcards.json` |
| `python .github/scripts/build_images.py --render` | `CERTS`, which it defines | the roadmap, the four cheat sheets, the social preview, both flashcard faces |
| `python .github/scripts/build_extra_images.py --render` | shared helpers from `build_images.py` | the six supporting cards |
| `python .github/scripts/build_booklet.py --render` | every image above, plus the glossary and the certificates gallery | `claude-certifications-booklet.pdf` |
| `python .github/scripts/update_resources.py` | the official source URLs | the mirrored PDFs |

Each image script writes an SVG next to its PNG. The SVG is an intermediate the renderer consumes; nothing else reads it, and it is committed only so the vector artwork is available without running the script.

Rendering needs headless Chrome. Set `CHROME_PATH` if it is not on the path.

Order matters when several things change at once: question bank, then tracker and flashcards, then images, then the booklet, because the booklet embeds the images and reads the flashcard count.

Continuous integration regenerates the question bank, the tracker, and the flashcards on every push and fails if the committed files differ, so those three can never drift.

The images and the booklet cannot be checked that way. They need a browser, and the booklet is set in a font the runner does not have, so a re-render would differ byte for byte with nothing actually wrong. Instead, each render records what it was built from in `.github/assets/build-manifest.json`, and CI checks whether any of those inputs changed afterwards:

```bash
python .github/scripts/build_images.py --verify
```

If it reports something stale, run the three render commands above and commit the artifacts together with the updated manifest. The manifest is written automatically by `--render`, so there is nothing to maintain by hand.

## Editorial rules

- Facts and recommendations stay separated. Certification pages state official facts first and put advice under a clearly labeled preparation section.
- Every mirrored document keeps its source URL and last-checked date in [guide/official-sources.md](official-sources.md).
- Plain, formal prose. No emojis, no decorative badges, no marketing language, sentence case headings.
- Summaries of official text are rewritten, not copied. The mirrored PDFs carry the official wording.
- Every image has alt text. Tables stay narrow enough to read on a phone.
- File names are lowercase kebab-case throughout.

## Release strategy

The repository uses semantic-flavored [GitHub releases](https://github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS/releases), with the change summary written in the release notes:

- **Major**: structural reorganization, or coverage of a new certification program area
- **Minor**: new documents, new mirrored PDFs, updated exam guide versions
- **Patch**: corrections, refreshed dates, link fixes

Tag releases as `vX.Y.Z`. A release is warranted whenever the mirrored PDFs change or a certification's facts change, so that anyone consuming the repository can pin a known-good state. Release notes carry the dated record of what changed, since commit messages are uniform by convention.

## Repository settings worth preserving

- Issues use the three templates (broken link or error, outdated content, resource suggestion); blank issues are disabled to keep reports actionable.
- Discussions are enabled and seeded; the participation rules live in [CONTRIBUTING.md](../.github/CONTRIBUTING.md#discussions). The non-negotiable rule is that real exam content is never shared, per the exam NDA.
- Workflows: lint (markdownlint and codespell) and link checking (lychee) run on pull requests, so contributions are self-checking.
- Dependabot updates the pinned workflow actions.

## The website

The site at [amey-thakur.github.io/CLAUDE-CERTIFICATIONS](https://amey-thakur.github.io/CLAUDE-CERTIFICATIONS/) is built from this repository on every push to main by the pages workflow. The repository stays the single source of truth: .github/pages/assemble.sh copies the certification folders, the guide, and the certificates into a build tree and adjusts the few links that would otherwise point outside the site, then MkDocs Material builds it using .github/mkdocs.yml. The landing page is .github/pages/index.md and the styling is .github/pages/extra.css.

When adding or renaming a page, add it to the nav section of .github/mkdocs.yml, or it will build without appearing in the site navigation.

## Takedown stance

The mirrored PDFs are Anthropic's property, republished here for candidate convenience with full attribution. If Anthropic or its representatives request removal, remove the files promptly, leave the source links in place, and note the change in the next release.

---

[Repository index](../README.md)
