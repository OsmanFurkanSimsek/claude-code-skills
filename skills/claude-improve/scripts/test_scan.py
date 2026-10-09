"""Tests for scan.py's export count, Stop-block count, --until and raw counts.
Run: python -m pytest --import-mode=importlib -p no:cacheprovider test_scan.py"""
import importlib.util, json, os, subprocess, sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("scan_under_test", os.path.join(HERE, "scan.py"))
scan = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scan)


@pytest.mark.parametrize("cmd,names", [
    ("export FOO=1", ["FOO"]),
    ("cd x && export FOO=1 && run", ["FOO"]),
    ("a; export FOO=1; b", ["FOO"]),
    ("a || export FOO=1", ["FOO"]),
    ("a | export FOO=1", ["FOO"]),
    ("(export FOO=1; run)", ["FOO"]),
    ("a\n  export FOO=1\nb", ["FOO"]),
    ("if t; then export FOO=1; fi", ["FOO"]),
    ("for i in 1; do export FOO=$i; done", ["FOO"]),
    ("if t; then :; else export FOO=1; fi", ["FOO"]),
    ("grep -q '^export PATH=' f", []),               # reads a file: no export (2026-10-09 false positives)
    ('grep -c "^export PATH=" f', []),
    ("grep -m1 -o \"^export PATH=.*\" f", []),
    ("echo export FOO=1", []),                       # an argument, not a command
    ("export FOO", []),                              # no value set
])
def test_export_only_at_a_command_position(cmd, names):
    assert scan.EXPORT_AT_COMMAND.findall(cmd) == names


def line(**o):
    return json.dumps(o)


def tool(ts, mid, name, inp):
    return line(type="assistant", timestamp=ts, cwd="/work/proj",
                message={"id": mid, "model": "m", "usage": {"input_tokens": 1000},
                         "content": [{"type": "tool_use", "id": "t" + mid, "name": name, "input": inp}]})


def stop_block(ts):
    return line(type="attachment", timestamp=ts, cwd="/work/proj",
                attachment={"type": "hook_blocking_error", "hookName": "Stop", "hookEvent": "Stop",
                            "blockingError": {"blockingError": "PROJECT.md was NOT updated after these project "
                                                               "edits:\n - notes/a.md"}})


@pytest.fixture
def projects(tmp_path):
    d = tmp_path / "projects" / "-work-proj"
    d.mkdir(parents=True)
    rows = [
        line(type="attachment", timestamp="2026-10-09T10:00:00Z", cwd="/work/proj",
             attachment={"type": "hook_success", "hookName": "SessionStart:startup", "content": "hi"}),
        tool("2026-10-09T10:00:05Z", "1", "Bash", {"command": "grep -q '^export PATH=' f && export FOO=1"}),
        stop_block("2026-10-09T10:01:00Z"),
        tool("2026-10-09T10:02:00Z", "2", "Edit", {"file_path": "C:\\work\\proj\\PROJECT.md"}),
        stop_block("2026-10-09T10:03:00Z"),
        tool("2026-10-09T12:00:00Z", "3", "Write", {"file_path": "/work/proj/PROJECT.md"}),
    ]
    (d / "s1.jsonl").write_text("\n".join(rows) + "\n", encoding="utf-8")
    (tmp_path / "addons").mkdir()
    return tmp_path


def run_scan(tmp, *extra):
    out, js = tmp / "scan.md", tmp / "scan.json"
    subprocess.run([sys.executable, os.path.join(HERE, "scan.py"), "--since", "2026-10-09 09:00",
                    "--projects-dir", str(tmp / "projects"), "--private-dir", str(tmp / "addons"),
                    "--out", str(out), "--json", str(js), *extra], check=True, capture_output=True)
    return out.read_text(encoding="utf-8"), json.loads(js.read_text(encoding="utf-8"))


def test_stop_blocks_and_reconciles(projects):
    md, m = run_scan(projects)
    assert m["hook.stop.project_md.blocks"] == 2 and m["hook.stop.project_md.reconciled"] == 2
    assert 'Stop blocks "PROJECT.md was NOT updated": 2, followed by an Edit/Write of a PROJECT.md' in md
    assert m["bash.export.FOO.count"] == 1 and "bash.export.PATH.per_week" not in m
    assert m["sessions.startup"] == 1 and m["sessions.count"] == 1


def test_until_stops_the_window_and_counts_stay_raw(projects):
    md, m = run_scan(projects, "--until", "2026-10-09 11:00")
    assert m["window.start"] == "2026-10-09 09:00" and m["window.end"] == "2026-10-09 11:00"
    assert "to 2026-10-09 11:00 UTC" in md
    # the second block's reconcile (12:00) lies after --until, so it is listed as not followed
    assert m["hook.stop.project_md.blocks"] == 2 and m["hook.stop.project_md.reconciled"] == 1
    assert "not followed:" in md
    assert m["bash.calls.count"] == 1 and m["bash.calls.per_week"] == round(1 * 7 / (2 / 24), 2)
    assert "bash.calls.count" not in md               # raw counts live in the --json file only


