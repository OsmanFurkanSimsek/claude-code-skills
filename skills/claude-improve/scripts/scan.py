#!/usr/bin/env python3
"""scan.py - measure how Claude Code has been working, from its own session transcripts.

Reads ~/.claude/projects/*/*.jsonl (main sessions) and their subagent files, counts only
entries whose timestamp falls inside the window, and writes:
  --out   a markdown report the agent reads (numbers + a few examples per signal)
  --json  stable metric keys, normalised to "per 7 days", for comparing runs, plus each one's raw <key>.count

Usage:
  python scan.py --days 7 --out scan.md --json scan.json
  python scan.py --since 2026-09-20 --out scan.md --json scan.json
  python scan.py --since "2026-10-09 10:30" --until "2026-10-09 12:00" --json since-done.json   (a Done inside the window)
Standard library only. Read-only: it never writes anywhere except --out / --json.
Test runs (eval relays, temp-folder child runs) stay out of every metric and are counted in the header;
--include-test-runs keeps them in.
"""
import argparse, collections, datetime as dt, glob, json, os, re, statistics, sys
import contextlib, importlib.util

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
    # Ledger CI-21: a Windows twin of a shell tool answered (System32 find/sort/timeout, WSL bash).
    "windows_twin": r"FIND: Parameter format not correct|Input file specified two times|"
                    r"ERROR: Invalid value for timeout|Windows Subsystem for Linux has no installed",
}
# Project folders of test runs, not the owner's work: eval relays (skill-creator `*-workspace-*`) and child
# runs started in a temp or scratchpad folder. 2026-10-08: 379 of 444 sessions in one window were these.
TEST_RUN_DIR = re.compile(r"AppData-Local-Temp|-workspace-", re.I)
# An env var set by the command itself: `export NAME=` only at a command position (start, after ; & | ( or a
# newline, or after then/do/else). `grep -q '^export PATH='` reads a file and is no export (2026-10-09 replay: 17 of 17 PATH hits).
EXPORT_AT_COMMAND = re.compile(r"(?:(?:^|[;&|(\n])\s*|\b(?:then|do|else)\s+)export\s+([A-Za-z_][A-Za-z0-9_]*)=")
# First line of the Stop gate's block when project files changed but PROJECT.md did not (hooks/furkan-stop-gate.js).
STOP_PROJECT_MD = "PROJECT.md was NOT updated"
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
# Owner asks about the time left while work runs (a pattern count, ledger key owner.time_asks).
TIME_ASK = re.compile(r"\b(how far are you|how long (will|does|is|do)|how much (more )?time|when will (it|you|this|that)|"
                      r"your estimate|take a long time|are you still working|still running\?)", re.I)
# A correction candidate about voice, tone or wording of a text written as the owner (owner.corrections.voice).
VOICE = re.compile(r"\b(voice|tone|sounds? like me|my style|my wording)\b", re.I)
# The tool a call named does not exist in that session (a disabled plugin or server, a wrong name).
NO_SUCH_TOOL = "No such tool available"
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


