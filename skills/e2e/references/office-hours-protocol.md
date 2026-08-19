# Office Hours protocol

Phase 1 of the end-to-end-development skill. Before Elon cuts requirements, this phase establishes what the actual problem is and who actually has it. Adapted from `gstack-office-hours` by Key Ng Wu; distilled for `/e2e` style.

Skip this phase entirely when `--skip-discovery` is set, when the marker shows Phase 1 already done (legacy: an existing `design-*.md` at the project root - Phase 0 resume detection handles this), or when the user explicitly says "just do it" / "skip discovery" partway through.

**Track-agnostic.** This phase works the same on both tracks. For a **Deliverable** (analysis, deck, report, dashboard, document), read "product" as the deliverable and "users" as its audience/stakeholders; "demand" is whether anyone actually needs this analysis/decision and will act on it.

## 1. Mode selection

Ask the user once (one `AskUserQuestion`):

> What's your goal with this build?

Options:
- **Startup** - building a real product, eventually for real users (possibly paying).
- **Builder** - side project, hackathon, learning, exploration, open source.

The choice picks the question set in step 2. If the user picks Builder, also skip the demand-evidence framing throughout - Builder mode is about delight, not validation.

## 2. Startup-mode forcing questions

Six forcing questions. **Ask one at a time** via `AskUserQuestion`. Never batch. Wait for the answer before composing the next question; the next question often depends on what you just heard.

1. **Demand Reality.** What's the strongest behavioral evidence someone wants this? Quotes don't count - actions do (people paying, switching tools, asking when it ships).
2. **Status Quo.** What workaround do users live with today? If "nothing" - that's a flag that demand is hypothetical, not real.
3. **Desperate Specificity.** Name the actual human who needs this most. Title, role, what happens to them if this doesn't exist.
4. **Narrowest Wedge.** What's shippable this week to *one* paying customer? Not the full vision - the smallest thing somebody would pay for.
5. **Observation.** What surprised you watching someone use it (or the workaround)? "Nothing yet" → consider whether step 6 is premature.
6. **Future-Fit.** Does this become *more* essential in 3 years, not less? If platforms or AI obsolete it, the wedge is wrong.

**Smart routing.** Don't always ask all six. Calibrate to stage:
- **Pre-product** (no users yet): Q1, Q2, Q3 only. Q4-Q6 require artifacts that don't exist.
- **Has users** (any traction): Q2, Q4, Q5.
- **Paying customers**: Q4, Q5, Q6.

## 3. Builder-mode generative questions

Builder mode is generative, not validation. Ask one at a time:

- What's the coolest version of this?
- Who's the first person you'd show it to? What's the "whoa" moment?
- Fastest path to something usable?
- What's the 10x version - what would make this remarkable, not just done?

## 4. Premise challenge

Surface 2-3 premises you've inferred from the answers, as statements requiring agree/disagree. Each goes through its own `AskUserQuestion`. Example premises:

- "The real problem is X, not Y." (Often the surface problem is a symptom.)
- "Existing tool Z already solves 70% of this - the wedge is the missing 30%."
- "If we build this for [persona], [other persona] will not adopt it."

Premises let the user catch you reasoning wrong before you commit to alternatives.

## 5. Mandatory alternatives

Produce **2-3 distinct approaches**. Required: one minimal viable, one ideal architecture. Optional: a third creative / orthogonal angle.

Each approach formatted as:

```
APPROACH <letter>: <Name>
  Summary: <1-2 sentences>
  Effort:  <S|M|L|XL>
  Risk:    <Low|Med|High>
  Pros:    <2-3 bullets>
  Cons:    <2-3 bullets>
  Reuses:  <existing code/patterns/tools, or prior decks/reports/templates/data - empty for greenfield>
```

Present via `AskUserQuestion`. **Do not proceed without the user picking one.** The user may also say "none of these - let's try X" - that's a fourth approach; capture it and re-confirm.

## 6. Output: distill into PROJECT.md (no separate file)

The interview's outcome goes straight into PROJECT.md's canonical sections - there is no `design-*.md` in the consolidated layout (legacy runs that already have one keep it). Distillation map:

| Interview outcome | PROJECT.md home |
|---|---|
| Problem statement (the problem, not the solution) + success criteria ("this worked", user-observable) | *Goal and definition of done* |
| Target user & narrowest wedge; mode (Startup / Builder); demand evidence & status quo (Startup) or "what makes this cool" (Builder) - one or two distilled lines each | *Goal and definition of done* (audience/wedge lines) |
| Constraints (time, money, team, regulatory, technical hard limits) | *Scope and non-goals* (as constraints) or *Decisions locked* if they force a choice |
| Agreed premises | *Decisions locked* (one line each, marked as premises) |
| Recommended approach (the user's pick) + one-line why | *Decisions locked* |
| Alternatives not picked | *Decisions locked* - one terse "considered <X>, rejected because <Y>" bullet each |
| What's not yet answered (feeds CEO Review, Elon, Research) | *Open questions* |

Distill, don't transcribe: the interview transcript stays in the conversation; PROJECT.md gets only the durable outcome, curated per the living-document discipline (reconcile in place, one fact one home).

## 7. Critical rules

- **Never start implementation.** This phase produces validated understanding (captured in PROJECT.md), nothing else.
- **One question at a time.** Batching forces shallow answers.
- **Alternatives are mandatory.** The user picks; you do not pre-commit.
- **Escape hatch:** if the user says "skip discovery" or "just do it" or `--skip-discovery` is set, capture whatever they said as the problem statement + chosen approach in PROJECT.md (*Goal* + *Decisions locked*), and advance.
- **No marketing language.** This is a decision document (engineering or analytical), not a pitch.

## 8. Hand-off

Final user-facing line, verbatim:

> Phase 1 complete, distilled into PROJECT.md (goal, wedge, chosen approach, open questions). Next: Phase 2 CEO Review (or skip with `--skip-discovery` to jump to Phase 3 Elon).

Then wait for the user's "go" (per the golden rule). Do not advance autonomously.
