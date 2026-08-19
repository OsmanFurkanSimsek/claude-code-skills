# Elon's Five-Step Algorithm

Source: Walter Isaacson, *Elon Musk*, "the algorithm" chapter.

The algorithm: **Question → Delete → Simplify → Accelerate → Automate**, in that order. The order matters; the book is explicit about why.

This is a thinking framework, not a persona. Do NOT roleplay Musk, mimic his voice, fabricate quotes, or speculate about what he "would" think. Apply the published algorithm to the user's problem, neutrally.

---

## Step 1 - Question every requirement

**Principle.** Each requirement must come with a real person's name. Never accept "the legal department said so" or "marketing requires it." Find the human who actually said it. Then question it - especially if the human is smart, because requirements from smart people are the most dangerous (people are less likely to push back). Then make the requirements less dumb.

**Why it's first.** If you optimize the wrong requirement, every later step compounds the waste. The cheapest thing to delete is a requirement that shouldn't exist.

**Translations.**
- Code: who asked for this feature? What problem are they actually solving? Could a smaller thing solve it?
- Plan: what is each milestone for? Who needs it? What changes if we drop it?
- Presentation: who is in the room? What do they need to walk away knowing? Everything else is probably noise.
- Research: what question are we actually answering? Who's it for? Is this the right question?

