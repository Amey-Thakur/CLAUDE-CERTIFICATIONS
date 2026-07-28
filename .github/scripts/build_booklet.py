#!/usr/bin/env python3
"""Build the shareable PDF booklet.

Assembles the roadmap, the cheat sheets, the supporting cards, and the written
guidance into one printable document, then renders it with headless Chrome.
The booklet is meant to travel on its own: someone who receives only the PDF
should be able to choose an exam, study for it, book it, and sit it.

    python .github/scripts/build_booklet.py            # HTML only
    python .github/scripts/build_booklet.py --render   # HTML and PDF

Standard library only.
"""

import base64
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_images import ASSETS, AUTHOR, CERTS, REPO, SITE, find_chrome  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
OUT_HTML = ASSETS / "booklet.html"
OUT_PDF = ROOT / "claude-certifications-booklet.pdf"


REPO_URL = f"https://{REPO}"
SITE_URL = f"https://{SITE}"


def link(text, href):
    """Anchors survive Chrome's print-to-pdf as clickable annotations."""
    return f'<a href="{href}">{text}</a>'


def data_uri(name, mime="image/png"):
    return f"data:{mime};base64," + base64.b64encode((ASSETS / name).read_bytes()).decode()


CSS = """
@page { size: A4 landscape; margin: 0; }
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
  color: #3d3a35;
  background: #faf9f5;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}
.page {
  position: relative;
  width: 297mm; height: 210mm;
  padding: 16mm 18mm 14mm;
  page-break-after: always;
  overflow: hidden;
  background: #faf9f5;
}
.page:last-child { page-break-after: auto; }
.rule-top { position: absolute; inset: 0 0 auto 0; height: 4mm; background: #c15f3c; }
h1 { font-size: 30pt; font-weight: 600; color: #1f1e1b; margin: 0 0 3mm; letter-spacing: -0.3pt; }
h2 { font-size: 17pt; font-weight: 600; color: #1f1e1b; margin: 0 0 2mm; }
h3 { font-size: 11pt; font-weight: 700; color: #8a857c; letter-spacing: 0.6pt;
     text-transform: uppercase; margin: 0 0 2.5mm; }
p { font-size: 10.5pt; line-height: 1.55; margin: 0 0 3mm; }
.lead { font-size: 12pt; color: #3d3a35; }
.muted { color: #6b6862; }
.small { font-size: 9pt; color: #6b6862; }
a { color: #c15f3c; text-decoration: none; }
a:hover { text-decoration: underline; }
.foot a { color: #6b6862; }
.cols { display: flex; gap: 10mm; }
.col { flex: 1; }
img.full { width: 100%; height: auto; display: block; border: 1px solid #e0ddd4; border-radius: 2mm; }
table { width: 100%; border-collapse: collapse; font-size: 9.5pt; }
th { text-align: left; font-size: 8.5pt; text-transform: uppercase; letter-spacing: 0.5pt;
     color: #8a857c; font-weight: 700; padding: 0 0 1.5mm; border-bottom: 1px solid #e0ddd4; }
td { padding: 1.6mm 0; border-bottom: 1px solid #f0eee6; vertical-align: top; }
ol, ul { margin: 0 0 3mm; padding-left: 5mm; font-size: 10pt; line-height: 1.6; }
li { margin-bottom: 1.2mm; }
.foot { position: absolute; left: 18mm; right: 18mm; bottom: 8mm;
        display: flex; align-items: center; gap: 3mm;
        border-top: 1px solid #e0ddd4; padding-top: 3mm; font-size: 8.5pt; color: #6b6862; }
.foot img { width: 8mm; height: 8mm; border: 1px solid #e0ddd4; }
.foot .who { font-weight: 600; color: #3d3a35; }
.foot .spacer { margin-left: auto; }
.foot .pageno { margin-left: 6mm; font-weight: 600; color: #3d3a35;
                min-width: 8mm; text-align: right; }
.cover { display: flex; flex-direction: column; height: 100%; justify-content: center; }
.cover .symbol { width: 22mm; margin-bottom: 8mm; }
.cover h1 { font-size: 42pt; }
.chips { display: flex; gap: 3mm; margin: 6mm 0 0; flex-wrap: wrap; }
.chip { font-size: 9.5pt; font-weight: 600; padding: 1.6mm 4mm; border-radius: 10mm; }
.byline { display: flex; align-items: center; gap: 4mm; margin-top: 12mm; }
.byline img { width: 16mm; height: 16mm; border: 1px solid #e0ddd4; }
.fill { color: #c15f3c; font-style: italic; }
.callout { background: #f0eee6; border-radius: 2mm; padding: 4mm 5mm; margin: 3mm 0; font-size: 10pt; }
.kv { display: flex; gap: 6mm; margin-bottom: 4mm; flex-wrap: wrap; }
.kv div { min-width: 24mm; }
.kv .v { font-size: 15pt; font-weight: 600; color: #1f1e1b; }
.kv .k { font-size: 8.5pt; color: #8a857c; }
"""

