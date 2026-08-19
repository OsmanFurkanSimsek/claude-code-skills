# CLAUDE.md template (thin constitution / bootstrap)

Use this when creating CLAUDE.md, which now happens in **Phase 0** (stood up with the initial marker) and is finalized in **Phase 5**. CLAUDE.md auto-loads into every session, so it must stay **thin** - roughly one screen. It is a bootstrap, not a log and not a tracker. Everything else lives in **PROJECT.md**: the durable detail (vision, architecture decisions, conventions, change log, lessons) in its canonical sections, the execution status in its `## Execution plan` section, research in `## Research notes`. CLAUDE.md's only jobs are: carry the `e2e-state` resume marker, point at PROJECT.md, and embed the `/live-document` bootstrap block that reminds every future session to read and curate PROJECT.md.

The first line after the title MUST be the e2e-state marker (now including `track=`). The skill's resume detection looks for it explicitly. The `<!-- live-document:start --> … <!-- live-document:end -->` block makes the project interoperable with the `/live-document` skill (its Curation mode detects that marker).

---

## Template body (copy and adapt)

```markdown
# CLAUDE.md - <Project name>

<!-- e2e-state: phase=ready-to-execute step=1 of=<N> track=<build|deliverable> last_checkpoint=<ISO-8601 timestamp UTC> -->

> Thin constitution for this project. The real, single source of truth is `PROJECT.md` (durable
> goal/scope/decisions/change-log/lessons, plus the `## Execution plan` phase/step tracker and
> `## Research notes` while the run is active). The `e2e-state` line above lets `/e2e` resume
> mid-flow after a `/clear`.

## Workflow contract

Built (or being built) under the `/e2e` skill, track **<build|deliverable>**. Phases:
1 Office Hours · 2 CEO Review · 3 Elon · 4 Research · 5 Plan · 6 Execute · 7 Holistic quality pass ·
8 Human review (mandatory before the critical review) · 9 Critical review · 10 Playwright (web frontend only) ·
11 Simplify/tighten · 12 Final verification.

Run `/e2e` in this directory at any time to resume from the `e2e-state` marker.

## Files of note

- `PROJECT.md` - the single source of truth: goal, scope, decisions locked, open questions, change
  log, lessons, plus (while the run is active) `## Research notes` and the `## Execution plan`
  master phase/step status table (with the Phase 8 playtest checklist inside it when applicable).

<!-- live-document:start -->
## Start-of-session protocol (auto-loads)

This block loads automatically every session. Its only job is to bootstrap you.
The real, single source of truth is `PROJECT.md` in this same folder.

Owner: <owner>. Project: <one line>. Dominant rule: <the one constraint that governs every change>.

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
   dropped). One source of truth; never create a second tracking file (PROJECT.md is the only
   tracker; its Execution plan section carries execution state).

### Hard rules
- Dominant constraint: <restate the one rule that governs every decision>.
- Change/approach hierarchy: <smallest viable change first; other project-specific ordering>.
- Ask before assuming - a clarifying question beats a wrong assumption.
- When the user must act: give Summary, then Reasoning, then numbered Steps in super simple words.
  Big work goes in chunks of 5-10 steps, ONE chunk per turn; wait for confirmation, update
  PROJECT.md first (chunk statuses in Plan / workstreams, active chunk in Current state), then say
  the context can be cleared safely. Answers with nothing to do: TLDR first, then detail, no steps.
- Real handoffs (3+ steps or any chunk) also get a Next Actions file pair in `next-actions/`:
  <YYYY-MM-DD_HH-MM>-next-actions.md + an interactive self-contained .html (TLDR paragraph, then
  reasoning with alternatives, then simple steps). Keep every dated pair - the date-time prefix
  finds the latest - and announce both paths in chat.
- Keep the project root tidy: file new screenshots / code examples / reports / next-action files
  into their subfolders; when 3+ loose files of one kind sit at root, propose a move list and tidy
  after ONE confirmation (never move source or config files silently).
- <project-specific guardrail agreed during discovery>
- Avoid the long-dash character in user-facing prose.
<!-- live-document:end -->

## Shipped (filled in at Phase 12)

<!-- Phase 12 appends here -->
```

## Notes for the writer (i.e., the calling skill)

- **Keep it thin.** Target ~one screen. CLAUDE.md is auto-loaded into every session, so length costs tokens forever. If you're tempted to add architecture decisions, conventions, or a change log here, that content belongs in **PROJECT.md** instead.
- **The `e2e-state` marker is the single most important line.** Do not omit it. Do not reformat it. Include `track=<build|deliverable>`. Other tooling parses it. Update it every time you advance a phase or step in Phase 6 (Execute).
- **The `<!-- live-document:start/end -->` block is required.** It is what makes maintenance self-sustaining after the e2e run and what lets the `/live-document` skill recognize the project. Fill the Owner / Project / Dominant rule / Hard rules slots from discovery. Do not delete the markers.
- **Self-heal cue (Next Actions):** a block whose Hard rules have no bullet containing "Next Actions" predates the 2026-07-17 revision; on resume, insert the two bullets above (Next Actions file pair + tidy root) right after the "Summary, then Reasoning" bullet.
- **The "Shipped" section is empty until Phase 12** - leave the placeholder.
- **If the project already has a CLAUDE.md when `/e2e` starts**, merge thoughtfully: keep their existing content, add the `e2e-state` marker and the workflow contract, append the live-document block at the end if it isn't already there, and put any vision/decisions into PROJECT.md rather than bloating CLAUDE.md. Do not overwrite their content without asking.
```