def user(ts, text):
    return line(type="user", timestamp=ts, cwd="/work/proj", message={"role": "user", "content": text})


def test_owner_time_asks_voice_corrections_and_missing_tools_are_counted(projects):
    d = projects / "projects" / "-work-proj"
    rows = [
        user("2026-10-09T10:10:00Z", "How far are you? How long will it take?"),     # one message, one ask
        user("2026-10-09T10:11:00Z", "are you still working on it"),
        user("2026-10-09T10:12:00Z", "That's wrong, it does not sound like me"),        # correction about voice
        user("2026-10-09T10:13:00Z", "you forgot the second table"),                     # correction, not voice
        user("2026-10-09T10:14:00Z", "<command-name>/clear</command-name> how far are you"),   # a command: no ask
        tool("2026-10-09T10:15:00Z", "9", "Gone", {}),
        line(type="user", timestamp="2026-10-09T10:15:01Z", cwd="/work/proj",
             message={"role": "user", "content": [{"type": "tool_result", "tool_use_id": "t9", "is_error": True,
                      "content": "<tool_use_error>Error: No such tool available: Gone</tool_use_error>"}]}),
    ]
    with open(d / "s1.jsonl", "a", encoding="utf-8") as fh:
        fh.write("\n".join(rows) + "\n")
    md, m = run_scan(projects)
    assert m["owner.time_asks.count"] == 2
    assert m["owner.corrections.count"] == 2 and m["owner.corrections.voice.count"] == 1
    assert m["tool.err.no_such_tool.count"] == 1
    assert "Owner asks about the time left: 2. Calls to a tool that does not exist: 1" in md


def test_new_owner_keys_are_zero_when_nothing_matches(projects):
    _, m = run_scan(projects)
    for k in ("owner.time_asks", "owner.corrections", "owner.corrections.voice", "tool.err.no_such_tool"):
        assert m[k + ".count"] == 0 and m[k + ".per_week"] == 0


def test_unused_installed_skills_are_zero_in_json_only(projects):
    md, m = run_scan(projects)
    sk = os.path.join(scan.CLAUDE, "skills")
    names = [d for d in os.listdir(sk) if os.path.isfile(os.path.join(sk, d, "SKILL.md"))] if os.path.isdir(sk) else []
    for n in names:                       # the fixture calls no skill: each installed one is written as 0
        assert m["skill.calls." + n + ".count"] == 0 and m["skill.calls." + n + ".per_week"] == 0
        assert '"skill.calls.' + n + '.per_week"' not in md          # scan.md's metrics block stays as it was


def test_known_quirks_are_explained_in_place(projects):
    md, _ = run_scan(projects)                      # the fixture has no cost-state line: its cost is unknown
    assert "1 session(s) have no cost record in the transcript yet (shown as $0), so this is a lower bound" in md
    assert "(? = no SessionStart" not in md         # its SessionStart (10:00) is inside the window
    md2, _ = run_scan(projects, "--since", "2026-10-09 10:01")
    assert "Sessions by start source: ? 1 (? = no SessionStart record inside the window: the session started " \
           "before it)" in md2


def test_big_read_names_its_file(projects):
    d = projects / "projects" / "-work-proj"
    rows = [tool("2026-10-09T10:20:00Z", "8", "Read", {"file_path": "C:\\work\\proj\\notes\\big-file.md"}),
            line(type="user", timestamp="2026-10-09T10:20:01Z", cwd="/work/proj",
                 message={"role": "user", "content": [{"type": "tool_result", "tool_use_id": "t8",
                                                       "content": "x" * 30000}]})]
    with open(d / "s1.jsonl", "a", encoding="utf-8") as fh:
        fh.write("\n".join(rows) + "\n")
    md, _ = run_scan(projects)
    assert "  - 30K Read (" in md and "): big-file.md [s1 10-09 10:20]" in md


def test_time_left_and_time_estimate_count_as_time_asks(projects):
    d = projects / "projects" / "-work-proj"
    rows = [user("2026-10-09T10:30:00Z", "how long time left?"),               # missed before 2026-10-09
            user("2026-10-09T10:31:00Z", "What is your final time estimate?"),
            user("2026-10-09T10:32:00Z", "the time table is fine")]               # no ask
    with open(d / "s1.jsonl", "a", encoding="utf-8") as fh:
        fh.write("\n".join(rows) + "\n")
    _, m = run_scan(projects)
    assert m["owner.time_asks.count"] == 2
