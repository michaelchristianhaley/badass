# Recovery Protocol

Use this protocol after the assistant has been a **BAD ASSISTANT**, especially after a HARD FAIL, Thrash, Drift, stale-state error, unsupported claim, untested script, or unauthorized method change.

## 1. Stop

Stop the affected work. Do not defend the failure, continue the broken plan, or issue another state-changing command.

## 2. Reopen the authoritative sources

Open directly:

1. `BADASS.md`
2. `control/outline.md`
3. `control/inspection-map.yml`
4. the exact live files, machine state, errors, or authoritative URLs involved

Do not use cached memory as evidence.

## 3. Name the failure

State:

- the exact incorrect action or claim;
- the BADASS section violated;
- whether it is a HARD FAIL, Thrash, Drift, or another failure;
- the known downstream effects;
- what remains unknown.

## 4. Complete the compliance matrix

Use `docs/SECTION-COMPLIANCE-MATRIX.md`.

Mark every applicable section `PASS`, `FAIL`, `UNKNOWN`, or `NOT APPLICABLE`. Evidence must be direct and current.

## 5. Reconcile the outline

Record:

- the current commit and state;
- every file inspected;
- the failure;
- the affected work;
- the current end goal;
- the current best-practice check;
- the proposed repair.

Do not rewrite the original outline steps. Append the recovery record.

## 6. Propose the smallest repair

Preserve the approved method.

If a method or tool replacement appears necessary, explain why and ask The User. Do not replace it without approval.

## 7. Execute safely

For state-changing work:

1. Parse and syntax-check.
2. Verify prerequisites and live state.
3. Run an isolated self-test.
4. Stop on any failed gate.
5. Execute.
6. Verify the actual result.
7. Record useful evidence.
8. Provide a practical undo path.

Read-only work does not require an undo path.

## 8. Verify and resume

Reinspect every downstream conclusion, command, file, and decision affected by the failure.

Resume only when:

- all applicable matrix rows pass;
- unknowns are resolved or accepted by The User;
- the outline is current;
- the repair is verified;
- the next action directly advances the actual end goal.
