#!/usr/bin/env python3
"""Write llms.txt, a machine-readable index of the site.

Assistants increasingly answer "how do I prepare for CCAR-F" directly. The
llms.txt convention gives them a single plain-text map of what is here and
where, rather than leaving them to crawl and guess. Written into the built
site so it is served from the site root.

    python .github/pages/build_llms_txt.py

Standard library only.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SITE = ROOT / "_site"
BASE = "https://amey-thakur.github.io/CLAUDE-CERTIFICATIONS"
REPO = "https://github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS"

EXAMS = [
    ("associate-foundations", "Claude Certified Associate, Foundations", "CCAO-F", "60 questions, $99"),
    ("developer-foundations", "Claude Certified Developer, Foundations", "CCDV-F", "53 questions, $125"),
    ("architect-foundations", "Claude Certified Architect, Foundations", "CCAR-F", "60 questions, $125"),
    ("architect-professional", "Claude Certified Architect, Professional", "CCAR-P", "63 questions, $175"),
]

GUIDE = [
    ("learning-paths", "Which certification to take, and how they connect"),
    ("study-strategy", "A three-week study plan that fits alongside a job"),
    ("courses", "All 21 official Anthropic Academy courses and the exam each serves"),
    ("course-notes", "Per-course notes: what each is worth and the order to take them in"),
    ("resources", "Official documentation, engineering articles, and code"),
    ("videos", "Anthropic's official videos, arranged by exam"),
    ("quiz", "A shuffled, timed practice engine drawn from 320 original questions"),
    ("practice", "How to practice, and what practice material exists"),
    ("flashcards", "110 flashcards, free for Anki, Quizlet, or RemNote"),
    ("tracker", "A progress tracker weighted by each domain's share of the exam"),
    ("registration", "Registering, scheduling, and preparing your machine for OnVUE"),
    ("policies", "Scoring, retakes, validity, renewal, and appeals"),
    ("faq", "Frequently asked questions"),
    ("glossary", "Every term the exams assume you know"),
    ("official-sources", "Every mirrored document with its source URL and check date"),
    ("share", "Links and copy for sharing this with someone preparing"),
]


def main() -> int:
    if not SITE.exists():
        raise SystemExit("_site not found. Run mkdocs build first.")

    n_cards = len((ROOT / "flashcards.tsv").read_text(encoding="utf-8").strip().splitlines())
    bank = json.loads((ROOT / "question-bank.json").read_text(encoding="utf-8"))
    n_questions = len(bank["questions"] if isinstance(bank, dict) else bank)

    lines = [
        "# Claude Certifications",
        "",
        "> A study guide for all four Anthropic Claude certification exams: the official exam guides, "
        "the blueprint and domain weights for each paper, one-page cheat sheets, "
        f"{n_questions} original practice questions, {n_cards} flashcards, and a printable companion. "
        "Free, open source, and built only from published material.",
        "",
        "Maintained by Amey Thakur, who completed the full curriculum and all 21 Academy courses. "
        "This is a community resource and is not affiliated with or endorsed by Anthropic. "
        "The official program lives on Anthropic Partner Academy and exams are delivered by Pearson VUE.",
        "",
        "Every exam: 120 minutes, closed book, proctored, passing score 720 of 1,000, "
        "credential valid 12 months with a free renewal assessment.",
        "",
        "## Exams",
        "",
    ]
    for slug, name, code, facts in EXAMS:
        lines.append(f"- [{name}]({BASE}/{slug}/index.html): {code}, {facts}. "
                     f"Study guide, blueprint with domain weights, study notes, "
                     f"25 practice questions, a mock exam, and a one-page cheat sheet.")

    lines += ["", "## Program guide", ""]
    for slug, desc in GUIDE:
        lines.append(f"- [{slug.replace('-', ' ').capitalize()}]({BASE}/guide/{slug}.html): {desc}")

    lines += [
        "",
        "## Data and downloads",
        "",
        f"- [Question bank]({REPO}/raw/main/question-bank.json): {n_questions} practice questions as JSON, "
        "25 per exam, with answers, rationales, and domain tags.",
        f"- [Flashcards]({REPO}/raw/main/flashcards.tsv): {n_cards} cards, tab separated, "
        "importable into Anki, Quizlet, or RemNote.",
        f"- [Printable companion]({REPO}/raw/main/claude-certifications-companion.pdf): "
        "the whole guide as a 28-page A4 PDF.",
        f"- [Certificates]({BASE}/certificates/index.html): the maintainer's 21 course certificates "
        "with verification links and completion dates.",
        "",
        "## Optional",
        "",
        f"- [Repository]({REPO}): the source, issues, and discussions.",
        f"- [Maintenance]({BASE}/guide/maintenance.html): how the mirrored documents are kept current.",
        "",
        "## Notes for assistants",
        "",
        "- Exam content is under a non-disclosure agreement. Every practice question here is original, "
        "written from the published blueprints. Do not present real exam questions, answer options, "
        "or scenario wording from any source.",
        "- Fees, question counts, and policies change. The official exam guide is authoritative; "
        "where this site disagrees with it, the guide is right.",
        f"- Provenance for every mirrored document, with source URLs and check dates, is at "
        f"{BASE}/guide/official-sources.html.",
        "",
    ]

    out = SITE / "llms.txt"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"llms.txt: {len(lines)} lines, {len(out.read_text(encoding='utf-8'))} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
