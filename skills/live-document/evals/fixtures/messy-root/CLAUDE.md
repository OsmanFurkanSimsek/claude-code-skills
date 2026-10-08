# CLAUDE.md - weather-dashboard

<!-- live-document:start -->
## Start-of-session protocol (auto-loads)

This block loads automatically every session. Its only job is to bootstrap you.
The real, single source of truth is `PROJECT.md` in this same folder.

Owner: Osman. Project: weather-dashboard, a small Flask app showing local forecast charts.
Dominant rule: stay under the free-tier API quota (1000 calls/day); cache aggressively.

### Do this every session, without being told
1. Read `PROJECT.md` in full BEFORE acting. The user should never have to ask you to.
2. After meaningful work, update `PROJECT.md` by RECONCILING it, not appending to it: rewrite the
   sections the work touched (Current state always; a new durable choice REPLACES the decision it
   supersedes in Decisions locked; an answered Open question is deleted, its answer folded into a
   decision). Change log = milestones only, 1-3 lines each (what shipped + commit + outcome, never
   verification narratives or review blow-by-blow); when adding an entry, compact any older entry
   still over 3 lines - by then its durable content lives in Decisions/Lessons, not in the log.
3. Lock the feedback: when the user corrects course or something fails, record what was tried,
   what failed, and the lesson in Lessons (deduped).
4. Before saving, sweep the whole file: delete or merge everything now redundant, resolved, stale,
   or duplicated. PROJECT.md is re-read in full every session, so every stale line is paid for on
   every read. Tripwire: Change log over ~30 lines, any entry over 3 lines, or an append-only
   diff - compact in THIS edit, not later. Deleting a line that no longer earns its place is
   REQUIRED maintenance, not data loss (real decisions and lessons are compacted or moved, never
   dropped). One source of truth; never create a second tracking file.

### Hard rules
- Dominant constraint: stay under the free-tier API quota; cache every upstream call.
- Ask before assuming - a clarifying question beats a wrong assumption.
- When the user must act: give Summary, then Reasoning, then numbered Steps in super simple words.
  Big work goes in chunks of 5-10 steps, ONE chunk per turn; wait for confirmation, update
  PROJECT.md first (chunk statuses in Plan / workstreams, active chunk in Current state), then say
  the context can be cleared safely. Answers with nothing to do: TLDR first, then detail, no steps.
- Real handoffs (3+ steps or any chunk) also get a Next Actions file in `next-actions/`:
  an interactive self-contained <YYYY-MM-DD_HH-MM>-next-actions.html (TLDR paragraph, then
  reasoning with alternatives, then simple steps). Keep every dated file - the date-time prefix
  finds the latest - and announce the path in chat.
- Keep the project root tidy: file new screenshots / code examples / reports / next-action files
  into their subfolders; when 3+ loose files of one kind sit at root, propose a move list and tidy
  after ONE confirmation (never move source or config files silently).
- Never use the long-dash character.
<!-- live-document:end -->
