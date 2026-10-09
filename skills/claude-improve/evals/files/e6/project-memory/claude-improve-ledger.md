# Claude improve ledger

> Every recommendation from the claude-improve review, the owner's answer, and how we check
> it worked. Read in full at the start of each review; one heading per item. (Invented test data.)

Last run: 2026-10-09 09:00 UTC

## Runs

| Date | Window | Sessions | Spend | New | Verified | Not working | Muted skipped |
|---|---|---|---|---|---|---|---|
| 2026-10-02 | 09-25 08:00 to 10-02 08:00 UTC | 11 | $88 | 2 | 1 | 0 | 1 |
| 2026-10-09 | 10-02 08:00 to 10-09 09:00 UTC (`reports/2026-10-09_claude-improve.md`); /insights report of 09:05 UTC mapped, 6 lines under "Checked, no action" | 9 | $71 | 1 | 0 | 0 | 1 |

## Open items

### CI-7 Edits fail because a formatter rewrites the file after every write
- Status: done | Raised: 2026-10-09 | Answered: 2026-10-09 | Done: 2026-10-09 10:30 UTC
- Signal: edit.err.modified_since.per_week; "modified since read" errors right after the formatter hook
- Evidence: 10-02 to 10-09: 6 "modified since read" errors in 9 sessions, each right after the formatter hook ran
- Fix: formatter hook moved from PostToolUse to Stop in `~/.claude/settings.json`
- Verify by: edit.err.modified_since.per_week below 1 (baseline 4.7)
- Owner: "do it"
- History: 2026-10-09 raised, approved; done 10:30 UTC, after the morning run

### CI-6 Shell commands break on heredocs
- Status: done | Raised: 2026-10-02 | Answered: 2026-10-02 | Done: 2026-10-02 08:20 UTC
- Signal: bash.err.heredoc_eof.per_week; inline scripts with quotes, `$` or backticks
- Evidence: 09-25 to 10-02: 5 EOF errors, 4 of them a Python script piped through `<<EOF` with a `$` inside
- Fix: rule "a script over ~10 lines goes to a file and runs by path" in `~/.claude/CLAUDE.md`
- Verify by: bash.err.heredoc_eof.per_week below 2 (baseline 5.0)
- Since Done: 8 sessions (5 startup), 0 heredoc_eof errors, through 2026-10-09 09:00 UTC
- Owner: "fix it"
- History: 2026-10-02 raised, approved, done; 2026-10-09 too early (8 sessions after Done, 0 errors)

## Checked, no action

| Checked | Source | Point | Verdict and where it is handled |
|---|---|---|---|
| 10-09 | /insights | Outputs longer than asked | No case after 10-05; the reply-format rule in `~/.claude/CLAUDE.md` covers it |
| 10-09 | /insights | Long sessions without a handoff | No: median session 38 min, 0 compactions |
| 10-09 | /insights | CLAUDE.md addition "## Scope" | No: already in `~/.claude/CLAUDE.md` |
| 10-09 | /insights | Hooks (feature) | No: the formatter hook is CI-7 |
| 10-09 | /insights | Custom Skills (feature) | No: the report-style skill exists |
| 10-09 | /insights | "Ask for the short version first", "Parallel checks" | No for the setup: habits, not a fix |

## Closed items

### CI-5 Helper agents run on the most expensive model
- Status: muted | Raised: 2026-09-25 | Answered: 2026-09-25
- Signal: subagents by model; share of helper runs on the top model
- Owner: "quality first, keep it"
- History: 2026-09-25 raised, muted

### CI-1 Big web pages land in the main context
- Status: verified | Raised: 2026-09-18 | Answered: 2026-09-18 | Done: 2026-09-18 09:10 UTC
- Signal: big_outputs_25k.per_week; tool results over 25K chars from web page fetches
- Fix: one line in `~/.claude/CLAUDE.md`: long pages go through a helper that saves them to a file
- Verify by: big_outputs_25k.per_week below 3 (baseline 9.0)
- Owner: "yes"
- History: 2026-09-18 raised, approved, done; 2026-10-02 verified (9.0 -> 1.0, 11 sessions after Done)
