# Repository Health

This repository is intentionally small, documentation-first, and designed to realign an assistant after it has behaved badly.

## Design goals

- Keep `BADASS.md` user-owned and stable.
- Make assistant comprehension testable.
- Separate active truth from historical evidence.
- Use deterministic inspection controls rather than assistant-selected relevance.
- Keep generated state out of Git history.
- Validate repository structure automatically.
- Load canonical rules through current native assistant instruction files.
- Generate a local session-state attestation before work.
- Preserve simple CLI workflows.

## GitHub best-practice basis

The repository follows current GitHub guidance by providing:

- a useful README;
- contribution guidance;
- a code of conduct;
- support and security guidance;
- repository-controlled line endings;
- repository-specific ignore rules;
- issue and pull-request templates;
- CODEOWNERS;
- automated validation;
- a clear license decision record.

Relevant official GitHub guidance:

- Repository best practices: <https://docs.github.com/en/repositories/creating-and-managing-repositories/best-practices-for-repositories>
- README guidance: <https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes>
- Healthy contributions: <https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions>
- Community profiles: <https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/about-community-profiles-for-public-repositories>
- Line endings: <https://docs.github.com/en/get-started/git-basics/configuring-git-to-handle-line-endings>
- Secure Actions use: <https://docs.github.com/en/actions/reference/security/secure-use>

## Generated inspection state

`control/file-inventory.csv` and `control/unclassified-files.txt` are local generated files.

They are ignored because:

1. A tracked inventory containing its own current hash is self-referential.
2. Generated inventory becomes stale immediately after a commit.
3. The outline and commit history preserve durable evidence.
4. The validator can reproduce the files at any time.

## Validation

Run:

```bash
python3 scripts/validate_repository.py --self-test
python3 scripts/validate_repository.py --refresh
python3 scripts/validate_repository.py --check
```

The GitHub Actions workflow runs validator and session-gate self-tests plus the repository check on pushes and pull requests. The README exposes the live workflow badge.

## Maintenance rule

Do not add files casually. Every tracked path must be classified by `control/inspection-map.json`, linked from an appropriate document, and validated before commit.

## Structured-state check

The repository tracks `control/state.json` and `schemas/state.schema.json`.
`scripts/state_sync.py` validates the schema and the exact state mirror in the
active outline. The independent `state-sync` workflow is a required branch
status check together with `validate`. Administrator enforcement remains off so
the repository owner's established direct Termux push workflow still works.

## Evidence check

The repository tracks `control/compliance-matrix.json` and
`schemas/compliance-matrix.schema.json`. `scripts/evidence_check.py` validates
the schema, exact BADASS section coverage, evidence paths, and the semantics of
`PASS`, `FAIL`, `ASK_USER`, and `NOT_APPLICABLE`. The independent
`evidence-check` workflow is required together with `validate` and `state-sync`.
Administrator enforcement remains unchanged, preserving The User's established
direct Termux push workflow.
