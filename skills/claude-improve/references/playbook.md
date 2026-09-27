# Playbook - signals, how to confirm them, usual fixes

Each row starts from something `scan.md` shows. "Confirm" is what to read in the raw transcripts
before believing it; "Usual fix" lists the smallest homes first. Thresholds are starting points, not
laws: a signal matters when it costs the owner time, money, trust or context.

## Cost and context

| Signal (scan key) | Confirm | Usual fix |
|---|---|---|
| High share of tokens on turns above 200K / 300K (`ctx.share_above_300k.pct`); a few sessions carry most of the spend | Open the top-spend sessions: did they drag on after the main task, or did one huge tool result inflate them? | A handoff habit (write the next step down, clear, continue fresh); a hook that notices context size and prompts the handoff; move big reads to helper agents |
| Tool results over 25K chars (`big_outputs_25k`), one tool dominating output volume | Which calls: whole-page fetches, long logs, full-file reads of big files? | Read with offset/limit; helper agent saves the full result to a file and returns a summary + path; ask the tool for fewer fields |
| Same file read 3+ times in a session (`repeated_reads`) | Was it re-read after edits (fine) or re-read because the content fell out of context? | Keep a short summary in the plan file; read the section, not the file |
| Large always-loaded files (global CLAUDE.md, rules, project CLAUDE.md) | Which parts are used every session vs. rarely? | Move rarely used detail to an on-demand file and leave a one-line pointer |
| Many ToolSearch calls per session | Same tools loaded over and over? | Mention the usual tools in the project instructions so they are loaded once, early |
| Frequent compactions | Did work get lost or repeated after them? | Same as the handoff fix above; save state before the limit |

## Reliability

| Signal (scan key) | Confirm | Usual fix |
|---|---|---|
| Bash `heredoc_eof` errors | Look at the failing commands: quotes, `$`, backticks, apostrophes in paths | Rule: scripts over ~10 lines go to a file and run by path; never inline them |
| `unicode` errors | Printing non-ASCII on a Windows console? | UTF-8 set once in the shell profile (not in every command) |
| `cmd_not_found` | Tool installed but not on PATH? | Add it to the shell profile, or document its full path in the global instructions |
| Env vars re-exported in commands (`bash.export.*`) | Same variable set in many sessions | Put it in the shell profile once; remove the rule that makes the agent re-type it |
| `no_such_file` / mangled paths | Backslash paths in bash, wrong working directory | Rule: forward slashes inside double quotes in bash; absolute paths |
| `auth` errors | Expired logins in the middle of work | A login helper script + one line saying when to run it |
| Edit `not_read_first` / `no_match` / `modified_since` | Stale reads, guessed strings | Usually benign at low counts; a spike means edits from a stale view - re-read before editing |
| MCP server with many errors | Which calls: wrong arguments, timeouts, auth? | Document the working call shape in the project instructions; fix the server config |
| API errors clustered on some days | Outage or local proxy/network? | Usually not actionable; note it, don't recommend |

## Guardrails and hooks

| Signal (scan key) | Confirm | Usual fix |
|---|---|---|
| A hook blocking the same thing many times (`hook.block.*`) | Real catches or false positives? Replay a few blocked commands | False positive: narrow the pattern and add a test with the replayed commands. Real and repeated: the agent needs the rule earlier (in the instructions it reads before acting) |
| A gate that blocks, then the agent retries the same thing | Same message several times in one session | Make the hook's message say exactly what to do instead, or let it rewrite the input itself |
| Blocking messages after writes piling up (PostToolUse / Stop) | Are they new problems each time, or the same list repeated? | Show only what changed since the last write; check at the end rather than after every write |
| A security hook that never fires | Test it with a harmless trigger through the real tool | Fix its input parsing; a silent hook exits 0 and looks healthy |

## Skills, agents, and the owner

| Signal (scan key) | Confirm | Usual fix |
|---|---|---|
| Installed skills never invoked (all-time) | Are they triggered by name elsewhere (a hook, another skill)? grep for them before calling them unused | Retire or merge them; each installed skill costs listing tokens every session |
| Duplicate skills under two names | Two copies with different content? | Keep one source; remove or rename the other |
| Helper agents all on the most expensive model | Does the owner want quality first? Check the ledger before raising | If the owner has not decided: offer a cheaper model for search-only helpers |
| Owner correction lines (section 6) | Read each in context. Count only real corrections: the owner repeating a rule, undoing something, or pushing back | A rule said 3+ times belongs in the global instructions (or a hook), not in one project |
| Owner stepping in to ask for a handoff or a stop | Was the context large? Did the agent miss a stopping point? | Same as the context fixes above |
| /insights facets friction (if present) | The facet text names the sessions; confirm the pattern repeats | Treat as candidates, never as findings on their own |

## Usually not a problem

- A guard that blocked a truly dangerous command.
- A few edit errors per week.
- API errors on one bad day.
- High spend in a week with a big deliverable, when the context share stayed normal.
- Zero interrupts and zero compactions (both are good).

Say these out loud only when the owner might otherwise worry about them.
