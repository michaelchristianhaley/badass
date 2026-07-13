# BADASS Repository Outline

## Original plan

1. Preserve `BADASS.md` as The User's governing behavior document.
2. Realign an assistant after it has been a BAD ASSISTANT.
3. Make comprehension and compliance observable.
4. Maintain deterministic inspection controls.
5. Keep active truth current while preserving approved historical evidence.
6. Keep the repository small, healthy, testable, and useful.

The original plan shall not be rewritten without The User's explicit direction.

## Current end goal

A current, inspectable repository that can stop a failing assistant, force direct rereading and evidence, identify the violated rules, repair downstream damage, and return the assistant to the user's actual project without Thrash, Drift, guessing, or lying.

## Current state

- `BADASS.md` is user-owned and read-only to The Assistant unless The User grants a specific exception.
- The repository provides a recovery protocol and section compliance matrix.
- Repository inspection uses a user-controlled map and full-read fallback gates.
- Generated inventory and unclassified-file reports are local and reproducible.
- Repository structure is automatically validated.
- Native Claude Code, Codex, and GitHub Copilot adapters route assistants into BADASS.
- A session gate generates current local state evidence before work.
- `control/state.json` provides schema-validated state synchronized with this outline.
- A non-canonical quick reference and worked recovery example are available.
- Repository content is licensed CC BY 4.0; scripts and workflow code are licensed MIT.

## Current operation

Repository-health bootstrap.

- Inspected base commit: `82d63febe80f7bb30f5257c15e8c689f55a34873`
- Resulting commit: the commit containing this outline update.
- Best-practice comparison: current official GitHub repository, README, community-health, line-ending, and Actions guidance was reviewed.
- BADASS.md changed: no.
- Files inspected before the operation:
  - `BADASS.md`
  - `README.md`
- Files created or updated by the operation: every tracked file listed in the resulting commit except `BADASS.md`.

## Progress

- [x] Establish governing document.
- [x] Add truthfulness and hard-fail controls.
- [x] Add deterministic repository inspection design.
- [x] Add recovery protocol.
- [x] Add section compliance matrix.
- [x] Add repository health and community files.
- [x] Add automated validation.
- [x] The User selected CC BY 4.0 for repository content and MIT for scripts and workflow code.
- [x] Add native assistant integration and session-state verification.
- [x] Add schema-validated, merge-blocking structured state.
- [x] Add a one-page quick reference and worked recovery example.
- [x] Remediate the Claude repository report except the user-owned license decision.
- [ ] Future operations append verified progress here.

## Operating notes

Append future records below. Do not rewrite the original plan.

### Record template

- Date:
- Operation:
- Inspected base commit:
- Resulting commit:
- User command:
- Best-practice comparison:
- Files inspected:
- Actions:
- Verified results:
- Current-state changes:
- Failures or unknowns:
- Next goal:

### 2026-07-12: Claude report remediation

- Operation: Governance review and repository maintenance.
- Inspected base commit: live `main` containing `BADASS - Claude Report.txt`.
- Resulting commit: the commit containing this record.
- User command: Review Claude's report and implement its changes.
- Best-practice comparison: current official Claude Code `CLAUDE.md`, OpenAI Codex `AGENTS.md`, GitHub Copilot repository instructions, ChatGPT Projects, GitHub Actions checkout v7, and GitHub licensing guidance were checked.
- Files inspected: every tracked file because the new Claude report was unclassified and the outline was stale.
- Actions: renamed the JSON inspection map truthfully; added native adapters, integration documentation, quick reference, session gate, worked example, CI badge, remediation record, BADASS version metadata, and narrowed formal-work scope; extended validation and classification.
- Verified results: validator self-test, session-gate self-test, full repository check, and isolated commit/push smoke test.
- Current-state changes: BADASS version 1.1.0; inspection map version 2; report moved to `docs/reviews/` without content loss.
- Failures or unknowns: repository license remains a user-owned open decision.
- Next goal: The User selects whether and how the repository will be licensed.

