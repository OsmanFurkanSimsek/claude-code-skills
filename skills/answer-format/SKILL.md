---
name: answer-format
description: Use when the user types /answer-format, asks how replies should be structured ("answer format", "response style", "how should you answer me", "use my format", "answer preference"), or wants to change those preferences. ALSO apply proactively to any substantive reply - one that reports work done, explains a finding, compares options, gives a status update, or ends in a recommendation. Structures the reply as Summary, then Why, then What you should do LAST, so the reader's next action always sits at the bottom of the message where their eyes already are, and keeps that step list alive across the whole conversation instead of dropping it when a follow-up question comes in. Composes with big-project. Do NOT use for a one-line factual answer, a verbatim code block or file the user asked for, a yes/no confirmation, a quick lookup, or when the user has explicitly asked for a different structure.
---

# answer-format

## What this is

One rule for how to end a message, applied consistently: **Summary, then Why, then What you should do - and the actions go last.**

Most assistant replies bury the reader's next action somewhere in the middle, or open with a wall of steps before the reader knows what happened. Both force scrolling. This format fixes the position of every part, so the reader learns where to look and stops re-reading.

The order is not decoration. It follows how someone actually reads a reply they asked for:

1. **Summary** answers *"what happened?"* - the thing they most want to know.
2. **Why** answers *"should I trust it?"* - available if they want it, skippable if they don't.
3. **What you should do** answers *"whose turn is it, and what do I do?"* - the thing they act on, placed at the bottom where the eye lands when a message finishes.

Because the actions sit last, the reader can scroll **up** for reasoning only when they want it. Actions-first forces scrolling in both directions on every message.

## The three sections

Use these as literal headings. Consistency is most of the value - the reader should be able to jump to the bottom without reading a word.

### 1. Summary

What happened, in plain words. A few sentences. No jargon, no tool names, no file paths unless the path *is* the answer.

Write it for someone who has not been watching. If the reply is about work that was done, say whether it worked. If something failed, say that here - never save bad news for the bottom.

### 2. Why

The reasoning, findings, numbers, and trade-offs behind the summary. This is where detail belongs: what was measured, what was ruled out, what was chosen over what, and what it cost.

This section earns the reader's trust, so it is the right place for honesty about limits: what was not checked, what is assumed, what might still be wrong. Length is free here - a reader who does not care skips it, and one who does gets the whole picture.

Use sub-headings when it runs long. Tables and short code blocks are fine here; they are not fine in the other two sections.

### 3. What you should do

**Last. Always at the very bottom.** Nothing goes after it - no sign-off, no summary of the summary, no extra caveat.

- **Numbered list, one action per line.** Two actions on one line is the most common way this format breaks.
- **Start each line with a concrete verb**: run, open, click, copy, paste, check, read, tell me, answer, decide.
- **Plain language.** If a line needs a term the reader may not know, define it in the Why section, not here.
- **Say who acts.** If a step is something you will do, do not put it here - this list is only the reader's work.
- **Commands go in a code block** on their own line so they can be copied without retyping.

If there is nothing for them to do, say so plainly:

> Nothing to do - this is finished.

Never leave it ambiguous whose turn it is. A missing actions section reads as "I forgot", not "you are done".

## Two shapes

Not every reply is a work report. Pick the shape from what was asked.

**Work was done** (a build, a fix, an investigation, a change): use all three sections as above.

**A pure question was asked** ("what is the difference between X and Y?", "does this repo use Z?"): there is no work for the reader to do, so the steps section would be noise. Instead:

- Lead with a **1-3 sentence direct answer** - the TLDR.
- Then the detail, at whatever length the question deserves.
- No numbered steps. If genuinely nothing follows, one plain line saying so is enough; if the answer naturally suggests a next move, offer it as a sentence, not a numbered list.

The rule behind both shapes: **the reader should never have to hunt for what to do next, and never be handed steps they did not need.**

## Big work goes in chunks

When the reader's part is long, do not hand over twenty steps at once. Give **5 to 10 steps**, stop, and wait for them to come back. Then give the next chunk.

Long lists get abandoned partway, and a reader halfway through step 14 has no way to tell you where they got stuck. Chunking keeps every hand-off small enough to finish and to report on.

## The action list is live across the whole conversation

The steps you hand over are not a per-message artifact. They are **one running checklist that the conversation owns** until the work is finished. Treat it as state you carry, not as something regenerated from scratch each turn.

This matters most in the case that looks harmless: you give five steps, and the reader comes back with a question about step 3. If you answer only the question, the list is gone. The reader now has to scroll back through the conversation to find out what was left, which is exactly the hunting this format exists to prevent - and worse, they may think answering the question *was* the remaining work.

**When the reader asks something mid-list:**

