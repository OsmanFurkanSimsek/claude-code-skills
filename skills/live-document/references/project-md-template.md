# `project-md-template.md` - the living source of truth

Create `PROJECT.md` from this skeleton, filled from the interview. If a `PROJECT.md` already
exists, augment it: add any missing sections and merge content in, without deleting existing
material. Tier 1 (header, Goal, Scope, Map, Current state, Open questions, Decisions) is injected
every session by the SessionStart hook; Tier 2 is read on demand. Maintain it in place every
session - add AND prune - under the hooks described in SKILL.md (Gates).

```markdown
# PROJECT.md - <project name>

> Single source of truth for this project. A fresh agent reading only this file should be able to
> continue correctly, with nothing re-explained. Two tiers: Tier 1 (through Decisions locked) is
> injected every session; Tier 2 (Plan, Change log, Lessons, Research notes) is read on demand.
> Maintained every session under the home rule: one home per fact, pointers everywhere else.

<!-- MAINTENANCE CONTRACT - read before editing this file. Enforced by hooks (project-md-lint).
Tier 1 (injected every session, max 14 KB / 180 lines): header, Goal, Scope, Map, Current state,
Open questions, Decisions locked (rule + who/when + pointer, max 4 lines each).
Tier 2 (read on demand, may grow): Plan, Change log (one entry per date, max 3 lines, older than
14 days -> 1 line, max 30 lines), Lessons (full story, max 8 lines each), Research notes.
Home rule: a fact lives in ONE home (lesson story here; rule body in the skill reference; run
analysis in the run file; owner preference in memory); elsewhere one line + a pointer. A line
leaves this file only when its home is named and exists. The Map names every folder and file
that matters and must stay current. Update = reconcile, not append. -->

## Goal and definition of done
<The outcome that counts as success, and how we will measure it.>

## Scope and non-goals
- In scope: <…>
- Out of scope / non-goals: <…>

## Map - where to find what
<!-- Row 1 = this file (what is ALWAYS here). Every path must exist; every top-level folder appears. -->
| Location | What lives there | Read it when |
|---|---|---|
| `PROJECT.md` | goals, this map, current state + next action, open questions, decisions index, lessons, milestones | every session (Tier 1 auto-injected) |
| `<folder or file>` | <what lives there> | <when to read it> |

## Current state and next action
<!-- Rewrite in place; must describe only NOW. -->
<What exists today, and the single next action.>

## Decisions locked
<!-- A changed decision REPLACES the old one; note the change once in Change log. -->
- <decision> - <one-line rationale>

## Plan / workstreams
<!-- Status markers updated in place: [ ] todo, [~] in progress, [x] done, [!] blocked. -->
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
| Current state and next action | Always rewritten in place to describe *now*. |
| Decisions locked | Supersede in place (a new decision replaces the one it supersedes); rule + who/when + pointer, max 4 lines; never delete a still-valid decision. |
| Plan / workstreams | Update status markers in place. |
| Open questions | Add/remove in place as questions arise and resolve. |
| Change log | Newest first, milestones only, one entry per date, 1-3 lines each; entries older than 14 days shrink to one line; max 30 lines. |
| Lessons | Full story, max 8 lines each, deduped against Decisions; the memory file is a pointer. Never lose a lesson. |

## Maintenance: keep it relevant, not just append

A compact version of this contract is embedded in the generated file itself (the MAINTENANCE
CONTRACT comment and the per-section comments), so the rules are in front of every future agent at
edit time, not just in this reference. Keep those comments intact when curating.

**Every update to PROJECT.md is also a cleanup, and the file has two tiers.** Tier 1 (header, Goal, Scope, Map, Current state, Open questions, Decisions locked) is injected every session by the SessionStart hook under a hard 14 KB / 180-line budget; Tier 2 (Plan, Change log, Lessons, Research notes) is read on demand and may grow within per-entry limits. More context beats no context, but bloat loses to optimal context: reconcile before you add, and apply the home rule - a fact lives in ONE home (lesson story here, rule body in the owning skill's references, run analysis in the run file, owner preference in memory) and appears elsewhere as one line plus a pointer. A line may leave this file only when its home is named and exists. The hooks (`project-md-lint`, the Stop gate, the PreCompact gate) enforce all of this.

Run this checklist on every update:
- **Supersede in place** - a changed decision overwrites the old one (note the change in Change log); never stack the old and new versions side by side.
- **Resolve and remove** - an answered Open question is deleted and folded into a decision or Current state; Open questions holds only live unknowns.
- **Live sections describe only now** - rewrite Current state and next action and Plan / workstreams in place; nothing historical lingers there.
- **One fact, one home** - a fact lives in exactly one section; don't restate a decision in Current state and Change log too.
- **Change log = milestones, not a diary** - an entry is 1-3 lines (what shipped + commit + outcome); verification narratives and review blow-by-blow never belong in it. Collapse old granular entries once their durable content is captured in Decisions locked / Lessons - the log's tail should decay to ~1 line per milestone.
- **Home rule** - one home per fact; pointers everywhere else; never delete a line whose home does not exist yet.
- **Map current** - any file or folder added, moved, or archived gets its Map row in the same edit; every path in the Map exists.
- **No invented sections** - use only the canonical headers above (including Map - where to find what), with no suffix; never add a "Reference"/"Summary"/"Notes" section that duplicates others.
- **Move, don't lose** - never drop a real decision or lesson; compact or relocate, but keep the signal.
