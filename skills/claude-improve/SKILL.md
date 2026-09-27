---
name: claude-improve
description: Use when the user types /claude-improve, asks for the weekly Claude Code review, or asks to go through past Claude Code conversations or transcripts to find what to improve ("how can we use Claude Code better", "review our sessions", "what keeps going wrong", "improve my Claude setup", "audit my transcripts"), or when a session-start note says the review is due. Do NOT use to debug one live failure, to review a code diff, or to sync or back up skills.
---

# Claude Improve - the weekly review of how Claude Code is working

Measure the recent sessions from Claude Code's own transcripts, compare them with the **ledger** of
everything recommended before, and bring the owner only three things: what was fixed (and whether the
fix worked), what is still waiting, and what is new. **Zero new recommendations is a valid result**;
there is no quota in either direction.

The ledger is what makes this weekly instead of one-off: it remembers every recommendation, the
owner's answer, the baseline number, and how to check it. An item the owner muted is never raised
again.

## Rules that hold in every run

- **No number, no recommendation.** Every finding cites counts from this run's scan and at least one
  real example. "Might be nice" ideas without evidence stay out.
- **The ledger decides what is new.** Match each candidate against it before writing anything:
  muted -> skip silently; open or approved -> update that item's evidence; only true novelties get a
  new ID.
- **Fold before adding.** The best fix is usually one line in an existing rule file, a tweak to an
  existing hook, or an edit to an existing skill. A new skill, hook or tool needs a reason why no
  existing home works.
- **A rule the agent keeps breaking needs enforcement, not repetition.** If the owner already wrote
  the rule and it is still broken, the fix is moving it closer (into the file being edited, a hook,
  a check), never a second copy of the same sentence.
- **Never mask a bad number.** If a metric looks wrong, find out why (a tracking gap, a scan bug, a
  real regression). Do not drop it or smooth it.
- **The owner decides.** You propose; nothing in the setup changes before the answer, except fixing
  the scan script itself.
- **Secrets are counted, never printed.** `scan.py` redacts them and flags them at the top of the
  report. Never grep a transcript in a way that prints the value; locate by session id only. A
  long-lived secret found in plain text is always the report's first item: the owner rotates it.

## Step 0 - Find and read the ledger

1. `project-memory/claude-improve-ledger.md` in the current folder; else
2. the path under `"ledger"` in `~/.claude/claude-improve.json`; else
3. ask once where it should live (suggest `project-memory/` of the repo that holds the owner's
   Claude setup, or of the current folder), create it from `references/ledger-format.md`, and write
   `~/.claude/claude-improve.json` as `{"ledger": "<absolute path>"}`.

Read the ledger **in full**. Note its `Last run:` date and every item's status.

## Step 1 - Scan

**Window: from the previous run to now, never a fixed week.** `--since` is the ledger's `Last run:`
date, however long ago it was: a review skipped for three weeks scans all three, so no session ever
falls between two runs. The window starts at the beginning of that day, so it overlaps the last run
slightly; overlap is harmless (metrics are per 7 days), a gap is not. Only two exceptions: a first
run (no `Last run:`) scans 30 days, and a run within 3 days of the last one still scans 3 days, so
there is enough data to compare.

```bash
python "<this skill>/scripts/scan.py" --from-ledger "<ledger path>" --out "<scratchpad>/scan.md" --json "<scratchpad>/scan.json"
```

`--from-ledger` applies exactly these rules; the report's first line states the window it used.

About one minute per 50 sessions; read-only. Read `scan.md` in full (about 25 KB). Its last section is
the metrics JSON with stable keys, normalised to per-7-days, which the ledger's `Verify by` lines use.
If the scan shows something it cannot explain (a zero where there should be traffic, an impossible
number), fix `scan.py` first and re-run; a wrong scan poisons every step after it.

## Step 2 - Check the past before the new

For every ledger item, in this order:

| Status | What to do this run |
|---|---|
| `done` | Judge it ONLY on traffic after its `Done:` time: re-run `scan.py --since "<Done time>"` for that metric. Fewer than 3 days or 10 sessions since then -> "too early", stays `done`. Improved as expected -> `verified` (before -> after). No change -> `not working`; it goes back to the owner. Never judge a fix on traffic from before it landed. |
| `open` | Raised but never answered: ask again in Step 5, with this run's numbers. |
| `not working` | Ask again in Step 5 with a different next move, never the same fix twice. |
| `approved` | Still not done after 2 runs -> list it under "stuck on our side" with the reason. |
| `waiting on owner` | List it under "still waiting on you", with the date first raised. Neutral wording, one line. |
| `later` | Re-raise only if its metric grew, or 4 weeks have passed since the answer. |
| `muted` | Never raise, never list. Count them in one line. |
| `benign` | Skip; re-check only if its numbers change shape (not just size). |
| `verified` | Nothing, unless the metric regressed past its baseline; then re-open as `not working`. |

