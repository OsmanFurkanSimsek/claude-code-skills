# Claude Code usage scan

Window: 2026-10-09 09:00 to 2026-10-09 12:00 UTC (0.1 days). Sessions: 4 (+0 with no assistant turn skipped); subagent runs: 1. Assistant usage counted once per message id (transcripts repeat it per content block). Secrets in examples are redacted.

## 1. Spend and context
- Spend: $9.80 (sum of per-session cost; a session that started before the window counts whole)
- Context tokens processed: 6.2 M; share processed on turns above 200K: 0.0%, above 300K: 0.0%
- By band (share of tokens, turns): lt100k 71.0% (88), 100_200k 29.0% (14), 200_300k 0.0% (0), 300_500k 0.0% (0), gt500k 0.0% (0)
- Sessions past 300K: 0 (spend $0.00); past 200K: 0
- Compactions: 0
- Turn duration: median 28s, p90 96s (102 turns)
- Top sessions by spend: report-builder 10-09 $4; data-pipeline 10-09 $3; notes-app 10-09 $2; claude-setup 10-09 $1
- Main-session tokens by model: claude-opus 5M, claude-sonnet 1M

## 2. Tool failures
- Tool calls: 214; errors by tool: Bash 1
- Bash/PowerShell: 61 calls, 1 errors. Classes:
  - no_such_file: 1
    - `[4444dddd 10-09 11:05] cat logs/load-2026-10-09.log | tail -20` -> cat: logs/load-2026-10-09.log: No such file or directory
- Sessions by start source: startup 3, clear 1; Windows-twin failures in forked sessions: 0
- Bash commands using a heredoc (`<<`): 0 of 61 (a quoting-rule behaviour signal even when none failed)

## 3. Hooks
- Hook events: command/PreToolUse 190, command/Stop 102, command/SessionStart 4
- Blocking errors after tools / at Stop (event, script, first line, count):
  - Stop / stop-hook: 1 x "PROJECT.md was NOT updated after these project edits:"
- Stop blocks "PROJECT.md was NOT updated": 1, followed by an Edit/Write of a PROJECT.md later in the same session: 1
- SessionStart hook output: 4 injections, max 640 chars, avg 512

## 4. Skills and agents
- Skill calls this window (Skill tool): report-style 1, claude-improve 1
- Slash commands this window: /clear 1, /claude-improve 1
- Personal skills installed: 4. Never invoked in any transcript: none
- Last invocation per installed skill: claude-improve 2026-10-09, report-style 2026-10-09, notes-sync 2026-10-08, session-handoff 2026-10-06
- Agent calls by type: general-purpose 1; model argument: none
- Subagent runs by model actually used: claude-opus 1
- Subagent runs by effort (runs, median minutes, median output tokens per run): high 1 (1.8 min, 2,950 tok)
- ToolSearch calls: 3 (max 1 in one session)

## 5. Context weight
- Loaded on every message: ~/.claude/CLAUDE.md 4.1 KB
- Tool output volume (chars total / calls / avg): Read 402K/66/6090; Bash 88K/61/1442; Grep 41K/38/1078
- Tool results over 25K chars: 0
- Cost per source, main session only (helper output is not counted): calls / chars total / avg / largest / over 25K
  - Read: 66 / 402K / 6090 / 19K / 0
  - Bash: 61 / 88K / 1442 / 9K / 0
- Same file Read 3+ times in one session: 0

## 6. Owner friction
- Interrupts: 0. API/system errors: 0
- Owner messages that read like a correction (0 candidates; read in context before counting any):
- /insights facets for 2 sessions, friction: {'excessive_changes': 1}
  - Claude ran the full 140-test suite twice after one-line edits, about 2 minutes in all.

## 7. Metrics (per 7 days unless named otherwise)
Raw counts: the `--json` file also holds `<key>.count` for every `.per_week` key below (the window's own count, for the ledger's `Since Done:` tallies).
```json
{
 "bash.calls.per_week": 3416.0,
 "bash.err.no_such_file.per_week": 56.0,
 "bash.errors.per_week": 56.0,
 "bash.heredoc_used.per_week": 0.0,
 "big_outputs_25k.per_week": 0.0,
 "compactions.per_week": 0.0,
 "ctx.sessions_over_200k.per_week": 0.0,
 "ctx.sessions_over_300k.per_week": 0.0,
 "ctx.share_above_200k.pct": 0.0,
 "ctx.share_above_300k.pct": 0.0,
 "hook.block.Stop.stop-hook.per_week": 56.0,
 "hook.stop.project_md.blocks": 1,
 "hook.stop.project_md.reconciled": 1,
 "interrupts.per_week": 0.0,
 "repeated_reads.per_week": 0.0,
 "sessions": 4,
 "sessions.per_week": 224.0,
 "sessions.startup": 3,
 "spend.usd": 9.8,
 "spend.usd.per_week": 548.8,
 "subagents.per_week": 56.0,
 "toolsearch.per_week": 168.0,
 "window.days": 0.1,
 "window.end": "2026-10-09 12:00",
 "window.since": "2026-10-09",
 "window.start": "2026-10-09 09:00"
}
```
