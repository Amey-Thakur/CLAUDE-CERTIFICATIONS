#!/usr/bin/env python3
"""Check that the citation metadata still matches the release it claims to describe.

CITATION.cff and codemeta.json both carry a version and a date. Nothing forces
them to be updated when a release is tagged, so they drift silently: a reader
who cites this repository gets a version number that was true three releases
ago, and the "Cite this repository" button hands them the wrong reference.

That is exactly what happened between v1.2.0 and v1.5.0, and neither file
complained, because they agreed with each other. Agreement is therefore not
enough on its own. This compares them to the newest tag as well.

Usage:
    python .github/scripts/check_metadata.py

The tag comparison is skipped when no tags are present, so a shallow checkout or
a fresh fork does not fail for a reason the author cannot fix. In CI, fetch tags
so the check actually runs.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def newest_tag():
    """The highest version tag, or None when the checkout has no tags."""
    try:
        out = subprocess.run(["git", "tag", "--list", "v*"], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    versions = []
    for line in out.split():
        raw = line.lstrip("v")
        if SEMVER.match(raw):
            versions.append(tuple(int(p) for p in raw.split(".")))
    if not versions:
        return None
    return ".".join(str(p) for p in max(versions))


def main():
    problems = []

    cff_text = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    cff_version = re.search(r'^version: "([^"]+)"', cff_text, re.M)
    cff_date = re.search(r'^date-released: "([^"]+)"', cff_text, re.M)
    header_date = re.search(r"^# Date: (\S+)", cff_text, re.M)

    meta = json.loads((ROOT / "codemeta.json").read_text(encoding="utf-8"))

    if not cff_version:
        problems.append("CITATION.cff has no version field")
    if not cff_date:
        problems.append("CITATION.cff has no date-released field")
    if problems:
        for p in problems:
            print(f"  FAIL  {p}")
        return 1

    cff_v, cff_d = cff_version.group(1), cff_date.group(1)
    meta_v, meta_d = meta.get("version"), meta.get("dateModified")

    for label, value in (("CITATION.cff version", cff_v),
                         ("codemeta.json version", meta_v)):
        if not value or not SEMVER.match(value):
            problems.append(f"{label} is not a semantic version: {value!r}")
    for label, value in (("CITATION.cff date-released", cff_d),
                         ("codemeta.json dateModified", meta_d)):
        if not value or not DATE.match(value):
            problems.append(f"{label} is not an ISO date: {value!r}")

    if cff_v != meta_v:
        problems.append(
            f"version disagrees: CITATION.cff says {cff_v}, codemeta.json says {meta_v}")

    # These two fields are not the same thing, and an earlier version of this
    # script wrongly demanded they match. `date-released` is when this version
    # was released and must not move afterwards; `dateModified` is when the
    # repository last changed and moves whenever anything is edited. The real
    # constraint is ordering.
    if meta_d < cff_d:
        problems.append(
            f"codemeta.json dateModified {meta_d} is before the release date "
            f"{cff_d}; the repository cannot have been modified before it shipped")
    if header_date and header_date.group(1) < cff_d:
        problems.append(
            f"CITATION.cff header comment says {header_date.group(1)}, "
            f"which is before date-released {cff_d}")
    if meta.get("dateCreated") and meta_d and meta["dateCreated"] > meta_d:
        problems.append(
            f"codemeta.json dateModified {meta_d} is before "
            f"dateCreated {meta['dateCreated']}")

    tag = newest_tag()
    if tag is None:
        print("  no tags in this checkout, so the release comparison is skipped")
    elif tag != cff_v:
        problems.append(
            f"newest tag is v{tag} but the metadata says {cff_v}. "
            f"Bump both files, or tag the release you meant to describe")
    else:
        print(f"  metadata matches the newest tag, v{tag}")

    for p in problems:
        print(f"  FAIL  {p}")
    if problems:
        print(f"\n  {len(problems)} problem(s).")
        return 1
    print(f"  version {cff_v}, dated {cff_d}, consistent across both files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
