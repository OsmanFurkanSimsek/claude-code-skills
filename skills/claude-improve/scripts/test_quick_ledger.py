"""Tests for quick_ledger.py (the quick path's ledger view and Since Done tallies).
Run: python -m pytest --import-mode=importlib -p no:cacheprovider test_quick_ledger.py"""
import importlib.util, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("quick_ledger_under_test", os.path.join(HERE, "quick_ledger.py"))
ql = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ql)
E6 = os.path.join(HERE, "..", "evals", "files", "e6")
LEDGER = os.path.join(E6, "project-memory", "claude-improve-ledger.md")

MINI = """# Claude improve ledger

Last run: 2026-10-09 09:00 UTC

## Runs

| Date | Window | Sessions | Spend | New | Verified | Not working | Muted skipped |
|---|---|---|---|---|---|---|---|
| 2026-10-09 | 10-02 08:00 to 10-09 09:00 UTC | 9 | $71 | 1 | 0 | 0 | 1 |

## Open items

### CI-9 Counted by a scan key
- Status: done | Raised: 2026-10-01 | Answered: 2026-10-01 | Done: 2026-10-01 08:00 UTC
- Signal: bash.err.unicode.per_week
- Fix: UTF-8 variables in the settings env block
- Verify by: bash.err.unicode.per_week below 1 (baseline 4)
- Since Done: 10 sessions (3 startup), 1 unicode error, through 2026-10-09 09:00 UTC

### CI-8 Counted by reading
- Status: later | Raised: 2026-10-01 | Answered: 2026-10-01 | Done: 2026-10-01 08:00 UTC
- Signal: owner asks about the wait
- Verify by: 0 asks a week
- Since Done: 10 sessions (3 startup), 0 asks, through 2026-10-09 09:00 UTC

### CI-7 Older fix without a tally
- Status: done | Raised: 2026-10-01 | Answered: 2026-10-01 | Done: 2026-10-05 08:00 UTC
- Signal: compactions.per_week
- Verify by: compactions.per_week below 1

### CI-6 Waiting
- Status: waiting on owner | Raised: 2026-10-01
- Signal: something

### CI-5 Later, nothing landed yet
- Status: later | Raised: 2026-10-01 | Answered: 2026-10-01
- Signal: interrupts.per_week

## Checked, no action

| Checked | Source | Point | Verdict and where it is handled |
|---|---|---|---|
| 10-09 | /insights | Outputs too long | No case after 10-05 |

## Closed items

### CI-1 Old
- Status: verified | Raised: 2026-09-18 | Answered: 2026-09-18 | Done: 2026-09-18 09:10 UTC
- Signal: owner messages "are we there yet"
- Fix: SECRET-CLOSED-BODY

### CI-2 Older, no signal
- Status: muted | Raised: 2026-09-10
"""
SCAN = {"window.start": "2026-10-09 09:00", "window.end": "2026-10-09 12:00", "sessions": 4, "sessions.count": 4,
        "sessions.startup": 2, "bash.err.unicode.count": 2, "compactions.count": 0}


def run(tmp_path, ledger_text, scan=None):
    led = tmp_path / "ledger.md"
    led.write_text(ledger_text, encoding="utf-8")
    cmd = [sys.executable, os.path.join(HERE, "quick_ledger.py"), "--ledger", str(led)]
    if scan is not None:
        sj = tmp_path / "scan.json"
        sj.write_text(json.dumps(scan), encoding="utf-8")
        cmd += ["--scan-json", str(sj)]
    before = sorted(os.listdir(tmp_path))
    out = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", check=True).stdout
    assert sorted(os.listdir(tmp_path)) == before          # read-only: nothing written
    return out


def test_e6_fixture_view_and_tallies():
    out = subprocess.run([sys.executable, os.path.join(HERE, "quick_ledger.py"), "--ledger", LEDGER,
                          "--scan-json", os.path.join(E6, "scan.json")],
                         capture_output=True, text=True, encoding="utf-8", check=True).stdout
    assert "Last run: 2026-10-09 09:00 UTC" in out
    assert "## Open items (2)" in out and "## Checked, no action (6)" in out
    assert "## Closed items: 2 (muted 1, verified 1)" in out
    # CI-7: Done 10:30 falls inside the 09:00-12:00 window -> the one in-window scan, nothing added
    assert 'start the tally with `scan.py --since "2026-10-09 10:30" --until "2026-10-09 12:00"' in out
    # CI-6: 8 (5) + this window's 4 (3); heredoc_eof absent from scan.json = 0 events
    assert "New: 12 sessions (8 startup), 0 heredoc_eof errors, through 2026-10-09 12:00 UTC" in out
    # CI-6's Fix is a rule line, not a restart: 8 startup of 12 does not make it too early
    assert ("(+0 from bash.err.heredoc_eof.count) -> under 10 startup does not matter: its Fix line names no "
            "restart") in out
    assert out.count("  Fix:") == 0                                       # no restart fix, so no Fix line
    assert len(out.splitlines()) < 40


