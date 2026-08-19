# Resume protocol

The end-to-end skill is designed to survive `/clear`. A future Claude session picks up mid-flow by reading two files: `CLAUDE.md` (thin constitution + state marker) and `PROJECT.md` (the living source of truth - goal, scope, decisions, lessons, plus the `## Research notes` and `## Execution plan` sections). This file describes how to do that reliably.

**Legacy layout:** projects created by an earlier version of this skill also have some of `PLAN.md`, `RESEARCH.md`, `design-*.md`, `ceo-plan-*.md`, `elon-*.md`, `PLAYTEST.md`. Any of those present means the run continues under that multi-file layout for its whole life - read PLAN.md as the execution tracker, RESEARCH.md as the research record, and so on. **Never migrate a legacy run to the consolidated layout mid-run.**

## The state marker

`CLAUDE.md` always contains exactly one line of the form:

```
<!-- e2e-state: phase=<phase-name> step=<N> of=<M> track=<build|deliverable> last_checkpoint=<ISO-8601 UTC> -->
```

Where:
- `phase-name` ∈ {`office-hours`, `ceo-review`, `elon`, `research`, `ready-to-execute`, `execute`, `holistic-test`, `human-playtest`, `critical-review`, `playwright`, `simplify`, `final`, `complete`}. `human-playtest` is a legacy label for the **Human review** phase (Phase 8). The **Critical review** phase (Phase 9, Claude-run, no Codex) is keyed `critical-review`; the old label `codex-review` is still accepted on resume as an alias for it, so projects created before the rename keep resuming correctly. The discovery phases `office-hours` / `ceo-review` / `elon` / `research` map to Phases 1 / 2 / 3 / 4.
- **The marker physically exists from Phase 0.** `CLAUDE.md` is created as the last action of Phase 0 (see SKILL.md), so the marker is written from the very first phase and is the authoritative state at all times. Artifact-based inference (`design-*.md` / `ceo-plan-*.md` / `elon-*.md` presence) is only a **fallback** for legacy projects or partial runs whose `CLAUDE.md` is missing or markerless.
- `track` ∈ {`build`, `deliverable`}. Set in Phase 0 and written into the marker when CLAUDE.md is created there, then carried unchanged thereafter. It selects the Build-vs-Deliverable behavior of Phases 6, 7, 9, and 11. A marker that lacks `track=` (a legacy project) is treated as `build`.
- `step=<N> of=<M>` is only meaningful during `phase=execute`. For other phases, you can omit it or set it to `step=0 of=0`.
- `last_checkpoint` is the timestamp of the last checkpoint Claude paused at.

This marker is the single source of truth. Trust it. Do not re-derive state by guessing from file contents.

## Detection routine (Phase 0)

When `/e2e` is invoked, before any other work:

1. Use Glob to check if `./CLAUDE.md` exists at the project root, and detect the layout: any of `PLAN.md`, `RESEARCH.md`, `design-*.md`, `ceo-plan-*.md`, `PLAYTEST.md` present → **legacy multi-file layout** (keep it for the life of the run); none present → **consolidated layout** (everything in PROJECT.md).
2. If `CLAUDE.md` exists:
   a. Read CLAUDE.md.
   b. Search for a line starting with `<!-- e2e-state:`.
   c. If found, parse out `phase`, `step`, `of`, `track`, `last_checkpoint`. Resume per the table below. A marker present with no `## Execution plan` section yet (or, legacy, no `PLAN.md`) is normal during discovery (Phases 1-4) - trust the marker; do not treat it as an error or a partial state.
   d. If not found, ask the user: "Found CLAUDE.md without an e2e-state marker. Was it created outside `/e2e`? Should I treat as fresh start or read it as context first?"
3. If legacy artifacts exist but `CLAUDE.md` does not → unusual (CLAUDE.md is the bootstrap and is written first). Ask the user how to proceed (likely a partial state from an interrupted run).
4. If no `CLAUDE.md` exists → check for legacy discovery artifacts. Glob for `design-*.md`, `ceo-plan-*.md`, `elon-*.md` at the project root:
   - `elon-*.md` present (and any of the earlier artifacts too) → resume Phase 4 (Research) under the legacy layout. Phases 1-3 are implicitly done.
   - `ceo-plan-*.md` present, no `elon-*.md` → resume Phase 3 (Elon) under the legacy layout. Phases 1-2 are done.
   - `design-*.md` present, no `ceo-plan-*.md` → resume Phase 2 (CEO Review) under the legacy layout. Phase 1 is done.
   - None of the above → genuinely fresh run (consolidated layout). Check whether to run discovery (Phase 1 + Phase 2): default ON for greenfield (no `package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod` / `*.csproj` in the project root); default OFF for existing projects; `--with-discovery` / `--skip-discovery` args override.

