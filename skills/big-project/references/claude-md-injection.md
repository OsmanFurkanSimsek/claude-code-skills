# CLAUDE.md injection payload

The owner's **delta** hard-rules: the rules `live-document` does not already carry. Add these to a project's `CLAUDE.md` hard-rules list (inside the `<!-- live-document:start -->` block if present, otherwise in the project's own hard-rules section).

**Insert only what is absent.** `live-document` already provides: ask-before-assuming, Summary/Reasoning/Steps chunk-delivery, Next Actions files, tidy-root, and no-long-dash. Never duplicate those. Re-running `big-project` self-heals by adding only the missing bullets below.

## Bullets to inject

```markdown
- Answer format: Summary first, then Why, then What you should do LAST - numbered, one action per line, concrete verbs. Nothing to do -> say so plainly. The owner reads the bottom for his next action.
- No unilateral owner decisions: names (tables, files, artifacts), where data lands, and whether to create a thing are the owner's calls. Propose 2-5 options with trade-offs and ask - never pick them yourself.
- Deliverables the owner reads or acts on are .md, never .txt (.txt only as a raw copy-paste code payload referenced from an .md). Name action docs `NEXT STEPS YYYY-MM-DD HHMM - <topic>.md`; newest is live, older gets a `> SUPERSEDED ...` banner. Keep every old dated file.
- Walkthroughs are numbered, one click or one input per step: exact button/field names, exact values and where each comes from, and what success looks like. Never compress sub-steps. Over ~10 steps -> deliver in chunks of 5-10, one per turn.
- Ship each code iteration as a NEW numbered file the owner swaps in (`..._v3.py`, never in-place); move retired versions to `superseded/`. QA shows ALL processed rows as in-place display grids, never extra tables or exported files.
- No long comment header at the top of a code file: top = a few lines max; every explanatory or version note sits next to (or below) the code section it concerns.
- Predict run duration before any long or expensive run (use a measured rate when one exists); record the measured actual afterward.
- Save feedback to memory the same turn: when the owner corrects course or something fails, record what was tried, what failed, and the lesson.
- Smallest viable change first: row caps, stage toggles, and capped runs against a playground before any full or production run; production is a one-line switch flipped only after approval.
- No guesswork: facts that feed a deliverable (mappings, categories, numbers) come from real data or an authoritative source, never asserted from model memory.
- Division of labor: the agent plans and writes code/artifacts as files; the owner executes in his environment and reports results back. Assume no direct access to that environment.
- Context-handoff rule - follow it LITERALLY: EVERY chat reply that completes work must END with this filled-in block: "1. You can clear the context NOW. Everything important is saved in PROJECT.md and <the live walkthrough file>. 2. Start a fresh session and paste exactly this message:" followed by the exact paste-ready kickoff message for the next agent. The block closes the reply itself, not only the walkthrough file.
```

## Applying the payload

1. Read the project `CLAUDE.md`.
2. For each bullet above, check whether an equivalent rule is already present (by meaning, not exact wording). Skip the ones already there.
3. Insert the remaining bullets into the hard-rules list. If a `<!-- live-document:start -->` block exists, add them inside it, after the existing hard-rules bullets and before `<!-- live-document:end -->`.
4. Report in one line which bullets were added and which were already present.