### 2026-07-12 remaining live consistency repair

- Inspected base commit: `451ea65ba2757d588988f62222fc7d2a59b13086`
- Scope: fix only defects confirmed in the live repository after the Claude-remediation push
- Confirmed defects:
  - `control/README.md` still named the removed `inspection-map.yml`
  - the validation workflow used mutable `actions/checkout@v7`
  - the validator enforced those stale values instead of the corrected state
- Changes:
  - corrected the control index to `inspection-map.json`
  - pinned `actions/checkout` v7.0.0 to `9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0`
  - updated the validator to enforce both corrections
- Validation: validator self-test, session-gate self-test, repository check, Python parse, and Git diff checks passed before commit
- Preserved: `BADASS.md` unchanged; license decision untouched
- Next goal: verify the pushed commit and live GitHub files directly

### 2026-07-12 dual-license implementation

- Operation: implement the license decision selected by The User
- Inspected base commit: `2d47196af5085eb231a1d0d684871e3ba69f4fd2`
- User command: make number 1 — CC BY 4.0 for text and MIT for scripts
- Actions: added the license boundary and notices; accepted decision 0004;
  updated README and license guidance; classified and validated the new files
- Preserved: `BADASS.md` unchanged
- Verification: repository checks, Git checks, push, and remote SHA verification
- Next goal: wait for The User's next BADASS instruction

### 2026-07-12 structured-state control

- Operation: add schema-validated, merge-blocking current state.
- Inspected base commit: `6fe3d8ff415cd3b98d6f2ec7939220f9b1a24977`
- Resulting commit: the commit containing this record and `control/state.json`.
- User command: implement item 2 from the external review.
- Best-practice comparison: current JSON Schema and GitHub required-status-check guidance was reviewed.
- Actions:
  - added `control/state.json` and `schemas/state.schema.json`;
  - added an exact fenced state mirror to the active outline;
  - added the self-testing `scripts/state_sync.py` validator;
  - added the independent `state-sync` workflow;
  - required `validate` and `state-sync` before non-administrative merges;
  - kept administrator enforcement off so The User's direct Termux push workflow remains available;
  - updated session attestation, inspection coverage, documentation, and repository validation.
- Verified results: schema self-test, state/outline synchronization, session gate, repository validator, workflow run, remote SHA, and branch required contexts are checked by the deployment script.
- Current-state changes: BADASS version 1.2.0; structured state is now tracked and enforced.
- Failures or unknowns: none at commit time; runtime assistant truthfulness remains outside what a state file can prove.
- Next goal: continue only when The User directs the next BADASS operation.

## Machine-readable state mirror

<!-- BADASS-STATE:START -->
```json
{
  "$schema": "../schemas/state.schema.json",
  "schema_version": 1,
  "project": "BADASS",
  "branch": "main",
  "status": "active",
  "updated": "2026-07-12",
  "current_end_goal": "A current, inspectable repository that can stop a failing assistant, force direct rereading and evidence, identify the violated rules, repair downstream damage, and return the assistant to the user's actual project without Thrash, Drift, guessing, or lying.",
  "active_operation": {
    "id": "structured-state-control",
    "name": "Add schema-validated, merge-blocking repository state",
    "status": "complete",
    "inspected_base_commit": "6fe3d8ff415cd3b98d6f2ec7939220f9b1a24977",
    "resulting_commit": "self"
  },
  "next_goal": "Continue only when The User directs the next BADASS operation.",
  "authoritative_paths": {
    "constitution": "BADASS.md",
    "outline": "control/outline.md",
    "inspection_map": "control/inspection-map.json",
    "state": "control/state.json"
  },
  "license_status": "selected",
  "open_user_decisions": [],
  "required_checks": [
    "validate",
    "state-sync"
  ]
}
```
<!-- BADASS-STATE:END -->