On any fresh run, or a virtual-state resume (`office-hours` / `ceo-review`) where no marker exists yet, also **classify the track** (Build vs Deliverable) per SKILL.md Phase 0. The track is recorded in the marker when CLAUDE.md is created in Phase 0. On a marker-based resume, read `track=` from the marker (absent → `build`).

## Resume targets by phase

Once the marker is parsed, jump directly to the right place. Do not redo earlier phases unless the user asks. "The plan" below means PROJECT.md's `## Execution plan` section (legacy: PLAN.md); "research" means `## Research notes` (legacy: RESEARCH.md).

| Marker phase | Resume action |
|---|---|
| `office-hours` | Phase 1. Read PROJECT.md for context; if its Goal/Decisions don't yet carry the Office Hours outcome (legacy: no `design-*.md`), (re-)enter Phase 1 from the top (tell the user previous answers, if any, are lost). |
| `ceo-review` | Phase 2. Read PROJECT.md (Goal, Scope, Decisions carry the Phase 1 outcome; legacy: also the latest `design-*.md`), then enter Phase 2. If a partial CEO outcome is already in Decisions (legacy: a partial `ceo-plan-*.md`), ask "Continue CEO Review from where it stopped?" |
| `elon` | Phase 3. Read PROJECT.md (legacy: also `ceo-plan-*.md` / `design-*.md`); invoke the `elon` skill to run Phase 3. |
| `research` | Phase 4. Read PROJECT.md; (re-)run Phase 4 research and write/continue the `## Research notes` section (legacy: `RESEARCH.md`). |
| `ready-to-execute` | Read PROJECT.md (goal/decisions + the Execution plan), summarize the plan in 5 lines, ask user "Ready to start step 1?" |
| `execute` | Read PROJECT.md, find the Execution plan step with status `in_progress` (or step `<N>` from marker if no `in_progress`), summarize what's been done, ask user "Resume step `<N>`?" |
| `holistic-test` | Skip to Phase 7 (Holistic quality pass). Ask user "Resume the holistic quality pass?" |
| `human-playtest` | Skip to Phase 8 (Human review). If a Playtest checklist exists (in the Execution plan's Phase 8 block; legacy: `PLAYTEST.md`), summarize fill state ("X of Y rows feedback'd, Z blockers/annoyings open"). Ask user "Resume human review?" If the user has finished and feedback is in, switch to fix-application mode; otherwise hand the wheel back. (Marker key stays `human-playtest`.) |
| `critical-review` (or legacy `codex-review`) | Skip to Phase 9 (Critical review). Both labels resolve here; new runs write `critical-review`. If a review was already run and some findings are still open, ask whether to re-run or apply the remaining ones. |
| `playwright` | Skip to Phase 10. |
| `simplify` | Skip to Phase 11. |
| `final` | Skip to Phase 12. |
| `complete` | Tell the user "This project's e2e run is already complete (per CLAUDE.md). Start a new feature on top, or audit the existing build?" |

Note: projects whose PLAN.md was created under the older 10-phase numbering keep their numbering for life. The marker phase names above are name-keyed (not number-keyed), so old markers resume correctly. Do not migrate existing projects - neither their row counts nor their file layout.

## Updating the marker

Update the marker every time you cross a phase boundary or complete a step in Phase 6 (Execute). Use `Edit` on CLAUDE.md to change just that one line - do not rewrite the whole file.

Examples of valid markers:

```
<!-- e2e-state: phase=execute step=3 of=7 track=build last_checkpoint=2026-05-10T14:22:11Z -->
<!-- e2e-state: phase=critical-review step=0 of=0 track=deliverable last_checkpoint=2026-05-10T15:01:44Z -->
<!-- e2e-state: phase=complete step=0 of=0 track=build last_checkpoint=2026-05-10T16:33:02Z -->
```

The timestamp lets the user tell at a glance "we paused this 3 days ago" vs "this is current work".

## Sanity checks before resuming

Before charging back into work, do a quick reality check:

1. **Did files change while you were away?** Run `git status` (if it's a git repo). If there are uncommitted changes that weren't there at the last checkpoint, ask the user "I see uncommitted changes since the last checkpoint - were these manual edits I should know about before resuming?"
2. **Does the Execution plan status match the marker?** If the marker says `step=4` but the plan shows step 3 still `in_progress`, surface the mismatch and ask.
3. **Are tests still green?** If resuming mid-execute, run the test suite once before continuing - silent regressions are far more expensive to debug than a 30-second test run.

If any of these surface inconsistencies, pause and ask the user. Do not "fix" the marker silently - the discrepancy might be the very thing the user wanted to investigate.

## When the marker is missing or corrupted

If you can't parse the marker (typo, truncation, file edited by hand), don't guess. Show the user what's in CLAUDE.md and ask: "Marker looks malformed. Reset to phase=<X> step=<N>, or treat as fresh run?" Let them decide.
