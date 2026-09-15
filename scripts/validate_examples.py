#!/usr/bin/env python3
"""Validate every schema in schemas/ against the JSON Schema meta-schema, then validate
every example in examples/manifest.json against its declared schema.
"""
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = ROOT / "schemas"
EXAMPLES_DIR = ROOT / "examples"
MANIFEST = EXAMPLES_DIR / "manifest.json"


def load_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def check_schemas_self_valid() -> list[str]:
    errors = []
    for schema_path in sorted(SCHEMAS_DIR.glob("*.schema.json")):
        schema = load_json(schema_path)
        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError as exc:
            errors.append(f"{schema_path.relative_to(ROOT)}: invalid schema: {exc.message}")
    return errors


def build_registry() -> Registry:
    resources = []
    for schema_path in SCHEMAS_DIR.glob("*.schema.json"):
        contents = load_json(schema_path)
        resource = Resource.from_contents(contents, default_specification=DRAFT202012)
        resources.append((contents["$id"], resource))
    return Registry().with_resources(resources)


def check_examples() -> list[str]:
    errors = []
    if not MANIFEST.exists():
        return [f"missing manifest: {MANIFEST.relative_to(ROOT)}"]

    manifest = load_json(MANIFEST)
    registry = build_registry()

    for entry in manifest.get("entries", []):
        example_path = ROOT / entry["example"]
        schema_path = ROOT / entry["schema"]

        if not example_path.exists():
            errors.append(f"{entry['example']}: file does not exist")
            continue
        if not schema_path.exists():
            errors.append(f"{entry['schema']}: file does not exist")
            continue

        schema = load_json(schema_path)
        example = load_json(example_path)
        validator = Draft202012Validator(schema, registry=registry)

        example_errors = sorted(validator.iter_errors(example), key=lambda e: list(e.path))
        for err in example_errors:
            location = "/".join(str(p) for p in err.path) or "<root>"
            errors.append(f"{entry['example']} ({location}): {err.message}")

    return errors


def main() -> int:
    errors = check_schemas_self_valid()
    errors += check_examples()

    if errors:
        print(f"FAILED — {len(errors)} issue(s):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    entry_count = len(load_json(MANIFEST).get("entries", []))
    schema_count = len(list(SCHEMAS_DIR.glob("*.schema.json")))
    print(f"OK — {schema_count} schema(s) self-valid, {entry_count} example(s) validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