**Coaching questions.**
1. In one paragraph, what are you trying to create and why?
2. Magic-wand probe: if a magic wand made the perfect version of this exist tomorrow, what would it look like? Not what's feasible - what's ideal.
3. List every requirement you think it has. For each one: who asked for it (a real person, or yourself), and tag it A (real constraint - physical/legal/contractual), B (convention - "we always do it this way" / "industry standard"), or C (unverified - a named person asked, but the underlying need hasn't been checked).
4. For any B that smells like analogy, drop down a level: what's physically or fundamentally true here? Does the convention still hold once you reason up from there?
5. Which requirement, if you removed it, would actually break the thing? Which ones just feel load-bearing?

---

## Step 2 - Delete any part of the process you can

**Principle.** Aggressive deletion of parts, steps, sections, features. "The best part is no part." Rule of thumb from the book: if you don't end up adding back at least 10% of what you deleted, you didn't delete enough.

**Why it's second.** Once requirements are named, the things that exist only to serve a fake requirement become visible and obvious to delete.

**Translations.**
- Code: which functions, files, abstractions, dependencies, configuration knobs can be cut?
- Plan: which phases, milestones, meetings, artifacts can disappear?
- Presentation: which slides? Which bullet points within a slide? Which examples?
- Research: which sub-questions, methods, sources can be dropped?

**Coaching questions.**
1. Looking at what you described in Step 1, what's the most ambitious thing you could delete? Start with anything tagged B.
2. What did you include because you thought "people expect this"? Strong delete candidate.
3. Limits probe: what survives if you cut 90%? What changes at 100x scale, or 1x user? The parts that hold up at the extremes are the ones that actually matter.
4. If you deleted the second-most-important feature/section/phase, what actually breaks?
5. Cut harder. Now: which one or two cuts will you have to add back? If none, you didn't cut enough.

---

## Step 3 - Simplify and organize

**Principle.** Now (and only now) make the surviving parts simpler and better organized.

**Why it's third, not first.** A common, expensive mistake - explicitly called out in the book - is to simplify or optimize a part that should not have existed in the first place. You will spend real effort polishing something that Step 2 would have deleted.

**Translations.**
- Code: reduce shared types, collapse layers of indirection, rename for clarity, group related functions, kill duplication.
- Plan: sequence remaining work so dependencies flow naturally; merge overlapping milestones.
- Presentation: tighten the narrative arc; one idea per slide; reorder for the audience.
- Research: group sub-questions, define terms once, structure the writeup before drafting it.

**Coaching questions.**
1. Of the parts that survived, which two or three are the most tangled or hardest to explain?
2. If a smart friend saw this for the first time, where would they get confused?
3. What's the simplest possible structure that holds the surviving pieces?
4. Idiot Index (when applicable): what's the ratio of total size to irreducible core - LoC vs. core logic, slide count vs. core message, plan length vs. real decisions? If it's >5x, where is the waste hiding?

---

## Step 4 - Accelerate cycle time

**Principle.** Every process can be sped up. "If a timeline is long, it's wrong." But only do this after Steps 1-3. The book is explicit: at Tesla, Musk wasted significant time accelerating processes that he later realized should have been deleted.

**Translations.**
- Code: shorter feedback loops - local tests, hot reload, smaller PRs, faster CI.
- Plan: shorter milestones - week-long checkpoints instead of month-long ones; demo earlier.
- Presentation: iterate faster - outline first, polish last; show a draft to one person on day one, not the finished deck on day five.
- Research: tighter loops between hypothesis and check; smaller experiments; share rough findings before they're polished.

**Coaching questions.**
1. Where in this work do you wait the longest between trying something and seeing if it worked?
2. What would a 2x faster version of that loop look like?
3. What's the shortest version of this whole project that still proves the core idea?

---

## Step 5 - Automate

**Principle.** Automation comes last. The Tesla Nevada/Fremont mistake was automating before deleting and simplifying. You end up with a beautifully automated process that does the wrong thing very efficiently.

**Translations.**
- Code: scripts, CI jobs, code generation, scheduled tasks - but only for the steps that survived all four prior cuts.
- Plan: templates, recurring meetings, status automation - only for the cadence that survived Step 2.
- Presentation: slide templates, reusable diagrams - only for the patterns that survived Step 3.
- Research: pipelines, scrapers, dashboards - only for the questions that survived Step 1.

**Coaching questions.**
1. Of what's left, what will you do more than three times?
2. For each candidate, has it been through all four prior steps? If not, automating is premature.
3. What's the smallest automation that pays for itself this month?

---

## Mental models

Supplementary tools to deploy during the algorithm. Honest attribution: labeled (Musk method) if from Isaacson's biography, or (complementary) otherwise.

**First-Principles Thinking (Musk method)**  
Use at: Step 1, when the user is reasoning by analogy. Probe: "Drop the analogy. What's physically or fundamentally true here? Build the answer up from that, not from what others are doing." Classic example from the biography: raw material cost of a rocket is a small fraction of its finished price, so most cost lives in the assembly process - not in physics.

**Magic-Wand Number (Musk method)**  
Use at: Step 1, right after establishing what the user is creating. Probe: "If a magic wand made the perfect version of this exist tomorrow, what would it look like?" Sets a target state independent of current constraints. The gap between magic-wand and feasible is the optimization space.

**A/B/C Requirement Classification (complementary)**  
Use at: Step 1, while listing requirements.
- A - real constraint (physical law, hard technical limit, legal/contractual obligation). Keep.
- B - convention ("we always do it this way", "industry standard", "people expect this"). Strong delete candidate in Step 2.
- C - unverified (a named person asked, but the underlying need hasn't been checked). Verify before deciding.

**Thinking in Limits (Musk method)**  
Use at: Step 2, especially when the user is reluctant to cut. Push the system to extremes: "What survives if you cut 90%? What changes at 100x scale? At 1x user?" Behavior at the extremes reveals which parts are load-bearing and which are decoration.

**Idiot Index (Musk method)**  
Use at: Step 3, only when there's a meaningful ratio to measure.
- Code: total LoC / core-logic LoC
- Presentation: total slides / slides carrying the core idea
- Plan: phases planned / phases that actually move the goal
- Manufacturing (original form): finished price / raw-material cost
Heuristic: if the ratio is >5x, waste is hiding somewhere.

**Pre-mortem / Inversion (complementary - Gary Klein / Charlie Munger)**  
Use at: after Step 5, before closing out (Phase B). Probe: "Imagine it's six months from now and this thing failed. What's the most likely reason? Is there a cheap thing you could do today to prevent that?" Surfaces risks the optimization pass misses.

---

## Interaction protocol

**Phase A - coach through the steps (one step per turn)**
- Do not dump all five steps in one response. Walk sequentially.
- Acknowledge what they're creating in one line.
- Run Step 1 coaching questions, then wait.
- After they answer, briefly reflect what they said, then run Step 2 questions. Wait again.
- Continue through Steps 3, 4, 5 - one step per turn, always waiting.
- If the user gives short answers, gently push back once ("can you go further on this?") but do not grind them.

**Phase A.5 - pre-mortem (one turn)**  
After Step 5: "One last probe: imagine it's six months from now and this thing failed. What's the most likely reason - and is there a cheap thing you could do today to prevent that?" Capture the answer for PROJECT.md Risks / Lessons.

**Phase B - close out into PROJECT.md**  
After the pre-mortem, summarize what changed across the five steps in 4-6 lines and state in one line that the outcome lands in PROJECT.md (mandatory and silent, into its canonical homes: surviving requirements and simplifications to Decisions locked, cuts to Scope and non-goals, deferrals to Open questions, pre-mortem risks to Risks / Lessons). Never ask where to record the outcome and never offer "keep it in chat vs a separate document" - a project-partner project always has (or is about to get) PROJECT.md as the single source of truth. Write a personal `elon-<short-slug>.md` copy (template below) only if the user asks for one unprompted, and never without explicit consent in the same turn.

---

## Output doc template

When (and only when) the user asks for a personal Elon session doc:

```markdown
# Elon algorithm: <one-line topic>

_Date: <yyyy-mm-dd> · Source: Walter Isaacson, _Elon Musk_, "the algorithm" chapter._

## What I'm creating
<user's one-paragraph description from Step 1>

_Magic-wand version: <one line from the magic-wand probe; omit if not answered>_

## Step 1 - Questioned requirements
| Requirement | Who asked | Class (A/B/C) | Verdict (keep / cut / reframe) | Note |

## Step 2 - Deleted
- What I cut:
- What I added back (target >=10% of cuts):

## Step 3 - Simplified
<the cleaned-up structure of what survived>

## Step 4 - Accelerated
<where the cycle got shorter, and how>

## Step 5 - Automated
<what's worth automating now, and what's deliberately deferred>

## Risks I'm watching
<from the pre-mortem. Omit if user passed on it.>

## Parking lot - not doing yet
<things the user explicitly chose to defer>
```

Slug rule: lowercase, hyphenated, <=6 words from the topic. E.g., `elon-analytics-dashboard.md`.

---

## Anti-patterns

- Do not roleplay Musk. No "as Elon would say." Apply the algorithm neutrally.
- Do not apply to trivial work. Ask first for small tasks.
- Do not skip ahead. Steps 3-5 done before Steps 1-2 waste effort on things that should have been deleted.
- Do not grind the user. Push back once on short answers; if still short, move on.
- Do not fabricate biography content. Cite only principles in this file.
- Do not write an `elon-*.md` unless the user asked for one, and never without explicit consent in the same turn. PROJECT.md is the opposite case: updating it is a mandatory, silent duty.
- Do not present PROJECT.md as optional. Asking "keep it in chat or write a separate document?" - or offering any alternative home for the outcome - is exactly the bug this rule prevents.
