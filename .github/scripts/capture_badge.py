#!/usr/bin/env python3
"""Photograph a Claude Academy badge from its own verification page.

The badge artwork is not served as a file anywhere. It is drawn by the
verification page, so the only way to hold a copy is to open that page and take
a picture of the badge element itself.

Every badge in certificates/badges/ was captured this way and they have to
match, or the gallery is a row of pictures at slightly different sizes and
tones. The recipe is fixed: the page in dark mode, the badge element alone at
three times scale so the type stays sharp when it is scaled back down, resized
to 720 by 490, and composited onto the same near-black the page uses so the
rounded corners meet a matching ground instead of white.

    python .github/scripts/capture_badge.py <slug> <verification-code>

Writes certificates/badges/<slug>.png. Needs Playwright and Chrome.
"""

import sys
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
OUT = ROOT / "certificates" / "badges"
VERIFY = "https://academy.claude.com/verify/"

SIZE = (720, 490)
GROUND = (20, 20, 20)
SCALE = 3

CHROME = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]

# The badge is drawn as an inline SVG inside a rounded div, not served as an
# image, which is why there is no file to download and why every selector that
# looks for one finds nothing. Its natural size is 720 by 491, which is where
# the stored size comes from.
SELECTORS = ["div[class*='badge']", "svg", "img"]


def capture(slug, code):
    from PIL import Image
    from playwright.sync_api import sync_playwright

    browser = next((c for c in CHROME if Path(c).exists()), None)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=browser) if browser \
            else p.chromium.launch()
        page = b.new_page(viewport={"width": 1280, "height": 900},
                          device_scale_factor=SCALE, color_scheme="dark")
        page.goto(VERIFY + code, wait_until="networkidle", timeout=90000)
        page.wait_for_timeout(1800)
        shot = None
        for selector in SELECTORS:
            found = page.query_selector_all(selector)
            for element in found:
                box = element.bounding_box()
                if box and box["width"] > 200 and box["height"] > 120:
                    shot = element.screenshot()
                    break
            if shot:
                break
        b.close()

    if shot is None:
        raise SystemExit(f"  {slug}: no badge-sized image on that page")

    with Image.open(BytesIO(shot)) as raw:
        art = raw.convert("RGBA").resize(SIZE, Image.LANCZOS)
    ground = Image.new("RGB", SIZE, GROUND)
    ground.paste(art, (0, 0), art)
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / f"{slug}.png"
    ground.save(target, "PNG", optimize=True)
    print(f"  {slug}.png written, {SIZE[0]} by {SIZE[1]}")
    return 0


def main():
    if len(sys.argv) != 3:
        print(__doc__.strip().splitlines()[-3].strip())
        return 1
    return capture(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    sys.exit(main())