ACCENTS = {"associate-foundations": "#c15f3c", "developer-foundations": "#7d8c5c",
           "architect-foundations": "#4f7d8c", "architect-professional": "#8a5f8c"}


def foot(label, number=None):
    """Credit strip, the part you are in, and the page number."""
    page_no = f'<span class="pageno">{number}</span>' if number else ""
    return (f'<div class="foot"><img src="{data_uri("avatar.jpg", "image/jpeg")}" alt="">'
            f'<span><span class="who">{AUTHOR}</span> · {link(REPO, REPO_URL)}</span>'
            f'<span class="spacer">{label}</span>{page_no}</div>')


def page(body, label="Claude Certifications", accent=None):
    """A page is stamped with its part label; numbering is applied at assembly."""
    band = f'<div class="rule-top" style="background:{accent}"></div>' if accent else '<div class="rule-top"></div>'
    return f'<section class="page" data-label="{label}">{band}{body}__FOOT__</section>'


def part_opener(number, title, blurb, contents, accent):
    items = "".join(f'<li>{c}</li>' for c in contents)
    return page(f'''<div style="display:flex;flex-direction:column;height:100%;justify-content:center;max-width:200mm">
        <div style="font-size:12pt;font-weight:700;letter-spacing:1.4pt;color:{accent}">PART {number}</div>
        <h1 style="font-size:38pt;margin-top:3mm">{title}</h1>
        <p class="lead" style="font-size:13pt;max-width:170mm">{blurb}</p>
        <ul style="margin-top:4mm;font-size:11pt;color:#6b6862">{items}</ul>
      </div>''', f"Part {number}: {title}", accent)


def cover():
    symbol = (ASSETS / "logos" / "claude-symbol.svg").read_text(encoding="utf-8")
    symbol_uri = "data:image/svg+xml;base64," + base64.b64encode(symbol.encode()).decode()
    chips = "".join(
        f'<span class="chip" style="background:{ACCENTS[c["slug"]]}1f;color:{ACCENTS[c["slug"]]}">'
        f'{c["role"].title()} {c["level"]}</span>' for c in CERTS)
    return f'''<section class="page"><div class="rule-top"></div>
      <div class="cover">
        <img class="symbol" src="{symbol_uri}" alt="">
        <h1>Claude Certifications</h1>
        <p class="lead" style="font-size:14pt;max-width:180mm">The complete field guide to the four Anthropic
        Claude certifications: what each exam measures, what it costs, how to prepare for it, and how to sit it.</p>
        <div class="chips">{chips}</div>
        <div class="byline">
          <img src="{data_uri("avatar.jpg", "image/jpeg")}" alt="">
          <div>
            <div style="font-size:12pt;font-weight:600;color:#1f1e1b">Compiled by {AUTHOR}</div>
            <div class="small" style="margin-top:1mm">Written while preparing for these exams, after working
            through every course in the official curriculum.<br>{link(REPO, REPO_URL)}  ·  {link(SITE, SITE_URL)}</div>
          </div>
        </div>
        <p class="small" style="margin-top:10mm;max-width:170mm">Facts drawn from the official Anthropic exam guides
        and program pages. A community study resource, not affiliated with or endorsed by Anthropic. Free to share.</p>
      </div>__FOOT__
    </section>'''


def foreword():
    return page(f'''<h3>A note from {AUTHOR}</h3>
      <h1 style="font-size:25pt;max-width:200mm">Why this booklet exists</h1>
      <div class="cols" style="margin-top:2mm">
        <div class="col">
          <p>I sat down to prepare for these certifications and found the material scattered: the blueprint in one
          PDF, the policies in another, the courses on a platform behind a sign-in, the registration mechanics
          somewhere else again, and the practical details, the ones that actually cost people a sitting, written
          down nowhere at all.</p>
          <p>So I collected it. Every official exam guide, every policy, every course, the blueprints with their real
          weights, and the things I only learned by going through it: which domains carry the marks, which options an
          exam question is quietly steering you away from, and how much of a failed attempt is logistics rather than
          knowledge.</p>
          <p>None of this required anything you do not already have. The official material is free, the blueprints
          tell you exactly what is tested, and the rest is steady work.</p>
        </div>
        <div class="col">
          <p>What I could not do is give you the questions, and I would not if I could. Every candidate signs a
          non-disclosure agreement, and a credential is only worth holding if the people holding it earned it. So
          everything here is built from published material: the official blueprints, the published scenarios, and
          practice written from scratch against them.</p>
          <p>Read the roadmap, pick the exam that matches the work you already do, and work its page. Keep the cheat
          sheet for the day before. If a fact here disagrees with the official exam guide, believe the guide, and
          please tell me so I can fix it.</p>
          <div class="callout" style="margin-top:4mm">I put this in one place so your time goes into learning rather
          than looking. If it helps you get certified, it did its job. Good luck.
          <div style="margin-top:2.5mm;font-weight:600">{AUTHOR}</div></div>
        </div>
      </div>''', "A note from the author")


