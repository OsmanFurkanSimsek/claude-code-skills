# PROJECT.md template

Use this to create the **living source of truth**: stand it up as a skeleton in **Phase 0** (with `TBD (Phase N)` placeholders), then expand it to full depth in **Phase 5** and maintain it every phase thereafter. It holds the important things about the project - goal, scope, the Map, current state, decision and key-lesson rule lines - and is maintained in place every session (add AND prune), unprompted. Everything with more detail than a rule line lives in `project-memory/` (see live-document's `references/project-memory-template.md`).

This template is **kept aligned with the `/live-document` skill** (`~/.claude/skills/live-document/references/project-md-template.md`): identical canonical section headers, so a project scaffolded by `/e2e` is recognized and curated by `/live-document`'s Curation mode without any extra work. The e2e-specific additions: the Build/Deliverable notes below, and two **e2e-owned project-memory files** that exist only while a run is active - `project-memory/research-notes.md` (added in Phase 4; template: `references/research-template.md`) and `project-memory/execution-plan.md` (added in Phase 5; template: `references/plan-template.md`; deleted at Phase 12). A run produces PROJECT.md, the thin CLAUDE.md, and the `project-memory/` folder - no tracking file outside those.

The living setup has three layers by read frequency (live-document, 2026-09-09): `CLAUDE.md` is read every message (thinnest); `PROJECT.md` is read in full once per session under a whole-file budget of 20 KB / 250 lines; `project-memory/` is read on demand via the Map. The thin CLAUDE.md auto-loads and reminds the agent to read PROJECT.md first. The PROJECT.md hooks (lint on write, edit gate, Stop gate, PreCompact gate - see live-document SKILL.md, Gates) make the maintenance mandatory. The standing test: a fresh agent reading PROJECT.md, and on demand the project-memory files its Map names, can continue the project correctly, with nothing re-explained.

---

## Template body (copy and adapt)

```markdown
# PROJECT.md - <project name>

> Single source of truth for this project, read in full once per session. A fresh agent reading
> this file, and on demand the `project-memory/` files its Map names, should be able to continue
> correctly with nothing re-explained. Built and maintained under `/e2e` (track: <build|deliverable>).
> `project-memory/execution-plan.md` tracks execution state while the run is active; this file and
> the other project-memory files hold everything durable. Do not duplicate one into the other.

<!-- MAINTENANCE CONTRACT - read before editing this file. Enforced by hooks (project-md-lint).
Three layers by read frequency: CLAUDE.md (every message, thinnest); this file (once per session,
in full, max 20 KB / 250 lines): Goal, Scope, Map, Current state, Decisions locked (rule + who/when,
max 2 lines each), Plan, Open questions, Lessons (key rules, max 3 lines each); project-memory/
(on demand via the Map, one file per topic, every file has a Map row): decisions.md (full wording),
lessons.md (stories, max 8 lines each), changelog.md (every milestone, one entry per date, max 3
lines, no total cap), research-notes.md and execution-plan.md (e2e-owned while the run is active;
execution-plan.md deleted at Phase 12), plus topic files. No change log, research notes, or
execution plan here. Home rule: a fact lives in ONE home (decision wording / lesson story /
milestone in project-memory; skill rule body in the skill's references; run analysis in the run
file; owner preference in memory); elsewhere one line + a pointer. A line leaves this file only
when its home is named and exists. Write order: project-memory home first, this file last. The Map
names every folder and file that matters and must stay current. Update = reconcile, not append. -->

## Goal and definition of done
<The outcome that counts as success, and how we will measure it. Pull from the Elon "Question
requirements" step and the discovery outcomes distilled here in Phases 1-2.>

## Scope and non-goals
- In scope: <what the requirements that survived Elon actually cover>
- Out of scope / non-goals: <what was explicitly cut (CEO Review "NOT in scope" + Elon "Delete"), one-line rationale each>

## Map - where to find what
<!-- Row 1 = this file (what is ALWAYS here). Then one row per project-memory/ file. Every path must exist; every top-level folder appears. -->
| Location | What lives there | Read it when |
|---|---|---|
| `PROJECT.md` | goals, this map, current state + next action, decisions index, key-lesson rules, open questions | every session, in full |
| `project-memory/decisions.md` | the full wording and rationale of every locked decision, incl. declined review findings | before changing or superseding a decision |
| `project-memory/lessons.md` | every lesson story, grouped by theme | when a rule feels wrong, before changing how we work |
| `project-memory/changelog.md` | every milestone (phase boundaries), newest first | when the history of a change matters |
| `project-memory/research-notes.md` | Phase 4 findings with citations (e2e-owned) | planning, or asking "why X over Y?" |
| `project-memory/execution-plan.md` | the master phase/step status table + per-step detail (e2e-owned; deleted at Phase 12) | every phase and step of the run |
| `<folder or file>` | <what lives there> | <when to read it> |

## Current state and next action
<!-- Rewrite in place; must describe only NOW. -->
<What exists today, and the single next action. During Phase 6 this tracks the step in flight; at
Phase 12 it reads "complete" or names the next milestone.>

## Decisions locked
<!-- Rule + who/when, max 2 lines each; full wording in project-memory/decisions.md under the same title. A changed decision REPLACES the old one in both places. -->
- **<Architecture / approach decision>** - <the rule in one line, citing a research finding or the Elon outcome> (<who>, <YYYY-MM-DD>).
- **<Build only: conventions>** - languages & versions; test framework (every step gets automated tests + manual verification); code style / linter; error-handling stance.
- **<Deliverable only: format & data decisions>** - output format, data sources of record, refresh cadence, chart/visual conventions, audience.
- **<Declined review finding (Phase 9)>** - <one terse line each, so future runs don't re-flag it; reasoning in decisions.md>.

## Plan / workstreams
<!-- Status markers updated in place: [ ] todo, [~] in progress, [x] done, [!] blocked.
Granular phase/step status lives in project-memory/execution-plan.md - keep this to the big picture. -->
- [ ] <workstream / milestone>

## Open questions
<!-- Live unknowns only, max 3 lines each; delete once answered. -->
- <question>

## Lessons
<!-- Key lessons as RULES (max 3 lines each) - only those that change how we work on this project. Every story lives in project-memory/lessons.md under the same title. -->
- **<Lesson title>** - <the rule> (<YYYY-MM-DD>). Story: `project-memory/lessons.md § <Lesson title>`.
```

The HTML comments are permanent fixtures of the generated file, NOT placeholders: they stay in
`PROJECT.md` forever so every future agent sees the contract at the moment of editing. Only the
`<…>` angle-bracket slots get replaced with real content at scaffold time.

## Section-by-section maintenance contract

| Section | Behavior |
|---|---|
| Goal and definition of done | Mostly stable; revise only if the goal genuinely changes. |
| Scope and non-goals | Edit in place as scope is clarified. |
| Map - where to find what | Edited in the same write as any file or folder added, moved, or archived, and whenever a project-memory file's content changes; one row per project-memory file; every path must exist; every top-level folder appears. |
| Current state and next action | Always rewritten in place to describe *now* (every Phase 6 step, every phase boundary). |
| Decisions locked | Supersede in place (a new decision replaces the one it supersedes, here AND in `project-memory/decisions.md`); rule + who/when, max 2 lines, same bold title in both. Architecture + (Build) conventions live here, not in CLAUDE.md. |
| Plan / workstreams | High-level only; update status markers in place. Granular steps are the execution plan's job. |
| Open questions | Add/remove in place as questions arise and resolve; max 3 lines each. |
| Lessons | Rules only, max 3 lines each; the story lives in `project-memory/lessons.md`, the memory file is a pointer. Never lose a lesson. |
| project-memory/changelog.md | Newest first, milestones only (phase boundaries), one entry per date, 1-3 lines each; no total cap. |
| project-memory/research-notes.md (e2e-owned) | Findings + citations; a finding that hardens into a decision moves to Decisions locked + decisions.md; compacted at Phase 12. |
| project-memory/execution-plan.md (e2e-owned) | Status table + detail blocks updated at every phase/step boundary; deleted (with its Map row) at Phase 12 after folding its outcome into changelog.md / Current state. |

## Maintenance: keep it relevant, not just append

**Every update to PROJECT.md is also a cleanup, and the setup has three layers.** `CLAUDE.md` is read every message (thinnest). `PROJECT.md` is read in full once per session (whole-file budget 20 KB / 250 lines) and holds the map, the state and the rule lines. `project-memory/` holds every detail, one file per topic, read on demand via the Map. More context beats no context, but bloat loses to optimal context: reconcile before you add, and apply the home rule - a fact lives in ONE home (decision wording, lesson story and milestone in project-memory; skill rule body in the owning skill's references; run analysis in the run file; owner preference in memory) and appears elsewhere as one line plus a pointer. A line may leave this file only when its home is named and exists. Write the project-memory home first and this file last. The hooks (`project-md-lint`, the edit gate, the Stop gate, the PreCompact gate) enforce all of this.

Run this checklist on every update:
- **Supersede in place** - a changed decision overwrites the old one in both files (note the change in `project-memory/changelog.md`); never stack the old and new versions side by side.
- **Resolve and remove** - an answered Open question is deleted and folded into a decision or Current state; Open questions holds only live unknowns.
- **Live sections describe only now** - rewrite Current state and next action and Plan / workstreams in place; nothing historical lingers there.
- **One fact, one home** - a fact lives in exactly one file and section; don't restate a decision in Current state and the changelog too.
- **Change log = milestones, not a diary** - lives in `project-memory/changelog.md`; an entry is 1-3 lines (what shipped + commit + outcome), one per date; verification narratives and review blow-by-blow never belong in it.
- **Home rule** - one home per fact; pointers everywhere else; never delete a line whose home does not exist yet; home first, this file last.
- **Map current** - any file or folder added, moved, or archived gets its Map row in the same edit; every project-memory file has a row with a summary and a "read it when"; every path in the Map exists.
- **No invented sections** - use only the canonical headers above, with no suffix; a new subject becomes a `project-memory/<topic>.md` with a Map row, never a "Reference"/"Summary"/"Notes"/"Change log" section here.
- **Move, don't lose** - never drop a real decision or lesson; compact or relocate, but keep the signal.

## Notes for the writer (Phase 5 and every later phase)

- **Fill from discovery, not imagination.** Goal/Scope/Decisions were distilled here by Phases 1-3 as they ran; Phase 5 deepens them with the research findings. Nothing gets invented at Phase 5 - it synthesizes what the earlier phases already put in the living docs.
- **This is the home for durable rule lines; project-memory is the home for their detail.** The thin CLAUDE.md deliberately does NOT hold architecture decisions or conventions - they live here (rule) and in `decisions.md` (wording) so CLAUDE.md stays ~one screen.
- **Maintain it unprompted.** Phases 6-12 each update the living docs (Current state, changelog.md, Decisions, lessons.md, execution-plan.md). The `<!-- live-document:start -->` block in CLAUDE.md is what reminds future sessions to keep doing so after the e2e run ends.
- **One source of truth.** Never a tracking file outside `project-memory/`. PROJECT.md is the map and the rule index; `project-memory/execution-plan.md` carries execution state; CLAUDE.md is a thin bootstrap, not a tracker. (Legacy runs keep their separate PLAN.md for life.)
