# Changelog

All notable repository changes are recorded here.

## 2026-07-12 — Claude report remediation

### Added

- native Claude Code, Codex, and GitHub Copilot instruction adapters;
- assistant integration guide and one-page quick reference;
- local session-state gate and attestation;
- worked HARD FAIL recovery example;
- Claude review archive and remediation record;
- visible CI status badge;
- BADASS version metadata.

### Changed

- renamed `control/inspection-map.yml` to truthful `control/inspection-map.json`;
- narrowed formal-work scope so unrelated casual conversation is not governed as project work;
- extended repository validation and CI coverage.

### Open decision

- The User has not selected a repository license.

## 2026-07-12

### Added

- assistant recovery protocol;
- section compliance matrix;
- user-controlled repository inspection map;
- active outline and decision records;
- cull and archive controls;
- repository validator and generated local inventory;
- GitHub Actions validation;
- README, contribution, conduct, security, support, ownership, and issue templates;
- line-ending, editor, and ignore controls.

### Preserved

- `BADASS.md` remained unchanged during the repository-health bootstrap.

### Open decision

- The User has not selected a repository license.

## 2026-07-12 — Remaining live consistency fixes

### Fixed

- corrected the stale `inspection-map.yml` reference in `control/README.md`;
- pinned `actions/checkout` v7.0.0 to its verified full commit SHA;
- extended validation so both corrections remain enforced.

### Preserved

- `BADASS.md` was not changed.
- The license decision remains reserved for The User.

## 2026-07-12 — Dual-license decision

### Added

- CC BY 4.0 notice for repository content;
- MIT notice for scripts and GitHub Actions workflow code;
- explicit license scope and attribution guidance.

### Changed

- license decision 0004 is Accepted;
- README and license guidance show the selected licenses;
- validation and inspection coverage require the license files.

### Preserved

- `BADASS.md` was not changed.

## 2026-07-12 — Structured state control

### Added

- schema-validated `control/state.json`;
- tracked JSON Schema for repository state;
- exact state synchronization with the active outline;
- self-testing state validator and independent `state-sync` workflow;
- required `validate` and `state-sync` branch contexts.

### Changed

- BADASS version advanced to 1.2.0 to govern structured state.
- Session attestation and repository validation now include current state.

## 2026-07-12 — Evidence compliance control

### Added

- schema-validated `control/compliance-matrix.json`;
- tracked JSON Schema for compliance evidence;
- exact BADASS section coverage and repository evidence-path checks;
- governed `PASS`, `FAIL`, `ASK_USER`, and `NOT_APPLICABLE` semantics;
- self-testing evidence validator and independent `evidence-check` workflow;
- required `validate`, `state-sync`, and `evidence-check` branch contexts.

### Changed

- BADASS version advanced to 1.3.0 to govern evidence claims.
- Session attestation and structured state now include compliance evidence.
- The human matrix uses `ASK_USER` instead of ambiguous `UNKNOWN`.
