# Claude Code skills

Ten skills I built for [Claude Code](https://claude.com/claude-code) and use every day.
Most are workflow skills: they change *how* the agent works on a problem, not what domain it
works in. Two (`presentation-design`, `notion-router`) are domain skills instead, built around a
specific kind of deliverable or tool. Nothing here is tied to a particular language, framework,
or company.

Install what you like, ignore the rest. Each skill is a self-contained folder.

---

## The skills

| Skill | Trigger | What it does |
|---|---|---|
| **e2e** | `/e2e` | Runs a full end-to-end, production-quality build as a phased pipeline: discovery, research, plan, execute, review, human feedback, testing. Works for software *and* for non-code deliverables (analysis, report, BI dashboard, deck). Resumable - it stores its own state in the project's `CLAUDE.md`. |
| **elon** | `/elon` | Applies Musk's five-step algorithm as an interactive coach: question every requirement, delete, simplify, accelerate, automate. Use it before you build, to cut scope rather than gold-plate it. |
| **system2thinker** | `/system2thinker` | A zero-assumptions requirements interview for the fuzzy start of a project. Challenges every requirement, runs a pre-mortem, and locks a clean requirement set. It deliberately does *not* build anything - it hands off to `live-document`. |
| **live-document** | `/live-document` | Sets up project memory that survives across sessions: a thin auto-loading `CLAUDE.md` plus a living `PROJECT.md` that future sessions maintain by *reconciling* it, not appending to it. This is the fix for "I keep losing context between sessions". |
| **project-partner** | `/project-partner` | The combined front door: scoping (`elon`) plus cross-session memory (`live-document`) in one skill, for when you are starting something substantial and do not want to pick. |
| **session-handoff** | `/session-handoff` | Produces a fixed-structure end-of-session summary (decisions, shipped changes, key files, running background jobs, verification steps, deferrals, open questions) so a fresh agent can pick up from the summary alone. Chat-only, writes no files. |
| **answer-format** | `/answer-format` | Fixes the shape of every substantial reply: **Summary** (what happened, plain words), then **Why** (reasoning, numbers, trade-offs), then **What you should do** last. Putting the actions at the bottom means you never hunt for your next step, and you can scroll up for the reasoning only when you want it. Includes paste-ready text for Claude desktop's personal-preferences box, where an always-loaded rule beats skill triggering. |
| **big-project** | `/big-project` | A thin personal working-style layer: answer format, one-action-per-line steps, no unilateral decisions, versioned code with full QA, validate-in-a-playground first. It delegates the real machinery to the three skills above rather than re-implementing it. Fork this one and put *your* preferences in `references/preferences.md`. |

### How they fit together

```
system2thinker      lock the requirements
      │
      ▼
    elon            cut the scope
      │
      ▼
     e2e            build it, phase by phase
      │
      ▼
live-document       keep the state across sessions
      │
      ▼
session-handoff     hand off cleanly before /clear
```

`project-partner` bundles the top two layers. `big-project` sits over all of it as a working-style layer,
and `answer-format` governs the shape of every reply along the way - it is the one skill here that is not
tied to a phase of work.

---

## Domain skills

Not part of the pipeline above - each is a standalone skill for a specific kind of work.

| Skill | Trigger | What it does |
|---|---|---|
| **presentation-design** | (auto) | Design principles for every deck, talk, or pitch: one idea per slide, real hard-won lessons on logos/SVGs/video embedding, typography that scales to the room, live-demo pacing, and a feedback loop that folds every correction back into the skill. Ready to use as-is. |
| **notion-router** | (auto) | Routes incoming notes, tasks, and ideas into the right place in *your* Notion workspace, and retrieves context from it. This one is a **template**, not a ready skill - it ships with a placeholder routing table and workspace map; fork it and fill in `references/notion-map-template.md` with your own pages and databases before it does anything useful. See its own `README.md` for the adaptation steps. |

---

## Install

**All of them:**

```powershell
git clone https://github.com/OsmanFurkanSimsek/claude-code-skills.git
cd claude-code-skills
pwsh ./install.ps1
```

**Just a few:**

```powershell
pwsh ./install.ps1 e2e elon live-document
```

**By hand** (any OS) - copy the folders you want into your skills directory:

```
Windows   %USERPROFILE%\.claude\skills\
macOS     ~/.claude/skills/
Linux     ~/.claude/skills/
```

Restart Claude Code afterwards, then type `/e2e` to check it loaded.

`install.ps1` overwrites a skill folder of the same name, so move your own version aside first if
you have edited one.

### Claude desktop app

`project-partner.skill` and `answer-format.skill` are those two skills packaged as desktop-app
bundles. Upload them in the desktop app's skill settings rather than copying the folders.
`answer-format` is the one most worth having there - see its `references/desktop-setup.md` for
the paste-ready preferences text that makes the format apply to every reply, not just the ones
where the skill happens to trigger.

---

## Optional extras

**`settings.example.json`** - the parts of my `~/.claude/settings.json` that are worth copying: a
`permissions.deny` list that blocks disk-wiping commands, `curl | sh` pipes, accidental
`npm publish`, and reads of `.env` / `~/.ssh` / `~/.aws` / cloud credential directories.

> **Read this before copying.** My real settings also run
> `"defaultMode": "bypassPermissions"` with `"skipDangerousModePermissionPrompt": true`, which
> means the agent stops asking before it acts. That is a deliberate trade I make on my own
> machine, and it is **not** in this example on purpose. Do not turn it on unless you have
> thought about what an agent can reach from your account. The deny list is a seatbelt, not a
> substitute for that decision.

**`CLAUDE.md.example`** - the global instruction file I load in every session. Its one real idea:
answer in the order *Summary → Why → What you should do*, with the actions last, because the
next thing you need is at the bottom of the message where your eyes already are.

**`statusline.ps1`** - a PowerShell status line showing model, a context-usage bar, session cost,
lines added/removed, elapsed time, and the current project. Wire it up via the `statusLine` block
in `settings.example.json`.

---

## Notes

- **Windows-first.** I work on Windows, so the helper scripts are PowerShell and some paths use
  `%USERPROFILE%`. The skills themselves are plain Markdown and work anywhere; only `install.ps1`,
  `sync-skills.ps1`, and `statusline.ps1` are Windows-specific.
- **Some skills reference each other.** `system2thinker` hands off to `live-document`;
  `big-project` delegates to `live-document`, `session-handoff`, and `e2e`; `project-partner`
  subsumes `elon` and `live-document`. They degrade gracefully if a partner skill is missing, but
  they are better together.
- **`e2e`, `live-document`, `project-partner`, and `session-handoff` ship `evals/` suites.** If you
  modify one, run its suite before and after and require the score to hold. That discipline is the
  only reason these stayed reliable through a year of edits.

## Acknowledgements

Two phases of `e2e` are adapted from [gstack](https://github.com/garrytan/gstack) (MIT): its
Office Hours phase became `/e2e` Phase 1, and its CEO Review phase became Phase 2, both
substantially reduced in scope. The adaptations are credited inline in
`skills/e2e/references/office-hours-protocol.md` and `ceo-review-protocol.md`.

Everything else here is my own.

## Contributing

Issues and pull requests are welcome, especially bug reports of the form "skill X triggered when
it should not have" or "did not trigger when it should have" - trigger accuracy is the hardest
part of a skill to get right, and real misfires are the most useful thing you can send me.

## License

MIT - see [LICENSE](LICENSE). Use them, fork them, change them.
