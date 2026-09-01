#!/usr/bin/env python3
"""Check the repository's exam facts against the official PDFs it mirrors.

Every page here carries a "facts last verified" date. That date is a claim, and
bumping it without re-reading the sources would be the exact failure this
repository exists to avoid: a confident assertion nobody checked.

So this reads the figures straight out of the mirrored exam guides and compares
them to what the markdown says. Run it before touching any verification date.

    python .github/scripts/verify_facts.py

Needs pymupdf. Exits non-zero if any published figure is missing from the docs
or disagrees with them.

What is checked, and what is not. The exam guides carry the exam codes, item
counts, duration, cut score, fees and domain weights, so all of those are
compared. The retake intervals, the twelve-month validity and the renewal terms
are published on Partner Academy rather than in any mirrored PDF, so they cannot
be checked here; they are listed at the end as needing a human to look.
"""

import re
import sys
from pathlib import Path

try:
    import pymupdf
except ImportError:
    print("  pymupdf is required: pip install pymupdf")
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent.parent

TRACKS = {
    "associate-foundations": "CCAO-F",
    "developer-foundations": "CCDV-F",
    "architect-foundations": "CCAR-F",
    "architect-professional": "CCAR-P",
}

# Published on Partner Academy rather than in any mirrored PDF, so this script
# cannot reach them. They are not unverified: each was read off Anthropic's own
# certification policy page on 1 September 2026, and the sentence that carries
# it is quoted here so the next check knows what it is looking for.
#
#   https://anthropic-partners.skilljar.com/page/policies-certifications
#   https://anthropic-partners.skilljar.com/page/faq-certifications
#
# The claim that used to sit in this list, "four attempts per rolling 12
# months", was removed from the documentation on the same day: no official
# source publishes any maximum. The policy page gives the growing waiting
# periods and says the attempt count resets on a new exam version, and stops
# there. See guide/policies.md.
CONFIRMED_ON_THE_SITE = [
    ("retake intervals of 14, 30 and 90 days",
     "14 days after your first failed attempt, 30 days after your second, "
     "and 90 days after your third"),
    ("credential validity of 12 months",
     "Certifications are valid for 12 months from the date you earn them"),
    ("free renewal assessment",
     "you can renew it for free by passing an open-book online assessment on "
     "Anthropic Partner Academy"),
    ("Pearson VUE delivery",
     "Exams are delivered through Pearson VUE"),
    ("Credly badging",
     "On June 30, 2026, certification moved to Pearson for exam delivery and "
     "to Credly for digital badging"),
]


def text_of(pdf):
    return "\n".join(page.get_text() for page in pymupdf.open(pdf))


def official(track):
    """Pull the published figures out of one exam guide."""
    t = text_of(ROOT / track / "exam-guide.pdf")
    lines = [ln.strip() for ln in t.splitlines()]

    facts = {"code": None, "items": None, "minutes": None, "cut": None,
             "fee": None, "weights": []}

    m = re.search(r"\b(CC[A-Z]{2}-[FP])\b", t)
    facts["code"] = m.group(1) if m else None

    for i, ln in enumerate(lines):
        if ln == "Number of items":
            for nxt in lines[i + 1:i + 4]:
                if nxt.isdigit():
                    facts["items"] = int(nxt)
                    break
            break

    m = re.search(r"(\d+)\s*minutes", t)
    facts["minutes"] = int(m.group(1)) if m else None

    m = re.search(r"[Ss]caled score of (\d{3})", t)
    facts["cut"] = int(m.group(1)) if m else None

    m = re.search(r"\$\s?(\d+)\s*USD", t)
    facts["fee"] = int(m.group(1)) if m else None

    # Two shapes appear across the four guides: "Domain 1: Name (14%)" and a
    # table form carrying one decimal place.
    facts["weights"] = [float(x) for x in
                        re.findall(r"Domain \d+:[^(\n]{3,80}\((\d{1,2}(?:\.\d)?)%\)", t)]
    if not facts["weights"]:
        facts["weights"] = [float(x) for x in re.findall(
            r"Domain\s*\d[^\n]{0,70}?\|?\s*(\d{1,2}\.\d)%", t)]
    return facts


