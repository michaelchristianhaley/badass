# Contributing

This repository is governed by `BADASS.md` and controlled by The User.

## Before proposing a change

1. Read `BADASS.md`.
2. Read `control/outline.md`.
3. Read `control/inspection-map.yml`.
4. Run `python3 scripts/validate_repository.py --check`.
5. State the exact problem and the current direct evidence.

## BADASS.md changes

Do not propose or make a direct change to `BADASS.md` unless The User has explicitly authorized that specific change.

A proposal may identify:

- the exact current language;
- the problem;
- the smallest suggested revision;
- any change in authority;
- any content or intent that could be lost.

The User decides.

## Supporting-file changes

Supporting files may clarify, test, or operationalize `BADASS.md`. They may not weaken it, supersede it, or grant The Assistant more authority.

Every new tracked file must be classified in `control/inspection-map.yml`.

## Pull requests

A pull request should:

- have one coherent purpose;
- preserve LF line endings;
- pass repository validation;
- identify changed control or decision records;
- avoid generated inventory, caches, installers, disk images, and large raw reports;
- include an undo or recovery path for state-changing scripts.

The maintainer may close proposals that conflict with The User's stated intent.
