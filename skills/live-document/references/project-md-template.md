# `project-md-template.md` - the living source of truth

Create `PROJECT.md` from this skeleton, filled from the interview. If a `PROJECT.md` already
exists, augment it: add any missing sections and merge content in, without deleting existing
material. Read on demand (not auto-loaded). Maintain it in place every session - add AND prune.

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
<The outcome that counts as success, and how we will measure it.>

## Scope and non-goals
- In scope: <…>
- Out of scope / non-goals: <…>

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
| Current state and next action | Always rewritten in place to describe *now*. |
| Decisions locked | Append durable choices; never delete (move/compact only). |
| Plan / workstreams | Update status markers in place. |
| Open questions | Add/remove in place as questions arise and resolve. |
| Change log | Append-only, newest first, milestones only, 1-3 lines each; compact the tail as entries age. |
| Lessons | Append, deduped; compact but never lose a lesson. |

## Maintenance: keep it relevant, not just append

A compact version of this contract is embedded in the generated file itself (the MAINTENANCE
CONTRACT comment and the per-section comments), so the rules are in front of every future agent at
edit time, not just in this reference. Keep those comments intact when curating.

**Every update to PROJECT.md is also a cleanup.** This file is re-read in full at the start of every session/phase, so every line that is redundant, stale, resolved, or duplicated is paid for again and again. It may grow **only** when there is genuinely more essential information to hold, never from accumulation. Before you add, reconcile: as facts change, update them in place and drop what they replace; as questions resolve, remove them. Duplication and staleness are bugs. There is **no size limit** - a big project may legitimately need a big file - the only test is whether every line still earns its place.

Run this checklist on every update:
- **Supersede in place** - a changed decision overwrites the old one (note the change in Change log); never stack the old and new versions side by side.
- **Resolve and remove** - an answered Open question is deleted and folded into a decision or Current state; Open questions holds only live unknowns.
- **Live sections describe only now** - rewrite Current state and next action and Plan / workstreams in place; nothing historical lingers there.
- **One fact, one home** - a fact lives in exactly one section; don't restate a decision in Current state and Change log too.
- **Change log = milestones, not a diary** - an entry is 1-3 lines (what shipped + commit + outcome); verification narratives and review blow-by-blow never belong in it. Collapse old granular entries once their durable content is captured in Decisions locked / Lessons - the log's tail should decay to ~1 line per milestone.
- **No invented sections** - use only the canonical headers above; never add a "Reference"/"Summary"/"Notes" section that duplicates others.
- **Move, don't lose** - never drop a real decision or lesson; compact or relocate, but keep the signal.