def contents(entries):
    """Built from the assembled page list, so it can never disagree with the booklet."""
    rows = []
    for part, title, blurb, number in entries:
        rows.append(f'<tr><td style="width:14mm;color:#8a857c;font-size:9pt">PART {part}</td>'
                    f'<td style="width:66mm"><strong>{title}</strong></td>'
                    f'<td class="muted">{blurb}</td>'
                    f'<td style="width:12mm;text-align:right;font-weight:600">{number}</td></tr>')
    return page(f'''<h1>What is in this booklet</h1>
      <p class="lead muted" style="max-width:205mm">Five parts, in the order a candidate needs them: choose the exam,
      learn what it measures, prepare for it, sit it, and know where to go afterwards.</p>
      <table style="margin-top:5mm"><tbody>{"".join(rows)}</tbody></table>
      <div class="callout" style="margin-top:5mm"><strong>How to use it.</strong> If you already know which exam you
      are taking, go straight to its pages in Part 2 and keep the cheat sheet for the day before. Everything here is
      derived from the official exam guides, which remain the authoritative source and are mirrored in the
      repository.</div>''', "Contents")



def image_page(title, blurb, image, label, note=None):
    tail = (f'<p class="small" style="margin-top:3mm">{note}</p>') if note else ""
    return page(f'''<h2>{title}</h2><p class="muted" style="max-width:210mm">{blurb}</p>
      <img class="full" src="{data_uri(image)}" alt="{title}" style="margin-top:3mm;max-height:128mm;object-fit:contain">{tail}''', label)


def flashcard_page(label):
    """Both faces of one card, so the deck is shown rather than described."""
    return page(f'''<h2>The deck, one card at a time</h2>
      <p class="muted" style="max-width:210mm">Every fact, domain weight, rule, and glossary term in this booklet is
      also a flashcard. One hundred and ten of them, generated from the same source as everything you have read, so
      they cannot drift out of date.</p>
      <div class="cols" style="margin-top:4mm">
        <div class="col"><img class="full" src="{data_uri("flashcard-front.png")}"
          alt="A flashcard asking which domain carries the most weight on the Developer Foundations exam"
          style="max-height:74mm;object-fit:contain"></div>
        <div class="col"><img class="full" src="{data_uri("flashcard-back.png")}"
          alt="The same card turned over, showing applications and integration at 33 percent"
          style="max-height:74mm;object-fit:contain"></div>
      </div>
      <p class="small" style="margin-top:4mm">Turn them in the browser, filtered by exam or by topic, at
      {link(SITE + "/guide/flashcards", SITE_URL + "/guide/flashcards.html")}, or download the deck as a single
      tab-separated file that Anki, Quizlet, and RemNote all import directly. Use it for the facts that have to be
      automatic on the day: weights, codes, retake windows, and the terms the questions assume you know.</p>''', label)


def worked_question_page(label):
    """One real question, worked through. The booklet describes the practice
    material everywhere else; this is the page that shows it."""
    return page(f'''<h3>What the questions actually look like</h3>
      <h1 style="font-size:24pt">One question, worked through</h1>
      <p class="lead muted" style="max-width:215mm">Every practice question in this repository is written
      the way the real items are: a scenario, one best answer, and three distractors that each fail a stated
      constraint. This one is from Architect Foundations. Read the scenario, commit to an answer, then read
      the reasoning.</p>
      <div class="callout" style="margin-top:4mm">
        <strong>Agentic architecture.</strong> Your support agent resolves most tickets but sometimes loops
        indefinitely, re-calling <code>lookup_order</code> on the same order. What is the correct structural fix?
        <div style="margin-top:3mm;line-height:1.7">
          A. Raise <code>max_tokens</code> so the loop has room to finish<br>
          B. Remove the <code>lookup_order</code> tool<br>
          C. Add explicit loop-termination conditions: cap tool iterations, detect repeated identical calls,
             and route to escalation<br>
          D. Lower the temperature
        </div>
      </div>
      <div class="cols" style="margin-top:4mm">
        <div class="col">
          <h3>The answer is C</h3>
          <p>Agent loops need engineered termination: an iteration budget, detection of repeated identical
          calls, and an escalation path for when the agent cannot make progress. The fix is structural, not a
          setting.</p>
          <h3 style="margin-top:4mm">Why the others are wrong</h3>
          <p>Raising the token budget (A) delays the symptom without bounding the loop. Removing the tool (B)
          breaks the resolution the agent exists to perform. Lowering the temperature (D) changes how the model
          words things and does nothing to iteration.</p>
        </div>
        <div class="col">
          <h3>What the question is really testing</h3>
          <p>Not whether you know what an agent is. Whether you reach for a control when you see unbounded
          autonomy. Every distractor here is something a working engineer might genuinely try first, which is
          exactly how the real exam builds its options: plausible, and wrong for a reason you can name.</p>
          <div class="callout" style="margin-top:3mm">
            <strong>There are 319 more.</strong> Three hundred and twenty original questions, eighty per
            certification, split between topic practice and three timed mock exams each. Every one carries this
            kind of reasoning, not just a letter.
            <div style="margin-top:2mm;font-weight:600">{link(SITE, SITE_URL)}</div>
          </div>
        </div>
      </div>''', label)


