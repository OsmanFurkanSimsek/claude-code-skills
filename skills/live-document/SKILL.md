---
name: live-document
description: Use when the user types /live-document, wants project state to survive across sessions ("keep track of this project", "I keep losing context between sessions", "set up project memory / a living doc", "remember where we left off"), or when starting a substantial project spanning multiple sessions. Also use on projects whose CLAUDE.md contains a <!-- live-document:start --> marker, or when a project's CLAUDE.md has grown past a thin bootstrap (every-message context bloat, "CLAUDE.md is too long"). Do NOT use for one-off edits, bug fixes, debugging, quick lookups, or when an active e2e/gsd build flow already governs the project's files.
argument-hint: "[optional: one-line project description]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
---

# /live-document

## Purpose

Stand up a **self-sustaining living project document** so that project state is never lost
between sessions, and a fresh agent (or a future you) can pick up the project without anyone
re-explaining anything. The skill does the *setup*: it interviews you until it genuinely
understands the project, then scaffolds three layers in the project root, each sized for how
often it is read:

- **`CLAUDE.md`** - loaded on EVERY message, so the THINNEST layer: budget **8 KB / 100 lines**
  (hook-checked), never grows. It holds only what every message needs: the bootstrap that reminds
  the agent to read and maintain the real source of truth, plus per-message hard rules.
- **`PROJECT.md`** - read ONCE per session, in full, before acting (until the context is cleared),
  so RICH with the important things: where to look for what (the Map), current state and next
  action, the decisions that shaped the project (rule lines), the key lessons (rule lines), open
  questions. Whole-file budget 20 KB / 250 lines.
- **`project-memory/`** - every other detail, one file per topic, read ON DEMAND: the full wording
  of every decision (`decisions.md`), every lesson story (`lessons.md`), every milestone
  (`changelog.md`), plus free topic files (a runbook, an architecture note, a registry). Every file
  has a Map row in `PROJECT.md` with a one-line summary and a "read it when", so nothing is lost
  in silence and the agent reads only what the task needs.

Because `CLAUDE.md` auto-loads, maintenance becomes **self-sustaining**: every future session is
reminded to read `PROJECT.md` first and to record what changed. After this one-time setup you
should never again have to tell an agent to read, update, or maintain these files, and the
PROJECT.md gates (hooks - see *Gates* below) make the maintenance mandatory, not advisory. The acceptance
test for the whole system: *a fresh agent reading `PROJECT.md` and, on demand, the
`project-memory/` files its Map names can continue the project correctly, with nothing re-explained.*

## When to use

- The user invokes `/live-document`.
- The user wants to stop losing track of a project across sessions - "keep track of this", "set up
  project memory / running notes / a project journal", "remember where we left off", "so the next
  session can continue".
- A substantial new project or initiative is starting that will clearly span multiple sessions and
  is worth keeping a durable record of.

## When NOT to use

- One-off edits, single-file changes, bug fixes, debugging, or quick lookups - these don't need a
  living doc.
- When an **e2e** or **gsd** build flow is already actively governing the project. Those flows own
  their own files (`PLAN.md`, `.planning/`, their own `CLAUDE.md` state marker). If the user is
  mid-flow there, don't hijack it. (You may still *coexist* - see Coexistence rules below - but
  prefer to let the active flow lead.)

## Operating style (apply throughout, every session)

You are the user's project partner, not a cheerleader. Hold this stance the whole way through:

- Be a critical, skeptical thought partner. Not every idea is good. Challenge ideas with evidence
  and strong arguments. Tell it like it is; do not sugar-coat; correct the user when they are wrong
  and say why.
- Ask before assuming. A clarifying question always beats a wrong assumption.
- Code-first for any coding or calculation task: show the code or the steps, then the result, then
  a short summary. Show non-trivial math step by step. Add a quick sanity check when relevant.
- Be concise, precise, analytical. No fluff, no flattery. **Never use the long-dash character.**
- For time-sensitive or high-stakes claims, check current authoritative sources and cite them.

## Communication format (always on)

Pick the mode with one test: does the user need to DO something themselves?

**Answer mode** - the user asked a question and has nothing to do:
- Start with a TLDR: the direct answer in 1-3 plain sentences.
- Then the detail: reasoning, evidence, alternatives, trade-offs.
- No steps section. Never add steps when the user has nothing to do.

