#!/usr/bin/env python3
"""Generate the repository's shareable images from one set of facts.

Produces the social preview card, the certification roadmap poster, and a
cheat sheet card per certification, all in the same visual language and all
carrying the maintainer's avatar and the repository link. Writing them from
data rather than by hand keeps the facts consistent with the documentation
and makes them regenerable when the program changes.

Rasterize afterwards with headless Chrome:
    python .github/scripts/build_images.py
    python .github/scripts/build_images.py --render   # also writes PNGs

Standard library only.
"""

import base64
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
ASSETS = ROOT / ".github" / "assets"
LOGOS = ASSETS / "logos"

REPO = "github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS"
SITE = "amey-thakur.github.io/CLAUDE-CERTIFICATIONS"
AUTHOR = "Amey Thakur"

INK = "#1f1e1b"
BODY = "#3d3a35"
MUTED = "#6b6862"
FAINT = "#8a857c"
RULE = "#e0ddd4"
PAPER = "#faf9f5"
CARD = "#ffffff"
CORAL = "#c15f3c"
CLAUDE = "#d97757"
OLIVE = "#7d8c5c"
TEAL = "#4f7d8c"
PLUM = "#8a5f8c"

FONT = "Segoe UI, Helvetica Neue, Arial, sans-serif"

CERTS = [
    {
        "role": "ASSOCIATE", "level": "Foundations", "accent": CORAL, "slug": "associate-foundations",
        "code": "CCAO-F", "items": "60 items", "fee": "$99", "extra": "pass 720/1000",
        "audience": "Consultants, sellers, and delivery leads",
        "domains": [("Output evaluation", 21), ("Workflow integration", 16), ("Governance and risk", 15),
                    ("Prompting", 14), ("Product and model choice", 12), ("Configuration", 12),
                    ("Troubleshooting", 10)],
        "prep": ["Claude 101", "Claude Platform 101", "AI Fluency: Framework",
                 "AI Capabilities and Limits", "Introduction to Cowork"],
        "note": "Does not count toward partner tier",
        "rules": [
            "Verify anything specific and consequential. Confidence is not evidence.",
            "Omission fails too. Read the source, not only the output.",
            "Anonymize, then analyze. Instructions are not a control.",
            "Match the model to the task in both directions.",
            "Structure beats intensifiers: role, sections, constraints, example.",
            "Projects hold what repeats; prompts hold what changes.",
            "Project knowledge is maintained by you, not self-updating.",
            "Diagnose what changed before rewriting anything.",
            "Escalate system integrations to Developer and Architect scope.",
        ],
    },
    {
        "role": "DEVELOPER", "level": "Foundations", "accent": OLIVE, "slug": "developer-foundations",
        "code": "CCDV-F", "items": "53 items", "fee": "$125", "extra": "pass 720/1000",
        "audience": "Engineers building on the Claude platform",
        "domains": [("Applications and integration", 33), ("Model selection and cost", 17),
                    ("Agents and workflows", 15), ("Prompt and context", 11), ("Tools and MCP", 11),
                    ("Security and safety", 8), ("Claude Code, eval", 6)],
        "prep": ["Building with the Claude API", "Introduction to MCP", "Claude Code in Action",
                 "Introduction to agent skills", "Introduction to subagents"],
        "note": "Counts toward partner tier",
        "rules": [
            "stop_reason drives the loop: tool_use executes, end_turn finishes.",
            "Batches for latency-tolerant volume: half cost, 24-hour window.",
            "Stable prefix first, then cache it. Cuts latency and cost together.",
            "Enforce a schema, validate, retry with the validation error.",
            "Known path is a workflow. Unknown path earns an agent.",
            "Subagents exist to isolate context, not to add horsepower.",
            "Pin model versions; upgrades become evaluated changes.",
            "Injection is defeated structurally, never by asking politely.",
            "A tool the agent does not hold cannot be misused.",
        ],
    },
    {
        "role": "ARCHITECT", "level": "Foundations", "accent": TEAL, "slug": "architect-foundations",
        "code": "CCAR-F", "items": "60 items", "fee": "$125", "extra": "4 of 6 scenarios",
        "audience": "Architects building production systems",
        "domains": [("Agentic architecture", 27), ("Claude Code workflows", 20),
                    ("Prompting, structured output", 20), ("Tool design and MCP", 18),
                    ("Context and reliability", 15)],
        "prep": ["Claude Code in Action", "Introduction to MCP", "Building with the Claude API",
                 "Agent skills and subagents", "The six published scenarios"],
        "note": "Counts toward partner tier",
        "rules": [
            "Agent loops need engineered termination, not a token budget.",
            "Escalate on policy gaps and lack of progress.",
            "Structured errors: a category and a retryable flag.",
            "Tool descriptions are the selection mechanism. Differentiate them.",
            "Hard limits belong in the tool layer, never in a prompt.",
            "CLAUDE.md hierarchy, with path-scoped rules for conditional context.",
            "CI means headless: print mode, JSON output, a schema.",
            "Subagents return findings; raw documents stay at the edge.",
            "Provenance must survive every handoff.",
        ],
    },
    {
        "role": "ARCHITECT", "level": "Professional", "accent": PLUM, "slug": "architect-professional",
        "code": "CCAR-P", "items": "63 items", "fee": "$175", "extra": "pass 720/1000",
        "audience": "Architects governing systems at scale",
        "domains": [("Integration", 19), ("Solution design", 17), ("Evaluation and testing", 16),
                    ("Governance and risk", 14), ("Stakeholders, lifecycle", 14),
                    ("Models and prompting", 13), ("Developer enablement", 7)],
        "prep": ["MCP: Advanced Topics", "Claude with Amazon Bedrock", "Claude on Google Cloud",
                 "An end-to-end system you built", "Anthropic engineering articles"],
        "note": "No prerequisite. Foundations does not upgrade",
        "rules": [
            "Climb the pattern ladder only when the rung below cannot hold.",
            "Least privilege means removal, not monitoring.",
            "Retrieval degradation after a data change is an index problem.",
            "Subjective quality is measured with rubrics and labeled sets.",
            "Prompt changes are production changes: regression, then A/B.",
            "Compliance is enforced before data crosses the boundary.",
            "Route human review by confidence and consequence.",
            "Present segmented, honest numbers, never a flattering average.",
            "Observability captures traces, not just outputs.",
        ],
    },
]


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def claude_symbol(x, y, scale, fill=CLAUDE):
    d = re.search(r'\sd="([^"]+)"', (LOGOS / "claude-symbol.svg").read_text(encoding="utf-8")).group(1)
    return f'<g transform="translate({x},{y}) scale({scale})"><path d="{d}" fill="{fill}"/></g>'


