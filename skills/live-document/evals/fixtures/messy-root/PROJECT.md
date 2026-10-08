# PROJECT.md - weather-dashboard

> Single source of truth for this project. A fresh agent reading only this file should be able to
> continue correctly, with nothing re-explained. Maintained every session: live sections edited in
> place; Change log holds milestones only (1-3 lines each, tail compacted as entries age); Lessons
> appended deduped; obsolete detail compacted.

<!-- MAINTENANCE CONTRACT - read before editing this file.
This file is re-read IN FULL at the start of every session; every line is paid for on every read.
Update = reconcile, not append.
1. New fact -> find its ONE home section; rewrite that section in place, deleting what it supersedes.
2. Answered Open question -> delete it; fold the answer into Decisions locked or Current state.
3. Change log = milestones only, newest first, 1-3 lines each (what shipped + commit + outcome).
   Verification narratives and review blow-by-blow never belong here. When adding an entry,
   compact any older entry still over 3 lines; its durable content lives in Decisions/Lessons.
4. Before saving, sweep the file: delete or merge every stale, resolved, or duplicated line.
   Deleting stale lines is required maintenance, not data loss; compact real decisions and lessons,
   never drop them.
5. Tripwire: Change log over ~30 lines, any entry over 3 lines, or a diff that only adds lines
   means compaction is overdue - fix it in THIS edit, not later.
Red flag: an edit that only appends. A healthy update rewrites more lines than it adds. -->

## Goal and definition of done

A single-page Flask dashboard showing today's and this week's local forecast as charts, refreshed
hourly, for Osman's home server. Done when the page loads in under a second from cache, survives
API outages gracefully, and has run a full week without manual restarts.

## Scope and non-goals

- In scope: one city (Ankara), current conditions + 7-day forecast, hourly cache refresh, one
  Flask route rendering one page with two charts.
- Out of scope / non-goals: multi-city support, user accounts, mobile app, historical archives.

## Current state and next action
<!-- Rewrite in place; must describe only NOW. -->

`dashboard.py` serves the page with current conditions and the 7-day chart; the file cache layer
works (verified during the July 12 debugging session). The hourly forecast chart renders but the
x-axis labels overlap at narrow widths.
**Next action:** fix the hourly chart's x-axis label overlap, then re-check the page at phone width.

## Decisions locked
<!-- A changed decision REPLACES the old one; note the change once in Change log. -->

- Open-Meteo as the data source (no API key, generous free tier) - chosen over OpenWeatherMap,
  whose free tier needed a key and had tighter limits.
- File-based JSON cache with a 1-hour TTL in `cache/` - a database is overkill for one city.
- Chart.js rendered client-side from a JSON endpoint - server-side matplotlib PNGs were slower
  and uglier.

## Plan / workstreams
<!-- Status markers updated in place: [ ] todo, [~] in progress, [x] done, [!] blocked. -->

- [x] Fetch + cache layer for Open-Meteo.
- [x] Current conditions + 7-day chart page.
- [~] Hourly forecast chart (renders; x-axis labels overlap at narrow widths).
- [ ] Week-long stability soak on the home server.

## Open questions
<!-- Live unknowns only; delete once answered. -->

- Should the soak test run before or after the hourly chart fix? (Osman to decide.)

## Change log
<!-- Milestones only, newest first. A line every session = a diary = a bug. -->

- 2026-07-13: 7-day chart page shipped with cache layer; page loads ~300ms warm.
- 2026-07-05: Project started; Open-Meteo picked; fetch + cache working.

## Lessons
<!-- Deduped; compact, never lose. -->

- Open-Meteo returns hourly arrays in UTC; converting at render time (not fetch time) avoided a
  double-shift bug that cost an evening (July 12).
