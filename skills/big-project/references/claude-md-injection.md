# CLAUDE.md injection payload

The owner's **delta** hard-rules: the rules `live-document` does not already carry. Add these to a project's `CLAUDE.md` hard-rules list (inside the `<!-- live-document:start -->` block if present, otherwise in the project's own hard-rules section).

**Insert only what is absent.** `live-document` already provides: ask-before-assuming, Summary/Reasoning/Steps chunk-delivery, Next Actions files, tidy-root, and no-long-dash. Never duplicate those. Re-running `big-project` self-heals by adding only the missing bullets below.

## Bullets to inject

```markdown
- Answer format: Summary first, then Why, then What you should do LAST - numbered, one action per line, concrete verbs. Nothing to do -> say so plainly. The owner reads the bottom for his next action.
- No unilateral owner decisions: names (tables, files, artifacts), where data lands, and whether to create a thing are the owner's calls. Propose 2-5 options with trade-offs and ask - never pick them yourself.
- Deliverables the owner READS are .md, never .txt (.txt only as a raw copy-paste code payload referenced from an .md) - run reports, analyses, tracking plans. The one exception is the Next Actions handoff, which is HTML only (live-document's rule): never write a .md twin of a Next Actions file, and the old `NEXT STEPS YYYY-MM-DD HHMM - <topic>.md` naming is retired. Before writing a new one, older-dated files move to `next-actions/archive/` (never deleted).
- Walkthroughs are numbered, one click or one input per step: exact button/field names, exact values and where each comes from, and what success looks like. Never compress sub-steps. Over ~10 steps -> deliver in chunks of 5-10, one per turn.
- Ship each code iteration as a NEW numbered file the owner swaps in (`..._v3.py`, never in-place); move retired versions to `superseded/`. QA shows ALL processed rows as in-place display grids, never extra tables or exported files.
- No long comment header at the top of a code file: top = a few lines max; every explanatory or version note sits next to (or below) the code section it concerns.
- Predict run duration before any long or expensive run (use a measured rate when one exists); record the measured actual afterward.
- Save feedback the same turn, under the home rule: a project lesson's full story goes to `project-memory/lessons.md` (its rule line to PROJECT.md Lessons only if it changes how we work) and its memory file is a pointer; an owner preference goes to memory in full. Never two stories of one lesson.
- Smallest viable change first: row caps, stage toggles, and capped runs against a playground before any full or production run; production is a one-line switch flipped only after approval.
- No guesswork: facts that feed a deliverable (mappings, categories, numbers) come from real data or an authoritative source, never asserted from model memory.
- Division of labor: the agent does everything its tools reach (MCPs, connectors, CLIs, scripts on this PC, files): back up, change, verify, then report. The owner acts only where no tool reaches or the decision is his (anything reaching other people, deleting his files, names, other people's systems).
- Context-handoff rule - follow it LITERALLY: before a chat reply that completes work past about 30% context or when the work is done, make PROJECT.md's Current state self-sufficient (`**Next action (on continue):**` = the agent's next steps, first check, files to open; owner-only tasks on a separate `**Waiting on <owner>:**` line), say in the Summary what was done and what comes next, then END the reply with: "1. You can clear the context NOW (`/clear`). Everything is saved in PROJECT.md: what was done and the next action. 2. Then just type: `continue`". A bare `continue` in a fresh session means: read PROJECT.md in full and carry out that next action without asking. Never a paste-ready kickoff message in the chat. Below about 30% with work left, keep working instead.
```

## Applying the payload

1. Read the project `CLAUDE.md`.
2. For each bullet above, check whether an equivalent rule is already present (by meaning, not exact wording). Skip the ones already there.
3. Insert the remaining bullets into the hard-rules list. If a `<!-- live-document:start -->` block exists, add them inside it, after the existing hard-rules bullets and before `<!-- live-document:end -->`.
4. Report in one line which bullets were added and which were already present.