def docs_for(track):
    """Every markdown page that states facts for this track."""
    out = ""
    for name in ("README.md", "notes.md", "cheat-sheet.md"):
        p = ROOT / track / name
        if p.exists():
            out += p.read_text(encoding="utf-8")
    for extra in (ROOT / "README.md", ROOT / ".github" / "pages" / "index.md"):
        if extra.exists():
            out += extra.read_text(encoding="utf-8")
    return out


def shown(value, blob):
    """Is this figure written somewhere in the docs?"""
    s = f"{value:g}" if isinstance(value, float) else str(value)
    return re.search(rf"(?<![\d.]){re.escape(s)}(?![\d])", blob) is not None


def main():
    problems, checked = [], 0

    for track, expected_code in TRACKS.items():
        f = official(track)
        blob = docs_for(track)
        label = track.replace("-", " ")

        if f["code"] != expected_code:
            problems.append(
                f"{label}: guide reports code {f['code']}, repo expects {expected_code}")
        else:
            checked += 1

        for field, name in (("items", "item count"), ("minutes", "duration"),
                            ("cut", "cut score"), ("fee", "fee")):
            value = f[field]
            if value is None:
                problems.append(f"{label}: could not read the {name} from the guide")
                continue
            checked += 1
            if not shown(value, blob):
                problems.append(f"{label}: guide says {name} {value}, "
                                f"not found in the docs")

        if f["weights"]:
            total = round(sum(f["weights"]), 1)
            if not 99.0 <= total <= 101.0:
                problems.append(
                    f"{label}: published weights sum to {total}, not 100")
            for w in f["weights"]:
                checked += 1
                if not shown(w, blob):
                    problems.append(
                        f"{label}: weight {w:g}% is published but absent from the docs")
            print(f"  {label}: {expected_code}, {f['items']} items, "
                  f"{f['minutes']} min, cut {f['cut']}, ${f['fee']}, "
                  f"{len(f['weights'])} domains summing to {total}")
        else:
            print(f"  {label}: {expected_code}, {f['items']} items, "
                  f"{f['minutes']} min, cut {f['cut']}, ${f['fee']}, "
                  f"scenario-based, no published weights")

    # The structured data on the website publishes each exam's domains as
    # competencyRequired. Those names are read by search engines, so a typo
    # there is a wrong fact served to everybody, and nothing else checks them.
    try:
        sys.path.insert(0, str(ROOT / ".github" / "pages"))
        from finalize import COMPETENCIES  # noqa: PLC0415
    except Exception as e:  # noqa: BLE001
        problems.append(f"could not read COMPETENCIES from finalize.py: {e}")
    else:
        for track, code in TRACKS.items():
            published = [n.strip() for n in re.findall(
                r"Domain \d+:\s*([^(\n]{3,70}?)\s*[\(\n]",
                text_of(ROOT / track / "exam-guide.pdf"))]
            claimed = COMPETENCIES.get(code, [])
            if not published:
                continue
            checked += len(claimed)
            for name in claimed:
                if not any(name.lower() == p.lower() for p in published):
                    problems.append(
                        f"{track}: structured data claims domain '{name}', "
                        f"which the guide does not list")
            for p in published:
                if not any(p.lower() == c.lower() for c in claimed):
                    problems.append(
                        f"{track}: guide lists domain '{p}', missing from the "
                        f"structured data")

    print()
    for p in problems:
        print(f"  FAIL  {p}")
    if problems:
        print(f"\n  {len(problems)} disagreement(s) with the official guides.")
        return 1

    print(f"  {checked} published figures checked, all present and matching.")
    print("\n  Not in the mirrored PDFs. Read off Anthropic's certification "
          "policy and FAQ pages on 1 September 2026, and quoted in this file:")
    for item, quote in CONFIRMED_ON_THE_SITE:
        print(f"    - {item}")
        print(f"        \"{quote}\"")
    return 0


if __name__ == "__main__":
    sys.exit(main())