def prompts_page(label):
    """Two prompts that work immediately, and a pointer to the rest."""
    return page(f'''<h3>Study with Claude</h3>
      <h1 style="font-size:24pt">Two prompts worth keeping</h1>
      <p class="lead muted" style="max-width:215mm">Claude is the most patient tutor you will get, but only if
      you ask properly. These two do more than any others. Type them as written, replacing the
      <span class="fill">coral italics</span> with your own details.</p>
      <div class="cols" style="margin-top:3mm">
        <div class="col">
          <h3>Find out where you actually stand</h3>
          <p class="small">Run this before you study anything. It produces a ranked list, which beats working
          through the syllabus in order.</p>
          <div class="callout small" style="line-height:1.6">
            You are helping me prepare for the <span class="fill">Claude Certified Architect, Foundations</span> exam. Here is the published blueprint with the weight
            of each domain: <span class="fill">paste the domain table</span>.<br><br>
            Ask me one question at a time, twelve in total, spread across the domains in proportion to their
            weight. Scenario-based, one best answer, four options. Do not tell me the answer until I have
            committed to one.<br><br>
            After all twelve, give me a score per domain, the two domains where I am weakest in weight order,
            what specifically I misunderstood rather than which questions I missed, and what to study first.
          </div>
        </div>
        <div class="col">
          <h3>Understand a question you got wrong</h3>
          <p class="small">The highest-value minute in your preparation. A wrong answer you understand is worth
          more than ten right ones you guessed.</p>
          <div class="callout small" style="line-height:1.6">
            I got this practice question wrong. Question: <span class="fill">paste it with all four options</span>. I chose:
            <span class="fill">your answer</span>. The correct answer is: <span class="fill">the correct answer</span>.<br><br>
            Do not just restate the rationale. Tell me what rule the question is actually testing, why the
            option I chose is attractive and what constraint it fails, what would have to change in the
            scenario for my answer to become correct, and two other situations where the same rule decides it.
          </div>
          <p class="small" style="margin-top:3mm">Seven more, including a study planner, an Architect scenario
          rehearsal, and one that reads a real score report and tells you the smallest gap to close, are at
          {link(SITE + "/guide/prompts", SITE_URL + "/guide/prompts.html")}</p>
        </div>
      </div>''', label)


def hard_won_page(label):
    """The payoff for the promise the foreword makes. Every item here is a fact
    from the official guides and policies, stated as the thing that actually
    costs people a sitting rather than as a policy line."""
    items = [
        ("The blueprint is the scope, and it is enforced",
         "Every exam guide says it plainly: anything outside the blueprint is not tested. People lose weeks "
         "reading around the subject. Print the blueprint, mark each objective red, amber, or green, and study "
         "red first."),
        ("Study by weight, not by interest",
         "Applications and integration is 33.1% of the Developer paper. Claude Code is 3.1%. Two evenings on the "
         "wrong one is a real cost. The weights are published; use them as your timetable."),
        ("A failed attempt costs weeks, not just money",
         "Fourteen days before a second attempt, thirty before a third, ninety before a fourth, and four "
         "attempts maximum in a rolling twelve months. That waiting period, not the fee, is what hurts."),
        ("Book earlier than you feel ready",
         "Rescheduling is free until twenty-four hours before. An early booking costs nothing and supplies the "
         "deadline that makes the studying happen. Inside twenty-four hours the fee is gone."),
        ("Most failed sittings are logistics",
         "Run the OnVUE system test on the machine and the network you will actually use, not a different one. "
         "A corporate network that blocks a single domain will end the exam after you have paid for it."),
        ("Fix your partner email before you plan anything",
         "Domain record changes take seven to ten days. Discovering this the week you meant to sit is the most "
         "avoidable delay in the whole process."),
        ("For Architect Foundations, rehearse all six scenarios",
         "The exam presents four, drawn from a published set of six. They are not a surprise. Working through "
         "all six beforehand converts the hardest paper into a familiar one."),
        ("The credential expires in twelve months",
         "Renewal is free, open book, and not proctored, so it is easy. Letting it lapse is not: you sit the "
         "full exam again at full price. Put the date in a calendar the day you pass."),
        ("Read the score report properly if you fail",
         "It gives percent-correct by domain. Weight each by its share of the paper and you will usually find "
         "the gap sits in one or two places, not everywhere."),
        ("Closed book means closed book",
         "No notes, no documentation, no translation tools, no Claude. Everything in this booklet is for "
         "before the exam, not during it."),
    ]
    left = "".join(f'<p style="margin-bottom:3.5mm"><strong style="color:#1f1e1b">{h}.</strong> '
                   f'<span class="muted">{b}</span></p>' for h, b in items[:5])
    right = "".join(f'<p style="margin-bottom:3.5mm"><strong style="color:#1f1e1b">{h}.</strong> '
                    f'<span class="muted">{b}</span></p>' for h, b in items[5:])
    return page(f'''<h3>The part nobody writes down</h3>
      <h1 style="font-size:25pt">What I would tell myself before the first exam</h1>
      <p class="lead muted" style="max-width:220mm">Ten things that are all published somewhere, and that
      almost nobody reads until it is too late to act on them. If you take one page from this booklet, take
      this one.</p>
      <div class="cols" style="margin-top:3mm;font-size:9.5pt">
        <div class="col">{left}</div>
        <div class="col">{right}</div>
      </div>''', label)


