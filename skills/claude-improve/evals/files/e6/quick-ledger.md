Last run: 2026-10-09 09:00 UTC
Last Runs row: | 2026-10-09 | 10-02 08:00 to 10-09 09:00 UTC (`reports/2026-10-09_claude-improve.md`); /insights report of 09:05 UTC mapped, 6 lines under "Checked, no action" | 9 | $71 | 1 | 0 | 0 | 1 |
This window: 2026-10-09 09:00 to 2026-10-09 12:00 UTC, 4 sessions (3 startup)
Window edge: a session that crosses a window edge counts in both windows' session counts, so a summed tally runs a little high (known and accepted, references/ledger-format.md): nothing to check.

## Open items (2)
- CI-7 Edits fail because a formatter rewrites the file after every write | done | Done 2026-10-09 10:30 UTC
  Verify by: edit.err.modified_since.per_week below 1 (baseline 4.7)
  Done is inside this window: start the tally with `scan.py --since "2026-10-09 10:30" --until "2026-10-09 12:00" --json <scratchpad>/since-CI-7.json`
  Hint: needs the Start scan above first; under 10 sessions there -> too early
- CI-6 Shell commands break on heredocs | done | Done 2026-10-02 08:20 UTC
  Verify by: bash.err.heredoc_eof.per_week below 2 (baseline 5.0)
  Since Done: 8 sessions (5 startup), 0 heredoc_eof errors, through 2026-10-09 09:00 UTC
  New: 12 sessions (8 startup), 0 heredoc_eof errors, through 2026-10-09 12:00 UTC (+0 from bash.err.heredoc_eof.count) -> under 10 startup does not matter: its Fix line names no restart (settings env, MCP server, shell profile, plugins), so every session counts
  Hint: verified - bash.err.heredoc_eof: 5.0 -> 0.0 a week, target < 2, 12 sessions since Done; its Fix line names no restart

## Checked, no action (6): skip these unless a session after Last run backs them
- 10-09 /insights: Outputs longer than asked
- 10-09 /insights: Long sessions without a handoff
- 10-09 /insights: CLAUDE.md addition "## Scope"
- 10-09 /insights: Hooks (feature)
- 10-09 /insights: Custom Skills (feature)
- 10-09 /insights: "Ask for the short version first", "Parallel checks"

## Closed items: 2 (muted 1, verified 1); match a candidate on these Signal lines
- CI-5 (muted): subagents by model; share of helper runs on the top model
- CI-1 (verified): big_outputs_25k.per_week; tool results over 25K chars from web page fetches
