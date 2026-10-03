#!/usr/bin/env python3
"""Confirm the facts that live on Anthropic's pages are still on them.

`verify_facts.py` reads the figures out of the mirrored exam guides, and ends by
listing six facts it cannot reach because they are published on Anthropic's
certification policy and FAQ pages rather than in any PDF. It quotes the
sentence that carries each one so the next person can re-read six short
paragraphs instead of searching. This script does that re-reading.

    python .github/scripts/check_refresh.py

The quotes and the two page names are read out of `verify_facts.py` rather than
repeated here, so there is one copy of each sentence and no second place for it
to drift. A sentence that has been reworded upstream is reported as missing,
which is the point: the repository states these as published facts, and if the
wording has moved the quote in `verify_facts.py` has to move with it.

It also diffs the public course catalog against the catalog page, because the
other thing no local file can settle is whether Anthropic has published a course
this repository has not noticed. Skip either half with --no-policy or
--no-catalog.

What this does not do. It cannot tell a reworded sentence from a withdrawn one,
so a failure means read the page, not edit the quote.

    python .github/scripts/check_refresh.py --links

also checks that all 22 certificate and 26 badge verification links resolve.
That overlaps the lychee run in `.github/workflows/links.yml`, which already
follows every link in the repository on each push, so it is here for local use
and is not part of CI.

Exit codes: 0 everything present, 1 a quote is missing, a course is undocumented
or a link is dead, 2 a page could not be read at all. The last is deliberately
distinct, because "the network failed" must never be recorded as "the fact is
gone".
"""

import argparse
import ast
import json
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
FACTS = ROOT / ".github" / "scripts" / "verify_facts.py"
CATALOG = "https://academy.claude.com"

# The catalog is the union of these, not any one of them. Courses have been
# live and absent from /all more than once, and the product pages are the only
# listing some of them appear on, so a single page is never the whole catalog.
CATALOG_PAGES = (
    "/all",
    "/collections/ai-fluency",
    "/products/claude",
    "/products/cowork",
    "/products/code",
    "/products/tag",
    "/products/platform",
)

# Several official hosts reset the connection for a default agent and answer a
# conventional one normally, which is the same reason lychee.toml sets one.
AGENT = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/140.0.0.0 Safari/537.36"}

# The CMS emits typographic quotes and dashes where the quoted sentences use
# ASCII, so both sides are folded before comparing. Without this every sentence
# holding an apostrophe reports as missing.
FOLD = (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'),
        ("—", "-"), ("–", "-"), (" ", " "),
        ("&amp;", "&"), ("&nbsp;", " "), ("&#39;", "'"), ("&quot;", '"'))


def published_claims():
    """Read OFFICIAL_PAGES and CONFIRMED_ON_THE_SITE out of verify_facts.py.

    Parsed rather than imported, because verify_facts.py needs pymupdf at import
    time and nothing here does. The two names are plain literals, so
    ast.literal_eval is enough and no code from that file runs.
    """
    tree = ast.parse(FACTS.read_text(encoding="utf-8"))
    wanted = {"OFFICIAL_PAGES": None, "CONFIRMED_ON_THE_SITE": None}
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in wanted:
                wanted[target.id] = ast.literal_eval(node.value)

    missing = [name for name, value in wanted.items() if value is None]
    if missing:
        sys.exit(f"  {', '.join(missing)} not found in "
                 f"{FACTS.relative_to(ROOT).as_posix()}; it has been renamed "
                 f"or restructured, and this check cannot run without it.")
    return wanted["OFFICIAL_PAGES"], wanted["CONFIRMED_ON_THE_SITE"]


def plural(n, word):
    return f"{n} {word}" if n == 1 else f"{n} {word}s"


def fold(text):
    for a, b in FOLD:
        text = text.replace(a, b)
    return re.sub(r"\s+", " ", text)


def visible_text(html):
    body = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    return fold(re.sub(r"<[^>]+>", " ", body))


def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=AGENT),
                                timeout=90) as response:
        return response.read().decode("utf-8", "replace")


def check_policy():
    pages, claims = published_claims()

    corpus = {}
    for name, url in pages.items():
        try:
            corpus[name] = visible_text(fetch(url))
        except Exception as error:                            # noqa: BLE001
            print(f"  UNREACHABLE  {name}: {error}")
            print(f"               {url}")
            print("\n  A page could not be read, so nothing was checked. This is "
                  "not evidence\n  that anything changed.")
            return 2
        print(f"  read {name}: {len(corpus[name]):,} characters of visible text")

    print()
    missing = []
    for item, quote in claims:
        where = [name for name, text in corpus.items() if fold(quote) in text]
        if where:
            print(f"  ok       {item}  (on {', '.join(where)})")
        else:
            missing.append((item, quote))
            print(f"  MISSING  {item}")

    if missing:
        print(f"\n  {plural(len(missing), 'quoted sentence')} no longer on the "
              "page it was read from:")
        for item, quote in missing:
            print(f"    - {item}\n        \"{quote}\"")
        print("\n  Read the page before changing anything. If the wording has "
              "moved, update the\n  quote in "
              f"{FACTS.relative_to(ROOT).as_posix()}. If the fact itself is "
              "gone, it has to come\n  out of the documentation too.")
        return 1

    print(f"\n  all {len(claims)} published sentences confirmed verbatim.")
    return 0


