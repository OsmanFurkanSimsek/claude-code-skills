# Ledger format

One markdown file holds every recommendation claude-improve has ever made. It is the review's
memory: a new run reads it first, so nothing is re-proposed, muted items stay quiet, and done items
get checked against their baseline.

## Template (copy when creating a new ledger)

```markdown
# Claude improve ledger

> Every recommendation from the weekly claude-improve review, the owner's answer, and how we check
> it worked. Read in full at the start of each review; one heading per item. (If this project keeps
> a PROJECT.md, its Map points here.)

Last run: YYYY-MM-DD

## Runs

| Date | Window | Sessions | Spend | New | Verified | Not working | Muted skipped |
|---|---|---|---|---|---|---|---|

## Open items

## Closed items
```

## One item

```markdown
### CI-012 Shell commands break on paths with an apostrophe
- Status: done | Raised: 2026-09-27 | Answered: 2026-09-27
- Signal: bash.err.heredoc_eof.per_week; commands containing a path with `'`
- Evidence: 39 EOF errors in 10 weeks, 13 of them with the apostrophe path in the command
- Fix: rule "write scripts to a file, run by path" in ~/.claude/CLAUDE.md
- Verify by: bash.err.heredoc_eof.per_week below 2 (baseline 3.9)
- Owner: "fix it"
- History: 2026-09-27 raised, approved, done
```

Fields:

- **ID** `CI-<n>`, never reused. Title in plain words: what goes wrong, not the metric name.
- **Status** - one of:
  - `open` - raised, no answer yet
  - `approved` - owner said do it; not done yet (planned chunk named in Fix)
  - `done` - fix in place, waiting for the metric to confirm
  - `verified` - the metric moved as expected (write before -> after in History)
  - `not working` - done, but the metric did not move; goes back to the owner
  - `waiting on owner` - the next step is the owner's (a setting, a rename, an account)
  - `later` - owner said not now; re-raise only if the metric grows or after 4 weeks
  - `muted` - owner said never; never raise again, never list, only count
  - `benign` - the agent checked a signal and found it is not a problem (say why in `Owner:`); skip
    it unless its numbers change shape. Saves the next run from re-investigating it.
- **Signal** - the scan metric key(s) and/or the pattern this rests on. This is what new candidates
  are matched against, so a muted item stays muted even when it comes back under new wording.
- **Evidence** - counts with their window, plus the example that convinced you.
- **Fix** - the smallest change and where it lives (file, hook, rule, skill).
- **Verify by** - metric key + target + baseline. Required before an item can be `done`.
- **Owner** - the owner's answer, verbatim when short; for `muted`, the reason.
- **History** - dated one-liners: raised, answered, done, verified / not working.

## Housekeeping

- Open and active items (`open`, `approved`, `done`, `not working`, `waiting on owner`, `later`)
  stay under **Open items**, newest first.
- `verified`, `muted` and `benign` items move to **Closed items**. Keep their `Signal` line (the matcher needs
  it); fold Evidence and History into one line when the file grows past about 30 KB.
- The Runs table gets one row per run, never edited afterwards.
