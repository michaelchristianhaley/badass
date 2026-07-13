# BADASS Repository Outline

This file is The Assistant's human-readable working memory for the active BADASS repository. It is deliberately compact and may be reorganized or culled as current work changes.

## Current end goal

A current, inspectable repository that can stop a failing assistant, force direct rereading and evidence, identify the violated rules, repair downstream damage, and return the assistant to the user's actual project without Thrash, Drift, guessing, or lying.

## Active working set

* The User explicitly authorized the `BADASS.md` revision represented by version 1.4.0.
* The active outline is assistant-owned working memory, not an append-only archive.
* Project `WISDOM.md` files selectively accumulate durable execution lessons.
* BADASS `WISDOM.md` receives only deliberately promoted cross-project lessons.
* Outline and wisdom changes do not silently create new governing rules.
* Git history, `CHANGELOG.md`, evidence files, decisions, culls, and archives preserve their own kinds of history and proof.

## Verified current state

* Repository inspection is controlled by `control/inspection-map.json` with full-read fallback gates.
* Structured state and compliance evidence remain schema-validated and merge-blocking.
* Native assistant adapters route sessions through BADASS, the active outline, and wisdom.
* Repository content uses CC BY 4.0; scripts and workflow code use MIT.

## Next goal

Use the compact outline and wisdom model during the next BADASS recovery and in active projects.

## Culling rule

Remove completed, rejected, superseded, or irrelevant branches from this file. Promote lasting facts to canonical documentation and durable lessons to the appropriate `WISDOM.md`. As active BADASS work approaches completion, this outline should approach an empty working set.

## Machine-readable state mirror

<!-- BADASS-STATE:START -->
```json
{
  "$schema": "../schemas/state.schema.json",
  "schema_version": 1,
  "project": "BADASS",
  "branch": "main",
  "status": "active",
  "updated": "2026-07-13",
  "current_end_goal": "A current, inspectable repository that can stop a failing assistant, force direct rereading and evidence, identify the violated rules, repair downstream damage, and return the assistant to the user's actual project without Thrash, Drift, guessing, or lying.",
  "active_operation": {
    "id": "outline-wisdom-model",
    "name": "Adopt assistant-owned active outlines and selective project wisdom",
    "status": "complete",
    "inspected_base_commit": "2bcb166460a4f4b9000067bc583460f14cbdb1b2",
    "resulting_commit": "self"
  },
  "next_goal": "Use the compact outline and wisdom model during the next BADASS recovery and in active projects.",
  "authoritative_paths": {
    "constitution": "BADASS.md",
    "outline": "control/outline.md",
    "inspection_map": "control/inspection-map.json",
    "state": "control/state.json",
    "compliance_matrix": "control/compliance-matrix.json"
  },
  "license_status": "selected",
  "open_user_decisions": [],
  "required_checks": [
    "validate",
    "state-sync",
    "evidence-check"
  ]
}
```
<!-- BADASS-STATE:END -->
