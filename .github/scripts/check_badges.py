#!/usr/bin/env python3
"""Check that every stated badge count matches the badges that actually exist.

The Claude Academy badge count appears in five places: the badge files
themselves, two galleries, and three sentences of prose. When a badge is added
by hand, at least one of those gets missed. It has been missed twice.

So the count is derived from the directory, and every other place has to agree
with it.

    python .github/scripts/check_badges.py

Exits non-zero on any disagreement.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
BADGES = ROOT / "certificates" / "badges"

WORDS = {
    "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
    "twenty-one": 21, "twenty-two": 22, "twenty-three": 23,
    "twenty-four": 24, "twenty-five": 25, "twenty-six": 26,
}


def spelled(n):
    for word, value in WORDS.items():
        if value == n:
            return word
    return None


def main():
    files = sorted(p.stem for p in BADGES.glob("*.png"))
    n = len(files)
    problems = []
    print(f"  {n} badge images in {BADGES.relative_to(ROOT).as_posix()}")

    # Every badge file must be shown in both galleries, and both galleries must
    # show only badges that exist.
    galleries = {
        "README.md": re.compile(r'certificates/badges/([\w-]+)\.png'),
        "certificates/README.md": re.compile(r'(?<!certificates/)badges/([\w-]+)\.png'),
    }
    for rel, pattern in galleries.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        shown = sorted(set(pattern.findall(text)))
        missing = [f for f in files if f not in shown]
        extra = [s for s in shown if s not in files]
        print(f"  {rel}: {len(shown)} badges shown")
        if missing:
            problems.append(f"{rel} does not show: {', '.join(missing)}")
        if extra:
            problems.append(f"{rel} shows badges with no image: {', '.join(extra)}")

    # The prose counts, each of which has drifted at least once.
    #
    # What is counted is the number of badges, which since 1 September 2026 is
    # not the number of courses that have one: AI Fluency for Creative Work
    # issued twice, so twenty-three courses hold twenty-four badges. Both
    # numbers appear in these sentences and the earlier patterns, written when
    # they were the same number, read whichever came first. So the phrase
    # looked for is the count standing immediately before the word "badges".
    word = spelled(n)
    COUNT = re.compile(r"(\*\*\d+\*\*|[A-Za-z]+(?:-[A-Za-z]+)?)\s+badges\b")
    for rel in ("README.md", "certificates/README.md", ".github/pages/index.md",
                ".github/pages/certificates-header.md"):
        text = (ROOT / rel).read_text(encoding="utf-8")
        found = [m.group(1).strip("*") for m in COUNT.finditer(text)]
        wanted = {str(n), word or str(n)}
        if not found:
            problems.append(f"{rel}: no sentence states how many badges there are")
            continue
        agreeing = [f for f in found if f.lower() in wanted]
        shown = ", ".join(f"'{f}'" for f in dict.fromkeys(found))
        print(f"  {rel}: prose says {shown}"
              f"{'' if agreeing else f' (expected {n} or {word})'}")
        if not agreeing:
            problems.append(f"{rel} says {shown}, but there are {n} badges")

    for p in problems:
        print(f"  FAIL  {p}")
    if problems:
        print(f"\n  {len(problems)} disagreement(s).")
        return 1
    print(f"\n  all badge counts agree on {n}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
