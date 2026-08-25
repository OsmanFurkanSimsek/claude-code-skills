---
name: life-analysis
description: Generate a comprehensive life-analysis HTML report from your personal life-tracking data in Notion (daily tracker, weekly reviews, periodic reviews plus side databases). Use when the user asks for a life analysis or life report in any wording - "how is my life going, analyze it", "run the life analysis", "refresh the report with current data" - or asks to re-run it. This is a TEMPLATE - fill in references/data-sources-template.md with your own databases before it can read anything. Do NOT use for single-fact lookups or writes to Notion, for analyzing one database in isolation, or when the user only wants a quick verbal summary without the HTML report.
---

# Life Analysis (template)

> This skill was seeded from a real, personal quantified-self reporting pipeline (a daily
> tracker, weekly and periodic reviews, and half a dozen side databases in Notion, compiled into
> one interactive HTML report) and generalized into a template. The PIPELINE ships complete -
> extraction, cleaning, the quantitative metric set, qualitative synthesis rules, the report
> blueprint, verification. The DATA MAP does not: your databases, fields, and metrics live in
> `references/data-sources-template.md`, which is a fill-in skeleton. The skill can read nothing
> until you fill it in.

Produces ONE self-contained, interactive HTML report from your Notion life data: quantitative
trends, correlations, and qualitative synthesis of journals, goals, habits, and the state of
your whole workspace - ending with a mentor-voiced "so what / then what" section, because the
report's real value is what you do next, not the charts.

## Hard rules

1. READ-ONLY. This skill never writes, edits, or deletes anything in Notion.
2. Personal data never enters a git repository. All intermediate files and the report live in
   the session scratchpad; deliver the file to the user, commit it nowhere.
3. Qualitative sections are SYNTHESIS, not chronology. Every qualitative topic gets 4-6
   pattern-level bullets in simple language plus a one-sentence summary; dated examples appear
   only as short parenthetical evidence. Never paste an agent's raw output into the report -
   distill it. (The month-by-month story section is the single exception: one short narrative
   card per month.)
4. Sensitive handling: journals contain private material - health, relationships, family, money.
   Write about it factually and respectfully; never quote crude language; and if any pages hold
   credentials, put them out of scope entirely and never open them.
5. Write the report in the user's language, and honor their formatting preferences throughout.

## Environment detection

- **Claude Code** (Bash + Write + Agent tool available): full pipeline as written; parallel
  subagents for the qualitative reading; verify over a local HTTP server.
- **Claude Desktop / a sandboxed environment** (no Agent tool): same pipeline, but read the
  qualitative digests yourself sequentially (they are pre-chunked small files) and deliver
  through the environment's file-output mechanism.
- Both need the Notion connector. If Notion tools are missing, say so and stop - never simulate
  data.

## Pipeline (8 phases)

Read `references/data-sources-template.md` before Phase 1 and
`references/report-blueprint.md` before Phase 6.

### Phase 0 - Discover
Count rows + MIN/MAX dates for the core trackers. Analysis period: first tracked day to today,
unless the user names a period. State row counts in the report footer and verify final numbers
against them. If a previous report exists in the conversation, note its cutoff date so the new
report can call out what changed since.

### Phase 1 - Extract
Pull core data with Notion's SQL-mode queries in date slices (results paginate; slice by date
range rather than re-querying smaller). Oversized results auto-save to files - parse those with
Python. If SQL mode hits its usage quota mid-session, fall back to view-mode queries (quota-free)
or wait; the mechanics are in the data-sources file.

### Phase 2 - Clean
Dedupe rows by their date identity (average numerics, keep all text). Trust date properties over
human-typed titles - week/period titles drift and duplicate. Write clean `daily.json` /
`weekly.json` to the scratchpad. Record every dedupe and gap for the data-quality section.

### Phase 3 - Quantitative analysis
Compute the standard metric set (see the data-sources file's recipes): monthly averages, 7-day
moving averages, a correlation matrix across your scores, day-of-week effects, behavior splits
(e.g. planned-vs-unplanned days, habit-vs-no-habit days), activity distributions, field
fill-rates, and body/health series if tracked. Save everything chart-ready into
`chart_data.json`.

### Phase 4 - Qualitative analysis
Export field-grouped digest files (goals/problems, learning/curiosity, social notes, the daily
narrative, weekly reflections - whatever your fields are), then analyze each with a
per-digest agent prompt: state the file path and format, the exact date-range slice, a numbered
output structure (month-by-month narrative, recurring themes with approximate counts, turning
points, category counts, short dated quotes, synthesis), and a transcription-noise warning if
your entries are voice-dictated. Demand honesty: "do not invent; report only what you counted."
Then apply hard rule 3: distill every agent report into pattern-level synthesis.

### Phase 5 - Workspace-wide analysis
Pull your task backlogs and goal databases for the period, plus a created-date search for new
pages in your notes areas. Produce: tasks opened/done per month, a channel-liveness map (which
databases are alive, dormant, repurposed - with row counts as evidence), backlog-vs-journal
consistency, goal staleness. Cross-compare with life metrics (e.g. task volume vs stress).

### Phase 6 - Build the report
One self-contained HTML file per `references/report-blueprint.md`: section skeleton, chart
inventory, a validated palette, CSS variables for light/dark, inline-SVG charts drawn by vanilla
JS, data embedded as JSON and injected by replacing a placeholder with Python. The report ENDS
with the mandatory "So What / Then What" mentor section (blueprint's final section): advice cards
grounded in this run's findings, a "beliefs your own data refutes" card, and a closing mentor
paragraph. Constraints: no CDN or external requests; responsive; tooltips via DOM API.

### Phase 7 - Verify and deliver
Checks: row counts match Phase 0; every chart container has an SVG child; zero console errors;
no horizontal overflow; no unresolved placeholder left in the output. Verify over a temporary
`python -m http.server` (kill it afterwards; `file://` previews render as static snapshots). Then
deliver the file and give a short chat summary whose last lines are the user's next actions.

## Re-run behavior

Each run regenerates the full report with current data - same section skeleton, fresh numbers,
fresh synthesis. Do not reuse stale conclusions: patterns listed as "known insights" in your
data-sources file are HYPOTHESES to re-test, not facts to restate - a null result that stays
null is itself a finding worth one line. When a previous report is available, add one short
"since the last report" note in the executive summary.

## Keeping this skill in sync

- When the user gives feedback on a report (format, depth, new sections), fold it into this
  SKILL.md or the references in the same session, so the next run starts corrected.
- When your workspace changes (new databases, renamed properties), update
  `references/data-sources-template.md` to match - it is the single map this pipeline trusts.
