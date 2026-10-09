# Claude improve ledger (invented test data)

Last run: 2026-10-08 12:00 UTC

## Runs

| Date | Window | Sessions | Spend | New | Verified | Not working | Muted skipped |
|---|---|---|---|---|---|---|---|
| 2026-10-08 | 10-01 08:00 to 10-08 12:00 UTC (`reports/2026-10-08_claude-improve.md`); 2 verdicts under "Checked, no action" | 31 | $190 | 1 | 0 | 0 | 0 |

## Open items

### CI-4 Edits fail because a formatter rewrites the file after every write
- Status: done | Raised: 2026-10-01 | Answered: 2026-10-01 | Done: 2026-10-05 09:00 UTC
- Signal: edit.err.modified_since.per_week
- Verify by: edit.err.modified_since.per_week below 1 (baseline 4.7)
- Since Done: 14 sessions (6 startup), 0 modified_since errors, through 2026-10-08 12:00 UTC
- Owner: "fix it"

## Checked, no action

| Checked | Source | Point | Verdict and where it is handled |
|---|---|---|---|
| 10-08 | /insights | Outputs longer than asked | Saved as a taste rule; no case after 10-08 12:00 |
| 10-08 | /doctor | docs-helper@acme plugin, 0 uses since install | Kept on purpose (the owner added it for the docs project); re-judge only if its counter moves |

## Closed items
