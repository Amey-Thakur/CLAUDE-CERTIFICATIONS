# Changelog

Notable changes to this repository. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and releases follow the strategy described in the [maintenance guide](guide/maintenance.md#release-strategy).

## [1.1.0] - 2026-07-27

### Added

- Documentation website at [amey-thakur.github.io/CLAUDE-CERTIFICATIONS](https://amey-thakur.github.io/CLAUDE-CERTIFICATIONS/), built with MkDocs Material and deployed from CI on every push
- Twenty-first certificate, AI Fluency for pK-12 Educators, with preview and verification link
- Certificate gallery with previews and Skilljar verification links for all courses
- Decision, troubleshooting, retake, and support-routing diagrams across the README and guide pages
- Citation metadata: CITATION.cff and codemeta.json
- Anthropic and Claude logo artwork from Wikimedia Commons, with attribution

### Changed

- Root reorganized: community files, assets, scripts, and tool configuration moved under .github, leaving certification folders, the guide, and certificates at the top level
- All commits are signed and follow a uniform message convention

## [1.0.0] - 2026-07-27

### Added

- One folder per certification (Associate – Foundations, Developer – Foundations, Architect – Foundations, Architect – Professional), each containing the study guide with the full exam blueprint and domain-weight chart, the official exam guide PDF, and the maintainer's study notes
- Mirrored official PDFs: all four exam guides (version 1.0, July 2026), the Anthropic Certification Exam Policy, the Certification Terms and Conditions, and the Exam Registration Guide, with provenance recorded in guide/official-sources.md
- Learning paths page covering the CPN learning path, per-certification prep courses, the public course catalog, and partner badges
- Registration and scheduling guide, including OnVUE system setup, the network domain allowlist, and the application shutdown list
- Certification policies summary and condensed FAQ, including the June 30, 2026 Pearson and Credly migration notes
- Study strategy with per-exam emphasis and checklists
- Maintainer's twenty-one Anthropic Academy course completion certificates with previews, issue dates, and verification links where issued
- Maintenance guide, resource update script, issue templates, pull request template, and CI for markdown lint, spell check, and link checking
