# Ledger format

One markdown file holds every recommendation claude-improve has ever made. It is the review's
memory: a new run reads it first, so nothing is re-proposed, muted items stay quiet, and done items
get checked against their baseline.

## Template (copy when creating a new ledger)

```markdown
# Claude improve ledger

> Every recommendation from the claude-improve review, the owner's answer, and how we check
> it worked. Read in full at the start of each review; one heading per item. (If this project keeps
> a PROJECT.md, its Map points here.)

Last run: YYYY-MM-DD HH:MM UTC

## Runs

| Date | Window | Sessions | Spend | New | Verified | Not working | Muted skipped |
|---|---|---|---|---|---|---|---|

## Open items

## Checked, no action

| Checked | Source | Point | Verdict and where it is handled |
|---|---|---|---|

## Closed items
```

"Checked, no action" holds every /insights point or suggestion and every /doctor extension verdict that needed no
item, so the next run skips it (rule "Never redo audited work"). Re-open a line only when evidence after `Last run:`
changes it; then it becomes an item. An /insights point no session after `Last run:` backs gets at most one line
("no case after <Last run>"), however its title is worded in the new report.

## One item

```markdown
### CI-012 Shell commands break on paths with an apostrophe
- Status: done | Raised: 2026-09-27 | Answered: 2026-09-27 | Done: 2026-09-27 11:46 UTC
- Signal: bash.err.heredoc_eof.per_week; commands containing a path with `'`
- Evidence: 39 EOF errors in 10 weeks, 13 of them with the apostrophe path in the command
- Fix: rule "write scripts to a file, run by path" in ~/.claude/CLAUDE.md
- Verify by: bash.err.heredoc_eof.per_week below 2 (baseline 3.9)
- Since Done: 23 sessions (9 startup), 1 heredoc_eof error, through 2026-10-09 12:01 UTC
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
  - `later` - owner said not now; re-raise when the metric grows or at the second run after the answer
  - `muted` - owner said never; never raise again, never list, only count
  - `benign` - the agent checked a signal and found it is not a problem (say why in `Owner:`); skip
    it unless its numbers change shape. Saves the next run from re-investigating it.
- **Signal** - the scan metric key(s) and/or the pattern this rests on. This is what new candidates
  are matched against, so a muted item stays muted even when it comes back under new wording.
- **Evidence** - counts with their window, plus the example that convinced you.
- **Fix** - the smallest change and where it lives (file, hook, rule, skill).
- **Verify by** - metric key + target + baseline. Required before an item can be `done`.
- **Done** - when the fix landed (UTC). Only traffic after it counts when judging the fix.
- **Since Done** - the running tally a fix is judged on, so no run re-scans days an earlier run scanned:
  `<N> sessions (<M> startup), <count> <what the Verify by metric counts>, through <YYYY-MM-DD HH:MM> UTC`.
  Every `done` item has one, and so does a `later` or `not working` item that still watches its fix.
  - **Start:** when Done falls inside a run's window, `scan.py --since "<Done>" --until "<window end>"` gives the
    first numbers. An item from before this line existed (2026-10-09) gets it once: from the numbers its History
    already states through `Last run:` when they name sessions and the metric's count, else one
    `scan.py --since "<Done>" --until "<window end>"` run, which already covers this window.
  - **Each later run:** add the window's own counts from `scan.json` (`sessions.count`, `sessions.startup`, the
    metric's `<key>.count`) and set "through" to the window's end, the new `Last run:`. A session active across a
    window's edge counts in both windows' `sessions`, so that sum runs a little high; `startup` counts each fresh
    start once, and event counts never repeat. `scripts/quick_ledger.py --scan-json` prints these sums; it reads the
    count from `<key>.count` when Signal or Verify by names a `<key>.per_week`, so name the key there when one fits.
  - **Not a plain count:** a share keeps its numerator and denominator ("3 of 23 outputs untouched"); a median or
    another number that cannot be summed lists each window's value with its sessions ("10-09: median 1 in 11
    sessions; 10-10: median 2 in 6"). A metric only reading can count (owner asks, a test child) names the count
    read in context. A one-time full re-scan written into `Verify by` with its date (for example "judge on
    11-05 with `--since 10-08`") is the only planned re-scan.
- **Owner** - the owner's answer, verbatim when short; for `muted`, the reason.
- **History** - dated one-liners: raised, answered, done, verified / not working.

## Housekeeping

- Open and active items (`open`, `approved`, `done`, `not working`, `waiting on owner`, `later`)
  stay under **Open items**, newest first.
- `verified`, `muted` and `benign` items move to **Closed items**. Keep their `Signal` line (the matcher needs
  it); fold Evidence and History into one line when the file grows past about 30 KB.
- The Runs table gets one row per run, never edited afterwards.
