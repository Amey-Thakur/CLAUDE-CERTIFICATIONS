#!/usr/bin/env python3
"""Generate a flashcard deck from the repository's own facts and rules.

Writes a tab-separated file that Anki, Quizlet, and RemNote all import
directly, plus a readable markdown version. Cards come from the exam facts,
the domain weights, the cheat sheet rules, and the glossary, so the deck stays
consistent with the documentation instead of being maintained separately.

    python .github/scripts/build_flashcards.py

Standard library only.
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_images import ASSETS, CERTS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
TSV = ROOT / "flashcards.tsv"
JSON_OUT = ASSETS / "flashcards.json"
MD = ROOT / "guide" / "flashcards.md"

NAMES = {
    "associate-foundations": "Associate – Foundations",
    "developer-foundations": "Developer – Foundations",
    "architect-foundations": "Architect – Foundations",
    "architect-professional": "Architect – Professional",
}


def exam_cards():
    for cert in CERTS:
        name = NAMES[cert["slug"]]
        tag = cert["slug"]
        yield (f"{name}: exam code", cert["code"], f"facts {tag}")
        yield (f"{name}: how many items", cert["items"], f"facts {tag}")
        yield (f"{name}: list fee before partner discount", cert["fee"], f"facts {tag}")
        heaviest, weight = cert["domains"][0]
        yield (f"{name}: heaviest domain and its weight", f"{heaviest} at {weight}%", f"blueprint {tag}")
        lightest, lweight = cert["domains"][-1]
        yield (f"{name}: lightest domain and its weight", f"{lightest} at {lweight}%", f"blueprint {tag}")
        order = " → ".join(f"{n} {w}%" for n, w in cert["domains"])
        yield (f"{name}: domains in weight order", order, f"blueprint {tag}")
        yield (f"{name}: who is it for", cert["audience"], f"facts {tag}")


def cloze(rule):
    """Hide the half of a rule that carries its point, so the prompt cannot
    answer itself. Cuts at the rule's own punctuation where it has any."""
    body = rule.rstrip(".")
    for mark in (": ", "; ", ", "):
        if mark in body:
            head, tail = body.split(mark, 1)
            return f"{head}{mark.strip()} ...", tail.strip()
    words = body.split()
    cut = max(2, round(len(words) * 0.55))
    return " ".join(words[:cut]) + " ...", " ".join(words[cut:])


def rule_cards():
    """Each cheat sheet rule becomes a prompt about the judgment it encodes.

    A rule that explains itself is asked as a why question, since the reasoning
    is the part worth holding. A rule that only states itself is asked as a
    cloze, so recalling it takes recall rather than reading.
    """
    for cert in CERTS:
        tag = cert["slug"]
        name = NAMES[cert["slug"]]
        for rule in cert["rules"]:
            if ". " in rule:
                claim, explanation = rule.split(". ", 1)
                yield (f"{name}: {claim}. Why?", explanation, f"rules {tag}")
            else:
                head, _ = cloze(rule)
                yield (f"{name}: finish the rule: {head}", rule, f"rules {tag}")


def shared_cards():
    return [
        ("Passing score on every Claude certification exam", "720 on a scaled range of 100 to 1,000", "facts shared"),
        ("Time limit on every Claude certification exam", "120 minutes, with about 135 minutes of total seat time", "facts shared"),
        ("How long is a Claude credential valid", "12 months from the date you earn it", "policy shared"),
        ("What does on-time renewal involve", "A free, open-book, non-proctored assessment on Anthropic Partner Academy, retakable as often as needed", "policy shared"),
        ("What happens if a credential lapses", "You must pass the full exam again at full fee", "policy shared"),
        ("Retake waiting periods after failed attempts", "14 days after the first, 30 after the second, 90 after the third", "policy shared"),
        ("Maximum attempts per exam per rolling 12 months", "Four", "policy shared"),
        ("Free cancellation or reschedule window", "At least 24 hours before the appointment; inside that, the fee is forfeited", "policy shared"),
        ("Who delivers the exams", "Pearson VUE, online proctored through OnVUE or at a test center", "facts shared"),
        ("Where does the digital badge come from", "Credly, by email after a pass", "facts shared"),
        ("Which exam does not count toward partner tier eligibility", "Claude Certified Associate", "facts shared"),
        ("Partner tier discounts on exam fees", "Select, Preferred, and Global Premier partners receive 50% off, applied at checkout", "facts shared"),
        ("How is the exam scored, in one phrase", "Criterion-referenced: against a fixed standard, not against other candidates", "policy shared"),
        ("What does the score report show beyond pass or fail", "The scaled score and percent-correct per domain", "policy shared"),
        ("Is there an official practice exam", "No. The previous platform's was retired in the Pearson migration; the exam guides' sample questions are the only official items", "policy shared"),
        ("What is the authoritative scope of an exam", "The blueprint in its official exam guide; anything outside it is not tested", "policy shared"),
        ("How many scenarios does Architect Foundations present, and from how many", "Four, drawn from a published bank of six", "facts architect-foundations"),
        ("Are the exams open book", "No. No notes, documentation, translation tools, or AI assistants", "policy shared"),
        ("Who may currently sit these exams", "People at Claude Partner Network organizations, registering with a recognized company email", "policy shared"),
        ("How long do partner email domain record changes take", "7 to 10 days, so resolve them before you plan to sit", "policy shared"),
        ("What does the exam NDA cover", "Questions, answer options, and scenarios, explicitly including study groups and online forums", "policy shared"),
        ("Where can you take the official courses without a partner account", "The public Claude Academy; every course is free there", "facts shared"),
    ]


