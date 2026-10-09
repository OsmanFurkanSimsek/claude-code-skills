#!/usr/bin/env python3
"""quick_ledger.py - what the quick path (Last run: under 24 hours old) needs from the ledger, in a few KB.

Prints Last run, the last Runs row, each open item (ID, title, Status, Done, Verify by, Since Done) and every
"Checked, no action" point as one line, so the model never reads the whole ledger on the quick path (an item's Fix
line too, when only a restart decides whether its tally is too early). Closed items are counted, and each one's
`Signal:` line is printed (ID, status, Signal; one line each) so a candidate is matched without grepping the ledger.
With --scan-json (this window's scan.json from scan.py) it also brings every `Since Done:` tally up to the
window's end: sessions and startup sessions summed, and the count summed when the item's Signal or Verify by
names a scan key (`<key>.per_week` -> `<key>.count`); a count no scan key holds is marked for reading in context.
An item whose Done falls inside the window needs the one `scan.py --since <Done> --until <window end>` that starts
its tally: --start-tallies runs those scans (in parallel) and prints each start; without it, the command is printed.
An older item with no tally gets the command to run once.
Each done item also gets a `Hint:` line, a suggested verdict with its reason: too early (under 10 sessions, a judge
date ahead, or a restart fix with under 10 fresh starts), or, when Verify by names one scan key with a numeric
target, verified / on track / not working from the summed count; "stays done, not judged yet" when the key meets its
target but every other Verify by condition needs a skill that ran 0 times; "needs reading" where no rule decides. A
skill the item names gets its call count from scan.json (0 when unused), and one line says the window-edge overlap is
known.

Usage:
  python quick_ledger.py --ledger <ledger.md> [--scan-json <scratchpad>/scan.json [--start-tallies <scratchpad>]]
Standard library only. Read-only: it prints to stdout; only --start-tallies writes, its since-<ID>.md/.json files.
"""
import argparse, datetime as dt, json, os, re, subprocess, sys

KEY = re.compile(r"\b([a-z][a-z0-9_]*(?:\.[A-Za-z0-9_-]+)+)\.per_week\b")
TALLY = re.compile(r"^(\d+) sessions \((\d+) startup\),\s*(.*?),\s*through (\d{4}-\d{2}-\d{2} \d{2}:\d{2})(?: UTC)?\s*$")
ACTIVE = ("done", "not working", "later")       # statuses whose fix is still watched (ledger-format.md)
EARLY = 10                                       # fewer sessions after Done -> "too early" (SKILL.md Step 2)
CANDIDATE = ("owner.corrections",)               # scan keys that count candidates (scan.py CORRECTION), not findings


def parse(text):
    """Split the ledger into its header facts, open items, checked rows and a closed-items summary."""
    out = {"last_run": None, "last_row": None, "items": [], "checked": [], "closed": {}, "signals": []}
    m = re.search(r"^Last run:\s*(.+?)\s*$", text, re.M)
    out["last_run"] = m.group(1) if m else None
    sec = {}
    for m in re.finditer(r"^## (.+?)\s*$", text, re.M):
        sec[m.group(1).strip().lower()] = m.start()
    bounds = sorted(sec.values()) + [len(text)]

    def body(name):
        s = sec.get(name)
        return "" if s is None else text[s:min(b for b in bounds if b > s)]

    rows = [l for l in body("runs").splitlines() if l.startswith("|") and not re.match(r"^\|\s*(Date|-)", l)]
    out["last_row"] = rows[-1] if rows else None
    for blk in re.split(r"^### ", body("open items"), flags=re.M)[1:]:
        lines = blk.splitlines()
        it = {"head": lines[0].strip()}
        for l in lines[1:]:
            m = re.match(r"^- ([A-Za-z ]+?):\s*(.*)$", l)
            if m:
                it[m.group(1).strip().lower()] = m.group(2).strip()
        st = it.get("status", "")
        it["state"] = st.split("|")[0].strip()
        m = re.search(r"Done:\s*(\d{4}-\d{2}-\d{2})(?:[ T](\d{2}:\d{2}))?", st)
        it["done"] = (m.group(1) + " " + (m.group(2) or "00:00")) if m else None
        out["items"].append(it)
    for l in body("checked, no action").splitlines():
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if l.startswith("|") and len(cells) >= 3 and cells[0] not in ("Checked",) and not set(cells[0]) <= set("-"):
            out["checked"].append(f"{cells[0]} {cells[1]}: {cells[2]}")
    for st in re.findall(r"^- Status:\s*([a-z ]+?)\s*(?:\||$)", body("closed items"), re.M):
        out["closed"][st] = out["closed"].get(st, 0) + 1
    for blk in re.split(r"^### ", body("closed items"), flags=re.M)[1:]:
        m = re.search(r"^- Signal:\s*(.*?)\s*$", blk, re.M)
        st = re.search(r"^- Status:\s*([a-z ]+?)\s*(?:\||$)", blk, re.M)
        out["signals"].append(f"{blk.split()[0]} ({st.group(1) if st else '?'}): "
                              f"{m.group(1) if m else '(no Signal line)'}")
    return out