**Action mode** - the user must do something themselves (click, type, run, configure, decide). Deliver exactly three parts, in this order, every time:

1. **Summary** - what we are doing, 1-2 sentences, plain words.
2. **Reasoning** - why we are doing it, plain words.
3. **Steps** - numbered and concrete, in super simple language. One action per step: where to click, what to type, what to run, and what the user should see if it worked. Write as if the user is seeing the screen for the first time. A high-level instruction like "configure the connector" is a bug; spell out every click.

**Decision mode** - the user must make an open decision: several viable paths, where his
preferences, risk tolerance or context decide the outcome, not a question with one correct answer.
If a user-level rule in `~/.claude/rules/` defines a structure for open decisions, that rule owns
the reply shape and replaces Answer mode and Action mode for that reply. Otherwise use Action mode
with the options and their trade-offs laid out in full before the steps.

**Chunking rule** - for Action-mode work with more than about 10 steps, or any multi-part plan:

- Never dump the full step list. Split the work into chunks of roughly 5-10 steps and deliver ONE chunk per turn.
- End every chunk by asking the user to confirm when the chunk is done, or to report what failed. Do not send the next chunk before that confirmation.
- Before delivering the next chunk, update PROJECT.md first: the full chunk list with status markers lives in Plan / workstreams, the active chunk is named in Current state and next action, and failures go to Lessons.
- After each PROJECT.md update, tell the user explicitly: everything is documented in PROJECT.md, so you can clear the context whenever you want and a fresh session will continue from the next chunk.

**Next Actions file** - a real handoff (about 3+ steps the user must do themselves, or ANY chunk of the chunking rule) also gets a durable copy the user can open outside the chat. Write an interactive, self-contained `next-actions/<YYYY-MM-DD_HH-MM>-next-actions.html` at the project root, following `references/next-actions-template.md` exactly (TLDR paragraph first, then reasoning with the alternatives considered and why this path won, then the steps in the same super-simple language). Every handoff gets a NEW dated file. The folder root always shows only the most recent date's file(s) - not necessarily today, whatever date last got a file, until a newer one appears. Before writing the new file (and again at the start of any session touching this project), sweep every file whose date is not the newest into `next-actions/archive/` (create it if missing) automatically, with no reminder needed. Never delete a file, only move it - the archive is the full history. Announce the path in one chat line. Trivial asks (one command, one click) stay chat-only.

**Recap on request** - when the user asks where we are ("where are we", "remind me", "recap", "I lost the thread"), reply in Answer mode with a plain-English recap of 3-5 sentences: the request that started this session, what we are doing and why, what is already done, what comes next. Source it from PROJECT.md *Current state* plus the conversation; write no file, add no steps. If the previous reply was long, restate its substance shorter and simpler under the recap.

The standing test for this section: the user always knows what we are doing, why we are doing it, and exactly what to do next, a context clear at any chunk boundary loses nothing, and every real handoff leaves a dated Next Actions file behind.

## Mode detection (do this first, on every invocation)

Check the project root for a live-document setup:

1. Read the root `CLAUDE.md` (if any) and look for the marker `<!-- live-document:start -->`.
2. Also check whether a `PROJECT.md` exists with this skill's section headers (Goal and definition
   of done, Map - where to find what, Decisions locked, Lessons) and whether a `project-memory/`
   folder exists (a set-up project that lacks it is a legacy layout - see self-heal below).

- **No marker / no living `PROJECT.md`** → **Setup mode** (interview + scaffold).
- **Marker present** → **Curation mode** (the project is already set up; read and maintain).

## Setup mode

### Phase 1 - Understand the project first (HARD GATE: create nothing until confirmed)

Do not create files, propose a solution, or start the task until you understand the project.

**Adaptive depth.** First gather what already exists so you don't ask what you can read:
- Skim the repo: `README`, existing `CLAUDE.md`/`PROJECT.md`, package/config files, directory
  layout, and recent commits if it's a git repo.
- Use any context already in this conversation.

Then **draft your current understanding** and ask only the *gaps* - in small batches. On a truly
blank/new project this is the full interview; on an existing project it should be a short list of
genuine unknowns. Keep asking focused follow-ups until you have **zero open questions**. Do not
fill gaps with assumptions. Cover at least:

