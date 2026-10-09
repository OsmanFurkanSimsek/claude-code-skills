# Decisions - report-builder

> Full wording of every decision for this project, one heading each. (Invented test data.)

## Monthly reports land in reports/YYYY-MM/
- One folder per month; the file name starts with the date. Owner, 2026-08-30.

## Run verification now, never schedule it for later
- When a change is made, its check runs in the same session: the query, the test, the read-back. Never write "I will
  verify this next time" or put the check on a later list. Owner, 2026-09-08: "If you can check it now, check it now.
  A check on a later list never happens."

## Numbers come from the warehouse, never from a pasted table
- A pasted table is a starting point only; every number in a report is re-read from the source. Owner, 2026-09-10.
