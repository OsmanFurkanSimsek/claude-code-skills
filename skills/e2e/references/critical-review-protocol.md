# Critical review protocol

Phase 9 of the end-to-end skill. The goal is a deep, independent, **read-only** review by a Claude reviewer subagent that surfaces issues - not one that edits anything. Claude (the orchestrator) applies the fixes after the user picks which to act on. No external CLI, no Codex.

Why a subagent: a reviewer with its own fresh context catches what the builder's context glosses over. If a subagent can't be spawned, run the same review inline yourself in max-thinking mode - the discipline (read-only findings → user approves → orchestrator applies → re-verify) is identical.

The review's *shape* depends on the `track=` field in CLAUDE.md's marker:

- **Build** - a code review: bugs, security, design, plan deviations, code quality.
- **Deliverable** - a critical-reasoning review: flaws in logic and argument, unsupported or overstated claims, weak/missing evidence, statistical or analytical errors, misleading visuals, structural and clarity problems, scope deviations. The reviewer reads the textual artifacts directly (markdown, notebooks, scripts, exported text, data summaries). For tool artifacts it cannot open (e.g., a `.pbix`, a binary deck), export the substance to text first (the measures, the claims, the data summary) or run the pass inline.

## Pre-flight

1. Read the `track=` field from CLAUDE.md's marker to pick the variant.
2. Pick the reviewer subagent:
   - **Build** → `superpowers:code-reviewer` (purpose-built for reviewing against a plan). If unavailable, use `general-purpose`.
   - **Deliverable** → `general-purpose` (there's no purpose-built critical-reasoning agent; the prompt below supplies the lens).
3. No flags, no model selection, no CLI to install. The reviewer is Claude.

## Invocation

Spawn the reviewer with a single Agent tool call. Pass the matching prompt below. **Tell the subagent explicitly that it is read-only.**

```
Agent(
  subagent_type: "<superpowers:code-reviewer | general-purpose>",
  description: "Phase 9 critical review of <short project name>",
  prompt: <see the matching variant below>
)
```

### Build variant (code review)

```
<task>
Deep, READ-ONLY code review for an end-to-end build at:
<absolute path to project root>

Anchors - read these first:
- Thin constitution / bootstrap: ./CLAUDE.md
- Living source of truth: ./PROJECT.md - goal, scope, decisions, lessons, plus its "Execution plan"
  section (step status) and "Research notes" section (research that informed decisions).
  (Legacy layout only: those two live in ./PLAN.md and ./RESEARCH.md instead.)

Then review the source under the project root.
</task>

<output_contract>
Group findings by severity:
- CRITICAL: bugs that produce wrong output, security issues, data loss/corruption risks.
- IMPORTANT: design flaws, missing error handling at boundaries, deviations from PROJECT.md decisions or its Execution plan, performance traps.
- NIT: style/readability/naming improvements where the WHY is non-obvious.

For each finding: file:line reference, one-paragraph description, concrete suggested fix (or fix direction).
If a severity bucket is empty, say "none" rather than padding.
</output_contract>

<safety>
You are READ-ONLY. Do not write, rename, or delete files. Do not run commands that modify state.
Report findings only; the orchestrator applies fixes after the user approves them.
If verifying something requires a change, describe the change instead of attempting it.
</safety>
```

### Deliverable variant (critical-reasoning review)

```
<task>
Deep, READ-ONLY critical-reasoning review of a non-code deliverable at:
<absolute path to project root>

Anchors - read these first:
- Thin constitution / bootstrap: ./CLAUDE.md
- Living source of truth: ./PROJECT.md - goal, scope, decisions, lessons, plus its "Execution plan"
  section (step status) and "Research notes" section (research with citations).
  (Legacy layout only: those two live in ./PLAN.md and ./RESEARCH.md instead.)

Then review the deliverable artifacts under the project root (the deck/report/analysis/document
text, notebooks, data summaries, exported measures). Review the THINKING, not code: is the
argument sound, is every claim supported, do the numbers reconcile, are the visuals honest,
is the structure clear and audience-fit?
</task>

<output_contract>
Group findings by severity:
- CRITICAL: false or unsupported claims, analytical/statistical errors, numbers that don't reconcile, misleading visuals, conclusions the evidence doesn't support.
- IMPORTANT: weak evidence, missing caveats, logical gaps, deviations from PROJECT.md scope, structural problems that obscure the message.
- NIT: clarity, wording, ordering, and presentation improvements where the WHY is non-obvious.

For each finding: a section / slide / cell reference (or file:line for text), one-paragraph description, concrete suggested fix (or fix direction).
If a severity bucket is empty, say "none" rather than padding.
</output_contract>

<safety>
You are READ-ONLY. Do not write, rename, or delete files. Do not run commands that modify state.
Report findings only; the orchestrator applies fixes after the user approves them.
If verifying something requires a change, describe the change instead of attempting it.
</safety>
```

## After the reviewer returns

1. **Stop. Do not auto-apply fixes.** Present the findings to the user grouped by severity.
2. Ask: "Which findings should I fix? You can say 'all critical', 'all important', specific numbers, or 'none of these'."
3. Wait for the user's direction.

## Applying fixes

For each approved finding:

1. Re-read the file at the cited line / the section referenced.
2. Make the fix using Edit (or Write for larger restructures).
3. Track which fixes you applied - you'll re-verify after.

When all approved fixes are in:

1. Re-run the Phase 7 routine for the track (Build: full suite + coverage; Deliverable: the affected acceptance checks + the whole-artifact consistency review).
2. If anything fails, the fix introduced a regression - Edit it again or revert. Do not move on with a red result.
3. Once it's green/consistent, surface a one-line summary per applied fix and ask the user "Move to Phase 10 (Playwright)?"

## What to do with declined findings

If the user declines a finding (e.g., "skip this one, intentional"), record that decision in PROJECT.md under *Decisions locked* (one terse bullet) so future runs don't re-flag the same thing without context.

## Common failure modes

- **Reviewer returns vague suggestions.** Re-prompt with the same template but add "be specific - file:line or section, and the exact change". Don't accept "consider improving error handling" or "tighten the argument" without a target.
- **Reviewer flags a deviation that's intentional.** Don't apply automatically - surface the user's earlier decision (from PROJECT.md / Elon output) and confirm.
- **Reviewer contradicts a locked decision.** PROJECT.md *Decisions locked* is the authority; the reviewer is a reviewer, not an authority. If it says "use library X" (or "restructure the deck") and PROJECT.md decided against it with a documented reason, decline and note why.
- **No subagent available.** Run the matching variant inline yourself in max-thinking mode. Same output contract, same read-only-then-approve discipline.
