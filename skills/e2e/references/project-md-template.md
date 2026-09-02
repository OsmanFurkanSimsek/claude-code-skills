# PROJECT.md template

Use this to create the **living source of truth**: stand it up as a skeleton in **Phase 0** (with `TBD (Phase N)` placeholders), then expand it to full depth in **Phase 5** and maintain it every phase thereafter. It holds everything durable about the project - goal, scope, decisions, change log, lessons - and is maintained in place every session (add AND prune), unprompted.

This template is **kept aligned with the `/live-document` skill** (`~/.claude/skills/live-document/references/project-md-template.md`): identical canonical section headers, so a project scaffolded by `/e2e` is recognized and curated by `/live-document`'s Curation mode without any extra work. The e2e-specific additions: the Build/Deliverable notes below, and two **e2e-owned sections** that exist only while a run is active - `## Research notes` (added in Phase 4; template: `references/research-template.md`) and `## Execution plan` (added in Phase 5; template: `references/plan-template.md`; deleted at Phase 12). PROJECT.md is the ONLY tracking file a run produces besides the thin CLAUDE.md.

PROJECT.md has two tiers: Tier 1 (header, Goal, Scope, Map, Current state, Open questions, Decisions locked) is injected every session by the SessionStart hook under a hard 14 KB / 180-line budget; Tier 2 (Plan, Change log, Lessons, Research notes, Execution plan) is read on demand and may grow within per-entry limits. The thin CLAUDE.md auto-loads and reminds the agent which tier to read when. The PROJECT.md hooks (lint on write, Stop gate, PreCompact gate - see live-document SKILL.md, Gates) make the maintenance mandatory. The standing test: a fresh agent reading only PROJECT.md can continue the project correctly, with nothing re-explained.

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

<!-- MAINTENANCE CONTRACT - read before editing this file. Enforced by hooks (project-md-lint).
Tier 1 (injected every session, max 14 KB / 180 lines): header, Goal, Scope, Map, Current state,
Open questions, Decisions locked (rule + who/when + pointer, max 4 lines each).
Tier 2 (read on demand, may grow): Plan, Change log (one entry per date, max 3 lines, older than
14 days -> 1 line, max 30 lines), Lessons (full story, max 8 lines each), Research notes,
Execution plan (deleted at Phase 12).
Home rule: a fact lives in ONE home (lesson story here; rule body in the skill reference; run
analysis in the run file; owner preference in memory); elsewhere one line + a pointer. A line
leaves this file only when its home is named and exists. The Map names every folder and file
that matters and must stay current. Update = reconcile, not append. -->

## Goal and definition of done
<The outcome that counts as success, and how we will measure it. Pull from the Elon "Question
requirements" step and the discovery outcomes distilled here in Phases 1-2.>

## Scope and non-goals
- In scope: <what the requirements that survived Elon actually cover>
- Out of scope / non-goals: <what was explicitly cut (CEO Review "NOT in scope" + Elon "Delete"), one-line rationale each>

## Map - where to find what
<!-- Row 1 = this file (what is ALWAYS here). Every path must exist; every top-level folder appears. -->
| Location | What lives there | Read it when |
|---|---|---|
| `PROJECT.md` | goals, this map, current state + next action, open questions, decisions index, lessons, milestones | every session (Tier 1 auto-injected) |
| `<folder or file>` | <what lives there> | <when to read it> |

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
| Map - where to find what | Edited in the same write as any file or folder added, moved, or archived; every path must exist; every top-level folder appears. |
| Current state and next action | Always rewritten in place to describe *now* (every Phase 6 step, every phase boundary). |
| Decisions locked | Supersede in place (a new decision replaces the one it supersedes); rule + who/when + pointer, max 4 lines. Architecture + (Build) conventions live here, not in CLAUDE.md. |
| Plan / workstreams | High-level only; update status markers in place. Granular steps are the Execution plan's job. |
| Open questions | Add/remove in place as questions arise and resolve. |
| Change log | Newest first, milestones only, one entry per date, 1-3 lines each; entries older than 14 days shrink to one line; max 30 lines. |
| Lessons | Full story, max 8 lines each, deduped against Decisions; the memory file is a pointer. Never lose a lesson. |
| Research notes (e2e-owned) | Findings + citations; a finding that hardens into a decision moves to Decisions locked; compacted at Phase 12. |
| Execution plan (e2e-owned) | Status table + detail blocks updated at every phase/step boundary; deleted at Phase 12 after folding its outcome into Change log / Current state. |

## Maintenance: keep it relevant, not just append

**Every update to PROJECT.md is also a cleanup, and the file has two tiers.** Tier 1 (header, Goal, Scope, Map, Current state, Open questions, Decisions locked) is injected every session by the SessionStart hook under a hard 14 KB / 180-line budget; Tier 2 (Plan, Change log, Lessons, Research notes, Execution plan) is read on demand and may grow within per-entry limits. More context beats no context, but bloat loses to optimal context: reconcile before you add, and apply the home rule - a fact lives in ONE home (lesson story here, rule body in the owning skill's references, run analysis in the run file, owner preference in memory) and appears elsewhere as one line plus a pointer. A line may leave this file only when its home is named and exists. The hooks (`project-md-lint`, the Stop gate, the PreCompact gate) enforce all of this.

Run this checklist on every update:
- **Supersede in place** - a changed decision overwrites the old one (note the change in Change log); never stack the old and new versions side by side.
- **Resolve and remove** - an answered Open question is deleted and folded into a decision or Current state; Open questions holds only live unknowns.
- **Live sections describe only now** - rewrite Current state and next action and Plan / workstreams in place; nothing historical lingers there.
- **One fact, one home** - a fact lives in exactly one section; don't restate a decision in Current state and Change log too.
- **Change log = milestones, not a diary** - an entry is 1-3 lines (what shipped + commit + outcome); verification narratives and review blow-by-blow never belong in it. Collapse old granular entries once their durable content is captured in Decisions locked / Lessons - the log's tail should decay to ~1 line per milestone.
- **Home rule** - one home per fact; pointers everywhere else; never delete a line whose home does not exist yet.
- **Map current** - any file or folder added, moved, or archived gets its Map row in the same edit; every path in the Map exists.
- **No invented sections** - use only the canonical headers above (including Map - where to find what) plus the two e2e-owned sections (Research notes, Execution plan), with no suffixes; never add a "Reference"/"Summary"/"Notes" section that duplicates others.
- **Move, don't lose** - never drop a real decision or lesson; compact or relocate, but keep the signal.

## Notes for the writer (Phase 5 and every later phase)

- **Fill from discovery, not imagination.** Goal/Scope/Decisions were distilled here by Phases 1-3 as they ran; Phase 5 deepens them with the Research notes findings. Nothing gets invented at Phase 5 - it synthesizes what the earlier phases already put in this file.
- **This is the home for durable detail.** The thin CLAUDE.md deliberately does NOT hold architecture decisions or conventions - they live here so CLAUDE.md stays ~one screen.
- **Maintain it unprompted.** Phases 6-12 each update this file (Current state, Change log, Decisions, Lessons, Execution plan). The `<!-- live-document:start -->` block in CLAUDE.md is what reminds future sessions to keep doing so after the e2e run ends.
- **One source of truth.** Do not create a second tracking file. PROJECT.md is the only tracker (its Execution plan section carries execution state); CLAUDE.md is a thin bootstrap, not a tracker. (Legacy runs keep their separate PLAN.md for life.)
```
