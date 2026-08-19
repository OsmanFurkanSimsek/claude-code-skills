# PLAN.md - notes-app (legacy e2e run)

## Steps

| # | Step | Status | Validation |
|---|---|---|---|
| 1 | SQLite schema + migrations | done | 9 tests green |
| 2 | Note CRUD service | done | 17 tests green |
| 3 | Markdown rendering | in_progress | - |
| 4 | Export to HTML | pending | - |

## Step details

### 3. Markdown rendering - Status: in_progress
Implements: render note bodies with marked. Depends on: 2.
Validation: vitest snapshot cases for headings, lists, code fences. Done when tests green.

## Outcome

(to be filled at the end of the run)
