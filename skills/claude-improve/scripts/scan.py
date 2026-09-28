#!/usr/bin/env python3
"""scan.py - measure how Claude Code has been working, from its own session transcripts.

Reads ~/.claude/projects/*/*.jsonl (main sessions) and their subagent files, counts only
entries whose timestamp falls inside the window, and writes:
  --out   a markdown report the agent reads (numbers + a few examples per signal)
  --json  stable metric keys, normalised to "per 7 days", for comparing runs

Usage:
  python scan.py --days 7 --out scan.md --json scan.json
  python scan.py --since 2026-09-20 --out scan.md --json scan.json
Standard library only. Read-only: it never writes anywhere except --out / --json.
"""
import argparse, collections, datetime as dt, glob, json, os, re, statistics, sys

C = collections.Counter
HOME = os.path.expanduser("~")
CLAUDE = os.path.join(HOME, ".claude")

BASH_ERR = {
    "module_not_found": r"No module named|ModuleNotFoundError|Cannot find module",
    "heredoc_eof": r"unexpected EOF|here-document|unterminated quoted|syntax error near unexpected",
    "unicode": r"UnicodeEncodeError|UnicodeDecodeError|'charmap' codec",
    "cmd_not_found": r"command not found|is not recognized as|Python was not found",
    "no_such_file": r"No such file or directory|cannot find the path|FileNotFoundError|Cannot find path",
    "traceback": r"Traceback \(most recent call last\)",
    "timeout": r"timed out|ETIMEDOUT|Command timed out",
    "auth": r"AADSTS|401 Unauthorized|403 Forbidden|token (has )?expired|az login|re-authenticate|not logged in",
    "permission": r"Permission denied|Access is denied|EPERM|EACCES",
    "powershell_parse": r"ParserError|CommandNotFoundException|ParameterBindingException",
    "hook_block": r"hook error|blocked by|BLOCKED",
}
EDIT_ERR = {
    "not_read_first": r"has not been read|must Read|Read it first",
    "no_match": r"String to replace not found|not found in file|old_string",
    "modified_since": r"modified since|has been modified|changed since",
}
# Owner pushback in plain English. A hit is a candidate, never a finding: read it in context.
CORRECTION = re.compile(
    r"\b(why did you|why didn'?t you|I told you|I said|again\b|third time|not what I|that'?s wrong|"
    r"you forgot|you missed|don'?t (do|ask|schedule|use)|stop (doing|asking)|still not|instead of|"
    r"I already|as I said|every time|keep (doing|asking|forgetting))", re.I)
BANDS = [(100e3, "lt100k"), (200e3, "100_200k"), (300e3, "200_300k"), (500e3, "300_500k"), (float("inf"), "gt500k")]
# First line of the PROJECT.md gate's non-blocking note (hooks/furkan-project-md-gate.js NOTE_HEAD).
GATE_NOTE = "PROJECT.md lint - new since your last write"


def band(ctx):
    for lim, name in BANDS:
        if ctx < lim:
            return name


def text_of(c):
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return "\n".join(b.get("text", "") if isinstance(b, dict) else str(b) for b in c)
    return "" if c is None else str(c)


# Secrets are counted, never printed: every example line passes through redact().
SECRET = re.compile(
    # Prefixes written as [x] classes so a leak-gate grep for the literal prefixes never hits this file.
    r"(sk[-]ant[-][\w-]{10,}|gh[p]_\w{20,}|github[_]pat_\w{20,}|xo[x][baprs]-[\w-]{10,}|A[K]IA[0-9A-Z]{16}|apify_api_\w{10,}"
    r"|Bearer\s+[\w.~+/-]{16,}"
    r"|\b[\w-]*(?:token|secret|password|passwd|api[_-]?key|access[_-]?key)[\w-]*[\"']?\s*[=:]\s*[\"']?"
    r"(?![$%<{(\[])(?=[^\s\"'&;|,]*\d)[^\s\"'&;|,]{12,})", re.I)   # a literal value with a digit, not $VAR/<placeholder>


def redact(s):
    return SECRET.sub(lambda m: m.group(0)[:m.group(0).find("=") + 1 if "=" in m.group(0) else 6] + "[REDACTED]", s or "")


def one_line(s, n):
    return redact(re.sub(r"\s+", " ", s or "").strip())[:n]


