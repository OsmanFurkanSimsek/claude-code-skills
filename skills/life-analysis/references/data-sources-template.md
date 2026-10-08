# Data sources - FILL THIS IN

The single map this pipeline trusts. Everything in `<angle brackets>` is a placeholder for your
own Notion workspace. Verify it against live schemas once, date that verification here, and
update this file whenever the workspace changes.

## Core trackers

### Daily tracker - one row per day
- Collection: `<collection://your-daily-tracker-id>`
- Date identity: `<date:Date:start>` (the property queries key on).
- Numeric scores (0-10 or your scale): <e.g. "Sleep Quality", "Energy Level", "Morning Mood",
  "Evening Mood", "Stress Level", "Overall Day Rating" - list YOURS exactly as named>.
- Duration fields (minutes): <e.g. "Exercise Duration", "Meditation Duration">.
- Checkboxes: <e.g. "Meditation", "Planned Intentionally"> - note the literal value your
  checkbox comparisons need (Notion SQL mode compares against `'__YES__'`).
- Multi-selects: <e.g. "Physical Activity" [option list]>.
- Text fields: <list them all - journals, reflections, gratitude, goals, problems, notes.
  The fill-rate analysis runs over this list, so completeness matters.>
- Quirks (write down every one you know - they are where analyses silently break):
  <duplicate rows per date? voice-dictated text with transcription noise? a topic narrated in
  one field although another field exists for it?>

### Weekly reviews - one row per week
- Collection: `<collection://your-weekly-reviews-id>`
- Identity: `<date:Date Range:start>` - if your week-title property is human-typed, assume it is
  UNRELIABLE (duplicates, gaps, shifts) and key on the date property instead.
- Rating: <"Week Rating" 0-10>. Body metrics if tracked: <weight, body-fat fraction (note the
  unit!), muscle mass>. Texts: <reflection fields, start/stop/continue, focus horizons>.

### Periodic reviews - monthly/quarterly/yearly
- Collection: `<collection://your-periodic-reviews-id>`
- Quirks to check: <does the period title run ahead of its content because you write it at the
  start of the next period? read the date-range property plus content, not the title.>
- Fields: <"Type" [Monthly, Quarterly, Yearly], "Period Rating", reflection texts>.

## Side databases (cross-checks + workspace analysis)

| DB | Collection | Use in the report |
|---|---|---|
| <Health log> | `<collection://...>` | Episode timeline (problem, start/end dates, notes); chronic-pattern detection |
| <Memories / experiences> | `<collection://...>` | Places and experiences; cross-check incidents against the health log |
| <Gratitude / other diaries> | `<collection://...>` | If a diary MIRRORS a daily-tracker field, read ONE of them, not both |
| <Work tasks> | `<collection://...>` | Backlog analysis: created per month, done-share, category share |
| <Mid/long-term tasks> | `<collection://...>` | Life-project timeline |
| <Goals / objectives> | `<collection://...>` | Formal goals vs lived life; staleness check |
| <Read-later / capture DBs> | `<collection://...>` | Channel-liveness check only |
| <Scribble / quick notes> | `<collection://...>` | Row COUNT only - content too costly |

New pages in period: a created-date-range Notion search scoped to your notes areas, plus one
unscoped sweep. Block-level additions to long-lived pages cannot be dated - say so honestly in
the data-quality section instead of guessing. **If any pages hold credentials, name them here as
NEVER-OPEN and keep them out of every query.**

## Quantitative recipes (Phase 3)

- Monthly averages per score + duration fields + habit percentages + n days.
- 7-day moving averages for the headline series (day rating, energy, sleep, stress...).
- Pearson correlation matrix over the scores + key durations (report n per pair; use short
  labels that fit a heatmap).
- Day-of-week means for rating, stress, exercise.
- Behavior splits: <planned vs unplanned days, habit-day vs non-habit-day> on rating/mood/stress.
- Activity distribution (total + per month), days-with-activity count.
- Field fill-rates over all text fields (drives form-simplification advice).
- Body series if tracked (dedupe weeks first).
- Week comparison: daily-average rating per week vs the retrospective week rating + correlation
  (a peak-end-effect test).
- Missing-day check + duplicate-date list (report both under data quality).

## Text-mining helpers (Python, keyword-based; approximate by design)

- NAME_MAP: if entries are voice-dictated, the same person's name appears in many variants.
  Maintain a `<Canonical=variant1=variant2>` map here and count DAYS mentioned (dedupe per day)
  across the social/gratitude/journal fields.
- Problem categories: `<your keyword buckets - work; home/moving; health; travel; other>`, per month.
- Gratitude categories (multi-label): `<your buckets>`.

## Known insight patterns from previous runs

HYPOTHESES to re-test each run, never facts to restate. Keep one line each, e.g.:
`<peak-end effect in week ratings; planned-day advantage; sleep->morning-mood chain r~0.7;
exercise-duration null result; seasonal confound to re-check when the next season's data lands>`.

## Query mechanics (Notion MCP, verified in practice)

**View mode is the default for all bulk reads. SQL is rationed.** See "Extraction budget" in
SKILL.md for the 10-call cap and the window ladder.

### View mode (quota-free, use for everything bulk)
`query_data_sources {mode:"view", view_url:"https://www.notion.so/<db-id>?v=<view-id>",
page_size:100, start_cursor:"..."}`
- Returns **every property** of every row, including all long text fields, no matter which
  properties the view displays.
- Paginates with `next_cursor`; `page_size` maxes at 100.
- Default views often come back newest first, so page only until you pass the window start date.
- Cannot aggregate. Counting, MIN and MAX still need SQL.

### Cached view URLs (skip the discovery fetches)
| Database | View URL |
|---|---|
| `<daily tracker>` | `<https://www.notion.so/<db-id>?v=<view-id>>` |
| `<periodic reviews>` | `<...>` |
| `<task backlog>` | `<...>` |

Discovering one costs two Notion fetches (fetch the `collection://` id, read its `url` field for
the database page id, fetch that id and read the views block) and zero quota. **Whenever a run
discovers a new view URL, add it to this table in the same session** so the next run does not pay
for it again.

### SQL mode (rationed, aggregates only)
- `SELECT ... FROM "collection://..." WHERE "date:Date:start" >= '...' ORDER BY ...`; checkbox
  filters compare against `'__YES__'`; results paginate at ~100 rows; oversized results
  auto-save to a file (parse with Python; with SELECT aliases, parse alias keys).
- **The quota counts calls, not rows.** A narrower date range costs exactly the same as a wide
  one, so never slice a query to save quota; slice only to stay under the 100-row page limit.
- The quota error does not recover inside a session; do not retry hoping it resets.
- Formula columns are not queryable in SQL mode.
- Shrink text payloads with `substr("Field",1,N)` when only previews are needed.
