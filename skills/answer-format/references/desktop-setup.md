# Using this format everywhere

A skill fires when the model judges it relevant. That is the right design for most skills, but it is a weak fit for an always-on style rule: a rule that should apply to *every* substantive reply should not depend on a per-message judgment call.

So use both mechanisms, for different reasons:

| Where | Reliable mechanism | What the skill adds |
|---|---|---|
| Claude Code | `~/.claude/CLAUDE.md` (global) or a project `CLAUDE.md` | The reasoning and worked examples, on demand via `/answer-format` |
| Claude desktop and web | Personal preferences in Settings | Same, plus a portable copy that travels with the skill |

The always-loaded file is what makes the format actually happen. The skill is where the *why* lives, so the rule can be understood and adjusted rather than just obeyed - and so it can be shared with someone else.

---

## Claude desktop and web

Settings -> Profile -> "What personal preferences should Claude consider in responses?"

Paste this:

```
Structure every substantive reply in this order, and never reorder it:

1. Summary - what happened, in plain words. A few sentences, no jargon. If
   something failed, say so here, not at the bottom.
2. Why - the reasoning, findings, numbers, and trade-offs. Detail belongs here.
   Say what you did not check or are assuming.
3. What you should do - LAST, at the very bottom, with nothing after it.
   Numbered, one action per line, starting with a concrete verb (run, open,
   click, copy, check, tell me, decide). Commands go in their own code block.
   Only list work that is mine, not yours. If there is nothing for me to do,
   write "Nothing to do - this is finished" so it is never ambiguous whose
   turn it is.

I read the bottom of a message for my next action, so actions-first makes me
scroll up and down. Reasoning sits above the actions so I can scroll up only
when I want it.

If I only asked a question and there is nothing for me to do, skip the numbered
steps and lead with a 1-3 sentence direct answer instead.

If my part runs long, give me 5-10 steps, then stop and wait for me rather than
handing over twenty at once.

Never use the long-dash character. Use a hyphen or rephrase.
```

Preferences apply to new conversations. An open chat keeps the old ones.

---

## Claude Code

Put the same rule in `~/.claude/CLAUDE.md` to make it global, or in a project's `CLAUDE.md` to scope it to one repo. Global is the right default for a style rule.

The condensed version, which is what belongs in an always-loaded file:

```markdown
# Answer format (every reply)

Order every reply, and never reorder it:

1. **Summary** - what happened, in plain words. A few sentences, no jargon.
   Bad news goes here, not at the bottom.
2. **Why** - reasoning, findings, numbers, trade-offs. Detail belongs here,
   including what was not checked.
3. **What you should do** - LAST, nothing after it. Numbered, one action per
   line, concrete verbs (run, open, click, copy, check, answer). Only the
   user's work, not yours. Nothing to do -> say "Nothing to do - this is
   finished" plainly.

Rationale: the user reads the bottom of the message for the next action.
Actions-first forces scrolling both ways.

Pure question with nothing to do -> skip the steps, lead with a 1-3 sentence
answer. Long hand-offs -> 5-10 steps per turn, then wait.

Never use the long-dash character.
```

Keep this short. An always-loaded file is re-read on every session, so every line is paid for repeatedly - the reasoning and the examples belong in the skill, not here.

---

## Installing the skill

**Claude Code** - copy the folder into your skills directory:

```
Windows   %USERPROFILE%\.claude\skills\answer-format\
macOS     ~/.claude/skills/answer-format/
Linux     ~/.claude/skills/answer-format/
```

Restart Claude Code, then type `/answer-format` to check it loaded.

**Claude desktop** - upload `answer-format.skill` in the desktop app's skill settings. Do not copy the folder; the desktop app expects the packaged bundle.

---

## Adapting it for someone else

Everything here is one person's preference, not a universal standard. The parts most worth reconsidering for a different reader:

- **The three section names.** Any stable set works. Stability is the value, not the specific words.
- **Actions last.** This suits a reader who acts on messages. Someone who mainly skims for conclusions may want the summary to carry more and the actions to be a single line.
- **Chunk size.** 5-10 steps suits someone working through a hand-off at a keyboard. Adjust to how much your reader does in one sitting.
- **The no-long-dash rule.** House style, nothing more.

What should survive any adaptation is the underlying idea: **fix the position of the reader's next action so they never have to hunt for it, and never hand them steps they did not need.**
