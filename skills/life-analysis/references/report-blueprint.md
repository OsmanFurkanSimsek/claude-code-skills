# Report blueprint (life-analysis-<year>.html)

One self-contained HTML file, written in the user's language. The skeleton below is the seed
skill's proven structure - rename, drop, or add sections to match what you actually track, but
keep the ordering logic: numbers first, stories second, advice last (the reader acts on the
bottom of the report).

## Section skeleton (numbered, with a pill nav at top)

1. **Executive summary** - 2-3 short paragraphs: how life is going (with numbers), the heaviest
   burden, the watch-items, plus a "since the last report" note when a previous run exists.
2. **Dashboard** - stat tiles: tracked days (+missed), average day rating (+trend), sleep,
   stress (+trend), daily movement minutes, body metrics (+change), habit percentages, goal hit
   rate - whatever your headline numbers are. Tile deltas colored good/bad/neutral.
3. **The pulse** - day-rating 7-day moving average as a time series with raw dots, shaded bands
   for notable episodes (sickness, travel), and 4-6 event annotations; below it, a dual small
   series for stress + one other headline score on the same axis.
4. **Month by month** - monthly small-multiple bar rows (rating, energy, sleep, stress, social,
   exercise minutes) + one narrative card per month (single short paragraph, left-accent border).
5. **Health & body** (if tracked) - weekly minis (weight, body fat, muscle); an episode timeline
   (colored gantt rows by category); a chronic-pattern card; cross-validation notes where two
   sources tell the same story (or don't).
6. **Habits** - activity horizontal bars; day-of-week rating bars; habit-percentage monthly
   bars; a habit-reading card (bullets).
7. **Correlations** - correlation heatmap (diverging palette, gray midpoint, values in cells);
   one bubble scatter for the strongest pair (bubble size = day count); weekly lived-average vs
   retrospective-rating two-series line; a "standout relationships" bullet card. Label
   correlation strength honestly and show n - a null result that keeps being null is a finding.
8. **Problems & goals** - problem-category stacked monthly bars; synthesis cards: how problems
   actually get solved (sprint vs drift), goal-hit matching, avoidance patterns.
9. **Curiosity, learning & social circle** (if journaled) - top-people horizontal bars (from the
   NAME_MAP); gratitude-category bars; synthesis cards.
10. **The whole workspace** - tasks-per-month bars; backlog bullets; the channel-liveness map
    summary; side-database cross-readings.
11. **Themes from the writing** - the 4-6 big stories of the period as prose cards + one "voice
    of the period" quote card (8-10 respectful, dated quotes).
12. **Conclusions** - two cards side by side (improving / needs watching); field fill-rate bars;
    a data-quality bullet card (dedupes, gaps, unreliable titles).
13. **Mentor advice: So What / Then What** (MANDATORY - the payoff section; invest quality
    here). Wise-mentor voice, direct, warm, second person. 6-8 theme cards (typical themes:
    purpose and goals, the biggest behavioral lever, the heaviest burden, health root-causes,
    work strategy, relationships, social life), EACH structured as three labeled paragraphs:
    **"What I see:"** (this run's evidence, with numbers and dates), **"What it means:"** (the
    honest interpretation), **"What you should do:"** (2-4 concrete, dated-where-possible
    actions). Then one **"Beliefs your own data refutes"** card: things the user believes that
    their own data contradicts, each with the evidence. Close with a single-paragraph personal
    mentor note (accent-bordered card). Rules: every piece of advice must trace to this run's
    findings - no generic self-help; quote the user's own words and principles back at them
    where possible; stay respectful on family/health material; no medical/legal prescriptions
    beyond process hygiene and "ask a professional" nudges.
    Footer after this section: full source list + row counts + "read-only analysis; nothing in
    Notion was modified".

## Design system

- Palette (validated for contrast in light and dark): series1 blue #2a78d6 (dark #3987e5),
  series2 orange #eb6834 (#d95926), series3 aqua #1baf7a (#199e70), series4 yellow #eda100
  (#c98500), series5 magenta #e87ba4 (#d55181), neutral gray #898781. Diverging heatmap: blue
  #2a78d6 <-> red #e34948, gray midpoint #f0efec (dark: #3987e5 / #e66767 / #383835).
- Light surfaces #fcfcfb page #f9f9f7; dark #1a1a19 / #0d0d0d. Ink: #0b0b0b / #52514e / #898781
  (dark #ffffff / #c3c2b7). Grid #e1e0d9 (dark #2c2c2a).
- CSS custom properties on `:root` (light default), dark via
  `@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){...} }` plus
  `:root[data-theme="dark"]{...}`. Explicit body background. System sans stack.
- Charts: hand-drawn inline SVG via small vanilla-JS helpers (a time-series chart with bands,
  annotations and crosshair hover; bar chart with rounded tops + value labels; horizontal bars;
  stacked bars with 2px gaps; heatmap; bubble scatter; gantt timeline; weekly minis).
  viewBox + width:100% for responsiveness; legends for >=2 series; direct value labels on bars;
  month tick labels in the user's language.
- Shared fixed-position tooltip built with createElement/textContent only - never innerHTML
  (safer, and some setups run hooks that reject innerHTML outright).
- Max width ~1080px; cards with 14px radius + hairline border; multi-column grids collapse to
  one column under 760px.

## Data injection + verification

- Write the page as `report_template.html` with a single `__CHART_DATA__` placeholder inside
  `<script id="cdata" type="application/json">`; inject `chart_data.json` with a Python
  `str.replace`; assert: no `</script` inside the JSON, exactly one placeholder, no qualitative
  placeholder markers left. Output name: `life-analysis-<year>.html`.
- Verify: serve the scratchpad over `python -m http.server <port>` in the background, open it,
  check console errors, `document.querySelectorAll('svg').length`, `scrollWidth <= innerWidth`,
  then STOP the server. A `file://` preview renders as a static snapshot - don't judge
  interactivity from it. Screenshots of very tall pages can fail in an embedded pane - fall back
  to structural JS checks.
- Deliver the file, then give a chat summary whose final lines are the user's next actions
  (including "open it in a real browser").
