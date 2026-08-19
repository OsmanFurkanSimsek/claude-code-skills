# PROJECT.md template

Use this to create the **living source of truth**: stand it up as a skeleton in **Phase 0** (with `TBD (Phase N)` placeholders), then expand it to full depth in **Phase 5** and maintain it every phase thereafter. It holds everything durable about the project - goal, scope, decisions, change log, lessons - and is maintained in place every session (add AND prune), unprompted.

This template is **kept aligned with the `/live-document` skill** (`~/.claude/skills/live-document/references/project-md-template.md`): identical canonical section headers, so a project scaffolded by `/e2e` is recognized and curated by `/live-document`'s Curation mode without any extra work. The e2e-specific additions: the Build/Deliverable notes below, and two **e2e-owned sections** that exist only while a run is active - `## Research notes` (added in Phase 4; template: `references/research-template.md`) and `## Execution plan` (added in Phase 5; template: `references/plan-template.md`; deleted at Phase 12). PROJECT.md is the ONLY tracking file a run produces besides the thin CLAUDE.md.

PROJECT.md is read on demand, **not** auto-loaded (the thin CLAUDE.md is what auto-loads and reminds the agent to read this file). Keep it bounded and skimmable. The standing test: a fresh agent reading only PROJECT.md can continue the project correctly, with nothing re-explained.

---

## Template body (copy and adapt)

```markdown
# PROJECT.md - <project name>

> Single source of truth for this project. A fresh agent reading only this file should be able to
> continue correctly, with nothing re-explained. Built and maintained under `/e2e` (track: <build|deliverable>).
> Maintained every session: live sections edited in place; Change log holds milestones only
> (1-3 lines each, tail compacted as entries age); Lessons appended deduped; obsolete detail
> compacted. The `## Execution plan` section tracks execution
> state; the canonical sections hold everything durable. Do not duplicate one into the other.

<!-- MAINTENANCE CONTRACT - read before editing this file.
This file is re-read IN FULL at the start of every session; every line is paid for on every read.
Update = reconcile, not append.
1. New fact -> find its ONE home section; rewrite that section in place, deleting what it supersedes.
2. Answered Open question -> delete it; fold the answer into Decisions locked or Current state.
3. Change log = milestones only, newest first, 1-3 lines each (what shipped + commit + outcome).
   Verification narratives and review blow-by-blow never belong here. When adding an entry,
   compact any older entry still over 3 lines; its durable content lives in Decisions/Lessons.
4. Before saving, sweep the file: delete or merge every stale, resolved, or duplicated line.
   Deleting stale lines is required maintenance, not data loss; compact real decisions and lessons,
   never drop them.
5. Tripwire: Change log over ~30 lines, any entry over 3 lines, or a diff that only adds lines
   means compaction is overdue - fix it in THIS edit, not later.
Red flag: an edit that only appends. A healthy update rewrites more lines than it adds. -->

## Goal and definition of done
<The outcome that counts as success, and how we will measure it. Pull from the Elon "Question
requirements" step and the discovery outcomes distilled here in Phases 1-2.>

## Scope and non-goals
- In scope: <what the requirements that survived Elon actually cover>
- Out of scope / non-goals: <what was explicitly cut (CEO Review "NOT in scope" + Elon "Delete"), one-line rationale each>

## Current state and next action
<!-- Rewrite in place; must describe only NOW. -->
<What exists today, and the single next action. During Phase 6 this tracks the step in flight; at
Phase 12 it reads "complete" or names the next milestone.>

## Decisions locked
<!-- A changed decision REPLACES the old one; note the change once in Change log. -->
- <Architecture / approach decision> - <one-line rationale citing a Research notes finding or the Elon outcome>
- <Build only: conventions> - languages & versions; **test framework** (every step gets automated
  tests + manual verification); code style / linter; error-handling stance.
- <Deliverable only: format & data decisions> - output format, data sources of record, refresh
  cadence, chart/visual conventions, audience.
- <Declined review findings (Phase 9 critical review), one terse bullet each, so future runs don't re-flag them.>

## Plan / workstreams
<!-- Status markers updated in place: [ ] todo, [~] in progress, [x] done, [!] blocked.
Granular phase/step status lives in the Execution plan section - keep this to the big picture. -->
- [ ] <workstream / milestone>

## Open questions
<!-- Live unknowns only; delete once answered. -->
- <question>

## Change log
<!-- Milestones only, newest first, 1-3 lines each; compact older entries as they age.
     A line every session = a diary = a bug. -->
