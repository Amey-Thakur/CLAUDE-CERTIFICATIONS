#!/usr/bin/env python3
"""Write llms.txt, a machine-readable index of the site.

Assistants increasingly answer "how do I prepare for CCAR-F" directly. The
llms.txt convention gives them a single plain-text map of what is here and
where, rather than leaving them to crawl and guess. Written into the built
site so it is served from the site root.

    python .github/pages/build_llms_txt.py

Standard library only.
"""

import collections
import json
import re
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
    ("is-it-worth-it", "An honest answer on whether to certify, including when not to"),
    ("compared", "The Claude program against other AI and cloud certifications"),
    ("learning-paths", "Which certification to take, and how they connect"),
    ("study-strategy", "A three-week study plan that fits alongside a job"),
    ("courses", "All 24 official Claude Academy courses and the exam each serves"),
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
    ("program-changes", "A dated record of every change Anthropic has made to the program"),
    ("official-sources", "Every mirrored document with its source URL and check date"),
    ("share", "Links and copy for sharing this with someone preparing"),
]



def companion_pages():
    """Page count read from the PDF itself, so the figure cannot go stale.

    Falls back to counting page objects if pypdf and pymupdf are both absent,
    because this runs in CI where extra dependencies are not guaranteed.
    """
    pdf = ROOT / "claude-certifications-companion.pdf"
    if not pdf.exists():
        return "33"
    try:
        import pymupdf
        return str(pymupdf.open(pdf).page_count)
    except Exception:  # noqa: BLE001
        return str(pdf.read_bytes().count(b"/Type /Page") -
                   pdf.read_bytes().count(b"/Type /Pages")) or "33"