def test_scan_key_count_is_summed(tmp_path):
    out = run(tmp_path, MINI, SCAN)
    assert ("New: 14 sessions (5 startup), 3 unicode error, through 2026-10-09 12:00 UTC "
            "(+2 from bash.err.unicode.count)") in out
    assert "  Fix: UTF-8 variables in the settings env block" in out and out.count("  Fix:") == 1


def test_count_without_scan_key_is_marked_for_reading(tmp_path):
    out = run(tmp_path, MINI, SCAN)
    assert "New: 14 sessions (5 startup), 0 asks, through 2026-10-09 12:00 UTC (count: no scan key" in out


def test_no_tally_before_window_gets_the_one_time_scan(tmp_path):
    out = run(tmp_path, MINI, SCAN)
    assert ('No tally yet: take it from History if it gives counts, else run once '
            '`scan.py --since "2026-10-05 08:00"') in out
    assert out.count("No tally yet") == 1                   # CI-5 (later, no Done) has nothing to tally


def test_waiting_item_gets_no_tally_and_closed_bodies_stay_out(tmp_path):
    out = run(tmp_path, MINI, SCAN)
    assert "- CI-6 Waiting | waiting on owner" in out
    assert out.count("New:") == 2
    assert "SECRET-CLOSED-BODY" not in out and "## Closed items: 2 (muted 1, verified 1)" in out


def test_closed_signal_lines_are_printed_one_each(tmp_path):
    out = run(tmp_path, MINI, SCAN)
    tail = out.split("## Closed items:")[1].splitlines()[1:]
    assert tail == ['- CI-1 (verified): owner messages "are we there yet"', "- CI-2 (muted): (no Signal line)"]
    assert "grep" not in out.split("## Closed items:")[1]


def test_already_through_window_end_adds_nothing(tmp_path):
    out = run(tmp_path, MINI.replace("through 2026-10-09 09:00 UTC", "through 2026-10-09 12:00 UTC"), SCAN)
    assert out.count("Already through 2026-10-09 12:00: nothing to add") == 2


def test_start_tallies_runs_the_in_window_scan_into_the_given_folder(tmp_path):
    empty = tmp_path / "projects"
    empty.mkdir()
    out = subprocess.run([sys.executable, os.path.join(HERE, "quick_ledger.py"), "--ledger", LEDGER,
                          "--scan-json", os.path.join(E6, "scan.json"), "--start-tallies", str(tmp_path),
                          "--projects-dir", str(empty)],
                         capture_output=True, text=True, encoding="utf-8", check=True).stdout
    assert (tmp_path / "since-CI-7.json").exists() and (tmp_path / "since-CI-7.md").exists()
    assert not (tmp_path / "since-CI-6.json").exists()      # CI-6's Done is before the window: tally, no scan
    assert ("Start (scan since Done, since-CI-7.md): 0 sessions (0 startup), through 2026-10-09 12:00 UTC; "
            "0 from edit.err.modified_since.count -> too early (under 10 sessions)") in out
    assert "New: 12 sessions (8 startup)" in out


def test_without_scan_json_only_the_view(tmp_path):
    out = run(tmp_path, MINI)
    assert "Since Done: 10 sessions (3 startup), 1 unicode error" in out and "New:" not in out
    assert "- 10-09 /insights: Outputs too long" in out


def test_owner_correction_key_is_a_candidate_count(tmp_path):
    led = MINI.replace("- Verify by: 0 asks a week", "- Verify by: owner.corrections.voice.per_week = 0")
    out = run(tmp_path, led, dict(SCAN, **{"owner.corrections.voice.count": 2}))
    assert ("New: 14 sessions (5 startup), 2 asks, through 2026-10-09 12:00 UTC (+2 from "
            "owner.corrections.voice.count; candidates: read them in scan.md section 6 before counting)") in out
    out0 = run(tmp_path / ".." / tmp_path.name, led, dict(SCAN, **{"owner.corrections.voice.count": 0}))
    assert "+0 from owner.corrections.voice.count)" in out0 and "candidates:" not in out0


def test_time_ask_key_turns_a_read_into_a_count(tmp_path):
    led = MINI.replace("- Verify by: 0 asks a week", "- Verify by: owner.time_asks.per_week = 0 (baseline 7)")
    out = run(tmp_path, led, dict(SCAN, **{"owner.time_asks.count": 0}))
    assert "New: 14 sessions (5 startup), 0 asks, through 2026-10-09 12:00 UTC (+0 from owner.time_asks.count)" in out
    assert "no scan key" not in out


