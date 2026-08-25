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
- **`PROJECT.md`** - the LIVING single source of truth. Holds the actual content; read on demand.

Because `CLAUDE.md` auto-loads, maintenance becomes **self-sustaining**: every future session is
reminded to read `PROJECT.md` first and to record what changed. After this one-time setup you
should never again have to tell an agent to read, update, or maintain these files. The acceptance
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

**Mirror a backup pointer (best-effort).** If a persistent memory facility is available
(e.g. `~/.claude/projects/<project-slug>/memory/MEMORY.md`), add a one-line pointer to these two
files there as a backup trigger. Otherwise the two files are the source of truth. Either way, do
not create a third tracking file.

After scaffolding, tell the user setup is done and that from now on these files maintain
themselves - they will not need to ask you to read or update them again.

## Curation mode

This is what every future session does (the `CLAUDE.md` auto-load reminds it), and what you do
when `/live-document` is invoked on an already-set-up project.

**Every update is also a cleanup, not just an append.** This is the heart of curation, and it
matters as much as adding. `PROJECT.md` is re-read in full at the start of every session, so every
line that is redundant, stale, resolved, or duplicated is paid for again and again - it overwhelms
the reader and wastes tokens on each pass. The file may grow **only** when there is genuinely more
essential information to hold, never from accumulation. Before you add, reconcile: as facts change,
update them in place and drop what they replace; as questions resolve, remove them. Duplication and
staleness are bugs. There is **no size limit** - a big project may legitimately need a big
`PROJECT.md` - the only test is whether every line still earns its place.

**The update algorithm - run it on every write to `PROJECT.md`:**

1. **Read `PROJECT.md` in full** before acting.
2. **Classify each new fact** the work produced: durable choice, lesson, state change, resolved
   question, or milestone. A fact has exactly ONE home section.
3. **Rewrite the home section in place, superseding old content.** *Current state and next action*
   is rewritten every time so it describes only NOW. A new durable choice REPLACES the decision it
   supersedes in *Decisions locked* (never stack old and new side by side). An answered *Open
   question* is deleted, its answer folded into a decision or *Current state*. Feedback and
   failures go to *Lessons* (deduped: what was tried, what failed, the lesson). Only a milestone
   earns a *Change log* entry (newest first), and an entry is **1-3 lines**: what shipped, the
   commit, the outcome. Verification narratives, review blow-by-blow, and mechanism detail never
   go in the log (they live in Decisions/Lessons or in the code). When adding an entry, compact
   any older entry still over 3 lines - the log's tail decays to ~1 line per milestone. Most
   updates add no entry; a line every session is a diary, which is a bug.
4. **Sweep the whole file before saving.** Delete or merge everything now redundant, resolved,
   stale, or duplicated, anywhere in the file - not just the sections you touched. Deleting a line
   that no longer earns its place is REQUIRED maintenance, not data loss (real decisions and
   lessons are compacted or moved, never dropped). No invented sections: use only this skill's
   canonical headers - plus, on e2e-managed projects, e2e's own `## Research notes` and
   `## Execution plan` sections - never add a "Reference"/"Summary"/"Notes" section that
   duplicates others.
5. **Red-flag test before saving:** an update that only adds lines and rewrites nothing is almost
   always wrong. If your diff is append-only, you skipped steps 3-4 - go back and sweep.
   Quantitative tripwires (these exist because qualitative "sweep" rules alone let a real project's
   file grow to 700 lines): the *Change log* tops ~30 lines, any log entry runs past 3 lines, or
   the file grew even though the work resolved or superseded something - each means compaction is
   overdue and must happen in THIS edit, not be deferred.
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
