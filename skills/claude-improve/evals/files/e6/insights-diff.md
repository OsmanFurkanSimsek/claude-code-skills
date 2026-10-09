# /insights since the last review

- New report: `report-2026-10-09-133000.html` (2026-10-09 13:30 local): 455 messages across 64 sessions (78 total) | 2026-07-01 to 2026-10-09
- Previous report: `report-2026-10-09-110500.html` (2026-10-09 11:05 local): 412 messages across 61 sessions (75 total) | 2026-07-01 to 2026-10-09
- Since (the ledger's Last run): 2026-10-09 09:00 UTC. Plain text of both: `insights-new.txt`, `insights-prev.txt` next to this file.

## Points in the new report

A title can change while the point stays the same (the text is rewritten every run); the facets below decide what is new.

- [friction] Outputs longer than asked (same title as before)
  - example: The weekly summary for the notes-app came out three pages long when one was asked for (10-03).
  - example: A status reply listed every file touched instead of the one result (10-05).
- [friction] Long sessions without a handoff (same title as before)
  - example: A data-pipeline session ran 3 hours before the plan was saved (10-04).
- [friction] Same test suite re-run after small edits (new title)
  - example: In a report-builder session the 140-test suite ran twice after one-line edits, about 2 minutes in all (10-09).
- [CLAUDE.md addition] ## Scope (same title as before)
- [feature] Hooks (same title as before)
- [feature] Custom Skills (same title as before)
- [new way] Ask for the short version first (same title as before)
- [horizon] Parallel checks (same title as before)

## Sessions after 2026-10-09 09:00 UTC with an /insights analysis

3 sessions active after it (test runs left out); 2 have an analysis (facet). A session without one was too short or not analysed yet.

- 3333cccc notes-app (last message 10-09 10:10 UTC): outcome fully_achieved; friction none
  - summary: The user asked to tag last week's notes; done.
- 2222bbbb report-builder (last message 10-09 10:50 UTC): outcome fully_achieved; friction excessive_changes 1
  - friction: Claude ran the full 140-test suite twice after one-line edits, about 2 minutes in all.

## How to use this

- A point that no facet above backs has all its cases before the last review: one line under "Checked, no action" ("no case after <Last run>") if the ledger does not cover it yet, else nothing. No helper, no transcript reading.
- A point a facet above backs is a candidate: read that session (its id is above) in context, as in Step 3.
- A suggestion (CLAUDE.md addition, feature, new way, horizon) the ledger already answered stays answered unless a facet above gives new evidence for it.
