# CLAUDE.md - weather-cli

## Purpose
weather-cli fetches forecasts from the Open-Meteo API, caches them in SQLite and prints them in the
terminal. It exists because the owner wants a fast, offline-friendly forecast at the command line.
Keep it a small, dependency-light CLI - not a framework.

## API reference
| Endpoint | What it returns | Key params |
|---|---|---|
| `GET /v1/forecast` | hourly + daily forecast, up to 16 days | `latitude, longitude, hourly, daily, forecast_days` |
| `GET /v1/archive` | historical weather back to 1940 | `start_date, end_date, hourly` |
| `GET /v1/air-quality` | air quality forecast | `hourly=pm10,pm2_5,european_aqi` |
| `GET /v1/marine` | wave height + swell | `hourly=wave_height,swell_wave_period` |
| `GET /v1/geocoding/search` | city name -> lat/lon | `name, count, language` |
| `GET /v1/elevation` | terrain elevation | `latitude, longitude` |
| `GET /v1/flood` | river discharge forecast | `daily=river_discharge` |

Limits verified against the live API: `forecast_days` max 16, `past_days` max 92, `models` max 4 per
call, hourly variables max 20 per call. Overshoot a value and the 400 names the real max. Free tier =
10,000 calls/day per IP; `X-RateLimit-Remaining` is on every response. Timezone must be an IANA name or
`auto`. Units: `temperature_unit=celsius|fahrenheit`, `wind_speed_unit=kmh|ms|mph|kn`.

## Dated API notes
- **2026-03-02 API check:** probed `/v1/forecast` with `hourly=temperature_2m,precipitation` and `forecast_days=16`; the forecast_days parameter now returns HTTP 400 above 16. Cache TTL kept at 30 min. Rate header `X-RateLimit-Remaining` read on every call; budget after the probe 9120 calls. Earlier note said `past_days` capped at 92; still true.
- **2026-04-11 API check:** probed `/v1/forecast` with `hourly=temperature_2m,precipitation` and `forecast_days=16`; the past_days parameter now returns HTTP 400 above 92. Cache TTL kept at 30 min. Rate header `X-RateLimit-Remaining` read on every call; budget after the probe 8840 calls. Earlier note said `past_days` capped at 92; still true.
- **2026-05-20 API check:** probed `/v1/forecast` with `hourly=temperature_2m,precipitation` and `forecast_days=16`; the models parameter now returns HTTP 400 above 4. Cache TTL kept at 30 min. Rate header `X-RateLimit-Remaining` read on every call; budget after the probe 9310 calls. Earlier note said `past_days` capped at 92; still true.
- **2026-06-30 API check:** probed `/v1/forecast` with `hourly=temperature_2m,precipitation` and `forecast_days=16`; the timezone parameter now returns HTTP 400 above 1. Cache TTL kept at 30 min. Rate header `X-RateLimit-Remaining` read on every call; budget after the probe 9901 calls. Earlier note said `past_days` capped at 92; still true.
- **2026-07-28 API check:** probed `/v1/forecast` with `hourly=temperature_2m,precipitation` and `forecast_days=16`; the hourly parameter now returns HTTP 400 above 20. Cache TTL kept at 30 min. Rate header `X-RateLimit-Remaining` read on every call; budget after the probe 9555 calls. Earlier note said `past_days` capped at 92; still true.
- **2026-08-19 API check:** probed `/v1/forecast` with `hourly=temperature_2m,precipitation` and `forecast_days=16`; the daily parameter now returns HTTP 400 above 14. Cache TTL kept at 30 min. Rate header `X-RateLimit-Remaining` read on every call; budget after the probe 9022 calls. Earlier note said `past_days` capped at 92; still true.
- **2026-09-10 API check:** probed `/v1/forecast` with `hourly=temperature_2m,precipitation` and `forecast_days=16`; the minutely_15 parameter now returns HTTP 400 above 96. Cache TTL kept at 30 min. Rate header `X-RateLimit-Remaining` read on every call; budget after the probe 8700 calls. Earlier note said `past_days` capped at 92; still true.

## Incident log
- **2026-02-14 incident:** forecast command hung for 60 s on a slow network. Root cause: no connect timeout on the HTTP client. Fix shipped the same day; see the commit for details.
- **2026-03-21 incident:** history returned an empty table for leap-day ranges. Root cause: date arithmetic used 365-day years. Fix shipped the same day; see the commit for details.
- **2026-05-02 incident:** cache served stale data across timezones. Root cause: cache key ignored the timezone parameter. Fix shipped the same day; see the commit for details.
- **2026-06-12 incident:** air command printed NaN for pm2_5. Root cause: null values were not filtered before formatting. Fix shipped the same day; see the commit for details.
- **2026-07-09 incident:** marine command crashed inland. Root cause: the API returns 400 for non-coastal coordinates. Fix shipped the same day; see the commit for details.
- **2026-08-03 incident:** CI burned 2,000 calls. Root cause: a live-API test slipped past the fixture guard. Fix shipped the same day; see the commit for details.

