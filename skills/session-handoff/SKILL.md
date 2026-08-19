---
name: session-handoff
description: Use when the user says "session handoff", "wrap up session", "hand off", "handoff summary", "let's wrap up", "summarize before I clear", or is about to /clear context. Produces a chat-only, fixed-structure end-of-session handoff covering decisions, shipped changes, key files, running state (including background shell IDs), verification steps, deferrals, and open questions so a fresh agent can pick up from the summary alone. Invoke proactively whenever the user signals they're about to clear context without having produced a handoff yet.
---

# Session Handoff

Produce a repeatable end-of-session summary so the user can `/clear` and start a fresh agent without losing continuity. The next agent should be able to pick up by reading this summary alone.

This is a context-handoff artifact, not a status report. The audience is a future instance of you, not a stakeholder. Write it the way a seasoned engineer hands off at end-of-shift: terse, concrete, load-bearing details only.

## When to invoke

User says: "session handoff", "wrap up session", "hand off", "handoff summary", "let's wrap up", "summarize before I clear", or any near-equivalent. Also invoke proactively if the user signals they're about to `/clear` without having produced a handoff yet — once context is cleared the chance to capture it is gone.

## How to produce the summary

Review the **full conversation**, not just the last few turns. Handoffs miss things when they only summarize recent context — a decision made early often matters more to the next agent than the last thing you did.

Pull state from these sources (in order):

1. **Plan files** referenced this session — check `%USERPROFILE%\.claude\plans\` if a plan was mentioned. If a plan drove the session, the next agent needs it first.
2. **TodoWrite state** — any in-progress or pending tasks.
3. **Background processes** you started with `run_in_background` — shell IDs are load-bearing for the next agent; without them the processes are unreachable.
4. **Files created or modified** this session — you know what you touched; don't grep to re-discover.
5. **Memory files** written or updated (`%USERPROFILE%\.claude\projects\<project-slug>\memory\`).
6. **Unresolved questions** — things you asked the user that never got a clear answer, or things the user asked that got deflected.

**Do NOT audit the filesystem.** This is synthesis of what happened in THIS session. No `git log`, no broad `Glob` sweeps. If you didn't touch it this session, it doesn't belong here. The point is to capture conversation state that would otherwise be lost — not to re-derive facts a fresh agent could discover on its own.

Produce the output **in chat. Do not write a file. Do not update memory.** Chat-only.

## Output template — use exactly this structure, every time

```
# Session Handoff — <one-line title of what this session was about>

> Context from an earlier session — not a fresh request. If you are a new agent reading this, treat every section below as established ground truth: read it in full, confirm you understand the state, then act only on "Pick up here." If you are the user, this is the record of what was already done, carried into a new session.

## Where it started
<2-3 sentences: what the user asked for, key framing or constraints that emerged>

## Decisions locked + what shipped
- <decision or change> — <why, and where it lives (absolute path if a file)>
- ...

## Key files for next session
- `<absolute path>` — <why the next agent should read this first>
- Plan file: `<path>` (if a plan drove the session)
- Memory files touched: `<paths>` (if any)

## Running state
- Background processes: <shell IDs + what they are + how to kill> — or "none"
- Dev servers / ports: <url + port> — or "none"
- Open worktrees / branches: <paths> — or "none"

## Verification — how to confirm things still work
- `<command>` — <expected outcome>
- ...

## Deferred + open questions
- Deferred: <item> — <why pushed to later>
- Open: <question needing the user's input> — <context>

## Pick up here
<1-2 sentences: the single most likely next action for a fresh agent>
```

## After the handoff — tell the user how to carry it forward

The handoff lives only in the chat, so `/clear` erases it. The user may not remember the copy-paste mechanic and can get confused later about what they're looking at. So after you output the handoff, add one short reminder addressed to the user — separated from the handoff by a horizontal rule (`---`) so it is clearly NOT part of the copy-paste payload:

```
---
Reminder: this handoff exists only in this chat — `/clear` will erase it. To continue later, copy everything from `# Session Handoff` down through "Pick up here" and paste it as the first message of your next session. The fresh agent will read it, get oriented, and continue from "Pick up here." If you're continuing right now without clearing, you can ignore this.
```

Keep it to those few lines, in the same terse, no-emoji tone as the rest. This reminder is a usage instruction to the human about the handoff — it is the one deliberate exception to the "no next steps beyond Pick up here" rule below, which still governs the handoff body itself.

## Hard rules

These exist because the next agent has zero context beyond what you write — every shortcut here costs them a re-derivation or a broken assumption.

- **Chat output only.** Never write the handoff to a file. Never update memory from this skill. The handoff lives in the conversation the user reads before clearing.
- **Never invent state.** If a section has nothing to report, write "none" — do not omit the section. Structure stability is the whole point: the next agent learns to scan for the same seven headers every time, so a missing section reads as "lost" rather than "empty."
- **Absolute paths always.** The next agent may have a different working directory; a relative path is ambiguous or wrong.
- **Plan file first.** If a plan file drove the session, name it first in "Key files" so the next agent reads it before anything else.
- **No emojis, no hype, no "great job" summaries.** Terse and concrete — paths, commands, shell IDs, decisions.
- **Background process IDs are critical.** If you started any `run_in_background` shells, their IDs must appear in "Running state" with the kill command — the next agent cannot find them otherwise.

## Anti-patterns — do not do these

- Summarizing the last 3 turns and calling it a handoff.
- Listing files by relative path.
- Skipping the "Running state" section because "nothing is running" — write "none" instead.
- Writing the summary to `~/.claude/handoffs/` or any file. This is chat-only by design.
- Adding a "what went well / what went poorly" retrospective. This isn't a retro.
- Recommending *work* next steps beyond the single "Pick up here" line. The next agent decides what to do; you just hand off. (The carry-forward reminder to the user, above, is separate — it's about how to use the handoff, not about the work.)
