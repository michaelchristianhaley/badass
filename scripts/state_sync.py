#!/usr/bin/env python3
"""Validate BADASS structured state and its exact outline mirror."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
import tempfile
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "control" / "state.json"
SCHEMA_PATH = ROOT / "schemas" / "state.schema.json"
OUTLINE_PATH = ROOT / "control" / "outline.md"
START = "<!-- BADASS-STATE:START -->"
END = "<!-- BADASS-STATE:END -->"


class StateError(RuntimeError):
    """Structured state is invalid or out of sync."""


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise StateError(f"cannot read JSON {path.relative_to(ROOT)}: {error}") from error


def type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    raise StateError(f"unsupported schema type: {expected}")


def validate_schema(value: Any, schema: dict[str, Any], path: str = "$") -> None:
    expected = schema.get("type")
    if expected is not None:
        allowed = [expected] if isinstance(expected, str) else expected
        if not isinstance(allowed, list) or not all(isinstance(item, str) for item in allowed):
            raise StateError(f"{path}: invalid type declaration in schema")
        if not any(type_matches(value, item) for item in allowed):
            raise StateError(f"{path}: expected {allowed}, got {type(value).__name__}")

    if "const" in schema and value != schema["const"]:
        raise StateError(f"{path}: expected constant {schema['const']!r}")

    if "enum" in schema and value not in schema["enum"]:
        raise StateError(f"{path}: {value!r} is not an allowed value")

    if isinstance(value, dict):
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        if not isinstance(properties, dict) or not isinstance(required, list):
            raise StateError(f"{path}: invalid object schema")
        missing = [key for key in required if key not in value]
        if missing:
            raise StateError(f"{path}: missing required keys: {', '.join(missing)}")
        if schema.get("additionalProperties") is False:
            extras = sorted(set(value).difference(properties))
            if extras:
                raise StateError(f"{path}: unexpected keys: {', '.join(extras)}")
        for key, child in value.items():
            if key in properties:
                child_schema = properties[key]
                if not isinstance(child_schema, dict):
                    raise StateError(f"{path}.{key}: invalid property schema")
                validate_schema(child, child_schema, f"{path}.{key}")

    if isinstance(value, list):
        minimum = schema.get("minItems")
        if minimum is not None and len(value) < minimum:
            raise StateError(f"{path}: expected at least {minimum} items")
        if schema.get("uniqueItems"):
            encoded = [json.dumps(item, sort_keys=True) for item in value]
            if len(encoded) != len(set(encoded)):
                raise StateError(f"{path}: items must be unique")
        item_schema = schema.get("items")
        if item_schema is not None:
            if not isinstance(item_schema, dict):
                raise StateError(f"{path}: invalid items schema")
            for index, item in enumerate(value):
                validate_schema(item, item_schema, f"{path}[{index}]")

    if isinstance(value, str):
        minimum = schema.get("minLength")
        if minimum is not None and len(value) < minimum:
            raise StateError(f"{path}: expected at least {minimum} characters")
        pattern = schema.get("pattern")
        if pattern is not None and re.fullmatch(pattern, value) is None:
            raise StateError(f"{path}: value does not match {pattern!r}")


def mirror_block(state: dict[str, Any]) -> str:
    return f"{START}\n```json\n{json.dumps(state, indent=2)}\n```\n{END}"


def extract_mirror(text: str) -> dict[str, Any]:
    if text.count(START) != 1 or text.count(END) != 1:
        raise StateError("outline must contain exactly one BADASS state mirror block")
    pattern = re.compile(
        re.escape(START) + r"\s*```json\s*(.*?)\s*```\s*" + re.escape(END),
        re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        raise StateError("outline state mirror is not fenced JSON")
    try:
        value = json.loads(match.group(1))
    except json.JSONDecodeError as error:
        raise StateError(f"outline state mirror is invalid JSON: {error}") from error
    if not isinstance(value, dict):
        raise StateError("outline state mirror must be an object")
    return value


def validate_current_state(state: dict[str, Any]) -> None:
    if state["branch"] != "main":
        raise StateError("state branch must be main")

    for name, relative in state["authoritative_paths"].items():
        if not (ROOT / relative).is_file():
            raise StateError(f"authoritative path {name} is missing: {relative}")

    licensed = (ROOT / "LICENSE.md").is_file()
    if licensed:
        if state["license_status"] != "selected":
            raise StateError("license_status must be selected when LICENSE.md exists")
        if any("license" in item.lower() for item in state["open_user_decisions"]):
            raise StateError("selected license cannot remain an open user decision")
    else:
        if state["license_status"] != "unresolved":
            raise StateError("license_status must be unresolved without LICENSE.md")
        if not any("license" in item.lower() for item in state["open_user_decisions"]):
            raise StateError("unresolved license must remain an open user decision")


def check() -> None:
    schema = load_json(SCHEMA_PATH)
    state = load_json(STATE_PATH)
    if not isinstance(schema, dict) or not isinstance(state, dict):
        raise StateError("schema and state roots must be objects")
    validate_schema(state, schema)
    validate_current_state(state)
    outline = OUTLINE_PATH.read_text(encoding="utf-8")
    mirror = extract_mirror(outline)
    if mirror != state:
        raise StateError("control/state.json does not match the outline state mirror")
    print("PASS: structured state is schema-valid and synchronized with the outline.")


def refresh() -> None:
    schema = load_json(SCHEMA_PATH)
    state = load_json(STATE_PATH)
    if not isinstance(schema, dict) or not isinstance(state, dict):
        raise StateError("schema and state roots must be objects")
    validate_schema(state, schema)
    validate_current_state(state)

    text = OUTLINE_PATH.read_text(encoding="utf-8")
    block = mirror_block(state)
    if START in text or END in text:
        pattern = re.compile(
            re.escape(START) + r".*?" + re.escape(END),
            re.DOTALL,
        )
        if len(pattern.findall(text)) != 1:
            raise StateError("cannot refresh malformed outline mirror markers")
        text = pattern.sub(block, text, count=1)
    else:
        text = text.rstrip() + "\n\n## Machine-readable state mirror\n\n" + block + "\n"
    OUTLINE_PATH.write_text(text, encoding="utf-8", newline="\n")
    print("PASS: outline state mirror refreshed from control/state.json.")


def self_test() -> None:
    schema = {
        "type": "object",
        "required": ["status", "items"],
        "additionalProperties": False,
        "properties": {
            "status": {"type": "string", "enum": ["active", "blocked"]},
            "items": {
                "type": "array",
                "minItems": 1,
                "uniqueItems": True,
                "items": {"type": "string", "minLength": 1},
            },
        },
    }
    valid = {"status": "active", "items": ["evidence"]}
    validate_schema(valid, schema)
    block = mirror_block(valid)
    if extract_mirror(block) != valid:
        raise StateError("mirror round-trip self-test failed")
    try:
        validate_schema({"status": "unknown", "items": []}, schema)
    except StateError:
        pass
    else:
        raise StateError("schema self-test failed to reject invalid state")
    with tempfile.TemporaryDirectory(prefix="badass-state-") as directory:
        path = Path(directory) / "state.json"
        path.write_text(json.dumps(valid), encoding="utf-8")
        if json.loads(path.read_text(encoding="utf-8")) != valid:
            raise StateError("JSON file self-test failed")
    print("PASS: state-sync self-test completed without modifying repository files.")


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--refresh", action="store_true")
    mode.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        if args.self_test:
            self_test()
        elif args.refresh:
            refresh()
        else:
            check()
    except (StateError, OSError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
