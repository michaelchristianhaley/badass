# BADASS

[![Validate repository](https://github.com/michaelchristianhaley/badass/actions/workflows/validate.yml/badge.svg)](https://github.com/michaelchristianhaley/badass/actions/workflows/validate.yml)

A recovery and realignment repository for an assistant after it has been a **BAD ASSISTANT**.

`BADASS.md` is the user-owned operating constitution. The rest of this repository helps an assistant prove that it has read the constitution, understood each section, inspected current state, corrected a failure, and returned to useful work without thrashing, drifting, guessing, or lying.

## Start here

After a serious assistant failure:

1. Let the native adapter load: [`CLAUDE.md`](CLAUDE.md), [`AGENTS.md`](AGENTS.md), or [Copilot instructions](.github/copilot-instructions.md).
2. Read [`BADASS.md`](BADASS.md) completely.
3. Read [`docs/QUICK-REFERENCE.md`](docs/QUICK-REFERENCE.md).
4. Read the active [`control/outline.md`](control/outline.md).
5. Read [`control/inspection-map.json`](control/inspection-map.json).
6. Use [`docs/RECOVERY-PROTOCOL.md`](docs/RECOVERY-PROTOCOL.md).
7. Complete the checks in [`docs/SECTION-COMPLIANCE-MATRIX.md`](docs/SECTION-COMPLIANCE-MATRIX.md).
8. Start the session gate and validate the repository with:

```bash
python3 scripts/session_gate.py --start
python3 scripts/validate_repository.py --check
```

The assistant does not edit `BADASS.md` unless The User explicitly grants a specific exception.

## What this repository does

- Defines the assistant behavior The User requires.
- Names hard fail states and unwanted behavior.
- Provides a deterministic recovery process after failure.
- Makes compliance observable rather than assumed.
- Maintains an inspectable outline, decision record, cull process, and archive.
- Validates repository structure and control coverage automatically.

## Repository map

| Path | Purpose |
|---|---|
| `BADASS.md` | User-owned governing rules. |
| `CLAUDE.md` | Claude Code session bootstrap. |
| `AGENTS.md` | OpenAI Codex and compatible agent bootstrap. |
| `.github/copilot-instructions.md` | GitHub Copilot repository instructions. |
| `docs/INTEGRATION.md` | Tool-specific context-loading instructions and limits. |
| `docs/QUICK-REFERENCE.md` | One-page repeated-session reference; non-canonical. |
| `docs/WORKED-EXAMPLE.md` | Demonstrated recovery from a realistic HARD FAIL. |
| `scripts/session_gate.py` | Local session-state attestation and stale-state detection. |
| `docs/RECOVERY-PROTOCOL.md` | Ordered recovery procedure after a bad-assistant event. |
| `docs/SECTION-COMPLIANCE-MATRIX.md` | Section-by-section proof of comprehension and compliance. |
| `docs/REPOSITORY-HEALTH.md` | Repository design, maintenance rules, and current GitHub best-practice basis. |
| `control/outline.md` | Active reality sandbox and progress record. |
| `control/inspection-map.json` | User-controlled file groups and operation mappings. |
| `control/decisions/` | Statused decision records. |
| `control/culls/` | Proposed and approved bad-information culls. |
| `control/archive/` | Verbatim material removed from active documents after approval. |
| `scripts/validate_repository.py` | Self-testing repository validator and local inventory generator. |
| `.github/` | Contribution, issue, ownership, and automated validation controls. |

## Generated local control files

The validator generates these local files:

```text
control/file-inventory.csv
control/unclassified-files.txt
```

They are intentionally ignored by Git. Tracking a file that contains its own current hash creates an impossible self-reference, and committing generated inventory makes it stale immediately. The active outline and Git history retain durable inspection evidence.

Generate them with:

```bash
python3 scripts/validate_repository.py --refresh
```

## Authority

The User controls:

- `BADASS.md`;
- the active outline;
- the inspection map;
- all persistent rules;
- all method or tool replacements;
- destructive work and culls;
- the repository license decision.

The assistant may inspect, validate, report conflicts, and suggest changes. It may not grant itself authority.

## Contributing and support

Read [`CONTRIBUTING.md`](CONTRIBUTING.md), [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md), [`SUPPORT.md`](SUPPORT.md), and [`SECURITY.md`](SECURITY.md).

## Integration

See [`docs/INTEGRATION.md`](docs/INTEGRATION.md) for current ChatGPT, Claude Code, Codex, GitHub Copilot, and generic-assistant setup.

## License status

No license has been selected. The decision remains with The User and is recorded in [`control/decisions/0004-license-selection.md`](control/decisions/0004-license-selection.md). A public GitHub repository is viewable, but no reuse license is implied.
