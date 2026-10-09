"""Read-only data pass for Claude Code's /doctor checks, used by claude-improve Step 1b ONLY when the owner typed
/doctor himself (the built-in is reserved for him). Prints counts and names only: never env/header values, never
whole settings files, hook commands reduced to script basenames.
Usage: doctor_data.py <out.md> [project dir] [since "YYYY-MM-DD HH:MM" UTC = the ledger's Last run]
The transcript part reads only lines after <since>: sessions before it were audited by the previous review (owner,
2026-10-09: "I don't want double work"). Config checks and the lifetime usage counters need no transcripts."""
import calendar, glob, json, os, re, sys, time, collections, statistics

HOME = os.path.expanduser("~")
CL = os.path.join(HOME, ".claude")
PROJ = (sys.argv[2] if len(sys.argv) > 2 else os.getcwd()).replace("\\", "/")
SINCE = sys.argv[3] if len(sys.argv) > 3 else time.strftime("%Y-%m-%d %H:%M", time.gmtime(time.time() - 14 * 86400))
since = calendar.timegm(time.strptime(SINCE, "%Y-%m-%d %H:%M"))
SINCE_ISO = SINCE.replace(" ", "T")
DAYS = round((time.time() - since) / 86400, 1)
out = []
P = out.append

def load(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f), None
    except FileNotFoundError:
        return None, "missing"
    except Exception as e:
        return None, f"PARSE ERROR {type(e).__name__} {getattr(e, 'lineno', '')}:{getattr(e, 'colno', '')}"

def base(cmd):
    m = re.findall(r"[\w.-]+\.(?:js|py|sh|ps1|mjs|cjs)", cmd or "")
    return m[-1] if m else (cmd or "?").split()[0][:40]

# ---- check 0: parse + installs
P("## check 0")
files = {"user settings": f"{CL}/settings.json", "user settings.local": f"{CL}/settings.local.json",
         "~/.claude.json": f"{HOME}/.claude.json", "project settings": f"{PROJ}/.claude/settings.json",
         "project settings.local": f"{PROJ}/.claude/settings.local.json", "project .mcp.json": f"{PROJ}/.mcp.json"}
data = {}
for k, p in files.items():
    d, err = load(p)
    data[k] = d
    P(f"- {k}: {err or 'OK'}")
cj = data["~/.claude.json"] or {}
P(f"- installMethod={cj.get('installMethod')!r} autoUpdates={cj.get('autoUpdates')!r} numStartups={cj.get('numStartups')}")
for p in [f"{HOME}/.local/bin/claude", f"{HOME}/.local/bin/claude.exe", f"{CL}/local"]:
    P(f"- exists {p.replace(HOME, '~')}: {os.path.exists(p)}")
us = data["user settings"] or {}
perm = us.get("permissions", {})
P(f"- user permissions.defaultMode={perm.get('defaultMode')!r} disableAutoMode={perm.get('disableAutoMode')!r}; "
  f"autoUpdatesChannel={us.get('autoUpdatesChannel')!r}; env keys present: DISABLE_AUTOUPDATER={'DISABLE_AUTOUPDATER' in (us.get('env') or {})}")
for k in ("project settings", "project settings.local"):
    d = data[k] or {}
    P(f"- {k}: defaultMode={d.get('permissions', {}).get('defaultMode')!r}, allow rules={len(d.get('permissions', {}).get('allow', []))}")

def frontmatter(path):
    try:
        t = open(path, encoding="utf-8").read()
    except Exception as e:
        return None, f"unreadable {type(e).__name__}"
    if not t.startswith("---"):
        return None, "no frontmatter"
    end = t.find("\n---", 3)
    if end < 0:
        return None, "unterminated frontmatter"
    block = t[3:end]
    try:
        import yaml
        fm = yaml.safe_load(block)
        if not isinstance(fm, dict):
            return None, "frontmatter not a mapping"
        return fm, None
    except Exception as e:
        return None, f"YAML error {type(e).__name__}: {str(e).splitlines()[0][:100]}"

P("- agents:")
names = collections.defaultdict(list)
for p in glob.glob(f"{CL}/agents/*.md") + glob.glob(f"{PROJ}/.claude/agents/**/*.md", recursive=True):
    fm, err = frontmatter(p)
    if err:
        P(f"  - {os.path.basename(p)}: {err}")
        continue
    if "name" not in fm:
        continue
    names[(os.path.dirname(p), fm["name"])].append(os.path.basename(p))
    if not fm.get("description"):
        P(f"  - {os.path.basename(p)}: name but NO description (never loads)")
