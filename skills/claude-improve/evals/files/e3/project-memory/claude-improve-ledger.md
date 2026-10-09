# Claude improve ledger

> Every recommendation from the claude-improve review, the owner's answer, and how we check
> it worked. Read in full at the start of each review; one heading per item. (Invented test data.)

Last run: 2026-10-02 08:00 UTC

## Runs

| Date | Window | Sessions | Spend | New | Verified | Not working | Muted skipped |
|---|---|---|---|---|---|---|---|
| 2026-09-25 | 09-18 08:00 to 09-25 08:00 UTC | 14 | $121 | 3 | 0 | 0 | 0 |
| 2026-10-02 | 09-25 08:00 to 10-02 08:00 UTC | 11 | $88 | 0 | 1 | 0 | 1 |

## Open items

### CI-4 Whole web pages land in the main context
- Status: done | Raised: 2026-09-25 | Answered: 2026-10-02 | Done: 2026-10-02 08:30 UTC
- Signal: big_outputs_25k.per_week; tool results over 25K chars from web page fetches
- Evidence: 09-18 to 09-25: 9 results over 25K, 7 of them whole-page fetches (largest 61K, a vendor changelog)
- Fix: one line in `~/.claude/CLAUDE.md`: "fetch a long page through a helper agent that saves it to a file and returns a summary + path"
- Verify by: big_outputs_25k.per_week below 3 (baseline 9.0)
- Owner: "do it"
- History: 2026-09-25 raised, later; 2026-10-02 re-raised, approved, done

### CI-3 Shell commands break on heredocs
- Status: done | Raised: 2026-09-25 | Answered: 2026-10-02 | Done: 2026-10-02 08:20 UTC
- Signal: bash.err.heredoc_eof.per_week; inline scripts with quotes, `$` or backticks
- Evidence: 09-18 to 09-25: 5 EOF errors, 4 of them a Python script piped through `<<EOF` with a `$` inside
- Fix: rule "a script over ~10 lines goes to a file and runs by path" in `~/.claude/CLAUDE.md`
- Verify by: bash.err.heredoc_eof.per_week below 2 (baseline 5.0)
- Owner: "fix it"
- History: 2026-09-25 raised, later; 2026-10-02 re-raised, approved, done

## Checked, no action

| Checked | Source | Point | Verdict and where it is handled |
|---|---|---|---|
| 2026-10-02 | /insights | "Sessions run long without a handoff" | no: median session 41 min, 0 compactions; nothing to fix |

## Closed items

### CI-2 Helper agents run on the most expensive model
- Status: muted | Raised: 2026-09-25 | Answered: 2026-09-25
- Signal: subagents by model; share of helper runs on the top model
- Owner: "quality first, keep it"
- History: 2026-09-25 raised, muted

### CI-1 Edits fail because the file changed since it was read
- Status: verified | Raised: 2026-09-18 | Answered: 2026-09-18 | Done: 2026-09-18 09:10 UTC
- Signal: edit.err.modified_since.per_week
- Evidence: 6 a week, all after a formatter hook rewrote the file
- Fix: formatter hook runs at Stop instead of after every write
- Verify by: edit.err.modified_since.per_week below 1 (baseline 6.0)
- Owner: "yes"
- History: 2026-09-18 raised, approved, done; 2026-10-02 verified (6.0 -> 0.0, 11 sessions after Done)
