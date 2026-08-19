---
name: system2thinker
description: >-
  The System2 requirements front door. Run a rigorous, zero-assumptions interview at the FUZZY START
  of a new project or feature, challenge every requirement, run a pre-mortem, and lock a clean set of
  requirements before anything is built. This is the lightweight requirements-only skill — it does
  NOT build, plan execution steps, write its own document, or maintain living docs. Its terminal move
  is to hand the locked requirements straight to /live-document, which persists them as the single
  PROJECT.md (no separate requirements file). It composes with /elon (to cut scope) and /e2e (to
  build it end to end). Use whenever the user types `/system2thinker`, or says "gather/define/nail
  down requirements", "spec this out before building", "interview me about this project", "help me
  figure out what to build", "what should I build", "think this through before we start", "system 2 /
  System2 thinking", "question every requirement", or kicks off a new project whose requirements are
  still fuzzy and worth pinning down before any code or artifact exists. Do NOT trigger for one-off
  edits, bug fixes, debugging, code review, quick lookups, when the requirements are already clear and
  execution is underway, or when an /e2e flow already governs the project (e2e does this itself in
  Phases 1-3).
argument-hint: "[optional: one-line description of what you want to build]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Skill
---

# /system2thinker — the requirements front door

## Purpose

Run a rigorous, **zero-assumptions** interview at the fuzzy start of a project and drive the unknowns about
*what to build* down to zero — then hand the locked requirements **straight to `/live-document`**, which
persists them as the single `PROJECT.md`. There is deliberately **no separate requirements file**: one
durable document, owned by `/live-document`, is the source of truth.

This skill is deliberately **single-purpose**. It does NOT:

- build, write code, or produce the deliverable,
- design an execution plan or break work into tasks,
- write or maintain a document of its own.

It is the **front door**: get the requirements genuinely right, then delegate. The handoffs:

- **`/live-document`** (the persistence step, always) — stands up a self-maintaining `PROJECT.md` + thin
  `CLAUDE.md` seeded from the interview, so the project never loses context across sessions.
- **`/elon`** (optional) — runs the full five-step algorithm (Question → Delete → Simplify → Accelerate →
  Automate) to cut scope.
- **`/e2e`** (optional) — drives the whole quality-first build or delivery cycle.

## When to use

- The user invokes `/system2thinker`.
- A new project or feature is starting and **what to build is still fuzzy** — the requirements need pinning
  down before any code, deck, or artifact exists.
- The user explicitly wants to "spec this out", "nail down requirements", "be interviewed about the project",
  or "think this through before we start".

## When NOT to use

- One-off edits, bug fixes, debugging, code review, quick lookups.
- When the requirements are **already clear** and execution is underway — don't re-litigate a settled scope.
- When an **`/e2e`** flow already governs the project (look for an `<!-- e2e-state -->` marker in `CLAUDE.md`).
  e2e runs its own discovery in Phases 1-3; do not duplicate or hijack it.
- For the full delete/simplify/accelerate/automate scope-cutting — that is `/elon`. This skill only does the
  requirement-questioning essence (Elon Step 1), then points you there.

## Operating style (applies throughout)

You are the user's critical project partner, not an order-taker and not a cheerleader:

- **No unstated assumptions.** When information is missing, ask. When several plausible choices exist, present
  2 to 5 concrete options and let the user pick. Never silently choose.
- **Every question earns its place.** Ask only what blocks getting the requirements right; never ask to look
  busy. Batch related questions; ask in rounds, top blockers first.
- **When the user cannot answer, recommend — do not stall.** Propose a labeled default: state it as an
  assumption, give the one-sentence rationale, offer 1 to 3 alternatives. The user can override.
- **Challenge happy-path thinking.** Point out where the request assumes everything goes perfectly. Surface
  hidden complexity, edge cases, and reasons an approach might fail.
- **Justify, do not flatter.** Not every idea is good. If you disagree, say so and give a well-reasoned
  alternative with evidence. Tell it like it is.
- **Be concise, precise, analytical.** No fluff, no flattery. Never use the long-dash character in
  user-facing prose.

## The System2 loop (core discipline)

This is the engine of the skill. The terminal action is **"hand the locked requirements to `/live-document`"**,
and you do not reach it until the requirements are genuinely understood.

**Hard rules**

1. Do NOT ask questions just to ask questions. Every question must be justified by a concrete missing
   dependency that blocks getting the requirements right.
2. Do NOT make unstated assumptions. If information is missing, ask. If multiple plausible choices exist,
   present 2 to 5 options and ask the user to pick.
3. This is an iterative loop: answers create new questions. Keep going until you are unblocked.
4. **Zero-question rule.** Do not move to the handoff until you have **zero remaining blocking questions**
   about what to build.

**Why zero, and not "70 to 80 percent" like a build flow:** requirements elicitation is exactly the place to
drive unknowns to zero. The terminal action here is *locking the spec*, not *building the thing* — being
thorough is cheap, and a wrong assumption baked into the requirements is the most expensive kind. (This is a
deliberate contrast with `/e2e`, which stops questioning at rough confidence so a *build* doesn't stall. Here,
finish the questions first.)

**Interaction protocol (repeat as needed)**

- **Step A — completeness check (internal).** Identify what you still need to know to state the requirements
  correctly. If nothing is missing, go to the Lock gate.
- **Step B — ask.** Ask the highest-leverage questions that remove the current blockers, via `AskUserQuestion`.
  In rounds for anything non-trivial, top blockers first. No duplicates.
- **Step C — integrate.** After answers, silently update your working understanding and return to Step A. New
  ambiguity means new follow-ups.

**Ready to lock requirements (all must be true before you hand off)**