def ts(s):
    return dt.datetime.strptime(s[:16], "%Y-%m-%d %H:%M")


# A fix needs a restart only when its Fix line names a settings env value, an MCP server, the shell profile, or the
# enabled plugins: those load once, when the process starts. Skill, rule, hook-script and memory edits do not.
RESTART_FIX = re.compile(r"settings env|\benv block|`env`|\bMCP server|mcpServers|\.mcp\.json|\.bashrc|\.bash_profile|"
                         r"\.zshrc|(?<![\w-])\.profile\b|shell profile|enabledPlugins", re.I)
RESTART = " -> under 10 startup and the fix needs a restart (its Fix line names {}): too early"
NO_RESTART = (" -> under 10 startup does not matter: its Fix line names no restart (settings env, MCP server, "
              "shell profile, plugins), so every session counts")


def early(n, startup, note, it=None):
    """Step 2's too-early mark; an item under 10 sessions needs no reading, so its count note is dropped.
    Under 10 startup sessions is too early only when the item's own Fix line names a restart."""
    if n < EARLY:
        return " -> too early (under 10 sessions)" + (": nothing to read" if "no scan key" in note else "")
    if startup >= EARLY:
        return ""
    m = RESTART_FIX.search((it or {}).get("fix", ""))
    return RESTART.format(m.group(0)) if m else NO_RESTART


def with_fix(line, it):
    """When a restart decides the verdict, add the item's Fix line so the named restart can be seen."""
    return [line] + ([f"  Fix: {it['fix']}"] if line.endswith(": too early") and " needs a restart " in line
                     and it.get("fix") else [])


def keys_of(it):
    return sorted(set(KEY.findall(it.get("signal", "") + " " + it.get("verify by", ""))))


def count_part(it, scan):
    """'<n> from <key>.count' when the item names scan keys, else a note that the count is read in context."""
    keys = keys_of(it)
    if not keys:
        return None, "count: no scan key; read the cases in context"
    add = sum(int(scan.get(k + ".count", 0)) for k in keys)
    cand = add and any(k.startswith(CANDIDATE) for k in keys)
    return add, f"{add} from {', '.join(k + '.count' for k in keys)}" + (
        "; candidates: read them in scan.md section 6 before counting" if cand else "")


def start_scans(items, end, outdir, projects_dir=None):
    """Run the one `scan.py --since <Done> --until <end>` per item whose Done is inside the window, in parallel."""
    here = os.path.dirname(os.path.abspath(__file__))
    procs = {}
    for it in items:
        ident = it["head"].split()[0]
        js = os.path.join(outdir, f"since-{ident}.json")
        cmd = [sys.executable, os.path.join(here, "scan.py"), "--since", it["done"], "--until", end,
               "--out", os.path.join(outdir, f"since-{ident}.md"), "--json", js]
        if projects_dir:
            cmd += ["--projects-dir", projects_dir]
        procs[ident] = (subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE), js)
    res = {}
    for ident, (p, js) in procs.items():
        err = p.communicate()[1]
        try:
            res[ident] = json.load(open(js, encoding="utf-8"))
        except (OSError, ValueError):
            res[ident] = {"error": (err or b"").decode("utf-8", "replace").strip()[-300:] or "no output"}
    return res


