# Working-style profile

The portable rules for how the owner likes a big project run. Read this in full at the start of every `big-project` session and follow every rule. This file is **domain-free**: tool-, data-, and model-specific rules (a particular cloud, BI tool, or LLM) live in the project's own `PROJECT.md` / `CLAUDE.md`, never here.

> This profile was seeded from a real project (a multi-source data pipeline) and generalized. Fork and edit it to adapt the skill for another person or team.

---

## 1. Answer format: Summary -> Why -> What you should do (last)

Order every reply: (1) **Summary** in plain words, what happened; (2) **Why**, the reasoning, numbers, and trade-offs; (3) **What you should do** LAST, at the very bottom, numbered, one action per line, concrete verbs (run, open, click, look at, answer). If there is nothing to do, say "Nothing to do - this is finished" plainly.

**Why:** the owner reads the bottom of the message for his next action. Actions-first forces him to scroll up and down; reasoning above the actions lets him scroll up only if he wants the why.

**How to apply:** when the owner has nothing to do (a pure question), drop the steps section and lead with a 1-3 sentence TLDR instead.

The step list is **live across the conversation**, not a per-message artifact: if the owner asks a question about step 3 of five, answer it and then re-show the whole list with 1-2 struck through, 3 marked current, and the rest pending. Keep the original numbers stable while the list is valid, so "step 3" keeps meaning what he meant; renumber cleanly from 1 only when the plan genuinely changes, and say so. The `answer-format` skill owns this rule in full - invoke it when installed rather than re-deriving the detail here.

## 2. End every completing reply with the two-step context-handoff block

Every chat reply that completes work ends with, filled in:

> 1. You can clear the context NOW. Everything important is saved in PROJECT.md, memory, the skill files, and `<the live walkthrough file>`.
> 2. Start a fresh session and paste exactly this message:
> `<the exact paste-ready kickoff message for the next agent>`

**Why:** the owner clears context often. He must never have to ask whether it is safe to clear or what to paste next. This is his signature rule, corrected more than once - follow it literally.

**How to apply:** the block closes the chat reply itself, not only the walkthrough file. Place it INSIDE the `What you should do` list as its final numbered steps - it is two actions for the owner, so it belongs in the actions section rather than appended after it. That satisfies this rule and the answer-format rule that nothing follows the numbered list. See `walkthrough-and-handoff.md` for the template. For a heavy explicit wrap-up ("summarize before I clear"), use the `session-handoff` skill's full summary instead.

## 3. No unilateral owner decisions

Names (of tables, files, artifacts), where data lands, and whether to create a thing (a table, a pipeline, a schedule) are the owner's calls. Never pick them yourself.

**Why:** these are ownership decisions with lasting consequences; a wrong guess is expensive to unwind.

**How to apply:** propose 2-5 concrete options with trade-offs and ask. Surface any inferred premise before writing code.

## 4. Deliverables as `.md`, never `.txt`; the handoff walkthrough is ONE HTML file

Anything the owner READS (run reports, analyses, tracking plans) is a Markdown file; `.txt` is only ever a raw copy-paste code payload referenced from an `.md`. The one exception is the handoff walkthrough: it is `live-document`'s single interactive `next-actions/<YYYY-MM-DD_HH-MM>-next-actions.html`, never a `.md` twin and never a separate `NEXT STEPS ... .md` (the owner retired that naming on 2026-09-02: "Why do you create both MD and HTML for Next Actions? ... HTML files are enough."). The newest date-time prefix is the live one; no SUPERSEDED banner.

**Why:** `.md` renders readably for reports; the HTML walkthrough is interactive (tick-off steps, copy buttons), and one file per handoff keeps the folder unambiguous. Two files with the same content were pure double production.

**How to apply:** keep every old dated file (the folder is the history); never edit an old walkthrough in place, write a new dated HTML.

## 5. Numbered, one-action-per-step walkthroughs

When the owner must do something himself, write it as a numbered list, **one click or one input per step**: exact button and field names, the exact value to type, where that value comes from, and what success looks like. A high-level instruction like "configure the connector" is a bug.

**Why:** the owner often works alone against the walkthrough, sometimes a day later; every compressed sub-step is a place he can get stuck.

**How to apply:** for more than ~10 steps, deliver in chunks of 5-10 and wait for confirmation before the next chunk. See `walkthrough-and-handoff.md`.

## 6. Code versioning + full QA

Ship each iteration as a **new numbered file** the owner swaps in (`..._v3.py`, not an in-place edit). QA shows **all** processed rows (no sample cap), as in-place display grids inside the notebook, never as extra exported tables or files.

**Why:** numbered files keep a clean, revertible history; full-row QA lets him actually inspect the data rather than trust a sample.

**How to apply:** move retired versions to a `superseded/` folder; keep only current code where it runs.

## 7. No long comment headers in code

The top of a code file is a few lines at most. Every explanatory or version note sits **next to (or below) the code section it concerns**, never as an article at the top.

**Why:** a long top-of-file essay buries the code and goes stale; notes next to their code stay accurate and get read in context. (Corrected more than once.)

## 8. Predict run duration

Before any long or expensive run, tell the owner how long you expect it to take. Record the measured actual afterward.

**Why:** he plans around run time and wants to know if a job is hung versus merely slow.

**How to apply:** base the estimate on a measured rate when one exists (for example "~200 rows/min").

## 9. Save feedback to memory the same turn

When the owner gives a correction or something fails, persist it immediately under the home rule: a project lesson's full story goes to `PROJECT.md` Lessons (max 8 lines) and its memory file is a pointer (frontmatter + Why/How-to-apply + "Full story: PROJECT.md § Lessons › <title>"); an owner preference about how to work goes to memory in full. Never two stories of one lesson.

**Why:** a correction that is not persisted gets repeated, which erodes trust - and a correction persisted twice drifts.

## 10. Single source of truth, reconcile not append

One living `PROJECT.md` in two tiers: Tier 1 (goal, scope, the Map, current state, open questions, decisions index) is injected every session by the SessionStart hook under a hard budget; Tier 2 (plan, change log, lessons in full, research notes) is read on demand and may grow. Edits rewrite and delete stale lines rather than pile on, but a line leaves only when its home is named and exists; the Map stays current with every move or archive. Never a second tracking file. The PROJECT.md hooks enforce this.

**Why:** more context beats no context, but bloat loses to optimal context - and every Tier 1 line is paid for on every read.

**How to apply:** this is owned by the `live-document` skill - delegate to it and follow its update algorithm.

## 11. Smallest viable change first; validate in a playground

Row caps, stage toggles, and capped runs against a playground before any full or production run. Production is a one-line switch flipped only after approval.

**Why:** cheap, fast checks catch mistakes before an expensive or irreversible run.

## 12. Ask before assuming

A clarifying question beats a wrong assumption. Surface inferred premises before acting.

**Why:** the cost of a question is one message; the cost of a wrong assumption is redone work. (Also carried by `live-document`; listed here so the profile is self-contained.)

## 13. No guesswork - research and evidence based

Facts that feed a deliverable (mappings, categorizations, numbers) come from real data or an authoritative source, never asserted from model memory.

**Why:** a confident-but-wrong fact in a report is worse than a gap; it misleads silently.

## 14. Division of labor: agent plans and writes files, owner executes

The agent plans in detail and writes code and artifacts as files. The owner runs them in his own environment and reports results back. Assume the agent has no direct access to that environment.

**Why:** the owner controls the execution environment; the agent's job is to make execution foolproof, not to run it.
