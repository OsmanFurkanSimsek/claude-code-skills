---
name: e2e
description: >-
  Use when the user types /e2e or asks for a full end-to-end, production-quality
  build or deliverable - "build this end to end", "build it the right way", "do
  the whole thing", "full development cycle", "do this analysis / report / Power
  BI dashboard the right way" - for software or a non-code deliverable
  (analysis, deck, report, BI dashboard, data pipeline, document). Also use when
  the project's CLAUDE.md contains an <!-- e2e-state: --> marker (resume the
  run). Flags: --coverage <lines>/<branches>, --track build|deliverable,
  --with-discovery, --skip-discovery. Lean toward triggering on "full" or
  "end-to-end" asks. Do NOT use for typo fixes, single-line edits, quick
  lookups, code-review-only requests, or debugging an isolated bug.
---

# End-to-end build & delivery

This skill drives a full feature, product, OR non-code deliverable (analysis, presentation, report, Power BI / BI dashboard, data pipeline, document, research write-up) through twelve phases. The product of running it is a working, verified, reviewed, simplified artifact plus **exactly two** durable docs at the project root that let the work survive a `/clear` and resume in any future session:

- `PROJECT.md` - the **living source of truth**: goal, scope, current state, decisions locked, open questions, change log, lessons - plus, while a run is active, two e2e-owned sections: `## Research notes` (Phase 4 findings with citations) and `## Execution plan` (the master phase/step status table and per-step detail; deleted at Phase 12 after its outcome is folded into *Change log* / *Current state*). Maintained every session, unprompted. Same base format the `/live-document` skill uses, so that skill can curate it too.
- `CLAUDE.md` - a **thin constitution / bootstrap** that auto-loads, points at PROJECT.md, and carries the `<!-- e2e-state: -->` resume marker.

**No other tracking files.** Discovery output (Office Hours, CEO Review, Elon) is distilled straight into PROJECT.md's canonical sections, research lands in `## Research notes`, the plan lands in `## Execution plan`, and the Phase 8 playtest checklist lives inside the Execution plan's Phase 8 detail block. Do not create `PLAN.md`, `RESEARCH.md`, `design-*.md`, `ceo-plan-*.md`, or `PLAYTEST.md` on a fresh run. **Legacy runs** (projects whose earlier `/e2e` version already created those files) keep their multi-file layout for the life of that run - see the resume protocol.

## Tracks: Build vs Deliverable

This skill runs in one of two tracks, classified in Phase 0 and recorded in the `e2e-state` marker as `track=build|deliverable`:

- **Build** - software: an app, CLI, library, service, or pipeline-as-code. Verification means automated tests, a coverage gate, a deep read-only *code* review, Playwright, and the `simplify` skill.
- **Deliverable** - a non-code artifact: analysis, presentation/deck, report, Power BI / BI dashboard, data model, document, or research write-up. Verification means explicit acceptance checks, a whole-artifact review against success criteria, a critical-reasoning review, and a tighten/refine pass.

The twelve phases are the same in both tracks. What "implement", "test", and "review" *mean* adapts to the track. Each phase below notes its Build vs Deliverable behavior where they differ.

## The golden rule

**Gate after every step.** The user explicitly chose maximum gating. Never advance from one phase to the next, and never advance from one step inside Phase 6 (Execute) to the next, without an explicit "go" from the user. Surface what just finished, what's next, and any open questions, then wait. The cost of an extra checkpoint is one user message; the cost of skipping a checkpoint is unwanted work.

## What gates and what doesn't: write files silently, gate only on progress

Gating is about **advancing through the workflow** - the next phase, or the next step inside Phase 6. It is **not** about writing files. **Never ask permission to produce or update an artifact** ("Should I write this section?", "May I update PROJECT.md?" are bugs): distilling discovery output, writing `## Research notes`, scaffolding `## Execution plan`, and updating the living docs are all a silent side effect of doing the phase's work.

The living docs (`PROJECT.md`, `CLAUDE.md`) get one extra duty: the user wants to **see them change**. Update them dynamically as the work unfolds - not in a batch at the end - and **report each update in one line** at the checkpoint that follows, e.g. *"Updated PROJECT.md: locked the SQLite data-model decision, logged the v1 scope cut to Lessons; bumped CLAUDE.md marker to phase=research."* So: write every update without asking; announce the living-doc updates so the user can react; reserve actual stop-and-wait gates for phase and Phase-6-step boundaries only.

## Working style (applies to every phase)

Run the entire cycle as a critical, skeptical thought partner (System2 mode), not an order-taker:

