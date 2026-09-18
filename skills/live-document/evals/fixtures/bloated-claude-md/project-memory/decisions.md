# Decisions locked - full wording

> Home of every locked decision's full wording and rationale for weather-cli. `PROJECT.md`
> `## Decisions locked` keeps one rule line per decision and points here.

## Cache before calling
- **Rule:** every command reads the SQLite cache first (30 min TTL). (Dana, 2026-03-02)
- **Why:** the free tier is 10k calls/day per IP.
