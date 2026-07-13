#!/usr/bin/env python3
"""Validate BADASS machine-readable compliance evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
import tempfile
from typing import Any

from state_sync import StateError, load_json, validate_schema

ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "control" / "compliance-matrix.json"
SCHEMA_PATH = ROOT / "schemas" / "compliance-matrix.schema.json"
ALLOWED = ["PASS", "FAIL", "ASK_USER", "NOT_APPLICABLE"]


class EvidenceError(RuntimeError):
    """Compliance evidence is invalid, incomplete, or overclaims proof."""


def badass_sections(path: Path | None = None) -> list[str]:
    source = path or (ROOT / "BADASS.md")
    sections: list[str] = []
    for line in source.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^#{1,2}\s+(.+?)\s*$", line)
        if match:
            sections.append(match.group(1))
    if not sections:
        raise EvidenceError("BADASS.md contains no governed sections")
    if len(sections) != len(set(sections)):
        raise EvidenceError("BADASS.md contains duplicate governed section headings")
    return sections


def resolve_evidence(reference: str) -> Path:
    relative = reference.split("#", 1)[0]
    if not relative:
        raise EvidenceError(f"empty evidence reference: {reference!r}")
    path = (ROOT / relative).resolve()
    try:
        path.relative_to(ROOT)
    except ValueError as error:
        raise EvidenceError(f"evidence escapes repository: {reference}") from error
    return path


def validate_rows(data: dict[str, Any], sections: list[str]) -> None:
    if data["allowed_statuses"] != ALLOWED:
        raise EvidenceError("allowed_statuses must exactly match the governed values")

    rows = data["rows"]
    names = [row["section"] for row in rows]
    if names != sections:
        missing = [section for section in sections if section not in names]
        extra = [section for section in names if section not in sections]
        raise EvidenceError(
            "matrix rows must exactly match BADASS sections in order; "
            f"missing={missing}, extra={extra}"
        )
    if len(names) != len(set(names)):
        raise EvidenceError("matrix contains duplicate section rows")

    for row in rows:
        section = row["section"]
        status = row["status"]
        evidence = row["evidence"]
        question = row["question"]
        remediation = row["remediation"]
        rationale = row["rationale"]

        for reference in evidence:
            if not resolve_evidence(reference).is_file():
                raise EvidenceError(
                    f"{section}: evidence path does not exist: {reference}"
                )

        if status == "PASS":
            if not evidence:
                raise EvidenceError(f"{section}: PASS requires direct evidence")
            if question is not None or remediation is not None:
                raise EvidenceError(
                    f"{section}: PASS cannot retain a question or remediation"
                )
        elif status == "FAIL":
            if not evidence:
                raise EvidenceError(f"{section}: FAIL requires direct evidence")
            if not remediation:
                raise EvidenceError(f"{section}: FAIL requires exact remediation")
            if question is not None:
                raise EvidenceError(f"{section}: FAIL cannot retain an open question")
        elif status == "ASK_USER":
            if not question:
                raise EvidenceError(f"{section}: ASK_USER requires an exact question")
            if not rationale:
                raise EvidenceError(f"{section}: ASK_USER requires a rationale")
            if remediation is not None:
                raise EvidenceError(
                    f"{section}: ASK_USER cannot assert remediation before judgment"
                )
        elif status == "NOT_APPLICABLE":
            if not rationale:
                raise EvidenceError(
                    f"{section}: NOT_APPLICABLE requires a specific rationale"
                )
            if question is not None or remediation is not None:
                raise EvidenceError(
                    f"{section}: NOT_APPLICABLE cannot retain a question or remediation"
                )
        else:
            raise EvidenceError(f"{section}: unsupported status {status!r}")


def check() -> None:
    schema = load_json(SCHEMA_PATH)
    matrix = load_json(MATRIX_PATH)
    if not isinstance(schema, dict) or not isinstance(matrix, dict):
        raise EvidenceError("schema and matrix roots must be objects")
    validate_schema(matrix, schema)
    validate_rows(matrix, badass_sections())

    counts = {status: 0 for status in ALLOWED}
    for row in matrix["rows"]:
        counts[row["status"]] += 1
    summary = ", ".join(f"{status}={counts[status]}" for status in ALLOWED)
    print(f"PASS: compliance evidence is schema-valid and complete ({summary}).")


def self_test() -> None:
    schema = {
        "type": "object",
        "required": ["allowed_statuses", "rows"],
        "additionalProperties": False,
        "properties": {
            "allowed_statuses": {
                "type": "array",
                "minItems": 4,
                "uniqueItems": True,
                "items": {"type": "string", "enum": ALLOWED},
            },
            "rows": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "required": [
                        "section",
                        "status",
                        "claim",
                        "evidence",
                        "question",
                        "remediation",
                        "rationale",
                    ],
                    "additionalProperties": False,
                    "properties": {
                        "section": {"type": "string", "minLength": 1},
                        "status": {"type": "string", "enum": ALLOWED},
                        "claim": {"type": "string", "minLength": 1},
                        "evidence": {
                            "type": "array",
                            "uniqueItems": True,
                            "items": {"type": "string", "minLength": 1},
                        },
                        "question": {"type": ["string", "null"]},
                        "remediation": {"type": ["string", "null"]},
                        "rationale": {"type": ["string", "null"]},
                    },
                },
            },
        },
    }
    valid = {
        "allowed_statuses": ALLOWED,
        "rows": [
            {
                "section": "Scope",
                "status": "ASK_USER",
                "claim": "Runtime compliance requires direct evidence.",
                "evidence": [],
                "question": "Does current direct evidence demonstrate compliance?",
                "remediation": None,
                "rationale": "Repository files cannot prove current session behavior.",
            }
        ],
    }
    validate_schema(valid, schema)
    validate_rows(valid, ["Scope"])

    invalid = json.loads(json.dumps(valid))
    invalid["rows"][0]["status"] = "PASS"
    invalid["rows"][0]["question"] = None
    invalid["rows"][0]["rationale"] = None
    try:
        validate_rows(invalid, ["Scope"])
    except EvidenceError:
        pass
    else:
        raise EvidenceError("self-test failed to reject PASS without evidence")

    invalid = json.loads(json.dumps(valid))
    invalid["rows"][0]["question"] = None
    try:
        validate_rows(invalid, ["Scope"])
    except EvidenceError:
        pass
    else:
        raise EvidenceError("self-test failed to reject ASK_USER without a question")

    with tempfile.TemporaryDirectory(prefix="badass-evidence-") as directory:
        source = Path(directory) / "BADASS.md"
        source.write_text("# Scope\n\n## Drift\n", encoding="utf-8", newline="\n")
        if badass_sections(source) != ["Scope", "Drift"]:
            raise EvidenceError("heading extraction self-test failed")

    print("PASS: evidence-check self-test completed without modifying repository files.")


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    try:
        self_test() if args.self_test else check()
    except (EvidenceError, StateError, OSError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
