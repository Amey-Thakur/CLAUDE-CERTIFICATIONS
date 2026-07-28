#!/usr/bin/env python3
"""Refresh the mirrored official PDFs from their canonical sources.

Downloads every document listed in RESOURCES, verifies it is a valid PDF,
and replaces the local copy only when the content actually changed.
Standard library only.

Usage:
    python .github/scripts/update_resources.py          # download and update
    python .github/scripts/update_resources.py --check  # report reachability only
"""

import hashlib
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

S3 = (
    "https://everpath-course-content.s3-accelerate.amazonaws.com/"
    "instructor%2F{instructor}%2Fpublic%2F{doc}"
)

RESOURCES = {
    "associate-foundations/exam-guide.pdf": S3.format(
        instructor="6nizmqk8tpzpfjvt6qmmav7rh",
        doc="1783542847%2FClaude+Certified+Associate+%E2%80%93+Foundations+Exam+Guide.pdf",
    ),
    "developer-foundations/exam-guide.pdf": S3.format(
        instructor="6nizmqk8tpzpfjvt6qmmav7rh",
        doc="1783542875%2FClaude+Certified+Developer+%E2%80%93+Foundations+Exam+Guide.pdf",
    ),
    "architect-foundations/exam-guide.pdf": S3.format(
        instructor="6nizmqk8tpzpfjvt6qmmav7rh",
        doc="1783542750%2FClaude+Certified+Architect+%E2%80%93+Foundations+Exam+Guide.pdf",
    ),
    "architect-professional/exam-guide.pdf": S3.format(
        instructor="6nizmqk8tpzpfjvt6qmmav7rh",
        doc="1783542810%2FClaude+Certified+Architect+%E2%80%93+Professional+Exam+Guide.pdf",
    ),
    "guide/anthropic-certification-exam-policy.pdf": S3.format(
        instructor="34hhd92iyp94a0gtbr15cy5jk",
        doc="1782870704%2FAnthropic+Certification+Exam+Policy.pdf",
    ),
    "guide/certification-terms-and-conditions.pdf": S3.format(
        instructor="34hhd92iyp94a0gtbr15cy5jk",
        doc="1782870634%2FCertification+Terms+and+Conditions.pdf",
    ),
    "guide/exam-registration-guide.pdf": S3.format(
        instructor="6nizmqk8tpzpfjvt6qmmav7rh",
        doc="1783542947%2FClaude+Certification+Program+-+Exam+Registration+Guide.pdf",
    ),
}


MAX_BYTES = 32 * 1024 * 1024


def fetch(url: str) -> bytes:
    """Download one mirrored document.

    Two guards, because this writes into the repository from the network. The
    response is capped so a misbehaving host cannot exhaust memory, and the
    URL that actually served the bytes has to still be HTTPS: redirects are
    followed by default, and a redirect to plaintext would let anything on the
    path substitute the document.
    """
    if not url.lower().startswith("https://"):
        raise OSError(f"refusing a non-HTTPS source: {url}")
    request = urllib.request.Request(url, headers={"User-Agent": "claude-certifications-updater"})
    with urllib.request.urlopen(request, timeout=60) as response:
        if not response.geturl().lower().startswith("https://"):
            raise OSError(f"redirected off HTTPS to {response.geturl()}")
        data = response.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise OSError(f"response exceeds {MAX_BYTES // 1024 // 1024} MB")
    return data


def main() -> int:
    check_only = "--check" in sys.argv
    failures = 0

    for relative_path, url in RESOURCES.items():
        local = REPO_ROOT / relative_path
        label = relative_path.split("/")[-1]

        try:
            data = fetch(url)
        except OSError as error:
            print(f"FAIL      {label}: {error}")
            failures += 1
            continue

        if not data.startswith(b"%PDF"):
            print(f"FAIL      {label}: response is not a PDF ({len(data)} bytes)")
            failures += 1
            continue

        if check_only:
            print(f"ok        {label}: reachable, {len(data)} bytes")
            continue

        new_hash = hashlib.sha256(data).hexdigest()
        old_hash = hashlib.sha256(local.read_bytes()).hexdigest() if local.exists() else None

        if new_hash == old_hash:
            print(f"unchanged {label}")
        else:
            local.parent.mkdir(parents=True, exist_ok=True)
            local.write_bytes(data)
            state = "updated" if old_hash else "added"
            print(f"{state.upper():9} {label}: {len(data)} bytes, sha256 {new_hash[:12]}")

    if failures:
        print(f"\n{failures} document(s) failed. If a source URL moved, find the new link on")
        print("https://anthropic-partners.skilljar.com/page/partner-certifications and update RESOURCES.")
    elif not check_only:
        print("\nDone. If files changed: review them, update the dates in guide/official-sources.md,")
        print("check the affected docs pages, and note the change in the next release.")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
