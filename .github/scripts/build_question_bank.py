#!/usr/bin/env python3
"""Build question-bank.json from the practice and mock exam markdown.

The markdown pages stay the human-readable source of truth; this produces the
machine-readable bank that mock_exam.py and the website quiz consume, so a
question is never written twice. Standard library only.

Usage:
    python .github/scripts/build_question_bank.py
    python .github/scripts/build_question_bank.py --check   # verify, do not write
"""

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

EXAMS = {
    "associate-foundations": "Claude Certified Associate - Foundations",
    "developer-foundations": "Claude Certified Developer - Foundations",
    "architect-foundations": "Claude Certified Architect - Foundations",
    "architect-professional": "Claude Certified Architect - Professional",
}

OPTION_RE = re.compile(r"^- ([A-D])\. (.+)$")


def parse_options(lines, start):
    """Collect consecutive option lines beginning at start."""
    options, i = {}, start
    while i < len(lines):
        m = OPTION_RE.match(lines[i].strip())
        if m:
            options[m.group(1)] = m.group(2).strip()
            i += 1
        elif options and lines[i].strip() == "":
            i += 1
        elif options:
            break
        else:
            i += 1
            if i - start > 4:
                break
    return options, i


def parse_practice(path, exam):
    """Practice pages label the domain inline and answer in a details block."""
    text = path.read_text(encoding="utf-8")
    blocks = re.split(r"\n(?=\*\*\d+\. )", text)
    questions = []
    for block in blocks:
        head = re.match(r"\*\*(\d+)\. ([^.*]+)\.\*\* (.+?)(?=\n)", block, re.S)
        if not head:
            continue
        lines = block.split("\n")
        options, _ = parse_options(lines, 0)
        ans = re.search(r"<details><summary>.*?</summary>\s*\n\s*\n\*\*([A-D])\.?\*\*\s*(.+?)\n\s*\n</details>", block, re.S)
        if not (options and ans):
            continue
        questions.append({
            "id": f"{exam}-practice-{head.group(1)}",
            "exam": exam,
            "source": "practice",
            "domain": head.group(2).strip(),
            "question": head.group(3).strip(),
            "options": options,
            "answer": ans.group(1),
            "rationale": " ".join(ans.group(2).split()),
        })
    return questions


def parse_mock(path, exam):
    """Mock pages hide the domain; answers live in a key table at the end."""
    text = path.read_text(encoding="utf-8")
    key = {}
    for row in re.finditer(r"^\| (\d+) \| ([A-D]) \| ([^|]+) \| ([^|]+) \|$", text, re.M):
        key[row.group(1)] = (row.group(2), row.group(3).strip(), row.group(4).strip())

    body = text.split("## Answer key")[0]
    blocks = re.split(r"\n(?=\*\*\d+\.\*\* )", body)
    questions = []
    for block in blocks:
        head = re.match(r"\*\*(\d+)\.\*\* (.+?)(?=\n)", block, re.S)
        if not head:
            continue
        num = head.group(1)
        if num not in key:
            continue
        options, _ = parse_options(block.split("\n"), 0)
        if not options:
            continue
        answer, domain, why = key[num]
        questions.append({
            "id": f"{exam}-mock-{num}",
            "exam": exam,
            "source": "mock",
            "domain": domain,
            "question": head.group(2).strip(),
            "options": options,
            "answer": answer,
            "rationale": why,
        })
    return questions


def build():
    bank = {"exams": {}, "questions": []}
    for slug, title in EXAMS.items():
        folder = REPO_ROOT / slug
        found = []
        found += parse_practice(folder / "practice-questions.md", slug)
        found += parse_mock(folder / "mock-exam.md", slug)
        bank["exams"][slug] = {"title": title, "count": len(found)}
        bank["questions"] += found
    return bank


def main() -> int:
    bank = build()
    problems = []
    for q in bank["questions"]:
        if len(q["options"]) != 4:
            problems.append(f'{q["id"]}: {len(q["options"])} options')
        if q["answer"] not in q["options"]:
            problems.append(f'{q["id"]}: answer {q["answer"]} not among options')
        if not q["rationale"]:
            problems.append(f'{q["id"]}: empty rationale')
    for slug, meta in bank["exams"].items():
        if meta["count"] < 25:
            problems.append(f'{slug}: only {meta["count"]} questions parsed')

    for slug, meta in bank["exams"].items():
        print(f'{slug}: {meta["count"]} questions')
    print(f'total: {len(bank["questions"])}')

    if problems:
        print("\nproblems:")
        print("\n".join(problems))
        return 1

    if "--check" not in sys.argv:
        out = REPO_ROOT / "question-bank.json"
        out.write_text(json.dumps(bank, indent=1) + "\n", encoding="utf-8")
        print(f"wrote {out.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
