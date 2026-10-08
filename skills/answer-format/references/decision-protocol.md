# Open decisions: the decision block

The Summary / Why / What-you-should-do format is for reporting. It is the wrong shape when the
reader has to *choose*: it buries the options in the Why and the choice in the steps. This
reference is the shape for that case. It is the generic twin of a user-level rule
(`~/.claude/rules/decision-protocol.md` in Claude Code); on surfaces that have no rules file
(the desktop app, the web app) it travels inside this skill.

## When it applies

Only when the reader must make an open decision: several viable paths, where their preferences,
risk tolerance or context decide the outcome. Not for factual answers, code output, status
reports, or closed questions with one correct answer. Those keep the normal format.

## Do the weighing first, silently

Before writing: rank the outcomes that matter, work out each option's consequences and rough
likelihood, check whether a hybrid beats the two closest options, and for a half-formed idea
expand it into variants and challenge it. None of that appears in the reply. Only its result does.

## Delivery 1: the option pop-up (Claude Code)

Where an option-chip question tool exists (`AskUserQuestion`), the decision IS the pop-up, with
nothing written before it:

| field | content | limit |
|---|---|---|
| question | `Decision needed: <choice>`, then `Problem: ...` (1-3 sentences, assumption stated), then `Outcome we need: ...` (1-2 sentences, most important first) | 120 words |
| header | one word for the topic | 12 chars |
| options | always exactly 4 chips: A-C = the 3 most feasible options, recommended one FIRST and marked `(Recommended)`; D = always `D. Your own idea`; label `A. <short name>` | label 6 words |
| description | what it is and what it costs or takes; on D: `None of these fits: pick this, press n, and write what you want.` | 40 words |
| preview | on A-C, plain text: `WHAT IT TAKES` (1-3 bullets), `RISKS` (2-3 bullets with high / medium / low), and on the recommended chip `WHY RECOMMENDED` (1-2 lines); on D: `YOUR OWN ANSWER` and one line on how to use it | 60 words, 10 lines |

**Why chip D is never a fourth option:** when chips carry preview boxes, the tool hides its own
"type something" row. Without D, the reader can only answer by picking one of your options first
and adding a note to it, even when none of them fits. If only 2 real paths exist, C is a hybrid or
one the reader may not have considered.

Cut detail before breaking a limit. Every chip is an option, never a question. One pop-up per
decision. Anything extra (background, a longer risk story, how each option would be done) goes
AFTER the pop-up, in the "What you should do" section or a next-actions file, never above it.
Reading the answer: D with a note is the reader's own idea, so plan from their words; D with no
note means ask for the idea in one chat line, no second pop-up; a note on A-C is a change to that
option, so apply it.

**The shape bends to the decision, never the other way round.** The tool allows up to 4 questions
per pop-up, 4 chips per question, and multi-select. Use it within these rules:

- More than 3 viable options: weigh them all (3 to 7) before writing and show only the 3 most
  feasible as A-C; D stays the open slot. Never split one decision across questions to show more.
  "Go deeper" or "show all options" gets the compact block, which lists every option weighed.
- "Include whatever you want" choices: `multiSelect: true`. Previews are unavailable then, so each
  description carries what it is, what it costs and its main risk, and the tool shows its own
  typing row as the open slot (up to 4 item chips, no chip D). Mark recommended items in the
  label and say in the question text which ones you would include and why.
- Several related decisions at once: one question per decision, up to 4 in one pop-up, each with
  its own header and its own chip D; Problem and Outcome go in the first question's text only.
- Two-step decisions: a second pop-up is fine when the first answer opens the next choice; say so
  in the first question.
- Ranking: top pick single-select, then a multi-select for what else to include.
- Any other pop-up with preview boxes, not only open decisions, also ends with `Your own idea`.
- Word limits apply per field, not per decision.

## Delivery 2: the compact block (desktop, web, print mode, subagents)

Where no pop-up exists, or the reader asks to "go deeper" or "show all options", write the same content as one block,
in this order and nothing else, 150-300 words:

```
Decision needed: <the exact choice>

Problem - what has to be decided and why now. 1-3 sentences, assumption stated.
Outcome we need - what a good result looks like, most important first. 1-2 sentences.
Options - 3 to 7
  A. <name> - what it is, what it costs. 1-2 lines.
  B. ...
  C. ... (up to G.)
  Or your own idea - just tell me.
Risks
  - <risk> - high / medium / low
  - ...
Recommendation - LAST. The pick and why, 2-3 sentences; a hybrid if two are close.
```

Never more than 450 words even when asked to go deeper; expand the one part that was asked for.

## Questions before deciding

Ask only when the answer would change the recommendation, and ask in one round. Otherwise state
the assumption inside the Problem and proceed. Do not stall for certainty on a reversible choice.

## Paste text for the desktop preferences box

Add this under the answer-format text in Settings -> Profile -> personal preferences:

```
Exception - open decisions (several viable paths, my call to make): do not use the three
sections above. Give one compact block instead, at most 300 words: "Decision needed: <choice>";
Problem (1-2 sentences); Outcome we need (1 sentence); Options, 3 to 7 (A-G), one or two lines
each with what each costs, ending with "Or your own idea - just tell me."; Risks, 2-4 bullets
each marked high / medium / low; Recommendation last, one or two sentences, clearly marked. Do
the weighing before you write and never show it. If I say "go deeper", expand only the part I
name. Factual answers and status keep the normal format.
```
