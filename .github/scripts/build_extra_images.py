#!/usr/bin/env python3
"""Generate the supporting shareable cards.

Cards that answer questions candidates actually ask, in the same visual language
as the roadmap and cheat sheets: which certification to take, the six published
Architect scenarios, the exam-day checklist, how the official courses map onto
the exams, how scoring and retakes work, a three-week study plan, what the
non-disclosure agreement lets you share, and the registration admin that costs
people their fee. Shares the palette, logos, and footer with build_images.py so
the whole set stays consistent.

    python .github/scripts/build_extra_images.py --render

Standard library only.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_images import (SHADE, footer_at, record_build,   # noqa: E402
    ASSETS, BODY, CARD, CORAL, FAINT, FONT, INK, MUTED, OLIVE, PAPER, PLUM, RULE, TEAL,
    claude_symbol, esc, footer, render,
)

HEAD_NOTE = "A community study resource. Not affiliated with or endorsed by Anthropic."


def frame(width, height, kicker, title, subtitle, accent=CORAL):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}"'
        f' height="{height}" font-family="{FONT}" role="img" aria-label="{esc(title)}: {esc(subtitle)}">',
        f'<rect width="{width}" height="{height}" fill="{PAPER}"/>',
        f'<rect width="{width}" height="8" fill="{accent}"/>',
        claude_symbol(70, 58, 0.46),
        f'<text x="126" y="76" font-size="12" font-weight="700" fill="{accent}" letter-spacing="1.2">{kicker}</text>',
        f'<text x="126" y="110" font-size="32" font-weight="600" fill="{INK}">{esc(title)}</text>',
        f'<text x="70" y="150" font-size="15.5" fill="{MUTED}">{esc(subtitle)}</text>',
        f'<line x1="70" y1="176" x2="{width - 70}" y2="176" stroke="{RULE}"/>',
    ]


def choose_card():
    """Which certification fits which person, with the deciding question first."""
    W, H = 1280, 968
    out = frame(W, H, "START HERE", "Which certification is yours?",
                "Pick the exam that matches the work you already do. There are no prerequisites, and each credential lasts 12 months.")

    lanes = [
        (CORAL, "You advise customers and run engagements",
         "Associate  ·  Foundations", "CCAO-F  ·  60 items  ·  $99",
         ["Turning business problems into Claude workflows",
          "Judging output quality and knowing when to escalate",
          "Data sensitivity and responsible use"],
         "Does not count toward partner tier"),
        (OLIVE, "You build with the API, Claude Code, or MCP",
         "Developer  ·  Foundations", "CCDV-F  ·  53 items  ·  $125",
         ["API mechanics: messages, streaming, batches, caching",
          "Agents, tools, MCP servers, and structured output",
          "Security, cost control, and evaluation"],
         "Counts toward partner tier"),
        (TEAL, "You design Claude solutions end to end",
         "Architect  ·  Foundations", "CCAR-F  ·  60 items  ·  $125",
         ["Agentic architecture and orchestration",
          "Claude Code configuration for teams and CI",
          "Four of six published scenarios appear on your paper"],
         "Counts toward partner tier"),
        (PLUM, "You govern Claude systems at enterprise scale",
         "Architect  ·  Professional", "CCAR-P  ·  63 items  ·  $175",
         ["Integration, retrieval, and observability at scale",
          "Evaluation frameworks and governance",
          "Communicating architecture to stakeholders"],
         "No prerequisite. Foundations does not upgrade into it"),
    ]

    y = 210
    for accent, question, name, facts, bullets, note in lanes:
        out.append(f'<rect x="70" y="{y}" width="{W - 140}" height="140" rx="8" fill="{CARD}" stroke="{RULE}"/>')
        out.append(f'<rect x="70" y="{y}" width="5" height="140" rx="2.5" fill="{accent}"/>')
        out.append(f'<text x="98" y="{y + 34}" font-size="17.5" font-weight="600" fill="{INK}">{esc(question)}</text>')
        out.append(f'<text x="98" y="{y + 60}" font-size="14" font-weight="700" fill="{accent}">{esc(name)}</text>')
        out.append(f'<text x="98" y="{y + 82}" font-size="13.5" fill="{MUTED}">{facts}</text>')
        out.append(f'<text x="98" y="{y + 112}" font-size="12.5" fill="{FAINT}">{esc(note)}</text>')
        by = y + 34
        for line in bullets:
            out.append(f'<circle cx="{600}" cy="{by - 5}" r="3.5" fill="{accent}"/>')
            out.append(f'<text x="616" y="{by}" font-size="13.5" fill="{BODY}">{esc(line)}</text>')
            by += 26
        y += 158

    out.append(f'<text x="70" y="{y + 12}" font-size="14" fill="{BODY}">Every exam: 120 minutes, closed book, proctored by Pearson VUE, passing at 720 of 1000, valid 12 months with a free renewal assessment.</text>')
    out.append(footer(W, y + 40, "Facts drawn from the official Anthropic exam guides"))
    out.append("</svg>")
    return "\n".join(out)


def scenarios_card():
    """The six published Architect Foundations scenarios, four of which appear."""
    W, H = 1280, 946
    out = frame(W, H, "ARCHITECT · FOUNDATIONS", "The six published exam scenarios",
                "Four of these six frame every question on your paper. Knowing them in advance is the largest preparation advantage on any Claude exam.", TEAL)

    scenarios = [
        ("Customer support resolution agent",
         "Agent SDK with MCP tools: get_customer, lookup_order, process_refund, escalate_to_human",
         "Loop termination · escalation triggers · tool scoping · structured errors"),
        ("Code generation with Claude Code",
         "A team using Claude Code for generation, refactoring, debugging, and documentation",
         "CLAUDE.md hierarchy · path-scoped rules · plan mode · custom commands"),
        ("Multi-agent research system",
         "A coordinator delegating to search, analysis, synthesis, and report subagents",
         "Context handoffs · provenance · error propagation · citation integrity"),
        ("Developer productivity tooling",
         "Agents exploring unfamiliar codebases with built-in tools and MCP servers",
         "Read, Write, Bash, Grep, Glob selection · MCP integration · large-context strategy"),
        ("Claude Code in CI/CD",
         "Automated code review, test generation, and pull request feedback",
         "Headless invocation · JSON output · explicit review criteria · false positives"),
        ("Structured data extraction",
         "Extraction from unstructured documents, validated against JSON schemas",
         "Schema design · validation retry loops · batch processing · confidence scoring"),
    ]

    y = 214
    for i, (title, context, rehearse) in enumerate(scenarios, 1):
        out.append(f'<rect x="70" y="{y}" width="{W - 140}" height="92" rx="8" fill="{CARD}" stroke="{RULE}"/>')
        out.append(f'<circle cx="102" cy="{y + 46}" r="17" fill="{TEAL}" opacity="0.12"/>')
        out.append(f'<text x="102" y="{y + 52}" font-size="17" font-weight="700" fill="{TEAL}" text-anchor="middle">{i}</text>')
        out.append(f'<text x="140" y="{y + 32}" font-size="17" font-weight="600" fill="{INK}">{esc(title)}</text>')
        out.append(f'<text x="140" y="{y + 55}" font-size="13.5" fill="{MUTED}">{esc(context)}</text>')
        out.append(f'<text x="140" y="{y + 77}" font-size="13" fill="{TEAL}">{esc(rehearse)}</text>')
        y += 100

    out.append(f'<text x="70" y="{y + 16}" font-size="14" fill="{BODY}">Rehearse each scenario until its likely questions are predictable. Every scenario names its primary domains in the official exam guide.</text>')
    out.append(footer(W, y + 44, "Scenarios published in the official Anthropic exam guide"))
    out.append("</svg>")
    return "\n".join(out)


def exam_day_card():
    """The checklist people screenshot the night before."""
    W, H = 1280, 940
    out = frame(W, H, "EXAM DAY", "The checklist worth keeping",
                "Most failed sittings are logistics, not knowledge. Work through this the week before, then again on the morning.")

    columns = [
        (CORAL, "A week before", [
            "Run the OnVUE system test on the exact machine and network",
            "Send the required Pearson domains to your IT team",
            "Confirm your registration name matches your photo ID exactly",
            "Request accommodations if you need them, before scheduling",
            "Check your partner discount appears at checkout",
        ]),
        (OLIVE, "The night before", [
            "Reschedule free of charge only until 24 hours out",
            "Clear the desk, unplug the second monitor, book the room",
            "Charge the machine and locate your government-issued ID",
            "Reread the exam guide blueprint one last time",
            "Sleep. The paper rewards judgment, not cramming",
        ]),
        (TEAL, "On the morning", [
            "Close browsers, Zoom, Teams, Outlook, Discord, remote access tools",
            "Close the Claude desktop app; OnVUE will not launch beside it",
            "Rerun the system test, even if it passed last week",
            "Start check-in early; it takes longer than you expect",
            "Eat something. Seat time is about 135 minutes",
        ]),
        (PLUM, "During the exam", [
            "Answer everything: an unanswered item scores zero",
            "Flag and move on rather than stalling on one question",
            "Read how many responses each multiple-response item wants",
            "Find the stated constraint, then eliminate against it",
            "Report a faulty question afterwards; it never counts against you",
        ]),
    ]

    y = 212
    for i, (accent, heading, items) in enumerate(columns):
        x = 70 + (i % 2) * 580
        top = y + (i // 2) * 300
        out.append(f'<rect x="{x}" y="{top}" width="560" height="272" rx="8" fill="{CARD}" stroke="{RULE}"/>')
        out.append(f'<rect x="{x}" y="{top}" width="560" height="5" rx="2.5" fill="{accent}"/>')
        out.append(f'<text x="{x + 24}" y="{top + 42}" font-size="17" font-weight="600" fill="{INK}">{heading}</text>')
        iy = top + 76
        for item in items:
            out.append(f'<rect x="{x + 24}" y="{iy - 11}" width="13" height="13" rx="3" fill="none" stroke="{accent}" stroke-width="1.6"/>')
            out.append(f'<text x="{x + 48}" y="{iy}" font-size="13.5" fill="{BODY}">{esc(item)}</text>')
            iy += 36
        y_last = top + 272

    out.append(f'<text x="70" y="{y_last + 40}" font-size="14" fill="{BODY}">Full registration and proctoring detail, including the complete domain allowlist and application shutdown list, is in the repository.</text>')
    out.append(footer(W, y_last + 68, "Requirements published by Anthropic and Pearson VUE"))
    out.append("</svg>")
    return "\n".join(out)


def courses_card():
    """Which of the official courses serve which exam."""
    W, H = 1280, 912
    out = frame(W, H, "OFFICIAL CURRICULUM", "Every course, and the exam it serves",
                "All of these are free on the public Claude Academy. No partner account is needed to learn the material; only the proctored exams require partner membership.", OLIVE)

    groups = [
        (CORAL, "Claude platform", [
            ("Claude 101", "Associate"),
            ("Claude Platform 101", "Associate"),
            ("Claude Code 101", "Developer · Architect"),
            ("Claude Code in Action", "Developer · Architect"),
            ("Introduction to Claude Cowork", "Associate"),
        ]),
        (OLIVE, "Developer and integration", [
            ("Building with the Claude API", "Developer · Architect"),
            ("Introduction to Model Context Protocol", "Developer · Architect"),
            ("Model Context Protocol: Advanced Topics", "Architect Professional"),
            ("Introduction to agent skills", "Developer · Architect"),
            ("Introduction to subagents", "Developer · Architect"),
        ]),
        (TEAL, "Deployment platforms", [
            ("Claude with Amazon Bedrock", "Architect"),
            ("Claude on Google Cloud", "Architect"),
        ]),
        (PLUM, "AI Fluency", [
            ("AI Fluency: Framework & Foundations", "Associate"),
            ("AI Capabilities and Limitations", "Associate"),
            ("AI Fluency for Builders", "Associate"),
            ("Roles: educators, pK-12, students, nonprofits, business, creative", "Context"),
            ("Teaching AI Fluency", "Instructors"),
        ]),
    ]

    y, bottom = 212, 0
    for i, (accent, heading, rows) in enumerate(groups):
        x = 70 + (i % 2) * 580
        top = y + (i // 2) * 316
        height = 44 + len(rows) * 32 + 18
        out.append(f'<rect x="{x}" y="{top}" width="560" height="{height}" rx="8" fill="{CARD}" stroke="{RULE}"/>')
        out.append(f'<rect x="{x}" y="{top}" width="560" height="5" rx="2.5" fill="{accent}"/>')
        out.append(f'<text x="{x + 24}" y="{top + 40}" font-size="16.5" font-weight="600" fill="{INK}">{heading}</text>')
        ry = top + 72
        for name, serves in rows:
            out.append(f'<text x="{x + 24}" y="{ry}" font-size="13.5" fill="{BODY}">{esc(name)}</text>')
            out.append(f'<text x="{x + 536}" y="{ry}" font-size="12.5" fill="{accent}" text-anchor="end">{esc(serves)}</text>')
            ry += 32
        bottom = max(bottom, top + height)

    out.append(f'<text x="70" y="{bottom + 44}" font-size="14" fill="{BODY}">Per-course notes on what each is worth, what to watch for, and the order worth taking them in are in the repository.</text>')
    out.append(footer(W, bottom + 72, "Course catalog published on Claude Academy"))
    out.append("</svg>")
    return "\n".join(out)


def scoring_card():
    """Scoring, retakes, and renewal: the mechanics candidates most often get wrong."""
    W, H = 1280, 946
    out = frame(W, H, "SCORING AND SECOND CHANCES", "What happens after you click submit",
                "How the score is built, what a failure actually costs, and how the credential stays alive.", PLUM)

    out.append(f'<rect x="70" y="212" width="{W - 140}" height="146" rx="8" fill="{CARD}" stroke="{RULE}"/>')
    out.append(f'<text x="98" y="246" font-size="12" font-weight="700" fill="{FAINT}" letter-spacing="0.8">HOW THE SCORE IS BUILT</text>')
    facts = [("100 – 1000", "scaled range"), ("720", "to pass"), ("criterion", "referenced, not a curve"),
             ("per domain", "percent correct reported")]
    fx = 98
    for value, label in facts:
        out.append(f'<text x="{fx}" y="292" font-size="24" font-weight="600" fill="{INK}">{value}</text>')
        out.append(f'<text x="{fx}" y="314" font-size="12.5" fill="{FAINT}">{label}</text>')
        fx += 290
    out.append(f'<text x="98" y="342" font-size="13" fill="{MUTED}">Scaling equates forms of different difficulty. The domain breakdown does not decide the result, but it is the best study signal you will get.</text>')

    out.append(f'<text x="70" y="404" font-size="12" font-weight="700" fill="{FAINT}" letter-spacing="0.8">IF YOU DO NOT PASS</text>')
    steps = [("1st attempt", "wait 14 days"), ("2nd attempt", "wait 30 days"),
             ("3rd attempt", "wait 90 days"), ("4th attempt", "cap for 12 months")]
    x = 70
    for i, (label, wait) in enumerate(steps):
        out.append(f'<rect x="{x}" y="426" width="264" height="76" rx="8" fill="{CARD}" stroke="{RULE}"/>')
        out.append(f'<rect x="{x}" y="426" width="264" height="4" rx="2" fill="{CORAL}" opacity="{1 - i * 0.18}"/>')
        out.append(f'<text x="{x + 20}" y="460" font-size="15.5" font-weight="600" fill="{INK}">{label}</text>')
        out.append(f'<text x="{x + 20}" y="484" font-size="13" fill="{MUTED}">{wait}</text>')
        if i < 3:
            out.append(f'<text x="{x + 278}" y="470" font-size="18" fill="{RULE}">&#8250;</text>')
        x += 296
    out.append(f'<text x="70" y="530" font-size="13" fill="{MUTED}">Every attempt costs the full fee, and your partner discount applies to retakes exactly as to a first sitting. Limits are per exam, so one failure never blocks a different track.</text>')

    out.append(f'<text x="70" y="586" font-size="12" font-weight="700" fill="{FAINT}" letter-spacing="0.8">KEEPING IT ALIVE</text>')
    lanes = [(OLIVE, "Renew on time", "A free, open-book, non-proctored assessment on Partner Academy, retakable as often as you need. Extends the credential another 12 months."),
             (CORAL, "Let it lapse", "The full proctored exam again, at the full fee. There is no partial credit for a credential that expired.")]
    y = 608
    for accent, title, body in lanes:
        out.append(f'<rect x="70" y="{y}" width="{W - 140}" height="88" rx="8" fill="{CARD}" stroke="{RULE}"/>')
        out.append(f'<rect x="70" y="{y}" width="5" height="88" rx="2.5" fill="{accent}"/>')
        out.append(f'<text x="98" y="{y + 34}" font-size="16" font-weight="600" fill="{INK}">{title}</text>')
        out.append(f'<text x="98" y="{y + 62}" font-size="13.5" fill="{MUTED}">{esc(body)}</text>')
        y += 100

    out.append(f'<text x="70" y="{y + 18}" font-size="13.5" fill="{BODY}">A disputed question never changes a pass or fail on its own; a confirmed faulty item that affected a result is remedied with a free retake.</text>')
    out.append(footer(W, y + 46, "Facts drawn from the official Anthropic exam guides and policies"))
    out.append("</svg>")
    return chr(10).join(out)


def study_plan_card():
    """Three weeks from blueprint to booking, for someone with a job."""
    W, H = 1280, 862
    out = frame(W, H, "A WORKING PLAN", "Three weeks, alongside a full-time job",
                "Compress or stretch it to fit. The shape matters more than the calendar: scope, then depth, then close.", OLIVE)

    weeks = [
        (CORAL, "Week one", "Scope",
         ["Read the exam guide end to end", "Turn the blueprint into a red, amber, green checklist",
          "Work the prep courses for your exam", "Mark items green only when you could explain them"]),
        (OLIVE, "Week two", "Depth",
         ["Attack red items first, weighted by domain percentage", "Build the thing the guide asks you to build",
          "Read the official documentation for weak areas", "Drill one weak domain a day"]),
        (TEAL, "Week three", "Close",
         ["Reread the exam guide", "Work the official sample questions and rationales",
          "Sit a timed mock and study the domain breakdown", "Run the system test on the exam machine"]),
    ]
    x = 70
    for accent, week, phase, items in weeks:
        out.append(f'<rect x="{x}" y="212" width="373" height="404" rx="8" fill="{CARD}" stroke="{RULE}"/>')
        out.append(f'<rect x="{x}" y="212" width="373" height="5" rx="2.5" fill="{accent}"/>')
        out.append(f'<text x="{x + 24}" y="252" font-size="12" font-weight="700" fill="{accent}" letter-spacing="1">{week.upper()}</text>')
        out.append(f'<text x="{x + 24}" y="288" font-size="24" font-weight="600" fill="{INK}">{phase}</text>')
        iy = 330
        for item in items:
            out.append(f'<circle cx="{x + 30}" cy="{iy - 5}" r="3.5" fill="{accent}"/>')
            words, line, lines = item.split(), "", []
            for w in words:
                trial = (line + " " + w).strip()
                if len(trial) > 38:
                    lines.append(line); line = w
                else:
                    line = trial
            lines.append(line)
            for j, ln in enumerate(lines):
                out.append(f'<text x="{x + 46}" y="{iy + j * 19}" font-size="13.5" fill="{BODY}">{esc(ln)}</text>')
            iy += 19 * len(lines) + 18
        x += 393

    out.append(f'<rect x="70" y="644" width="{W - 140}" height="72" rx="8" fill="{SHADE}"/>')
    out.append(f'<text x="94" y="672" font-size="12" font-weight="700" fill="{FAINT}" letter-spacing="0.8">THE TWO RULES THAT MATTER MOST</text>')
    out.append(f'<text x="94" y="698" font-size="13.5" fill="{BODY}">Study by domain weight, not by what interests you  ·  build something real, because the exams test judgment and judgment comes from hitting the tradeoffs yourself</text>')

    out.append(f'<text x="70" y="754" font-size="13.5" fill="{MUTED}">Book the exam once the checklist is mostly green. Rescheduling is free until 24 hours out, so an early booking costs nothing and sets a deadline.</text>')
    out.append(footer(W, 782, "Method from the official preparation guidance"))
    out.append("</svg>")
    return chr(10).join(out)


def flashcard_face(back):
    """One card, drawn as a card: the credit line sits inside the border, so a
    crop that removes it visibly cuts the card in half."""
    W, H = 1000, 640
    X, Y = 40, 36
    CW, CH = W - 2 * X, H - 2 * Y
    x0, x1 = X + 40, X + CW - 40
    kicker, tag = ("ANSWER", "Back"), ("QUESTION", "Front  ·  tap to flip")
    k, note = (kicker if back else tag)[0], (kicker if back else tag)[1]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"'
           f' font-family="{FONT}" role="img" aria-label="Flashcard {"back: applications and integration at 33 percent" if back else "front: the heaviest domain on the Developer exam"}">',
           f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
           f'<rect x="{X}" y="{Y}" width="{CW}" height="{CH}" rx="16" fill="{CARD}" stroke="{OLIVE if back else RULE}"/>',
           f'<clipPath id="card"><rect x="{X}" y="{Y}" width="{CW}" height="{CH}" rx="16"/></clipPath>',
           f'<rect x="{X}" y="{Y}" width="{CW}" height="7" fill="{OLIVE}" clip-path="url(#card)"/>',
           f'<text x="{x0}" y="{Y + 74}" font-size="13" font-weight="700" fill="{OLIVE}" letter-spacing="1.2">{k}</text>',
           claude_symbol(x1 - 46, Y + 56, 0.38)]
    if back:
        out += [f'<text x="{x0}" y="{Y + 152}" font-size="34" font-weight="600" fill="{INK}">Applications and integration,</text>',
                f'<text x="{x0}" y="{Y + 196}" font-size="34" font-weight="600" fill="{OLIVE}">33.1% of the paper</text>',
                f'<text x="{x0}" y="{Y + 256}" font-size="16" fill="{MUTED}">A third of the exam sits in one domain. Study it first.</text>',
                f'<rect x="{x0}" y="{Y + 282}" width="{int((x1 - x0) * 0.331)}" height="8" rx="4" fill="{OLIVE}"/>',
                f'<rect x="{x0 + int((x1 - x0) * 0.331)}" y="{Y + 282}" width="{(x1 - x0) - int((x1 - x0) * 0.331)}" height="8" rx="4" fill="{RULE}"/>',
                f'<text x="{x0}" y="{Y + 336}" font-size="13" fill="{FAINT}">blueprint  ·  developer-foundations</text>',
                f'<text x="{x0}" y="{Y + 386}" font-size="14" fill="{MUTED}">Every fact, weight, rule, and term in the deck</text>']
    else:
        out += [f'<text x="{x0}" y="{Y + 146}" font-size="30" font-weight="600" fill="{INK}">Developer Foundations:</text>',
                f'<text x="{x0}" y="{Y + 188}" font-size="30" font-weight="600" fill="{INK}">heaviest domain and its weight?</text>',
                f'<text x="{x0}" y="{Y + 252}" font-size="16" fill="{MUTED}">Tap the card to reveal the answer.</text>',
                f'<text x="{x0}" y="{Y + 320}" font-size="13" fill="{FAINT}">blueprint  ·  developer-foundations</text>',
                f'<text x="{x0}" y="{Y + 386}" font-size="14" fill="{MUTED}">One of 110 cards, free for Anki, Quizlet, or RemNote</text>']
    out.append(footer_at(x0, x1, Y + CH - 116, note))
    out.append("</svg>")
    return chr(10).join(out)


def flashcard_front():
    return flashcard_face(False)


def flashcard_back():
    return flashcard_face(True)


def share_card():
    """The confidentiality line, which almost nobody states plainly."""
    W, H = 1280, 684
    out = frame(W, H, "CONFIDENTIALITY", "What you may and may not share",
                "Every candidate signs a non-disclosure agreement, and it extends explicitly to online forums.",
                PLUM)

    lanes = [
        (CORAL, "Never post or request", [
            "Exam questions, in any wording",
            "Answer options",
            "Scenarios from the live exam",
            "Screenshots of any item",
            "Recalled questions, even in a private study group",
        ]),
        (OLIVE, "Fair game, and useful to others", [
            "The published blueprints and domain weights",
            "The official exam guides and sample questions",
            "Your own notes and original practice material",
            "How you prepared, and what you would change",
            "How the exam felt, and how you scored",
        ]),
    ]

    top = 212
    for i, (accent, heading, items) in enumerate(lanes):
        x = 70 + i * 580
        out.append(f'<rect x="{x}" y="{top}" width="560" height="264" rx="8" fill="{CARD}" stroke="{RULE}"/>')
        out.append(f'<rect x="{x}" y="{top}" width="560" height="5" rx="2.5" fill="{accent}"/>')
        out.append(f'<text x="{x + 24}" y="{top + 42}" font-size="17" font-weight="600" fill="{INK}">{esc(heading)}</text>')
        iy = top + 82
        for item in items:
            out.append(f'<circle cx="{x + 30}" cy="{iy - 5}" r="3.2" fill="{accent}"/>')
            out.append(f'<text x="{x + 48}" y="{iy}" font-size="13.5" fill="{BODY}">{esc(item)}</text>')
            iy += 38

    y = top + 264
    out.append(f'<text x="70" y="{y + 46}" font-size="15.5" font-weight="600" fill="{INK}">The line is content versus experience.</text>')
    out.append(f'<text x="70" y="{y + 76}" font-size="14" fill="{BODY}">Posting what was on the paper puts your own credential at risk. Posting how you prepared helps the next person and costs you nothing.</text>')
    out.append(footer(W, y + 104, "Confidentiality terms published by Anthropic"))
    out.append("</svg>")
    return "\n".join(out)


def registration_card():
    """The logistics that end an attempt before the first question."""
    W, H = 1280, 856
    out = frame(W, H, "REGISTRATION", "The admin that costs people their fee",
                "None of this is on the exam. All of it can end your attempt before the first question.",
                TEAL)

    columns = [
        (CORAL, "Before you can register", [
            "A company email on a domain in your partner record",
            "Personal email addresses do not work",
            "Domain record changes take 7 to 10 days",
            "Check the partner discount appears at checkout",
        ]),
        (OLIVE, "Your Pearson profile", [
            "The name must match your government photo ID exactly",
            "You confirm this at registration, before scheduling",
            "Request any correction more than 24 hours ahead",
            "The corporate phone number is deliberate; leave it alone",
        ]),
        (TEAL, "Scheduling", [
            "Choose online proctoring or a test center",
            "Choose online proctoring or a Pearson test center",
            "Reschedule or cancel free until 24 hours out",
            "Inside 24 hours, or a no-show, the fee is forfeited",
        ]),
        (PLUM, "What a mismatch costs", [
            "Pearson refuses entry, and you do not test",
            "The fee is forfeited under their policy",
            "A correction after refusal does not undo it",
            "You pay again to reschedule",
        ]),
    ]

    y = 212
    for i, (accent, heading, items) in enumerate(columns):
        x = 70 + (i % 2) * 580
        top = y + (i // 2) * 264
        out.append(f'<rect x="{x}" y="{top}" width="560" height="236" rx="8" fill="{CARD}" stroke="{RULE}"/>')
        out.append(f'<rect x="{x}" y="{top}" width="560" height="5" rx="2.5" fill="{accent}"/>')
        out.append(f'<text x="{x + 24}" y="{top + 42}" font-size="17" font-weight="600" fill="{INK}">{esc(heading)}</text>')
        iy = top + 84
        for item in items:
            out.append(f'<circle cx="{x + 30}" cy="{iy - 5}" r="3.2" fill="{accent}"/>')
            out.append(f'<text x="{x + 48}" y="{iy}" font-size="13.5" fill="{BODY}">{esc(item)}</text>')
            iy += 40
        y_last = top + 236

    out.append(f'<text x="70" y="{y_last + 40}" font-size="14" fill="{BODY}">Fix the name on the day you register rather than the day you sit. Inside 24 hours there may not be time to apply the correction.</text>')
    out.append(footer(W, y_last + 68, "Requirements published by Anthropic and Pearson VUE"))
    out.append("</svg>")
    return "\n".join(out)


def main() -> int:
    images = {
        "card-choose-certification.svg": choose_card(),
        "card-what-you-can-share.svg": share_card(),
        "card-registration.svg": registration_card(),
        "card-architect-scenarios.svg": scenarios_card(),
        "card-exam-day.svg": exam_day_card(),
        "card-courses.svg": courses_card(),
        "card-scoring.svg": scoring_card(),
        "card-study-plan.svg": study_plan_card(),
        "flashcard-front.svg": flashcard_front(),
        "flashcard-back.svg": flashcard_back(),
    }
    for name, svg in images.items():
        path = ASSETS / name
        path.write_text(svg + "\n", encoding="utf-8")
        print(f"wrote {name}")
        if "--render" in sys.argv:
            render(path)

    if "--render" in sys.argv:
        record_build("cards", [__file__, Path(__file__).with_name("build_images.py"),
                               ASSETS / "avatar.jpg", *(ASSETS / "logos").glob("*.svg")])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
