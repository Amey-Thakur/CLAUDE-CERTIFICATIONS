#!/usr/bin/env python3
"""Read each badge's issue date from its own verification page.

The date a badge was issued is printed on Anthropic's verification page for
that badge and nowhere else. It is not the course completion date: nineteen of
these were issued together when Claude Academy started issuing badges, months
after the courses themselves were finished.

The page is a JavaScript application, so the date is not in the HTML that
arrives; the page has to be run to see it. Each one is opened once and what it
says is written into badges.json beside the verification code it came from, so
nothing downstream has to visit twenty-one pages to know a date.

    python .github/scripts/read_badge_dates.py            # only what is missing
    python .github/scripts/read_badge_dates.py --all      # read every one again

Needs Playwright and Chrome.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
BADGES = ROOT / "certificates" / "badges" / "badges.json"
VERIFY = "https://academy.claude.com/verify/"

CHROME = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
ISSUED = re.compile(r"ISSUED\s+([A-Z]+)\s+(\d{1,2}),\s*(\d{4})", re.I)


def read(page, code):
    page.goto(VERIFY + code, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(800)
    m = ISSUED.search(page.inner_text("body"))
    if not m:
        return None
    month = m.group(1).capitalize()
    if month not in MONTHS:
        return None
    return f"{int(m.group(2))} {month} {m.group(3)}"


def main():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("  Playwright is not installed: pip install playwright")
        return 1

    again = "--all" in sys.argv
    badges = json.loads(BADGES.read_text(encoding="utf-8"))
    wanted = [b for b in badges if again or not b.get("issued")]
    if not wanted:
        print("  every badge already carries the date it was issued")
        return 0

    browser = next((c for c in CHROME if Path(c).exists()), None)
    read_ok = failed = 0
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=browser) if browser \
            else p.chromium.launch()
        page = b.new_page(viewport={"width": 1200, "height": 900})
        for badge in wanted:
            try:
                issued = read(page, badge["code"])
            except Exception as error:  # noqa: BLE001
                print(f"  {badge['title']}: {str(error)[:70]}")
                failed += 1
                continue
            if not issued:
                print(f"  {badge['title']}: the page states no issue date")
                failed += 1
                continue
            badge["issued"] = issued
            read_ok += 1
            print(f"  {issued:20} {badge['title']}", flush=True)
        b.close()

    BADGES.write_text(json.dumps(badges, indent=2, ensure_ascii=False) + "\n",
                      encoding="utf-8")
    dates = {}
    for badge in badges:
        if badge.get("issued"):
            dates[badge["issued"]] = dates.get(badge["issued"], 0) + 1
    spread = ", ".join(f"{n} on {when}" for when, n in
                       sorted(dates.items(), key=lambda kv: kv[0]))
    print(f"  {read_ok} read, {failed} that did not answer")
    print(f"  issued: {spread}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
