# `project-memory-template.md` - the detail layer (read on demand)

`project-memory/` is the folder next to `PROJECT.md` that holds every detail a rule line cannot
carry: the full wording of decisions, the lesson stories, the milestone history, and any topic that
deserves its own file (a runbook, an architecture note, an ID registry, carried-over items). It is
read ON DEMAND: an agent opens a file only when its Map row in `PROJECT.md` says the task touches
it, and always before editing it. Nothing is lost in silence (every fact has a home) and nothing
bloats the once-per-session read (`PROJECT.md` stays under 20 KB).

## Rules for every file in the folder

- **One file per topic**, lowercase kebab-case name, `.md`. The three standard files exist in every
  project: `decisions.md`, `lessons.md`, `changelog.md`. e2e projects add `research-notes.md` and
  `execution-plan.md`. Add a topic file when a subject has more than a rule line of detail.
- **Standard header**, first lines of every file (the lint warns without it):
  ```markdown
  # <Topic> - <what this file is>

  > Home of <topic> for <project>. `PROJECT.md`'s Map points here; it keeps <the index line / the
  > rule line / nothing> for each entry. <One-line maintenance rule for this file.>
  ```
- **A Map row in `PROJECT.md`** for every file: `` `project-memory/<file>` | <one-line summary of
  what lives there> | <read it when> `` - the lint fails without it, and the summary is what a
  future agent decides from, so keep it current whenever the file's content changes.
- **Size**: split a file by topic when it passes 40 KB (the lint warns). Group with `##` headings
  inside a file; the `file.md § Heading` pointer form resolves to those headings.
- **Write order**: edit the project-memory file FIRST, then `PROJECT.md` (its Map row / index
  line) LAST. The Stop gate requires `PROJECT.md` to be the newest project write; this order
  passes on the first try and the pointer never precedes its target.
- **Reconcile, never append**: a superseded decision is replaced, not stacked; a lesson is one
  story under one title; history belongs in `changelog.md` only.

## The three standard files

### `decisions.md`

```markdown
# Decisions locked - full wording

> Home of every locked decision's full wording and rationale for <project>. `PROJECT.md`
> `## Decisions locked` keeps one rule line per decision (same bold title, max 2 lines) and points
> here. A new decision that supersedes an old one REPLACES it in both files; note the change once
> in `changelog.md`.

## <Decision title>
- **Rule:** <the rule, as in PROJECT.md>. (<who>, <YYYY-MM-DD>)
- **Why:** <the reasoning, the alternatives rejected, the evidence>.
- **Mechanism / where it lives:** <the file, hook, script, or process that implements it>.
```

One `##` heading per decision, same title as the bold lead in `PROJECT.md`, so the pointer
`` `project-memory/decisions.md § <Decision title>` `` resolves. The lint warns when the number of
decisions here differs from the number of rule lines in `PROJECT.md`.

### `lessons.md`

```markdown
# Lessons - the full stories

> Home of every lesson story for <project>, grouped by theme. `PROJECT.md` `## Lessons` keeps only
> the rules that change how we work here (max 3 lines each) and points here. One bullet per
> lesson, max 8 lines: what was tried, what failed, the lesson, the date. Never lose a lesson.

## <Theme>

### <Lesson title>
- <What was tried -> what happened -> the lesson>. (<YYYY-MM-DD>)
```

A `###` heading per lesson (same title as the rule line in `PROJECT.md` when one exists), grouped
under `##` themes. The lint fails a story over 8 lines.

### `changelog.md`

```markdown
# Change log - every milestone

> Home of the milestone history for <project>, newest first, one entry per date, 1-3 lines each
> (what shipped, the commit, the outcome). `PROJECT.md` holds no history; `## Current state and
> next action` describes only now. No total cap and no ageing rule: this file is the full record.

- <YYYY-MM-DD>: <what shipped> (<commit>); <outcome>.
```

The lint fails an entry over 3 lines or two entries on one date; verification narratives and
review blow-by-blow never belong here.

## Migration from the single-file layout (one-time, in a dedicated session)

A project whose root has no `project-memory/` folder, or whose `PROJECT.md` contract comment lacks
the phrase "project-memory", is on the pre-2026-09-09 layout (one file, two tiers). Migrate it in a
dedicated session, never mid-task (the hooks keep the format rules in legacy grace until the file
lints clean once):

1. Read `PROJECT.md` in full. Create `project-memory/` (if the project used a `playbook/` folder
   for the same purpose, rename it with `git mv`, fix the Map paths and any skill reference that
   named it).
2. **Decisions:** for each bullet in `## Decisions locked`, write a `## <title>` block in
   `decisions.md` with the full wording; leave in `PROJECT.md` a rule line (bold title + rule +
   who/when, max 2 lines). Same title in both places.
3. **Lessons:** move every story to `lessons.md` under a theme, one `###` per lesson (max 8 lines
   each). Keep in `PROJECT.md` only the lessons that change how we work here, as rules (max 3
   lines) with a `Story:` pointer. Update memory pointer files ("Full story: ...") to the new
   path.
4. **Change log:** move the whole `## Change log` section to `changelog.md` as is (older entries
   may stay at their current length; there is no ageing rule there). Delete the section from
   `PROJECT.md`.
5. **e2e sections:** move `## Research notes` to `research-notes.md` and `## Execution plan` to
   `execution-plan.md` (only between phases on an active run), delete the sections.
6. **Other long content** (a narrative in Current state, a stakeholder table, a runbook): give it
   a topic file and leave one line + a pointer.
7. **Map:** add one row per project-memory file with a one-line summary and a "read it when".
8. **Contract:** replace the title blockquote and the `MAINTENANCE CONTRACT` comment with the ones
   in `project-md-template.md`; replace the per-section comments that changed (Decisions locked,
   Open questions, Lessons).
9. **CLAUDE.md block:** replace items 1-4 of the `<!-- live-document:start -->` block with the
   current ones from `claude-md-block.md`; keep every other line and the markers.
10. Run `node ~/.claude/hooks/project-md-lint.js PROJECT.md` until clean (the first clean run
    arms the format gates for this project). Record the migration as one `changelog.md` entry.
