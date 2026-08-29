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

ANTHROPIC = {"@type": "Organization", "name": "Anthropic",
             "url": "https://www.anthropic.com"}

# One entry per exam, so search engines can surface them individually. The fee
# and item count are the published figures, checked against the official exam
# guides by verify_facts.py on every CI run, so this table cannot quietly drift
# away from the PDFs it claims to describe.
EXAMS = [
    ("associate-foundations/index.html", "Claude Certified Associate, Foundations",
     "CCAO-F", 60, 99),
    ("developer-foundations/index.html", "Claude Certified Developer, Foundations",
     "CCDV-F", 53, 125),
    ("architect-foundations/index.html", "Claude Certified Architect, Foundations",
     "CCAR-F", 60, 125),
    ("architect-professional/index.html", "Claude Certified Architect, Professional",
     "CCAR-P", 63, 175),
]

# The domains each paper tests, which become competencyRequired. Taken from the
# published blueprints; verify_facts.py checks these names against the guides.
COMPETENCIES = {
    "CCAO-F": ["Prompting and Task Execution", "Output Evaluation and Validation",
               "Product and Model Selection", "Workflow Integration and Solution Design",
               "Configuration and Knowledge Management",
               "Governance, Risk, and Responsible Use", "Troubleshooting and Optimization"],
    "CCDV-F": ["Agents and Workflows", "Applications and Integration", "Claude Code",
               "Eval, Testing, and Debugging", "Model Selection and Optimization",
               "Prompt and Context Engineering", "Security and Safety", "Tools and MCPs"],
    "CCAR-F": ["Agentic Architecture & Orchestration", "Tool Design & MCP Integration",
               "Claude Code Configuration & Workflows",
               "Prompt Engineering & Structured Output", "Context Management & Reliability"],
    "CCAR-P": ["Solution Design & Architecture",
               "Claude Models, Prompting & Context Engineering", "Integration",
               "Evaluation, Testing & Optimization", "Governance, Safety & Risk Management",
               "Stakeholder Communication & Lifecycle Management",
               "Developer Productivity & Operational Enablement"],
}


def credential(path, name, code, items, fee):
    """The schema.org type built for certifications.

    Course describes the studying; EducationalOccupationalCredential describes
    the credential itself, which is what somebody searching "Claude
    certification" is actually looking for. Both are emitted, and they link to
    each other.
    """
    return {
        "@type": "EducationalOccupationalCredential",
        "@id": f"{BASE}/#{code.lower()}",
        "name": name,
        "alternateName": code,
        "identifier": code,
        "url": f"{BASE}/{path}",
        "description": (f"{name} ({code}), an Anthropic certification exam of {items} "
                        f"items over 120 minutes, passing at a scaled score of 720 on a "
                        f"100 to 1,000 range, listed at ${fee} USD."),
        "credentialCategory": "certificate",
        "educationalLevel": "Professional" if code.endswith("-P") else "Foundations",
        "recognizedBy": ANTHROPIC,
        "validFor": "P12M",
        "competencyRequired": COMPETENCIES.get(code, []),
        "inLanguage": "en",
    }

FAQ_RE = re.compile(r"<p><strong>(.*?)</strong>(.*?)</p>", re.S)
TAG_RE = re.compile(r"<[^>]+>")

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BANK_PATH = REPO_ROOT / "question-bank.json"
BANK = json.loads(BANK_PATH.read_text(encoding="utf-8")) if BANK_PATH.exists() else {}
QUESTIONS = BANK.get("questions", [])

# A page of questions maps to one quiz. The keys are the page, the values are
# the (exam, source) pair that selects its questions out of the bank.
QUIZ_PAGES = {}
for _slug in ("associate-foundations", "developer-foundations",
              "architect-foundations", "architect-professional"):
    QUIZ_PAGES[f"{_slug}/practice-questions.html"] = (_slug, "practice")
    for _n in (1, 2, 3):
        QUIZ_PAGES[f"{_slug}/mock-exam-{_n}.html"] = (_slug, f"mock-{_n}")


