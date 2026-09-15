#!/usr/bin/env python3
"""Advisory (non-blocking) scan for a lowercase must/should/may/shall/required that isn't
part of the bolded normative-keyword convention the rest of the spec uses. RFC 2119 prose
legitimately uses these words non-normatively too (e.g. "an attacker must guess"), so this
never fails CI — it prints a report for a human reviewer to glance at.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "docs" / "spec" / "index.md"

KEYWORDS = ("must not", "must", "shall not", "shall", "should not", "should", "may", "required")
# Longest-first so "must not" is checked before bare "must".
KEYWORDS = tuple(sorted(KEYWORDS, key=len, reverse=True))

WORD_RE = re.compile(
    r"\b(" + "|".join(re.escape(k) for k in KEYWORDS) + r")\b",
    re.IGNORECASE,
)


def main() -> int:
    if not SPEC.exists():
        print(f"spec file not found: {SPEC}", file=sys.stderr)
        return 0  # advisory only

    lines = SPEC.read_text(encoding="utf-8").splitlines()
    in_code_fence = False
    flagged = []

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_fence = not in_code_fence
            continue
        if in_code_fence or stripped.startswith(">") or "`" in line:
            continue

        for m in WORD_RE.finditer(line):
            word = m.group(1)
            if word.isupper() or word[0].isupper():
                continue  # "**MUST**"-style bolded keyword, or a capitalized label like "Required"
            flagged.append((i, word, line.strip()))

    if not flagged:
        print("OK — no un-bolded RFC 2119 keyword usage found.")
        return 0

    print(f"ADVISORY — {len(flagged)} lowercase normative-keyword-looking word(s) outside "
          f"the bolded convention (not a failure, just worth a human glance):")
    for lineno, word, content in flagged:
        print(f"  - line {lineno} ({word!r}): {content}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
