# Claude improve ledger

> Every recommendation from the claude-improve review, the owner's answer, and how we check
> it worked. Read in full at the start of each review; one heading per item. (Invented test data.)

Last run: 2026-09-18 08:00 UTC

## Runs

| Date | Window | Sessions | Spend | New | Verified | Not working | Muted skipped |
|---|---|---|---|---|---|---|---|
| 2026-09-11 | 08-28 08:00 to 09-11 08:00 UTC | 23 | $204 | 2 | 0 | 0 | 0 |
| 2026-09-18 | 09-11 08:00 to 09-18 08:00 UTC | 13 | $97 | 0 | 1 | 0 | 1 |

## Open items

## Checked, no action

| Checked | Source | Point | Verdict and where it is handled |
|---|---|---|---|
| 2026-09-18 | /insights | "Owner often asks for shorter replies" | no: 1 case in 13 sessions; the reply-format rule in `~/.claude/CLAUDE.md` already covers it |

## Closed items

### CI-2 Helper agents run on the most expensive model
- Status: muted | Raised: 2026-09-11 | Answered: 2026-09-11
- Signal: subagents by model; share of helper runs on the top model
- Owner: "quality first, keep it"
- History: 2026-09-11 raised, muted

### CI-1 Edits fail because the file changed since it was read
- Status: verified | Raised: 2026-09-11 | Answered: 2026-09-11 | Done: 2026-09-11 09:10 UTC
- Signal: edit.err.modified_since.per_week
- Evidence: 6 a week, all after a formatter hook rewrote the file
- Fix: formatter hook runs at Stop instead of after every write
- Verify by: edit.err.modified_since.per_week below 1 (baseline 6.0)
- Owner: "yes"
- History: 2026-09-11 raised, approved, done; 2026-09-18 verified (6.0 -> 0.0, 13 sessions after Done)
