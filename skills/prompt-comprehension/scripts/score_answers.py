#!/usr/bin/env python3
"""Score comprehension-test outputs against an answer key.

Usage: score_answers.py <key.json> <output.txt>...

The key maps question letters to the correct option, e.g. {"a": "B", "b": "A"}.
Only lines after the last SCENARIOS marker count, so the restatement cannot
score by accident. The first answer given for a letter wins. An output showing
a tool call or an auto-activated capability is marked CONTAM: the model may have
read the key or other outputs, so its score is not evidence.
"""
import json
import re
import sys

SCENARIOS_MARKER = "SCENARIOS"
ANSWER_LINE = re.compile(r"^\W*([a-z])\s*[:.)]\s*\**\s*([ABC])\b")
ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;]*m")
CONTAMINATION_TELLS = ("╭", "auto-activated")


def parse_answers(text):
    answers = {}
    for line in text.rsplit(SCENARIOS_MARKER, 1)[-1].splitlines():
        match = ANSWER_LINE.match(line)
        if match and match.group(1) not in answers:
            answers[match.group(1)] = match.group(2)
    return answers


def main():
    with open(sys.argv[1]) as key_file:
        key = json.load(key_file)
    for path in sys.argv[2:]:
        with open(path) as output_file:
            text = ANSI_ESCAPE.sub("", output_file.read())
        answers = parse_answers(text)
        wrong = [f"{q}:{answers.get(q, '-')}!={want}" for q, want in key.items() if answers.get(q) != want]
        contam = " CONTAM" if any(tell in text for tell in CONTAMINATION_TELLS) else ""
        print(f"{path} {len(key) - len(wrong)}/{len(key)}{contam} wrong: {' '.join(wrong) or 'none'}")


if __name__ == "__main__":
    main()