## How to run
```
pip install -e .
weather-cli forecast "Copenhagen" --days 7
weather-cli history "Copenhagen" --from 2026-01-01 --to 2026-01-31
pytest -q
```
Cache lives in `~/.cache/weather-cli/cache.sqlite`; delete it to force a refetch. `--no-cache` bypasses it.

## Files
- `src/weather_cli/api.py` - HTTP client, retries, rate-limit header parsing.
- `src/weather_cli/cache.py` - SQLite cache with a 30 minute TTL.
- `src/weather_cli/cli.py` - Typer commands (forecast, history, air, marine).
- `tests/` - pytest suite; every bugfix gets a regression test.

## Conventions
- Python 3.11+, type hints everywhere, `ruff format`.
- Never call the API in tests - use the recorded fixtures in `tests/fixtures/`.
- Commit messages: imperative mood.

<!-- live-document:start -->
## Start-of-session protocol (auto-loads)

This block loads automatically every message. Its only job is to bootstrap you.
The real source of truth is `PROJECT.md` in this same folder (read once per session), with every
detail in `project-memory/` (read on demand via its Map).

Owner: Dana. Project: weather-cli, a CLI that fetches forecasts from the Open-Meteo API and caches them. Dominant rule: never exceed the free API tier (10k calls/day).

### Do this every session, without being told
1. Read `PROJECT.md` IN FULL at session start, before acting - the SessionStart hook only tells
   you its size and lists the `project-memory/` files; the edit gate denies project writes until
   you have read it. Open a `project-memory/` file when its Map row says the task touches it, and
   ALWAYS before editing it. The user never has to ask.
2. After meaningful work, update the living setup by RECONCILING, not appending - project-memory
   home FIRST, `PROJECT.md` LAST: Current state always; a new durable choice REPLACES the one it
   supersedes in `project-memory/decisions.md` (full wording) and in Decisions locked (rule +
   who/when + a one-line why, max 3 lines); an answered Open question is deleted and folded into a decision; a
   milestone gets one 1-3 line entry in `project-memory/changelog.md` (one per date, never a diary).
3. Lock the feedback - home rule: a lesson's story goes to `project-memory/lessons.md` (max 8
   lines, under its theme), its rule to `PROJECT.md` Lessons (max 3 lines) only if it changes how
   we work here, and its memory file is a pointer; an owner preference goes to memory in full.
   Never two stories of one lesson. Keep the Map current: one row per project-memory file with a
   summary and a "read it when", and a row for every folder or file added, moved, or archived.
4. Before saving, sweep: delete or merge everything now redundant, resolved, stale, or duplicated
   - a line may leave only when its home is named and exists. `PROJECT.md` stays under 20 KB / 250
   lines with no change log, research notes or execution plan inside it. Tripwires are enforced by
   hooks: the lint blocks a malformed write, the Stop gate will not end a turn that edited project
   files until `PROJECT.md` is reconciled and lints clean, and one compaction is held while a
   reconcile is pending. Fix in THIS edit, not later. Never a tracking file outside `project-memory/`.

### Hard rules
- Dominant constraint: stay inside the free API tier; cache before calling.
- Change/approach hierarchy: smallest viable change first.
- Ask before assuming - a clarifying question beats a wrong assumption.
- When the user must act: give Summary, then Reasoning, then numbered Steps in super simple words.
  Big work goes in chunks of 5-10 steps, ONE chunk per turn; wait for confirmation, update
  PROJECT.md first (chunk statuses in Plan / workstreams, active chunk in Current state), then say
  the context can be cleared safely. Answers with nothing to do: TLDR first, then detail, no steps.
- Real handoffs (3+ steps or any chunk) also get a Next Actions file in `next-actions/`:
  an interactive self-contained <YYYY-MM-DD_HH-MM>-next-actions.html (TLDR paragraph, then
  reasoning with alternatives, then simple steps). Keep every dated file - the date-time prefix
  finds the latest - and announce the path in chat.
- Keep the project root tidy: file new screenshots / code examples / reports / next-action files
  into their subfolders; when 3+ loose files of one kind sit at root, propose a move list and tidy
  after ONE confirmation (never move source or config files silently).
- Never use the long-dash character.
<!-- live-document:end -->
