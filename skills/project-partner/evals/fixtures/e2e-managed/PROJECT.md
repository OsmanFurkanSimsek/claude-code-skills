# PROJECT.md - churn-dashboard

> Single source of truth. A fresh agent reading only this file can continue correctly.

## Goal and definition of done

A Power BI dashboard the retention team opens every Monday: churn by segment, cohort trends,
and an at-risk account list. Done when all measures validate against the warehouse extract.

## Scope and non-goals

- In: churn measures, cohort page, at-risk list, weekly refresh.
- Out: predictions/ML scoring, self-serve report authoring.

## Current state and next action

Step 3 of 4 (data-model page) in progress. Next action: validate the measures against the
July extract, then checkpoint.

## Decisions locked

- Star schema: FactChurn + DimAccount/DimSegment/DimDate; measures in one dedicated table.

## Plan / workstreams

See ## Execution plan below.

## Open questions

- (none)

## Change log

- 2026-07-14: Steps 1-2 done (data prep, churn measures), measures tie to extract.

## Lessons

- (none yet)

## Research notes

- SQLBI star-schema guidance: single measures table, no calculated columns in facts (accessed 2026-07-08).

## Execution plan

### Status (master table)

| # | Phase / step | Status | Validation / outcome |
|---|---|---|---|
| 1-5 | Discovery, Elon, Research, Plan | done | distilled into sections above |
| 6.1 | Data prep + refresh | done | row counts tie to extract |
| 6.2 | Churn measures | done | 6 measures validate on known cases |
| 6.3 | Data-model page | in_progress | - |
| 6.4 | Cohort + at-risk pages | pending | - |
| 7-12 | Quality pass through final summary | pending | - |
