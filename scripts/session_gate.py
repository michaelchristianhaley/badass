#!/usr/bin/env python3
"""Generate and verify a local BADASS session-state attestation."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
ATTESTATION = ROOT / "control" / "session-attestation.json"
REQUIRED = [
    "BADASS.md",
    "docs/QUICK-REFERENCE.md",
    "control/outline.md",
    "control/inspection-map.json",
    "docs/SECTION-COMPLIANCE-MATRIX.md",
]


class GateError(RuntimeError):
    pass


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise GateError(result.stderr.strip() or "git command failed")
    return result.stdout.strip()


def metadata() -> dict[str, str]:
    lines = (ROOT / "BADASS.md").read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise GateError("BADASS.md has no version front matter")
    values: dict[str, str] = {}
    for line in lines[1:]:
        if line == "---":
            break
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip()
    for key in ("version", "last_revised", "status", "owner"):
        if not values.get(key):
            raise GateError(f"BADASS.md metadata missing {key}")
    return values


def build_attestation() -> dict:
    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            raise GateError(f"required session file missing: {relative}")
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "commit": git("rev-parse", "HEAD"),
        "branch": git("branch", "--show-current"),
        "worktree_clean": not bool(git("status", "--porcelain")),
        "badass": metadata(),
        "files": {relative: sha256(ROOT / relative) for relative in REQUIRED},
    }


def start() -> None:
    attestation = build_attestation()
    ATTESTATION.write_text(
        json.dumps(attestation, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print("PASS: BADASS session gate started.")
    print(f"Commit: {attestation['commit']}")
    print(f"BADASS version: {attestation['badass']['version']}")
    print(f"Attestation: {ATTESTATION.relative_to(ROOT)}")
    print("Required reading:")
    for relative in REQUIRED:
        print(f"  {relative}")


def check() -> None:
    if not ATTESTATION.is_file():
        raise GateError("session attestation missing; run --start")
    recorded = json.loads(ATTESTATION.read_text(encoding="utf-8"))
    current = build_attestation()
    if recorded.get("commit") != current["commit"]:
        raise GateError("session attestation commit is stale")
    if recorded.get("branch") != current["branch"]:
        raise GateError("session attestation branch is stale")
    if recorded.get("worktree_clean") != current["worktree_clean"]:
        raise GateError("session attestation worktree state is stale")
    if recorded.get("files") != current["files"]:
        raise GateError("session attestation file hashes are stale")
    print("PASS: session attestation matches current repository state.")


def self_test() -> None:
    with tempfile.TemporaryDirectory(prefix="badass-session-gate-") as directory:
        path = Path(directory) / "sample.txt"
        path.write_text("evidence\n", encoding="utf-8", newline="\n")
        first = sha256(path)
        if first != sha256(path):
            raise GateError("hash self-test failed")
        path.write_text("changed\n", encoding="utf-8", newline="\n")
        if first == sha256(path):
            raise GateError("stale-hash self-test failed")
    print("PASS: session-gate self-test completed without modifying repository files.")


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--start", action="store_true")
    modes.add_argument("--check", action="store_true")
    modes.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        if args.start:
            start()
        elif args.check:
            check()
        else:
            self_test()
    except (GateError, OSError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
