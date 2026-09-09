# `claude-md-block.md` - the thin bootstrap to append/create

Append this block to the project-root `CLAUDE.md` (or create the file with it). Preserve any
existing content above it. Fill the `<…>` slots from the interview. Keep it thin - this file
auto-loads every session and must NOT grow into a log.

```markdown
<!-- live-document:start -->
## Start-of-session protocol (auto-loads)

This block loads automatically every message. Its only job is to bootstrap you.
The real source of truth is `PROJECT.md` in this same folder (read once per session), with every
detail in `project-memory/` (read on demand via its Map).

Owner: <owner>. Project: <one line>. Dominant rule: <the one constraint that governs every change>.

### Do this every session, without being told
1. Read `PROJECT.md` IN FULL at session start, before acting - the SessionStart hook only tells
   you its size and lists the `project-memory/` files; the edit gate denies project writes until
   you have read it. Open a `project-memory/` file when its Map row says the task touches it, and
   ALWAYS before editing it. The user never has to ask.
2. After meaningful work, update the living setup by RECONCILING, not appending - project-memory
   home FIRST, `PROJECT.md` LAST: Current state always; a new durable choice REPLACES the one it
   supersedes in `project-memory/decisions.md` (full wording) and in Decisions locked (rule +
   who/when, max 2 lines); an answered Open question is deleted and folded into a decision; a
   milestone gets one 1-3 line entry in `project-memory/changelog.md` (one per date, never a diary).
3. Lock the feedback - home rule: a lesson's story goes to `project-memory/lessons.md` (max 8
   lines, under its theme), its rule to `PROJECT.md` Lessons (max 3 lines) only if it changes how
   we work here, and its memory file is a pointer; an owner preference goes to memory in full.
   Never two stories of one lesson. Keep the Map current: one row per project-memory file with a
   summary and a "read it when", and a row for every folder or file added, moved, or archived.
4. Before saving, sweep: delete or merge everything now redundant, resolved, stale, or duplicated
   - a line may leave only when its home is named and exists. `PROJECT.md` stays under 20 KB / 250
   lines with no change log, research notes or execution plan inside it. Tripwires are enforced by
   hooks: the lint blocks a malformed write, the Stop gate will not end a turn that edited project
   files until `PROJECT.md` is reconciled and lints clean, and one compaction is held while a
   reconcile is pending. Fix in THIS edit, not later. Never a tracking file outside `project-memory/`.

### Hard rules
- Dominant constraint: <restate the one rule that governs every decision>.
- Change/approach hierarchy: <smallest viable change first; <other project-specific ordering>>.
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
- <project-specific guardrail agreed during setup>
- Never use the long-dash character.
<!-- live-document:end -->
```

## Notes for the agent applying this block

- The `<!-- live-document:start -->` / `<!-- live-document:end -->` markers are how the skill
  later detects that a project is already set up (Curation mode). Keep them intact.
- Self-heal detection cue: an OLD-style block is recognizable by the phrase "after any answer or
  change", an item saying "Curate, do not bloat", or items 2-4 that lack the word "Tripwire"
  (pre entry-length-cap discipline). On next touch, Curation mode replaces items 2-4 of that
  block with the current ones above (see SKILL.md).
- Hard rules: add as many bullets as needed. Include the dominant constraint, the change/approach
  hierarchy, "ask before assuming", the Summary/Reasoning/Steps chunk-delivery rule, the Next
  Actions + tidy-root bullets, and any project-specific guardrails agreed during the interview.
- Self-heal cue (home rule, 2026-09-02): a block whose items 1-4 lack the phrase "home rule"
  predates the two-tier / hooks revision; on next touch, Curation mode replaces items 1-4 with the
  current ones above.
- Self-heal cue (project-memory, 2026-09-09): a block whose items 1-4 lack the phrase
  "project-memory" predates the three-layer layout (PROJECT.md read once per session +
  `project-memory/` detail folder); Curation mode replaces items 1-4 with the current ones above
  as part of the project's migration (see SKILL.md, self-heal, and
  `references/project-memory-template.md`).
- Self-heal cue (Next Actions): a block whose Hard rules have no bullet containing "Next Actions"
  predates the 2026-07-17 revision; on next touch, Curation mode inserts the two bullets above
  (Next Actions file + tidy root) right after the "Summary, then Reasoning" bullet.
- If a `CLAUDE.md` already exists, this block goes at the END, leaving all prior content untouched.