def question_dataset():
    """The question bank as a Dataset, so it is discoverable as data.

    320 original questions with answers, rationales and domain tags is the
    largest single asset here, and as a bare JSON file in a repository nothing
    was describing it to a search engine.
    """
    return {
        "@type": "Dataset",
        "@id": f"{BASE}/#question-bank",
        "name": "Claude certification practice question bank",
        "description": (
            f"{len(QUESTIONS)} original multiple-choice practice questions for the four "
            "Anthropic Claude certification exams, each with its answer, a written "
            "rationale, the exam it belongs to, and the blueprint domain it tests. "
            "Written from the published exam guides; no exam content is reproduced."),
        "creator": AUTHOR, "publisher": PUBLISHER,
        "license": "https://opensource.org/licenses/MIT",
        "isAccessibleForFree": True, "inLanguage": "en",
        "keywords": ["Claude certification", "Anthropic", "practice questions",
                     "CCAO-F", "CCDV-F", "CCAR-F", "CCAR-P", "exam preparation"],
        "distribution": {
            "@type": "DataDownload",
            "encodingFormat": "application/json",
            "contentUrl": ("https://github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS"
                           "/raw/main/question-bank.json"),
        },
        "measurementTechnique": "Multiple choice, single correct answer",
        "variableMeasured": ["exam", "domain", "question", "options", "answer", "rationale"],
    }


def quiz(relative, url, title):
    """Mark a page of questions up as a Quiz.

    Each question carries its options as suggestedAnswer and the correct one as
    acceptedAnswer, which is the shape search engines and assistants read. This
    is the difference between a page that mentions practice questions and a page
    whose individual questions can be surfaced as answers.
    """
    exam, source = QUIZ_PAGES[relative]
    items = [q for q in QUESTIONS
             if q.get("exam") == exam and q.get("source") == source]
    if not items:
        return None
    parts = []
    for q in items:
        options = q.get("options", {})
        answer = q.get("answer")
        if not options or answer not in options:
            continue
        parts.append({
            "@type": "Question",
            "name": text_of(q.get("question", ""), 300),
            "eduQuestionType": "Multiple choice",
            "learningResourceType": "Practice problem",
            "about": {"@type": "Thing", "name": q.get("domain", "")},
            "acceptedAnswer": {
                "@type": "Answer",
                "text": options[answer],
                "comment": {"@type": "Comment",
                            "text": text_of(q.get("rationale", ""), 400)},
            },
            "suggestedAnswer": [
                {"@type": "Answer", "text": t, "position": i}
                for i, (letter, t) in enumerate(sorted(options.items()))
                if letter != answer
            ],
        })
    if not parts:
        return None
    return {
        "@type": "Quiz",
        "@id": f"{url}#quiz",
        "name": title,
        "url": url,
        "about": {"@type": "Thing", "name": "Anthropic Claude certification"},
        "educationalLevel": "Professional" if exam.endswith("professional") else "Foundations",
        "learningResourceType": "Quiz",
        "isAccessibleForFree": True,
        "inLanguage": "en",
        "author": AUTHOR, "publisher": PUBLISHER,
        "numberOfQuestions": len(parts),
        "hasPart": parts,
    }


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
        for path, name, code, items, fee in EXAMS:
            nodes.append({
                "@type": "Course", "url": f"{BASE}/{path}", "name": name,
                "description": f"Study guide, blueprint, practice questions, and cheat sheet for the "
                               f"{name} certification exam ({code}) from Anthropic.",
                "courseCode": code, "provider": PUBLISHER, "author": AUTHOR,
                "isAccessibleForFree": True, "inLanguage": "en",
                "about": {"@type": "Thing", "name": "Anthropic Claude certification"},
                "teaches": COMPETENCIES.get(code, []),
                "educationalCredentialAwarded": {"@id": f"{BASE}/#{code.lower()}"},
                "hasCourseInstance": {"@type": "CourseInstance",
                                      "courseMode": "online", "courseWorkload": "PT20H"},
            })
            nodes.append(credential(path, name, code, items, fee))
        nodes.append(question_dataset())
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

    # Pages of practice questions and mock exams are quizzes, and their
    # individual questions are the part worth surfacing.
    if relative in QUIZ_PAGES:
        node = quiz(relative, url, title)
        if node:
            nodes.append(node)

    # Each exam page describes the credential it prepares for.
    for path, name, code, items, fee in EXAMS:
        if relative == path:
            nodes.append(credential(path, name, code, items, fee))
            break

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
