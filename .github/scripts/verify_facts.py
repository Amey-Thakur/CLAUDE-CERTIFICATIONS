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

# Published on Partner Academy, not in any mirrored PDF.
UNVERIFIABLE_HERE = [
    "retake intervals of 14, 30 and 90 days",
    "four attempts per rolling 12 months",
    "credential validity of 12 months",
    "free renewal assessment",
    "Credly badging and Pearson VUE delivery",
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

    print()
    for p in problems:
        print(f"  FAIL  {p}")
    if problems:
        print(f"\n  {len(problems)} disagreement(s) with the official guides.")
        return 1

    print(f"  {checked} published figures checked, all present and matching.")
    print("\n  Not checkable from the mirrored PDFs, confirm on Partner Academy:")
    for item in UNVERIFIABLE_HERE:
        print(f"    - {item}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
