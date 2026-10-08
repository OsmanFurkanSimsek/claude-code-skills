# Lessons - the full stories

> Home of every lesson story for weather-cli, grouped by theme. `PROJECT.md` `## Lessons` keeps
> only the rules and points here.

## Testing

### Record fixtures, never hit the API in tests
- A live-API test ran in CI on every push and burned 2,000 calls in one run. Tests now replay recorded fixtures. (2026-04-11)