for (d, n), fs in names.items():
    if len(fs) > 1:
        P(f"  - COLLISION name {n!r}: {fs}")
P(f"  - agent definitions with a name: {sum(len(v) for v in names.values())}")

P("- skills (user):")
skill_desc = {}
for p in sorted(glob.glob(f"{CL}/skills/*/SKILL.md")):
    d = os.path.basename(os.path.dirname(p))
    fm, err = frontmatter(p)
    if err:
        P(f"  - {d}: {err}")
        continue
    skill_desc[fm.get("name", d)] = len(str(fm.get("name", d))) + len(str(fm.get("description", "")))
P(f"  - user skills parsed OK: {len(skill_desc)}; listing chars {sum(skill_desc.values())} (est. {sum(skill_desc.values())//4} tok)")
for n, c in sorted(skill_desc.items(), key=lambda x: -x[1])[:6]:
    P(f"    - {n}: {c} chars")

# ---- plugins
P("## plugins")
ep = us.get("enabledPlugins") or {}
inst, _ = load(f"{CL}/plugins/installed_plugins.json")
inst_keys = list((inst or {}).get("plugins", {}).keys()) if isinstance(inst, dict) else []
pu = cj.get("pluginUsage") or {}
plug_listing = {}
for key in sorted(set(inst_keys) | set(ep.keys())):
    if not re.fullmatch(r"[\w.@:-]+", key):
        P(f"- SUSPICIOUS key skipped"); continue
    enabled = ep.get(key)
    name, _, mkt = key.partition("@")
    vers = (inst or {}).get("plugins", {}).get(key) or []
    ipath = vers[0].get("installPath") if vers and isinstance(vers, list) and isinstance(vers[0], dict) else None
    chars = 0; nsk = 0
    if ipath and os.path.isdir(ipath):
        for sp in glob.glob(os.path.join(ipath, "skills", "*", "SKILL.md")) + glob.glob(os.path.join(ipath, "commands", "*.md")):
            fm, err = frontmatter(sp)
            nsk += 1
            if fm:
                chars += len(str(fm.get("name", ""))) + len(str(fm.get("description", "")))
    u = pu.get(key) or {}
    plug_listing[key] = chars if enabled else 0
    P(f"- {key}: enabled={enabled} items={nsk} listing_chars={chars} usage_total={u.get('usageCount', 0)} last={str(u.get('lastUsedAt', ''))[:10]}")

# ---- MCP config
P("## mcp config")
P(f"- user mcpServers: {sorted((cj.get('mcpServers') or {}).keys())}")
pe = (cj.get("projects") or {})
for k, v in pe.items():
    if k.replace("\\", "/").lower() == PROJ.lower():
        P(f"- project-local mcpServers: {sorted((v.get('mcpServers') or {}).keys())}; disabledMcpServers: {v.get('disabledMcpServers')}")
P(f"- alwaysLoad servers: {[k for k, v in (cj.get('mcpServers') or {}).items() if isinstance(v, dict) and v.get('alwaysLoad')]}")

# ---- skill usage counters
P("## skillUsage (lifetime)")
su = cj.get("skillUsage") or {}
for k, v in sorted(su.items(), key=lambda x: -(x[1] or {}).get("usageCount", 0)):
    lu = (v or {}).get("lastUsedAt")
    lus = time.strftime("%Y-%m-%d", time.gmtime(lu / 1000)) if isinstance(lu, (int, float)) else str(lu)[:10]
    P(f"- {k}: {(v or {}).get('usageCount')} last {lus}")

# ---- hooks config
P("## hooks config (user)")
for ev, entries in (us.get("hooks") or {}).items():
    for e in entries:
        for h in e.get("hooks", []):
            P(f"- {ev} [{e.get('matcher', '')}] {base(h.get('command'))} timeout={h.get('timeout')} async={h.get('async')}")

# ---- transcripts (real sessions, last DAYS)
P(f"## transcripts since {SINCE} UTC ({DAYS} days)")
def test_run(dirname, cwd):
    c = (cwd or "").replace("\\", "/").lower()
    return "-workspace" in dirname or "/appdata/local/temp" in c or "scratchpad" in c
