# Claude improve ledger (invented test data)

Last run: 2026-10-09 14:00 UTC

## Runs

| Date | Window | Sessions | Spend | New | Verified | Not working | Muted skipped |
|---|---|---|---|---|---|---|---|
| 2026-10-09 | 10-02 08:00 to 10-09 14:00 UTC (`reports/2026-10-09_claude-improve.md`); /doctor and /insights included, 3 verdicts under "Checked, no action" | 9 | $71 | 0 | 1 | 0 | 0 |

## Open items

## Checked, no action

| Checked | Source | Point | Verdict and where it is handled |
|---|---|---|---|
| 10-09 | /insights | Outputs longer than asked | Saved as a taste rule; no case after 14:00 |
| 10-09 | /doctor | docs-helper@acme plugin, 0 uses since install | Kept on purpose (the owner added it for the docs project); re-judge only if its counter moves |
| 10-09 | /doctor | format-on-save.js hook, median 210 ms over 31 runs | Fine |

## Closed items

### CI-3 Format hook blocks edits
- Status: verified | Raised: 2026-09-20 | Done: 2026-09-21 10:00 UTC
- Signal: hook.block.PostToolUse.format-on-save.js.per_week
