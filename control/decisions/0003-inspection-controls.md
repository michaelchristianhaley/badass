# Decision 0003: Deterministic Inspection Controls

- Status: Accepted
- Date: 2026-07-12
- Scope: Repository operations
- Reason: The User does not trust assistant-selected relevance after repeated missed files and stale assumptions.
- Reversal condition: The User explicitly approves another inspection system.

## Decision

A user-controlled inspection map and active outline control normal inspection scope.

Missing, stale, invalid, contradictory, unmapped, or unclassified state triggers a full repository read.

The Assistant shall not substitute its own relevance judgment for these gates.