def main() -> int:
    if not SITE.exists():
        raise SystemExit("_site not found. Run mkdocs build first.")

    n_cards = len((ROOT / "flashcards.tsv").read_text(encoding="utf-8").strip().splitlines())
    bank = json.loads((ROOT / "question-bank.json").read_text(encoding="utf-8"))
    n_questions = len(bank["questions"] if isinstance(bank, dict) else bank)

    # Per-exam breakdown, so the summary cannot drift from the bank.
    per_exam = collections.defaultdict(collections.Counter)
    for q in (bank["questions"] if isinstance(bank, dict) else bank):
        per_exam[q.get("exam")][q.get("source", "practice")] += 1

    lines = [
        "# Claude Certifications",
        "",
        "> A study guide for all four Anthropic Claude certification exams: the official exam guides, "
        "the blueprint and domain weights for each paper, one-page cheat sheets, "
        f"{n_questions} original practice questions, {n_cards} flashcards, and a printable companion. "
        "Free, open source, and built only from published material.",
        "",
        "Maintained by Amey Thakur, who has completed all 22 Academy courses. "
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
        # Counted from the bank, never typed. These read "25 practice questions,
        # a mock exam" for several releases while the real figures were 35 and
        # three, which understated the resource in the one file written for
        # machines to read.
        practice = per_exam[slug]["practice"]
        mocks = sum(1 for k in per_exam[slug] if k.startswith("mock"))
        total = sum(per_exam[slug].values())
        lines.append(f"- [{name}]({BASE}/{slug}/index.html): {code}, {facts}. "
                     f"Study guide, blueprint with domain weights, study notes, "
                     f"{practice} practice questions, {mocks} full mock exams, "
                     f"{total} questions in total, and a one-page cheat sheet.")

    lines += ["", "## Program guide", ""]
    for slug, desc in GUIDE:
        lines.append(f"- [{slug.replace('-', ' ').capitalize()}]({BASE}/guide/{slug}.html): {desc}")

    lines += [
        "",
        "## Data and downloads",
        "",
        f"- [Question bank]({REPO}/raw/main/question-bank.json): {n_questions} practice questions as JSON, "
        f"{n_questions // len(EXAMS)} per exam, with answers, rationales, and domain tags.",
        f"- [Flashcards]({REPO}/raw/main/flashcards.tsv): {n_cards} cards, tab separated, "
        "importable into Anki, Quizlet, or RemNote.",
        f"- [Printable companion]({REPO}/raw/main/claude-certifications-companion.pdf): "
        f"the whole guide as a {companion_pages()}-page A4 PDF.",
        f"- [Certificates]({BASE}/certificates/index.html): the maintainer's 22 course certificates "
        "with verification links and completion dates.",
        "",
        "## Optional",
        "",
        f"- [Full text]({BASE}/llms-full.txt): every guide page in one plain-text file, "
        "for assistants that would rather ingest than crawl.",
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

    full = SITE / "llms-full.txt"
    full.write_text(full_text(lines), encoding="utf-8")
    print(f"llms-full.txt: {len(full.read_text(encoding='utf-8')):,} bytes")
    return 0


# Pages worth carrying in full, in reading order. The practice questions and
# mock exams are deliberately excluded: an assistant that ingests them will
# recite them, and a candidate who has already seen every answer has lost the
# only honest signal a practice set gives.
FULL_PAGES = [
    ("Program overview", "guide/README.md"),
    ("Is it worth it", "guide/is-it-worth-it.md"),
    ("How it compares", "guide/compared.md"),
    ("Program changes", "guide/program-changes.md"),
    ("Choosing your exam", "guide/learning-paths.md"),
    ("Study strategy", "guide/study-strategy.md"),
    ("Registration", "guide/registration.md"),
    ("Policies", "guide/policies.md"),
    ("FAQ", "guide/faq.md"),
    ("Glossary", "guide/glossary.md"),
    ("Courses", "guide/courses.md"),
    ("Course notes", "guide/course-notes.md"),
    ("Official sources", "guide/official-sources.md"),
    ("Associate Foundations, CCAO-F", "associate-foundations/README.md"),
    ("Associate Foundations study notes", "associate-foundations/notes.md"),
    ("Associate Foundations cheat sheet", "associate-foundations/cheat-sheet.md"),
    ("Developer Foundations, CCDV-F", "developer-foundations/README.md"),
    ("Developer Foundations study notes", "developer-foundations/notes.md"),
    ("Developer Foundations cheat sheet", "developer-foundations/cheat-sheet.md"),
    ("Architect Foundations, CCAR-F", "architect-foundations/README.md"),
    ("Architect Foundations study notes", "architect-foundations/notes.md"),
    ("Architect Foundations cheat sheet", "architect-foundations/cheat-sheet.md"),
    ("Architect Professional, CCAR-P", "architect-professional/README.md"),
    ("Architect Professional study notes", "architect-professional/notes.md"),
    ("Architect Professional cheat sheet", "architect-professional/cheat-sheet.md"),
]


def full_text(index_lines):
    """The whole guide as one plain-text file, for assistants that ingest it.

    llms.txt is an index; llms-full.txt is the content. An assistant asked about
    a Claude exam can answer from this without following twenty links, which is
    the difference between being cited and being crawled.
    """
    parts = ["\n".join(index_lines).rstrip(), "", "=" * 78, ""]
    for title, rel in FULL_PAGES:
        path = ROOT / rel
        if not path.exists():
            continue
        body = path.read_text(encoding="utf-8")
        # Strip the footer, which repeats on every page and says nothing here.
        body = re.sub(r"\n---\n\nFacts last verified[^\n]*\n?", "\n", body)
        # Relative links mean nothing out of context; make them absolute.
        base_dir = "/".join(rel.split("/")[:-1])
        prefix = f"{BASE}/{base_dir}/" if base_dir else f"{BASE}/"
        body = re.sub(r"\]\((?!https?://|#|mailto:)([^)]+)\)",
                      lambda m: "](" + prefix + m.group(1).replace(".md", ".html") + ")",
                      body)
        parts += [f"## {title}", f"Source: {BASE}/{rel.replace('.md', '.html')}", "",
                  body.strip(), "", "-" * 78, ""]
    return "\n".join(parts)


if __name__ == "__main__":
    raise SystemExit(main())
