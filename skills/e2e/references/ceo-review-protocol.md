# CEO Review protocol

Phase 2 of the end-to-end-development skill. Office Hours (Phase 1) settled *what* the problem is and *who* has it. CEO Review asks: what's the platonic / 10x version of the solution, and where on that spectrum should this build actually land? It runs *before* Elon (Phase 3) so Elon has a 10x vision to cut from, not a vague starting point.

Adapted from `gstack-plan-ceo-review` by Key Ng Wu, but **substantially lighter**. gstack's full CEO review covers security threat modelling, error/rescue registry, observability, deployment & rollout, and seven other engineering review sections - those duplicate concerns already covered by `/e2e`'s Phase 5 (Plan, ultrathink-depth) and Phase 9 (the deep critical review). The CEO phase here owns scope and ambition only.

Skip this phase entirely when `--skip-discovery` is set, when the marker shows Phase 2 already done (legacy: an existing `ceo-plan-*.md` - Phase 0 detection handles this), or when the user says "skip CEO" partway through.

**Track-agnostic.** Scope and ambition apply to both tracks. For a **Deliverable**, the "10x version" is the most ambitious, most useful version of the analysis/deck/report; "files touched" reads as "sections/slides/pages touched"; "existing code to leverage" reads as "prior decks/reports/templates/data to reuse".

## 1. System audit (existing-project only)

Skip for greenfield. Otherwise, do a quick sweep before engaging the user:

- `git log --oneline -30` - recent intent.
- Glob recently-modified files - where the code is currently active.
- Grep `TODO|FIXME|HACK|XXX` - declared debt.
- Read PROJECT.md in full - the Phase 1 outcome and any prior decisions to honor or revisit live there. (Legacy runs: also Glob prior `design-*.md`, `ceo-plan-*.md`, `RESEARCH.md`, `PLAN.md`.)

Two outputs from this audit, kept in working memory: 2-3 well-designed patterns to emulate, and 1-2 anti-patterns to avoid.

## 2. Step 0: Nuclear scope challenge

Before any 10x talk, pressure-test the premise.

### 0A. Premise challenge

Ask via `AskUserQuestion` (separate questions, never batched):

- Is this actually the right problem, or is it a symptom of a different problem?
- What's the user-observable outcome we're optimising for?
- What happens if we do nothing for 6 months?

### 0B. Existing-work leverage (existing-project / existing-materials only)

What partially solves each sub-problem already? Are we rebuilding when we should be refactoring or reusing? Build: list specific files/modules. Deliverable: list prior decks/reports/templates/datasets to build on.

### 0C. Dream-state mapping

Sketch the three-state flow as ASCII:

```
CURRENT STATE  →  THIS PLAN  →  12-MONTH IDEAL
<status quo>      <output of      <platonic version
                   this build>     of the product>
```

Where does this build leave us vs. the 12-month ideal? The gap is the implicit roadmap.

### 0D. Mandatory alternatives

Produce **2-3 distinct approaches** at the *scope-and-ambition* level (not implementation; that's Phase 5 Plan's job):

```
APPROACH <letter>: <Name>
  Summary: <1-2 sentences - what's in scope>
  Effort:  <S|M|L|XL>
  Risk:    <Low|Med|High>
  Pros:    <2-3 bullets>
  Cons:    <2-3 bullets>
  Reuses:  <what we'd build on - code/patterns, or prior decks/reports/templates/data>
```

Required: one minimal viable, one ideal architecture. Optional: a third creative angle.

### 0E. Mode selection

Present 4 modes via `AskUserQuestion`. Recommend a default based on context (greenfield → EXPANSION; small bug or small deliverable → HOLD; > 15 files or sections touched → REDUCTION):

- **EXPANSION** - greenfield feature or new deliverable; dream big, then trim.
- **SELECTIVE EXPANSION** - enhancement to an existing feature/deliverable; baseline + cherry-picked upgrades.
- **HOLD SCOPE** - bug fix, refactor, or narrow/known scope; rigorous review of *what's already chosen*.
- **REDUCTION** - > 15 files or sections touched, or smell of overbuild; cut to essentials.