def item(verify, since="10 sessions (10 startup), 0 errors, through 2026-10-09 09:00 UTC", fix="a rule line",
         status="done", done="2026-10-02 09:00 UTC", head="CI-9 Hinted"):
    return MINI.split("### CI-9")[0] + (f"### {head}\n- Status: {status} | Raised: 2026-10-01 | Done: {done}\n"
                                         f"- Fix: {fix}\n- Verify by: {verify}\n- Since Done: {since}\n\n"
                                         "## Checked, no action\n\n## Closed items\n")


def hint_line(out):
    return [l.strip() for l in out.splitlines() if l.strip().startswith("Hint:")]


def test_window_edge_is_one_line_with_a_scan_only(tmp_path):
    out = run(tmp_path, MINI, SCAN)
    assert out.count("Window edge: a session that crosses a window edge counts in both windows") == 1
    assert "nothing to check" in out
    assert "Window edge" not in run(tmp_path, MINI)


def test_e6_hints_verified_on_the_tally_and_start_first():
    out = subprocess.run([sys.executable, os.path.join(HERE, "quick_ledger.py"), "--ledger", LEDGER,
                          "--scan-json", os.path.join(E6, "scan.json")],
                         capture_output=True, text=True, encoding="utf-8", check=True).stdout
    assert hint_line(out) == [
        "Hint: needs the Start scan above first; under 10 sessions there -> too early",
        "Hint: verified - bash.err.heredoc_eof: 5.0 -> 0.0 a week, target < 2, 12 sessions since Done; "
        "its Fix line names no restart"]


def test_hint_too_early_by_sessions_judge_date_and_restart(tmp_path):
    few = item("bash.err.x.per_week below 1 (baseline 3)", since="2 sessions (2 startup), 0 errors, through "
               "2026-10-09 09:00 UTC")
    assert hint_line(run(tmp_path, few, SCAN)) == ["Hint: too early - 6 sessions since Done, under 10"]
    later = item("rounds per output fall. Judge on 2026-11-05 (`--since 2026-10-08`)")
    assert hint_line(run(tmp_path, later, SCAN)) == ["Hint: too early - its Verify by judges it on 2026-11-05"]
    restart = item("bash.err.x.per_week below 1", since="20 sessions (3 startup), 0 errors, through 2026-10-09 "
                   "09:00 UTC", fix="a block in `~/.bashrc`")
    assert hint_line(run(tmp_path, restart, SCAN)) == [
        "Hint: too early - the fix needs a restart (its Fix line names .bashrc) and only 5 sessions since Done were "
        "fresh starts"]
    # MINI's CI-9: 14 sessions, 5 startup, Fix "settings env" -> a restart fix; CI-8 (later) gets no hint
    out = run(tmp_path, MINI, SCAN)
    assert hint_line(out)[0].startswith("Hint: too early - the fix needs a restart (its Fix line names settings env)")
    assert "Hint:" not in out.split("- CI-8")[1].split("- CI-7")[0]           # later: no hint
    assert hint_line(out)[1] == "Hint: needs reading - no Since Done tally in the standard form"   # CI-7


def test_only_a_restart_fix_makes_few_fresh_starts_too_early(tmp_path):
    since = "11 sessions (1 startup), 0 errors, through 2026-10-09 09:00 UTC"
    # skill files moved, pointer files, a taste profile, the MCP tools used, a plugin skill: none needs a restart
    for fix in ("voice rules move into `skill-a/references/voice/`; about 20 pointer files (rules, hooks)",
                "a working-style profile section in the skill", "the report reads the MCP tools' output",
                "a new plugin skill folder"):
        out = run(tmp_path, item("bash.err.x.per_week below 1 (baseline 3)", since=since, fix=fix), SCAN)
        assert ("New: 15 sessions (3 startup), 0 errors, through 2026-10-09 12:00 UTC (+0 from bash.err.x.count) -> "
                "under 10 startup does not matter: its Fix line names no restart") in out, fix
        assert "  Fix:" not in out and "needs a restart" not in out, fix
        assert "restart" not in hint_line(out)[0].split("; its Fix line")[0], fix
    # a settings env value, an MCP server, the shell profile or the enabled plugins: too early under 10 fresh starts
    for fix, word in (("UTF-8 variables in the settings env block", "settings env"),
                      ("adds the `reports` MCP server to the user config", "MCP server"),
                      ("two blocks in `~/.bash_profile`", ".bash_profile"),
                      ("`enabledPlugins` false for both", "enabledPlugins")):
        out = run(tmp_path, item("bash.err.x.per_week below 1 (baseline 3)", since=since, fix=fix), SCAN)
        assert (f"-> under 10 startup and the fix needs a restart (its Fix line names {word}): too early") in out, fix
        assert f"  Fix: {fix}" in out, fix
        assert hint_line(out)[0].startswith(f"Hint: too early - the fix needs a restart (its Fix line names {word})")