def tally(it, scan, started=None):
    """The item's Since Done line brought to the window's end, or the scan that starts it."""
    start, end = scan.get("window.start"), scan.get("window.end")
    ident = it["head"].split()[0]
    cmd = f'scan.py --since "{it["done"]}" --until "{end}" --json <scratchpad>/since-{ident}.json'
    if it["done"] and start and ts(it["done"]) >= ts(start):
        if started is None or ident not in started:
            return [f"  Done is inside this window: start the tally with `{cmd}`"]
        s = started[ident]
        if "error" in s:
            return [f"  Done is inside this window; its scan failed ({s['error']}): run `{cmd}`"]
        add, note = count_part(it, s)
        n, st = s.get("sessions.count", s.get("sessions", 0)), s.get("sessions.startup", 0)
        return with_fix(f"  Start (scan since Done, since-{ident}.md): {n} sessions ({st} startup), through {end} "
                        "UTC" + ("" if n < EARLY and add is None else f"; {note}") + early(n, st, note, it), it)
    sd = it.get("since done")
    if not sd:
        if not it["done"]:
            return []                                    # nothing landed yet: no tally to keep
        return [f"  No tally yet: take it from History if it gives counts, else run once `{cmd}`"]
    m = TALLY.match(sd)
    if not m:
        return ["  Since Done line not in the standard form: update it by hand"]
    n, s, what, through = int(m.group(1)), int(m.group(2)), m.group(3), m.group(4)
    if through >= end:
        return [f"  Already through {through}: nothing to add"]
    n2, s2 = n + int(scan.get("sessions.count", scan.get("sessions", 0))), s + int(scan.get("sessions.startup", 0))
    add, note = count_part(it, scan)
    c = re.match(r"^(\d+)(\s.*)$", what)
    if add is not None and c:
        what = f"{int(c.group(1)) + add}{c.group(2)}"
        note = f"+{note}"
    elif add is not None:
        note = f"this window: {note}; the tally's count is not a number, add it by hand"
    else:
        note = "count: no scan key; read this window's cases in context"
    shown = "" if n2 < EARLY and add is None else f" ({note})"
    return with_fix(f"  New: {n2} sessions ({s2} startup), {what}, through {end} UTC{shown}{early(n2, s2, note, it)}", it)


EDGE = ("Window edge: a session that crosses a window edge counts in both windows' session counts, so a summed "
        "tally runs a little high (known and accepted, references/ledger-format.md): nothing to check.")
JUDGE_ON = re.compile(r"[Jj]udge (?:it )?on (\d{4}-\d{2}-\d{2})")
OPS = {"below": "<", "under": "<", "<": "<", "at most": "<=", "<=": "<=", "=": "=", "==": "=",
       "above": ">", "over": ">", ">": ">", "at least": ">=", ">=": ">="}
TARGET = re.compile(r"(?<![\w-])(below|under|at most|above|over|at least|<=|>=|==|=|<|>)\s*(\d+(?:\.\d+)?)(?![\d:-])")
BASELINE = re.compile(r"baseline\s+(\d+(?:\.\d+)?)\s*(?:a week|/week|per week)?\s*(?=[),;]|$)")


def named_skills(text, scan):
    """(name, calls) for each skill named in the text that scan.json counts (scan.py writes 0 for an unused skill)."""
    names = sorted({k[len("skill.calls."):-len(".count")] for k in scan
                    if k.startswith("skill.calls.") and k.endswith(".count")})
    return [(n, int(scan[f"skill.calls.{n}.count"])) for n in names
            if len(n) >= 4 and re.search(r"(?<![\w/-])" + re.escape(n) + r"(?![\w/-])", text)]


def skill_counts(it, scan):
    """'name n' for each skill the item names that scan.json counts."""
    text = " ".join((it["head"], it.get("signal", ""), it.get("verify by", "")))
    return [f"{n} {c}" for n, c in named_skills(text, scan)]