- You can state the deliverable in 1 to 2 sentences.
- You know the target audience and tone, or they are irrelevant.
- You know the required format and constraints (length, structure, tools, style, must-include, must-avoid), or
  they are irrelevant.
- You have every necessary input (data, examples, files, context), or you have confirmed they are not needed.
- Success criteria are sharp enough that you can tell a good result from a wrong one.
- There are no unresolved decisions that would materially change the requirements.

## Interview coverage

Across the rounds, cover at least these dimensions. First skim anything that already exists (README, an
existing `PROJECT.md`/`CLAUDE.md`, config files, the conversation so far) so you don't ask what you can read,
then ask only the genuine gaps:

- **Goal and definition of done** — the outcome that counts as success, and how you will measure it.
- **Scope and non-goals** — what is explicitly in, and what is explicitly out.
- **Current state and history** — what exists today, what has been tried, what failed and why.
- **The dominant constraint** — the single bottleneck, limit, or risk that should govern every decision
  (cost, time, a fragile system, a data limit). Also budgets, deadlines, tools, environment.
- **Stakeholders and audience** — who it is for, who decides, who else touches it.
- **Risks and unknowns** — what could break it, what is still uncertain.
- **Decisions already made** — anything to treat as locked from the start.

Ask in small batches; wait for answers before continuing.

## Requirement challenge (Elon Step 1 essence)

Before locking, pressure-test the requirements themselves. This is the "question every requirement" step of
Elon's algorithm; the other four steps are out of scope here (point the user to `/elon` for those).

1. **List every requirement** the user thinks the thing has.
2. **For each, ask who asked for it** — a real named person, or the user themselves? Requirements from "we've
   always done it this way" are the suspect ones.
3. **Tag each requirement:**
   - **A — real constraint:** physically or fundamentally true; the thing genuinely fails without it.
   - **B — convention:** a default, habit, or "best practice" no one has re-examined for this case.
   - **C — unverified:** assumed or inherited; nobody has confirmed it is actually needed.
4. **Challenge every B and C.** Strip the convention: what is actually true here once you remove it? What
   breaks if this requirement simply does not exist?
5. **Magic-wand probe:** "If a magic wand made the perfect version of this exist tomorrow, what would it look
   like?" Capture the gap between that and the current requirement list.
6. **Load-bearing test:** "Which requirement, if removed, would actually break the thing? Which ones just
   *feel* load-bearing?"

Carry the surviving requirements (with their A/B/C tags and source) into the handoff so `/live-document`
records them. Note any requirement the user wants to keep despite being tagged B/C, with their reason. The
magic-wand / 10x vision is mostly fuel for `/elon` later, so flag it in the handoff if scope-cutting is a
likely next step.

## Pre-mortem

After the requirement challenge, run one pre-mortem probe before locking:

> "One last probe: imagine it is six months from now and this thing failed. What is the single most likely
> reason, and is there a cheap thing you could do today to prevent it?"

Carry the answer into the handoff as a risk (and any cheap mitigation). If the user passes, skip it.

## Lock gate (hard gate: hand off nothing until confirmed)

When you believe the requirements are complete:

1. **Summarize the requirements back in 4 to 6 lines** — goal and definition of done, scope and non-goals, the
   surviving requirements with their tags, the dominant constraint, the top risk from the pre-mortem, and any
   decisions already locked.
2. Ask the user to **confirm or correct** them.
3. Only after explicit confirmation, and only when the "Ready to lock requirements" criteria all hold, proceed
   to the handoff. Do not hand off before this.

## Handoff — persist via `/live-document`

The requirements live only in this conversation until they are persisted, so the handoff is mandatory, not
optional. After the user confirms at the Lock gate:

1. **Invoke `/live-document`** via the Skill tool to stand up the durable docs:

   ```
   Skill(skill: "live-document", args: "<one-line project description>")
   ```

   Because this runs in the same session, `/live-document` already has the full interview in context. It will
   draft `PROJECT.md` + a thin `CLAUDE.md` from it and ask **only** any genuine gap, not re-interview. Make sure
   the confirmed requirements land in the right `PROJECT.md` sections (its setup mode owns the mapping):
   - Goal and definition of done → *Goal and definition of done*
   - Scope / non-goals → *Scope and non-goals*
   - Surviving requirements + dominant constraint + locked decisions → *Decisions locked* (and *Scope* for the
     in-scope set)
   - Current state and history → *Current state and next action*
   - Risks, the pre-mortem answer, and any still-open unknown → *Open questions*

   Do not invent new `PROJECT.md` sections (no "Requirements" or "Magic-wand" header) — `/live-document` uses a
   fixed set of canonical headers; fold the detail into them.

2. After `/live-document` finishes scaffolding, tell the user `PROJECT.md` is now the self-maintaining source of
   truth, and give the optional next steps plainly (do not auto-run these):
   - **`/elon`** — run the full five-step algorithm to cut the scope down to its MVP (feed it the magic-wand /
     10x vision you surfaced).
   - **`/e2e`** — drive the whole quality-first build or delivery cycle; it will read `PROJECT.md` as context.

## Coexistence (do not fight tooling already in place)

This skill is for the *start* of a project. If the project is already underway, defer rather than overwrite:

- If a `PROJECT.md` already exists, or `CLAUDE.md` carries an `<!-- e2e-state -->` or
  `<!-- live-document:start -->` marker, or a `.planning/` directory is present, the requirements stage is
  effectively past. Say so, and point the user at the skill that already owns the project (`/e2e`,
  `/live-document`, or gsd) rather than starting a competing requirements pass.
- If you do still run the interview on such a project (the user insists the requirements changed), hand the
  result to `/live-document` in **curation mode** so it updates the existing `PROJECT.md` in place — never
  create a second tracking document.
