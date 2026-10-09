# Claude Code usage scan

Window: 2026-09-18 08:00 to 2026-10-09 08:00 UTC (21.0 days). Sessions: 38 (+2 with no assistant turn skipped); subagent runs: 27. Assistant usage counted once per message id (transcripts repeat it per content block). Secrets in examples are redacted.

## 1. Spend and context
- Spend: $286.10 (sum of per-session cost; a session that started before the window counts whole)
- Context tokens processed: 182.4 M; share processed on turns above 200K: 14.2%, above 300K: 4.1%
- By band (share of tokens, turns): lt100k 46.0% (1904), 100_200k 39.8% (702), 200_300k 10.1% (88), 300_500k 4.1% (31), gt500k 0.0% (0)
- Sessions past 300K: 2 (spend $31.20); past 200K: 7
- Compactions: 0
- Turn duration: median 31s, p90 140s (1311 turns)
- Top sessions by spend: report-builder 09-23 $22; data-pipeline 10-01 $19; notes-app 10-07 $16; report-builder 09-29 $14; data-pipeline 09-24 $12; notes-app 10-02 $11
- Main-session tokens by model: claude-opus 151M, claude-sonnet 31M

## 2. Tool failures
- Tool calls: 4,210; errors by tool: Edit 6, Bash 4, WebFetch 2
- Bash/PowerShell: 1206 calls, 4 errors. Classes:
  - no_such_file: 3
    - `cat data/export_0921.csv | head` -> cat: data/export_0921.csv: No such file or directory
  - exit_nonzero: 1
    - `pytest -q tests/test_load.py` -> 1 failed, 14 passed
- Sessions by start source: startup 22, clear 16; Windows-twin failures in forked sessions: 0
- Edit/Write errors: no_match 4, not_read_first 2
- Bash commands using a heredoc (`<<`): 5 of 1206 (a quoting-rule behaviour signal even when none failed)

## 3. Hooks
- Hook events: command/PreToolUse 3790, command/Stop 1311, command/SessionStart 38
- SessionStart hook output: 38 injections, max 640 chars, avg 509

## 4. Skills and agents
- Skill calls this window (Skill tool): report-style 11, claude-improve 1
- Slash commands this window: /clear 16, /claude-improve 1
- Personal skills installed: 4. Never invoked in any transcript: none
- Last invocation per installed skill: claude-improve 2026-09-18, report-style 2026-10-08, notes-sync 2026-10-03, session-handoff 2026-10-05
- Agent calls by type: general-purpose 27; model argument: none
- Subagent runs by model actually used: claude-opus 27
- Subagent runs by effort (runs, median minutes, median output tokens per run): high 27 (2.4 min, 3,620 tok)
- ToolSearch calls: 41 (max 4 in one session)

## 5. Context weight
- Loaded on every message: ~/.claude/CLAUDE.md 4.1 KB
- Tool output volume (chars total / calls / avg): Read 5310K/905/5867; Bash 1830K/1206/1517; Grep 702K/588/1193
- Tool results over 25K chars: 2
  - 34K Read (report-builder): reports/2026-09/2026-09-23_monthly.md
  - 27K Read (data-pipeline): logs/load-2026-10-01.log
- Same file Read 3+ times in one session: 2 - top: PLAN.md x3 (report-builder), PLAN.md x3 (data-pipeline)

## 6. Owner friction
- Interrupts: 3. API/system errors: 0
- Owner messages that read like a correction (6 candidates; read in context before counting any):
  - [report-builder 09-22] no, run the check now, don't schedule it for later. you have the query, run it
  - [report-builder 09-23] no worries, take your time with the chart
  - [data-pipeline 09-30] again: run the check now, don't schedule it for later. a check on a list never happens
  - [notes-app 10-02] stop here for today, I'll continue tomorrow
  - [data-pipeline 10-03] no, use the September file instead of August
  - [notes-app 10-07] I said this before: run the check now, don't schedule it for later

## 7. Metrics (per 7 days unless named otherwise)
```json
{
 "bash.calls.per_week": 402.0,
 "bash.err.exit_nonzero.per_week": 0.33,
 "bash.err.no_such_file.per_week": 1.0,
 "bash.errors.per_week": 1.33,
 "bash.heredoc_used.per_week": 1.67,
 "big_outputs_25k.per_week": 0.67,
 "compactions.per_week": 0.0,
 "ctx.sessions_over_200k.per_week": 2.33,
 "ctx.sessions_over_300k.per_week": 0.67,
 "ctx.share_above_200k.pct": 14.2,
 "ctx.share_above_300k.pct": 4.1,
 "edit.err.modified_since.per_week": 0.0,
 "edit.err.no_match.per_week": 1.33,
 "edit.err.not_read_first.per_week": 0.67,
 "interrupts.per_week": 1.0,
 "repeated_reads.per_week": 0.67,
 "sessions": 38,
 "sessions.per_week": 12.67,
 "spend.usd": 286.1,
 "spend.usd.per_week": 95.37,
 "subagents.per_week": 9.0,
 "toolsearch.per_week": 13.67
}
```
