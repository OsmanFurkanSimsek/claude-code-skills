---
name: big-project
description: Use when the owner types /big-project, or is starting or resuming a substantial multi-session project and wants it run the way he likes to work - "set this up the way I like", "run this like my big projects", "my usual way of working", "apply my working style". Applies the owner's durable working-style profile (Summary/Why/What-you-should-do answer format; the two-step context-handoff block that ends a completing reply past 30% context or when work is done; no unilateral owner decisions; one dated HTML Next Actions walkthrough per handoff, never a .md twin; numbered one-action steps; versioned code + full QA; predict-run-duration; save-feedback-to-memory same turn; validate-in-a-playground first; the agent does what its tools reach and reports after). Composes with live-document (PROJECT.md + CLAUDE.md), session-handoff (clear-time summary), and e2e (full rigor), and DELEGATES their machinery instead of re-implementing it. Do NOT use for one-off edits, bug fixes, quick lookups, or a single small change.
---

# big-project

## What this is

A **personal working-style layer**. Invoking `/big-project` makes the current project run the way the owner likes his big projects to run. It is deliberately thin: its whole substance is one portable profile of the owner's durable preferences (`references/preferences.md`), which it injects into the project and enforces every session.

**It composes; it never reinvents.** Keeping a living document, getting ready to `/clear`, and handing off to the next agent are already solved by skills the owner has. `big-project` delegates those:

- `live-document` owns `PROJECT.md` + the thin `CLAUDE.md` + the `project-memory/` detail folder and their reconcile-not-append discipline.
- `session-handoff` owns the heavy chat-only end-of-session summary.
- `e2e` owns the full twelve-phase rigor when the owner wants it (they coexist; the profile still applies).

`big-project` adds the one thing none of them carry: **how the owner personally likes to work**, as a reusable profile that any project can inherit.

## The profile lives in `references/preferences.md`

That file is the single home for the owner's portable rules. It is **domain-free on purpose**: tool-, data-, and model-specific rules (a particular cloud, a particular BI tool, a particular LLM) stay in the project's own `PROJECT.md` / `CLAUDE.md`, never in this skill. That is what makes the skill reusable across any kind of big project, not just one.

Read `references/preferences.md` in full at the start of every `big-project` session and follow every rule in it.

## Setup flow (on invocation)

1. **Detect the project's doc state.** Read the root `CLAUDE.md` and look for a `<!-- live-document:start -->` block or an `<!-- e2e-state ... -->` marker.
2. **Stand up the doc plumbing if missing (delegate, do not build):**
   - No living doc and the owner wants full rigor -> tell him `/e2e` is the heavier path and let him choose; the profile still applies on top.
   - No living doc, normal path -> invoke `Skill(live-document)` to scaffold `PROJECT.md` + the thin `CLAUDE.md` + `project-memory/`. Do not write those files yourself.
   - Living doc already present -> layer on top only; touch nothing the `live-document` or `e2e` marker owns.
3. **Inject the owner's delta into the project `CLAUDE.md`.** Apply the hard-rules bullets and the two-step handoff block from `references/claude-md-injection.md` into the project's hard-rules list. **Insert only what is absent** - `live-document` already carries ask-before-assuming, Summary/Reasoning/Steps, the single Next Actions HTML file, tidy-root, and no-long-dash, so never duplicate those. Re-running the skill self-heals: it adds only missing rules.
4. **Announce** in one line what was injected, then follow the profile for the rest of the session.

## Always-on enforcement (short list; full list in `references/preferences.md`)

- **Answer format:** Summary, then Why, then What you should do LAST - numbered, one action per line. Nothing to do -> say so plainly.
  The `answer-format` skill is the full version of this one rule (live step lists that survive follow-up questions, worked examples,
  desktop setup). If it is installed, invoke it and let it own reply shape; this skill keeps owning everything else. Its handoff note
  matters: the two-step context-handoff block below goes INSIDE the numbered actions as the final steps, never appended after them.
  If a user-level rule in `~/.claude/rules/` defines a structure for open decisions, that rule
  outranks both this bullet and `answer-format` for those replies; everything else is unchanged.
- **End a completing reply, past about 30% context or when the work is done, with the two-step context-handoff block**: (1) you can clear the context now, everything is in PROJECT.md; (2) then just type `continue`. First make PROJECT.md's next action self-sufficient, because it replaces the old paste-ready kickoff message (owner, 2026-09-27: no long text to copy). A bare `continue` in a fresh session means: read PROJECT.md in full and carry out that next action without asking. This is the owner's signature rule; honor it literally at those points. Below about 30% with work left, keep working instead (`references/preferences.md` section 2).
- **Wrap-up past 30% context** (the context-budget hook announces it): from then on the aim is to stop as soon as stopping loses nothing. Not a hard stop and no stop line: you decide the point. Finish the step you are on in full (never skip or thin out a detail), start no new planned step, write everything a fresh agent needs into PROJECT.md, check that nothing still runs, then end the turn with the handoff block. About 50% is a guide, not a wall. Full rule: `references/preferences.md` section 2a.
- **No unilateral owner decisions.** Names, write targets, and whether-to-create-something are the owner's call. Propose 2-5 options with trade-offs and ask.
- **Predict run duration** before any long or expensive run; record the measured actual afterward.
- **Save feedback to memory the same turn** a correction is given.
- **Versioned code files + full QA** (new numbered file swapped in, never in-place; QA shows all processed rows in place).
- **Smallest viable change first; validate in a playground** before any full or production run.
- **Division of labor:** the agent does everything its tools reach (MCPs, connectors, CLIs, scripts, files) and reports after, with a backup and proof; the owner acts only where no tool reaches or the decision is his.

## Composition contract

- `PROJECT.md`, the thin `CLAUDE.md` and `project-memory/`: created and curated by `live-document`. `big-project` only injects hard-rules bullets, never rewrites the living docs.
- Ordinary completing replies, past about 30% context or when the work is done, end with the lightweight two-step handoff block (clear now / type `continue`; from `references/walkthrough-and-handoff.md`). The handoff content itself lives in `PROJECT.md`'s next action, which `live-document` owns; `big-project` only sets how complete it must be.
- An explicit "wrap up session" / "summarize before I clear" invokes `session-handoff` for the full seven-section summary.
- Multi-step manual work for the owner gets exactly ONE file: `live-document`'s interactive `next-actions/<YYYY-MM-DD_HH-MM>-next-actions.html`. Its content follows the walkthrough outline in `references/walkthrough-and-handoff.md`. Never a `.md` twin, never a separate `NEXT STEPS ... .md` (owner, 2026-09-02: "HTML files are enough").
- Never hijack an active `e2e` flow; stay additive.

## When NOT to use

One-off edits, bug fixes, quick lookups, a single small change, or a project already fully governed by an active `e2e` flow that the owner does not want restyled.
