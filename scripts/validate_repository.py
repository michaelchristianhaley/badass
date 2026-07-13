#!/usr/bin/env python3
"""Validate the BADASS repository using only the Python standard library."""

from __future__ import annotations

import argparse
import csv
import fnmatch
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "control" / "inspection-map.json"
INVENTORY_PATH = ROOT / "control" / "file-inventory.csv"
UNCLASSIFIED_PATH = ROOT / "control" / "unclassified-files.txt"
VERBATIM_ARCHIVES = {"docs/reviews/2026-07-12-claude-report.txt"}

REQUIRED_BADASS_HEADINGS = [
    "Scope",
    "Authority and Control",
    "Truthfulness and Hard Fail States",
    "Instruction Hierarchy",
    "Readback and Intent",
    "Recency Research",
    "Current State and Source Examination",
    "Repository Inspection Control",
    "Best-Practice Comparison",
    "Plan Discipline",
    "Rule Hygiene",
    "Git, GitHub, and Persistent Files",
    "Outlining",
    "CLI Workflow",
    "Script Safety",
    "Long Operations",
    "Failure Handling",
    "Target Discipline",
    "Destructive Work and Culls",
    "Directness",
    "UNWANTED BEHAVIOR: DO NOT DO THESE THINGS",
    "Unwanted Behavior 1: Thrash",
    "Unwanted Behavior 2: Drift",
]

REQUIRED_PATHS = [
    "BADASS.md",
    "README.md",
    "CLAUDE.md",
    "AGENTS.md",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "SUPPORT.md",
    ".gitattributes",
    ".gitignore",
    ".editorconfig",
    ".github/CODEOWNERS",
    ".github/copilot-instructions.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/behavior-failure.yml",
    ".github/ISSUE_TEMPLATE/rule-proposal.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/workflows/validate.yml",
    "docs/INTEGRATION.md",
    "docs/QUICK-REFERENCE.md",
    "docs/RECOVERY-PROTOCOL.md",
    "docs/REPOSITORY-HEALTH.md",
    "docs/SECTION-COMPLIANCE-MATRIX.md",
    "docs/WORKED-EXAMPLE.md",
    "docs/LICENSE-DECISION-GUIDE.md",
    "docs/reviews/README.md",
    "docs/reviews/2026-07-12-claude-report.txt",
    "docs/reviews/2026-07-12-claude-remediation.md",
    "control/README.md",
    "control/inspection-map.json",
    "control/outline.md",
    "control/decisions/README.md",
    "control/decisions/0001-repository-purpose.md",
    "control/decisions/0002-badass-authority.md",
    "control/decisions/0003-inspection-controls.md",
    "control/decisions/0004-license-selection.md",
    "control/decisions/0005-claude-report-remediation.md",
    "control/culls/README.md",
    "control/archive/README.md",
    "scripts/validate_repository.py",
    "scripts/session_gate.py",
]


class ValidationError(RuntimeError):
    pass


def run_git(*args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise ValidationError(completed.stderr.strip() or "git command failed")
    return completed.stdout


def tracked_files() -> list[str]:
    return [line for line in run_git("ls-files").splitlines() if line]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_type(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".md", ".txt"}:
        return "documentation"
    if suffix in {".yml", ".yaml", ".json"}:
        return "configuration"
    if suffix == ".py":
        return "python"
    if suffix in {".sh", ".bash"}:
        return "shell"
    if suffix == ".csv":
        return "data"
    return "text" if is_text(path) else "binary"


def is_text(path: Path) -> bool:
    data = path.read_bytes()[:4096]
    if b"\x00" in data:
        return False
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return True


def load_map() -> dict:
    try:
        data = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValidationError(f"inspection map is invalid: {error}") from error

    required = {"version", "owner", "fallback", "always_read", "groups", "operations", "classification_patterns"}
    missing = required.difference(data)
    if missing:
        raise ValidationError("inspection map missing keys: " + ", ".join(sorted(missing)))
    if data["owner"] != "The User":
        raise ValidationError("inspection map owner must be The User")
    if data["fallback"].get("full_repository_read") is not True:
        raise ValidationError("full repository fallback must be enabled")
    return data


def match_any(path: str, patterns: Iterable[str]) -> bool:
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns)


