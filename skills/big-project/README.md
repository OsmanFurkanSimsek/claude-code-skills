# big-project

A personal **working-style layer** skill for Claude Code. Invoke `/big-project` to make any project run the way the owner likes his big, multi-session projects to run.

## What problem it solves

Across big projects the owner has one consistent way of working (a fixed answer format, a signature context-handoff block, no unilateral owner decisions, versioned code, predict-run-duration, and so on). That style used to live scattered across a global `CLAUDE.md`, each project's `CLAUDE.md`, and a pile of memory files. `big-project` captures it once, as a portable profile, and applies it to any project on demand.

## Design principle: compose, do not reinvent

`big-project` is intentionally thin. It does **not** re-implement the living document, the `/clear`-readiness, or the next-agent handoff - those are already handled by sibling skills, and `big-project` delegates to them:

| Concern | Owned by | `big-project`'s role |
|---|---|---|
| Living `PROJECT.md` + thin `CLAUDE.md` | `live-document` | Delegates creation/curation; only injects hard-rules bullets |
| Ready to `/clear` at any point | `live-document`, `e2e` | Relies on them; adds the two-step handoff block on top |
| End-of-session handoff summary | `session-handoff` | Calls it for the heavy explicit summary |
| Full build/deliverable rigor | `e2e` | Coexists; profile still applies |
| **How the owner personally likes to work** | **`big-project`** | **The gap it fills** |

## Layout

```
big-project/
  SKILL.md                          # orchestrator: setup flow, composition contract, enforcement
  README.md                         # this file
  references/
    preferences.md                  # the portable working-style profile (the core artifact)
    claude-md-injection.md          # exact hard-rules bullets + handoff block to add to a project CLAUDE.md
    walkthrough-and-handoff.md      # numbered one-action walkthrough format + the two-step handoff block
```

`SKILL.md` is the only file auto-read on trigger; everything in `references/` is loaded on demand (progressive disclosure).

## How it works

1. `/big-project` is invoked on a project.
2. It detects whether a `live-document` or `e2e` doc setup already exists.
   - Missing -> it invokes `live-document` to scaffold `PROJECT.md` + `CLAUDE.md` (or points the owner at `/e2e` for full rigor).
   - Present -> it layers on top without touching what those flows own.
3. It injects the owner's **delta** hard-rules (the ones `live-document` does not already carry) into the project `CLAUDE.md`, inserting only what is absent so re-running self-heals.
4. Every session afterward, the agent follows `references/preferences.md`.

## Portability note

The profile in `references/preferences.md` is **domain-free**. Tool-, data-, and model-specific rules stay in each project's own docs. To adapt this skill for a different person or team, fork it and edit `references/preferences.md` and `references/claude-md-injection.md`; the `SKILL.md` orchestration stays the same.

## Dependencies

Works best alongside these Claude Code skills: `live-document`, `session-handoff`, and `e2e`. It functions without them (it will still inject the hard-rules and enforce the profile), but delegation of the living document and handoff is only available when they are installed.
