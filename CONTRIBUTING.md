# Contributing to MIP

MIP is a specification, not a library — the bar for changing it is higher than for changing
code, because every RP and Client implementation depends on the wire behavior staying stable.

## Proposing a change

1. **Open an issue first** describing the problem or gap, before writing a PR. Point to the
   specific section(s) of [`docs/spec/index.md`](docs/spec/index.md) affected. A PR that
   changes normative text without a preceding issue discussion will be asked to split into
   one.
2. Classify the change against §12 (Versioning & Extensibility) before proposing wording:
   - **Editorial** (typo, clarification that doesn't change any MUST/SHOULD/MAY): no version
     bump required.
   - **Minor** (new optional endpoint, optional field, optional discovery field): bumps
     `MINOR`. Must not change the meaning of an existing required field.
   - **Major** (any breaking wire change): bumps `MAJOR`. Needs the strongest justification —
     this breaks every existing implementation.
3. If the change touches a wire shape, update the matching file(s) under `schemas/` and add
   or update an example under `examples/` (registered in `examples/manifest.json`). A PR that
   changes spec prose without updating the schema/example is incomplete — CI enforces this
   via `scripts/validate_examples.py`.
4. Add a `CHANGELOG.md` entry under an `[Unreleased]` heading.
5. If the change adds or renumbers a section, run `python scripts/check_references.py`
   locally — a renumbered section silently breaking a `§x.y` cross-reference elsewhere in the
   document is the most common way this spec would quietly rot.

## Normative language

Use RFC 2119 keywords (MUST, MUST NOT, REQUIRED, SHOULD, SHOULD NOT, MAY) deliberately and
bold them, exactly as the rest of the spec does. `scripts/check_rfc2119.py` runs in CI as an
advisory (non-blocking) check for a lowercase `must`/`should`/`may`/`shall` outside that
convention — it will not fail your PR, but a reviewer will ask about a flagged line.

## Decision process

There's a single maintainer ([@Deftu](https://github.com/Deftu)) making the final call on
normative changes for now. This isn't a permanent stance — if/when other implementers are
depending on MIP in production, this section will describe a real review/sign-off process
instead. Until then: open the issue, make the case, expect scrutiny proportional to whether
the change is editorial, minor, or major.

## Local checks

```
pip install -r requirements.txt
python scripts/validate_examples.py
python scripts/check_references.py
python scripts/check_rfc2119.py
pymarkdown --config .pymarkdown.json scan -r docs/ README.md CONTRIBUTING.md SECURITY.md CHANGELOG.md
mkdocs build --strict
```

These are the same checks CI runs (`.github/workflows/ci.yml`) — run them before opening a
PR.
