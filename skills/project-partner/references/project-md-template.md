# PROJECT.md Template

Create `PROJECT.md` from this skeleton, filled from the interview. If a PROJECT.md already exists, augment it: add any missing sections and merge content in, without deleting existing material. Read on demand (not auto-loaded). Maintain it in place every session - add AND prune.

---

```markdown
# PROJECT.md - <project name>
> Single source of truth for this project. A fresh agent reading only this file should be able to
> continue correctly, with nothing re-explained. Maintained every session: live sections edited in
> place; Change log holds milestones only (1-3 lines each, tail compacted as entries age); Lessons
> appended deduped; obsolete detail compacted.

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
<!-- Mostly stable; revise only if the goal genuinely changes. -->
<The outcome that counts as success, and how we will measure it.>

## Scope and non-goals
<!-- Edit in place as scope is clarified. -->
- In scope: <...>
- Out of scope / non-goals: <...>

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
PROJECT.md forever so every future agent - including one in a completely fresh session or a
different environment with no memory of this skill - sees the contract at the moment of editing,
not just when the skill itself happens to be loaded. Only the `<...>` angle-bracket slots get
replaced with real content at scaffold time.

For e2e-managed projects, PROJECT.md also carries e2e's own `## Research notes` and
`## Execution plan` sections (see Coexistence rules in SKILL.md). Treat those as canonical while
e2e's flow is active; do not fold their content into the sections above or invent a duplicate.

---

## Section-by-section maintenance contract

| Section | Behavior |
|---|---|
| Goal and definition of done | Mostly stable; revise only if the goal genuinely changes. |
| Scope and non-goals | Edit in place as scope is clarified. |
| Current state and next action | Always rewritten in place to describe now. |
| Decisions locked | A changed decision replaces the one it supersedes in place; never delete a decision outright (move/compact only). |
| Plan / workstreams | Update status markers in place. |
| Open questions | Add/remove in place as questions arise and resolve. |
| Change log | Milestones only, newest first, 1-3 lines each; compact the tail as entries age. |
| Lessons | Append, deduped; compact but never lose a lesson. |

---

## The update algorithm (run it on every write to PROJECT.md)

1. Read PROJECT.md in full before acting.
2. Classify each new fact the work produced: durable choice, lesson, state change, resolved question, or milestone. A fact has exactly ONE home section.
3. Rewrite the home section in place, superseding old content. Current state and next action is rewritten every time so it describes only NOW. A new durable choice REPLACES the decision it supersedes in Decisions locked (never stack old and new side by side). An answered Open question is deleted, its answer folded into a decision or Current state. Feedback and failures go to Lessons (deduped: what was tried, what failed, the lesson). Only a milestone earns a Change log entry (newest first), and an entry is 1-3 lines: what shipped, the commit, the outcome. Verification narratives, review blow-by-blow, and mechanism detail never go in the log (they live in Decisions/Lessons). When adding an entry, compact any older entry still over 3 lines - the log's tail decays to ~1 line per milestone. Most updates add no entry.
4. Sweep the whole file before saving. Delete or merge everything now redundant, resolved, stale, or duplicated, anywhere in the file - not just the sections you touched. Deleting a line that no longer earns its place is REQUIRED maintenance, not data loss (real decisions and lessons are compacted or moved, never dropped). No invented sections: use only this skill's canonical headers - plus, on e2e-managed projects, e2e's own `## Research notes` and `## Execution plan` sections - never add a "Reference"/"Summary"/"Notes" section that duplicates others.

**Red-flag test before saving:** an update that only adds lines and rewrites nothing is almost always wrong. If your diff is append-only, you skipped steps 2-4 - go back and sweep. Quantitative tripwires: the Change log tops ~30 lines, any log entry runs past 3 lines, or the file grew even though the work resolved or superseded something - each means compaction is overdue and must happen in THIS edit, not be deferred.

---

## Curation checklist (run on every update)

- **Supersede in place** - a changed decision overwrites the old one (note in Change log); never stack old and new versions side by side.
- **Resolve and remove** - an answered Open question is deleted and folded into a decision or Current state; Open questions holds only live unknowns.
- **Live sections describe only now** - rewrite Current state and Plan / workstreams in place; nothing historical lingers there.
- **One fact, one home** - a fact lives in exactly one section; do not restate a decision in both Current state and Change log.
- **Change log = milestones, not a diary** - an entry is 1-3 lines (what shipped + commit + outcome); verification narratives and review blow-by-blow never belong in it. Collapse old granular entries once their durable content is captured in Decisions locked / Lessons - the log's tail should decay to ~1 line per milestone.
- **No invented sections** - use only the canonical headers above; never add a "Reference" / "Summary" / "Notes" section that duplicates others.
- **Move, don't lose** - never drop a real decision or lesson; compact or relocate, but keep the signal.
- **Red-flag test** - an append-only diff (nothing rewritten or deleted) is almost always an incomplete update.

The standing test: a fresh agent reading only PROJECT.md can continue correctly without the user re-explaining anything.
