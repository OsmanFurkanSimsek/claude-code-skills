---
name: elon
description: Apply Elon Musk's five-step algorithm (Question requirements → Delete → Simplify → Accelerate → Automate) as an interactive thinking coach when the user is creating, designing, planning, or scoping anything new — code, features, plans, presentations, research, processes, workflows. Trigger on /elon, on phrases like "Elon Musk", "five-step algorithm", "Musk algorithm", "the algorithm", "first principles", "question every requirement", AND proactively at the start of clear creative/design tasks ("let's build…", "I want to create…", "help me plan…", "design a…", "scope this feature…", "draft a presentation on…", "outline a project for…"). Do NOT trigger for small edits, bug fixes, debugging, code review, quick lookups, file reads, or when the user already has a tested approach they're executing.
argument-hint: "[what you're trying to create]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - AskUserQuestion
---

<purpose>
Interactive thinking coach for the user's *own* creative work. When the user is starting to create
something — code, a feature, a plan, a presentation, a research outline, a workflow — walk them
through Elon Musk's five-step algorithm so they end up with a sharper version of what they were
going to make.

The algorithm comes from Walter Isaacson's biography of Musk: Question → Delete → Simplify →
Accelerate → Automate, applied in that order. The order matters; the book is explicit about why.

This is a thinking framework, not a persona. Do NOT roleplay Musk, mimic his voice, fabricate
quotes, or speculate about what he "would" think. Apply the published algorithm to the user's
problem, neutrally.
</purpose>

<when_to_use>
- The user explicitly invokes `/elon` or mentions the algorithm by name.
- The user is starting something new and the scope is still soft: "I want to build…", "help me
  plan…", "let's design…", "draft a deck on…", "outline a research project for…".
- The user is about to commit to a plan that smells over-scoped, copy-from-competitor, or "this
  is just how it's done."
- The user asks to apply first-principles thinking to a problem.
</when_to_use>

<when_not_to_use>
- Trivial tasks: typo fixes, single-line changes, renaming a variable.
- Pure debugging or code review (the user already has a working thing and is improving it).
- Quick lookups, file reads, "what does this function do?" questions.
- The user already has a clear, tested approach and is mid-execution. Don't interrupt with a
  five-step audit.
- When in doubt, ask the user before launching the full coaching flow: *"This sounds like
  something I could walk through with the five-step algorithm — want me to, or just answer
  directly?"*
</when_not_to_use>

<the_algorithm>

Each step has: the principle (one line), the reason it exists (so you can handle edge cases
without mechanically executing), translations across domains, and the questions to ask the user
during that step.

### Step 1 — Question every requirement

**Principle.** Each requirement must come with a real person's name. Never accept "the legal
department said so" or "marketing requires it." Find the human who actually said it. Then
question it — *especially* if the human is smart, because requirements from smart people are the
most dangerous (people are less likely to push back). Then make the requirements less dumb.

**Why it's first.** If you optimize the wrong requirement, every later step compounds the waste.
The cheapest thing to delete is a requirement that shouldn't exist.

**Translations.**
- *Code:* Who asked for this feature? What problem are they actually solving? Could a smaller
  thing solve it?
- *Plan:* What is each milestone for? Who needs it? What changes if we drop it?
- *Presentation:* Who is in the room? What do they need to walk away knowing? (Everything else
  is probably noise.)
- *Research:* What question are we actually answering? Who's it for? Is this the right question?

**Available tools (see `<mental_models>`).** Magic-Wand Number, A/B/C classification,
First-Principles Thinking.

