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

from build_images import ASSETS, AUTHOR, CERTS, REPO, SITE  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
OUT_HTML = ASSETS / "booklet.html"
OUT_PDF = ROOT / "claude-certifications-booklet.pdf"
CHROME = Path("C:/Program Files/Google/Chrome/Application/chrome.exe")


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
          <div style="margin-top:2.5mm;font-weight:600">— {AUTHOR}</div></div>
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
      </div>''', "Preparing")


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
          credential another 12 months. Let it lapse and the full exam must be passed again at full fee.</p>
          <h3 style="margin-top:5mm">Appeals and faulty questions</h3>
          <p>Decisions can be appealed to Pearson within 14 days. Separately, anyone may report a question that looks
          wrong, ambiguous, or out of scope; reporting never counts against you, and a confirmed faulty item that
          affected a result is remedied with a free retake rather than a changed score.</p>
          <div class="callout"><strong>Eligibility.</strong> Certification is currently open to people at Claude
          Partner Network organizations, registering with a recognised company email. Domain record changes take 7 to
          10 days, so resolve any email problem well before you plan to sit.</div>
        </div>
      </div>''', "Policies")


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
          scores you per domain the way the real report does.</p>
          <h3 style="margin-top:4mm">Study the way you already study</h3>
          <p>A flashcard deck covering every fact, domain weight, rule, and term, in a format Anki, Quizlet, and
          RemNote all import directly. A progress tracker that weights each domain by its share of the exam, so the
          number tells you how much of the paper you can actually answer.</p>
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
      </div>''', "The repository")


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
          <div style="margin-top:2.5mm;font-weight:600">— {AUTHOR}</div></div>
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
                  ["What the living version does that paper cannot", "Where to go next"],
                  [repository_page(), closing()]))

    # First pass: lay out pages so the contents can carry real numbers.
    pages, entries, number = [], [], 2
    layout = []
    for num, title, blurb, bullets, body_pages in parts:
        layout.append((num, title, blurb, bullets, body_pages))

    running = 4  # cover 1, foreword 2, contents 3, first part opener 4
    for num, title, blurb, bullets, body_pages in layout:
        entries.append((num, title, blurb, running))
        running += 1 + len(body_pages)

    pages.append(cover())
    pages.append(foreword())
    pages.append(contents(entries))
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
        if not CHROME.exists():
            print("Chrome not found; skipping PDF")
            return 0
        subprocess.run(
            [str(CHROME), "--headless", "--disable-gpu", "--no-pdf-header-footer",
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
