"""Read-only data pass for Claude Code's /doctor checks, run by claude-improve Step 1b in EVERY run (owner,
2026-10-09: /doctor and /insights are part of the review, without a full pass over periods already audited). Prints
counts and names only: never env/header values, never whole settings files, hook commands reduced to script basenames.
Usage: doctor_data.py <out.md> [project dir] [since "YYYY-MM-DD HH:MM" UTC = the ledger's Last run] [--no-save] [--seed]
No double work, two ways. (1) The transcript part reads only lines after <since>: sessions before it were audited by
the previous review. (2) The config part (settings, agents, skills, plugins, MCP, hooks) is compared with a baseline
kept in ~/.claude/claude-improve-doctor-state.json (a regenerable cache; missing = a full first pass): <out.md> lists
only what moved, plus standing lines; the full dump goes to <out>.full.md. The baseline is keyed by <since>: the same
<since> is the same review, so a retry compares with the same baseline again and never hides what moved; a later
<since> is a new review, and the previous review's last pass becomes its baseline. --no-save writes nothing; --seed
makes this pass the baseline for <since> (first install, after a restore). A usage counter is listed when its
extension was at 2 uses or fewer (the unused ones a verdict is about); counters of extensions already in use are only
counted."""
import calendar, glob, json, os, re, sys, time, collections, statistics

ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
NO_SAVE = "--no-save" in sys.argv
SEED = "--seed" in sys.argv
HOME = os.path.expanduser("~")
CL = os.path.join(HOME, ".claude")
PROJ = (ARGS[1] if len(ARGS) > 1 else os.getcwd()).replace("\\", "/")
SINCE = ARGS[2] if len(ARGS) > 2 else time.strftime("%Y-%m-%d %H:%M", time.gmtime(time.time() - 14 * 86400))
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
P(f"- installMethod={cj.get('installMethod')!r} autoUpdates={cj.get('autoUpdates')!r}")
P(f"- numStartups={cj.get('numStartups')} (not compared)")
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
unused_plugins = []
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
    if enabled and nsk and not u.get("usageCount"):
        unused_plugins.append(f"{key} ({chars} chars)")
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

# ---- compare the config part with the previous pass (no double work)
STATE = os.path.join(CL, "claude-improve-doctor-state.json")
DIFFABLE = ("check 0", "plugins", "mcp config", "skillUsage (lifetime)", "hooks config (user)")
PROBLEM = re.compile(r"PARSE ERROR|COLLISION|NO description|YAML error|unreadable|no frontmatter|unterminated|SUSPICIOUS")
LOW_USE = 2

def split_sections(lines):
    secs, name = collections.OrderedDict(), None
    for ln in lines:
        if ln.startswith("## "):
            name = ln[3:]
            secs[name] = []
        elif name is not None:
            secs[name].append(ln)
    return secs

def parts(line):
    """(key, struct, counter): a usage counter is compared apart from the rest of its line."""
    s = line.strip()
    m = re.search(r"usage_total=(\d+)", s) or re.search(r": (\d+) last ", s)
    counter = int(m.group(1)) if m else None
    struct = re.sub(r"usage_total=\d+", "usage_total=#", s)
    struct = re.sub(r": \d+ last .*$", ": # last ...", struct)
    struct = re.sub(r"last=\S*", "last=...", struct)
    key = struct.split(": ", 1)[0] if ": " in struct else struct
    return key, struct, counter

def keyed(lines):
    d = {}
    for ln in lines:
        if "(not compared)" in ln:
            continue
        key, struct, counter = parts(ln)
        n = 1
        while key in d:
            n += 1
            key = f"{key}#{n}"
        d[key] = (struct, counter, ln.strip())
    return d

secs = split_sections(out)
cur = {n: secs.get(n, []) for n in DIFFABLE}
try:
    with open(STATE, encoding="utf-8") as fh:
        st = json.load(fh)
except Exception:
    st = {}
if st.get("since") == SINCE:            # the same review again (a retry): the same baseline
    prev, saved_at = st.get("baseline"), st.get("baseline_saved")
elif st:                                # a later review: the previous review's last pass is the baseline
    prev, saved_at = st.get("latest"), st.get("saved")
else:
    prev, saved_at = None, None

problems = [ln.strip() for n in DIFFABLE for ln in cur[n] if PROBLEM.search(ln)]
short = []
S = short.append
S("## problems (standing; each needs a verdict only if the ledger does not hold it)")
S("\n".join(f"- {p}" for p in problems) if problems else "- none")
S("- enabled plugins with 0 uses (standing; a verdict is needed only if the ledger holds none): "
  + (", ".join(unused_plugins) if unused_plugins else "none"))
if prev is None:
    S("## changed since the last doctor pass")
    S("- no baseline yet: first pass, so the whole config part is new (full dump below)")
    for n in DIFFABLE:
        S(f"### {n}")
        short.extend(cur[n])
else:
    changes, same, quiet = [], 0, 0
    for n in DIFFABLE:
        old, new = keyed(prev.get(n, [])), keyed(cur[n])
        for k, (struct, counter, line) in new.items():
            if k not in old:
                changes.append(f"+ [{n}] {line}")
            elif old[k][0] != struct:
                changes.append(f"~ [{n}] {old[k][2]}  ->  {line}")
            elif old[k][1] != counter:
                if (old[k][1] or 0) <= LOW_USE:
                    changes.append(f"~ [{n}] {old[k][2]}  ->  {line}")
                else:
                    quiet += 1
            else:
                same += 1
        for k, (struct, counter, line) in old.items():
            if k not in new:
                changes.append(f"- [{n}] {line}")
    S(f"## changed since the last doctor pass (saved {saved_at})")
    S("\n".join(changes) if changes else "- nothing moved")
    S(f"- {same} config lines identical; {quiet} usage counters of extensions already in use moved up (not listed)")
for n, lines in secs.items():
    if n.startswith("transcripts since"):
        short.append("## " + n)
        short.extend(lines)

full = "\n".join(out)
text = "\n".join(short)
dst = ARGS[0] if ARGS else "doctor-data.md"
open(os.path.splitext(dst)[0] + ".full.md", "w", encoding="utf-8").write(full)
open(dst, "w", encoding="utf-8").write(text)
print(text)
if not NO_SAVE:
    now = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())
    new_state = {"since": SINCE, "baseline": prev, "baseline_saved": saved_at, "latest": cur, "saved": now}
    if SEED:
        new_state.update(baseline=cur, baseline_saved=now)
    try:
        with open(STATE, "w", encoding="utf-8") as fh:
            json.dump(new_state, fh, indent=1)
    except Exception as e:
        print(f"(baseline not saved: {type(e).__name__})")
