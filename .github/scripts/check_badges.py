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
    "nineteen": 19, "twenty": 20, "twenty-one": 21, "twenty-two": 22,
    "eighteen": 18, "seventeen": 17,
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
    word = spelled(n)
    checks = [
        ("README.md",
         re.compile(r"and \*\*(\d+)\*\* were issued as a digital completion badge"),
         str(n)),
        ("certificates/README.md",
         re.compile(r"^(\S+) courses were also issued as a digital completion badge", re.M),
         word.capitalize() if word else None),
        (".github/pages/index.md",
         re.compile(r"(\S+) courses were also issued as a digital completion badge"),
         word.capitalize() if word else None),
        (".github/pages/certificates-header.md",
         re.compile(r"(\S+) issued a completion badge"),
         word),
    ]
    for rel, pattern, expected in checks:
        text = (ROOT / rel).read_text(encoding="utf-8")
        m = pattern.search(text)
        if not m:
            problems.append(f"{rel}: could not find the badge count sentence")
            continue
        found = m.group(1)
        ok = found.lower() == str(expected).lower()
        print(f"  {rel}: prose says '{found}'{'' if ok else f' (expected {expected})'}")
        if not ok:
            problems.append(f"{rel} says '{found}', but there are {n} badges")

    for p in problems:
        print(f"  FAIL  {p}")
    if problems:
        print(f"\n  {len(problems)} disagreement(s).")
        return 1
    print(f"\n  all badge counts agree on {n}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