## Step 3 - Find what is new

Work through `references/playbook.md` (signal -> how to confirm -> usual fix). For every signal that
looks worth raising:

1. **Confirm it in the raw transcripts** before believing it: grep the example text from `scan.md` in
   `~/.claude/projects/*/*.jsonl` and read 1-3 cases in context. Many signals are benign (a gate
   that correctly blocked a real mistake, a correction that was really a new request).
2. **Match it against the ledger** by signal AND cause: the same metric with a different cause (big
   results from file reads vs. from web fetches) is a new item. A muted item mutes its own proposal,
   not every future finding on that metric.
3. **Keep it only if** it recurs (3+ times, or once at real cost), has a concrete fix, and the fix
   costs less than the problem.

When confirming needs more than a few transcript reads, hand the digging to a helper agent on the
same model: it writes what it found to a scratch file and returns a short summary plus the path.
Full transcripts in the main context are the very bloat this review looks for.

## Step 4 - Report

In this order, plain words, numbers inline:

1. **Summary** - window, sessions, spend, and the one headline (2-4 sentences).
2. **Fixed and working** - one line each: item, before -> after.
3. **Not working yet** - item, what the numbers show, the proposed next move.
4. **Still waiting** - on the owner / on us, one line each with the date first raised.
5. **New** - numbered; each: plain-words title, evidence (counts + one short example), the smallest
   fix and where it lives, effort, and the metric that will show next week whether it worked.
6. **Muted** - one line: "N muted items skipped" (list them only if asked).

Nothing new? Say so in one line under **New**. Always save the full report as
`reports/YYYY-MM-DD_claude-improve.md` in the ledger's project. If the owner's rules say nothing may
come before a decision pop-up, show the pop-up first (the report path in the first question) and the
chat summary after the answers.

## Step 5 - Ask, one decision per recommendation

Use the AskUserQuestion pop-up: one question per new, `open` or `not working` item, up to 4 questions per
pop-up (a second pop-up for the rest). Chips, in this order:

- `A. Do it (Recommended)` - preview: WHAT IT TAKES (1-3 bullets), RISKS (with high / medium / low)
- `B. Later` - preview: what waiting costs per week, in the scan's numbers
- `C. Never - mute it` - preview: "Muted for good; never raised again."
- `D. Your own idea` - preview: "Pick this, press n, and type what you want instead."

If the owner's setup defines its own decision format (a rules file or CLAUDE.md), follow that
instead. Without a pop-up tool, ask the same choices in one short numbered list.

## Step 6 - Record, then act

1. **Ledger first, right after the answers:** status, the owner's words in `Owner:` (verbatim when
   short), today's date in `History:`. Set `Last run:` to now as `YYYY-MM-DD HH:MM` UTC (the next
   run's `--since`) and add one `Runs` row whose Window shows the exact from and to scanned.
2. **Do it** + small and reversible (under ~30 minutes): do it now, verify it, set `done` with
   `Done: YYYY-MM-DD HH:MM` UTC, `Verify by` + baseline. Larger: status `approved` and add it to the project's plan as its own
   chunk; say which session will do it.
3. **Later** -> `later`. **Never** -> `muted` with the reason. **Own idea** -> rewrite the item from
   the owner's words, then treat it as `Do it`.
4. If the ledger lives in a git repo, commit it with that repo's normal flow.

## Common mistakes

| Mistake | Instead |
|---|---|
| Padding the list to look thorough, or cutting it to a round number | Report exactly what the evidence supports |
| Re-raising a muted item with new wording | Match by `Signal:`, not by title |
| Calling a fix "done" without a metric | Every `done` item needs `Verify by` + baseline |
| Believing a keyword hit (a "correction" that was a new request) | Read the case in context first |
| Proposing a new skill or hook first | Name the existing home that could hold it, or why none can |
| Dumping transcripts into the main context | Helper agent writes to a file; read only what you need |
| Leaving "not working" fixes silently `done` | Re-open them with the numbers; they go to the owner |

## Weekly reminder (optional)

A SessionStart hook can read the ledger's `Last run:` line and add one sentence to the session's
context when 7+ days have passed ("claude-improve is due; offer it at a natural pause"). Keep it to
one line, once per day. The review itself always runs on the owner's word, never automatically.
