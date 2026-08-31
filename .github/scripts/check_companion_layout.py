#!/usr/bin/env python3
"""Check every companion page for content that overflows or overlaps.

The companion is fixed-size pages with `overflow: hidden`, so a page that has
grown too tall does not look broken. It looks finished, with the last line
quietly cut off. Reading the PDF cannot tell you that either, because the
missing content is simply not there.

So the check runs against the HTML in a real browser, where every element still
reports where it is: anything sticking out of the printable box is an overflow,
and any two leaf elements sharing pixels is an overlap.

    python .github/scripts/check_companion_layout.py

Needs Playwright and a Chrome. Exits non-zero on any page with either fault.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
HTML = ROOT / ".github" / "assets" / "companion.html"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_images import find_chrome  # noqa: E402

# The measurement runs in the page itself. Returning geometry rather than a
# verdict keeps the reporting here, where it can be read.
PROBE = """
() => {
  const mm = 96 / 25.4;
  const pages = [...document.querySelectorAll('section.page')];
  // A leaf is an element with no element children: the things that actually
  // paint. Comparing containers would report every parent as overlapping its
  // own child.
  const leaves = el => [...el.querySelectorAll('*')].filter(
    n => n.children.length === 0 && n.getBoundingClientRect().width > 0.5
                                 && n.getBoundingClientRect().height > 0.5);
  return pages.map((page, i) => {
    const pr = page.getBoundingClientRect();
    const cs = getComputedStyle(page);
    const pad = k => parseFloat(cs['padding' + k]);
    const box = {
      left: pr.left + pad('Left'), top: pr.top + pad('Top'),
      right: pr.right - pad('Right'), bottom: pr.bottom - pad('Bottom'),
    };
    // The footer and the top rule are placed against the page, not the
    // content box, so they are measured separately and excluded here.
    const skip = n => n.closest('.foot, .rule-top, .page-foot') !== null;
    const items = leaves(page).filter(n => !skip(n));

    const over = [];
    for (const n of items) {
      const r = n.getBoundingClientRect();
      const dx = Math.max(0, box.left - r.left, r.right - box.right);
      const dy = Math.max(0, box.top - r.top, r.bottom - box.bottom);
      if (dx > 1 || dy > 1) {
        over.push({
          tag: n.tagName, text: (n.textContent || n.alt || '').trim().slice(0, 60),
          rightBy: +(dx / mm).toFixed(2), belowBy: +(dy / mm).toFixed(2),
        });
      }
    }

    // Compare the boxes that are actually painted, not the bounding box. An
    // inline element running over several lines has a bounding box spanning
    // from the start of its first line to the end of its last, which encloses
    // whatever shares those lines with it. Comparing that reported every
    // "<strong>Term.</strong> <span>definition</span>" pair as an overlap.
    const boxes = items.map(n => [...n.getClientRects()].filter(
      r => r.width > 0.5 && r.height > 0.5));
    const hit = [];
    for (let a = 0; a < items.length; a++) {
      for (let b = a + 1; b < items.length; b++) {
        // Text inside its own container is not an overlap; it is containment.
        if (items[a].contains(items[b]) || items[b].contains(items[a])) continue;
        let worst = null;
        for (const ra of boxes[a]) for (const rb of boxes[b]) {
          const w = Math.min(ra.right, rb.right) - Math.max(ra.left, rb.left);
          const h = Math.min(ra.bottom, rb.bottom) - Math.max(ra.top, rb.top);
          // A hairline of shared edge is rounding, not an overlap. Anything a
          // reader could see is more than a third of a millimetre each way.
          if (w > mm / 3 && h > mm / 3 && (!worst || w * h > worst.w * worst.h)) {
            worst = {w, h};
          }
        }
        if (worst) {
          hit.push({
            a: items[a].tagName + ' ' + (items[a].textContent || items[a].alt || '').trim().slice(0, 34),
            b: items[b].tagName + ' ' + (items[b].textContent || items[b].alt || '').trim().slice(0, 34),
            w: +(worst.w / mm).toFixed(2), h: +(worst.h / mm).toFixed(2),
          });
        }
      }
    }
    return {
      n: i + 1, label: page.dataset.label || '', items: items.length,
      over, hit: hit.slice(0, 6), hits: hit.length,
    };
  });
}
"""


def main():
    if not HTML.exists():
        print(f"  no {HTML.relative_to(ROOT).as_posix()}; run build_companion.py first")
        return 1
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("  playwright is not installed; skipping the layout check")
        return 0

    # Prefer the Chrome the rest of the build already uses, so the measurement
    # is taken in the browser that renders the PDF. On a runner that has none,
    # Playwright's own build answers instead.
    chrome = find_chrome()
    launch = {"executable_path": str(chrome)} if chrome else {}

    with sync_playwright() as p:
        browser = p.chromium.launch(**launch)
        page = browser.new_page(viewport={"width": 1400, "height": 1000})
        page.goto(HTML.as_uri(), wait_until="load")
        page.wait_for_timeout(600)
        pages = page.evaluate(PROBE)
        browser.close()

    bad = 0
    for info in pages:
        if not info["over"] and not info["hits"]:
            continue
        bad += 1
        print(f"  page {info['n']} ({info['label']}), {info['items']} elements")
        for o in info["over"][:6]:
            where = []
            if o["rightBy"]:
                where.append(f"{o['rightBy']}mm past the side")
            if o["belowBy"]:
                where.append(f"{o['belowBy']}mm past the bottom")
            print(f"      OVERFLOW  {o['tag']} {o['text']!r} {' and '.join(where)}")
        for h in info["hit"]:
            print(f"      OVERLAP   {h['a']!r} over {h['b']!r} "
                  f"({h['w']}mm x {h['h']}mm)")
        if info["hits"] > len(info["hit"]):
            print(f"      ... and {info['hits'] - len(info['hit'])} more overlaps")

    if bad:
        print(f"\n  {bad} of {len(pages)} pages have a layout fault.")
        return 1
    print(f"  {len(pages)} pages: nothing overflows the printable box, "
          f"nothing overlaps.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