- **No unstated assumptions.** When information is missing, ask. When several plausible choices exist, present 2 to 5 concrete options and let the user pick. Do not silently choose.
- **Every question must earn its place.** Ask only what blocks correct execution or quality. Batch related questions; ask in rounds, top blockers first.
- **Iterate to confidence, then act.** Keep clarifying until you are roughly 70 to 80 percent confident you can execute correctly. The moment you cross that bar, stop asking and do the work.
- **When the user cannot answer, recommend, do not stall.** Propose a labeled default: state it as an assumption, give the one-sentence rationale, and offer 1 to 3 alternatives.
- **Challenge happy-path thinking.** Surface hidden complexity, edge cases, and reasons an approach might fail.
- **Justify, do not flatter.** If you disagree, say so and give a well-reasoned alternative with evidence. Correct mistakes and say why.
- **Code-first for coding or calculation tasks.** Show the code or the steps, then the result, then a short summary. Show non-trivial math step by step; add a sanity check when relevant.
- **Be concise, precise, analytical.** Avoid the long-dash character in user-facing prose.

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

**Next Actions file pair** - a real handoff (about 3+ steps the user must do themselves, or ANY chunk of the chunking rule) also gets a durable copy the user can open outside the chat. Write `next-actions/<YYYY-MM-DD_HH-MM>-next-actions.md` plus a same-stem interactive `.html` at the project root, following `references/next-actions-template.md` exactly (TLDR paragraph first, then reasoning with the alternatives considered and why this path won, then the steps in the same super-simple language). Every handoff gets a NEW dated pair; keep every old pair - the folder is the history and the date-time prefix finds the latest. Announce both paths in one chat line. Trivial asks (one command, one click, a bare "go/continue" checkpoint) stay chat-only. In this workflow the Phase 8 hand-off to the user is always a real handoff; a Phase 6 step qualifies whenever the user must do multi-step manual work.

The standing test for this section: the user always knows what we are doing, why we are doing it, and exactly what to do next, a context clear at any chunk boundary loses nothing, and every real handoff leaves a dated Next Actions pair behind.

## Living-document discipline (applies to every phase)

**Stand up the living docs at the very start, not at Phase 5.** On a fresh run, create a thin `CLAUDE.md` (carrying the `e2e-state` marker) and a `PROJECT.md` skeleton in Phase 0, *before* discovery runs - so the user can `/clear` after ANY phase boundary and resume cold. A long discovery+build run must never hold state only in the context window. Every phase from Phase 1 on updates both files and bumps the marker. Phase 5 does not *create* these files; it *expands* PROJECT.md to full depth and writes `## Execution plan`.

From Phase 1 onward, PROJECT.md is the single source of truth, maintained unprompted exactly as the `/live-document` skill prescribes. **Every update is a reconcile-and-sweep, never an append** - PROJECT.md is re-read in full at every phase and every future session, so each stale line is paid for again and again. On every write:

- Rewrite the touched sections in place, superseding old content: *Current state and next action* describes only NOW; a new durable choice REPLACES the decision it supersedes in *Decisions locked* (never stack old and new); an answered *Open question* is deleted, its answer folded into a decision. One fact, one home section.
- Feedback and failures go to *Lessons* (deduped: what was tried, what failed, the lesson).
- Only a milestone (usually a phase boundary) earns a *Change log* entry (newest first), and an entry is **1-3 lines**: what shipped, the commit, the outcome. Verification narratives, review blow-by-blow, and mechanism detail never go in the log. When adding an entry, compact any older entry still over 3 lines - the log's tail decays to ~1 line per milestone. Most mid-phase updates add no entry.
- Sweep the whole file before saving: delete or merge everything now redundant, resolved, stale, or duplicated - anywhere in the file. Deleting a line that no longer earns its place is REQUIRED maintenance, not data loss (real decisions and lessons are compacted or moved, never dropped). No invented sections: only the template's canonical headers plus the two e2e-owned sections; there is no size limit - the only test is whether every line still earns its place.
- **Red-flag test:** an update that only adds lines and rewrites nothing is almost always wrong. Quantitative tripwires: the *Change log* tops ~30 lines, any entry runs past 3 lines, or the file grew even though the work resolved or superseded something - each means compaction is overdue and must happen in THIS edit, not be deferred.

One source of truth only: `## Execution plan` tracks *execution state*; the canonical sections hold *everything durable*. Do not duplicate one into the other (legacy runs: the execution state lives in PLAN.md instead - same rule). Write these updates silently, but surface a one-line summary of what changed at each checkpoint.

**Folder tidiness - part of the same discipline.** A run sheds artifacts (screenshots, scratch code, exports); a root full of them hides the files that matter. Tripwire: 3+ loose root files of one recognizable kind (screenshots/images, code examples or scratch snippets, generated reports/exports/logs, next-action files outside `next-actions/`), or roughly 8+ loose non-doc files overall. When tripped: build the FULL move list (e.g. "12 .png -> screenshots/"), show it, ask ONE yes/no question, move only after the yes. Canonical folders: `screenshots/`, `code-examples/`, `reports/`, `next-actions/`. Safety: grep each filename for references before moving (update the reference in the same pass, or leave the file and say why); use `git mv` in git repos; never move CLAUDE.md, PROJECT.md, README, manifests/configs/dotfiles, source trees, or the run's own tracked artifacts (legacy PLAN.md etc.). Once the folders exist, file NEW artifacts straight into them and record the layout once in *Decisions locked*.

