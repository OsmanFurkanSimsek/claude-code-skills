# Walkthrough and handoff templates

Two templates the profile relies on: the numbered walkthrough (rule 5) and the two-step context-handoff block (rule 2).

---

## 1. Walkthrough template

Use for any work the owner must do himself. **The walkthrough IS `live-document`'s Next Actions file**: one interactive, self-contained `next-actions/<YYYY-MM-DD_HH-MM>-next-actions.html` per handoff (HTML template in `live-document/references/next-actions-template.md`). Never write a `.md` twin next to it and never a separate `NEXT STEPS ... .md` - the owner retired that naming on 2026-09-02 ("Why do you create both MD and HTML for Next Actions? ... HTML files are enough."). Every handoff gets a NEW dated file; keep every old one - the date-time prefix says which is live, so no SUPERSEDED banner is needed. The outline below is the CONTENT the HTML carries, in this order.

```markdown
# <topic> - YYYY-MM-DD HH:MM

## Summary (plain words)
<1-2 sentences: what we are doing.>

## Why
<Plain words: why we are doing it. Alternatives considered and why this path won.>

## What you should do

### Part A - <sub-goal>
1. <One click or one input. Exact button/field name. Exact value to type, and where it comes from.>
   Success looks like: <what the owner should see.>
2. ...

### Part B - <sub-goal>
1. ...

## Context handoff (per the standing rule)
1. You can clear the context NOW. Everything important is saved in PROJECT.md and this file.
2. Start a fresh session and paste exactly this message:
   > <exact paste-ready kickoff message for the next agent>
```

**Chunking:** more than ~10 steps -> deliver 5-10 at a time, one chunk per turn; wait for the owner to confirm the chunk is done or report what failed before sending the next. Update `PROJECT.md` (chunk statuses in Plan / workstreams, active chunk in Current state) before the next chunk, per `live-document`.

---

## 2. Two-step context-handoff block (ends every completing reply)

Every chat reply that finishes work ends with this, filled in. It also closes every walkthrough file, but the file alone is not enough - the block must be the end of the chat reply itself.

```markdown
1. You can clear the context NOW. Everything important is saved in PROJECT.md and <the live walkthrough file>.
2. Start a fresh session and paste exactly this message:
   > <exact paste-ready kickoff message for the next agent>
```

### Filled example

```markdown
1. You can clear the context NOW. Everything important is saved in PROJECT.md and `next-actions/2026-07-22_15-30-next-actions.html`.
2. Start a fresh session and paste exactly this message:
   > Continue the project in this folder. Read PROJECT.md in full, then open the newest file in `next-actions/`. We just finished mapping source B's columns onto the existing model; the next action is the capped 500-row validation run described in Part C of that walkthrough. Predict the run time before I start it.
```

### What makes the kickoff message good

- It points the next agent at `PROJECT.md` and the live walkthrough by name.
- It states the single next action in one line.
- It is self-contained: a fresh agent with zero prior context can act on it.

### Relationship to `session-handoff`

The two-step block is the lightweight close of an ordinary reply. For an explicit "wrap up session" / "summarize before I clear", use the `session-handoff` skill instead - it produces the full seven-section end-of-session summary. The two are complementary: the block for every reply, `session-handoff` for a deliberate wrap-up.
