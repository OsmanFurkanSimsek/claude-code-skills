---
name: live-document
description: Use when the user types /live-document, wants project state to survive across sessions ("keep track of this project", "I keep losing context between sessions", "set up project memory / a living doc", "remember where we left off"), or when starting a substantial project spanning multiple sessions. Also use on projects whose CLAUDE.md contains a <!-- live-document:start --> marker. Do NOT use for one-off edits, bug fixes, debugging, quick lookups, or when an active e2e/gsd build flow already governs the project's files.
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
understands the project, then scaffolds two files in the project root:

- **`CLAUDE.md`** - a THIN, auto-loading bootstrap (~one screen, never grows). Claude Code loads
  it automatically every session; its only job is to remind the agent to read and maintain the
  real source of truth.
- **`PROJECT.md`** - the LIVING single source of truth, in two tiers: Tier 1 (goal, scope, the
  Map, current state, open questions, decisions index) is injected by the SessionStart hook every
  session; Tier 2 (plan, change log, lessons in full, research notes) is read on demand.

Because `CLAUDE.md` auto-loads, maintenance becomes **self-sustaining**: every future session is
reminded to read `PROJECT.md` first and to record what changed. After this one-time setup you
should never again have to tell an agent to read, update, or maintain these files, and the
PROJECT.md gates (hooks - see *Gates* below) make the maintenance mandatory, not advisory. The acceptance
test for the whole system: *a fresh agent reading only `PROJECT.md` can continue the project
correctly, with nothing re-explained.*

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

**Chunking rule** - for Action-mode work with more than about 10 steps, or any multi-part plan:

- Never dump the full step list. Split the work into chunks of roughly 5-10 steps and deliver ONE chunk per turn.
- End every chunk by asking the user to confirm when the chunk is done, or to report what failed. Do not send the next chunk before that confirmation.
- Before delivering the next chunk, update PROJECT.md first: the full chunk list with status markers lives in Plan / workstreams, the active chunk is named in Current state and next action, and failures go to Lessons.
- After each PROJECT.md update, tell the user explicitly: everything is documented in PROJECT.md, so you can clear the context whenever you want and a fresh session will continue from the next chunk.

**Next Actions file** - a real handoff (about 3+ steps the user must do themselves, or ANY chunk of the chunking rule) also gets a durable copy the user can open outside the chat. Write an interactive, self-contained `next-actions/<YYYY-MM-DD_HH-MM>-next-actions.html` at the project root, following `references/next-actions-template.md` exactly (TLDR paragraph first, then reasoning with the alternatives considered and why this path won, then the steps in the same super-simple language). Every handoff gets a NEW dated file; keep every old one - the folder is the history and the date-time prefix finds the latest. Announce the path in one chat line. Trivial asks (one command, one click) stay chat-only.

**Recap on request** - when the user asks where we are ("where are we", "remind me", "recap", "I lost the thread"), reply in Answer mode with a plain-English recap of 3-5 sentences: the request that started this session, what we are doing and why, what is already done, what comes next. Source it from PROJECT.md *Current state* plus the conversation; write no file, add no steps. If the previous reply was long, restate its substance shorter and simpler under the recap.

The standing test for this section: the user always knows what we are doing, why we are doing it, and exactly what to do next, a context clear at any chunk boundary loses nothing, and every real handoff leaves a dated Next Actions file behind.

## Mode detection (do this first, on every invocation)

Check the project root for a live-document setup:

1. Read the root `CLAUDE.md` (if any) and look for the marker `<!-- live-document:start -->`.
2. Also check whether a `PROJECT.md` exists with this skill's section headers (Goal and definition
   of done, Decisions locked, Change log, Lessons).

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

### Phase 2 - Scaffold the two files in the project root (only after confirmation)

**`CLAUDE.md` (thin bootstrap) - append, never overwrite.**
Use the block in `references/claude-md-block.md`, filled from the interview.
- If a `CLAUDE.md` already exists: **append** the block between its `<!-- live-document:start -->`
  and `<!-- live-document:end -->` markers, preserving every existing line above it. Never delete
  or rewrite content you didn't add.
- If no `CLAUDE.md` exists: create one with a one-line header plus the block.
- Keep it thin (~one screen). It is a bootstrap, not a log - it must not grow.

**`PROJECT.md` (living source of truth) - create or augment.**
Use the template in `references/project-md-template.md`, filled from the interview.
- If no `PROJECT.md` exists: create it from the template.
- If a `PROJECT.md` already exists (e.g. from gsd): **augment** it - add any missing living
  sections and merge in the interview content without deleting existing material. One file only;
  do not create a second tracking document.

