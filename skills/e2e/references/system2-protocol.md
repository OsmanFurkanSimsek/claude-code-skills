# System2 Protocol - requirement lock inside an e2e run

Folded into e2e from the retired `system2thinker` skill (2026-09-13). e2e's Working style already
carries the operating rules (no unstated assumptions, every question earns its place, recommend
instead of stalling, challenge the happy path, justify instead of flatter). This file holds the
parts only the requirements front door had: the zero-question rule for the lock stage, the
interview dimensions, the requirement challenge, the pre-mortem probe and the lock gate. Phase 1
(Office Hours) uses the interview coverage; Phase 3 (Elon) runs the challenge, the pre-mortem and
the lock gate; a run with `--skip-discovery` does all of it in Phase 3.

## Two confidence bars

- **Requirement lock (Phases 1-3):** drive blocking questions about *what to build* to **zero**.
  Locking a spec is cheap to do thoroughly, and a wrong assumption baked into the requirements is
  the most expensive kind of mistake. Do not leave Phase 3 with a blocking question open.
- **Execution (Phase 4 on):** iterate until roughly 70 to 80 percent confident, then act. A build
  must not stall on questions that only execution can answer.

## Hard rules while locking

1. Do NOT ask questions just to ask questions. Every question must be justified by a concrete
   missing dependency that blocks getting the requirements right.
2. Do NOT make unstated assumptions. If information is missing, ask. If several plausible choices
   exist, present 2 to 5 options and let the user pick.
3. It is an iterative loop: answers create new questions. Keep going until unblocked.
4. Zero-question rule: no lock, and no Phase 4, until zero blocking questions remain.

## Interaction loop (repeat as needed)

- **Step A - completeness check (internal).** Identify what you still need to know to state the
  requirements correctly. If nothing is missing, go to the Lock gate.
- **Step B - ask.** The highest-leverage questions that remove the current blockers, via
  `AskUserQuestion`, in the *Question rounds* shape from SKILL.md (numbered, each with a
  recommended answer), top blockers first, no duplicates. Facts are your job (look them up);
  decisions are the user's.
- **Step C - integrate.** After answers, silently update the working understanding and PROJECT.md,
  then return to Step A. New ambiguity means new follow-ups.
- **When the user cannot answer**, recommend: a labeled assumption, its one-sentence rationale,
  1 to 3 alternatives. When the answer sits with a third person, write the questionnaire
  (`references/questionnaire-template.md`) and proceed on labeled assumptions.

## Interview coverage (Phase 1, or Phase 3 when discovery was skipped)

First skim what already exists (README, an existing `PROJECT.md` / `CLAUDE.md`, config files, the
conversation so far) so you never ask what you can read. Then cover at least these dimensions and
ask only the genuine gaps, in small batches:

- **Goal and definition of done** - the outcome that counts as success, and how it is measured.
- **Scope and non-goals** - what is explicitly in, and what is explicitly out.
- **Current state and history** - what exists today, what was tried, what failed and why.
- **The dominant constraint** - the single bottleneck, limit or risk that should govern every
  decision (cost, time, a fragile system, a data limit); also budgets, deadlines, tools, environment.
  It fills the `Dominant-rule` slot of the CLAUDE.md live-document block.
- **Stakeholders and audience** - who it is for, who decides, who else touches it.
- **Risks and unknowns** - what could break it, what is still uncertain.
- **Decisions already made** - anything to treat as locked from the start.

Distill each answer straight into PROJECT.md (goal and success criteria -> *Goal and definition
of done*; scope -> *Scope and non-goals*; decisions already made and the dominant constraint ->
*Decisions locked*; current state -> *Current state and next action*; unknowns -> *Open questions*).

## Requirement challenge (Phase 3, Step 1 of the algorithm)

The "question every requirement" step of `references/elon-algorithm.md`, run before anything is
deleted or simplified:

1. **List every requirement** the user thinks the thing has.
2. **Ask who asked for each one** - a real named person, or the user? "We have always done it this
   way" requirements are the suspect ones.
3. **Tag each requirement:** **A** real constraint (physically, legally or contractually true; the
   thing fails without it) / **B** convention (a default or "best practice" nobody re-examined for
   this case) / **C** unverified (assumed or inherited; nobody confirmed it is needed).
4. **Challenge every B and C.** Strip the convention: what is actually true here once it is
   removed? What breaks if the requirement simply does not exist?
5. **Magic-wand probe:** "If a magic wand made the perfect version of this exist tomorrow, what
   would it look like?" The gap between that and the requirement list is the optimization space
   (with discovery, the CEO Review's 10x vision already holds this).
6. **Load-bearing test:** "Which requirement, if removed, would actually break the thing? Which
   ones just feel load-bearing?"

Surviving requirements keep their A/B/C tag and source into *Decisions locked*; a B or C the user
keeps anyway is recorded with the reason.

## Pre-mortem probe (Phase 3, after the five steps)

One question before locking:

> "One last probe: imagine it is six months from now and this thing failed. What is the single most
> likely reason, and is there a cheap thing you could do today to prevent it?"

The answer goes to *Open questions* as a risk with its cheap mitigation, or to *Decisions locked*
if it settles something now. Skip it if the user passes. (Phase 5 runs a second, plan-level
pre-mortem against the execution plan; that one is not a duplicate of this.)

## Lock gate (hard gate: Phase 4 starts only after confirmation)

When you believe the requirements are complete:

1. **Read them back in 4 to 6 lines** - goal and definition of done, scope and non-goals, the
   surviving requirements with their tags, the dominant constraint, the top risk from the
   pre-mortem, and the decisions already locked.
2. Ask the user to **confirm or correct** them.
3. Proceed only after explicit confirmation AND when every "ready to lock" criterion holds:
   - The deliverable can be stated in 1 to 2 sentences.
   - Target audience and tone are known, or irrelevant.
   - Required format and constraints (length, structure, tools, style, must-include, must-avoid)
     are known, or irrelevant.
   - Every necessary input (data, examples, files, context) is in hand, or confirmed not needed.
   - Success criteria are sharp enough to tell a good result from a wrong one.
   - No unresolved decision would materially change the requirements.

The confirmed read-back is what Phase 3 folds into PROJECT.md before its end-of-phase ritual.