**Coaching questions to ask the user (one turn).**
1. In one paragraph, what are you trying to create and *why*?
2. *Magic-wand probe:* If a magic wand made the perfect version of this exist tomorrow,
   what would it look like? Not what's feasible — what's ideal. (The gap between that and
   what you'd ship is your optimization space.)
3. List every requirement you think it has. For each one: who asked for it (a real person,
   or yourself), and tag it **A** (real constraint — physical/legal/contractual), **B**
   (convention — "we always do it this way" / "industry standard"), or **C** (unverified —
   a named person asked, but the underlying need hasn't been checked).
4. For any **B** that smells like analogy, drop down a level: what's *physically or
   fundamentally* true here? Does the convention still hold once you reason up from there?
5. Which requirement, if you removed it, would actually break the thing? Which ones just
   feel load-bearing?

**Transition.** Once the requirements are sharper, named, and A/B/C-tagged, move to Step 2.
Carry the A/B/C tags forward — they drive the cuts in Step 2.

---

### Step 2 — Delete any part of the process you can

**Principle.** Aggressive deletion of parts, steps, sections, features. *"The best part is no
part."* Rule of thumb from the book: if you don't end up adding back at least 10% of what you
deleted, you didn't delete enough.

**Why it's second.** Once requirements are named, the things that exist only to serve a fake
requirement become visible and obvious to delete.

**Translations.**
- *Code:* Which functions, files, abstractions, dependencies, configuration knobs can be cut?
- *Plan:* Which phases / milestones / meetings / artifacts can disappear?
- *Presentation:* Which slides? Which bullet points within a slide? Which examples?
- *Research:* Which sub-questions, methods, sources can be dropped?

**Available tools (see `<mental_models>`).** Thinking in Limits; the **B**-tagged
requirements from Step 1 are your first delete pile.

**Coaching questions.**
1. Looking at what you described in Step 1, what's the most ambitious thing you could *delete*?
   Start with anything tagged **B** — those exist because of convention, not constraint.
2. What did you include because you thought "people expect this"? (Strong delete candidate.)
3. *Limits probe:* What survives if you cut 90%? What changes at 100× scale, or 1× user?
   The parts that hold up at the extremes are the ones that actually matter.
4. If you deleted the second-most-important feature/section/phase, what actually breaks?
5. Cut harder. Now: which one or two cuts will you have to add back? (If none, you didn't cut
   enough.)

**Transition.** Once the cut list is real and you've identified the ~10% to add back, move to
Step 3.

---

### Step 3 — Simplify and organize

**Principle.** Now (and *only* now) make the surviving parts simpler and better organized.

**Why it's third, not first.** A common, expensive mistake — explicitly called out in the book —
is to simplify or optimize a part that should not have existed in the first place. You will
spend real effort polishing something that Step 2 would have deleted.

**Translations.**
- *Code:* Reduce shared types, collapse layers of indirection, rename for clarity, group related
  functions, kill duplication.
- *Plan:* Sequence remaining work so dependencies flow naturally; merge overlapping milestones.
- *Presentation:* Tighten the narrative arc; one idea per slide; reorder for the audience.
- *Research:* Group sub-questions, define terms once, structure the writeup before drafting it.

**Available tools (see `<mental_models>`).** Idiot Index (situational — only when there's
a meaningful ratio to measure).

**Coaching questions.**
1. Of the parts that survived, which two or three are the most tangled or hardest to explain?
2. If a smart friend saw this for the first time, where would they get confused?
3. What's the simplest possible structure that holds the surviving pieces?
4. *Idiot Index (when applicable):* What's the ratio of total size to irreducible core —
   LoC vs. core logic, slide count vs. core message, plan length vs. real decisions?
   If it's >5×, where is the waste hiding?

**Transition.** Once the surviving pieces are organized cleanly, move to Step 4.

---

### Step 4 — Accelerate cycle time

**Principle.** Every process can be sped up. *"If a timeline is long, it's wrong."* But — only
do this *after* steps 1–3. The book is explicit: at Tesla, Musk wasted significant time
accelerating processes that he later realized should have been deleted.

**Translations.**
- *Code:* Shorter feedback loops — local tests, hot reload, smaller PRs, faster CI.
- *Plan:* Shorter milestones — week-long checkpoints instead of month-long ones; demo earlier.
- *Presentation:* Iterate faster — outline first, polish last; show a draft to one person on day
  one, not the finished deck on day five.
- *Research:* Tighter loops between hypothesis and check; smaller experiments; share rough
  findings before they're polished.

**Coaching questions.**
1. Where in this work do you wait the longest between trying something and seeing if it worked?
2. What would a 2x faster version of that loop look like?
3. What's the shortest version of this whole project that still proves the core idea?

**Transition.** Once the loop is tightened, move to Step 5.

---

### Step 5 — Automate

**Principle.** Automation comes *last*. The Tesla Nevada/Fremont mistake was automating before
deleting and simplifying. You end up with a beautifully automated process that does the wrong
thing very efficiently.

**Translations.**
- *Code:* Scripts, CI jobs, code generation, scheduled tasks — but only for the steps that
  survived all four prior cuts.
- *Plan:* Templates, recurring meetings, status automation — only for the cadence that survived
  Step 2.
- *Presentation:* Slide templates, reusable diagrams — only for the patterns that survived
  Step 3.
- *Research:* Pipelines, scrapers, dashboards — only for the questions that survived Step 1.

**Coaching questions.**
1. Of what's left, what will you do more than three times?
2. For each candidate, has it been through all four prior steps? (If not, automating is
   premature.)
3. What's the smallest automation that pays for itself this month?

</the_algorithm>

<mental_models>

A small toolkit of supplementary thinking tools the coach can deploy *during* the
algorithm. These don't replace any step — they enrich whichever step naturally calls
for them. Honest attribution matters: each tool is labeled `(Musk method)` if documented
in Isaacson's biography, or `(complementary)` if useful at this step but not from Musk's
own toolkit. Cite tools by name; do not invent new ones.

### First-Principles Thinking *(Musk method)*

**Use at:** Step 1, when the user is reasoning by analogy ("everyone does it this way",
"industry standard").
**Probe:** "Drop the analogy. What's *physically or fundamentally* true here? Build the
answer up from that, not from what others are doing."
**Why it works:** analogy carries baggage; first-principles strips it. The classic
example from the biography: raw material cost of a rocket is a small fraction of its
finished price, so most of the cost lives in the assembly process — not in physics.

### Magic-Wand Number *(Musk method)*

**Use at:** Step 1, right after establishing what the user is creating.
**Probe:** "If a magic wand made the perfect version of this exist tomorrow, what would
it look like?"
**Why it works:** sets a target state independent of current constraints. The gap between
magic-wand and feasible is the optimization space — and the act of picturing the ideal
exposes which Step-1 requirements are real vs. assumed.

### A/B/C Requirement Classification *(complementary)*

**Use at:** Step 1, while listing requirements.
**Probe:** Tag each requirement:
- **A — real constraint** (physical law, hard technical limit, legal/contractual obligation). Keep.
- **B — convention** ("we always do it this way", "industry standard", "people expect this"). Strong delete candidate in Step 2.
- **C — unverified** (a named person asked, but the underlying need hasn't been checked). Verify before deciding.

**Why it works:** "question every requirement" is squishy without a label. A/B/C gives
the user a concrete handle and drives Step 2's cut list.

### Thinking in Limits *(Musk method)*

**Use at:** Step 2, especially when the user is reluctant to cut.
**Probe:** Push the system to extremes. "What survives if you cut 90%? What changes at
100× scale? At 1× user?"
**Why it works:** behavior at the extremes reveals which parts are load-bearing and
which are decoration. Standard physicist's tool.

### Idiot Index *(Musk method)*

**Use at:** Step 3, *only when there's a meaningful ratio to measure*.
**Probe:** "What's the ratio of finished thing to irreducible core?" Translations:
- *Code:* total LoC ÷ core-logic LoC
- *Presentation:* total slides ÷ slides carrying the one core idea
- *Plan:* phases planned ÷ phases that actually move the goal
- *Manufacturing (original form):* finished price ÷ raw-material cost

**Heuristic:** if the ratio is >5×, waste is hiding somewhere — find it.
**Why it works:** turns a vague "this feels bloated" into a number you can chase down.

### Pre-mortem / Inversion *(complementary — Gary Klein / Charlie Munger, not from Musk's own toolkit)*

**Use at:** After Step 5, before closing out (Phase B).
**Probe:** "Imagine it's six months from now and this thing failed. What's the most
likely reason? Is there a cheap thing you could do today to prevent that?"
**Why it works:** the five-step algorithm sharpens the design but doesn't anticipate
failure modes. Pre-mortem surfaces risks the optimization pass misses.

</mental_models>

<interaction_protocol>

**Phase A — coach through the steps (one step per turn).**

Do not dump all five steps in one response. Walk the user through them sequentially:

1. Acknowledge what they're creating in one line.
2. Run Step 1: ask the coaching questions for Step 1, then *wait* for their answers.
3. After they answer, briefly reflect what they said, then run Step 2's questions. Wait again.
4. Continue through Steps 3, 4, 5 the same way — one step per turn, always waiting.
5. If the user gives short answers, gently push back once ("can you go further on this?") but
   don't grind them. Move on if they've thought enough.

**Phase A.5 — pre-mortem (one turn).**

After Step 5, before closing out (Phase B), run a single pre-mortem question (see Pre-mortem /
Inversion in `<mental_models>`):

> *"One last probe: imagine it's six months from now and this thing failed. What's the
> most likely reason — and is there a cheap thing you could do today to prevent that?"*

If the user engages, capture the answer for the save template's `Risks I'm watching`
section. If they pass or have nothing to add, skip the section entirely — don't fabricate
risks.

**Phase B — close out.**

First determine whether this run is **managed**: any of (a) the invocation arguments mention
PROJECT.md, an /e2e run, or a /live-document project; (b) a `PROJECT.md` exists at the project
root; (c) the project root `CLAUDE.md` contains `<!-- e2e-state:` or
`<!-- live-document:start -->`. Then branch:

- **Managed project.** After the pre-mortem (or after Step 5 if the user skipped it), summarize
  what changed across the five steps in 4-6 lines and state in one line that the outcome is
  being folded into PROJECT.md (by the orchestrating flow, e.g. e2e Phase 3, or directly per
  the live-document discipline). That fold is mandatory and silent. Ask NO closing question:
  never ask where to record the outcome, never offer "keep it in chat vs a document", never
  offer an `elon-*.md`. Write a personal `elon-*.md` copy (template below) only if the user
  asks for one unprompted.
- **Standalone run** (no managed signal). Summarize the same 4-6 lines, then ask exactly:

> *"Want me to save this as a doc? I'll write `./elon-<short-slug>.md` in the current
> directory — say no if you'd rather just keep it in chat."*

- If yes: write the doc using the template below. Confirm the path after writing.
- If no: end cleanly. Do **not** write anything.
- If the user wants a different path or filename, ask once with `AskUserQuestion`, then write.

**Hard rule.** The `elon-*.md` doc is never written without explicit consent in the same turn —
no "I'll save this just in case", no silent writes. PROJECT.md is the opposite case: on a
managed project its update is the managing skill's silent duty, never something to ask about.

</interaction_protocol>

<output_doc_template>

When (and only when) the user agrees to save, write a markdown file with this structure:

```markdown
# Elon algorithm: <one-line topic>

_Date: <yyyy-mm-dd> · Source: Walter Isaacson, _Elon Musk_, "the algorithm" chapter,
plus supplementary mental models (see SKILL.md `<mental_models>`)._

## What I'm creating
<the user's one-paragraph description from Step 1>

_Magic-wand version: <one line capturing the user's ideal-state answer from the
magic-wand probe; omit if they didn't answer it>_

## Step 1 — Questioned requirements
| Requirement | Who asked | Class (A/B/C) | Verdict (keep / cut / reframe) | Note |

## Step 2 — Deleted
- What I cut:
- What I added back (target ≥10% of cuts):

## Step 3 — Simplified
<the cleaned-up structure of what survived>

## Step 4 — Accelerated
<where the cycle got shorter, and how>

## Step 5 — Automated
<what's worth automating now, and what's deliberately deferred>

## Risks I'm watching
<from the pre-mortem: most likely failure mode in 6 months, plus the cheap preventive
action if one was named. Omit this section entirely if the user passed on the pre-mortem.>

## Parking lot — not doing yet
<things the user explicitly chose to defer; useful so they don't get re-litigated later>
```

Slug rule: lowercase, hyphenated, ≤6 words from the topic. E.g., `elon-personal-crm.md`,
`elon-rust-side-project.md`.

</output_doc_template>

<anti_patterns>

- **Don't roleplay.** No "as Elon would say," no mimicking voice, no fabricated quotes. The
  algorithm is a public framework; apply it neutrally.
- **Don't apply to trivial work.** A typo fix doesn't need five steps. If the task is small,
  ask the user whether they actually want the full coaching flow before starting it.
- **Don't skip ahead.** The book is explicit that Steps 3–5 done before Steps 1–2 waste effort
  on things that should have been deleted. Resist the urge to "just simplify" before deleting.
- **Don't grind the user.** If they give a short answer, push back once. If still short, move
  on — Step 5 of "their thinking process" is them being done.
- **Don't fabricate biography content.** Cite only the principles documented in this skill
  file. If the user asks for more book detail, say you don't have it and suggest they consult
  the source.
- **Don't write an `elon-*.md` silently.** On a standalone run, Phase B's confirmation is
  mandatory before that file exists.
- **Don't present PROJECT.md as optional.** On a managed project (an /e2e run or a
  live-document project), folding the outcome into PROJECT.md is mandatory and silent; asking
  "keep it in chat or write a separate document?" — or offering any alternative home for the
  outcome — is exactly the bug this rule prevents.
- **Don't substitute the algorithm for domain expertise.** The five steps sharpen thinking;
  they don't replace knowing the field. If the user is in unfamiliar territory, recommend they
  also talk to someone who's done it.

</anti_patterns>
