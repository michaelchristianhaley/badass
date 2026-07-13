# Integration

BADASS only affects an assistant when the assistant actually receives the governing instructions. This document describes current, explicit integration paths. `BADASS.md` remains canonical.

## Required session sequence

Every integration shall make the assistant:

1. load or read `BADASS.md`;
2. read `docs/QUICK-REFERENCE.md`;
3. read `control/outline.md` and `control/inspection-map.json`;
4. run `python3 scripts/session_gate.py --start` when local repository tools are available;
5. run `python3 scripts/validate_repository.py --check` before repository changes;
6. stop when a gate fails.

The session gate verifies repository state and produces a local attestation. It cannot prove that an assistant is truthful. The compliance matrix, direct evidence, and The User's review remain necessary.

## Claude Code

Claude Code loads repository-level `CLAUDE.md` files as persistent project instructions. Keep the provided root `CLAUDE.md` in the repository and start Claude Code from the repository tree.

Official documentation: <https://docs.anthropic.com/en/docs/claude-code/memory>

## OpenAI Codex

Codex reads root `AGENTS.md` before work. Keep the provided root `AGENTS.md` in the repository and start Codex from the repository tree.

Official documentation: <https://developers.openai.com/codex/guides/agents-md>

## GitHub Copilot

GitHub Copilot supports repository-wide instructions in `.github/copilot-instructions.md`. The provided file routes Copilot to the canonical BADASS sources.

Official documentation: <https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot>

## ChatGPT Projects

Add `BADASS.md` and `docs/QUICK-REFERENCE.md` to the ChatGPT Project files. Add a Project instruction requiring the assistant to open the current repository outline and inspection map before technical work. Re-upload or reconnect files after material repository changes.

Official documentation: <https://help.openai.com/en/articles/10169521-projects-in-chatgpt>

## Other assistants

Use the platform's native project-instruction feature when one exists. Provide the full `BADASS.md`, not only the quick reference. Require the assistant to identify the exact BADASS source and current outline before beginning work.

## Verification limits

Native instruction files and session gates improve reliable loading and state verification. They do not make model compliance mathematically enforceable. Claims of compliance still require observable evidence under `docs/SECTION-COMPLIANCE-MATRIX.md`.
