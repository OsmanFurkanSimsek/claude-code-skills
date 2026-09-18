# `project-md-template.md` - the living source of truth (the once-per-session layer)

Create `PROJECT.md` from this skeleton, filled from the interview. If a `PROJECT.md` already
exists, augment it: add any missing sections and merge content in, without deleting existing
material. `PROJECT.md` is read IN FULL once per session (the SessionStart hook tells the agent its
size and to Read it; the edit gate enforces it), so it holds the important things - the Map,
current state, the decisions and key lessons as rule lines, open questions - under a whole-file
budget of 20 KB / 250 lines. Everything with more detail than a rule line lives in
`project-memory/` (see `project-memory-template.md`) and is read on demand via the Map. Maintain
both in place every session - add AND prune - under the hooks described in SKILL.md (Gates).

```markdown
# PROJECT.md - <project name>

> Single source of truth for this project, read in full once per session. A fresh agent reading
> this file, and on demand the `project-memory/` files its Map names, should be able to continue
> correctly with nothing re-explained. Maintained every session under the home rule: one home per
> fact, pointers everywhere else.

<!-- MAINTENANCE CONTRACT - read before editing this file. Enforced by hooks (project-md-lint).
Three layers by read frequency: CLAUDE.md (every message, thinnest, max 8 KB / 100 lines); this file (once per session,
in full, max 20 KB / 250 lines): Goal, Scope, Map, Current state, Decisions locked (rule + one-line why + who/when,
max 3 lines each), Plan, Open questions, Lessons (key rules, max 3 lines each); project-memory/
(on demand via the Map, one file per topic, every file has a Map row): decisions.md (full wording),
lessons.md (stories, max 8 lines each), changelog.md (every milestone, one entry per date, max 3
lines, no total cap), plus topic files. No change log, research notes, or execution plan here.
Home rule: a fact lives in ONE home (decision wording / lesson story / milestone in project-memory;
skill rule body in the skill's references; run analysis in the run file; owner preference in
memory); elsewhere one line + a pointer. A line leaves this file only when its home is named and
exists. Write order: project-memory home first, this file last. The Map names every folder and
file that matters and must stay current. Update = reconcile, not append. -->

## Goal and definition of done
<The outcome that counts as success, and how we will measure it.>

## Scope and non-goals
- In scope: <…>
- Out of scope / non-goals: <…>

## Map - where to find what
<!-- Row 1 = this file (what is ALWAYS here). Then one row per project-memory/ file. Every path must exist; every top-level folder appears. -->
| Location | What lives there | Read it when |
|---|---|---|
| `PROJECT.md` | goals, this map, current state + next action, decisions index, key-lesson rules, open questions | every session, in full |
| `project-memory/decisions.md` | the full wording and rationale of every locked decision | before changing or superseding a decision |
| `project-memory/lessons.md` | every lesson story, grouped by theme | when a rule feels wrong, before changing how we work |
| `project-memory/changelog.md` | every milestone since the start, newest first | when the history of a change matters |
| `<folder or file>` | <what lives there> | <when to read it> |

## Current state and next action
<!-- Rewrite in place; must describe only NOW. -->
<What exists today, and the single next action.>

## Decisions locked
<!-- Rule + one-line why + who/when, max 3 lines each; full wording in project-memory/decisions.md under the same title. Nothing is lost by the split: the lint fails a pointer whose heading is gone. A changed decision REPLACES the old one in both places. -->
- **<Decision title>** - <the rule in one line> (<who>, <YYYY-MM-DD>).

## Plan / workstreams
<!-- Status markers updated in place: [ ] todo, [~] in progress, [x] done, [!] blocked. -->
- [ ] <workstream / milestone>

## Open questions
<!-- Live unknowns only, max 3 lines each; delete once answered. -->
- <question>

## Lessons
<!-- Key lessons as RULES with a one-line why (max 3 lines each) - only those that change how we work on this project. Every story lives in project-memory/lessons.md under the same title; nothing is lost by the split, the lint fails a pointer whose heading is gone. -->
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
| Map - where to find what | Edited in the same write as any file or folder added, moved, or archived, and whenever a project-memory file's content changes; one row per project-memory file with a one-line summary and a "read it when"; every path must exist; every top-level folder appears. |
| Current state and next action | Always rewritten in place to describe *now*. |
| Decisions locked | Supersede in place (a new decision replaces the one it supersedes, here AND in `project-memory/decisions.md`); rule + one-line why + who/when, max 3 lines; the same bold title in both files; never delete a still-valid decision. |
| Plan / workstreams | Update status markers in place. |
| Open questions | Add/remove in place as questions arise and resolve; max 3 lines each. |
| Lessons | Rules only, max 3 lines each, only lessons that change how we work here; the story lives in `project-memory/lessons.md` under the same title, the memory file is a pointer. Never lose a lesson. |

## Maintenance: keep it relevant, not just append

A compact version of this contract is embedded in the generated file itself (the MAINTENANCE
CONTRACT comment and the per-section comments), so the rules are in front of every future agent at
edit time, not just in this reference. Keep those comments intact when curating.

**Every update to PROJECT.md is also a cleanup, and the setup has three layers.** `CLAUDE.md` is
read every message (thinnest). `PROJECT.md` is read in full once per session (whole-file budget
20 KB / 250 lines) and holds the map, the state and the rule lines. `project-memory/` holds every
detail, one file per topic, read on demand via the Map. More context beats no context, but bloat
loses to optimal context: reconcile before you add, and apply the home rule - a fact lives in ONE
home (decision wording, lesson story and milestone in project-memory; skill rule body in the
skill's references; run analysis in the run file; owner preference in memory) and appears
elsewhere as one line plus a pointer. A line may leave this file only when its home is named and
exists. Write the project-memory home first and this file last. The hooks (`project-md-lint`, the
edit gate, the Stop gate, the PreCompact gate) enforce all of this.

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
