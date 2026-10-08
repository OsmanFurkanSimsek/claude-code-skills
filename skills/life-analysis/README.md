# life-analysis

A **template** skill for Claude Code that turns your personal life-tracking data in Notion (a
daily tracker, weekly/periodic reviews, and whatever side databases you keep) into ONE
self-contained, interactive HTML life-analysis report - trends, correlations, qualitative
synthesis of your journals, and a closing mentor section that tells you what to actually do.

## What problem it solves

If you track your life in Notion, the data mostly just sits there. Ad-hoc questions ("does
meditation actually help my stress?") get ad-hoc, unreliable answers, and nobody re-reads six
months of journal entries. This skill makes the review repeatable: one command produces a full
report with the numbers computed properly (moving averages, correlation matrix with n, behavior
splits, fill rates), the writing distilled into pattern-level synthesis instead of a chronology,
and every previous insight re-tested against fresh data rather than restated.

The parts that made the seed pipeline work all ship here:

- a **strict read-only rule** and a personal-data-never-in-git rule
- **date-identity cleaning** - trusting date properties over human-typed week/period titles,
  which duplicate and drift in every real workspace
- **"distill, don't narrate"** - qualitative sections are 4-6 pattern bullets plus a one-line
  summary, never day-by-day retelling, never pasted agent output
- **hypotheses, not facts** - previous runs' insights are re-tested each run; a null result
  that stays null is reported as a finding
- the **"So What / Then What" mentor section** - what I see / what it means / what you should
  do, plus a "beliefs your own data refutes" card, because the report is read bottom-up for
  next actions
- a verified **self-contained HTML** build: no CDN, inline-SVG charts, light/dark theming,
  structural checks before delivery

## Why this ships as a template, not a ready skill

The pipeline is generic; the data map is not. Your database IDs, your exact field names, your
scales and checkboxes and voice-dictation quirks are the entire extraction layer - and a real
person's map is also deeply private (health fields, journal categories, names). So the pipeline
ships complete and `references/data-sources-template.md` is a fill-in skeleton.

## Layout

```
life-analysis/
  SKILL.md                              # the 8-phase pipeline, hard rules, re-run behavior
  README.md                             # this file
  references/
    data-sources-template.md            # FILL IN: your databases, fields, quirks, recipes
    report-blueprint.md                 # the report skeleton, design system, verification
```

## How to adapt it

1. Fork this folder into your own `~/.claude/skills/` (rename it if you like).
2. Fill in `references/data-sources-template.md`: your collection IDs, every field name exactly
   as Notion spells it, and - most importantly - the quirks section (duplicate rows? unreliable
   titles? which field actually holds what?). The quirks are where analyses silently break.
3. Skim `references/report-blueprint.md` and rename/drop sections to match what you actually
   track. Keep the mentor section - it is the payoff.
4. Run it once on a short period (a month) and check the numbers by hand against Notion before
   trusting a full-history run.

## Dependencies

Needs the Notion MCP connector with database query access, plus Python available in the session
for cleaning, metrics, and the data-injection step. The qualitative phase uses Claude Code's
Agent tool when available and degrades to sequential reading without it.

## Privacy note

Everything this skill touches is personal data. It is read-only by rule, keeps all intermediate
files in the session scratchpad, and the report is delivered to you as a file - commit it
nowhere, and keep your filled-in data-sources map out of any public repository.
