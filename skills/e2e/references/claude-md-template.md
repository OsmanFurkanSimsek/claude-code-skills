# CLAUDE.md template (thin constitution / bootstrap)

Use this when creating CLAUDE.md, which now happens in **Phase 0** (stood up with the initial marker) and is finalized in **Phase 5**. CLAUDE.md auto-loads into every message, so it must stay **thin** - roughly one screen. It is a bootstrap, not a log and not a tracker. Everything else lives in **PROJECT.md** (read in full once per session: goal, scope, the Map, current state, decision and key-lesson rule lines) and **`project-memory/`** (read on demand: full decision wording, lesson stories, the changelog, and while the run is active `research-notes.md` and `execution-plan.md`). CLAUDE.md's only jobs are: carry the `e2e-state` resume marker, point at PROJECT.md, and embed the `/live-document` bootstrap block that reminds every future session to read and curate the living docs.

The first line after the title MUST be the e2e-state marker (now including `track=`). The skill's resume detection looks for it explicitly. The `<!-- live-document:start --> … <!-- live-document:end -->` block makes the project interoperable with the `/live-document` skill (its Curation mode detects that marker).

---

## Template body (copy and adapt)

```markdown
# CLAUDE.md - <Project name>

<!-- e2e-state: phase=ready-to-execute step=1 of=<N> track=<build|deliverable> last_checkpoint=<ISO-8601 timestamp UTC> -->

> Thin constitution for this project. The real source of truth is `PROJECT.md` (read once per
> session: goal, scope, the Map, current state, decisions and key lessons) with every detail in
> `project-memory/` (read on demand: full decision wording, lesson stories, the changelog, and while
> the run is active `execution-plan.md` and `research-notes.md`). The `e2e-state` line above lets
> `/e2e` resume mid-flow after a `/clear`.

## Workflow contract

Built (or being built) under the `/e2e` skill, track **<build|deliverable>**. Phases:
1 Office Hours · 2 CEO Review · 3 Elon · 4 Research · 5 Plan · 6 Execute · 7 Holistic quality pass ·
8 Human review (mandatory before the critical review) · 9 Critical review · 10 Playwright (web frontend only) ·
11 Simplify/tighten · 12 Final verification.

Run `/e2e` in this directory at any time to resume from the `e2e-state` marker.

## Files of note

- `PROJECT.md` - the single source of truth, read in full once per session: goal, scope, the Map,
  current state, decisions locked, open questions, key lessons.
- `project-memory/` - the detail layer, read on demand via the Map: `decisions.md`, `lessons.md`,
  `changelog.md`, and while the run is active `research-notes.md` and `execution-plan.md` (the
  master phase/step status table, with the Phase 8 playtest checklist inside it when applicable).

<!-- live-document:start -->
## Start-of-session protocol (auto-loads)

This block loads automatically every message. Its only job is to bootstrap you.
The real source of truth is `PROJECT.md` in this same folder (read once per session), with every
detail in `project-memory/` (read on demand via its Map).

Owner: <owner>. Project: <one line>. Dominant rule: <the one constraint that governs every change>.

### Do this every session, without being told
1. Read `PROJECT.md` IN FULL at session start, before acting - the SessionStart hook only tells
   you its size and lists the `project-memory/` files; the edit gate denies project writes until
   you have read it. Open a `project-memory/` file when its Map row says the task touches it
   (`execution-plan.md` on every phase and step of the run), and ALWAYS before editing it.
2. After meaningful work, update the living setup by RECONCILING, not appending - project-memory
   home FIRST, `PROJECT.md` LAST: Current state always; a new durable choice REPLACES the one it
   supersedes in `project-memory/decisions.md` (full wording) and in Decisions locked (rule +
   who/when + a one-line why, max 3 lines); an answered Open question is deleted and folded into a decision; a
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
   reconcile is pending. Fix in THIS edit, not later. Never a tracking file outside `project-memory/`
   (`execution-plan.md` there carries execution state).

### Hard rules
- Dominant constraint: <restate the one rule that governs every decision>.
- Change/approach hierarchy: <smallest viable change first; other project-specific ordering>.
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
- <project-specific guardrail agreed during discovery>
- Avoid the long-dash character in user-facing prose.
<!-- live-document:end -->

## Shipped (filled in at Phase 12)

<!-- Phase 12 writes TWO lines here: "Concluded <date>." and "What shipped and the current state
live in PROJECT.md, Current state and next action." CLAUDE.md never carries project state. -->
```

## Notes for the writer (i.e., the calling skill)

- **Keep it thin.** Target ~one screen. CLAUDE.md is auto-loaded into every message, so length costs tokens forever. If you're tempted to add architecture decisions, conventions, or a change log here, that content belongs in **PROJECT.md** / **`project-memory/`** instead.
- **The `e2e-state` marker is the single most important line.** Do not omit it. Do not reformat it. Include `track=<build|deliverable>`. Other tooling parses it. Update it every time you advance a phase or step in Phase 6 (Execute).
- **The `<!-- live-document:start/end -->` block is required.** It is what makes maintenance self-sustaining after the e2e run and what lets the `/live-document` skill recognize the project. Fill the Owner / Project / Dominant rule / Hard rules slots from discovery. Do not delete the markers.
- **Self-heal cue (Next Actions):** a block whose Hard rules have no bullet containing "Next Actions" predates the 2026-07-17 revision; on resume, insert the two bullets above (Next Actions file + tidy root) right after the "Summary, then Reasoning" bullet.
- **The "Shipped" section is empty until Phase 12** - leave the placeholder; at Phase 12 it becomes a two-line pointer, never a summary (a summary here goes stale and duplicates PROJECT.md).
- **Self-heal cue (home rule, 2026-09-02):** a block whose items 1-4 lack the phrase "home rule" predates the two-tier / hooks revision; on resume, replace items 1-4 with the current ones above.
- **Self-heal cue (project-memory, 2026-09-09):** a block whose items 1-4 lack the phrase "project-memory" predates the three-layer layout; replace items 1-4 with the current ones above as part of the project's migration at the next phase boundary (see SKILL.md self-heal item (g)).
- **If the project already has a CLAUDE.md when `/e2e` starts**, merge thoughtfully: keep their existing content, add the `e2e-state` marker and the workflow contract, append the live-document block at the end if it isn't already there, and put any vision/decisions into PROJECT.md / `project-memory/decisions.md` rather than bloating CLAUDE.md. Do not overwrite their content without asking.
