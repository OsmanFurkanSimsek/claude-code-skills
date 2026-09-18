# PROJECT.md - weather-cli

> Single source of truth for this project, read in full once per session. A fresh agent reading
> this file, and on demand the `project-memory/` files its Map names, should be able to continue
> correctly with nothing re-explained. Maintained every session under the home rule: one home per
> fact, pointers everywhere else.

<!-- MAINTENANCE CONTRACT - read before editing this file. Enforced by hooks (project-md-lint).
Three layers by read frequency: CLAUDE.md (every message, thinnest); this file (once per session,
in full, max 20 KB / 250 lines): Goal, Scope, Map, Current state, Decisions locked (rule + one-line why + who/when,
max 3 lines each), Plan, Open questions, Lessons (key rules, max 3 lines each); project-memory/
(on demand via the Map, one file per topic, every file has a Map row): decisions.md (full wording),
lessons.md (stories, max 8 lines each), changelog.md (every milestone, one entry per date, max 3
lines, no total cap), plus topic files. No change log, research notes, or execution plan here.
Home rule: a fact lives in ONE home (decision wording / lesson story / milestone in project-memory;
skill rule body in the skill's references; run analysis in the run file; owner preference in
memory); elsewhere one line + a pointer. A line leaves this file only when its home is named and
exists. Write order: project-memory home first, this file last. The Map names every folder and
file that matters and must stay current. Update = reconcile, not append. -->

## Goal and definition of done
A fast CLI forecast that works offline from cache. Done when `weather-cli forecast <city>` answers in
under 300 ms from cache and the test suite passes without network access.

## Scope and non-goals
- In scope: forecast, history, air quality and marine commands; SQLite cache.
- Out of scope: a GUI, paid API tiers, push notifications.

## Map - where to find what
| Location | What lives there | Read it when |
|---|---|---|
| `PROJECT.md` | goals, this map, current state + next action, decisions index, key-lesson rules, open questions | every session, in full |
| `project-memory/decisions.md` | the full wording and rationale of every locked decision | before changing or superseding a decision |
| `project-memory/lessons.md` | every lesson story, grouped by theme | when a rule feels wrong, before changing how we work |
| `project-memory/changelog.md` | every milestone since the start, newest first | when the history of a change matters |
| `src/` | the CLI source | coding |

## Current state and next action
v0.3 shipped (forecast + history + cache). Next action: add the `air` command.

## Decisions locked
- **Cache before calling** - every command reads the SQLite cache first (30 min TTL); why: the free tier is 10k calls/day (Dana, 2026-03-02).

## Plan / workstreams
- [x] forecast + history + cache
- [ ] air quality command

## Open questions
- Should marine data share the forecast cache table?

## Lessons
- **Record fixtures, never hit the API in tests** - a live test burned 2k calls in one CI run (2026-04-11). Story: `project-memory/lessons.md § Record fixtures, never hit the API in tests`.