def anthropic_wordmark(x, y, width, fill=BODY):
    svg = (LOGOS / "anthropic-wordmark.svg").read_text(encoding="utf-8")
    paths = re.findall(r'<path[^>]*d="([^"]+)"', svg)
    scale = width / 1024.2
    body = "".join(f'<path d="{d}" fill="{fill}"/>' for d in paths)
    return f'<g transform="translate({x},{y}) scale({scale})">{body}</g>'


def avatar(x, y, size):
    """The maintainer's GitHub photo, square as it appears on the profile."""
    data = base64.b64encode((ASSETS / "avatar.jpg").read_bytes()).decode()
    return (
        f'<image x="{x}" y="{y}" width="{size}" height="{size}" preserveAspectRatio="xMidYMid slice"'
        f' href="data:image/jpeg;base64,{data}"/>'
        f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="none" stroke="{RULE}"/>'
    )


def footer_at(x0, x1, y, note=None):
    """The standing credit line: who made this, where it lives, whose exams it covers."""
    parts = [f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{RULE}"/>']
    parts.append(avatar(x0, y + 20, 40))
    parts.append(f'<text x="{x0 + 54}" y="{y + 40}" font-size="15" font-weight="600" fill="{BODY}">{AUTHOR}</text>')
    parts.append(f'<text x="{x0 + 54}" y="{y + 58}" font-size="13.5" fill="{MUTED}">{REPO}</text>')
    parts.append(anthropic_wordmark(x1 - 130, y + 26, 130))
    if note:
        parts.append(f'<text x="{x1}" y="{y + 62}" font-size="12" fill="{FAINT}" text-anchor="end">{esc(note)}</text>')
    return "".join(parts)


def footer(width, y, note=None):
    return footer_at(70, width - 70, y, note)


def bar(x, y, width, value, maximum, colour, opacity=1.0):
    w = max(6, round(width * value / maximum))
    return f'<rect x="{x}" y="{y}" width="{w}" height="5" rx="2.5" fill="{colour}" opacity="{opacity}"/>'


def social_preview():
    W, H = 1280, 640
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"'
           f' font-family="{FONT}" role="img" aria-label="Claude Certifications: study guides, official documents,'
           f' practice engine, and cheat sheets for all four Anthropic Claude certifications">',
           f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
           f'<rect width="{W}" height="8" fill="{CORAL}"/>']

    out.append(claude_symbol(70, 52, 0.52))
    out.append(f'<text x="134" y="90" font-size="44" font-weight="600" fill="{INK}">Claude Certifications</text>')
    out.append(f'<text x="134" y="120" font-size="19" fill="{BODY}">Everything you need to pass, in one place.</text>')

    chip_y = 156
    chips = [("Associate", CORAL), ("Developer", OLIVE), ("Architect Foundations", TEAL),
             ("Architect Professional", PLUM)]
    x = 70
    for label, colour in chips:
        w = 22 + len(label) * 8.7
        out.append(f'<rect x="{x}" y="{chip_y}" width="{w:.0f}" height="32" rx="16" fill="{colour}" opacity="0.12"/>')
        out.append(f'<text x="{x + w / 2:.0f}" y="{chip_y + 21}" font-size="14" font-weight="600"'
                   f' fill="{colour}" text-anchor="middle">{label}</text>')
        x += w + 12

    rows = [
        (CORAL, "Every official exam guide, policy, and blueprint", "mirrored, sourced, and dated"),
        (OLIVE, "A study guide and working notes per exam", "domain by domain, weighted as the exam is"),
        (TEAL, "A practice engine that shuffles and scores", "in the browser or your terminal"),
        (PLUM, "A one-page cheat sheet for each exam", "the page you read the hour before"),
        (CORAL, "Every official course, catalogued and reviewed", "with the order worth taking them in"),
        (OLIVE, "Registration, proctoring, policies, and costs", "the logistics nobody writes down"),
    ]
    top = 226
    for i, (colour, title, sub) in enumerate(rows):
        cx = 70 + (i % 2) * 600
        cy = top + (i // 2) * 74
        out.append(f'<circle cx="{cx + 5}" cy="{cy - 5}" r="4.5" fill="{colour}"/>')
        out.append(f'<text x="{cx + 26}" y="{cy}" font-size="17.5" font-weight="600" fill="{INK}">{esc(title)}</text>')
        out.append(f'<text x="{cx + 26}" y="{cy + 23}" font-size="15" fill="{MUTED}">{esc(sub)}</text>')

    out.append(f'<text x="70" y="452" font-size="15.5" fill="{BODY}">Free, open source, and written by someone who sat the exams. No sign-up, no paywall, no braindumps.</text>')
    out.append(footer(W, 492, "Facts drawn from the official Anthropic exam guides"))
    out.append("</svg>")
    return "\n".join(out)


def roadmap():
    W, H = 1400, 1046
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"'
           f' font-family="{FONT}" role="img" aria-label="Claude certification roadmap: four certifications with'
           f' exam facts, domain weights, and the courses that prepare for each">',
           f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
           f'<rect width="{W}" height="8" fill="{CORAL}"/>']

    out.append(claude_symbol(70, 48, 0.46))
    out.append(f'<text x="126" y="82" font-size="34" font-weight="600" fill="{INK}">Claude Certification Roadmap</text>')
    out.append(f'<text x="126" y="110" font-size="16" fill="{MUTED}">Four certifications, three roles. What each exam covers, what it costs, and what prepares you for it.</text>')
    out.append(f'<line x1="70" y1="146" x2="{W - 70}" y2="146" stroke="{RULE}"/>')

    col_w, gap, top = 300, 20, 178
    for i, cert in enumerate(CERTS):
        x = 70 + i * (col_w + gap)
        a = cert["accent"]
        out.append(f'<rect x="{x}" y="{top}" width="{col_w}" height="656" rx="8" fill="{CARD}" stroke="{RULE}"/>')
        out.append(f'<rect x="{x}" y="{top}" width="{col_w}" height="5" rx="2.5" fill="{a}"/>')
        out.append(f'<text x="{x + 22}" y="{top + 40}" font-size="12" font-weight="700" fill="{a}" letter-spacing="1.2">{cert["role"]}</text>')
        out.append(f'<text x="{x + 22}" y="{top + 68}" font-size="21" font-weight="600" fill="{INK}">{cert["level"]}</text>')
        out.append(f'<text x="{x + 22}" y="{top + 92}" font-size="13.5" fill="{MUTED}">{cert["code"]}  ·  {cert["items"]}  ·  {cert["fee"]}</text>')
        out.append(f'<text x="{x + 22}" y="{top + 112}" font-size="13.5" fill="{MUTED}">120 min  ·  {cert["extra"]}</text>')
        out.append(f'<text x="{x + 22}" y="{top + 142}" font-size="12.5" fill="{BODY}">{esc(cert["audience"])}</text>')

        out.append(f'<text x="{x + 22}" y="{top + 182}" font-size="11" font-weight="700" fill="{FAINT}" letter-spacing="0.7">DOMAINS BY WEIGHT</text>')
        y = top + 208
        for j, (name, weight) in enumerate(cert["domains"]):
            out.append(f'<text x="{x + 22}" y="{y}" font-size="12.5" fill="{BODY}">{esc(name)}</text>')
            out.append(f'<text x="{x + col_w - 22}" y="{y}" font-size="12.5" fill="{MUTED}" text-anchor="end">{weight}%</text>')
            out.append(bar(x + 22, y + 7, col_w - 44, weight, 33, a, max(0.55, 1 - j * 0.06)))
            y += 32

        y = top + 470
        out.append(f'<line x1="{x + 22}" y1="{y - 22}" x2="{x + col_w - 22}" y2="{y - 22}" stroke="{RULE}"/>')
        out.append(f'<text x="{x + 22}" y="{y}" font-size="11" font-weight="700" fill="{FAINT}" letter-spacing="0.7">PREPARE WITH</text>')
        y += 26
        for name in cert["prep"]:
            out.append(f'<text x="{x + 22}" y="{y}" font-size="13" fill="{BODY}">{esc(name)}</text>')
            y += 23
        out.append(f'<text x="{x + 22}" y="{top + 622}" font-size="11.5" fill="{FAINT}">{esc(cert["note"])}</text>')

    strip = top + 692
    out.append(f'<rect x="70" y="{strip}" width="{W - 140}" height="48" rx="8" fill="#f0eee6"/>')
    out.append(f'<text x="94" y="{strip + 30}" font-size="13.5" fill="{BODY}">Every exam: 120 minutes  ·  closed book  ·  Pearson VUE, online or test centre  ·  pass at 720 of 1000  ·  valid 12 months, free renewal  ·  badge via Credly  ·  partner tiers get 50% off</text>')

    out.append(footer(W, strip + 76, "Facts drawn from the official Anthropic exam guides"))
    out.append("</svg>")
    return "\n".join(out)


