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
    assert ("(+0 from bash.err.heredoc_eof.count) -> under 10 startup: too early only for a fix that needs a "
            "restart") in out
    assert "  Fix: rule \"a script over ~10 lines goes to a file and runs by path\"" in out   # restart or not: no grep
    assert out.count("  Fix:") == 1                                       # CI-7 (2 sessions) needs no Fix line
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