**Memory is a home, not a mirror (home rule).** If a persistent memory facility is available
(e.g. `~/.claude/projects/<project-slug>/memory/`), add a one-line pointer to these two files in
its index as a backup trigger, and from then on split by type: an owner preference about how to
work lives in memory in full; a project lesson's full story lives in `PROJECT.md` `## Lessons` and
its memory file is a pointer (frontmatter + Why/How-to-apply + "Full story: PROJECT.md § Lessons ›
<title>"). Never two stories of one lesson, and never a third tracking file.

After scaffolding, tell the user setup is done and that from now on these files maintain
themselves - they will not need to ask you to read or update them again.

## Curation mode

This is what every future session does (the `CLAUDE.md` auto-load reminds it), and what you do
when `/live-document` is invoked on an already-set-up project.

**Every update is also a cleanup, not just an append.** This is the heart of curation, and it
matters as much as adding. Before you add, reconcile: as facts change, update them in place and
drop what they replace; as questions resolve, remove them. Duplication and staleness are bugs.

**Two tiers, one file (2026-09-02).** `PROJECT.md` may grow - more context beats no context - but
bloat loses to optimal context, so the file is split by section into what every session pays for
and what is read on demand:
- **Tier 1 - injected at session start by the SessionStart hook**, hard budget **14 KB / 180
  lines** (the harness silently truncates larger hook output to a 2 KB preview): the header +
  contract, `## Goal and definition of done`, `## Scope and non-goals`, `## Map - where to find
  what`, `## Current state and next action`, `## Open questions`, `## Decisions locked` (index
  form: rule + who/when + pointer, max 4 lines each).
- **Tier 2 - read on demand** (grep or Read the section when the task touches it, and always
  before editing the file), may grow, per-entry limits only: `## Plan / workstreams`, `## Change
  log` (entries max 3 lines, one entry per date, entries older than 14 days shrink to one line,
  max 30 lines), `## Lessons` (full stories, max 8 lines each), `## Research notes` (e2e).

**Home rule - a fact lives in ONE home; everywhere else it is one line plus a pointer.** A project
lesson's full story -> `## Lessons` (its memory file is a pointer). An owner preference about how
to work -> memory, in full. A rule body, recipe, ID registry, or template -> the owning skill's
`references/`. A per-run analysis -> the dated run file. State, the decisions index, the Map, and
milestones -> `PROJECT.md`. A line may leave `PROJECT.md` only when its home is named and exists;
no home means create the home first or keep the line. Deleting a duplicate is maintenance, not loss.

**The Map is the contract.** `## Map - where to find what` is a table `location | what lives
there | read it when`. Row 1 is `PROJECT.md` itself and states what is ALWAYS here (goals, map,
current state and next action, open questions, decisions index, lessons, milestones). Every other
row names a folder, file, skill reference, memory folder, or external registry. Every path in it
must exist and every top-level project folder must appear in it - archiving or moving anything
without a Map update fails the lint, so the turn cannot end.

**The update algorithm - run it on every write to `PROJECT.md`:**

1. **Know what you are editing.** The SessionStart hook injected Tier 1; before writing, read every
   Tier 2 section you will touch (and any section the task touches) - never edit a section you
   have not read this session.
2. **Classify each new fact** the work produced: durable choice, lesson, state change, resolved
   question, or milestone. A fact has exactly ONE home section.
3. **Rewrite the home section in place, superseding old content.** *Current state and next action*
   is rewritten every time so it describes only NOW. A new durable choice REPLACES the decision it
   supersedes in *Decisions locked* (never stack old and new side by side); a decision is the rule
   + who/when + a pointer, max 4 lines - the mechanism lives in its home. An answered *Open
   question* is deleted, its answer folded into a decision or *Current state*; a partly settled one
   is split at once. Feedback and failures go to *Lessons* as the full story (max 8 lines, deduped
   against Decisions; the memory file becomes a pointer). Only a milestone earns a *Change log*
   entry (newest first), **1-3 lines**: what shipped, the commit, the outcome - one entry per date
   (merge same-day work), entries older than 14 days shrink to one line, the log stays under 30
   lines. Verification narratives, review blow-by-blow, and mechanism detail never go in the log.
   Most updates add no entry; a line every session is a diary, which is a bug. Whenever a file or
   folder is added, moved, or archived, its *Map* row changes in the same edit.
4. **Sweep the whole file before saving.** Delete or merge everything now redundant, resolved,
   stale, or duplicated, anywhere in the file - not just the sections you touched. Deleting a line
   that no longer earns its place is REQUIRED maintenance, not data loss - but only when its home
   is named and exists (home rule); real decisions and lessons are compacted or moved, never
   dropped. No invented sections: use only this skill's canonical headers (Goal and definition of
   done, Scope and non-goals, Map - where to find what, Current state and next action, Decisions
   locked, Plan / workstreams, Open questions, Change log, Lessons) - plus, on e2e-managed
   projects, e2e's own `## Research notes` and `## Execution plan` - never a "Reference"/"Summary"/
   "Notes" section, and never a suffix on a canonical header.