def proof_page(label):
    """The certificates behind the booklet, grouped as the gallery groups them.
    Names and groupings are read from the gallery so the page cannot drift.
    No dates and no duration: the certificates record completion, not a schedule."""
    text = (ROOT / "certificates" / "README.md").read_text(encoding="utf-8")
    groups = []
    for m in re.finditer(r"^## (.+)$", text, re.M):
        nxt = text.find(chr(10) + "## ", m.end())
        body = text[m.end():nxt if nxt > 0 else len(text)]
        names = [n.replace("&amp;", "and") for n in re.findall(r"<b>([^<]+)</b>", body)]
        if names:
            groups.append((m.group(1), names))
    total = sum(len(n) for _, n in groups)

    def block(g):
        title, names = g
        rows = "".join(f'<li style="margin-bottom:0.8mm">{n}</li>' for n in names)
        return (f'<h3 style="margin-top:2.5mm">{title}</h3>'
                f'<ul style="font-size:8.5pt;line-height:1.5;margin:0;padding-left:4mm">{rows}</ul>')

    shots = ["claude-101.png", "building-with-the-claude-api.png",
             "introduction-to-model-context-protocol.png", "teaching-ai-fluency.png"]
    strip = "".join(
        f'<img src="data:image/png;base64,'
        f'{base64.b64encode((ROOT / "certificates" / "previews" / s).read_bytes()).decode()}"'
        f' style="width:23%;border:1px solid #e0ddd4;border-radius:1mm">' for s in shots)

    half = (len(groups) + 1) // 2
    left = "".join(block(g) for g in groups[:half])
    right = "".join(block(g) for g in groups[half:])

    return page(f'''<h3>Receipts, not claims</h3>
      <h1 style="font-size:25pt">The {total} certificates behind this booklet</h1>
      <p class="lead muted" style="max-width:220mm">Every course in the official Anthropic Academy curriculum,
      completed before this booklet was written. Each certificate is issued by Anthropic Education, carries its
      own Skilljar verification record, and can be checked by anyone.</p>

      <div style="display:flex;gap:2%;margin:3mm 0 2mm">{strip}</div>

      <div class="cols">
        <div class="col">{left}</div>
        <div class="col">{right}</div>
      </div>

      <p class="small" style="margin-top:2mm">Every certificate, its PDF, and its verification link is at
      {link(SITE + "/certificates", SITE_URL + "/certificates/index.html")}. The courses are free to anyone on
      the public Academy.</p>''', label)


def glossary_page(label):
    """The vocabulary the exam guides assume you already have, read from the
    repository's glossary so the two cannot disagree."""
    text = (ROOT / "guide" / "glossary.md").read_text(encoding="utf-8")
    rows = [(a.strip(), b.strip()) for a, b in re.findall(r"^\| ([^|]+) \| ([^|]+) \|$", text, re.M)]
    rows = [(a, re.sub(r"\[([^\]]+)\]\([^)]+\)", r"", b))
            for a, b in rows if a not in ("Term", "---") and not a.startswith("---")]
    half = (len(rows) + 1) // 2

    def column(items):
        return "".join(
            f'<p style="margin-bottom:2mm;font-size:8.5pt;line-height:1.45">'
            f'<strong style="color:#1f1e1b">{a}.</strong> <span class="muted">{b}</span></p>'
            for a, b in items)

    return page(f'''<h3>Reference</h3>
      <h1 style="font-size:25pt">The words the exams assume you know</h1>
      <p class="lead muted" style="max-width:220mm">The exam guides use these terms without defining them, and
      questions are written on the assumption that you read them the way the programme does. {len(rows)} terms.</p>
      <div class="cols" style="margin-top:3mm">
        <div class="col">{column(rows[:half])}</div>
        <div class="col">{column(rows[half:])}</div>
      </div>''', label)


def cert_page(cert, label=None):
    accent = ACCENTS[cert["slug"]]
    domains = "".join(
        f'<tr><td>{n}</td><td style="text-align:right;color:{accent};font-weight:600;width:16mm">{w}%</td></tr>'
        for n, w in cert["domains"])
    rules = "".join(f"<li>{r}</li>" for r in cert["rules"])
    prep = " · ".join(cert["prep"])
    return page(f'''<h3 style="color:{accent}">{cert["role"]} · {cert["level"]}</h3>
      <h1 style="font-size:26pt">Claude Certified {cert["role"].title()}</h1>
      <div class="kv">
        <div><div class="v">{cert["code"]}</div><div class="k">exam code</div></div>
        <div><div class="v">{cert["items"].split()[0]}</div><div class="k">items</div></div>
        <div><div class="v">120</div><div class="k">minutes</div></div>
        <div><div class="v">720</div><div class="k">to pass</div></div>
        <div><div class="v">{cert["fee"]}</div><div class="k">list fee</div></div>
        <div><div class="v">12</div><div class="k">months valid</div></div>
      </div>
      <div class="cols">
        <div class="col" style="max-width:100mm">
          <h3>Where the marks are</h3>
          <table><tbody>{domains}</tbody></table>
          <h3 style="margin-top:5mm">Who it is for</h3>
          <p style="font-size:10pt">{cert["audience"]}. {cert["note"]}.</p>
        </div>
        <div class="col">
          <h3>If you remember nothing else</h3>
          <ol>{rules}</ol>
          <h3 style="margin-top:4mm">Prepare with</h3>
          <p style="font-size:9.5pt" class="muted">{prep}</p>
        </div>
      </div>''', label or f'{cert["role"].title()} {cert["level"]}')


