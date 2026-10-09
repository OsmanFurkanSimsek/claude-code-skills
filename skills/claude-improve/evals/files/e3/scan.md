# Claude Code usage scan

Window: 2026-10-02 08:00 to 2026-10-09 08:00 UTC (7.0 days). Sessions: 12 (+1 with no assistant turn skipped); subagent runs: 9. Assistant usage counted once per message id (transcripts repeat it per content block). Secrets in examples are redacted.

## 1. Spend and context
- Spend: $96.40 (sum of per-session cost; a session that started before the window counts whole)
- Context tokens processed: 61.3 M; share processed on turns above 200K: 19.0%, above 300K: 8.0%
- By band (share of tokens, turns): lt100k 41.2% (612), 100_200k 39.8% (231), 200_300k 11.0% (38), 300_500k 8.0% (17), gt500k 0.0% (0)
- Sessions past 300K: 1 (spend $19.80); past 200K: 3
- Compactions: 0
- Turn duration: median 34s, p90 151s (418 turns)
- Top sessions by spend: report-builder 10-06 $20; notes-app 10-03 $14; report-builder 10-08 $11; data-pipeline 10-04 $9; notes-app 10-07 $8; data-pipeline 10-02 $7
- Main-session tokens by model: claude-opus 49M, claude-sonnet 12M

## 2. Tool failures
- Tool calls: 1,384; errors by tool: Edit 3, Bash 1, WebFetch 1
- Bash/PowerShell: 402 calls, 1 errors. Classes:
  - no_such_file: 1
    - `ls reports/2026-10-07_summary.md` -> ls: cannot access 'reports/2026-10-07_summary.md': No such file or directory
- Sessions by start source: startup 7, clear 5; Windows-twin failures in forked sessions: 0
- Edit/Write errors: no_match 2, not_read_first 1
  - no_match: String to replace not found in file (report-builder, 10-06)
  - not_read_first: File has not been read yet (notes-app, 10-03)
- Bash commands using a heredoc (`<<`): 2 of 402 (a quoting-rule behaviour signal even when none failed)

## 3. Hooks
- Hook events: command/PreToolUse 1186, command/Stop 418, command/SessionStart 12
- SessionStart hook output: 12 injections, max 640 chars, avg 512

## 4. Skills and agents
- Skill calls this window (Skill tool): claude-improve 1, report-style 4
- Slash commands this window: /clear 5, /claude-improve 1
- Personal skills installed: 4. Never invoked in any transcript: none
- Last invocation per installed skill: claude-improve 2026-10-02, report-style 2026-10-08, notes-sync 2026-09-30, session-handoff 2026-09-29
- Agent calls by type: general-purpose 9; model argument: none
- Subagent runs by model actually used: claude-opus 9
- Subagent runs by effort (runs, median minutes, median output tokens per run): high 9 (2.1 min, 3,410 tok)
- ToolSearch calls: 14 (max 3 in one session)

## 5. Context weight
- Loaded on every message: ~/.claude/CLAUDE.md 4.1 KB
- Tool output volume (chars total / calls / avg): Read 1840K/310/5935; Bash 612K/402/1522; Grep 233K/201/1159; WebFetch 96K/6/16000
- Tool results over 25K chars: 1
  - 31K Read (report-builder): reports/2026-10-06_quarterly.md
- Cost per source, main session only (helper output is not counted): calls / chars total / avg / largest / over 25K
  - Read: 310 / 1840K / 5935 / 31K / 1
  - Bash: 402 / 612K / 1522 / 19K / 0
  - WebFetch: 6 / 96K / 16000 / 22K / 0
- Same file Read 3+ times in one session: 1 - top: PLAN.md x3 (report-builder)

## 6. Owner friction
- Interrupts: 0. API/system errors: 0
- Owner messages that read like a correction (0 candidates; read in context before counting any):

## 7. Metrics (per 7 days unless named otherwise)
```json
{
 "bash.calls.per_week": 402.0,
 "bash.err.heredoc_eof.per_week": 0.0,
 "bash.err.no_such_file.per_week": 1.0,
 "bash.errors.per_week": 1.0,
 "bash.heredoc_used.per_week": 2.0,
 "big_outputs_25k.per_week": 1.0,
 "compactions.per_week": 0.0,
 "ctx.sessions_over_200k.per_week": 3.0,
 "ctx.sessions_over_300k.per_week": 1.0,
 "ctx.share_above_200k.pct": 19.0,
 "ctx.share_above_300k.pct": 8.0,
 "edit.err.modified_since.per_week": 0.0,
 "edit.err.no_match.per_week": 2.0,
 "edit.err.not_read_first.per_week": 1.0,
 "interrupts.per_week": 0.0,
 "repeated_reads.per_week": 1.0,
 "sessions": 12,
 "sessions.per_week": 12.0,
 "spend.usd": 96.4,
 "spend.usd.per_week": 96.4,
 "subagents.per_week": 9.0,
 "toolsearch.per_week": 14.0
}
```
