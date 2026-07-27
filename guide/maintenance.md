# Maintenance guide

How this repository stays current. Written for maintainers and anyone submitting substantial pull requests.

## What must be kept true

The repository's value is that its facts match the official program. The volatile facts, and where they live:

| Fact | Lives in | Official source |
| --- | --- | --- |
| Prices, discounts, question counts | README, all four certification pages, FAQ | [Certifications page](https://anthropic-partners.skilljar.com/page/partner-certifications), exam guides |
| Exam guide versions and blueprints | Certification pages, mirrored PDFs | Exam guide PDFs on the certifications page |
| Policies: retakes, validity, renewal | exam-policies.md, exam-faq.md | [Policies page](https://anthropic-partners.skilljar.com/page/policies-certifications), policy PDFs |
| Course catalog and prep paths | learning-paths.md | [All courses](https://anthropic-partners.skilljar.com/page/all-courses), [prep courses](https://anthropic-partners.skilljar.com/page/claude-certification-exam-prep-courses) |
| OnVUE requirements | exam-registration.md | [Setup page](https://anthropic-partners.skilljar.com/page/computer-and-network-setup) |

Every documentation page carries a "facts last verified" date in its footer. Update that date only after actually re-checking the page's facts against the sources above.

## Routine

**Weekly, automated.** The link-check workflow runs on a schedule and flags dead links. Treat a newly dead official link as a signal that Anthropic moved or changed something, not just as a link to fix.

**Monthly, manual.** Run the resource updater and review what changed:

```bash
python scripts/update_resources.py
```

The script re-downloads every mirrored official PDF, verifies each file is a valid PDF, and reports which files changed by hash. If an exam guide changed, diff the exam facts (version, item counts, domains, weights, fees) against the matching documentation page, update the page, update its footer date, and record the change in CHANGELOG.md.

**When Anthropic announces changes.** Program changes have historically landed as dated cutovers (the June 30, 2026 Pearson migration; the August 31, 2026 Global Premier discount expiry). Dated facts like these are written into the pages deliberately so that stale ones are findable: search the docs for the current year to audit them.

## Editorial rules

- Facts and recommendations stay separated. Certification pages state official facts first and put advice under a clearly labeled preparation section.
- Every mirrored document keeps its source URL and last-checked date in [guide/official-sources.md](official-sources.md).
- Plain, formal prose. No emojis, no decorative badges, no marketing language, sentence case headings.
- Summaries of official text are rewritten, not copied. The mirrored PDFs carry the official wording.
- Every image has alt text. Tables stay narrow enough to read on a phone.
- File names are lowercase kebab-case throughout.

## Release strategy

The repository uses semantic-flavored releases recorded in [CHANGELOG.md](../CHANGELOG.md):

- **Major**: structural reorganization, or coverage of a new certification program area
- **Minor**: new documents, new mirrored PDFs, updated exam guide versions
- **Patch**: corrections, refreshed dates, link fixes

Tag releases as `vX.Y.Z`. A release is warranted whenever the mirrored PDFs change or a certification's facts change, so that anyone consuming the repository can pin a known-good state.

## Repository settings worth preserving

- Issues use the three templates (broken link or error, outdated content, resource suggestion); blank issues are disabled to keep reports actionable.
- Discussions are enabled and seeded; the participation rules live in [CONTRIBUTING.md](../CONTRIBUTING.md#discussions). The non-negotiable rule is that real exam content is never shared, per the exam NDA.
- Workflows: lint (markdownlint and codespell) and link checking (lychee) run on pull requests, so contributions are self-checking.
- Dependabot updates the pinned workflow actions.

## Takedown stance

The mirrored PDFs are Anthropic's property, republished here for candidate convenience with full attribution. If Anthropic or its representatives request removal, remove the files promptly, leave the source links in place, and note the change in the changelog.

---

[Repository index](../README.md)