hook_d = collections.defaultdict(list); hook_cancel = collections.Counter(); hook_err = collections.Counter()
mcp_calls = collections.Counter(); skill_calls = collections.Counter(); slash = collections.Counter()
denials = collections.Counter(); denial_kind = collections.defaultdict(collections.Counter)
nsess = 0; nleft = 0; days_seen = set()
for f in glob.glob(f"{CL}/projects/*/*.jsonl"):
    if os.path.getmtime(f) < since:
        continue
    dirname = os.path.basename(os.path.dirname(f))
    tool_by_id = {}; cwd = None; lines = []
    try:
        fh = open(f, encoding="utf-8", errors="replace")
    except Exception:
        continue
    with fh:
        for line in fh:
            if cwd is None and '"cwd"' in line:
                m = re.search(r'"cwd":"([^"]*)"', line)
                if m: cwd = m.group(1)
            if not any(s in line for s in ('"tool_use"', 'durationMs', 'toolDenialKind', 'command-name')):
                continue
            lines.append(line)
    if test_run(dirname, cwd):
        nleft += 1; continue
    nsess += 1
    for line in lines:
        try:
            o = json.loads(line)
        except Exception:
            continue
        if (o.get("timestamp") or "") < SINCE_ISO:
            continue          # audited by the previous review
        ts = o.get("timestamp", "")[:10]
        if ts: days_seen.add(ts)
        if o.get("type") == "assistant":
            for c in (o.get("message") or {}).get("content") or []:
                if isinstance(c, dict) and c.get("type") == "tool_use":
                    n = c.get("name", "")
                    tool_by_id[c.get("id")] = (n, (c.get("input") or {}).get("command", "") if n == "Bash" else "")
                    if n.startswith("mcp__"):
                        mcp_calls[n.split("__")[1]] += 1
                    if n == "Skill":
                        skill_calls[str((c.get("input") or {}).get("skill"))] += 1
        elif o.get("type") == "attachment":
            a = o.get("attachment") or {}
            t = a.get("type", "")
            if t.startswith("hook") and a.get("durationMs") is not None:
                key = (a.get("hookEvent") or str(a.get("hookName", "")).split(":")[0], base(a.get("command")))
                hook_d[key].append(a.get("durationMs") or 0)
                if t == "hook_cancelled" and a.get("timedOut"):
                    hook_cancel[key] += 1
                if t in ("hook_non_blocking_error", "hook_error_during_execution"):
                    hook_err[key] += 1
        elif o.get("type") == "user":
            k = o.get("toolDenialKind")
            if k and k not in ("interrupted", "cancelled"):
                for c in ((o.get("message") or {}).get("content") or []):
                    if isinstance(c, dict) and c.get("type") == "tool_result":
                        n, cmd = tool_by_id.get(c.get("tool_use_id"), ("?", ""))
                        if n == "Bash":
                            w = cmd.strip().split()
                            n = "Bash(" + " ".join(w[:2])[:40] + ")"
                        denials[n] += 1; denial_kind[n][k] += 1
            msg = (o.get("message") or {}).get("content")
            s = msg if isinstance(msg, str) else json.dumps(msg)[:2000]
            for m in re.findall(r"<command-name>/([\w:-]+)</command-name>", s or ""):
                slash[m] += 1
P(f"- real sessions {nsess}, test-run files left out {nleft}, days with activity {len(days_seen)}")
P("- hook durations ms (event, script: runs, median, p90, max, timeouts, errors):")
for key, v in sorted(hook_d.items(), key=lambda x: -statistics.median(x[1])):
    v2 = sorted(v)
    P(f"  - {key[0]} {key[1]}: n={len(v)} med={int(statistics.median(v2))} p90={int(v2[int(len(v2)*0.9)-1 if len(v2) > 1 else 0])} max={int(v2[-1])} to={hook_cancel[key]} err={hook_err[key]}")
P(f"- MCP calls by server: {dict(mcp_calls.most_common())}")
P(f"- Skill tool calls: {dict(skill_calls.most_common())}")
P(f"- slash commands: {dict(slash.most_common(25))}")
P(f"- denials (excl. interrupted/cancelled): {sum(denials.values())}")
for n, c in denials.most_common(15):
    P(f"  - {n}: {c} {dict(denial_kind[n])}")
P(f"- plugin listing chars enabled total {sum(plug_listing.values())} (est. {sum(plug_listing.values())//4} tok)")

text = "\n".join(out)
dst = sys.argv[1] if len(sys.argv) > 1 else "doctor-data.md"
open(dst, "w", encoding="utf-8").write(text)
print(text)
