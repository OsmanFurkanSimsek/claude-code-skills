# CLAUDE.md - heic2jpg

## Coding conventions
- Python 3.11+, type-hinted, formatted with `ruff format`.
- Prefer the standard library; only add a dependency when it clearly pays for itself.
- Tests live in `tests/`, run with `pytest -q`. Every bugfix gets a regression test.
- Commit messages: imperative mood, scope prefix, e.g. `cli: add --recursive flag`.

## Project notes
- Entry point is `heic2jpg/__main__.py`.
- We target macOS and Linux; Windows is best-effort only.