def preparing():
    return page('''<h1>Preparing</h1>
      <div class="cols">
        <div class="col">
          <h3>A method that works</h3>
          <ol>
            <li><strong>Read the exam guide twice.</strong> Once before studying, once after. It states plainly that
            the blueprint is the authoritative scope: anything outside it is not on the exam.</li>
            <li><strong>Turn the blueprint into a checklist.</strong> Mark each objective red, amber, or green, and
            study red first, weighted by the domain percentages rather than by interest.</li>
            <li><strong>Build something real.</strong> Every official guide asks for this. The exams test judgment in
            scenarios, and judgment comes from having hit the tradeoffs yourself.</li>
            <li><strong>Use the official sample questions as calibration.</strong> The rationales matter more than the
            answers: they show what the exam considers wrong, and why.</li>
            <li><strong>Book once the checklist is mostly green.</strong> Rescheduling is free until 24 hours out, so
            an early booking costs nothing and sets a deadline.</li>
          </ol>
        </div>
        <div class="col">
          <h3>Practising without breaking the agreement</h3>
          <p>Every candidate accepts a non-disclosure agreement covering exam questions, answer options, and
          scenarios, and it extends explicitly to online forums. Real exam content must never be shared or sought.
          There is also no official practice exam: the previous platform's was retired in the move to Pearson.</p>
          <p>What works instead, and stays clean: generate your own questions from the published blueprint. The
          repository ships a bank of original questions with a shuffled, timed engine that runs in the browser or a
          terminal, and a set of Claude Code commands that quiz, drill, and plan against the blueprints.</p>
          <div class="callout"><strong>The honest framing.</strong> Practice questions calibrate your knowledge
          against the blueprint. They are not exam items, and treating any question set as "the real ones" is both a
          policy violation and a poor strategy, because the item bank is confidential and rotates.</div>
        </div>
      </div>''', "Part 3: Prepare")


def policies():
    return page('''<h1>Policies and scoring</h1>
      <div class="cols">
        <div class="col">
          <h3>How the score is built</h3>
          <p>Each exam is criterion-referenced: you are measured against a fixed standard set by subject matter
          experts, not against other candidates. Results are reported on a scaled range of 100 to 1,000, with 720
          required to pass, and scaling equates forms of slightly different difficulty.</p>
          <p>Your score report also shows percent-correct per domain. Those percentages do not decide the result, but
          they are the most reliable study signal you will get, and they should drive the next plan.</p>
          <h3 style="margin-top:5mm">Retakes</h3>
          <p>Waiting periods grow with each failed attempt: 14 days after the first, 30 after the second, 90 after the
          third, with at most four attempts per exam in a rolling 12 months. Each attempt costs the full fee, and
          partner discounts apply to retakes as to first sittings.</p>
        </div>
        <div class="col">
          <h3>Validity and renewal</h3>
          <p>A credential lasts 12 months from the day it is earned. Renewing before it expires is free: an open-book,
          non-proctored assessment on Anthropic Partner Academy, retakable as often as needed, extending the
          credential another 12 months. The credential itself arrives as a digital badge from Credly, by email, shortly after a pass. Let it lapse and the full exam must be passed again at full fee.</p>
          <h3 style="margin-top:5mm">Appeals and faulty questions</h3>
          <p>Decisions can be appealed to Pearson within 14 days. Separately, anyone may report a question that looks
          wrong, ambiguous, or out of scope; reporting never counts against you, and a confirmed faulty item that
          affected a result is remedied with a free retake rather than a changed score.</p>
          <div class="callout"><strong>Eligibility.</strong> Certification is currently open to people at Claude
          Partner Network organizations, registering with a recognised company email. Domain record changes take 7 to
          10 days, so resolve any email problem well before you plan to sit.</div>
        </div>
      </div>''', "Part 4: Sit it")


