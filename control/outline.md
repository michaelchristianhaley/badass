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
- A non-canonical quick reference and worked recovery example are available.
- License selection remains a user decision.

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
- [ ] The User selects a repository license.
- [x] Add native assistant integration and session-state verification.
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