- **Goal and definition of done** - what outcome counts as success, and how we measure it.
- **Scope and non-goals** - what is explicitly in, and what is explicitly out.
- **Current state and history** - what exists today, what has been tried, what failed and why.
- **The dominant constraint** - the one bottleneck, limit, or risk that should govern every
  decision (cost, time, a fragile system, a data limit). Also budgets, deadlines, tools, environment.
- **Stakeholders and audience** - who it is for, who decides, who else touches it.
- **Risks and unknowns** - what could break it, what is still uncertain.
- **Decisions already made** - anything to treat as locked from the start.

When you believe you understand it, **summarize the project back in a few lines and ask the user to
confirm or correct it BEFORE scaffolding anything.**

### Phase 2 - Scaffold the three layers in the project root (only after confirmation)

**`CLAUDE.md` (thin bootstrap) - append, never overwrite.**
Use the block in `references/claude-md-block.md`, filled from the interview.
- If a `CLAUDE.md` already exists: **append** the block between its `<!-- live-document:start -->`
  and `<!-- live-document:end -->` markers, preserving every existing line above it.
- Then measure the file (`wc -c CLAUDE.md`). If it exceeds **8 KB / 100 lines**, or more than 3 KB
  sits outside the block, run the *CLAUDE.md routing test* (Curation mode) on the content above the
  block, show the move list, and ask ONE yes/no. Until the yes, every existing line stays; after it,
  each section moves to its home (deleted only where its home already holds it).
- If no `CLAUDE.md` exists: create one with a one-line header plus the block.
- It is a bootstrap, not a log - it must not grow.

**`PROJECT.md` (living source of truth) - create or augment.**
Use the template in `references/project-md-template.md`, filled from the interview.
- If no `PROJECT.md` exists: create it from the template.
- If a `PROJECT.md` already exists (e.g. from gsd): **augment** it - add any missing living
  sections and merge in the interview content without deleting existing material.

**`project-memory/` (the detail layer) - create with its three standard files.**
Use `references/project-memory-template.md`: `decisions.md` (full wording of every decision),
`lessons.md` (every story, grouped by theme), `changelog.md` (every milestone). Each starts with
the standard header (title + a blockquote naming `PROJECT.md` as the map that points here) and
gets a Map row in `PROJECT.md` with a one-line summary and a "read it when". Add a topic file
whenever a subject has more detail than a rule line can carry (a runbook, an architecture note,
an ID registry); never a tracking file OUTSIDE `project-memory/` (no `NOTES.md`, no second
PROJECT.md, no dated status files at the root).

