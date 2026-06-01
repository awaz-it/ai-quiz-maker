"""AI Quiz Maker from Notes - main CLI

Usage:
 - Run the script and paste or type/paste lecture notes.
 - Finish your paste with a line containing only END and press Enter.

The script will generate 5 MCQs, 5 True/False, and 5 Fill-in-the-blanks,
print them to the console, and save them to `quiz_output.json`.
"""
import json
import os
from pathlib import Path

from quiz_generator import generate_mcq, generate_true_false, generate_fill_blank


def read_multiline_input(end_token: str = "END") -> str:
    print("Paste your lecture notes below. When finished, type a line with only 'END' and press Enter:")
    lines = []
    try:
        while True:
            line = input()
            if line.strip() == end_token:
                break
            lines.append(line)
    except EOFError:
        # Allow EOF as alternative to END
        pass
    return "\n".join(lines)


def pretty_print_quiz(mcqs, tfs, blanks):
    print("\n===== Multiple Choice Questions (MCQ) =====\n")
    for i, q in enumerate(mcqs, 1):
        print(f"Q{i}: {q['question']}")
        for j, opt in enumerate(q['options']):
            letter = chr(ord('a') + j)
            marker = ' (correct)' if j == q['answer'] else ''
            print(f"  {letter}) {opt}{marker}")
        print()

    print("\n===== True / False =====\n")
    for i, t in enumerate(tfs, 1):
        ans = 'True' if t['answer'] else 'False'
        print(f"{i}. \"{t['statement']}\" → {ans}")

    print("\n===== Fill in the Blanks =====\n")
    for i, b in enumerate(blanks, 1):
        print(f"{i}. {b['question']}")
        print(f"   Answer: {b['answer']}\n")


def main():
    notes = read_multiline_input()
    if not notes.strip():
        print("No input detected. Exiting.")
        return

    mcqs = generate_mcq(notes, count=5)
    tfs = generate_true_false(notes, count=5)
    blanks = generate_fill_blank(notes, count=5)

    pretty_print_quiz(mcqs, tfs, blanks)

    out = {
        "mcq": mcqs,
        "true_false": tfs,
        "fill_in_blank": blanks,
    }

    out_path = Path(os.getcwd()) / "quiz_output.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(f"\nSaved quiz to: {out_path}")


if __name__ == "__main__":
    main()
