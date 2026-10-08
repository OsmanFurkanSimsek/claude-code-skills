# PROJECT.md - taskcli

> Single source of truth. A fresh agent reading only this file can continue correctly.

## Goal and definition of done

A stdlib-only Python CLI to add, list, and complete daily tasks stored in a local JSON file.
Done when all five execution steps pass their tests and the suite meets the 80/70 coverage gate.

## Scope and non-goals

- In: add/list/done commands, JSON persistence, colored terminal output.
- Out: sync, multi-user, GUI, external dependencies.

## Current state and next action

Step 1 (storage layer) done and tested. Step 2 (config loader) in progress.
Next action: finish step 2, then checkpoint.

## Decisions locked

- Python 3.12, stdlib only; pytest for tests (dev-only dependency).
- Tasks stored in ~/.taskcli/tasks.json, one JSON array.

## Plan / workstreams

See ## Execution plan below.

## Open questions

- (none)

## Change log

- 2026-07-10: Step 1 (storage layer) shipped; tests green.
- 2026-07-09: Phases 1-5 complete; plan locked at 5 steps.

## Lessons

- (none yet)

## Research notes

- pytest 8.x is current stable; tmp_path fixture is the idiomatic way to test file IO (accessed 2026-07-09).

## Execution plan

### Status (master table)

| # | Phase / step | Status | Validation / outcome |
|---|---|---|---|
| 1-5 | Discovery, Elon, Research, Plan | done | distilled into sections above |
| 6.1 | Storage layer (load/save JSON) | done | 5 tests, green |
| 6.2 | Config loader | in_progress | - |
| 6.3 | add/list/done commands | pending | - |
| 6.4 | Colored output | pending | - |
| 6.5 | CLI entry point + argparse wiring | pending | - |
| 7 | Holistic quality pass (coverage gate 80/70) | pending | - |
| 8 | Human review & feedback | pending | - |
| 9 | Critical review | pending | - |
| 10 | Playwright | pending | expected skip - no web frontend |
| 11 | Simplification | pending | - |
| 12 | Final verification & summary | pending | - |

### Step details

#### 6.1 Storage layer - Status: done
Verification (2026-07-10): 4 pytest cases green; corrupt-file and empty-file cases covered.

#### 6.2 Config loader - Status: in_progress
Implements: read ~/.taskcli/config.toml with defaults. Depends on: 6.1.
Validation: pytest cases for missing file, partial config, bad TOML. Done when tests green.
