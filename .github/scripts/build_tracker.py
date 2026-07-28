#!/usr/bin/env python3
"""Generate the data behind the study progress tracker.

The tracker weights each domain by its share of the real exam, so progress
reflects how much of the paper you have actually covered rather than how many
boxes you have ticked. Milestones come from the preparation guidance every
official exam guide gives.

    python .github/scripts/build_tracker.py

Standard library only.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_images import ASSETS, CERTS  # noqa: E402

OUT = ASSETS / "tracker.json"

NAMES = {
    "associate-foundations": "Claude Certified Associate - Foundations",
    "developer-foundations": "Claude Certified Developer - Foundations",
    "architect-foundations": "Claude Certified Architect - Foundations",
    "architect-professional": "Claude Certified Architect - Professional",
}

MILESTONES = [
    "Read the exam guide end to end",
    "Turn the blueprint into a red, amber, green checklist",
    "Work the prep courses for this exam",
    "Build the thing the guide asks you to build",
    "Work the official sample questions and their rationales",
    "Score 80% or better on a timed mock exam",
    "Run the OnVUE system test on the machine you will use",
    "Book the exam",
]


def main() -> int:
    data = {"exams": {}}
    for cert in CERTS:
        data["exams"][cert["slug"]] = {
            "title": NAMES[cert["slug"]],
            "code": cert["code"],
            "accent": cert["accent"],
            "domains": [{"name": name, "weight": weight} for name, weight in cert["domains"]],
            "milestones": MILESTONES,
        }
    OUT.write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8")
    total = sum(len(e["domains"]) for e in data["exams"].values())
    print(f"{OUT.name}: {len(data['exams'])} exams, {total} domains, {len(MILESTONES)} milestones each")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