def untested(it, key, counts):
    """The unused skills when every Verify by condition besides the key's names a skill that ran 0 times: such a
    condition cannot be judged yet, so the item stays done. None when any other condition could be judged now."""
    cl = clauses(it.get("verify by", ""))
    own = [c for c in cl if key in c]
    others = [c for c in cl if c not in own] if own else cl[1:]
    idle = []
    for c in others:
        zero = [n for n, k in named_skills(c, counts) if k == 0]
        if not zero:
            return None
        idle += [n for n in zero if n not in idle]
    return idle or None


def clauses(text):
    """The Verify by conditions: parentheses dropped, split on ';' and ' and ', 'scan key ...' clauses left out."""
    prev = None
    while prev != text:
        prev, text = text, re.sub(r"\([^()]*\)", "", text)
    parts = [p.strip(" ,.") for p in re.split(r";| and ", text)]
    return [p for p in parts if p and not p.lower().startswith("scan key")]


def target_of(it, key):
    """(op, number) the Verify by sets for the key: '<key>.per_week below 2', '= 0 a week', or a leading '0 ...'."""
    vb = it.get("verify by", "")
    m = re.search(re.escape(key) + r"\.per_week\s*" + TARGET.pattern[len(r"(?<![\w-])"):], vb)
    if m:
        return OPS[m.group(1)], float(m.group(2))
    cl = clauses(vb)
    if not cl:
        return None
    m = TARGET.search(cl[0])
    if m:
        return OPS[m.group(1)], float(m.group(2))
    m = re.match(r"^(?:[^,\d]*,\s*)?(\d+(?:\.\d+)?)\s+[a-z]", cl[0])
    return ("=", float(m.group(1))) if m else None


def meets(value, op, t):
    return {"<": value < t, "<=": value <= t, "=": value == t, ">": value > t, ">=": value >= t}[op]