**Memory is a home, not a mirror (home rule).** If a persistent memory facility is available
(e.g. `~/.claude/projects/<project-slug>/memory/`), add a one-line pointer to these files in its
index as a backup trigger, and from then on split by type: an owner preference about how to work
lives in memory in full; a project lesson's full story lives in `project-memory/lessons.md`, its
rule line (if it changes how we work on this project) in `PROJECT.md` `## Lessons`, and its memory
file is a pointer (frontmatter + Why/How-to-apply + "Full story: `project-memory/lessons.md §
<title>`"). Never two stories of one lesson.

After scaffolding, tell the user setup is done and that from now on these files maintain
themselves - they will not need to ask you to read or update them again.

## Curation mode

This is what every future session does (the `CLAUDE.md` auto-load reminds it), and what you do
when `/live-document` is invoked on an already-set-up project.

**Every update is also a cleanup, not just an append.** This is the heart of curation, and it
matters as much as adding. Before you add, reconcile: as facts change, update them in place and
drop what they replace; as questions resolve, remove them. Duplication and staleness are bugs.

**Three layers by read frequency (2026-09-09).** More context beats no context, but bloat loses
to optimal context, so the living setup is split by how often each part is read:
- **`CLAUDE.md`** - every message. Budget **8 KB / 100 lines** (hook-checked). It holds exactly:
  the title, an `e2e-state` marker if any, at most a 1-3 line pointer (e.g. e2e's Shipped note),
  and the live-document block with the per-message hard rules inside it. Everything else is routed
  by the *CLAUDE.md routing test* below.
- **`PROJECT.md`** - once per session, IN FULL, before acting. The SessionStart hook does not
  inject its content (the harness persists hook output above a moving threshold and shows a 2 KB
  preview); it tells you the file's size and to Read it now, and the edit gate denies project
  writes until you have. Whole-file budget **20 KB / 250 lines**. Sections: the header + contract,
  `## Goal and definition of done`, `## Scope and non-goals`, `## Map - where to find what`,
  `## Current state and next action`, `## Decisions locked` (index: rule + one-line why + who/when, max 3 lines
  each), `## Plan / workstreams`, `## Open questions`, `## Lessons` (key lessons as rules, max 3
  lines each). Nothing else: no change log, no research notes, no execution plan in this file.
- **`project-memory/`** - on demand, via the Map. `decisions.md` (the full wording and rationale
  of every decision), `lessons.md` (every story, max 8 lines each, grouped by theme),
  `changelog.md` (every milestone, newest first, one entry per date, max 3 lines each, no total
  cap - it is the full history), e2e's `research-notes.md` and `execution-plan.md`, and any topic
  file. A file over 40 KB gets split by topic. Read a file only when its Map row says the task
  touches it, and ALWAYS before editing it.
- **Nothing is lost by the split.** Every decision and every behavior-changing lesson keeps its
  rule AND a one-line why in `PROJECT.md`, so the once-per-session read carries what to do and the
  short reason; only the full story, the alternatives and the mechanism move out. Each rule line
  carries a pointer to its home, the lint fails a pointer whose heading is gone and warns when the
  decision counts differ between the two files, and a line may leave `PROJECT.md` only when its
  home exists.

**CLAUDE.md routing test - where each piece of content lives.** Ask these of every section or
fact, in order; the first yes wins:
1. Does EVERY message need it, even a one-line question? (the dominant constraint, a safety
   guardrail such as "never commit a key", the `e2e-state` marker, a pointer such as "before any
   API call read `project-memory/api-reference.md`") -> `CLAUDE.md`, as a 1-2 line Hard rules
   bullet inside the block.
2. Does every SESSION need it before acting? (goal, scope, current state, the current verified
   snapshot, decision and key-lesson rules, the Map) -> `PROJECT.md`.
3. Does only SOME task need it? (reference tables, API or gateway details, limits and how they were
   found, dated notes, refresh or incident history, run instructions, file lists, benchmark
   verdicts, runbooks) -> a `project-memory/<topic>.md`, with a Map row whose "read it when" names
   those tasks.
4. Does another file already hold it? (README, config comments, a skill) -> delete it from
   `CLAUDE.md` once that home is verified, and repoint every reference to it.
A pointer line in `CLAUDE.md` names the task and the file; it never restates the content.

**Home rule - a fact lives in ONE home; everywhere else it is one line plus a pointer.** A
decision's RULE (+ who/when) -> `PROJECT.md` `## Decisions locked`; its full wording and
rationale -> `project-memory/decisions.md`. A lesson's STORY -> `project-memory/lessons.md`; its
RULE, only if it changes how we work on this project -> `PROJECT.md` `## Lessons`. A milestone ->
`project-memory/changelog.md` only. An owner preference about how to work -> memory, in full. A
rule body, recipe, ID registry, or template that belongs to a skill -> that skill's `references/`.
A per-run analysis -> the dated run file. A subject with more detail than a rule line -> its own
`project-memory/<topic>.md`. State, the Map, and the indexes -> `PROJECT.md`. A line may leave
`PROJECT.md` only when its home is named and exists; no home means create the home first or keep
the line. Deleting a duplicate is maintenance, not loss. **Write order: the project-memory home
FIRST, `PROJECT.md` LAST** - the pointer never precedes its target, and the Stop gate (which
requires `PROJECT.md` to be the newest project write) passes on the first try.

**The Map is the contract.** `## Map - where to find what` is a table `location | what lives
there | read it when`. Row 1 is `PROJECT.md` itself and states what is ALWAYS here (goals, map,
current state and next action, decisions index, key-lesson rules, open questions). Then ONE ROW
PER `project-memory/` FILE, each with a one-line summary of what lives there and when to open it.
Then every folder, file, skill reference, memory folder, or external registry that matters. Every
path in it must exist, every top-level project folder and every project-memory file must appear
in it - adding, archiving or moving anything without a Map update fails the lint, so the turn
cannot end.

**The update algorithm - run it on every write to `PROJECT.md` or a `project-memory/` file:**

1. **Know what you are editing.** `PROJECT.md` was read in full at session start (the edit gate
   enforces it); before writing a `project-memory/` file, Read it - never edit a file you have not
   read this session.
2. **Classify each new fact** the work produced: durable choice, lesson, state change, resolved
   question, or milestone. A fact has exactly ONE home (file and section, per the home rule).
3. **Rewrite the home in place, superseding old content - home first, `PROJECT.md` last.**
   *Current state and next action* is rewritten every time so it describes only NOW. A new
   durable choice REPLACES the decision it supersedes in BOTH `decisions.md` (full wording) and
   *Decisions locked* (rule + one-line why + who/when, max 3 lines; never stack old and new side by side). An
   answered *Open question* is deleted, its answer folded into a decision or *Current state*; a
   partly settled one is split at once. Feedback and failures go to `lessons.md` as the full story
   (max 8 lines, under its theme, deduped against Decisions; the memory file becomes a pointer),
   and to *Lessons* as a rule line (max 3 lines) only if they change how we work here. Only a
   milestone earns a `changelog.md` entry (newest first), **1-3 lines**: what shipped, the commit,
   the outcome - one entry per date (merge same-day work). Verification narratives, review
   blow-by-blow, and mechanism detail never go in the log. Most updates add no entry; a line every
   session is a diary, which is a bug. Whenever a file or folder is added, moved, or archived, and
   whenever a project-memory file's content changes, its *Map* row changes in the same edit.
4. **Sweep before saving.** Delete or merge everything now redundant, resolved, stale, or
   duplicated, anywhere in `PROJECT.md` and in the files you touched. Deleting a line that no
   longer earns its place is REQUIRED maintenance, not data loss - but only when its home is named
   and exists (home rule); real decisions and lessons are compacted or moved, never dropped. No
   invented sections in `PROJECT.md`: use only this skill's canonical headers (Goal and definition
   of done, Scope and non-goals, Map - where to find what, Current state and next action,
   Decisions locked, Plan / workstreams, Open questions, Lessons) - never a "Reference"/"Summary"/
   "Notes"/"Change log" section, and never a suffix on a canonical header; a new subject becomes a
   `project-memory/<topic>.md` with a Map row instead.
5. **Red-flag test before saving:** an update that only adds lines and rewrites nothing is almost
   always wrong. If your diff is append-only, you skipped steps 3-4 - go back and sweep.
   Quantitative tripwires, enforced by `project-md-lint` on every write (see *Gates* below):
   `PROJECT.md` over 20 KB / 250 lines, `CLAUDE.md` over 8 KB / 100 lines (every-message budget,
   blocking once that file has fit it once), a decision over 3 lines, a lesson rule over 3 lines, an open
   question over 3 lines or partly settled, a `## Change log` / `## Research notes` / `## Execution
   plan` section still in `PROJECT.md`, a `project-memory/` file without a Map row, a Map path that
   does not exist, a top-level folder missing from the Map, a pointer that does not resolve (a
   `project-memory/x.md § Heading` whose heading is gone is an error - the index line has lost its
   home), a `lessons.md` story over 8 lines, a `changelog.md` entry over 3 lines or two entries on
   one date, a non-canonical header. Each means compaction is overdue and must happen in THIS
   edit - the Stop gate will not end the turn otherwise. Warnings (do not block): a project-memory
   file over 40 KB, a Map row without a "read it when", a decisions count that differs between
   *Decisions locked* and `decisions.md`, a file without the standard header, more than 3 KB of
   `CLAUDE.md` outside the live-document block, a `CLAUDE.md` without the block (or none at all).
6. **Self-heal the setup.** A one-time upgrade so existing projects pick up the current discipline
   on next touch:
   - *project-memory layout (2026-09-09):* if the project root has no `project-memory/` folder, or
     `PROJECT.md`'s contract comment lacks the phrase "project-memory", the project is on the
     single-file layout. Migrate it in a DEDICATED session (say so and ask when the task at hand
     is something else - the hooks keep the format rules in legacy grace until the file lints
     clean once): follow the migration procedure in `references/project-memory-template.md`
     (create the folder and the three standard files, move the full content out, leave rule lines
     + pointers, add the Map rows, replace the contract and the title blockquote with the
     template's, rename a `playbook/` folder to `project-memory/` if that is what the project
     used, replace the `CLAUDE.md` block's items 1-4, run *CLAUDE.md slimming* below), then run
     the lint until clean.
   - *CLAUDE.md slimming (2026-09-18):* if `CLAUDE.md` is over 8 KB / 100 lines or carries more
     than 3 KB outside the live-document block (the SessionStart bootstrap and the lint both say
     so), every message is paying for content most messages never use. Build the move list with
     the *CLAUDE.md routing test* (one row per section: section -> home, and whether that home
     already holds it), show it, and ask ONE yes/no. After the yes: write each home first (a new
     `project-memory/` topic file gets its Map row), grep the project and its memory folder for
     pointers to the moved sections and repoint them, leave in `CLAUDE.md` only routing-test-1
     content plus the block, then write `PROJECT.md` last and lint until clean. The first time
     `CLAUDE.md` fits the budget arms its gate: from then on a turn that pushes it back over is
     blocked. "Never delete content you did not create" means nothing is LOST - it does not mean
     a fat `CLAUDE.md` stays fat. Leaving it untouched because "it was already there" is the
     failure this step exists for. Never slim silently and never mid-task: ask first.
   - *Bootstrap:* if this project's `CLAUDE.md` `<!-- live-document:start -->` block carries
     old-style maintenance items (recognizable by the phrase "after any answer or change", a
     "Curate, do not bloat" item, or items 2-4 that lack the word "Tripwire"), replace just
     items 2-4 of that block with the current items 2-4 from `references/claude-md-block.md`.
     Preserve every other line and the markers.
   - *Living doc:* if `PROJECT.md` lacks the `MAINTENANCE CONTRACT` comment, inject it right under
     the title blockquote, and add the per-section comments from
     `references/project-md-template.md` under each canonical header that lacks one. If its
     contract lacks the `Tripwire` item, replace the whole comment with the current one from the
     template.
   - Format rule: if the block's Hard rules have no bullet containing the words "Summary, then Reasoning", insert the current chunk-delivery bullet from `references/claude-md-block.md` right after the "Ask before assuming" rule.
   - Next Actions rule: if the block's Hard rules have no bullet containing the words "Next Actions", insert the two current bullets (Next Actions file + tidy root) from `references/claude-md-block.md` right after the "Summary, then Reasoning" bullet.
   - Map + home rule (2026-09-02): if `PROJECT.md` lacks `## Map - where to find what`, scaffold it
     right after *Scope and non-goals* from the file's own pointers and the project's top-level
     folders, then fix what the lint reports. If the `CLAUDE.md` block's items 1-4 lack the phrase
     "home rule" or the phrase "project-memory", replace items 1-4 with the current ones from
     `references/claude-md-block.md`; if `PROJECT.md`'s contract comment lacks either phrase,
     replace it with the template's.
   - For e2e-managed projects, never touch the `e2e-state` marker or `PLAN.md`; e2e's
     `## Research notes` / `## Execution plan` migrate to `project-memory/research-notes.md` /
     `execution-plan.md` only between phases, never mid-phase.

**Folder tidiness - part of every curation pass.** The project root is part of the living setup: a
root full of loose screenshots, scratch code, and generated reports hides the files that matter.
Check it at session start and whenever you touch the project:

- Tripwire: 3+ loose root files of one recognizable kind (screenshots/images, code examples or
  scratch snippets, generated reports/exports/logs, next-action files outside `next-actions/`), or
  roughly 8+ loose non-doc files overall.
- When tripped, build the FULL move list (e.g. "12 .png -> screenshots/"), show it, and ask ONE
  yes/no question. Move only after the yes - never silently. Canonical folders: `screenshots/`,
  `code-examples/`, `reports/`, `next-actions/`, `project-memory/` (detail layer, never a move
  target for artifacts and never moved itself); add others sparingly, only when a real cluster
  exists.
- Safety: grep each filename for references before moving; if something references the file,
  update the reference in the same edit or leave the file in place and say why. Use `git mv` in
  git repos. Never move CLAUDE.md, PROJECT.md, README, `project-memory/`, manifests/configs/dotfiles,
  source trees, or anything an active e2e/gsd flow owns.
- Prevention beats cleanup: once the folders exist, file NEW artifacts of those kinds straight
  into them, and record the layout once in *Decisions locked* so every future session keeps the
  habit.

The standing test: a fresh agent reading `PROJECT.md`, and on demand the `project-memory/` files
its Map names, can continue correctly without the user re-explaining anything.

## Gates (hooks) - what makes the maintenance mandatory

Prose rules are advisory; these hooks (in `~/.claude/hooks/`, registered globally, active only in
a working directory that holds a `PROJECT.md`) are not:

- `furkan-session-context.js` (SessionStart, also after `/clear` and compaction) emits a short
  bootstrap (under 2,000 chars, so it is fully visible even when the harness persists hook
  output): `PROJECT.md`'s size and the instruction to Read it in full now, the `project-memory/`
  file list with sizes (and any file newer than `PROJECT.md`, which means its Map row or index
  lines may be stale), `CLAUDE.md`'s size against its every-message budget (an over-budget file
  gets a "!!" line asking for the slimming move list), the lint summary, and any PENDING RECONCILE left by an earlier session that
  edited project files without updating `PROJECT.md` - this survives `/clear` and compaction. It
  also resets the session's "PROJECT.md read" flag.
- `furkan-edit-gate.js` (PreToolUse on Write/Edit) denies a substantive project edit (project
  files and `project-memory/`; `PROJECT.md` and `CLAUDE.md` themselves are exempt) until
  `PROJECT.md` has been Read in full this session (whole file, no offset/limit). Fail-safe: after 3
  denies it allows, says so, and the next SessionStart reports it.
- `furkan-project-md-gate.js` (PostToolUse on Read/Write/Edit) records the full Read of
  `PROJECT.md`, records every substantive project edit (`project-memory/` files count), and on a
  write to `PROJECT.md` runs `project-md-lint.js` (on a write to a `project-memory/` file, only
  that file's rules; on a write to `CLAUDE.md`, only its every-message budget); errors come back
  as feedback to fix in the same turn.
- `furkan-stop-gate.js` (Stop) refuses to end a turn that edited project files until `PROJECT.md`
  was written afterwards AND lints clean, and a turn of a session that wrote `CLAUDE.md` while
  `CLAUDE.md` is over budget (at most 4 blocks per condition, then it gives up loudly).
  Q&A turns, reads, and edits outside the project or under `next-actions/` never block. If only
  `project-memory/` files changed, the fix is to re-touch their Map rows / index lines.
- `furkan-precompact-gate.js` (PreCompact) holds one compaction while a reconcile is pending.
- Legacy grace: the FORMAT rules bite for a project only after its `PROJECT.md` has linted clean
  once under the CURRENT contract (the lint CLI or a clean write sets the flag; the 2026-09-09
  layout renamed the flag so every project re-earns it); until then only the reconcile rule
  applies and the bootstrap nudges. Migrate an old project in a dedicated session, not mid-task.
  `CLAUDE.md`'s budget has its own grace flag (`claude1-`): it only warns until that project's
  `CLAUDE.md` has fit the budget once, then it blocks like any other error.

How to satisfy a block: read the listed files, reconcile home first and `PROJECT.md` last per the
update algorithm, keep the Map current, end the turn. `node ~/.claude/hooks/project-md-lint.js
PROJECT.md` runs the lint by hand. Changing a limit means changing `LIMITS` in the lint AND the
numbers in this skill, its templates, and the e2e / project-partner / big-project clones together.

## Coexistence rules (do not fight other tooling)

Other skills also write project-root files. Detect them and stay additive:

- **e2e** - look for `<!-- e2e-state ... -->` in `CLAUDE.md`. Append your block to `CLAUDE.md`;
  never touch the e2e state marker. e2e projects carry two e2e-owned files in `project-memory/`
  (`research-notes.md`, `execution-plan.md`; older runs had them as `PROJECT.md` sections) - while
  the marker is not `phase=complete` leave their structure to the e2e flow (curate everything else
  normally). Legacy e2e projects have a separate `PLAN.md` (and possibly `RESEARCH.md` /
  `design-*.md` / `ceo-plan-*.md`) - never touch those.
- **gsd** - look for a `.planning/` directory and a gsd-style `PROJECT.md`. Augment that
  `PROJECT.md` in place; never touch `.planning/`.

Rule of thumb: append to `CLAUDE.md`, augment `PROJECT.md`, and never delete content you did not
create. An over-budget `CLAUDE.md` is slimmed by MOVING its content to its home after the owner's
one yes (*CLAUDE.md slimming*), never by deleting it and never by leaving it fat.
