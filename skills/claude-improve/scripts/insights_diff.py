#!/usr/bin/env python3
"""insights_diff.py - what an /insights report can add since the last review, without re-mapping old points.

/insights rewrites its whole text from every session it ever analysed (months), so two reports of the same day
share almost no lines. What can be new is only what sessions after `Last run:` brought: their per-session
analyses (`usage-data/facets/<session>.json`), dated through `usage-data/session-meta/<session>.json`.
This script lists the points of the new report (marked: same title as the previous report or not) and every
facet of a session active after --since, so each point is judged in one line and no helper re-dates old cases.

Usage:
  python insights_diff.py --since "YYYY-MM-DD HH:MM" --out <scratchpad>/insights-diff.md
      [--new <report.html>] [--prev <report.html>] [--usage-dir ~/.claude/usage-data]
Defaults: --new = newest report-*.html, --prev = the newest one older than --new. Writes both reports as plain
text next to --out (insights-new.txt, insights-prev.txt). Read-only otherwise. Standard library only.
"""
import argparse, datetime as dt, glob, html, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from html2text import convert  # noqa: E402

TEST_RUN_DIR = re.compile(r"AppData-Local-Temp|-workspace-", re.I)   # same rule as scan.py
KINDS = [("friction", "friction-title"), ("CLAUDE.md addition", "cmd-code"), ("feature", "feature-title"),
         ("new way", "pattern-title"), ("horizon", "horizon-title")]