def parse_ts(s):
    try:
        return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


def hook_script(cmd):
    """Basename of the script a hook command runs (e.g. my-gate.js), else the first word."""
    m = re.findall(r"[\\/]([\w.-]+\.(?:js|sh|py|ps1|cjs|mjs))", cmd or "")
    return m[-1] if m else one_line(cmd, 30)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=float, default=7)
    ap.add_argument("--since", help="YYYY-MM-DD or 'YYYY-MM-DD HH:MM' in UTC (overrides --days); "
                    "use a fix's Done time to judge it only on traffic after the fix")
    ap.add_argument("--from-ledger", help="ledger file: scan from its 'Last run:' date/time to now, however "
                    "long or short that is (no Last run: every transcript on disk). Overrides --since/--days")
    ap.add_argument("--projects-dir", default=os.path.join(CLAUDE, "projects"))
    ap.add_argument("--out", help="markdown report path (default: stdout)")
    ap.add_argument("--json", help="metrics JSON path")
    ap.add_argument("--examples", type=int, default=3, help="examples kept per signal")
    a = ap.parse_args()

    now = dt.datetime.now(dt.timezone.utc)
    since = (dt.datetime.fromisoformat(a.since).replace(tzinfo=dt.timezone.utc) if a.since
             else now - dt.timedelta(days=a.days))
    open_start = False
    if a.from_ledger:
        # From the previous run to now, never time-bound: 5 days, a month or 3 months are all covered.
        with open(a.from_ledger, encoding="utf-8") as fh:
            m = re.search(r"^Last run:\s*(\d{4}-\d{2}-\d{2})(?:[ T](\d{2}:\d{2}))?", fh.read(), re.M)
        if not m:
            since = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc); open_start = True
        else:
            last = dt.datetime.fromisoformat(m.group(1) + " " + (m.group(2) or "00:00"))
            since = last.replace(tzinfo=dt.timezone.utc)
    days = max((now - since).total_seconds() / 86400, 1e-9)
    per_week = lambda n: round(n * 7 / days, 2)
    since_ms = since.timestamp()

    main_files = glob.glob(os.path.join(a.projects_dir, "*", "*.jsonl"))
    sub_files = glob.glob(os.path.join(a.projects_dir, "*", "*", "subagents", "*.jsonl"))

    # ---- accumulators ----
    sessions = {}                      # sid -> dict
    tool_calls = C(); tool_err = C(); bash_err = C(); bash_ex = collections.defaultdict(list)
    edit_err = C(); edit_ex = collections.defaultdict(list); bash_first = C(); exports = C()
    out_chars = C(); out_n = C(); big_out = []; reads_rep = []; mcp_calls = C(); mcp_err = C()
    hook_att = C(); hook_msgs = C(); pre_blocks = C(); pre_ex = collections.defaultdict(list); gate_notes = C()
    skills_win = C(); cmds_win = C(); agents = C(); agent_model_arg = C()
    band_tok = C(); band_turns = C(); compacts = C(); api_err = C(); interrupts = 0
    corrections = []; toolsearch = []; turn_ms = []; ss_sizes = []; cwd_seen = C()
    model_tok = C(); heredoc_used = 0; secrets_in_cmds = 0; secret_where = set(); empty_sessions = 0

    for f in main_files:
        try:
            if os.path.getmtime(f) < since_ms:
                continue
        except OSError:
            continue
        sid = os.path.basename(f)[:-6]
        s = None
        id2 = {}; seen_msg = set(); reads = C(); ts_n = 0; cost = None; cost_models = {}
        with open(f, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    o = json.loads(line)
                except Exception:
                    continue
                t = o.get("type")
                if t == "cost-state":           # cumulative; keep the latest in the file
                    cost = o.get("totalCostUSD"); cost_models = o.get("modelUsage") or {}
                    continue
                ts = parse_ts(o.get("timestamp") or "")
                if ts is None or ts < since:
                    continue
                if s is None:
                    s = sessions[sid] = {"project": "?", "first": ts, "last": ts, "max_ctx": 0, "turns": 0}
                s["last"] = ts
                if o.get("cwd"):
                    s["project"] = os.path.basename(o["cwd"].rstrip("\\/")) or o["cwd"]
                    s["cwd"] = o["cwd"]
                if t == "system":
                    st = o.get("subtype")
                    if st == "compact_boundary":
                        compacts[(o.get("compactMetadata") or {}).get("trigger", "?")] += 1
                    elif st == "turn_duration":
                        turn_ms.append(o.get("durationMs") or 0)
                    elif st and "error" in st.lower():
                        api_err[st] += 1
                elif t == "attachment":
                    at = (o.get("attachment") or {})
                    typ = str(at.get("type", ""))
                    if typ.startswith("hook"):
                        ev = str(at.get("hookName", "?")).split(":")[0]
                        hook_att[(typ, ev)] += 1
                        if typ in ("hook_blocking_error", "hook_error", "hook_non_blocking_error"):
                            be = at.get("blockingError")
                            msg = str(be.get("blockingError") if isinstance(be, dict) else (be or at.get("stderr") or ""))
                            # The message often starts with '[<hook command>]: '; name the script from it.
                            pm = re.match(r"\[(.*?)\]: (.*)", msg, re.S)
                            script = hook_script(at.get("command") or (pm.group(1) if pm else "")) or (ev.lower() + "-hook")
                            first = (pm.group(2) if pm else msg).strip().split("\n")[0]
                            hook_msgs[(ev, script, one_line(first, 110))] += 1
                        if ev == "SessionStart" and at.get("content"):
                            ss_sizes.append(len(text_of(at.get("content"))))
                        # Non-blocking lint notes after a write (since 2026-09-28 the PROJECT.md gate no
                        # longer blocks), so ledger CI-3 counts them next to the blocks.
                        if typ == "hook_additional_context" and text_of(at.get("content")).startswith(GATE_NOTE):
                            gate_notes[(ev, "furkan-project-md-gate.js")] += 1
                elif t == "assistant":
                    m = o.get("message") or {}
                    mid = m.get("id")
                    if mid and mid not in seen_msg:     # one entry per content block; count usage once
                        seen_msg.add(mid)
                        u = m.get("usage") or {}
                        ctx = sum(u.get(k) or 0 for k in ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))
                        if ctx:
                            band_tok[band(ctx)] += ctx; band_turns[band(ctx)] += 1
                            s["max_ctx"] = max(s["max_ctx"], ctx); s["turns"] += 1
                            model_tok[m.get("model", "?")] += ctx
                    for b in m.get("content") or []:
                        if not isinstance(b, dict) or b.get("type") != "tool_use":
                            continue
                        nm = b.get("name", "?"); inp = b.get("input") or {}
                        id2[b.get("id")] = (nm, inp)
                        tool_calls[nm] += 1
                        if nm.startswith("mcp__"):
                            mcp_calls[nm.split("__")[1]] += 1
                        if nm == "Read":
                            reads[inp.get("file_path", "")] += 1
                        elif nm == "ToolSearch":
                            ts_n += 1
                        elif nm == "Skill":
                            skills_win[inp.get("skill", "?")] += 1
                        elif nm in ("Agent", "Task"):
                            agents[inp.get("subagent_type") or "(default)"] += 1
                            agent_model_arg[inp.get("model") or "(inherits parent)"] += 1
                        elif nm == "Bash":
                            cmd = inp.get("command") or ""
                            w = cmd.strip().split()
                            if w:
                                bash_first[w[0][:25]] += 1
                            if "<<" in cmd:
                                heredoc_used += 1
                            if SECRET.search(cmd):
                                secrets_in_cmds += 1
                                secret_where.add(s["project"] + " " + sid[:8] + " " + ts.strftime("%m-%d"))
                            for var in re.findall(r"\bexport\s+([A-Za-z_][A-Za-z0-9_]*)=", cmd):
                                exports[var] += 1
                elif t == "user":
                    m = o.get("message") or {}
                    c = m.get("content")
                    if isinstance(c, str):
                        if "[Request interrupted" in c:
                            interrupts += 1
                        cm = re.findall(r"<command-name>/?([^<\s]+)</command-name>", c)
                        if cm:
                            cmds_win[cm[0]] += 1
                        elif not c.startswith("<") and len(c) < 2000 and CORRECTION.search(c) and not o.get("isMeta"):
                            item = (s["project"] + " " + sid[:8], ts.strftime("%m-%d %H:%M"), one_line(c, 260))
                            if item not in corrections:
                                corrections.append(item)
                        continue
                    for b in c or []:
                        if not isinstance(b, dict):
                            continue
                        if b.get("type") == "text" and "[Request interrupted" in b.get("text", ""):
                            interrupts += 1
                        if b.get("type") != "tool_result":
                            continue
                        nm, inp = id2.get(b.get("tool_use_id"), ("?", {}))
                        txt = text_of(b.get("content"))
                        out_chars[nm] += len(txt); out_n[nm] += 1
                        if len(txt) > 25000:
                            big_out.append((len(txt), nm, s["project"], one_line(json.dumps(inp)[:200], 110)))
                        if not b.get("is_error"):
                            continue
                        tool_err[nm] += 1
                        if nm.startswith("mcp__"):
                            mcp_err[nm.split("__")[1]] += 1
                        pm = re.match(r"PreToolUse:(\w+) hook error: \[(.*?)\]: (.*)", txt, re.S)
                        if pm:
                            key = (pm.group(1), hook_script(pm.group(2)))
                            pre_blocks[key] += 1
                            if len(pre_ex[key]) < a.examples:
                                pre_ex[key].append(f"[{sid[:8]} {ts:%m-%d %H:%M}] " + one_line(pm.group(3), 200))
                            continue
                        if nm in ("Bash", "PowerShell"):
                            hit = False
                            for k, p in BASH_ERR.items():
                                if re.search(p, txt):
                                    bash_err[k] += 1; hit = True
                                    if len(bash_ex[k]) < a.examples:
                                        bash_ex[k].append((f"[{sid[:8]} {ts:%m-%d %H:%M}] " + one_line(inp.get("command", ""), 120), one_line(txt, 160)))
                            if not hit:
                                bash_err["other"] += 1
                                if len(bash_ex["other"]) < a.examples + 3:
                                    bash_ex["other"].append((f"[{sid[:8]} {ts:%m-%d %H:%M}] " + one_line(inp.get("command", ""), 120), one_line(txt, 160)))
                        elif nm in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
                            k = next((k for k, p in EDIT_ERR.items() if re.search(p, txt)), "other")
                            edit_err[k] += 1
                            if len(edit_ex[k]) < a.examples:
                                edit_ex[k].append(f"[{sid[:8]} {ts:%m-%d %H:%M}] " + one_line(txt, 160))
        if s is not None and s["turns"] == 0:       # a failed probe (e.g. claude -p with a dead key)
            del sessions[sid]; empty_sessions += 1
            s = None
        if s is not None:
            s["cost"] = cost; s["models"] = cost_models; s["toolsearch"] = ts_n
            for fp, n in reads.items():
                if n >= 3:
                    reads_rep.append((n, s["project"], os.path.basename(fp)))
            cwd_seen[s.get("cwd", "")] += 1
            toolsearch.append(ts_n)

    # ---- subagent files: which model actually ran ----
    sub_models = C(); sub_n = 0
    for f in sub_files:
        try:
            if os.path.getmtime(f) < since_ms:
                continue
        except OSError:
            continue
        mdl = None
        with open(f, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if '"type":"assistant"' in line:
                    try:
                        o = json.loads(line)
                    except Exception:
                        continue
                    ts = parse_ts(o.get("timestamp") or "")
                    if ts and ts >= since:
                        mdl = (o.get("message") or {}).get("model")
                        break
        if mdl:
            sub_models[mdl] += 1; sub_n += 1

    # ---- all-time skill use (fast path: only lines that can hold a skill call) ----
    skills_all = C(); skills_last = {}
    for f in main_files:
        with open(f, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if '"name":"Skill"' not in line and "<command-name>" not in line:
                    continue
                try:
                    o = json.loads(line)
                except Exception:
                    continue
                day = (o.get("timestamp") or "")[:10]
                names = []
                m = o.get("message") or {}
                c = m.get("content")
                if isinstance(c, str):
                    names += re.findall(r"<command-name>/?([^<\s]+)</command-name>", c)
                elif isinstance(c, list):
                    for b in c:
                        if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") == "Skill":
                            names.append((b.get("input") or {}).get("skill", "?"))
                for n in names:
                    n = n.split(":")[-1]
                    skills_all[n] += 1
                    skills_last[n] = max(skills_last.get(n, ""), day)
    installed = sorted(d for d in os.listdir(os.path.join(CLAUDE, "skills"))
                       if os.path.isfile(os.path.join(CLAUDE, "skills", d, "SKILL.md"))) \
        if os.path.isdir(os.path.join(CLAUDE, "skills")) else []

    # ---- always-loaded context (paid on every message) ----
    def size(p):
        try:
            return os.path.getsize(p)
        except OSError:
            return None
    always = [("~/.claude/CLAUDE.md", size(os.path.join(CLAUDE, "CLAUDE.md")))]
    for r in sorted(glob.glob(os.path.join(CLAUDE, "rules", "*.md"))):
        always.append(("~/.claude/rules/" + os.path.basename(r), size(r)))
    proj_md = []
    for cwd, n in cwd_seen.most_common():
        if cwd:
            b = size(os.path.join(cwd, "CLAUDE.md"))
            if b:
                proj_md.append((os.path.basename(cwd.rstrip("\\/")), b, n))

    # ---- optional /insights facets ----
    facets = []
    fdir = os.path.join(CLAUDE, "usage-data", "facets")
    for fp in glob.glob(os.path.join(fdir, "*.json")):
        try:
            j = json.load(open(fp, encoding="utf-8"))
        except Exception:
            continue
        if j.get("session_id") in sessions:
            facets.append(j)

    # ---- derived numbers ----
    S = list(sessions.values())
    if open_start and S:            # first run over every transcript: the window starts at the oldest one
        since = min(x["first"] for x in S)
        days = max((now - since).total_seconds() / 86400, 1e-9)   # per_week() reads this at call time
    tot_tok = sum(band_tok.values()) or 1
    share = lambda keys: round(100 * sum(band_tok[k] for k in keys) / tot_tok, 1)
    spend = sum(x["cost"] or 0 for x in S)
    over300 = [x for x in S if x["max_ctx"] > 300e3]
    over200 = [x for x in S if x["max_ctx"] > 200e3]
    bash_calls = tool_calls["Bash"] + tool_calls["PowerShell"]
    metrics = {
        "window.days": round(days, 1), "window.since": since.strftime("%Y-%m-%d"),
        "sessions": len(S), "sessions.per_week": per_week(len(S)),
        "spend.usd": round(spend, 2), "spend.usd.per_week": per_week(spend),
        "spend.over300k_sessions.pct": round(100 * sum(x["cost"] or 0 for x in over300) / spend, 1) if spend else 0,
        "ctx.tokens.m": round(tot_tok / 1e6, 1),
        "ctx.share_above_200k.pct": share(["200_300k", "300_500k", "gt500k"]),
        "ctx.share_above_300k.pct": share(["300_500k", "gt500k"]),
        "ctx.sessions_over_300k.per_week": per_week(len(over300)), "ctx.sessions_over_200k.per_week": per_week(len(over200)),
        "bash.heredoc_used.per_week": per_week(heredoc_used),
        "secrets.in_commands.per_week": per_week(secrets_in_cmds),
        "sessions.empty_skipped": empty_sessions,
        "compactions.per_week": per_week(sum(compacts.values())),
        "bash.calls.per_week": per_week(bash_calls),
        "bash.errors.per_week": per_week(tool_err["Bash"] + tool_err["PowerShell"]),
        "interrupts.per_week": per_week(interrupts),
        "subagents.per_week": per_week(sub_n),
        "toolsearch.per_week": per_week(sum(toolsearch)),
        "big_outputs_25k.per_week": per_week(len(big_out)),
        "repeated_reads.per_week": per_week(len(reads_rep)),
    }
    for k, v in bash_err.items():
        metrics["bash.err." + k + ".per_week"] = per_week(v)
    for k, v in edit_err.items():
        metrics["edit.err." + k + ".per_week"] = per_week(v)
    for (ev, script, _), v in hook_msgs.items():
        key = "hook.block." + ev + "." + script + ".per_week"
        metrics[key] = round(metrics.get(key, 0) + per_week(v), 2)
    for (tool, script), v in pre_blocks.items():
        key = "hook.block.PreToolUse." + script + ".per_week"
        metrics[key] = round(metrics.get(key, 0) + per_week(v), 2)
    for (ev, script), v in gate_notes.items():
        key = "hook.context." + ev + "." + script + ".per_week"
        metrics[key] = round(metrics.get(key, 0) + per_week(v), 2)
    for k, v in exports.items():
        metrics["bash.export." + k + ".per_week"] = per_week(v)
    for k, v in skills_win.items():                  # plugin:name and name count as one skill
        key = "skill.calls." + k.split(":")[-1] + ".per_week"
        metrics[key] = round(metrics.get(key, 0) + per_week(v), 2)

    # ---- report ----
    L = []
    P = L.append
    P("# Claude Code usage scan")
    P("")
    P(f"Window: {since:%Y-%m-%d %H:%M} to {now:%Y-%m-%d %H:%M} UTC ({days:.1f} days). Sessions: {len(S)} "
      f"(+{empty_sessions} with no assistant turn skipped); subagent runs: {sub_n}. "
      "Assistant usage counted once per message id (transcripts repeat it per content block). "
      "Secrets in examples are redacted.")
    if secrets_in_cmds:
        P("")
        P(f"**SECRETS: {secrets_in_cmds} command(s) carried a token-shaped value in plain text** "
          f"(where: {'; '.join(sorted(secret_where)[:6])}). Count only; never print or copy the value. "
          "The fix is rotation by the owner, raised first in the report.")
    P("")
    P("## 1. Spend and context")
    P(f"- Spend: ${spend:,.2f} (sum of per-session cost; a session that started before the window counts whole)")
    P(f"- Context tokens processed: {tot_tok/1e6:,.1f} M; share processed on turns above 200K: "
      f"{metrics['ctx.share_above_200k.pct']}%, above 300K: {metrics['ctx.share_above_300k.pct']}%")
    P("- By band (share of tokens, turns): " + ", ".join(
        f"{n} {round(100*band_tok[n]/tot_tok,1)}% ({band_turns[n]})" for _, n in BANDS))
    P(f"- Sessions past 300K: {len(over300)} (spend ${sum(x['cost'] or 0 for x in over300):,.2f}); past 200K: {len(over200)}")
    P(f"- Compactions: {dict(compacts) or 0}")
    if turn_ms:
        tm = sorted(turn_ms)
        P(f"- Turn duration: median {tm[len(tm)//2]/1000:.0f}s, p90 {tm[int(len(tm)*.9)]/1000:.0f}s ({len(tm)} turns)")
    P("- Top sessions by spend: " + "; ".join(
        f"{x['project']} {x['first']:%m-%d} ${x['cost'] or 0:,.0f} max {x['max_ctx']//1000}K"
        for x in sorted(S, key=lambda x: -(x["cost"] or 0))[:6]))
    P("- Main-session tokens by model: " + ", ".join(f"{k} {v/1e6:,.0f}M" for k, v in model_tok.most_common(5)))
    P("")
    P("## 2. Tool failures")
    P(f"- Tool calls: {sum(tool_calls.values())}; errors by tool: " + ", ".join(f"{k} {v}" for k, v in tool_err.most_common(10)))
    P(f"- Bash/PowerShell: {bash_calls} calls, {tool_err['Bash'] + tool_err['PowerShell']} errors. Classes:")
    for k, v in bash_err.most_common():
        P(f"  - {k}: {v}")
        for cmd, err in bash_ex[k]:
            P(f"    - `{cmd}` -> {err}")
    if edit_err:
        P("- Edit/Write errors: " + ", ".join(f"{k} {v}" for k, v in edit_err.most_common()))
        for k, ex in edit_ex.items():
            for e in ex:
                P(f"  - {k}: {e}")
    if mcp_calls:
        P("- MCP calls (errors) by server: " + ", ".join(f"{k} {v} ({mcp_err[k]})" for k, v in mcp_calls.most_common(10)))
    P(f"- Bash commands using a heredoc (`<<`): {heredoc_used} of {bash_calls} (a quoting-rule behaviour signal "
      "even when none failed)")
    if exports:
        P("- Env vars re-exported inside commands (a profile/setup gap if frequent): "
          + ", ".join(f"{k} x{v}" for k, v in exports.most_common(8)))
    P("")
    P("## 3. Hooks")
    P("- Hook events: " + ", ".join(f"{t}/{e} {v}" for (t, e), v in hook_att.most_common(12)))
    if pre_blocks:
        P("- PreToolUse blocks (tool, script, count):")
        for (tool, script), v in pre_blocks.most_common(10):
            P(f"  - {tool} / {script}: {v}")
            for e in pre_ex[(tool, script)]:
                P(f"    - {e}")
    if hook_msgs:
        P("- Blocking errors after tools / at Stop (event, script, first line, count):")
        for (ev, script, msg), v in hook_msgs.most_common(12):
            P(f"  - {ev} / {script}: {v} x \"{msg}\"")
    if gate_notes:
        P("- Non-blocking lint notes after writes (event, script, count): "
          + ", ".join(f"{ev} / {script}: {v}" for (ev, script), v in gate_notes.most_common()))
    if ss_sizes:
        P(f"- SessionStart hook output: {len(ss_sizes)} injections, max {max(ss_sizes)} chars, avg {sum(ss_sizes)//len(ss_sizes)}")
    P("")
    P("## 4. Skills and agents")
    P("- Skill calls this window (Skill tool): " + (", ".join(f"{k} {v}" for k, v in skills_win.most_common()) or "none"))
    P("- Slash commands this window: " + (", ".join(f"/{k} {v}" for k, v in cmds_win.most_common(15)) or "none"))
    never = [n for n in installed if skills_all[n] == 0]
    P(f"- Personal skills installed: {len(installed)}. Never invoked in any transcript: {', '.join(never) or 'none'}")
    P("- Last invocation per installed skill: " + ", ".join(f"{n} {skills_last.get(n, 'never')}" for n in installed))
    P("- Agent calls by type: " + (", ".join(f"{k} {v}" for k, v in agents.most_common(8)) or "none")
      + "; model argument: " + (", ".join(f"{k} {v}" for k, v in agent_model_arg.most_common()) or "none"))
    P("- Subagent runs by model actually used: " + (", ".join(f"{k} {v}" for k, v in sub_models.most_common()) or "none"))
    P(f"- ToolSearch calls: {sum(toolsearch)} (max {max(toolsearch) if toolsearch else 0} in one session)")
    P("")
    P("## 5. Context weight")
    P("- Loaded on every message: " + ", ".join(f"{n} {b/1024:.1f} KB" for n, b in always if b))
    if proj_md:
        P("- Project CLAUDE.md files (size, sessions this window): " + ", ".join(f"{n} {b/1024:.1f} KB x{s}" for n, b, s in proj_md[:10]))
    P("- Tool output volume (chars total / calls / avg): " + "; ".join(
        f"{k} {v//1000}K/{out_n[k]}/{v//max(1,out_n[k])}" for k, v in out_chars.most_common(8)))
    P(f"- Tool results over 25K chars: {len(big_out)}")
    for n, nm, proj, inp in sorted(big_out, reverse=True)[:8]:
        P(f"  - {n//1000}K {nm} ({proj}): {inp}")
    P(f"- Same file Read 3+ times in one session: {len(reads_rep)}"
      + (" - top: " + ", ".join(f"{f} x{n} ({p})" for n, p, f in sorted(reads_rep, reverse=True)[:6]) if reads_rep else ""))
    P("")
    P("## 6. Owner friction")
    P(f"- Interrupts: {interrupts}. API/system errors: {dict(api_err) or 0}")
    P(f"- Owner messages that read like a correction ({len(corrections)} candidates; read in context before counting any):")
    for proj, day, txt in corrections[:40]:
        P(f"  - [{proj} {day}] {txt}")
    if facets:
        fr = C()
        for j in facets:
            fr.update(j.get("friction_counts") or {})
        P(f"- /insights facets for {len(facets)} sessions, friction: {dict(fr.most_common(10))}")
        for j in facets:
            if j.get("friction_detail"):
                P(f"  - {one_line(j['friction_detail'], 220)}")
    P("")
    P("## 7. Metrics (per 7 days unless named otherwise)")
    P("```json")
    P(json.dumps(metrics, indent=1, sort_keys=True))
    P("```")

    report = "\n".join(L) + "\n"
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(report)
    else:
        sys.stdout.write(report)
    if a.json:
        with open(a.json, "w", encoding="utf-8") as fh:
            json.dump(metrics, fh, indent=1, sort_keys=True)
    print(f"scan: {len(S)} sessions, {days:.1f} days, report {len(report)//1024} KB"
          + (f" -> {a.out}" if a.out else ""), file=sys.stderr)


if __name__ == "__main__":
    main()
