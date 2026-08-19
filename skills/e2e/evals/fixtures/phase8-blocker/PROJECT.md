# PROJECT.md - q3-deck

> Single source of truth. A fresh agent reading only this file can continue correctly.

## Goal and definition of done

A 12-slide Q3 churn analysis deck for leadership; every figure reconciles to the warehouse
extract; one idea per slide; ends with three costed retention options.

## Scope and non-goals

- In: churn by segment, cohort trends, driver analysis, three retention options.
- Out: pricing redesign, competitor benchmarking.

## Current state and next action

Phase 8 (human review) in progress: Osman walked the deck and filled the playtest checklist.
Next action: triage and fix the open rows below, re-verify, then close Phase 8.

## Decisions locked

- Deck built as marp markdown; figures exported from the warehouse extract of 2026-07-01.

## Plan / workstreams

See ## Execution plan below.

## Open questions

- (none)

## Change log

- 2026-07-14: Phase 7 done - all success criteria met, cross-slide numbers reconcile.

## Lessons

- (none yet)

## Execution plan

### Status (master table)

| # | Phase / step | Status | Validation / outcome |
|---|---|---|---|
| 1-6 | Discovery through Execute (4 steps) | done | all acceptance checks pass |
| 7 | Holistic quality pass | done | criteria met, consistent end to end |
| 8 | Human review & feedback | in_progress | checklist below |
| 9 | Critical review | pending | - |
| 10 | Playwright | pending | expected skip - not a web app |
| 11 | Tighten | pending | - |
| 12 | Final verification & summary | pending | - |

### Phase 8 detail - Status: in_progress

#### Playtest checklist

| Row | What to check | Result |
|---|---|---|
| 1 | Narrative spine lands in 90 seconds | OK |
| 2 | Slide 4 cohort chart supports the claim | OK |
| 3 | Slide 9 totals match slide 4 table | blocker: totals differ by 212 accounts |
| 4 | Three retention options each have a cost | nit: option C cost is a wide range |