def cheat_sheet(cert):
    W, H = 1280, 872
    a = cert["accent"]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"'
           f' font-family="{FONT}" role="img" aria-label="Cheat sheet for the Claude Certified {cert["role"].title()}'
           f' {cert["level"]} exam: facts, domain weights, and the rules that decide questions">',
           f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
           f'<rect width="{W}" height="8" fill="{a}"/>']

    out.append(claude_symbol(70, 62, 0.50))
    out.append(f'<text x="136" y="80" font-size="12.5" font-weight="700" fill="{a}" letter-spacing="1.2">{cert["role"]}  ·  {cert["level"].upper()}  ·  CHEAT SHEET</text>')
    out.append(f'<text x="136" y="112" font-size="30" font-weight="600" fill="{INK}">Claude Certified {cert["role"].title()}</text>')

    facts = [(cert["code"], "exam code"), (cert["items"].split()[0], "items"), ("120", "minutes"),
             ("720", "to pass"), (cert["fee"], "list fee"), ("12", "months valid")]
    fx = 70
    out.append(f'<line x1="70" y1="140" x2="{W - 70}" y2="140" stroke="{RULE}"/>')
    for value, label in facts:
        out.append(f'<text x="{fx}" y="182" font-size="26" font-weight="600" fill="{INK}">{value}</text>')
        out.append(f'<text x="{fx}" y="204" font-size="12.5" fill="{FAINT}">{label}</text>')
        fx += 190
    out.append(f'<line x1="70" y1="232" x2="{W - 70}" y2="232" stroke="{RULE}"/>')

    out.append(f'<text x="70" y="272" font-size="12" font-weight="700" fill="{FAINT}" letter-spacing="0.8">WHERE THE MARKS ARE</text>')
    y = 306
    for j, (name, weight) in enumerate(cert["domains"]):
        out.append(f'<text x="70" y="{y}" font-size="14" fill="{BODY}">{esc(name)}</text>')
        out.append(f'<text x="500" y="{y}" font-size="14" fill="{MUTED}" text-anchor="end">{weight}%</text>')
        out.append(bar(70, y + 9, 430, weight, 33, a, max(0.55, 1 - j * 0.06)))
        y += 40

    out.append(f'<text x="580" y="272" font-size="12" font-weight="700" fill="{FAINT}" letter-spacing="0.8">IF YOU REMEMBER NOTHING ELSE</text>')
    y = 304
    for i, rule in enumerate(cert["rules"], 1):
        out.append(f'<text x="580" y="{y}" font-size="13" font-weight="700" fill="{a}">{i}</text>')
        out.append(f'<text x="602" y="{y}" font-size="13.5" fill="{BODY}">{esc(rule)}</text>')
        y += 30

    out.append(f'<rect x="70" y="608" width="{W - 140}" height="70" rx="8" fill="#f0eee6"/>')
    out.append(f'<text x="94" y="636" font-size="12" font-weight="700" fill="{FAINT}" letter-spacing="0.8">ON THE DAY</text>')
    out.append(f'<text x="94" y="660" font-size="13.5" fill="{BODY}">Answer everything, unanswered scores zero  ·  flag and return rather than stalling  ·  read how many responses each item wants  ·  find the stated constraint, then eliminate</text>')

    out.append(f'<text x="70" y="716" font-size="13.5" fill="{MUTED}">Full sheet, study guide, notes, practice questions, and a timed mock exam: {SITE}</text>')
    out.append(footer(W, 752, "Facts drawn from the official Anthropic exam guide"))
    out.append("</svg>")
    return "\n".join(out)


def render(svg_path):
    chrome = Path("C:/Program Files/Google/Chrome/Application/chrome.exe")
    if not chrome.exists():
        print(f"skip render, Chrome not found: {svg_path.name}")
        return
    svg = svg_path.read_text(encoding="utf-8")
    width = int(re.search(r'width="(\d+)"', svg).group(1))
    height = int(re.search(r'height="(\d+)"', svg).group(1))
    png = svg_path.with_suffix(".png")
    subprocess.run(
        [str(chrome), "--headless", "--disable-gpu", "--hide-scrollbars",
         f"--screenshot={png}", f"--window-size={width},{height}", svg_path.as_uri()],
        capture_output=True, check=False,
    )
    print(f"{png.name}: {png.stat().st_size // 1024} KB" if png.exists() else f"{png.name}: FAILED")


def main() -> int:
    images = {"social-preview.svg": social_preview(), "roadmap.svg": roadmap()}
    for cert in CERTS:
        images[f"cheat-sheet-{cert['slug']}.svg"] = cheat_sheet(cert)

    for name, svg in images.items():
        path = ASSETS / name
        path.write_text(svg + "\n", encoding="utf-8")
        print(f"wrote {name}")
        if "--render" in sys.argv:
            render(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
