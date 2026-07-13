# Claude Report Remediation

- Status: Implemented with one user-owned decision still open
- Source: `2026-07-12-claude-report.txt`
- Date: 2026-07-12

## Finding disposition

| Claude finding | Action |
|---|---|
| JSON stored as `inspection-map.yml` | Renamed to `control/inspection-map.json`; all references and validation updated. |
| No session integration | Added `CLAUDE.md`, `AGENTS.md`, `.github/copilot-instructions.md`, `docs/INTEGRATION.md`, and `scripts/session_gate.py`. |
| Long constitution lacks repeatable summary | Added `docs/QUICK-REFERENCE.md`; it is explicitly non-canonical. |
| CI not visibly verifiable | Existing CI retained, extended with session-gate self-test and live start/check, and exposed with a README status badge. |
| No worked example | Added `docs/WORKED-EXAMPLE.md`. |
| License unresolved | Still open because only The User may choose legal permissions; added `docs/LICENSE-DECISION-GUIDE.md`. |
| BADASS lacks version metadata | Added user-authorized front matter with version, revision date, status, and owner. |
| Scope may overreach into casual conversation | Narrowed the formal-work rule to technical, project, repository, system, advice, and task-oriented work. |

## Enforcement boundary

The new adapters and session gate improve instruction loading and state evidence. The session attestation checks the branch, commit, required-file hashes, and clean/dirty worktree state. They cannot prove internal model honesty. Behavioral proof still requires direct evidence and the section compliance matrix.