- <what shipped + commit + outcome>

## Lessons
<!-- Deduped; compact, never lose. -->
- <attempt -> outcome -> lesson>

## Research notes
<!-- e2e-owned; added in Phase 4 from references/research-template.md. Curated: findings that
harden into decisions move to Decisions locked; compacted at Phase 12. -->
<TBD (Phase 4)>

## Execution plan
<!-- e2e-owned; added in Phase 5 from references/plan-template.md. Master phase/step status table
+ detail blocks. Deleted at Phase 12 after the outcome folds into Change log / Current state. -->
<TBD (Phase 5)>
```

The HTML comments are permanent fixtures of the generated file, NOT placeholders: they stay in
`PROJECT.md` forever so every future agent sees the contract at the moment of editing. Only the
`<…>` angle-bracket slots get replaced with real content at scaffold time.

## Section-by-section maintenance contract

| Section | Behavior |
|---|---|
| Goal and definition of done | Mostly stable; revise only if the goal genuinely changes. |
| Scope and non-goals | Edit in place as scope is clarified. |
| Current state and next action | Always rewritten in place to describe *now* (every Phase 6 step, every phase boundary). |
| Decisions locked | Append durable choices; never delete (move/compact only). Architecture + (Build) conventions live here, not in CLAUDE.md. |
| Plan / workstreams | High-level only; update status markers in place. Granular steps are the Execution plan's job. |
| Open questions | Add/remove in place as questions arise and resolve. |
| Change log | Append-only, newest first, milestones only, 1-3 lines each; compact the tail as entries age. |
| Lessons | Append, deduped; compact but never lose a lesson. |
| Research notes (e2e-owned) | Findings + citations; a finding that hardens into a decision moves to Decisions locked; compacted at Phase 12. |
| Execution plan (e2e-owned) | Status table + detail blocks updated at every phase/step boundary; deleted at Phase 12 after folding its outcome into Change log / Current state. |

## Maintenance: keep it relevant, not just append

**Every update to PROJECT.md is also a cleanup.** This file is re-read in full at the start of every session/phase, so every line that is redundant, stale, resolved, or duplicated is paid for again and again. It may grow **only** when there is genuinely more essential information to hold, never from accumulation. Before you add, reconcile: as facts change, update them in place and drop what they replace; as questions resolve, remove them. Duplication and staleness are bugs. There is **no size limit** - a big project may legitimately need a big file - the only test is whether every line still earns its place.

Run this checklist on every update:
- **Supersede in place** - a changed decision overwrites the old one (note the change in Change log); never stack the old and new versions side by side.
- **Resolve and remove** - an answered Open question is deleted and folded into a decision or Current state; Open questions holds only live unknowns.
- **Live sections describe only now** - rewrite Current state and next action and Plan / workstreams in place; nothing historical lingers there.
- **One fact, one home** - a fact lives in exactly one section; don't restate a decision in Current state and Change log too.
- **Change log = milestones, not a diary** - an entry is 1-3 lines (what shipped + commit + outcome); verification narratives and review blow-by-blow never belong in it. Collapse old granular entries once their durable content is captured in Decisions locked / Lessons - the log's tail should decay to ~1 line per milestone.
- **No invented sections** - use only the canonical headers above plus the two e2e-owned sections (Research notes, Execution plan); never add a "Reference"/"Summary"/"Notes" section that duplicates others.
- **Move, don't lose** - never drop a real decision or lesson; compact or relocate, but keep the signal.

## Notes for the writer (Phase 5 and every later phase)

- **Fill from discovery, not imagination.** Goal/Scope/Decisions were distilled here by Phases 1-3 as they ran; Phase 5 deepens them with the Research notes findings. Nothing gets invented at Phase 5 - it synthesizes what the earlier phases already put in this file.
- **This is the home for durable detail.** The thin CLAUDE.md deliberately does NOT hold architecture decisions or conventions - they live here so CLAUDE.md stays ~one screen.
- **Maintain it unprompted.** Phases 6-12 each update this file (Current state, Change log, Decisions, Lessons, Execution plan). The `<!-- live-document:start -->` block in CLAUDE.md is what reminds future sessions to keep doing so after the e2e run ends.
- **One source of truth.** Do not create a second tracking file. PROJECT.md is the only tracker (its Execution plan section carries execution state); CLAUDE.md is a thin bootstrap, not a tracker. (Legacy runs keep their separate PLAN.md for life.)
```