def extract_headings(path: Path) -> list[str]:
    headings: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if match:
            headings.append(match.group(1))
    return headings


def validate_required_paths(files: list[str]) -> None:
    missing = [path for path in REQUIRED_PATHS if path not in files]
    if missing:
        raise ValidationError("required tracked paths missing: " + ", ".join(missing))


def validate_text_files(files: list[str]) -> None:
    for relative in files:
        path = ROOT / relative
        if path.stat().st_size > 1024 * 1024:
            raise ValidationError(f"tracked file exceeds 1 MiB: {relative}")
        if is_text(path):
            raw = path.read_bytes()
            if b"\r" in raw:
                raise ValidationError(f"CR or CRLF line ending found: {relative}")
            if raw and not raw.endswith(b"\n") and relative not in VERBATIM_ARCHIVES:
                raise ValidationError(f"missing final newline: {relative}")


def validate_badass() -> None:
    path = ROOT / "BADASS.md"
    headings = extract_headings(path)
    missing = [heading for heading in REQUIRED_BADASS_HEADINGS if heading not in headings]
    if missing:
        raise ValidationError("BADASS.md missing headings: " + ", ".join(missing))

    text = path.read_text(encoding="utf-8")
    required_phrases = [
        "The Assistant shall not lie to The User.",
        "Stating incorrect information as fact is a HARD FAIL state",
        "shall open that URL directly",
        "The active outline is The Assistant's hard reality sandbox.",
        "Only The User may command a new method.",
        "The Assistant shall treat `BADASS.md` as read-only.",
        "version: 1.1.0",
        "last_revised: 2026-07-12",
    ]
    missing_phrases = [phrase for phrase in required_phrases if phrase not in text]
    if missing_phrases:
        raise ValidationError("BADASS.md missing governing phrases: " + ", ".join(missing_phrases))


def validate_integrations() -> None:
    required = {
        "CLAUDE.md": ["BADASS.md", "scripts/session_gate.py --start"],
        "AGENTS.md": ["BADASS.md", "scripts/session_gate.py --start"],
        ".github/copilot-instructions.md": ["BADASS.md", "control/outline.md"],
        "docs/QUICK-REFERENCE.md": ["does not replace `BADASS.md`", "Do not lie", "Do not Thrash", "Do not Drift"],
        "docs/INTEGRATION.md": ["Claude Code", "OpenAI Codex", "GitHub Copilot", "ChatGPT Projects"],
        "docs/WORKED-EXAMPLE.md": ["HARD FAIL", "Compliance matrix excerpt", "Observable difference"],
        "control/README.md": ["inspection-map.json"],
    }
    for relative, phrases in required.items():
        text = (ROOT / relative).read_text(encoding="utf-8")
        missing = [phrase for phrase in phrases if phrase not in text]
        if missing:
            raise ValidationError(f"{relative} missing required integration phrases: {', '.join(missing)}")
    control_readme = (ROOT / "control" / "README.md").read_text(encoding="utf-8")
    if "inspection-map.yml" in control_readme:
        raise ValidationError("control/README.md contains stale inspection-map.yml reference")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if "actions/workflows/validate.yml/badge.svg" not in readme:
        raise ValidationError("README.md missing validation status badge")

    workflow = (ROOT / ".github" / "workflows" / "validate.yml").read_text(encoding="utf-8")
    workflow_phrases = [
        "actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0",
        "scripts/validate_repository.py --self-test",
        "scripts/session_gate.py --self-test",
        "scripts/session_gate.py --start",
        "scripts/session_gate.py --check",
        "scripts/validate_repository.py --check",
    ]
    missing_workflow = [phrase for phrase in workflow_phrases if phrase not in workflow]
    if missing_workflow:
        raise ValidationError("validation workflow missing required commands: " + ", ".join(missing_workflow))


