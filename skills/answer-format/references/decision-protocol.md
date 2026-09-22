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
| options | 3-4 chips, recommended one FIRST and marked `(Recommended)`; label `A. <short name>` | label 6 words |
| description | what it is and what it costs or takes | 40 words |
| preview | plain text: `WHAT IT TAKES` (1-3 bullets), `RISKS` (2-3 bullets with high / medium / low), and on the recommended chip `WHY RECOMMENDED` (1-2 lines) | 60 words, 10 lines |

Cut detail before breaking a limit. Every chip is an option, never a question. One pop-up per
decision. Anything extra (background, a longer risk story, how each option would be done) goes
AFTER the pop-up, in the "What you should do" section or a next-actions file, never above it.

## Delivery 2: the compact block (desktop, web, print mode, subagents)

Where no pop-up exists, or the reader asks to "go deeper", write the same content as one block,
in this order and nothing else, 150-300 words:

```
Decision needed: <the exact choice>

Problem - what has to be decided and why now. 1-3 sentences, assumption stated.
Outcome we need - what a good result looks like, most important first. 1-2 sentences.
Options
  A. <name> - what it is, what it costs. 1-2 lines.
  B. ...
  C. ...
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
Problem (1-2 sentences); Outcome we need (1 sentence); Options A-C (D) one or two lines each with
what each costs; Risks, 2-4 bullets each marked high / medium / low; Recommendation last, one or
two sentences, clearly marked. Do the weighing before you write and never show it. If I say
"go deeper", expand only the part I name. Factual answers and status keep the normal format.
```
