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
1. You can clear the context NOW (`/clear`). Everything is saved in PROJECT.md: what was done and the next action.
2. Then just type: `continue`
```

PROJECT.md's `**Next action (on continue):**` names this file, so the next agent opens it by itself.

**Chunking:** more than ~10 steps -> deliver 5-10 at a time, one chunk per turn; wait for the owner to confirm the chunk is done or report what failed before sending the next. Update `PROJECT.md` (chunk statuses in Plan / workstreams, active chunk in Current state) before the next chunk, per `live-document`.

---

## 2. Two-step context-handoff block (ends every completing reply)

Every chat reply that finishes work ends with this. It also closes every walkthrough file, but the file alone is not enough - the block must be the end of the chat reply itself. There is no kickoff message to copy (owner, 2026-09-27): the next action lives in PROJECT.md, and a bare `continue` starts it.

```markdown
1. You can clear the context NOW (`/clear`). Everything is saved in PROJECT.md: what was done and the next action.
2. Then just type: `continue`
```

### Filled example (PROJECT.md side, written BEFORE the block)

```markdown
**Next action (on continue):** run the capped 500-row validation of source B (Part C of
`next-actions/2026-07-22_15-30-next-actions.html`); first check the column map in
`project-memory/source-b-mapping.md` still matches the model; predict the run time before starting.
**Waiting on the owner:** grant the service account read access to source B.
```

And the reply's Summary says it in plain words: "Source B's columns are mapped. Next, after `continue`: the capped 500-row validation run."

### What makes PROJECT.md's next action good

- A fresh agent with zero chat context can act on it: steps in order, the first check, every file to open by path.
- Agent work and owner-only work are on separate lines, so `continue` never waits on the owner by accident.
- It is rewritten in place every handoff (live-document: Current state describes only now).

### What `continue` means to the next agent

A bare `continue` (or "go on", "carry on") as the first message of a fresh session: read PROJECT.md in full,
open the files its next action names, carry out the agent steps without asking what to do, and stop at the end
of that chunk or at the first owner decision.

### Relationship to `session-handoff`

The two-step block is the lightweight close of an ordinary reply. For an explicit "wrap up session" / "summarize before I clear", use the `session-handoff` skill instead - it produces the full seven-section end-of-session summary. The two are complementary: the block for every reply, `session-handoff` for a deliberate wrap-up.