5. **Red-flag test before saving:** an update that only adds lines and rewrites nothing is almost
   always wrong. If your diff is append-only, you skipped steps 3-4 - go back and sweep.
   Quantitative tripwires, enforced by `project-md-lint` on every write (see *Gates* below): Tier 1
   over 14 KB / 180 lines, a decision over 4 lines, a lesson over 8 lines, an open question over 3
   lines or partly settled, a Change log over 30 lines, an entry over 3 lines, two entries on one
   date, an entry older than 14 days still over 1 line, a pointer that does not resolve, a Map path
   that does not exist, a top-level folder missing from the Map, a non-canonical header. Each means
   compaction is overdue and must happen in THIS edit - the Stop gate will not end the turn otherwise.
6. **Self-heal the setup.** A one-time upgrade so existing projects pick up the current discipline
   on next touch:
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
     "home rule", replace items 1-4 with the current ones from `references/claude-md-block.md`; if
     `PROJECT.md`'s contract comment lacks "home rule", replace it with the template's.
   - For e2e-managed projects, never touch the `e2e-state` marker or `PLAN.md`.

**Folder tidiness - part of every curation pass.** The project root is part of the living setup: a
root full of loose screenshots, scratch code, and generated reports hides the files that matter.
Check it at session start and whenever you touch the project:

- Tripwire: 3+ loose root files of one recognizable kind (screenshots/images, code examples or
  scratch snippets, generated reports/exports/logs, next-action files outside `next-actions/`), or
  roughly 8+ loose non-doc files overall.
- When tripped, build the FULL move list (e.g. "12 .png -> screenshots/"), show it, and ask ONE
  yes/no question. Move only after the yes - never silently. Canonical folders: `screenshots/`,
  `code-examples/`, `reports/`, `next-actions/`; add others sparingly, only when a real cluster
  exists.
- Safety: grep each filename for references before moving; if something references the file,
  update the reference in the same pass or leave the file in place and say why. Use `git mv` in
  git repos. Never move CLAUDE.md, PROJECT.md, README, manifests/configs/dotfiles, source trees,
  or anything an active e2e/gsd flow owns.
- Prevention beats cleanup: once the folders exist, file NEW artifacts of those kinds straight
  into them, and record the layout once in *Decisions locked* so every future session keeps the
  habit.

The standing test: a fresh agent reading only `PROJECT.md` can continue correctly without the user
re-explaining anything.

## Gates (hooks) - what makes the maintenance mandatory

Prose rules are advisory; these hooks (in `~/.claude/hooks/`, registered globally, active only in
a working directory that holds a `PROJECT.md`) are not:

- `furkan-session-context.js` (SessionStart) injects Tier 1, lists the Tier 2 sections with their
  sizes, appends the lint summary, and surfaces any PENDING RECONCILE left by an earlier session
  that edited project files without updating `PROJECT.md` - this survives `/clear` and compaction.
- `furkan-project-md-gate.js` (PostToolUse on Write/Edit) records every substantive project edit
  and, on a write to `PROJECT.md`, runs `project-md-lint.js`; errors come back as feedback to fix
  in the same turn.
- `furkan-stop-gate.js` (Stop) refuses to end a turn that edited project files until `PROJECT.md`
  was written afterwards AND lints clean (at most 4 blocks per condition, then it gives up loudly).
  Q&A turns, reads, and edits outside the project or under `next-actions/` never block.
- `furkan-precompact-gate.js` (PreCompact) holds one compaction while a reconcile is pending.
- Legacy grace: the FORMAT rules bite for a project only after its `PROJECT.md` has linted clean
  once (the lint CLI or a clean write sets the flag); until then only the reconcile rule applies and
  the SessionStart line nudges. Bring an old file into shape in a dedicated session, not mid-task.

How to satisfy a block: read the listed files, reconcile `PROJECT.md` per the update algorithm,
keep the Map current, end the turn. `node ~/.claude/hooks/project-md-lint.js PROJECT.md` runs the
lint by hand. Changing a limit means changing `LIMITS` in the lint AND the numbers in this skill,
its templates, and the e2e / big-project clones together.

## Coexistence rules (do not fight other tooling)

Other skills also write project-root files. Detect them and stay additive:

- **e2e** - look for `<!-- e2e-state ... -->` in `CLAUDE.md`. Append your block to `CLAUDE.md`;
  never touch the e2e state marker. Consolidated e2e projects carry two e2e-owned sections inside
  `PROJECT.md` (`## Research notes`, `## Execution plan`) - treat them as canonical, and while the
  marker is not `phase=complete` leave their structure to the e2e flow (curate the rest of the file
  normally). Legacy e2e projects have a separate `PLAN.md` (and possibly `RESEARCH.md` /
  `design-*.md` / `ceo-plan-*.md`) - never touch those.
- **gsd** - look for a `.planning/` directory and a gsd-style `PROJECT.md`. Augment that
  `PROJECT.md` in place; never touch `.planning/`.

Rule of thumb: append to `CLAUDE.md`, augment `PROJECT.md`, and never delete or rewrite files you
did not create.
