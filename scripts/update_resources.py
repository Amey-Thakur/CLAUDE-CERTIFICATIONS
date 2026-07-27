#!/usr/bin/env python3
"""Refresh the mirrored official PDFs from their canonical sources.

Downloads every document listed in RESOURCES, verifies it is a valid PDF,
and replaces the local copy only when the content actually changed.
Standard library only.

Usage:
    python scripts/update_resources.py          # download and update
    python scripts/update_resources.py --check  # report reachability only
"""

import hashlib
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

S3 = (
    "https://everpath-course-content.s3-accelerate.amazonaws.com/"
    "instructor%2F{instructor}%2Fpublic%2F{doc}"
)

RESOURCES = {
    "pdfs/exam-guides/claude-certified-associate-foundations-exam-guide.pdf": S3.format(
        instructor="6nizmqk8tpzpfjvt6qmmav7rh",
        doc="1783542847%2FClaude+Certified+Associate+%E2%80%93+Foundations+Exam+Guide.pdf",
    ),
    "pdfs/exam-guides/claude-certified-developer-foundations-exam-guide.pdf": S3.format(
        instructor="6nizmqk8tpzpfjvt6qmmav7rh",
        doc="1783542875%2FClaude+Certified+Developer+%E2%80%93+Foundations+Exam+Guide.pdf",
    ),
    "pdfs/exam-guides/claude-certified-architect-foundations-exam-guide.pdf": S3.format(
        instructor="6nizmqk8tpzpfjvt6qmmav7rh",
        doc="1783542750%2FClaude+Certified+Architect+%E2%80%93+Foundations+Exam+Guide.pdf",
    ),
    "pdfs/exam-guides/claude-certified-architect-professional-exam-guide.pdf": S3.format(
        instructor="6nizmqk8tpzpfjvt6qmmav7rh",
        doc="1783542810%2FClaude+Certified+Architect+%E2%80%93+Professional+Exam+Guide.pdf",
    ),
    "pdfs/policies/anthropic-certification-exam-policy.pdf": S3.format(
        instructor="34hhd92iyp94a0gtbr15cy5jk",
        doc="1782870704%2FAnthropic+Certification+Exam+Policy.pdf",
    ),
    "pdfs/policies/certification-terms-and-conditions.pdf": S3.format(
        instructor="34hhd92iyp94a0gtbr15cy5jk",
        doc="1782870634%2FCertification+Terms+and+Conditions.pdf",
    ),
    "pdfs/policies/claude-certification-exam-registration-guide.pdf": S3.format(
        instructor="6nizmqk8tpzpfjvt6qmmav7rh",
        doc="1783542947%2FClaude+Certification+Program+-+Exam+Registration+Guide.pdf",
    ),
}


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "claude-certifications-updater"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


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
        print("\nDone. If files changed: review them, update the dates in pdfs/README.md,")
        print("check the affected docs pages, and record the change in CHANGELOG.md.")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
