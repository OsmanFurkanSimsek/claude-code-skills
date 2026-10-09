---
name: claude-improve
description: Use when the user types /claude-improve, asks for the Claude Code review (weekly, monthly, or whenever), or asks to go through past Claude Code conversations or transcripts to find what to improve ("how can we use Claude Code better", "review our sessions", "what keeps going wrong", "improve my Claude setup", "audit my transcripts"), types /doctor or asks for /insights together with the review, or when a session-start note says the review is due. Do NOT use to debug one live failure, to review a code diff, or to sync or back up skills.
---

# Claude Improve - review how Claude Code has been working since the last review

Run it whenever the owner likes (after 5 days, a month or three months): it measures **every session
since the previous review** from Claude Code's own transcripts, compare them with the **ledger** of
everything recommended before, and bring the owner only three things: what was fixed (and whether the
fix worked), what is still waiting, and what is new. **Zero new recommendations is a valid result**;
there is no quota in either direction.

The ledger is what makes this a continuing review instead of a one-off: it remembers every recommendation, the
owner's answer, the baseline number, and how to check it. An item the owner muted is never raised
again.

## Rules that hold in every run

- **Never redo audited work.** Every source starts at the ledger's `Last run:`; what came before was audited by
  the previous run. A point already in the ledger (an item, or a line under "Checked, no action") is skipped
  unless new evidence after `Last run:` changes it. The owner, 2026-10-09: "be sure to save time when we run it, so
  we don't rerun the already audited sessions ... check when we did it last time and solve the problem we haven't
  solved yet. I don't want double work."
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

**Window: from the previous run to now. Never time-bound.** The start is the ledger's `Last run:`
date and time, however long or short ago: 5 days, a month and three months are all covered in full,
so no session ever falls between two runs. A first run (no `Last run:`) covers every transcript on
disk. Metric keys ending in `.per_week` are rates (count x 7 / days scanned), only so runs of
different lengths compare fairly; they are not a limit.

```bash
python "<this skill>/scripts/scan.py" --from-ledger "<ledger path>" --out "<scratchpad>/scan.md" --json "<scratchpad>/scan.json"
```

`--from-ledger` applies exactly these rules; the report's first line states the window it used.

About one minute per 50 sessions; read-only. Read `scan.md` in full (about 25 KB). Its last section is
the metrics JSON with stable keys, normalised to per-7-days, which the ledger's `Verify by` lines use.
If the scan shows something it cannot explain (a zero where there should be traffic, an impossible
number), fix `scan.py` first and re-run; a wrong scan poisons every step after it.

## Step 1b - Setup health (/doctor) and Claude Code's own session report (/insights)