def test_hint_from_a_numeric_target(tmp_path):
    scan = dict(SCAN, **{"bash.err.x.count": 1})
    met = item("bash.err.x.per_week below 2 (baseline 5)")          # 0 + 1 over 7.1 days -> 1.0 a week
    assert hint_line(run(tmp_path, met, scan)) == [
        "Hint: verified - bash.err.x: 5 -> 1.0 a week, target < 2, 14 sessions since Done"]
    track = item("bash.err.x.per_week below 0.5 (baseline 5)")
    assert hint_line(run(tmp_path, track, scan))[0].startswith(
        "Hint: on track - bash.err.x down from 5 to 1.0 a week, target < 0.5 not reached yet")
    bad = item("bash.err.x.per_week below 0.5 (baseline 1)")
    assert hint_line(run(tmp_path, bad, scan))[0].startswith("Hint: not working - bash.err.x at 1.0 a week, baseline 1")
    nobase = item("bash.err.x.per_week below 0.5")
    assert hint_line(run(tmp_path, nobase, scan))[0].startswith("Hint: needs reading - bash.err.x misses its target")


def test_hint_zero_target_forms_and_extra_conditions(tmp_path):
    lead = item("0 tasks that needed it (asks or failed calls); scan key tool.err.no_such_tool.per_week")
    assert hint_line(run(tmp_path, lead, SCAN))[0].startswith("Hint: verified - tool.err.no_such_tool: 0.0 a week")
    two = item("after the merge, 0 corrections (baseline 3) and every prompt still loads the rules; "
               "scan key owner.corrections.voice.per_week")
    assert hint_line(run(tmp_path, two, SCAN)) == [
        "Hint: needs reading - owner.corrections.voice meets its target (0 since Done, target = 0); read the other "
        "Verify by conditions"]
    cand = item("owner.corrections.voice.per_week = 0")
    out = run(tmp_path, cand, dict(SCAN, **{"owner.corrections.voice.count": 2}))
    assert hint_line(out) == ["Hint: needs reading - 2 owner.corrections.voice candidates; read them in scan.md section 6"]
    nokey = item("0 asks a week")
    assert hint_line(run(tmp_path, nokey, SCAN)) == [
        "Hint: needs reading - no scan key; judge it from the Verify by line"]


def test_other_condition_on_an_unused_skill_stays_done(tmp_path):
    vb = ("after the merge, 0 corrections (baseline 3) and every helper-skill trigger prompt still loads the rules; "
          "scan key owner.corrections.voice.per_week")
    led = item(vb, head="CI-9 Merge helper-skill into main-skill")
    unused = dict(SCAN, **{"skill.calls.helper-skill.count": 0, "skill.calls.main-skill.count": 2})
    assert hint_line(run(tmp_path, led, unused)) == [
        "Hint: stays done, not judged yet - owner.corrections.voice meets its target (0 since Done, target = 0), but "
        "its other Verify by condition needs helper-skill to run, and it ran 0 times in this window"]
    # the skill ran: the other condition can be judged now, so the item needs reading as before
    used = dict(unused, **{"skill.calls.helper-skill.count": 1})
    assert hint_line(run(tmp_path, led, used))[0].startswith("Hint: needs reading - owner.corrections.voice meets")
    # a second other condition that names no unused skill: still needs reading
    two = item(vb.replace("; scan key", " and the report lists it; scan key"), head="CI-9 Merge helper-skill")
    assert hint_line(run(tmp_path, two, unused))[0].startswith("Hint: needs reading - owner.corrections.voice meets")
    # the key misses its target: the unused skill changes nothing
    miss = dict(unused, **{"owner.corrections.voice.count": 1})
    assert "stays done" not in hint_line(run(tmp_path, led, miss))[0]


def test_named_skill_count_is_printed_zero_included(tmp_path):
    led = item("every helper-skill prompt still loads, counted by `other-skill/scripts/x.py`; scan key "
               "owner.corrections.voice.per_week",
               head="CI-9 Merge helper-skill into main-skill")
    scan = dict(SCAN, **{"skill.calls.helper-skill.count": 0, "skill.calls.main-skill.count": 3,
                         "skill.calls.other-skill.count": 5})
    out = run(tmp_path, led, scan)
    assert "  Skill calls this window: helper-skill 0, main-skill 3 (from scan.json; 0 = not used" in out
    assert "other-skill" not in [l for l in out.splitlines() if "Skill calls" in l][0]   # a path, not a mention