def glossary_cards():
    text = (ROOT / "guide" / "glossary.md").read_text(encoding="utf-8")
    for row in re.finditer(r"^\| ([^|]+) \| ([^|]+) \|$", text, re.M):
        term, meaning = row.group(1).strip(), row.group(2).strip()
        if term in ("Term", "---") or term.startswith("---"):
            continue
        meaning = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", meaning)
        yield (f"Glossary: {term}", meaning, "glossary shared")


def clean(value):
    return " ".join(value.replace("\t", " ").split())


def main() -> int:
    cards = []
    for source in (exam_cards(), rule_cards(), shared_cards(), glossary_cards()):
        for front, back, tags in source:
            cards.append((clean(front), clean(back), tags))

    seen, unique = set(), []
    for card in cards:
        if card[0] not in seen:
            seen.add(card[0])
            unique.append(card)

    TSV.write_text("\n".join("\t".join(c) for c in unique) + "\n", encoding="utf-8")
    print(f"{TSV.name}: {len(unique)} cards")

    # The website's flip cards read this; the TSV stays the portable export.
    JSON_OUT.write_text(json.dumps(
        {"cards": [{"front": f, "back": b, "tags": tg.split()} for f, b, tg in unique]},
        indent=1) + chr(10), encoding="utf-8")
    print(f"{JSON_OUT.name}: written")

    groups = {}
    for front, back, tags in unique:
        groups.setdefault(tags.split()[0], []).append((front, back))

    titles = {"facts": "Exam facts", "blueprint": "Blueprints and weights",
              "rules": "The rules that decide questions", "policy": "Policies and scoring",
              "glossary": "Glossary"}
    widget = (Path(__file__).resolve().parent.parent / "pages" / "flashcards-widget.html").read_text(encoding="utf-8")
    body = [
        "# Flashcards",
        "",
        f"Every fact, weight, rule, and term in this repository as a deck of {len(unique)} cards. Turn them here, "
        "or take the file and study them anywhere.",
        "",
        widget.rstrip(),
        "",
        "## Take the deck with you",
        "",
        "[flashcards.tsv](../flashcards.tsv) imports directly into Anki, Quizlet, or RemNote: three tab-separated "
        "columns, front, back, and tags, so you can study one certification or one topic at a time.",
        "",
        "```text",
        "https://github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS/raw/main/flashcards.tsv",
        "```",
        "",
        "> [!TIP]\n> In Anki, choose File, then Import, select the file, set the field separator to Tab, and map the "
        "third column to Tags. Filter by a tag such as `developer-foundations` or `policy` to drill one area.",
        "",
        "![A card, front face](../.github/assets/flashcard-front.png)",
        "",
        "![The same card turned over](../.github/assets/flashcard-back.png)",
        "",
        "## Every card in writing",
        "",
        "The full deck below, for reading, printing, or checking one fact quickly. It is generated from the same "
        "source as the rest of the documentation, so it cannot drift out of date.",
        "",
    ]
    for key in ("facts", "blueprint", "rules", "policy", "glossary"):
        rows = groups.get(key, [])
        if not rows:
            continue
        body += [f"## {titles[key]}", "", "| Front | Back |", "| --- | --- |"]
        body += [f"| {f.replace('|', '·')} | {b.replace('|', '·')} |" for f, b in rows]
        body += [""]
    body += ["---", "", "Facts drawn from the official Anthropic exam guides. "
             "[Repository index](../README.md)", ""]
    MD.write_text("\n".join(body), encoding="utf-8")
    print(f"{MD.name}: written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
