# PROJECT.md - taskcli

> Single source of truth. A fresh agent reading only this file can continue correctly.

## Goal and definition of done

A stdlib-only Python CLI to add, list, and complete daily tasks stored in a local JSON file.

## Scope and non-goals

- In: add/list/done commands, JSON persistence, colored terminal output.
- Out: sync, multi-user, GUI, external dependencies.

## Current state and next action

Phases 1-8 done: all 5 steps green, coverage 86%/74% (gate 80/70), human playtest fixes applied.
Next action: Phase 9 critical review (read-only reviewer, then user picks fixes).

## Decisions locked

- Python 3.12, stdlib only; pytest for tests (dev-only dependency).
- Tasks stored in ~/.taskcli/tasks.json, one JSON array.

## Plan / workstreams

See ## Execution plan below.

## Open questions

- (none)

## Change log

- 2026-07-13: Phase 8 done - 1 blocker fix (crash on empty list), 2 annoying fixes; suite re-green.
- 2026-07-12: Phase 7 done - 48 tests, coverage 86/74, smoke pass.
- 2026-07-10: Phases 1-6 done; 5 steps shipped.

## Lessons

- Older Windows terminals need ANSI escape support enabled at startup before colored output works.

## Execution plan

### Status (master table)

| # | Phase / step | Status | Validation / outcome |
|---|---|---|---|
| 1-6 | Discovery through Execute (5 steps) | done | all steps green |
| 7 | Holistic quality pass | done | 48 tests, 86%/74% vs 80/70 gate |
| 8 | Human review & feedback | done | 1 blocker + 2 annoying fixed, re-verified |
| 9 | Critical review | pending | - |
| 10 | Playwright | pending | expected skip - no web frontend |
| 11 | Simplification | pending | - |
| 12 | Final verification & summary | pending | - |
