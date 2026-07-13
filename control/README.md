# Control Directory

This directory implements the repository-inspection, outline, decision, cull, and archive controls required by `BADASS.md`.

## Files

- `inspection-map.json`: user-controlled inspection scope.
- `state.json`: schema-validated current state synchronized with `outline.md`.
- `compliance-matrix.json`: schema-validated section evidence and `ASK_USER` judgments.
- `outline.md`: active project reality sandbox and human-readable state mirror.
- `session-attestation.json`: generated local session-state evidence.
- `file-inventory.csv`: generated local tracked-file inventory.
- `unclassified-files.txt`: generated local list of uncovered paths.
- `decisions/`: statused decision records.
- `culls/`: proposed and approved bad-information culls.
- `archive/`: verbatim material removed from active documents after approval.

## Generated files

Run:

```bash
python3 scripts/validate_repository.py --refresh
```

This creates `file-inventory.csv` and `unclassified-files.txt`. Run `python3 scripts/session_gate.py --start` to create `session-attestation.json`.

Validate durable state with:

```bash
python3 scripts/state_sync.py --check
python3 scripts/evidence_check.py --check
```

Generated files are intentionally ignored by Git and must not be treated as durable history.

## Authority

The User controls the inspection map, outline, cull approvals, decision statuses, and archives. The Assistant may report conflicts or missing coverage but may not silently change these controls.