1. Answer the question first. That is what they asked, and it belongs at the top under Summary.
2. Then re-show the whole list under `## What you should do`, with status marked.

Mark status inline so one glance shows where things stand:

> ## What you should do
>
> 1. ~~Install the CLI~~ - done
> 2. ~~Open a new terminal~~ - done
> 3. **Log in** with `acme auth login` - you are here. It prints a code, which you paste into the browser page it opens.
> 4. Copy the workspace ID from the dashboard.
> 5. Tell me the ID and I will finish the setup.

**Keep the original numbers stable while a list is live.** The reader says "step 3" and means the third thing you told them. Renumbering mid-flight silently changes what their words refer to. If the plan genuinely changes - a step turns out to be unnecessary, or two new ones appear - reissue the whole list renumbered cleanly from 1, and say in the Summary that the steps changed and why. Stable numbering while live; a clean renumber when the plan actually changes.

**When an answer changes the later steps, say so explicitly.** If explaining step 3 reveals that steps 4 and 5 are now wrong, that is the headline, not a footnote. Put it in the Summary and reissue the corrected list.

**Stop carrying the list when it is genuinely done** - the reader confirms completion, the work is finished, or the conversation has clearly moved to something else. Then close it out with "Nothing to do - this is finished" rather than repeating a list of struck-through items forever.

## Working with other skills

This skill governs **the shape of a reply**. It deliberately owns nothing else, so it can sit underneath skills that own a workflow without fighting them.

**With `big-project`.** That skill carries this format as one rule among many; this skill is the full version of that one rule. They compose - `big-project` owns the working style and the project plumbing, `answer-format` owns how each reply is laid out.

One interaction needs care. `big-project` requires every completing reply to end with a two-step context-handoff block ("you can clear context now" / "paste this into a fresh session"), while this skill says nothing comes after the actions. That is not a real conflict once you see what the handoff block is: **two actions for the reader**. So it does not go *after* the actions section - it goes *inside* it, as the last numbered steps:

> ## What you should do
>
> 1. Open the dashboard and confirm the new chart renders.
> 2. Tell me if the colours need changing.
> 3. You can clear the context now - everything important is in `PROJECT.md` and `walkthrough-2026-08-19.md`.
> 4. Start a fresh session and paste exactly this:
>    ```
>    Continue the dashboard work. Read PROJECT.md first, then walkthrough-2026-08-19.md.
>    Next up is the colour pass in section 4.
>    ```

Both rules are honoured literally: the handoff is the last thing in the message, and nothing follows the numbered list.

**With `live-document`, `e2e`, and `session-handoff`.** Those own documents and phase state, not reply shape, so this skill applies on top without adjustment. The one exception is `session-handoff`: its output is a fixed seven-section template the reader asked for verbatim, so let that template stand rather than wrapping it in Summary / Why / What you should do.

## What breaks this format

These are the failure modes worth watching for, and why each one hurts:

| Mistake | Why it matters |
|---|---|
| Actions placed before the reasoning | Forces scrolling up and down; the whole point is a fixed bottom position. |
| Something added after the actions | The reader stops at the last numbered line. Anything below it is invisible. |
| Two or three actions crammed onto one line | They do one and think they are done. One line, one action. |
| Steps listed when there is nothing to do | Trains the reader to ignore the section. Say "Nothing to do" instead. |
| Jargon in Summary or in the steps | Both sections are for scanning. Detail and terminology belong in Why. |
| Bad news held back until the bottom | Erodes trust. If it failed, the Summary says it failed. |
| Steps mixing your work and theirs | They cannot tell which lines are their job. The list is theirs alone. |
| Hedging that hides the outcome | "Should mostly work now" tells them nothing. Say what was verified and what was not. |

## Formatting notes

- **Never use the long-dash character.** Use a hyphen or rewrite the sentence.
- Headings are `## Summary`, `## Why`, `## What you should do`. Keeping the words stable is what lets the reader skip straight to the bottom.
- Bold sparingly, for the one phrase in a paragraph that carries the point.
- This format governs prose replies. It does not apply inside a file you are writing, a commit message, or a code block the reader asked for verbatim.

## Worked examples

Read `references/examples.md` for full before-and-after examples covering a work report, a pure question, a failure report, and a chunked hand-off. Reading one example teaches the shape faster than re-reading the rules.

## Using this outside Claude Code

A skill fires when the model judges it relevant, which is right for most skills but weak for an always-on style rule. For reliable everyday use, put the format where it is always loaded:

- **Claude Code:** `~/.claude/CLAUDE.md` (global) or a project `CLAUDE.md`.
- **Claude desktop and web:** the personal-preferences box in Settings.

`references/desktop-setup.md` has paste-ready text for both, and explains when to reach for the skill instead.
