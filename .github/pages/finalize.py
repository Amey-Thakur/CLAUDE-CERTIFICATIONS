#!/usr/bin/env python3
"""Inject Open Graph, Twitter card, and JSON-LD structured data into the built site.

MkDocs Material emits a description meta tag but no social card tags, so links
shared on LinkedIn, Slack, or X would render without a preview image. This adds
them per page, reusing the title and description already in the HTML.
Run after `mkdocs build`. Standard library only.
"""

import html
import json
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent.parent / "_site"
BASE = "https://amey-thakur.github.io/CLAUDE-CERTIFICATIONS"
IMAGE = f"{BASE}/assets/social-preview.png"

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S)

AUTHOR = {"@type": "Person", "name": "Amey Thakur", "url": "https://github.com/Amey-Thakur"}
PUBLISHER = {"@type": "Organization", "name": "Claude Certifications",
             "url": BASE, "logo": {"@type": "ImageObject", "url": f"{BASE}/assets/logos/claude-symbol.svg"}}

# One course entry per exam, so search engines can surface them individually.
EXAMS = [
    ("associate-foundations/index.html", "Claude Certified Associate, Foundations", "CCAO-F"),
    ("developer-foundations/index.html", "Claude Certified Developer, Foundations", "CCDV-F"),
    ("architect-foundations/index.html", "Claude Certified Architect, Foundations", "CCAR-F"),
    ("architect-professional/index.html", "Claude Certified Architect, Professional", "CCAR-P"),
]

FAQ_RE = re.compile(r"<p><strong>(.*?)</strong>(.*?)</p>", re.S)
TAG_RE = re.compile(r"<[^>]+>")


def text_of(fragment, limit=320):
    clean = html.unescape(TAG_RE.sub("", fragment)).strip()
    clean = re.sub(r"\s+", " ", clean)
    return clean[:limit]


def structured_data(relative, url, title, description, text):
    """The schema a page qualifies for, as a JSON-LD graph."""
    nodes = []

    if relative == "index.html":
        nodes.append({
            "@type": "WebSite", "@id": f"{BASE}/#website", "url": f"{BASE}/",
            "name": "Claude Certifications", "description": description,
            "author": AUTHOR, "publisher": PUBLISHER, "inLanguage": "en",
        })
        for path, name, code in EXAMS:
            nodes.append({
                "@type": "Course", "url": f"{BASE}/{path}", "name": name,
                "description": f"Study guide, blueprint, practice questions, and cheat sheet for the "
                               f"{name} certification exam ({code}) from Anthropic.",
                "courseCode": code, "provider": PUBLISHER, "author": AUTHOR,
                "isAccessibleForFree": True, "inLanguage": "en",
                "about": {"@type": "Thing", "name": "Anthropic Claude certification"},
                "hasCourseInstance": {"@type": "CourseInstance",
                                      "courseMode": "online", "courseWorkload": "PT20H"},
            })
    else:
        nodes.append({
            "@type": "TechArticle", "@id": f"{url}#article", "url": url,
            "headline": title, "description": description,
            "author": AUTHOR, "publisher": PUBLISHER, "inLanguage": "en",
            "isAccessibleForFree": True,
            "isPartOf": {"@id": f"{BASE}/#website"},
        })

    # The FAQ page carries question-and-answer pairs search engines can surface.
    if relative == "guide/faq.html":
        pairs = []
        for q, a in FAQ_RE.findall(text):
            question, answer = text_of(q, 160), text_of(a)
            if question and answer and len(answer) > 30:
                pairs.append({"@type": "Question", "name": question,
                              "acceptedAnswer": {"@type": "Answer", "text": answer}})
        if pairs:
            nodes.append({"@type": "FAQPage", "@id": f"{url}#faq", "mainEntity": pairs[:25]})

    crumbs = [{"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"}]
    parts = relative.split("/")
    if len(parts) > 1:
        crumbs.append({"@type": "ListItem", "position": 2, "name": parts[0].replace("-", " ").title(),
                       "item": f"{BASE}/{parts[0]}/"})
    crumbs.append({"@type": "ListItem", "position": len(crumbs) + 1, "name": title, "item": url})
    nodes.append({"@type": "BreadcrumbList", "itemListElement": crumbs})

    return json.dumps({"@context": "https://schema.org", "@graph": nodes},
                      ensure_ascii=False, separators=(",", ":"))
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
        ld = structured_data(relative, url, html.unescape(title), html.unescape(description), text)
        tags += '<script type="application/ld+json">' + ld + '</script>' + chr(10)

        page.write_text(text.replace("</head>", tags + "</head>", 1), encoding="utf-8")
        patched += 1

    print(f"social tags and structured data added to {patched} pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