The mode determines step 3.

## 3. Mode-specific analysis

### EXPANSION

- **10x vision.** What's this look like if it's 10x better than today's status quo?
- **Platonic ideal.** No constraints - what's the perfect version?
- **Delight opportunities.** Generate 5+ candidate delights (UX moments, capability leaps, integrations, unobvious-but-magical features).
- **Opt-in ceremony.** *Each* delight opportunity gets its own `AskUserQuestion` (in / out / save for later). **Never batch.** Batching causes "yes to all" by default, which is exactly the failure mode this phase exists to prevent.

### SELECTIVE EXPANSION

- **Complexity check.** If the baseline scope already touches 8+ files, that's a smell - flag it.
- **Minimum viable scope.** What ships standalone, without the new candidates?
- **Expansion scan.** What 3-5 additions would compound the value most?
- **Cherry-pick ceremony.** One `AskUserQuestion` per candidate. Neutral posture - the baseline is the default; expansion is opt-in.

### HOLD SCOPE

- **Complexity check.** Confirm the scope as defined is < 8 files / < 2 new classes.
- **Minimum viable scope.** Restate it in one sentence so the user can sign off.

### REDUCTION

- **Ruthless minimum.** What's the smallest scope that still solves the named problem?
- **"Must ship together" vs "nice to ship together."** Each candidate currently in scope: must, or nice? Move every "nice" out.

## 4. Output: distill into PROJECT.md (no separate file)

The review's outcome goes straight into PROJECT.md's canonical sections - there is no `ceo-plan-*.md` in the consolidated layout (legacy runs that already have one keep it). Distillation map:

| Review outcome | PROJECT.md home |
|---|---|
| Mode (EXPANSION / SELECTIVE EXPANSION / HOLD SCOPE / REDUCTION) + 10x vision / platonic ideal - one or two lines, the upper bound Elon will cut from | *Goal and definition of done* |
| Dream-state delta (`CURRENT STATE → THIS PLAN → 12-MONTH IDEAL`) - one distilled line on where this build lands vs the ideal | *Goal and definition of done* |
| Every scope decision: In / Deferred / Skipped, with its one-line why (the completeness principle survives as one terse bullet per decision) | *Decisions locked* (In) and *Scope and non-goals* (Deferred / Skipped, each with rationale) |
| "What's NOT in scope" list | *Scope and non-goals* (out-of-scope bullets with one-line rationale each) |
| Reuses (existing code / pattern / library to lean on) | *Decisions locked* |
| Open questions for Phase 3 (Elon) | *Open questions* |

Distill, don't transcribe: PROJECT.md gets the durable decisions, reconciled in place (a scope decision that changes an earlier Phase 1 line REPLACES it).

## 5. Critical rules

- **Completeness principle.** With AI assistance the marginal cost of full coverage is near-zero - surface every scope candidate rather than silently dropping them. Each item the user rejects becomes a row in "What's NOT in scope" with a reason; never just disappear it.
- **One issue = one `AskUserQuestion`.** Never batch. Batching causes default-yes; explicit one-by-one prompts force the cost-benefit conversation.
- **Silent failure = critical defect.** A deferred-but-undocumented scope decision is the worst outcome. If a candidate didn't make it in, it's an out-of-scope bullet in *Scope and non-goals* with rationale.
- **Stay at the scope/ambition altitude.** Don't drift into architecture, security threat modelling, observability - those belong in Phase 5 (Plan) and Phase 9 (the critical review). The CEO phase asks "what should we build?", not "how should we build it?"
- **Escape hatch.** If the user says "skip" or `--skip-discovery` is set, record mode=HOLD SCOPE and the already-chosen approach as the only scope decision in PROJECT.md, and advance.

## 6. Hand-off

Final user-facing line, verbatim:

> Phase 2 complete, scope and ambition distilled into PROJECT.md. Next: Phase 3 Elon - Elon will ruthlessly cut from the 10x vision down to MVP.

Then wait for the user's "go" (per the golden rule). Do not advance autonomously.
