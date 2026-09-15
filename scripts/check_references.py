#!/usr/bin/env python3
"""Verify every internal §N(.N)* / Appendix X(.N)* cross-reference in the spec resolves to
a real heading or Appendix C bullet label. A renumbered section silently breaking a
cross-reference elsewhere in the document is invisible in review and only found by a
confused implementer — this catches it at CI time instead.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "docs" / "spec" / "index.md"

# "## 5. Flow A ..." / "### 5.1 Challenge issuance" / "## 0. Status of this document"
HEADING_NUMBER_RE = re.compile(r"^#{2,3}\s+(\d+(?:\.\d+)?)\b")
# "## Appendix A — Discovery Document"
APPENDIX_HEADING_RE = re.compile(r"^#{2,3}\s+Appendix\s+([A-Z])\b")
# "- **C.1** —" style bullet labels used inside Appendix C
BULLET_LABEL_RE = re.compile(r"^\s*-\s+\*\*([A-Z]\.\d+)\*\*")

# References in prose: "§5.1", "§10.2's", "§0"
SECTION_REF_RE = re.compile(r"§(\d+(?:\.\d+)?)")
# "Appendix C", "Appendix C.2"
APPENDIX_REF_RE = re.compile(r"Appendix\s+([A-Z])(?:\.(\d+))?")
# bare "C.2" / "C.2's" mentions (only single uppercase letter + dot + digits)
BARE_LABEL_REF_RE = re.compile(r"(?<![A-Za-z0-9])([A-Z])\.(\d+)(?![0-9])")

# Known references to *external* documents that happen to look like our own numbering
# (e.g. "RFC 7519 §2" is RFC 7519's own §2, not this spec's).
EXTERNAL_REF_ALLOWLIST = {
    ("RFC 2119", None),
    ("RFC 3339", None),
    ("RFC 4122", None),
    ("RFC 7519", "2"),
}


def collect_valid_refs(lines: list[str]) -> tuple[set[str], set[str]]:
    section_numbers: set[str] = set()
    appendix_letters: set[str] = set()
    appendix_labels: set[str] = set()

    for line in lines:
        m = HEADING_NUMBER_RE.match(line)
        if m:
            section_numbers.add(m.group(1))
            continue
        m = APPENDIX_HEADING_RE.match(line)
        if m:
            appendix_letters.add(m.group(1))
            continue
        m = BULLET_LABEL_RE.match(line)
        if m:
            appendix_labels.add(m.group(1))

    return section_numbers, appendix_letters | appendix_labels


def find_broken_refs(text: str, lines: list[str]) -> list[str]:
    section_numbers, appendix_tokens = collect_valid_refs(lines)
    problems = []

    for i, line in enumerate(lines, start=1):
        if line.lstrip().startswith("#"):
            continue  # headings define refs, they don't consume them

        for m in SECTION_REF_RE.finditer(line):
            ref = m.group(1)
            if ref not in section_numbers:
                problems.append(f"line {i}: §{ref} does not match any heading")

        for m in APPENDIX_REF_RE.finditer(line):
            letter, sub = m.group(1), m.group(2)
            token = f"{letter}.{sub}" if sub else letter
            if letter not in appendix_tokens and token not in appendix_tokens:
                problems.append(f"line {i}: Appendix {token} does not match any heading/label")

        for m in BARE_LABEL_REF_RE.finditer(line):
            letter, sub = m.group(1), m.group(2)
            token = f"{letter}.{sub}"
            if token in EXTERNAL_REF_ALLOWLIST or (letter, None) in EXTERNAL_REF_ALLOWLIST:
                continue
            if token not in appendix_tokens:
                problems.append(f"line {i}: {token} does not match any Appendix heading/label")

    return problems


def main() -> int:
    if not SPEC.exists():
        print(f"FAILED — spec file not found: {SPEC}", file=sys.stderr)
        return 1

    text = SPEC.read_text(encoding="utf-8")
    lines = text.splitlines()
    problems = find_broken_refs(text, lines)

    if problems:
        print(f"FAILED — {len(problems)} broken cross-reference(s):", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1

    print("OK — every internal cross-reference resolves.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
