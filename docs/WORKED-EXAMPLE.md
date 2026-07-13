# Worked Recovery Example

This example demonstrates how BADASS changes an assistant's behavior after a real failure pattern. It is illustrative, not a substitute for current evidence.

## Failure

The User says that a repository change was pushed and provides terminal evidence. The Assistant opens a stale web rendering, then states:

> The revision did not reach the live branch.

That claim is incorrect and was stated as direct fact without adequate verification.

## Classification

- **HARD FAIL:** incorrect information was stated as fact.
- **Stale-state error:** a cached or stale view was treated as live evidence.
- **Truthfulness violation:** the assistant overstated what the source proved.
- **Current-state violation:** the exact live raw file and current commit were not verified.

## Recovery protocol applied

### 1. Stop

The Assistant stops the affected work and issues no further state-changing command.

### 2. Reopen authoritative sources

The Assistant directly opens the exact repository URL supplied by The User, the raw file, the active outline, and the inspection map. It does not search for the repository first.

### 3. Correct the statement

The Assistant states:

> My statement that the revision was not live was incorrect. The current raw file contains the approved revision. I relied on a stale rendering and overstated it as current evidence.

### 4. Trace downstream impact

The Assistant identifies every later conclusion based on the false claim, including any proposed re-push, rollback, or formatting repair.

### 5. Reconcile the outline

The recovery record includes the failure, direct sources inspected, current commit, affected conclusions, correction, and next goal.

### 6. Apply the smallest repair

No file is changed merely to repair the false claim. The repair is to correct the record, reverify affected work, and resume the original goal.

## Compliance matrix excerpt

| Section | Initial result | Recovery evidence | Final result |
|---|---|---|---|
| Truthfulness and Hard Fail States | FAIL | Exact false statement identified; direct raw source opened; downstream claims reinspected. | PASS |
| Current State and Source Examination | FAIL | Current raw file and live branch inspected directly. | PASS |
| Repository Inspection Control | UNKNOWN | Outline and map checked; changed and unclassified files read. | PASS |
| Plan Discipline | PASS | Original method preserved; no unrelated replacement path introduced. | PASS |
| Failure Handling | FAIL | Failure first defended instead of corrected. | PASS after explicit correction and reinspection |
| Directness | PASS | Corrected fact and next action stated directly. | PASS |

## Observable difference

Without BADASS, the assistant may apologize and continue. Under BADASS, the assistant must stop, name the exact false claim, prove the correction, trace downstream damage, update the outline, and resume only when applicable matrix rows pass.