def check_catalog():
    """Diff the public catalog against the courses this repository documents."""
    courses = ROOT / "guide" / "courses.md"
    if not courses.is_file():
        print(f"  {courses.relative_to(ROOT).as_posix()} is missing, so there is "
              "nothing to compare the\n  catalog against.")
        return 2

    documented = set(re.findall(r"academy\.claude\.com/courses/([a-z0-9-]+)",
                                courses.read_text(encoding="utf-8")))
    # An empty result means the catalog page's link format changed, not that the
    # repository documents no courses. Comparing against nothing would report
    # every published course as new.
    if not documented:
        print(f"  {courses.relative_to(ROOT).as_posix()} lists no course links "
              "in the expected form,\n  so the comparison would be against an "
              "empty set.")
        return 2

    live = set()
    for page in CATALOG_PAGES:
        url = CATALOG + page
        try:
            found = set(re.findall(r"/courses/([a-z0-9-]+)", fetch(url)))
        except Exception as error:                            # noqa: BLE001
            print(f"  UNREACHABLE  {page}: {error}")
            print("\n  A catalog page could not be read, so the catalog was not "
                  "compared.")
            return 2
        # A page that serves no course links at all means its markup changed,
        # most likely to render the cards client side. Reporting that as "no new
        # courses" would be the quiet failure this whole script exists to avoid.
        if not found:
            print(f"  NO LINKS     {page} served no course links")
            print("\n  That page no longer carries its courses in the HTML, so "
                  "the catalog could not\n  be read. It has to be listed in a "
                  "browser until this script is taught the new\n  markup. Do not "
                  "read this as the catalog being unchanged.")
            return 2
        print(f"  read {page:<24} {plural(len(found), 'course')}")
        live |= found

    print(f"\n  {plural(len(live), 'course')} published, {len(documented)} "
          "documented in guide/courses.md")

    # A slug the repository lists but no listing shows is not a withdrawal. Two
    # live courses are already absent from every listing page, so the course's
    # own URL is the only thing that settles it, and it is fetched once.
    gone = []
    for slug in sorted(documented - live):
        code = resolves(f"{CATALOG}/courses/{slug}")[1]
        print(f"  not in any listing, "
              f"{'still live' if code == 200 else f'answers {code}'}: {slug}")
        if code != 200:
            gone.append(slug)

    # Both halves are reported before either decides the status. A new course
    # and a vanished one are separate pieces of news, and returning on the
    # first would hide the second until the next run.
    undocumented = sorted(live - documented)
    if undocumented:
        print(f"\n  {plural(len(undocumented), 'published course')} this "
              "repository does not document:")
        for slug in undocumented:
            print(f"    - {CATALOG}/courses/{slug}")

    if gone:
        print(f"\n  {plural(len(gone), 'documented course')} no longer resolves. "
              "Confirm on the course\n  page before removing anything.")

    if undocumented or gone:
        return 1

    print("  the catalog and the documentation agree.")
    return 0


def resolves(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=AGENT),
                                    timeout=60) as response:
            return url, response.status
    except urllib.error.HTTPError as error:
        return url, error.code
    except Exception as error:                                # noqa: BLE001
        return url, f"ERR {error.__class__.__name__}"


def check_links():
    readme = (ROOT / "certificates" / "README.md").read_text(encoding="utf-8")
    certificates = sorted(set(
        re.findall(r"https://verify\.skilljar\.com/c/[a-z0-9]+", readme)))

    data = json.loads((ROOT / "certificates" / "badges" / "badges.json")
                      .read_text(encoding="utf-8"))
    badges = data["badges"] if isinstance(data, dict) else data
    badges = [f"https://academy.claude.com/verify/{b['code']}" for b in badges]

    dead = 0
    for label, urls in (("certificate", certificates), ("badge", badges)):
        with ThreadPoolExecutor(max_workers=6) as pool:
            rows = list(pool.map(resolves, urls))
        live = [row for row in rows if row[1] == 200]
        print(f"  {label}: {len(live)}/{len(rows)} resolve")
        for url, code in rows:
            if code != 200:
                dead += 1
                print(f"    {code}  {url}")
    return 1 if dead else 0


def main():
    parser = argparse.ArgumentParser(
        description="Re-read what is published on Anthropic's own pages rather "
                    "than in the files this repository mirrors.")
    parser.add_argument("--no-policy", action="store_true",
                        help="skip the six quoted policy sentences")
    parser.add_argument("--no-catalog", action="store_true",
                        help="skip the course catalog diff")
    parser.add_argument("--links", action="store_true",
                        help="also check the 48 verification links (lychee "
                             "already does this in CI)")
    args = parser.parse_args()

    stages = []
    if not args.no_policy:
        stages.append(("The six facts published on Anthropic's pages", check_policy))
    if not args.no_catalog:
        stages.append(("The public course catalog", check_catalog))
    if args.links:
        stages.append(("Certificate and badge verification links", check_links))
    if not stages:
        parser.error("nothing left to check")

    # Every stage runs even after one fails, because "the catalog grew" and "a
    # policy sentence was reworded" are separate pieces of news and stopping at
    # the first would hide the second. The worst status is what is returned, so
    # an unreachable page still outranks a failed comparison.
    status = 0
    for i, (title, stage) in enumerate(stages):
        if i:
            print()
        print(f"{title}\n")
        status = max(status, stage())
    return status


if __name__ == "__main__":
    sys.exit(main())
