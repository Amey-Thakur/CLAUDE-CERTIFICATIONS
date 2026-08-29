#!/usr/bin/env python3
"""Check every practice and mock question for structural defects.

The markdown is the human-readable source of truth. mock_exam.py and the site
quiz shuffle at run time, so the file itself should always present options in
order. It did not: 150 questions across eight files had their option lines out
of sequence, which makes a reader hunt for the option they want and looks like
carelessness in a resource whose whole claim is care.

This checks four things per question:

  order       options run A, B, C, D
  letters     no gaps and no duplicates
  answer      the answer key names a letter the question actually offers
  coverage    every question in the markdown reaches question-bank.json

    python .github/scripts/check_questions.py

Exits non-zero on any defect.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
OPTION = re.compile(r"^- ([A-D])\. (.+)$")
# Two heading shapes are in use: "**13.** text" in the mock exams and
# "**1. Domain name.** text" in the practice sets. Matching only the number and
# its full stop covers both; anything narrower catches one set and silently
# skips the other, which is how a first attempt counted 180 of 320.
QUESTION = re.compile(r"^\*\*(\d+)\.")
KEY_ROW = re.compile(r"^\|\s*(\d+)\s*\|\s*([A-D](?:\s*,\s*[A-D])*)\s*\|")
# The practice sets put the answer in a details block instead of a key table.
INLINE_ANSWER = re.compile(r"^\*\*([A-D](?:\s*(?:and|,)\s*[A-D])*)\.\*\*")


def questions_in(path):
    """Yield (number, [letters]) for each question block in a markdown file."""
    lines = path.read_text(encoding="utf-8").splitlines()
    number, letters = None, []
    for line in lines:
        q = QUESTION.match(line)
        if q:
            if number is not None:
                yield number, letters
            number, letters = int(q.group(1)), []
            continue
        o = OPTION.match(line)
        if o and number is not None:
            letters.append(o.group(1))
    if number is not None:
        yield number, letters


def answer_key(path):
    """Question number to the letters marked correct, in either notation.

    Mock exams carry a key table at the end; practice sets put the answer in a
    details block under each question. Both are read, so neither format escapes
    the check.
    """
    out, current = {}, None
    for line in path.read_text(encoding="utf-8").splitlines():
        q = QUESTION.match(line)
        if q:
            current = int(q.group(1))
            continue
        m = KEY_ROW.match(line)
        if m:
            out[int(m.group(1))] = [c.strip() for c in m.group(2).split(",")]
            continue
        inline = INLINE_ANSWER.match(line)
        if inline and current is not None and current not in out:
            out[current] = re.findall(r"[A-D]", inline.group(1))
    return out


def main():
    problems, checked = [], 0
    files = sorted(p for p in ROOT.rglob("*.md")
                   if re.search(r"(practice-questions|mock-exam-\d)\.md$", p.name))

    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        key = answer_key(path)
        for number, letters in questions_in(path):
            if not letters:
                continue
            checked += 1
            where = f"{rel} Q{number}"
            if letters != sorted(letters):
                problems.append(f"{where}: options run {','.join(letters)}, not in order")
            if len(set(letters)) != len(letters):
                problems.append(f"{where}: duplicate option letter")
            expected = [chr(ord('A') + i) for i in range(len(letters))]
            if sorted(set(letters)) != expected:
                problems.append(
                    f"{where}: letters {','.join(sorted(set(letters)))}, expected "
                    f"{','.join(expected)}")
            for answer in key.get(number, []):
                if answer not in letters:
                    problems.append(
                        f"{where}: answer key says {answer}, which the question "
                        f"does not offer")

    bank = json.loads((ROOT / "question-bank.json").read_text(encoding="utf-8"))
    print(f"  {checked} questions in {len(files)} files, "
          f"{len(bank['questions'])} in question-bank.json")
    if len(bank["questions"]) != checked:
        problems.append(
            f"question-bank.json holds {len(bank['questions'])} questions but the "
            f"markdown has {checked}; run build_question_bank.py")

    for p in problems:
        print(f"  FAIL  {p}")
    if problems:
        print(f"\n  {len(problems)} defect(s).")
        return 1
    print("  every question is in order, fully lettered, and keyed to a real option.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