def clean(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()


def points(src):
    """[(kind, title, examples)] in report order; a CLAUDE.md addition is titled by its first line."""
    out = []
    for kind, cls in KINDS:
        for m in re.finditer(r'class="%s"[^>]*>(.*?)</(?:div|code)>' % cls, src, re.S):
            title = clean(m.group(1).strip().split("\n")[0])
            ex = []
            if kind == "friction":
                tail = src[m.end():m.end() + 6000]
                em = re.search(r'class="friction-examples"[^>]*>(.*?)</ul>', tail, re.S)
                ex = [clean(x) for x in re.findall(r"<li[^>]*>(.*?)</li>", em.group(1), re.S)] if em else []
            out.append((kind, title, ex))
    return out


def norm(t):
    return re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()


def headline(text):
    return next((l for l in text.splitlines() if re.match(r"[\d,]+ messages across [\d,]+ sessions", l)), "?")


def stamp(path):
    m = re.search(r"report-(\d{4}-\d{2}-\d{2})-(\d{2})(\d{2})(\d{2})\.html$", path)
    return f"{m.group(1)} {m.group(2)}:{m.group(3)} local" if m else os.path.basename(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", required=True, help="the ledger's Last run:, 'YYYY-MM-DD HH:MM' UTC")
    ap.add_argument("--out", required=True)
    ap.add_argument("--new"); ap.add_argument("--prev")
    ap.add_argument("--usage-dir", default=os.path.join(os.path.expanduser("~"), ".claude", "usage-data"))
    a = ap.parse_args()
    since = dt.datetime.fromisoformat(a.since).replace(tzinfo=dt.timezone.utc)
    reports = sorted(glob.glob(os.path.join(a.usage_dir, "report-*.html")))
    new = a.new or (reports[-1] if reports else None)
    if not new:
        sys.exit("no report-*.html in " + a.usage_dir)
    prev = a.prev or next((r for r in reversed(reports) if os.path.basename(r) < os.path.basename(new)), None)
    out_dir = os.path.dirname(os.path.abspath(a.out))
    src_new = open(new, encoding="utf-8", errors="replace").read()
    src_prev = open(prev, encoding="utf-8", errors="replace").read() if prev else ""
    txt_new, txt_prev = convert(src_new), convert(src_prev)
    open(os.path.join(out_dir, "insights-new.txt"), "w", encoding="utf-8").write(txt_new)
    if prev:
        open(os.path.join(out_dir, "insights-prev.txt"), "w", encoding="utf-8").write(txt_prev)
    p_new, p_prev = points(src_new), points(src_prev)
    old_titles = {(k, norm(t)) for k, t, _ in p_prev}

    # Sessions active after --since, dated by their session-meta; test runs left out as in scan.py.
    after, faceted = [], []
    for mp in glob.glob(os.path.join(a.usage_dir, "session-meta", "*.json")):
        try:
            meta = json.load(open(mp, encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if TEST_RUN_DIR.search(re.sub(r"[^A-Za-z0-9]", "-", meta.get("project_path") or "")):
            continue
        times = [t for t in (meta.get("user_message_timestamps") or []) + [meta.get("start_time")] if t]
        last = max((dt.datetime.fromisoformat(t.replace("Z", "+00:00")) for t in times), default=None)
        if not last or last < since:
            continue
        sid = meta.get("session_id") or os.path.basename(mp)[:-5]
        after.append(sid)
        fp = os.path.join(a.usage_dir, "facets", sid + ".json")
        if os.path.isfile(fp):
            try:
                f = json.load(open(fp, encoding="utf-8"))
            except (OSError, ValueError):
                continue
            proj = os.path.basename((meta.get("project_path") or "?").rstrip("\\/").replace("\\", "/"))
            faceted.append((last, sid, proj, f))

    L = ["# /insights since the last review", "",
         f"- New report: `{os.path.basename(new)}` ({stamp(new)}): {headline(txt_new)}",
         f"- Previous report: " + (f"`{os.path.basename(prev)}` ({stamp(prev)}): {headline(txt_prev)}" if prev else "none"),
         f"- Since (the ledger's Last run): {since:%Y-%m-%d %H:%M} UTC. Plain text of both: `insights-new.txt`, "
         "`insights-prev.txt` next to this file.", "",
         "## Points in the new report", "",
         "A title can change while the point stays the same (the text is rewritten every run); the facets below "
         "decide what is new.", ""]
    for kind, title, ex in p_new:
        tag = "same title as before" if (kind, norm(title)) in old_titles else "new title"
        L.append(f"- [{kind}] {title} ({tag})")
        for e in ex:
            L.append(f"  - example: {e[:300]}")
    gone = [(k, t) for k, t, _ in p_prev if (k, norm(t)) not in {(k2, norm(t2)) for k2, t2, _ in p_new}]
    if gone:
        L += ["", "Titles in the previous report only: " + "; ".join(f"[{k}] {t}" for k, t in gone)]
    L += ["", f"## Sessions after {since:%Y-%m-%d %H:%M} UTC with an /insights analysis", "",
          f"{len(after)} sessions active after it (test runs left out); {len(faceted)} have an analysis (facet). "
          "A session without one was too short or not analysed yet.", ""]
    for last, sid, proj, f in sorted(faceted, key=lambda x: x[0]):
        fr = ", ".join(f"{k} {v}" for k, v in (f.get("friction_counts") or {}).items()) or "none"
        L.append(f"- {sid[:8]} {proj} (last message {last:%m-%d %H:%M} UTC): outcome {f.get('outcome', '?')}; "
                 f"friction {fr}")
        if f.get("friction_detail"):
            L.append(f"  - friction: {clean(f['friction_detail'])[:400]}")
        elif f.get("brief_summary"):
            L.append(f"  - summary: {clean(f['brief_summary'])[:200]}")
    L += ["", "## How to use this", "",
          "- A point that no facet above backs has all its cases before the last review: one line under "
          "\"Checked, no action\" (\"no case after <Last run>\") if the ledger does not cover it yet, else nothing. "
          "No helper, no transcript reading.",
          "- A point a facet above backs is a candidate: read that session (its id is above) in context, as in "
          "Step 3.",
          "- A suggestion (CLAUDE.md addition, feature, new way, horizon) the ledger already answered stays "
          "answered unless a facet above gives new evidence for it."]
    open(a.out, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"insights_diff: {len(p_new)} points ({sum(1 for k, t, _ in p_new if (k, norm(t)) not in old_titles)} "
          f"new titles), {len(after)} sessions after since, {len(faceted)} with a facet -> {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