def hint(it, scan, started=None):
    """A suggested verdict for a done item with its one-line reason; 'needs reading' where no rule decides."""
    end = scan.get("window.end")
    if not it["done"] or not end:
        return None
    ident = it["head"].split()[0]
    inside = scan.get("window.start") and ts(it["done"]) >= ts(scan["window.start"])
    keys = keys_of(it)
    if inside:
        s = (started or {}).get(ident)
        if not s or "error" in s:
            return "needs the Start scan above first; under 10 sessions there -> too early"
        n, st = int(s.get("sessions.count", s.get("sessions", 0))), int(s.get("sessions.startup", 0))
        count = sum(int(s.get(k + ".count", 0)) for k in keys) if keys else None
    else:
        m = TALLY.match(it.get("since done", ""))
        if not m:
            return "needs reading - no Since Done tally in the standard form"
        n, st = int(m.group(1)), int(m.group(2))
        if m.group(4) < end:
            n += int(scan.get("sessions.count", scan.get("sessions", 0)))
            st += int(scan.get("sessions.startup", 0))
        c = re.match(r"^(\d+)\s", m.group(3))
        count = None
        if keys and c:
            count = int(c.group(1)) + (sum(int(scan.get(k + ".count", 0)) for k in keys) if m.group(4) < end else 0)
    if n < EARLY:
        return f"too early - {n} sessions since Done, under 10"
    j = JUDGE_ON.search(it.get("verify by", ""))
    if j and j.group(1) > end[:10]:
        return f"too early - its Verify by judges it on {j.group(1)}"
    restart = RESTART_FIX.search(it.get("fix", ""))
    if st < EARLY and restart:
        return (f"too early - the fix needs a restart (its Fix line names {restart.group(0)}) and only {st} "
                "sessions since Done were fresh starts")
    if len(keys) != 1 or count is None:
        why = "no scan key" if not keys else ("several scan keys" if len(keys) > 1 else "the tally's count is not a number")
        return f"needs reading - {why}; judge it from the Verify by line"
    key = keys[0]
    tgt = target_of(it, key)
    if not tgt:
        return f"needs reading - {key} has no numeric target in Verify by"
    if key.startswith(CANDIDATE) and count:
        return f"needs reading - {count} {key} candidates; read them in scan.md section 6"
    days = max((ts(end) - ts(it["done"])).total_seconds() / 86400, 1 / 24)
    rate = round(count * 7 / days, 1)
    op, t = tgt
    got = f"{count} since Done" + ("" if op == "=" and t == 0 else f" ({rate} a week over {days:.1f} days)")
    want = f"target {op} {t:g}"
    no_restart = "" if st >= EARLY else "; its Fix line names no restart"
    if meets(count if (op == "=" and t == 0) else rate, op, t):
        if len(clauses(it.get("verify by", ""))) > 1:
            idle = untested(it, key, s if inside else scan)
            if idle:
                where = "since Done" if inside else "in this window"
                return (f"stays done, not judged yet - {key} meets its target ({got}, {want}), but its other Verify "
                        f"by condition needs {' and '.join(idle)} to run, and it ran 0 times {where}")
            return f"needs reading - {key} meets its target ({got}, {want}); read the other Verify by conditions"
        b = BASELINE.search(it.get("verify by", ""))
        return (f"verified - {key}: " + (f"{b.group(1)} -> " if b else "") + f"{rate} a week, {want}, "
                f"{n} sessions since Done{no_restart}")
    b = BASELINE.search(it.get("verify by", ""))
    if not b:
        return f"needs reading - {key} misses its target ({got}, {want}); compare with the baseline in Verify by"
    if rate < float(b.group(1)):
        return f"on track - {key} down from {b.group(1)} to {rate} a week, {want} not reached yet"
    return f"not working - {key} at {rate} a week, baseline {b.group(1)}, {want}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--scan-json", help="this window's scan.json; adds its counts to every Since Done tally")
    ap.add_argument("--start-tallies", metavar="DIR", help="with --scan-json: run the scan since Done for each item "
                    "whose Done is inside the window (in parallel), writing since-<ID>.md/.json into DIR")
    ap.add_argument("--projects-dir", help=argparse.SUPPRESS)      # passed to scan.py (tests)
    a = ap.parse_args()
    L = parse(open(a.ledger, encoding="utf-8").read())
    scan = json.load(open(a.scan_json, encoding="utf-8")) if a.scan_json else None
    started = None
    if scan and a.start_tallies:
        inside = [it for it in L["items"] if it["state"] in ACTIVE and it["done"] and scan.get("window.start")
                  and ts(it["done"]) >= ts(scan["window.start"])]
        started = start_scans(inside, scan["window.end"], a.start_tallies, a.projects_dir)
    P = [f"Last run: {L['last_run']}", f"Last Runs row: {L['last_row']}"]
    if scan:
        n = scan.get("sessions.count", scan.get("sessions"))
        P.append(f"This window: {scan.get('window.start')} to {scan.get('window.end')} UTC, "
                 f"{n} sessions ({scan.get('sessions.startup', 0)} startup)")
        P.append(EDGE)
    P += ["", f"## Open items ({len(L['items'])})"]
    for it in L["items"]:
        P.append(f"- {it['head']} | {it['state']}" + (f" | Done {it['done']} UTC" if it["done"] else ""))
        if it.get("verify by"):
            P.append(f"  Verify by: {it['verify by']}")
        if it.get("since done"):
            P.append(f"  Since Done: {it['since done']}")
        if scan and it["state"] in ACTIVE:
            P += tally(it, scan, started)
            sk = skill_counts(it, scan)
            if sk:
                P.append(f"  Skill calls this window: {', '.join(sk)} (from scan.json; 0 = not used, no read needed)")
            h = hint(it, scan, started) if it["state"] == "done" else None
            if h:
                P.append(f"  Hint: {h}")
    P += ["", f"## Checked, no action ({len(L['checked'])}): skip these unless a session after Last run backs them"]
    P += [f"- {c}" for c in L["checked"]]
    closed = ", ".join(f"{k} {v}" for k, v in sorted(L["closed"].items()))
    P += ["", f"## Closed items: {sum(L['closed'].values())} ({closed}); match a candidate on these Signal lines"]
    P += [f"- {x}" for x in L["signals"]]
    sys.stdout.write("\n".join(P) + "\n")


if __name__ == "__main__":
    main()