**Self-heal older projects on resume** - four one-time, silent upgrades: (a) if the CLAUDE.md `<!-- live-document:start -->` block carries old-style maintenance items (the phrase "after any answer or change", a "Curate, do not bloat" / "Maintain, don't just append" item, or items 2-4 lacking the word "Tripwire"), replace just items 2-4 with the current items from `references/claude-md-template.md`; (b) if PROJECT.md lacks the `MAINTENANCE CONTRACT` comment, inject it under the title blockquote and add the per-section comments from `references/project-md-template.md`; if its contract lacks the `Tripwire` item, replace the whole comment with the template's; (c) if the block's Hard rules have no bullet containing "Summary, then Reasoning", insert the current chunk-delivery bullet from `references/claude-md-template.md` right after the "Ask before assuming" rule; (d) if the block's Hard rules have no bullet containing "Next Actions", insert the two current bullets (Next Actions file pair + tidy root) from `references/claude-md-template.md` right after the "Summary, then Reasoning" bullet. Preserve every other line and the markers; **never touch the `e2e-state` marker, and on legacy runs never touch PLAN.md**. Do NOT migrate a legacy multi-file run to the consolidated layout mid-run.

## Clear context at any phase boundary

Living docs + marker are refreshed at the **end of every phase** so the user can `/clear` after *any* phase and resume cold. Treat this as a first-class feature:

- **Every phase is a safe clear point**, and Phase 6 step boundaries too (the marker carries `step=<N> of=<M>`).
- **Offer it at every checkpoint**: end each phase-boundary checkpoint with one clause, e.g. *"... - you can `/clear` now and re-invoke `/e2e` here to resume from the marker, or say 'go' to continue."* Phase 5 keeps its stronger verbatim message.
- **On resume, trust the marker.** A clear after Phase 2 resumes at Phase 3, after Phase 7 at Phase 8, and so on - even during discovery.

## The twelve phases

0. **Bootstrap, resume detection & track classification** - start fresh or pick up mid-flow; detect legacy layouts; classify Build vs Deliverable.
1. **Office Hours** (conditional) - problem validation: who, what, why, narrowest wedge. Distilled straight into PROJECT.md.
2. **CEO Review** (conditional) - platonic / 10x version, scope decisions. Distilled straight into PROJECT.md.
3. **Elon algorithm** - invoke `/elon` so the user ruthlessly cuts down to MVP from the 10x vision; outcome folded into PROJECT.md.
4. **Research** - current state of the art. Lands in PROJECT.md `## Research notes`.
5. **Plan** - synthesize discovery + Elon + Research into a full-depth PROJECT.md (including `## Execution plan`) and a finalized thin CLAUDE.md, with deep reasoning.
6. **Execute** - walk the Execution plan steps; each step gets implementation + automated tests (Build) or acceptance checks (Deliverable) + manual verification.
7. **Holistic quality pass** - Build: full suite + measured coverage gate. Deliverable: whole-artifact review against success criteria.
8. **Human review & feedback** (mandatory) - user exercises or reads the product; blocker/annoying items fixed and re-verified before any expensive review.
9. **Critical review** - deep read-only review by a Claude reviewer subagent (no external CLI). User picks which findings to apply.
10. **Playwright UI testing** - only if a web frontend was detected and the user opts in.
11. **Simplification / tighten** - Build: `simplify` skill. Deliverable: tighten/refine pass. Re-verify to prove no regression.
12. **Final verification & summary** - mark CLAUDE.md complete, finalize PROJECT.md, summarize what shipped.

## Skill arguments

Parse arguments from the invocation (e.g., `/e2e --track deliverable build a Q3 sales analysis deck`). Four are supported:

- `--coverage <lines>/<branches>` - Phase 7 coverage-gate thresholds, **Build track only**. Default: `80/70`. Soft-fail (asks for direction, never silently advances). Ignored on the Deliverable track.
- `--track {build|deliverable}` - force the track instead of auto-detecting it in Phase 0.
- `--with-discovery` - force Phases 1 + 2 to run even on an existing project.
- `--skip-discovery` - skip Phases 1 + 2 even on a greenfield project.

Hold these in working memory through the run. If a value doesn't match the allowed set, surface it and ask. The remaining arguments after flags are the **target** - what the user wants built or produced. Pass it verbatim into Phase 1 (or, with `--skip-discovery`, into Phase 3 Elon).

## The end-of-phase ritual

Every phase from 1 through 11 finishes with the same five moves. Phase sections below just say "run the end-of-phase ritual (marker: `phase=<next>`)" plus anything extra:

1. **Flip status** - from Phase 5 on: set the phase's row in the Execution plan master table AND its detail block's `Status` line to `done` (both must agree), and fill the detail block's `Verification` block with the phase's evidence.
2. **Curate PROJECT.md** - reconcile per the Living-document discipline (*Current state* always; decisions superseded in place; answered questions deleted; milestone line in *Change log*; failures to *Lessons*; sweep).
3. **Bump the marker** - update CLAUDE.md's `<!-- e2e-state: ... -->` to the next phase (and step, in Phase 6), with a fresh `last_checkpoint` timestamp.
4. **Report the living-doc updates in one line.**
5. **Checkpoint and wait** - say what finished and what's next, offer the `/clear` reminder clause, and wait for the user's go.