def private_sections(folder, ctx):
    """Optional local add-ons, never shipped publicly: every <folder>/*.private.py except test_*.

    Interface: the add-on defines section(ctx) and may set TITLE (default: its file name). ctx holds
    projects_dir, since, now (aware UTC datetimes), days and examples. section() returns a list of
    markdown lines, or (lines, metrics); metric keys join this scan's metrics as "<file stem>.<key>".
    Each add-on gets its own "## <TITLE>" section before the metrics. One that fails to import or
    raises gives one line instead and the scan goes on; metrics that JSON cannot hold are dropped with one line.
    Loading writes no bytecode. No add-on: report and metrics are unchanged.
    """
    lines, metrics = [], {}
    for path in sorted(glob.glob(os.path.join(folder, "*.private.py"))):
        name = os.path.basename(path)
        if name.startswith("test_"):
            continue
        stem = name[:-len(".private.py")]
        modname = "scan_addon_" + re.sub(r"\W", "_", stem)
        keep_flag = sys.dont_write_bytecode
        sys.dont_write_bytecode = True                      # loading never writes a __pycache__ next to the add-on
        try:
            with contextlib.redirect_stdout(sys.stderr):    # an add-on's prints never reach the report
                spec = importlib.util.spec_from_file_location(modname, path)
                mod = importlib.util.module_from_spec(spec)
                sys.modules[modname] = mod                  # dataclasses and typing look the module up by name
                spec.loader.exec_module(mod)
                out = mod.section(dict(ctx))
            body, extra = out if isinstance(out, tuple) else (out, {})
            sec = ["", "## " + one_line(str(getattr(mod, "TITLE", stem)), 120)] + [str(x) for x in body]
            add = {stem + "." + str(k): v for k, v in (extra or {}).items()}
            try:
                json.dumps(add, sort_keys=True)
            except (TypeError, ValueError):
                sec, add = sec + [f"- Add-on {name}: metrics dropped (not JSON-serialisable)"], {}
        except (Exception, SystemExit) as e:
            sec, add = ["", f"- Add-on {name} not run: {type(e).__name__}: {one_line(str(e), 150)}"], {}
        finally:
            sys.dont_write_bytecode = keep_flag
            sys.modules.pop(modname, None)
        lines += sec
        metrics.update(add)
    return lines, metrics


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=float, default=7)
    ap.add_argument("--since", help="YYYY-MM-DD or 'YYYY-MM-DD HH:MM' in UTC (overrides --days); "
                    "use a fix's Done time to judge it only on traffic after the fix")
    ap.add_argument("--from-ledger", help="ledger file: scan from its 'Last run:' date/time to now, however "
                    "long or short that is (no Last run: every transcript on disk). Overrides --since/--days")
    ap.add_argument("--until", help="'YYYY-MM-DD HH:MM' UTC, exclusive (default: now); a Done time inside this "
                    "run's window is scanned --since Done --until the window's end, so its tally stops where the window does")
    ap.add_argument("--projects-dir", default=os.path.join(CLAUDE, "projects"))
    ap.add_argument("--out", help="markdown report path (default: stdout)")
    ap.add_argument("--json", help="metrics JSON path")
    ap.add_argument("--examples", type=int, default=3, help="examples kept per signal")
    ap.add_argument("--private-dir", default=os.path.dirname(os.path.abspath(__file__)),
                    help="folder whose *.private.py add-ons add their own sections (default: this script's folder)")
    ap.add_argument("--include-test-runs", action="store_true",
                    help="count eval and temp-folder test runs too (default: left out, named in the header)")
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
    end = dt.datetime.fromisoformat(a.until).replace(tzinfo=dt.timezone.utc) if a.until else now
    days = max((end - since).total_seconds() / 86400, 1e-9)
    per_week = lambda n: round(n * 7 / days, 2)
    since_ms = since.timestamp()

    main_files = glob.glob(os.path.join(a.projects_dir, "*", "*.jsonl"))
    sub_files = glob.glob(os.path.join(a.projects_dir, "*", "*", "subagents", "*.jsonl"))

    # ---- test runs: left out of every metric, but counted (with their spend) so nothing is hidden ----
    is_test = lambda f: TEST_RUN_DIR.search(os.path.relpath(f, a.projects_dir).replace("\\", "/").split("/")[0])
    test_n = 0; test_cost = 0.0
    if not a.include_test_runs:
        test_files = [f for f in main_files if is_test(f)]
        main_files = [f for f in main_files if not is_test(f)]
        sub_files = [f for f in sub_files if not is_test(f)]
        for f in test_files:
            try:
                if os.path.getmtime(f) < since_ms:
                    continue
            except OSError:
                continue
            test_n += 1; cost = None
            with open(f, encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    if '"cost-state"' in line:
                        with contextlib.suppress(Exception):
                            cost = json.loads(line).get("totalCostUSD")
            test_cost += cost or 0

    # ---- accumulators ----
    sessions = {}                      # sid -> dict
    tool_calls = C(); tool_err = C(); bash_err = C(); bash_ex = collections.defaultdict(list)
    edit_err = C(); edit_ex = collections.defaultdict(list); bash_first = C(); exports = C()
    out_chars = C(); out_n = C(); big_out = []; reads_rep = []; mcp_calls = C(); mcp_err = C()
    out_max = C(); out_big = C()       # per tool: largest result, results over 25K (cost per source)
    hook_att = C(); hook_msgs = C(); pre_blocks = C(); pre_ex = collections.defaultdict(list); gate_notes = C()
    skills_win = C(); cmds_win = C(); agents = C(); agent_model_arg = C()
    band_tok = C(); band_turns = C(); compacts = C(); api_err = C(); interrupts = 0
    corrections = []; toolsearch = []; turn_ms = []; ss_sizes = []; cwd_seen = C()
    model_tok = C(); heredoc_used = 0; secrets_in_cmds = 0; secret_where = set(); empty_sessions = 0
    twin_fork = 0; stop_blocks = 0; stop_followed = 0; stop_unfollowed = []
    time_asks = 0; voice_corr = 0; no_such_tool = 0

    for f in main_files:
        try:
            if os.path.getmtime(f) < since_ms:
                continue
        except OSError:
            continue
        sid = os.path.basename(f)[:-6]
        s = None
        id2 = {}; seen_msg = set(); reads = C(); ts_n = 0; cost = None; cost_models = {}
        stop_pm = []; pm_edits = []        # Stop blocks "PROJECT.md was NOT updated"; Edit/Write of a PROJECT.md
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
                if ts is None or ts < since or ts >= end:
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
                        # How the session started (startup, resume, clear, compact, fork): a /clear or
                        # /compact session keeps the process, MCP servers and settings env it came from.
                        if ev == "SessionStart" and "source" not in s:
                            s["source"] = str(at.get("hookName", "")).partition(":")[2] or "?"
                        if typ in ("hook_blocking_error", "hook_error", "hook_non_blocking_error"):
                            be = at.get("blockingError")
                            msg = str(be.get("blockingError") if isinstance(be, dict) else (be or at.get("stderr") or ""))
                            # The message often starts with '[<hook command>]: '; name the script from it.
                            pm = re.match(r"\[(.*?)\]: (.*)", msg, re.S)
                            script = hook_script(at.get("command") or (pm.group(1) if pm else "")) or (ev.lower() + "-hook")
                            first = (pm.group(2) if pm else msg).strip().split("\n")[0]
                            hook_msgs[(ev, script, one_line(first, 110))] += 1
                            if ev == "Stop" and typ == "hook_blocking_error" and STOP_PROJECT_MD in msg:
                                stop_pm.append(ts)   # ledger CI-3: is each block followed by a reconcile?
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
                            for var in EXPORT_AT_COMMAND.findall(cmd):
                                exports[var] += 1
                        if nm in ("Edit", "Write", "MultiEdit") and \
                                re.split(r"[\\/]", str(inp.get("file_path") or ""))[-1].upper() == "PROJECT.MD":
                            pm_edits.append(ts)
                elif t == "user":
                    m = o.get("message") or {}
                    c = m.get("content")
                    if isinstance(c, str):
                        if "[Request interrupted" in c:
                            interrupts += 1
                        cm = re.findall(r"<command-name>/?([^<\s]+)</command-name>", c)
                        if cm:
                            cmds_win[cm[0]] += 1
                        elif not c.startswith("<") and len(c) < 2000 and not o.get("isMeta"):
                            time_asks += bool(TIME_ASK.search(c))
                            item = (s["project"] + " " + sid[:8], ts.strftime("%m-%d %H:%M"), one_line(c, 260))
                            if CORRECTION.search(c) and item not in corrections:
                                corrections.append(item)
                                voice_corr += bool(VOICE.search(c))
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
                        out_chars[nm] += len(txt); out_n[nm] += 1; out_max[nm] = max(out_max[nm], len(txt))
                        if len(txt) > 25000:
                            out_big[nm] += 1
                            big_out.append((len(txt), nm, s["project"], one_line(json.dumps(inp)[:200], 110)))
                        if not b.get("is_error"):
                            continue
                        tool_err[nm] += 1
                        no_such_tool += NO_SUCH_TOOL in txt
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
                                    if k == "windows_twin" and s.get("source") == "fork":
                                        twin_fork += 1   # owner 2026-10-09: forks are watched, not hooked
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
            for bt in stop_pm:
                stop_blocks += 1
                if any(e > bt for e in pm_edits):
                    stop_followed += 1
                elif len(stop_unfollowed) < a.examples + 3:
                    stop_unfollowed.append(f"{s['project']} {sid[:8]} {bt:%m-%d %H:%M}")
            for fp, n in reads.items():
                if n >= 3:
                    reads_rep.append((n, s["project"], os.path.basename(fp)))
            cwd_seen[s.get("cwd", "")] += 1
            toolsearch.append(ts_n)

    # ---- subagent files: which model and effort actually ran, minutes and output tokens per run ----
    sub_models = C(); sub_n = 0; sub_effort = C(); sub_type_effort = C()
    sub_min = collections.defaultdict(list); sub_out = collections.defaultdict(list)
    for f in sub_files:
        try:
            if os.path.getmtime(f) < since_ms:
                continue
        except OSError:
            continue
        mdl = eff = t0 = t1 = None; out_tok = {}
        with open(f, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if '"type":"assistant"' not in line:
                    continue
                try:
                    o = json.loads(line)
                except Exception:
                    continue
                ts = parse_ts(o.get("timestamp") or "")
                if not ts or ts < since or ts >= end:
                    continue
                msg = o.get("message") or {}
                mdl = mdl or msg.get("model"); eff = eff or o.get("effort")
                t0 = t0 or ts; t1 = ts
                out_tok[msg.get("id")] = (msg.get("usage") or {}).get("output_tokens") or 0   # repeated per block
        if not mdl:
            continue
        sub_models[mdl] += 1; sub_n += 1; eff = eff or "(none)"
        try:
            with open(f[:-len(".jsonl")] + ".meta.json", encoding="utf-8") as fh:
                typ = json.load(fh).get("agentType") or "?"
        except Exception:
            typ = "?"
        sub_effort[eff] += 1; sub_type_effort[(typ, eff)] += 1
        sub_min[eff].append((t1 - t0).total_seconds() / 60); sub_out[eff].append(sum(out_tok.values()))

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
        days = max((end - since).total_seconds() / 86400, 1e-9)   # per_week() reads this at call time
    tot_tok = sum(band_tok.values()) or 1
    share = lambda keys: round(100 * sum(band_tok[k] for k in keys) / tot_tok, 1)
    spend = sum(x["cost"] or 0 for x in S)
    over300 = [x for x in S if x["max_ctx"] > 300e3]
    over200 = [x for x in S if x["max_ctx"] > 200e3]
    bash_calls = tool_calls["Bash"] + tool_calls["PowerShell"]
    starts = C(x.get("source", "?") for x in S)
    counts = C()                       # raw count behind every .per_week key, for the ledger's Since Done: tallies

    def rate(key, n):
        """Set a .per_week metric (summed when the key repeats) and keep its raw count as <key>.count."""
        metrics[key] = round(metrics[key] + per_week(n), 2) if key in metrics else per_week(n)
        counts[key[:-len(".per_week")] + ".count"] += n

    metrics = {
        "window.days": round(days, 1), "window.since": since.strftime("%Y-%m-%d"),
        "window.start": since.strftime("%Y-%m-%d %H:%M"), "window.end": end.strftime("%Y-%m-%d %H:%M"),
        "sessions": len(S), "sessions.startup": starts["startup"],
        "spend.usd": round(spend, 2), "spend.usd.per_week": per_week(spend),
        "spend.over300k_sessions.pct": round(100 * sum(x["cost"] or 0 for x in over300) / spend, 1) if spend else 0,
        "ctx.tokens.m": round(tot_tok / 1e6, 1),
        "ctx.share_above_200k.pct": share(["200_300k", "300_500k", "gt500k"]),
        "ctx.share_above_300k.pct": share(["300_500k", "gt500k"]),
        "sessions.empty_skipped": empty_sessions,
        "sessions.test_runs_left_out": test_n,
        "hook.stop.project_md.blocks": stop_blocks, "hook.stop.project_md.reconciled": stop_followed,
    }
    for key, n in (("sessions.per_week", len(S)),
                   ("ctx.sessions_over_300k.per_week", len(over300)), ("ctx.sessions_over_200k.per_week", len(over200)),
                   ("bash.heredoc_used.per_week", heredoc_used), ("bash.err.windows_twin.fork.per_week", twin_fork),
                   ("secrets.in_commands.per_week", secrets_in_cmds),
                   ("compactions.per_week", sum(compacts.values())), ("bash.calls.per_week", bash_calls),
                   ("bash.errors.per_week", tool_err["Bash"] + tool_err["PowerShell"]), ("interrupts.per_week", interrupts),
                   ("subagents.per_week", sub_n), ("toolsearch.per_week", sum(toolsearch)),
                   ("big_outputs_25k.per_week", len(big_out)), ("repeated_reads.per_week", len(reads_rep)),
                   ("owner.time_asks.per_week", time_asks), ("owner.corrections.per_week", len(corrections)),
                   ("owner.corrections.voice.per_week", voice_corr), ("tool.err.no_such_tool.per_week", no_such_tool)):
        rate(key, n)
    for k, v in bash_err.items():
        rate("bash.err." + k + ".per_week", v)
    for k, v in edit_err.items():
        rate("edit.err." + k + ".per_week", v)
    for (ev, script, _), v in hook_msgs.items():
        rate("hook.block." + ev + "." + script + ".per_week", v)
    for (tool, script), v in pre_blocks.items():
        rate("hook.block.PreToolUse." + script + ".per_week", v)
    for (ev, script), v in gate_notes.items():
        rate("hook.context." + ev + "." + script + ".per_week", v)
    for k, v in exports.items():
        rate("bash.export." + k + ".per_week", v)
    for k, v in skills_win.items():                  # plugin:name and name count as one skill
        rate("skill.calls." + k.split(":")[-1] + ".per_week", v)
    for k, v in sub_effort.items():                  # helper effort tiers (ledger CI-23)
        rate("subagents.effort." + k + ".per_week", v)
        metrics["subagents.median_minutes." + k] = round(statistics.median(sub_min[k]), 1)
        metrics["subagents.median_output_tokens." + k] = int(statistics.median(sub_out[k]))
    all_min = [x for v in sub_min.values() for x in v]; all_out = [x for v in sub_out.values() for x in v]
    metrics["subagents.median_minutes"] = round(statistics.median(all_min), 1) if all_min else 0
    metrics["subagents.median_output_tokens"] = int(statistics.median(all_out)) if all_out else 0
    src_chars = C(); src_n = C(); src_max = C(); src_big = C()   # cost per source: each MCP server, Bash, Read
    for nm, v in out_chars.items():
        if nm.startswith("mcp__") or nm in ("Bash", "Read"):
            src = nm.split("__")[1] if nm.startswith("mcp__") else nm
            src_chars[src] += v; src_n[src] += out_n[nm]; src_big[src] += out_big[nm]
            src_max[src] = max(src_max[src], out_max[nm])
    for src, v in src_chars.items():
        rate("tool.out." + src + ".calls.per_week", src_n[src])
        rate("tool.out." + src + ".chars.per_week", v)
        metrics["tool.out." + src + ".avg"] = v // max(1, src_n[src])
        metrics["tool.out." + src + ".max"] = src_max[src]
        rate("tool.out." + src + ".over_25k.per_week", src_big[src])

    # ---- local add-ons (scripts/*.private.py, see private_sections) ----
    addon_lines, addon_metrics = private_sections(a.private_dir, {
        "projects_dir": a.projects_dir, "since": since, "now": end, "days": days, "examples": a.examples})
    metrics.update(addon_metrics)

    # ---- report ----
    L = []
    P = L.append
    P("# Claude Code usage scan")
    P("")
    P(f"Window: {since:%Y-%m-%d %H:%M} to {end:%Y-%m-%d %H:%M} UTC ({days:.1f} days). Sessions: {len(S)} "
      f"(+{empty_sessions} with no assistant turn skipped); subagent runs: {sub_n}. "
      + (f"Left out: {test_n} test-run session files (${test_cost:,.2f}; eval and temp-folder runs, "
         "`--include-test-runs` keeps them). " if test_n else "") +
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
    P(f"- Sessions by start source: " + ", ".join(f"{k} {v}" for k, v in starts.most_common())
      + f"; Windows-twin failures in forked sessions: {twin_fork}")
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
    P(f"- Stop blocks \"{STOP_PROJECT_MD}\": {stop_blocks}, followed by an Edit/Write of a PROJECT.md later in the "
      f"same session: {stop_followed}" + (" (not followed: " + "; ".join(stop_unfollowed) + ")" if stop_unfollowed else ""))
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
    P("- Subagent runs by effort (runs, median minutes, median output tokens per run): " + (", ".join(
        f"{k} {v} ({statistics.median(sub_min[k]):.1f} min, {int(statistics.median(sub_out[k])):,} tok)"
        for k, v in sub_effort.most_common()) or "none"))
    P("- Subagent runs by type/effort: " + (", ".join(f"{t}/{e} {v}" for (t, e), v in sub_type_effort.most_common(10)) or "none"))
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
    P("- Cost per source, main session only (helper output is not counted): calls / chars total / avg / largest / over 25K")
    for src, v in src_chars.most_common():
        P(f"  - {src}: {src_n[src]} / {v//1000}K / {v//max(1, src_n[src])} / {src_max[src]//1000}K / {src_big[src]}")
    P(f"- Same file Read 3+ times in one session: {len(reads_rep)}"
      + (" - top: " + ", ".join(f"{f} x{n} ({p})" for n, p, f in sorted(reads_rep, reverse=True)[:6]) if reads_rep else ""))
    P("")
    P("## 6. Owner friction")
    P(f"- Interrupts: {interrupts}. API/system errors: {dict(api_err) or 0}. Owner asks about the time left: "
      f"{time_asks}. Calls to a tool that does not exist: {no_such_tool}")
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
    L.extend(addon_lines)
    P("")
    P("## 7. Metrics (per 7 days unless named otherwise)")
    P("Raw counts: the `--json` file also holds `<key>.count` for every `.per_week` key below (the window's own "
      "count, for the ledger's `Since Done:` tallies).")
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
            json.dump({**metrics, **counts}, fh, indent=1, sort_keys=True)
    print(f"scan: {len(S)} sessions, {days:.1f} days, report {len(report)//1024} KB"
          + (f" -> {a.out}" if a.out else ""), file=sys.stderr)


if __name__ == "__main__":
    main()