def repository_page():
    """What the living version does that paper cannot, and why it is worth the trip."""
    return page(f'''<h3>Beyond this booklet</h3>
      <h1 style="font-size:25pt">The repository behind it</h1>
      <p class="lead muted" style="max-width:215mm">This booklet is a snapshot, printed on a date. The repository is
      the living version: maintained, link-checked every week, and updated when Anthropic changes the program. These
      are the things paper cannot do.</p>
      <div class="cols" style="margin-top:3mm">
        <div class="col">
          <h3>Practise, not just read</h3>
          <p>A bank of original practice questions with a shuffled, timed engine that runs in your browser or your
          terminal. It reorders questions and options on every run, so nothing can be memorised by position, and it
          scores you per domain the way the real report does. Three timed mock exams per certification, each
          with questions that appear nowhere else, so a second sitting still measures something.</p>
          <h3 style="margin-top:4mm">Study the way you already study</h3>
          <p>A flashcard deck covering every fact, domain weight, rule, and term, in a format Anki, Quizlet, and
          RemNote all import directly. A progress tracker that weights each domain by its share of the exam, so the
          number tells you how much of the paper you can actually answer. Anthropic's own videos, including the
          complete AI Fluency course, arranged by the exam each one serves and playable in the page.</p>
          <h3 style="margin-top:4mm">A coach that knows the blueprint</h3>
          <p>Open the repository in Claude Code and six commands are waiting: run a diagnostic to find weak domains,
          drill one of them, sit a timed mock, build a study plan or a week of sessions, and interpret a real score
          report into a decision.</p>
        </div>
        <div class="col">
          <h3>The official documents, kept current</h3>
          <p>Every official exam guide and policy PDF, mirrored with its source URL and the date it was last checked,
          so you can verify anything here against the original in one click. A weekly job re-checks every link, and a
          script re-downloads the documents and reports what changed.</p>
          <h3 style="margin-top:4mm">The parts that go stale fastest</h3>
          <p>Fees, discounts, question counts, and the migration-era rules change. The repository carries dated facts
          and a maintenance routine designed to catch them. When something here disagrees with the official exam
          guide, the guide is right, and the repository is where the correction lands first.</p>
          <h3 style="margin-top:4mm">Other candidates</h3>
          <p>A discussion space for preparation questions and exam experiences, under one firm rule: real exam content
          is never posted. If this booklet helped, the most useful thing you can do is answer someone else's question
          there.</p>
          <div class="callout" style="margin-top:3mm"><strong>Everything is free and open source.</strong> No account,
          no paywall, no email capture. Take it, use it, fork it, and send it to whoever is studying next.
          <div style="margin-top:2mm;font-weight:600">{link(REPO, REPO_URL)}</div></div>
        </div>
      </div>''', "Part 5: Keep going")


def closing():
    return page(f'''<h1>Where to go next</h1>
      <div class="cols">
        <div class="col">
          <h3>Three places to go</h3>
          <p style="font-size:11pt"><strong>{link(REPO, REPO_URL)}</strong><br>
          <span class="muted">The repository: practice engine, flashcards, progress tracker, and the mirrored
          official documents.</span></p>
          <p style="font-size:11pt"><strong>{link(SITE, SITE_URL)}</strong><br>
          <span class="muted">The same material as a searchable website, with the practice engine in the
          browser.</span></p>
          <p style="font-size:11pt"><strong>{link("anthropic.skilljar.com", "https://anthropic.skilljar.com/")}</strong><br>
          <span class="muted">The official courses, free, without a partner account. Registration and the exams
          run through Anthropic Partner Academy and Pearson VUE.</span></p>
        </div>
        <div class="col">
          <h3>If this helped</h3>
          <p>Share it with whoever is studying next. Corrections are welcome as issues, and questions about
          preparation belong in the repository's discussions, where the one firm rule is that real exam content is
          never posted.</p>
          <p>If it saved you time, starring the repository is the whole marketing budget: it is how the next
          candidate searching for this finds it instead of a braindump site.</p>
          <div class="callout">Whatever you are preparing for, the path is the same: read the blueprint, close the
          gaps honestly, build something real, and book the date. You do not need permission or a better moment.
          <div style="margin-top:2.5mm;font-weight:600">{AUTHOR}</div></div>
          <p class="small">Facts drawn from the official Anthropic exam guides and program pages, verified against
          them on publication. A community study resource, not affiliated with or endorsed by Anthropic. Claude and
          Anthropic are trademarks of Anthropic PBC.</p>
        </div>
      </div>''', "Thank you")


