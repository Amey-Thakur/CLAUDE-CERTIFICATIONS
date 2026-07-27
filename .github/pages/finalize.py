#!/usr/bin/env python3
"""Inject Open Graph and Twitter card tags into the built site.

MkDocs Material emits a description meta tag but no social card tags, so links
shared on LinkedIn, Slack, or X would render without a preview image. This adds
them per page, reusing the title and description already in the HTML.
Run after `mkdocs build`. Standard library only.
"""

import html
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent.parent / "_site"
BASE = "https://amey-thakur.github.io/CLAUDE-CERTIFICATIONS"
IMAGE = f"{BASE}/assets/social-preview.png"

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S)
DESC_RE = re.compile(r'<meta name="description" content="(.*?)"', re.S)


def main() -> int:
    if not SITE.exists():
        raise SystemExit("_site not found. Run mkdocs build first.")

    patched = 0
    for page in SITE.rglob("*.html"):
        text = page.read_text(encoding="utf-8")
        if 'property="og:' in text:
            continue

        title_match = TITLE_RE.search(text)
        desc_match = DESC_RE.search(text)
        title = html.escape(html.unescape(title_match.group(1).strip())) if title_match else "Claude Certifications"
        description = desc_match.group(1) if desc_match else ""

        relative = page.relative_to(SITE).as_posix()
        url = f"{BASE}/" if relative == "index.html" else f"{BASE}/{relative}"

        tags = (
            f'<meta property="og:type" content="website">\n'
            f'<meta property="og:site_name" content="Claude Certifications">\n'
            f'<meta property="og:title" content="{title}">\n'
            f'<meta property="og:description" content="{description}">\n'
            f'<meta property="og:image" content="{IMAGE}">\n'
            f'<meta property="og:url" content="{url}">\n'
            f'<meta name="twitter:card" content="summary_large_image">\n'
            f'<meta name="twitter:title" content="{title}">\n'
            f'<meta name="twitter:description" content="{description}">\n'
            f'<meta name="twitter:image" content="{IMAGE}">\n'
        )
        page.write_text(text.replace("</head>", tags + "</head>", 1), encoding="utf-8")
        patched += 1

    print(f"social tags added to {patched} pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
