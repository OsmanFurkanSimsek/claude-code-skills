Last run: 2026-10-09 09:00 UTC
Last Runs row: | 2026-10-09 | 10-02 08:00 to 10-09 09:00 UTC (`reports/2026-10-09_claude-improve.md`); /insights report of 09:05 UTC mapped, 6 lines under "Checked, no action" | 9 | $71 | 1 | 0 | 0 | 1 |
This window: 2026-10-09 09:00 to 2026-10-09 12:00 UTC, 4 sessions (3 startup)

## Open items (2)
- CI-7 Edits fail because a formatter rewrites the file after every write | done | Done 2026-10-09 10:30 UTC
  Verify by: edit.err.modified_since.per_week below 1 (baseline 4.7)
  Done is inside this window: start the tally with `scan.py --since "2026-10-09 10:30" --until "2026-10-09 12:00" --json <scratchpad>/since-CI-7.json`
- CI-6 Shell commands break on heredocs | done | Done 2026-10-02 08:20 UTC
  Verify by: bash.err.heredoc_eof.per_week below 2 (baseline 5.0)
  Since Done: 8 sessions (5 startup), 0 heredoc_eof errors, through 2026-10-09 09:00 UTC
  New: 12 sessions (8 startup), 0 heredoc_eof errors, through 2026-10-09 12:00 UTC (+0 from bash.err.heredoc_eof.count) -> under 10 startup: too early only for a fix that needs a restart (settings env, MCP, profile)
  Fix: rule "a script over ~10 lines goes to a file and runs by path" in `~/.claude/CLAUDE.md`

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