def build_html():
    """Assemble the booklet as five signposted parts, then number every page."""
    accents = [ACCENTS["associate-foundations"], ACCENTS["developer-foundations"],
               ACCENTS["architect-foundations"], ACCENTS["architect-professional"], "#c15f3c"]

    parts = []

    parts.append((1, "Choose your exam",
                  "Four certifications across three roles, with no prerequisites in either direction. Pick the one "
                  "that matches the work you already do.",
                  ["Which certification is yours", "The roadmap: every exam side by side"],
                  [image_page("Which certification is yours?",
                              "Pick the exam that matches the work you already do.",
                              "card-choose-certification.png", "Part 1: Choose your exam"),
                   image_page("The roadmap",
                              "All four certifications: what each measures, what it costs, and what prepares you for it.",
                              "roadmap.png", "Part 1: Choose your exam")]))

    exam_pages = []
    for cert in CERTS:
        label = f'Part 2: {cert["role"].title()} {cert["level"]}'
        exam_pages.append(cert_page(cert, label))
        exam_pages.append(image_page(f'Cheat sheet: {cert["role"].title()} {cert["level"]}',
                                     "The page worth keeping for the hour before the exam.",
                                     f'cheat-sheet-{cert["slug"]}.png', label,
                                     f'The full sheet, with the reasoning behind every rule and a timed mock exam '
                                     f'for this certification, is at {link(SITE, SITE_URL)}'))
        if cert["slug"] == "architect-foundations":
            exam_pages.append(image_page("The six published scenarios",
                                         "Four of these six frame every question on this paper. Rehearse them.",
                                         "card-architect-scenarios.png", label,
                                         f'Practice questions framed inside these scenarios are in the practice '
                                         f'engine at {link(SITE, SITE_URL)}'))
    parts.append((2, "Know your exam",
                  "A page of facts and a cheat sheet for each certification: the blueprint with real domain weights, "
                  "and the rules that decide questions.",
                  ["Associate, Developer, and both Architect exams",
                   "The six published Architect Foundations scenarios"],
                  exam_pages))

    parts.append((3, "Prepare",
                  "What to study, in what order, and how to practise without touching material you are not allowed "
                  "to touch.",
                  ["The official curriculum and the exam each course serves",
                   "A three-week plan that fits alongside a job", "The flashcard deck",
                   "One question worked through, and two prompts worth keeping",
                   "A method, and practising within the agreement"],
                  [image_page("The official curriculum",
                              "Every Anthropic course, free on the public Academy, and the exam each one serves.",
                              "card-courses.png", "Part 3: Prepare",
                              f'Notes on what each course is worth and the order worth taking them in are at {link(SITE, SITE_URL)}'),
                   image_page("A working study plan",
                              "Three weeks alongside a job: scope, then depth, then close.",
                              "card-study-plan.png", "Part 3: Prepare",
                              f'A progress tracker keeps this checklist for you, weighted by exam share, at {link(SITE, SITE_URL)}'),
                   flashcard_page("Part 3: Prepare"),
                   worked_question_page("Part 3: Prepare"),
                   prompts_page("Part 3: Prepare"),
                   preparing()]))

    parts.append((4, "Sit it",
                  "Booking, proctoring, and the day itself, then what the result means and what happens if it is not "
                  "the one you wanted.",
                  ["The exam-day checklist", "Scoring, retakes, validity, and renewal"],
                  [image_page("Exam day", "Most failed sittings are logistics, not knowledge.",
                              "card-exam-day.png", "Part 4: Sit it",
                              f'The complete network allowlist and application shutdown list are at {link(SITE, SITE_URL)}'),
                   image_page("Scoring and second chances",
                              "How the score is built, what a failed attempt costs, and how the credential stays alive.",
                              "card-scoring.png", "Part 4: Sit it"),
                   policies()]))

    parts.append((5, "Keep going",
                  "You now have everything the exam asks of you. What follows is where to find the parts that keep moving.",
                  ["The vocabulary the exams assume", "The twenty-one course certificates behind it",
                   "What the living version does that paper cannot", "Where to go next"],
                  [glossary_page("Part 5: Keep going"), proof_page("Part 5: Keep going"),
                   repository_page(), closing()]))

    # First pass: lay out pages so the contents can carry real numbers.
    pages, entries = [], []
    layout = []
    for num, title, blurb, bullets, body_pages in parts:
        layout.append((num, title, blurb, bullets, body_pages))

    # The front matter is assembled first so the contents can count it rather
    # than assume it. Adding a front page now corrects the page numbers itself.
    front = [cover(), foreword(), None, hard_won_page("Before you start")]
    contents_at = front.index(None)

    running = len(front) + 1
    for num, title, blurb, bullets, body_pages in layout:
        entries.append((num, title, blurb, running))
        running += 1 + len(body_pages)

    front[contents_at] = contents(entries)
    pages.extend(front)
    for i, (num, title, blurb, bullets, body_pages) in enumerate(layout):
        pages.append(part_opener(num, title, blurb, bullets, accents[i]))
        pages.extend(body_pages)

    numbered = []
    for i, html in enumerate(pages, 1):
        label = re.search(r'data-label="([^"]*)"', html)
        label = label.group(1) if label else "Claude Certifications"
        numbered.append(html.replace("__FOOT__", "" if i == 1 else foot(label, i)))

    return ("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<title>Claude Certifications: the complete field guide</title>"
            f"<style>{CSS}</style></head><body>{''.join(numbered)}</body></html>")


def main() -> int:
    OUT_HTML.write_text(build_html(), encoding="utf-8")
    print(f"wrote {OUT_HTML.name}")

    if "--render" in sys.argv:
        chrome = find_chrome()
        if chrome is None:
            print("No Chrome found; skipping PDF. Set CHROME_PATH to override.")
            return 0
        subprocess.run(
            [str(chrome), "--headless", "--disable-gpu", "--no-pdf-header-footer",
             f"--print-to-pdf={OUT_PDF}", OUT_HTML.as_uri()],
            capture_output=True, check=False,
        )
        if OUT_PDF.exists():
            print(f"{OUT_PDF.name}: {OUT_PDF.stat().st_size // 1024} KB")
        else:
            print("PDF render failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
