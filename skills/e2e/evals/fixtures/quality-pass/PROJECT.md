# PROJECT.md - taskcli

> Single source of truth. A fresh agent reading only this file can continue correctly.

## Goal and definition of done

A stdlib-only Python CLI to add, list, and complete daily tasks stored in a local JSON file.
Done when all five execution steps pass their tests and the suite meets the 80/70 coverage gate.

## Scope and non-goals

- In: add/list/done commands, JSON persistence, colored terminal output.
- Out: sync, multi-user, GUI, external dependencies.

## Current state and next action

All 5 execution steps done and green. Phase 7 (holistic quality pass) in progress: full suite
run and coverage measurement. Next action: apply the coverage gate, then smoke test.

## Decisions locked

- Python 3.12, stdlib only; pytest + pytest-cov for tests (dev-only dependencies).
- Tasks stored in ~/.taskcli/tasks.json, one JSON array.
- Coverage gate: default 80/70 (no --coverage flag was passed).

## Plan / workstreams

See ## Execution plan below.

## Open questions

- (none)

## Change log

- 2026-07-12: Steps 6.4-6.5 shipped; all execution steps done, 48 tests green.
- 2026-07-10: Steps 6.1-6.3 shipped.

## Lessons

- (none yet)

## Execution plan

### Status (master table)

| # | Phase / step | Status | Validation / outcome |
|---|---|---|---|
| 1-5 | Discovery, Elon, Research, Plan | done | distilled into sections above |
| 6.1-6.5 | All execution steps | done | 48 tests green across steps |
| 7 | Holistic quality pass (coverage gate 80/70) | in_progress | suite green; coverage being measured |
| 8 | Human review & feedback | pending | - |
| 9 | Critical review | pending | - |
| 10 | Playwright | pending | expected skip - no web frontend |
| 11 | Simplification | pending | - |
| 12 | Final verification & summary | pending | - |