Two more sources for Step 3, in every run (owner, 2026-10-09: "make them part of" the review "so we don't miss
anything"). Neither changes anything; their findings become candidates like any scan signal.

- **/doctor** (the built-in setup check: install, unused extensions, CLAUDE.md size, slow hooks, version,
  permissions) is reserved for the owner to start. When he typed it with the review (`/claude-improve /doctor`),
  the MAIN session runs its checks read-only itself; a helper cannot load it and refuses its check list (10-09,
  twice). Data first, one read-only script: `python "<this skill>/scripts/doctor_data.py" "<scratchpad>/doctor-data.md"
  "<project dir>" "<Last run, YYYY-MM-DD HH:MM>"` (config and parse checks, lifetime usage counters, plugins; hook
  durations, calls and denials only since `Last run:`; never `env` values; about 5 s), then judge each check and
  write one line per check, "nothing found" included. An extension verdict already under "Checked, no action" is
  re-judged only when its counter moved. Skip its own confirm-and-apply
  questions: its proposals go through Step 5. Without /doctor in his message, say in one line that it was not
  included and how to include it next time.
- **/insights** runs without him, in a background print-mode child (about 70 s, cwd in the scratchpad):
  `MSYS_NO_PATHCONV=1 env -u ANTHROPIC_API_KEY claude -p "/insights" --disallowedTools "Write,Edit,NotebookEdit,Agent" --no-session-persistence`
  (`MSYS_NO_PATHCONV=1`, or Git Bash turns `/insights` into a folder path). It prints the report path
  (`~/.claude/usage-data/report-<date>.html`); `scripts/html2text.py <html> <txt>` makes it readable. Its points are
  model-estimated over months, but it caches each session's analysis and adds only new sessions. Map EVERY point
  and suggestion: one already under "Checked, no action" or in an item is skipped unless it names something after
  `Last run:`; a new one gets its item or a verdict, confirmed only in transcripts after `Last run:` (a helper for
  more than a few reads). Record each verdict under "Checked, no action" in the ledger.

## Step 2 - Check the past before the new

For every ledger item, in this order:

| Status | What to do this run |
|---|---|
| `done` | Judge it ONLY on traffic after its `Done:` time: re-run `scan.py --since "<Done time>"` for that metric. Fewer than 10 sessions since then -> "too early", stays `done`. A fix that needs a restart (settings env, MCP, profile) counts only sessions with start source `startup`: a /clear or /compact session keeps its old process (`scan.py` prints the source). Improved as expected -> `verified` (before -> after). No change -> `not working`; it goes back to the owner. Never judge a fix on traffic from before it landed. |
| `open` | Raised but never answered: ask again in Step 5, with this run's numbers. |
| `not working` | Ask again in Step 5 with a different next move, never the same fix twice. |
| `approved` | Still not done after 2 runs -> list it under "stuck on our side" with the reason. |
| `waiting on owner` | List it under "still waiting on you", with the date first raised. Neutral wording, one line. |
| `later` | Re-raise when its metric grew, or at the second run after the answer. |
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

When confirming needs more than a few transcript reads, hand the digging to a helper agent of the
tier the task needs: it writes what it found to a scratch file and returns a short summary plus the path.
Full transcripts in the main context are the very bloat this review looks for.

## Step 4 - Report

In this order, plain words, numbers inline:

1. **Summary** - window, sessions, spend, and the one headline (2-4 sentences).
2. **Fixed and working** - one line each: item, before -> after.
3. **Not working yet** - item, what the numbers show, the proposed next move.
4. **Still waiting** - on the owner / on us, one line each with the date first raised.
5. **New** - numbered; each: plain-words title, evidence (counts + one short example), the smallest
   fix and where it lives, effort, and the metric that will show at the next run whether it worked.
6. **Setup health (/doctor)** - one line per check, a keep or turn-off verdict with one reason for every unused
   extension, then **/insights** - every point and suggestion with its item or a yes/no and one reason.
7. **Muted** - one line: "N muted items skipped" (list them only if asked).

Nothing new? Say so in one line under **New**. Always save the full report as
`reports/YYYY-MM-DD_claude-improve.md` in the ledger's project. If the owner's rules say nothing may
come before a decision pop-up, show the pop-up first (the report path in the first question) and the
chat summary after the answers.

## Step 5 - Ask, one decision per recommendation

Use the AskUserQuestion pop-up: one question per new, `open` or `not working` item, up to 4 questions per
pop-up (a second pop-up for the rest). Chips, in this order:

A change that lets more run without asking (a default permission mode, an allow rule) is always its own question,
never part of a clean-up item.

- `A. Do it (Recommended)` - preview: WHAT IT TAKES (1-3 bullets), RISKS (with high / medium / low)
- `B. Later` - preview: what waiting costs until the next run, in the scan's numbers
- `C. Never - mute it` - preview: "Muted for good; never raised again."
- `D. Your own idea` - preview: "Pick this, press n, and type what you want instead."

If the owner's setup defines its own decision format (a rules file or CLAUDE.md), follow that
instead, but keep `C. Never - mute it` on every item: A-B are the two best options (one may be `Later`), C mutes,
D is his own idea (owner, 2026-10-09: muting stays one click, the ledger depends on it). Without a pop-up tool,
ask the same choices in one short numbered list.

## Step 6 - Record, then act

1. **Ledger first, right after the answers:** status, the owner's words in `Owner:` (verbatim when
   short), today's date in `History:`. Set `Last run:` to the END of the window this run scanned (the
   scan's first line), as `YYYY-MM-DD HH:MM` UTC: it is the next run's `--since`, and the time of writing would
   leave the sessions between the scan and the write unscanned for good. Add one `Runs` row whose Window
   shows the exact from and to scanned.
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
| Handing /doctor's checks to a helper | It refuses; the main session runs them on the owner's own /doctor |
| "Nothing new from /insights" after checking only some of its points | Map every point and suggestion, one line each |
| Leaving "not working" fixes silently `done` | Re-open them with the numbers; they go to the owner |

## Reminder (optional, never a limit)

A SessionStart hook can read the ledger's `Last run:` line and add one sentence to the session's
context when the owner's chosen gap has passed ("claude-improve is due; offer it at a natural
pause"). Keep it to one line, once per day. It only reminds: whenever the review runs, it still
covers everything since the last run, and it runs on the owner's word, never automatically.
