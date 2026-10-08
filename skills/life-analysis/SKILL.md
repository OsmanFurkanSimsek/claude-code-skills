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
6. ONE PASS ONLY. The whole analysis must finish in a single run. Never stop halfway and ask the
   user to re-run later, and never deliver a report with a section that says "this could not be
   pulled". Budget the extraction up front (see "Extraction budget" below) and shrink the window
   instead of shrinking the report.
7. DEFAULT WINDOW: the last 12 months, or the full history if it is shorter. Do not go past 12
   months unless the user names a longer period.

## Environment detection

- **Claude Code** (Bash + Write + Agent tool available): full pipeline as written; parallel
  subagents for the qualitative reading; verify over a local HTTP server.
- **Claude Desktop / a sandboxed environment** (no Agent tool): same pipeline, but read the
  qualitative digests yourself sequentially (they are pre-chunked small files) and deliver
  through the environment's file-output mechanism.
- Both need the Notion connector. If Notion tools are missing, say so and stop - never simulate
  data.

## Extraction budget (read this before any query)

Learned the hard way: a full run used up the workspace SQL quota at its 13th SQL query, and the
side databases could not be read at all.

- **The quota counts CALLS, not rows.** One SQL call returning 100 rows costs the same as one
  returning 1. Shortening the analysis window does NOT save quota; making fewer calls does.
- **View mode (`mode:"view"`) is quota-free and returns EVERY property**, including all long text
  fields, whatever the view's displayed properties are. It is the workhorse; SQL is the exception.
- Therefore: **bulk extraction is always view mode. SQL is reserved for aggregates that view mode
  cannot do** (COUNT, MIN, MAX). Hard cap: **10 SQL calls per run**, spent as below.

SQL budget (10 calls, in this order):
1-3. Row count + MIN/MAX date for each of the three core trackers.
4. One `COUNT(field)` call covering all the daily tracker's text fields (field fill rates).
5. One small side database that needs a full pull (only if it fits in one call).
6-10. Reserve. Do not spend these on anything a view can return.

Cost model for view mode: quota-free but token-heavy. A daily tracker with about 20 text fields
runs about 750 characters per row, so six months is roughly 140k characters across 3 calls of
about 60 rows; 12 months is about twice that. Token pressure, not quota, limits the window.

### Window ladder
Always degrade by TIME first, never by dropping report sections:

`12 months -> 6 months -> 3 months -> 1 month`

Step down one rung when either the SQL quota errors out with the reserve calls already spent, or
the view-mode extraction is clearly going to exhaust the context before Phase 6. State the window
used in the header and footer of the report. Only if the ladder has bottomed out at 1 month may
you reduce coverage further, and then in this order:
1. Drop the side databases (section 10 of the blueprint shrinks to the task backlog only).
2. Drop the low-value daily text fields (pick them in the data-sources file) by pulling a
   narrower SQL projection instead of the view.
3. Never drop sections 1-9 or 13.

## Pipeline (8 phases)

Read `references/data-sources-template.md` before Phase 1 and
`references/report-blueprint.md` before Phase 6.

### Phase 0 - Discover
Three SQL calls: row count + MIN/MAX date for the three core trackers. Set the window from the
ladder (default 12 months back from today, or the full history if shorter). State row counts in
the report footer and verify final numbers against them. If a previous report exists in the
conversation, note its cutoff date so the new report can call out what changed since.

### Phase 1 - Extract
Default path is view mode for everything bulk. Getting a view URL costs two Notion fetches the
first time (fetch the `collection://` id to get the database page URL, then fetch that page and
read its views block) but zero quota; cache known URLs in the data-sources file and skip the
discovery fetches next time. Page with `page_size` up to 100 and follow `next_cursor`; default
views often come back newest first, so stop paging once you pass the window start date. Then
spend SQL calls 4 and 5 on the fill-rate COUNT and the small side database. Oversized results
auto-save to files - parse those with Python, never re-query smaller. The mechanics are in the
data-sources file.

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
Pull your task backlogs and goal databases for the period **through view mode**, never SQL (each
needs its view URL cached in the data-sources file first), plus a created-date search for new
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
Checks: the analysis window is stated in the header and the footer; row counts match Phase 0;
every chart container has an SVG child; zero console errors;
no horizontal overflow; no unresolved placeholder left in the output. Verify over a temporary
`python -m http.server` (kill it afterwards; `file://` previews render as static snapshots). Then
deliver the file and give a short chat summary whose last lines are the user's next actions.

## Re-run behavior

Each run regenerates the full report with current data - same section skeleton, fresh numbers,
fresh synthesis, for the window chosen by the ladder. Do not reuse stale conclusions: patterns listed as "known insights" in your
data-sources file are HYPOTHESES to re-test, not facts to restate - a null result that stays
null is itself a finding worth one line. When a previous report is available, add one short
"since the last report" note in the executive summary.

## Keeping this skill in sync

- When the user gives feedback on a report (format, depth, new sections), fold it into this
  SKILL.md or the references in the same session, so the next run starts corrected.
- When your workspace changes (new databases, renamed properties), update
  `references/data-sources-template.md` to match - it is the single map this pipeline trusts.
- Every run that discovers a new view URL adds it to the cached table in the data-sources file
  before delivering the report.
- Every run replaces the "Known insight patterns" block in the data-sources file with what the
  current data actually showed, so the next run inherits live hypotheses rather than stale ones.