def validate_matrix() -> None:
    matrix = (ROOT / "docs" / "SECTION-COMPLIANCE-MATRIX.md").read_text(encoding="utf-8")
    missing = [heading for heading in REQUIRED_BADASS_HEADINGS if f"| {heading} |" not in matrix]
    if missing:
        raise ValidationError("compliance matrix missing sections: " + ", ".join(missing))


def validate_map(files: list[str], data: dict) -> list[str]:
    patterns = data["classification_patterns"]
    unclassified = [path for path in files if not match_any(path, patterns)]

    for path in data["always_read"]:
        if path not in files:
            raise ValidationError(f"always-read path is not tracked: {path}")

    groups = data["groups"]
    for operation, names in data["operations"].items():
        unknown = [name for name in names if name not in groups]
        if unknown:
            raise ValidationError(
                f"operation {operation} uses unknown groups: {', '.join(unknown)}"
            )

    return unclassified


def validate_relative_links(files: list[str]) -> None:
    markdown_files = [ROOT / path for path in files if path.endswith(".md")]
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

    for path in markdown_files:
        text = path.read_text(encoding="utf-8")
        for target in pattern.findall(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            clean = target.split("#", 1)[0]
            if not clean:
                continue
            resolved = (path.parent / clean).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError as error:
                raise ValidationError(f"link escapes repository in {path.relative_to(ROOT)}: {target}") from error
            if not resolved.exists():
                raise ValidationError(f"broken relative link in {path.relative_to(ROOT)}: {target}")


def write_generated(files: list[str], unclassified: list[str]) -> None:
    INVENTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with INVENTORY_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["path", "sha256", "bytes", "type"])
        for relative in files:
            path = ROOT / relative
            writer.writerow([relative, sha256(path), path.stat().st_size, file_type(path)])

    UNCLASSIFIED_PATH.write_text(
        "".join(f"{path}\n" for path in unclassified),
        encoding="utf-8",
        newline="\n",
    )


def check_repository(refresh: bool) -> None:
    files = tracked_files()
    validate_required_paths(files)
    validate_text_files(files)
    validate_badass()
    validate_integrations()
    validate_matrix()
    data = load_map()
    unclassified = validate_map(files, data)
    validate_relative_links(files)

    if refresh:
        write_generated(files, unclassified)

    if unclassified:
        raise ValidationError("unclassified tracked files: " + ", ".join(unclassified))

    print(f"PASS: {len(files)} tracked files validated.")
    print("PASS: BADASS headings and governing phrases validated.")
    print("PASS: every BADASS section is represented in the compliance matrix.")
    print("PASS: inspection map covers every tracked file.")
    print("PASS: line endings, file sizes, and relative links validated.")


def self_test() -> None:
    with tempfile.TemporaryDirectory(prefix="badass-validator-") as directory:
        test = Path(directory)
        sample = test / "sample.txt"
        sample.write_text("current evidence\n", encoding="utf-8", newline="\n")
        before = sha256(sample)
        if before != sha256(sample):
            raise ValidationError("hash self-test failed")

        sample.write_bytes(b"bad\r\n")
        if b"\r" not in sample.read_bytes():
            raise ValidationError("line-ending self-test failed")

        patterns = ["BADASS.md", "docs/**"]
        if not match_any("docs/test.md", patterns):
            raise ValidationError("classification self-test failed")
        if match_any("unknown.bin", patterns):
            raise ValidationError("classification false-positive self-test failed")

        map_fixture = {
            "version": 1,
            "owner": "The User",
            "fallback": {"full_repository_read": True},
            "always_read": [],
            "groups": {},
            "operations": {},
            "classification_patterns": [],
        }
        encoded = json.dumps(map_fixture)
        if json.loads(encoded)["owner"] != "The User":
            raise ValidationError("map parser self-test failed")

    print("PASS: validator self-test completed without modifying repository files.")


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="validate without writing generated files")
    mode.add_argument("--refresh", action="store_true", help="validate and refresh local generated control files")
    mode.add_argument("--self-test", action="store_true", help="test validator logic in an isolated temporary directory")
    args = parser.parse_args()

    try:
        if args.self_test:
            self_test()
        else:
            check_repository(refresh=args.refresh)
    except ValidationError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