---

## Phase 0: Bootstrap, resume detection & track classification

Before doing anything else, check whether this project already has e2e state.

1. Glob for `CLAUDE.md` at the project root. **`CLAUDE.md` is the primary resume signal** - it carries the `e2e-state` marker and exists from Phase 0 onward. Also Glob for `PLAN.md`, `RESEARCH.md`, `design-*.md`, `ceo-plan-*.md`, `PLAYTEST.md`: any of these marks a **legacy multi-file run** - resume it under its old layout (those files stay the trackers for the life of that run; do not migrate).
2. If `CLAUDE.md` exists, Read it and look for a line matching `<!-- e2e-state: phase=<X> step=<N> of=<M> track=<T> ... -->`.
3. If a state marker is found, follow `references/resume-protocol.md` to jump to the right phase and step. Tell the user "resuming from phase X, step N of M (track=T)" and wait for confirmation.
4. If `CLAUDE.md` exists but has no marker, ask: "Found CLAUDE.md without an e2e state marker. Treat as fresh start, or read it as context first?" (Legacy artifacts without CLAUDE.md: unusual - ask how to proceed.)
5. If no `CLAUDE.md` exists, check for **legacy discovery artifacts**:
   - `elon-*.md` exists -> Phases 1-3 implicitly done; resume Phase 4 (Research) under the legacy layout.
   - `ceo-plan-*.md` exists, no `elon-*.md` -> resume Phase 3 (Elon) under the legacy layout.
   - `design-*.md` exists, no `ceo-plan-*.md` -> resume Phase 2 (CEO Review) under the legacy layout.
   - None -> genuinely fresh run (consolidated layout). Decide discovery (Phases 1 + 2):
     - **Greenfield** (no `package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod` / `*.csproj`): default ON. Ask "Greenfield project - run Office Hours and CEO Review to validate the problem before Elon? (recommended)"
     - **Existing project**: default OFF - skip straight to Phase 3 (Elon), unless `--with-discovery` was passed.
     - `--skip-discovery` forces OFF regardless; `--with-discovery` forces ON regardless.

The manifest Glob above doubles as project-state detection for later phases: **greenfield** (none found) vs **existing**.

### Classify the track (Build vs Deliverable)

On a fresh run (or a resume whose marker lacks `track=`), set the track:

- If `--track` was passed, use it.
- Else infer: **Build** - a code manifest exists OR the target describes software (app, CLI, API, library, service, pipeline-as-code). **Deliverable** - the target describes a non-code artifact (analysis, deck, report, Power BI / dashboard, data model, document, research write-up).
- If ambiguous (e.g., "build a data pipeline"), ask once via `AskUserQuestion`: Build (software) or Deliverable (analysis / deck / report / BI / doc)?

The track governs Phases 6, 7, 9, and 11 and is written into the marker as `track=<build|deliverable>`.

### Stand up the living docs immediately (fresh runs only)

On any fresh run, create the two living docs **as soon as the discovery decision is known** - from the flags and project state when they decide it, otherwise from the user's answer to the discovery question (create the docs as the very first action after that answer, before any Phase 1 work). The project must be resumable from CLAUDE.md alone before discovery starts:

- **`CLAUDE.md`** - thin constitution from `references/claude-md-template.md`, marker set to the phase that runs next: `<!-- e2e-state: phase=<office-hours|elon> step=0 of=0 track=<build|deliverable> last_checkpoint=<ISO-8601 UTC> -->` (`office-hours` when discovery will run; `elon` when it won't). Fill the `<!-- live-document -->` block's Owner / Project / Dominant-rule slots from what the target already tells you.
- **`PROJECT.md`** - skeleton from `references/project-md-template.md`, filled with what's known (target, track, greenfield/existing). Unknown sections get `TBD (Phase N)` placeholders.

Do NOT write `## Execution plan` here - that stays a Phase 5 artifact. Update both files and bump the marker at the end of every phase from Phase 1 on (`office-hours` -> `ceo-review` -> `elon` -> `research` -> `ready-to-execute`). On a **resume**, these files already exist - skip creation and follow the resume protocol.

---

## Phase 1: Office Hours (conditional)

Before Elon cuts requirements, this phase establishes *which* requirements are real (adapted from gstack-office-hours by Key Ng Wu; for a Deliverable, "the product" is the artifact and "users" are its audience). Skip when `--skip-discovery` is set, the marker shows Phase 1 done, or (legacy) a `design-*.md` exists.

Follow `references/office-hours-protocol.md`: ask Startup vs Builder mode once, then the mode's forcing questions **one at a time** via `AskUserQuestion` (never batch), surface 2-3 premises for agree/disagree, produce **2-3 distinct approaches** (minimal viable / ideal / optional creative, each with effort, risk, pros, cons, reuses), and require the user to pick one. Distill the outcome straight into PROJECT.md per the protocol's distillation map (problem + success criteria -> *Goal*; wedge + constraints -> *Goal* / *Scope and non-goals*; chosen approach + one terse "considered X, rejected because Y" bullet per alternative -> *Decisions locked*; unresolved -> *Open questions*). No separate file.

Run the end-of-phase ritual (marker: `phase=ceo-review`). Checkpoint: "Phase 1 (Office Hours) complete, distilled into PROJECT.md. Move to Phase 2 (CEO Review)?"

---

## Phase 2: CEO Review (conditional)

Office Hours settled *what* the problem is; CEO Review asks *how ambitious* the solution should be (adapted from gstack-plan-ceo-review, scope-and-ambition only). Skip when `--skip-discovery` is set, the marker shows Phase 2 done, or (legacy) a `ceo-plan-*.md` exists.

Follow `references/ceo-review-protocol.md`: system audit (existing projects only), the Step 0 nuclear scope challenge with **mandatory alternatives**, mode selection via `AskUserQuestion` (EXPANSION / SELECTIVE EXPANSION / HOLD SCOPE / REDUCTION), mode-specific analysis with one `AskUserQuestion` per delight opportunity (never batch). Distill straight into PROJECT.md per the protocol's distillation map (mode + 10x vision -> *Goal* (the upper bound Elon cuts from); every In / Deferred / Skipped scope decision with its one-line why + reuses -> *Decisions locked*; "NOT in scope" with rationales -> *Scope and non-goals*; open items -> *Open questions*). No separate file.

Run the end-of-phase ritual (marker: `phase=elon`). Checkpoint: "Phase 2 (CEO) complete, distilled into PROJECT.md. Move to Phase 3 (Elon)?"

---

## Phase 3: Elon algorithm

Invoke the `elon` skill via the Skill tool with the target as input. `/elon` is interactive coaching (five steps, one turn at a time) and already works for non-code work - do not drive it autonomously; it needs real user input. If discovery ran, point it at PROJECT.md so it has the 10x vision to cut from:

```
Skill(skill: "elon", args: "<the target verbatim> - see PROJECT.md at the project root for the discovery context (goal, 10x vision, scope decisions); running inside an /e2e run: the outcome is folded into PROJECT.md silently at phase end - do not offer to save a separate document")
```

With discovery skipped, omit the PROJECT.md pointer clause but keep the running-inside-/e2e clause. The five-step outcome lives in the conversation and is folded into PROJECT.md silently at the end of this phase. Inside an e2e run `/elon` must NOT ask where to record the outcome or offer any chat-vs-document / `elon-*.md` choice - PROJECT.md is the only home; a personal `elon-*.md` copy is written only if the user asks for one unprompted (that file is a personal copy, never a tracker).

When `/elon` finishes: summarize the five-step outcome in 5-10 lines; fold it into PROJECT.md (deleted requirements -> *Scope and non-goals* with one-line whys; surviving requirements + simplifications -> *Decisions locked*; revisit-laters -> *Open questions*). Run the end-of-phase ritual (marker: `phase=research`). Checkpoint: "Phase 3 (Elon) complete, folded into PROJECT.md. Move to Phase 4 (Research)?"

---

## Phase 4: Research

Goal: understand the current state of the art so Phase 5 plans against reality, not training-data assumptions. The model's cutoff is older than today; even one search that surfaces "library X moved to v3 with breaking changes" or "this dataset was revised last quarter" can save the whole downstream plan.

1. **If existing project**: invoke `Skill(skill: "claude-mem:learn-codebase")` first. Skip for greenfield and pure Deliverable work with no codebase.
2. **Web research** with `WebSearch` (and `Context7` MCP if available), keyed off the Elon outputs:
   - **Build track:** latest stable versions of relevant frameworks, libraries, runtimes; common architecture patterns for this class of problem; database and storage options; known pitfalls, security considerations, deprecated approaches.
   - **Deliverable track:** the audience and what "good" looks like for them; format and presentation conventions; authoritative data sources and their freshness; domain facts, benchmarks, comparable examples; known failure modes (misleading charts, unsourced claims, stale data, double-counting).
3. **Synthesize** into PROJECT.md `## Research notes` using `references/research-template.md` (it carries both track shapes). Cite sources with URLs and access dates. No separate RESEARCH.md - findings that harden into decisions move to *Decisions locked* with their citation; the section keeps only still-load-bearing reference material.

Run the end-of-phase ritual (the marker stays `phase=research` until Phase 5 advances it). Checkpoint: present the research summary and ask "Move to Phase 5 (Plan)?"

---

## Phase 5: Plan with ultrathink depth

This is the highest-leverage phase. A bad plan is far cheaper to fix here than in Phase 6. Apply maximum reasoning effort.

**Reason at ultrathink depth before writing the plan:**
- List at least three plausible architectural / structural alternatives (Deliverable: three ways to structure the analysis, narrative, or data model).
- Score each against the discovery + Elon outcomes in PROJECT.md and the `## Research notes` findings.
- Identify the smallest viable slice - the minimum set of steps that delivers real value.
- **Pre-mortem:** imagine it's 6 to 12 months out and this shipped but failed - what is the single most likely reason, and is there a cheap thing to do now to prevent it? Route the answer into *Open questions* (a live risk) or *Decisions locked* (an adopted mitigation).
- Only then commit to one approach.

**Expand the living docs and add the execution tracker** (the two files already exist from Phase 0):

1. **`PROJECT.md`** - expand the skeleton into the full living source of truth (template: `references/project-md-template.md`), filling every `TBD` from the discovery, Elon, and Research content already in the file. For Build, *Decisions locked* also records the conventions: languages, test framework, code style.
2. **`CLAUDE.md`** - finalize the thin constitution (template: `references/claude-md-template.md`): workflow contract, Files of note, and the live-document bootstrap block complete and accurate; ~one screen. Advance the marker to `<!-- e2e-state: phase=ready-to-execute step=1 of=<N> track=<T> last_checkpoint=<ISO-8601 UTC> -->`.
3. **`## Execution plan`** - write from `references/plan-template.md`. Enumerate every step (typically 3-8); each declares what it implements or produces, dependencies, **validation strategy** (Build: which automated tests + what manual verification; Deliverable: which acceptance checks - numbers reconcile, claims cited, one idea per slide, measure returns the expected value - + manual verification), and definition of done. For a Deliverable, a "step" is a section or component of the artifact.

**Scaffold the full twelve-phase workflow, not just the implementation steps:** the section contains ONE master status table with a row for every phase 1-12 AND a sub-numbered row per Phase 6 step (6.1, 6.2, ...). Phases 1-5 marked `done`; 7-12 `pending` with their checklists scaffolded inline. This is the single source of truth for "where are we?" - do not maintain a separate steps table.

**Strong checkpoint here** (heaviest context point in the run). Tell the user verbatim:

> Phase 5 complete. PROJECT.md (goal, decisions, research notes, execution plan) and CLAUDE.md are written. **You can `/clear` now if context is heavy** - when you re-invoke `/e2e` in this directory, I'll detect the state marker in CLAUDE.md and resume from Phase 6 step 1. Or say "continue" to push through without clearing.

Wait for "continue" or `/clear`+re-invocation.

---

## Phase 6: Execute (looped, gated per step)

For each step in the Execution plan (legacy runs: PLAN.md), in order:

1. **Implement / produce** this step only (Build: the code; Deliverable: the section/component). Do not start step N+1 work.
2. **Write the validation.** Build: automated tests in the project's framework (greenfield: pick a sensible default and record it in PROJECT.md). Deliverable: run this step's acceptance checks.
3. **Run until green / clean.** Fix failures by addressing root causes - never silence failing tests, weaken assertions, or fix the check instead of the artifact.
4. **Manual verification.** Exercise the result end-to-end against the step's definition of done. UI changes: a Playwright screenshot or a described observation. Deck/report: read the section as the audience would.
5. Run the end-of-phase ritual for the step (marker: `phase=execute step=<N+1> of=<M>`; the master-table row AND detail block flip to `done` with a short outcome note, e.g. "56 tests, 1.5s", plus a fuller `Verification (<date>):` block in the detail section). Checkpoint: "Step N of M complete: <one-line summary>. Move to step N+1?"

If a step uncovers something the plan got wrong, **edit the Execution plan** (and note it in *Lessons* / *Change log*) before moving on. The plan is a living document, not a frozen contract.

When all steps are done, advance to Phase 7.

---

## Phase 7: Holistic quality pass

Per-step validation proves each piece works in isolation. This phase proves they work together.

**Build track:**
1. Run the full test suite from the project root.
2. **Measure coverage** with the project's tool (`vitest --coverage`, `pytest --cov`, `go test -coverprofile`, `cargo llvm-cov`, ...). Detect it from PROJECT.md's test-framework decision + the manifest; ask if ambiguous.
3. **Apply the coverage gate** against `--coverage` (default `80/70`). At or above both thresholds: advance silently. Below either: surface the gap (which files/functions/branches) and ask verbatim: *"Coverage L%/B% below target (lines/branches). Add tests, lower the threshold for this project, or accept as-is and continue?"* **Soft-fail** - never silently advance, never block the user against their will.
4. Smoke-test the integrated product: launch it, exercise the main flows declared in the PROJECT.md goal.

**Deliverable track:**
1. Review the **whole artifact** against PROJECT.md's success criteria and every step's acceptance checks.
2. Check cross-section consistency: no contradictions, numbers reconcile end-to-end (slide 9's total matches slide 4's table), terminology and narrative consistent.
3. Any unmet criterion: surface the gap and ask the same soft-fail question (fix, drop the criterion, or accept).
4. Full read-through / dry-run as the audience would.

Both tracks: if anything regresses, fix it, update the plan and canonical sections, re-run. Then run the end-of-phase ritual (marker: `phase=human-playtest`; Verification block gets Build: suite size, pass count, coverage L%/B%, smoke summary; Deliverable: criteria checked, consistency findings, read-through result). Checkpoint (Build): "Full suite green, coverage at L%/B% (target T_L%/T_B%), smoke test passing. Move to Phase 8 (Human review)?" (Deliverable): "Whole-artifact review complete, all success criteria met, end-to-end consistent. Move to Phase 8 (Human review)?"

---

## Phase 8: Human review & feedback (mandatory before the critical review)

Phase 7 asks "does it do what the plan said?" Phase 8 asks "is what the plan said actually any good?" - readability, pacing, persuasiveness, frustration points, the squishy stuff no automated check catches. Skipping it means the expensive critical review goes hard on a build the user has not yet validated.

1. **Detect surface.**
   - **Web frontend present** (Glob for `package.json` containing React/Vue/Svelte/Next/Vite/Angular, or `*.html`, or `src/components/`, `app/`, `pages/`) -> add a **`#### Playtest checklist`** under the Execution plan's Phase 8 detail block, from `references/playtest-template.md`, one row per major user-facing flow (from the PROJECT.md goal + success criteria).
   - **Deliverable** -> same, using the template's Deliverable variant: one row per major claim, section, chart, or flow the audience will hit.
   - **No surface to walk** (library, trivial-output CLI) -> skip the checklist; tell the user verbally what to exercise and collect feedback as free text.
2. **Hand off to user:** *"Phase 7 green. Please exercise / read the product end to end. Mark each checklist row `OK`, `nit: ...`, `annoying: ...`, or `blocker: ...` - in the file or right here in chat. Bring it back when done."* This hand-off is always a real handoff: also write the Next Actions file pair (per the Communication format) walking the user through exercising the product and marking the rows.
3. **Triage feedback:** `blocker` (crashes, core flow broken, objectively wrong) -> must fix. `annoying` (works but tedious / confusing / unconvincing) -> must fix. `nit` (minor polish) -> log for Phase 11. `out-of-scope` -> log + reject in writing.
4. **Apply fixes:** for every blocker and annoying item, fix, re-run the Phase 7 routine for the track, confirm no regression, re-walk only the affected rows.
5. Run the end-of-phase ritual (marker: `phase=critical-review`; legacy `phase=codex-review` markers still parse on resume). Extra: the Verification block records triage counts, one line per applied fix, and the post-fix Phase 7 result - then **delete the Playtest checklist subsection** (its outcome now lives in the Verification block). Checkpoint: *"Phase 8 done - N blocker fixes, M annoying fixes, K nits logged for Phase 11. Move to Phase 9 (review)?"*

**Hard rule:** do not advance to Phase 9 with any `blocker` or `annoying` row open.

---

## Phase 9: Critical review (deep, read-only)

**Precondition:** Phase 8 is `done` with no open `blocker` / `annoying` rows.

Spawn a **read-only Claude reviewer subagent** for a deep, independent pass - fresh eyes catch what the builder's own context glosses over. No external CLI. The reviewer **surfaces findings only**; fixes are applied by you, after the user picks them:

- **Build track - code review.** Spawn `superpowers:code-reviewer` (or `general-purpose` if unavailable): reviews the source against PROJECT.md (goal, decisions locked, Execution plan) for bugs, security issues, design problems, plan deviations, code-quality concerns.
- **Deliverable track - critical-reasoning review.** Spawn a `general-purpose` agent with the critical lens: flaws in logic, unsupported or overstated claims, weak evidence, statistical/analytical errors, misleading visuals, structural and clarity problems, scope deviations. It reads the artifacts directly; for tool artifacts it cannot open (a `.pbix`, a binary deck), export the substance to text first - or run the critical pass inline yourself in max-thinking mode.

Instruct the reviewer to be **read-only** (report, do not edit) and to group findings by severity (critical / important / nit) with file:line or section references. Exact prompt structures: `references/critical-review-protocol.md`.

When findings come back: present them grouped by severity; ask the user which to fix (never auto-apply); apply approved fixes one by one; re-run the full Phase 7 routine. Run the end-of-phase ritual (marker: `phase=playwright`; Verification block: reviewer used, findings by severity, count applied, one line per applied fix). Record declined findings in *Decisions locked* (one terse bullet each) so future runs don't re-flag them. Checkpoint: "Critical review applied (X fixes). Move to Phase 10 (Playwright)?"

---

## Phase 10: Playwright UI testing (conditional)

Detect a web frontend (same Glob signals as Phase 8). None (most Deliverable runs, code with no UI): print "No web frontend detected - skipping Playwright phase" and advance to Phase 11. Found: ask "Frontend detected at `<path>` - run Playwright UI tests?" and wait.

If yes, follow `references/playwright-protocol.md`: launch the dev server in the background, drive the browser via the Playwright MCP tools, exercise the golden path from the Execution plan's success criteria plus the protocol's five edge cases, check the accessibility tree on every page, watch console health, report findings, fix what's found and re-run the affected flows.

Run the end-of-phase ritual (marker: `phase=simplify`; status may be `skipped - no web frontend`). Checkpoint: "Playwright phase done (or skipped). Move to Phase 11 (Simplification / tighten)?"

---

## Phase 11: Simplification / tighten

Implementation phases leave dead code, half-finished abstractions, redundant slides, unsupported tangents. Clean them up - and prove nothing breaks.

**Build track:** invoke `Skill(skill: "simplify")`, then **re-run the full Phase 7 routine** (suite + coverage gate) plus the key Playwright flows if applicable. If anything broke, the simplification went too far - back out the offending changes and re-run.

**Deliverable track:** tighten/refine - cut redundancy and filler, sharpen prose, drop sections that don't earn their place, simplify the data model or measure set, remove any claim not backed by evidence. Then **re-run the affected acceptance checks and the Phase 7 consistency review**. If something load-bearing was dropped, restore it and re-check.

Run the end-of-phase ritual (marker: `phase=final`; Verification block: what was simplified/tightened + post-pass result). Checkpoint: "Simplification / tighten done, everything still passes. Move to Phase 12 (final summary)?"

---

## Phase 12: Final verification & summary

1. Update the CLAUDE.md marker to `<!-- e2e-state: phase=complete track=<T> -->` and add a "Shipped" section listing what got built/produced and the date.
2. **Retire the Execution plan section.** Fold its outcome into the canonical sections (shipped summary + final validation -> *Change log* milestone line and *Current state*; step-level lessons -> *Lessons*), then **delete the entire `## Execution plan` section**. A completed run's step table is dead weight. (Legacy runs: fill PLAN.md's Outcome paragraph and mark all rows `done` instead - do not delete their PLAN.md.)
3. **Compact `## Research notes`** to only the findings still load-bearing for future work (with citations); delete findings that only justified now-locked decisions (those are already cited there).
4. Finalize **PROJECT.md** with a full curation sweep: *Current state* set to the shipped state and next action (or "complete - no further action"); decisions, change log, and lessons reflect the whole run; merge duplicates, collapse the log to milestones, delete every resolved *Open question*. The standing test must hold: a fresh agent reading only PROJECT.md can continue without re-explanation.
5. Print a tight summary: what shipped, validation passing (Build: tests + coverage; Deliverable: criteria met + consistency), review fixes applied, simplification clean. One paragraph max.

