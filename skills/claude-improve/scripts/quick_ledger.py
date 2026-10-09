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


RESTART = " -> under 10 startup: too early only for a fix that needs a restart (settings env, MCP, profile)"


def early(n, startup, note):
    """Step 2's too-early mark; an item under 10 sessions needs no reading, so its count note is dropped."""
    if n < EARLY:
        return " -> too early (under 10 sessions)" + (": nothing to read" if "no scan key" in note else "")
    return RESTART if startup < EARLY else ""


def with_fix(line, it):
    """When only a restart decides the verdict, add the item's Fix line so no ledger read is needed."""
    return [line] + ([f"  Fix: {it['fix']}"] if line.endswith(RESTART) and it.get("fix") else [])


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
                        "UTC" + ("" if n < EARLY and add is None else f"; {note}") + early(n, st, note), it)
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
    return with_fix(f"  New: {n2} sessions ({s2} startup), {what}, through {end} UTC{shown}{early(n2, s2, note)}", it)


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
    P += ["", f"## Open items ({len(L['items'])})"]
    for it in L["items"]:
        P.append(f"- {it['head']} | {it['state']}" + (f" | Done {it['done']} UTC" if it["done"] else ""))
        if it.get("verify by"):
            P.append(f"  Verify by: {it['verify by']}")
        if it.get("since done"):
            P.append(f"  Since Done: {it['since done']}")
        if scan and it["state"] in ACTIVE:
            P += tally(it, scan, started)
    P += ["", f"## Checked, no action ({len(L['checked'])}): skip these unless a session after Last run backs them"]
    P += [f"- {c}" for c in L["checked"]]
    closed = ", ".join(f"{k} {v}" for k, v in sorted(L["closed"].items()))
    P += ["", f"## Closed items: {sum(L['closed'].values())} ({closed}); match a candidate on these Signal lines"]
    P += [f"- {x}" for x in L["signals"]]
    sys.stdout.write("\n".join(P) + "\n")


if __name__ == "__main__":
    main()
