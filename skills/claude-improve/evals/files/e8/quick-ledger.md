Last run: 2026-10-09 14:00 UTC
Last Runs row: | 2026-10-09 | 10-02 08:00 to 10-09 14:00 UTC (`reports/2026-10-09_claude-improve.md`); /doctor and /insights included, 3 verdicts under "Checked, no action" | 9 | $71 | 0 | 1 | 0 | 0 |
This window: 2026-10-09 14:00 to 2026-10-09 15:00 UTC, 2 sessions (1 startup)
Window edge: a session that crosses a window edge counts in both windows' session counts, so a summed tally runs a little high (known and accepted, references/ledger-format.md): nothing to check.

## Open items (0)

## Checked, no action (3): skip these unless a session after Last run backs them
- 10-09 /insights: Outputs longer than asked
- 10-09 /doctor: docs-helper@acme plugin, 0 uses since install: kept on purpose (the owner added it for the docs project); re-judge only if its counter moves
- 10-09 /doctor: format-on-save.js hook, median 210 ms over 31 runs: fine

## Closed items: 1 (verified 1); match a candidate on these Signal lines
- CI-3 (verified): hook.block.PostToolUse.format-on-save.js.per_week