The skill is done. Exactly two docs (`PROJECT.md`, `CLAUDE.md`) remain, and PROJECT.md keeps maintaining itself under the `/live-document` bootstrap for the life of the project.

---

## Resume protocol (quick reference)

If invoked in a project where CLAUDE.md contains an e2e-state marker, jump straight to that phase/step. Full details in `references/resume-protocol.md`. The TL;DR: the marker is the source of truth (including `track=`); trust it, read CLAUDE.md + PROJECT.md (legacy runs: also PLAN.md and the old artifact files), summarize what's been done, and continue from where it left off.

## When something goes wrong

- **Reviewer subagent unavailable:** run the Phase 9 critical review inline yourself in max-thinking mode - same severity-grouped output, same read-only-then-user-approves discipline. No external CLI is ever required.
- **Playwright MCP not available:** tell the user, ask whether to skip Phase 10 or install (`npx @playwright/mcp@latest`).
- **Tests / checks are flaky:** do not retry blindly. Investigate the root cause before deciding whether the test (or the check) or the work is wrong.
- **A phase reveals the plan was wrong:** edit the Execution plan, note it in *Lessons* / *Change log*, then continue. Don't pretend nothing changed.
- **Coverage tool not detectable (Build):** ask the user. Common: vitest (`--coverage`), jest (`--coverage`), pytest (`--cov` via pytest-cov), go (`go test -coverprofile`), cargo (`cargo llvm-cov` or `cargo tarpaulin`). Document the choice in PROJECT.md.
- **Track was misclassified:** tell the user, switch the `track=` field in the marker, adapt Phases 6/7/9/11 from that point. Don't restart.
- **Legacy layout or numbering:** projects with a PLAN.md (or `design-*.md` / `ceo-plan-*.md` / `RESEARCH.md` / `PLAYTEST.md`) keep the old multi-file layout for the life of the run; projects on the older 10-phase numbering keep their numbering for life (the phase-name enum is a superset, so old markers still parse). A missing `track=` means `build`. Only a fresh `/e2e` run uses the consolidated two-file layout and 1-12 numbering.

## What this skill is NOT

- It is not a quick-build tool - it deliberately trades speed for rigor.
- It is not code-only - the Deliverable track runs analyses, decks, reports, dashboards, and documents through the same rigor.
- It does not commit to git, push, or open PRs unless the user asks separately.
- It does not auto-apply review findings - that is always user-directed.
- It does not skip checkpoints under any circumstance, even when "everything looks fine".
