#!/usr/bin/env python3
"""Run a shuffled, timed mock exam from question-bank.json.

Every run draws a different sample and shuffles the option order, so nothing
can be memorized by position. Scores are reported with a per-domain breakdown
in the style of the real score report. Standard library only.

Usage:
    python .github/scripts/mock_exam.py                       # 15 questions, pick exam
    python .github/scripts/mock_exam.py --exam developer-foundations --count 25
    python .github/scripts/mock_exam.py --exam architect-foundations --domain "Tool Design"
    python .github/scripts/mock_exam.py --review              # answers shown as you go
    python .github/scripts/mock_exam.py --seed 7              # reproducible run
"""

import argparse
import json
import random
import time
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BANK = REPO_ROOT / "question-bank.json"
LETTERS = "ABCD"


def load_bank():
    if not BANK.exists():
        raise SystemExit("question-bank.json not found. Run build_question_bank.py first.")
    return json.loads(BANK.read_text(encoding="utf-8"))


def choose_exam(bank, requested):
    slugs = list(bank["exams"])
    if requested:
        matches = [s for s in slugs if requested.lower() in s]
        if len(matches) == 1:
            return matches[0]
        raise SystemExit(f"Unknown exam {requested!r}. Choose from: {', '.join(slugs)}")
    print("\nWhich exam?\n")
    for i, slug in enumerate(slugs, 1):
        print(f'  {i}. {bank["exams"][slug]["title"]}')
    while True:
        pick = input("\nNumber: ").strip()
        if pick.isdigit() and 1 <= int(pick) <= len(slugs):
            return slugs[int(pick) - 1]


def shuffle_options(question, rng):
    """Return options in a fresh order with the correct letter remapped."""
    items = [(letter, text) for letter, text in sorted(question["options"].items())]
    rng.shuffle(items)
    options, answer = {}, None
    for new_letter, (old_letter, text) in zip(LETTERS, items):
        options[new_letter] = text
        if old_letter == question["answer"]:
            answer = new_letter
    return options, answer


def run():
    parser = argparse.ArgumentParser(description="Shuffled mock exam from the question bank.")
    parser.add_argument("--exam", help="exam slug or fragment, for example 'developer'")
    parser.add_argument("--count", type=int, default=15, help="number of questions (default 15)")
    parser.add_argument("--domain", help="restrict to domains containing this text")
    parser.add_argument("--review", action="store_true", help="show the answer after each question")
    parser.add_argument("--seed", type=int, help="fix the shuffle for a reproducible run")
    args = parser.parse_args()

    bank = load_bank()
    rng = random.Random(args.seed)
    slug = choose_exam(bank, args.exam)

    pool = [q for q in bank["questions"] if q["exam"] == slug]
    if args.domain:
        pool = [q for q in pool if args.domain.lower() in q["domain"].lower()]
        if not pool:
            raise SystemExit(f"No questions match domain {args.domain!r}")

    count = min(args.count, len(pool))
    questions = rng.sample(pool, count)

    title = bank["exams"][slug]["title"]
    minutes = max(5, round(count * 2))
    print(f"\n{title}")
    print(f"{count} questions drawn from a pool of {len(pool)}, about {minutes} minutes.")
    print("Answer with A, B, C, or D. Enter S to skip, Q to stop early.\n")
    input("Press Enter to start. ")

    started = time.time()
    results = []
    for index, question in enumerate(questions, 1):
        options, answer = shuffle_options(question, rng)
        print(f"\n{'-' * 68}\nQuestion {index} of {count}\n")
        print(question["question"] + "\n")
        for letter in LETTERS:
            print(f"  {letter}. {options[letter]}")
        while True:
            reply = input("\nYour answer: ").strip().upper()
            if reply in ("A", "B", "C", "D", "S", "Q"):
                break
            print("Enter A, B, C, D, S to skip, or Q to stop.")
        if reply == "Q":
            print("\nStopping early.")
            break
        correct = reply == answer
        results.append({"q": question, "given": reply, "answer": answer, "correct": correct,
                        "options": options})
        if args.review:
            verdict = "Correct" if correct else f"Incorrect. The answer is {answer}"
            print(f"\n  {verdict}. {question['rationale']}")

    elapsed = time.time() - started
    report(results, elapsed, title, args.review)


def report(results, elapsed, title, reviewed):
    if not results:
        print("\nNo questions answered.")
        return
    right = sum(1 for r in results if r["correct"])
    total = len(results)
    percent = round(100 * right / total)

    print(f"\n{'=' * 68}\n{title}: {right} of {total} correct ({percent}%)")
    print(f"Time: {int(elapsed // 60)}m {int(elapsed % 60)}s\n")

    by_domain = defaultdict(lambda: [0, 0])
    for r in results:
        stats = by_domain[r["q"]["domain"]]
        stats[1] += 1
        stats[0] += 1 if r["correct"] else 0
    print("By domain, as the real score report breaks it down:\n")
    width = max(len(d) for d in by_domain)
    for domain, (got, asked) in sorted(by_domain.items(), key=lambda kv: kv[1][0] / kv[1][1]):
        print(f"  {domain.ljust(width)}  {got}/{asked}")

    weak = [d for d, (got, asked) in by_domain.items() if got / asked < 0.7]
    if weak:
        print("\nStudy next: " + "; ".join(sorted(weak)))

    if not reviewed:
        missed = [r for r in results if not r["correct"]]
        if missed and input(f"\nReview the {len(missed)} you missed? [y/N] ").strip().lower() == "y":
            for r in missed:
                print(f"\n{'-' * 68}\n{r['q']['question']}\n")
                for letter in LETTERS:
                    mark = "correct" if letter == r["answer"] else ("your answer" if letter == r["given"] else "")
                    print(f"  {letter}. {r['options'][letter]}" + (f"   <- {mark}" if mark else ""))
                print(f"\n  {r['q']['rationale']}")

    print("\nThis is a study aid. The real exam reports a scaled score from 100 to 1,000, passing at 720.")


if __name__ == "__main__":
    try:
        run()
    except (KeyboardInterrupt, EOFError):
        print("\nStopped.")
