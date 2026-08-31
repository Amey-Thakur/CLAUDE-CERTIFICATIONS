#!/usr/bin/env python3
"""Write the Claude Academy badge galleries from one list.

The same badges are shown in three places: the repository README, the
certificates page, and the website home page. Each was maintained by hand, and
each has been left a badge behind at least once, which is why check_badges.py
exists at all.

They are generated here instead, from certificates/badges/badges.json, into
three columns. Three divides the count evenly, so the grid is a full rectangle
with no short final row; a layout that leaves gaps looks like something is
missing even when nothing is.

    python .github/scripts/build_badges.py            # write the galleries
    python .github/scripts/build_badges.py --check    # fail if they are stale

Exits non-zero if a badge has no image, an image has no entry, or the count
does not divide into the column width.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
BADGES = ROOT / "certificates" / "badges"
DATA = BADGES / "badges.json"
COLUMNS = 3

START = "<!-- badges:start -->"
END = "<!-- badges:end -->"

# Where each gallery lives, how it reaches the images, and which of the two
# cell shapes it uses. The certificates page shows the verification code; the
# other two show the course name and a link.
GALLERIES = {
    "README.md": ("certificates/badges", "named"),
    "certificates/README.md": ("badges", "coded"),
    ".github/pages/index.md": ("certificates/badges", "named"),
}


def load():
    badges = json.loads(DATA.read_text(encoding="utf-8"))
    have = {p.stem for p in BADGES.glob("*.png")}
    want = {b["slug"] for b in badges}
    problems = []
    for slug in sorted(want - have):
        problems.append(f"{slug} is listed but has no image")
    for slug in sorted(have - want):
        problems.append(f"{slug}.png exists but is not listed")
    if len(badges) % COLUMNS:
        problems.append(
            f"{len(badges)} badges do not fill rows of {COLUMNS}; the gallery "
            f"would end on a short row of {len(badges) % COLUMNS}")
    return badges, problems


def cell(badge, prefix, shape):
    verify = f"https://academy.claude.com/verify/{badge['code']}"
    alt = (f"Claude Academy completion badge for {badge['title']}, "
           f"issued to Amey Thakur")
    width = f"{round(100 / COLUMNS)}%"
    img = (f'<a href="{verify}" title="Verify {badge["title"]} on Claude Academy">'
           f'<img src="{prefix}/{badge["slug"]}.png" width="100%" alt="{alt}"></a>')
    if shape == "coded":
        caption = (f'<br><sub><b>{badge["title"]}</b><br>'
                   f'<a href="{verify}">Verify</a> · '
                   f'<code>{badge["code"][:12]}…</code></sub>')
    else:
        caption = (f'<br><sub><b>{badge["title"]}</b><br>'
                   f'<a href="{verify}">Verify</a></sub>')
    return (f'<td align="center" width="{width}">\n{img}\n{caption}\n</td>')


def gallery(badges, prefix, shape):
    lines = ["<table>"]
    for i in range(0, len(badges), COLUMNS):
        lines.append("<tr>")
        for badge in badges[i:i + COLUMNS]:
            lines.append(cell(badge, prefix, shape))
        lines.append("</tr>")
    lines.append("</table>")
    return "\n".join(lines)


def main():
    check = "--check" in sys.argv
    badges, problems = load()
    for p in problems:
        print(f"  FAIL  {p}")
    if problems:
        return 1

    rows = len(badges) // COLUMNS
    print(f"  {len(badges)} badges, {rows} rows of {COLUMNS}")

    stale = []
    for rel, (prefix, shape) in GALLERIES.items():
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        if START not in text or END not in text:
            print(f"  FAIL  {rel} has no {START} / {END} markers")
            return 1
        head, rest = text.split(START, 1)
        _, tail = rest.split(END, 1)
        body = f"{START}\n\n{gallery(badges, prefix, shape)}\n\n{END}"
        new = head + body + tail
        if new == text:
            print(f"  {rel}: current")
            continue
        if check:
            stale.append(rel)
            print(f"  {rel}: STALE")
            continue
        path.write_text(new, encoding="utf-8")
        print(f"  {rel}: written")

    if stale:
        print(f"\n  {len(stale)} gallery(ies) stale. Run: "
              f"python .github/scripts/build_badges.py")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
