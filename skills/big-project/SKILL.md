---
name: big-project
description: Use when the owner types /big-project, or is starting or resuming a substantial multi-session project and wants it run the way he likes to work - "set this up the way I like", "run this like my big projects", "my usual way of working", "apply my working style". Applies the owner's durable working-style profile (Summary/Why/What-you-should-do answer format; the two-step context-handoff block that ends every completing reply; no unilateral owner decisions; .md timestamped-superseding walkthroughs; numbered one-action steps; versioned code + full QA; predict-run-duration; save-feedback-to-memory same turn; validate-in-a-playground first; assistant-plans / owner-executes division of labor). Composes with live-document (PROJECT.md + CLAUDE.md), session-handoff (clear-time summary), and e2e (full rigor), and DELEGATES their machinery instead of re-implementing it. Do NOT use for one-off edits, bug fixes, quick lookups, or a single small change.
---

# big-project

## What this is

A **personal working-style layer**. Invoking `/big-project` makes the current project run the way the owner likes his big projects to run. It is deliberately thin: its whole substance is one portable profile of the owner's durable preferences (`references/preferences.md`), which it injects into the project and enforces every session.

**It composes; it never reinvents.** Keeping a living document, getting ready to `/clear`, and handing off to the next agent are already solved by skills the owner has. `big-project` delegates those:

- `live-document` owns `PROJECT.md` + the thin `CLAUDE.md` and their reconcile-not-append discipline.
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
   - No living doc, normal path -> invoke `Skill(live-document)` to scaffold `PROJECT.md` + the thin `CLAUDE.md`. Do not write those files yourself.
   - Living doc already present -> layer on top only; touch nothing the `live-document` or `e2e` marker owns.
3. **Inject the owner's delta into the project `CLAUDE.md`.** Apply the hard-rules bullets and the two-step handoff block from `references/claude-md-injection.md` into the project's hard-rules list. **Insert only what is absent** - `live-document` already carries ask-before-assuming, Summary/Reasoning/Steps, Next Actions pairs, tidy-root, and no-long-dash, so never duplicate those. Re-running the skill self-heals: it adds only missing rules.
4. **Announce** in one line what was injected, then follow the profile for the rest of the session.

## Always-on enforcement (short list; full list in `references/preferences.md`)

- **Answer format:** Summary, then Why, then What you should do LAST - numbered, one action per line. Nothing to do -> say so plainly.
  The `answer-format` skill is the full version of this one rule (live step lists that survive follow-up questions, worked examples,
  desktop setup). If it is installed, invoke it and let it own reply shape; this skill keeps owning everything else. Its handoff note
  matters: the two-step context-handoff block below goes INSIDE the numbered actions as the final steps, never appended after them.
- **End every completing reply with the two-step context-handoff block** (clear context now + a paste-ready kickoff message for the next agent). This is the owner's signature rule; honor it literally, every reply that finishes work.
- **No unilateral owner decisions.** Names, write targets, and whether-to-create-something are the owner's call. Propose 2-5 options with trade-offs and ask.
- **Predict run duration** before any long or expensive run; record the measured actual afterward.
- **Save feedback to memory the same turn** a correction is given.
- **Versioned code files + full QA** (new numbered file swapped in, never in-place; QA shows all processed rows in place).
- **Smallest viable change first; validate in a playground** before any full or production run.
- **Division of labor:** the agent plans and writes code/artifacts as files; the owner executes in his environment and reports back.

## Composition contract

- `PROJECT.md` and the thin `CLAUDE.md`: created and curated by `live-document`. `big-project` only injects hard-rules bullets, never rewrites the living doc.
- Ordinary completing replies end with the lightweight two-step handoff block (from `references/walkthrough-and-handoff.md`).
- An explicit "wrap up session" / "summarize before I clear" invokes `session-handoff` for the full seven-section summary.
- Multi-step manual work for the owner gets a numbered `.md` walkthrough per `references/walkthrough-and-handoff.md`, plus `live-document`'s Next Actions file pair.
- Never hijack an active `e2e` or `gsd` flow; stay additive.

## When NOT to use

One-off edits, bug fixes, quick lookups, a single small change, or a project already fully governed by an active `e2e`/`gsd` flow that the owner does not want restyled.
