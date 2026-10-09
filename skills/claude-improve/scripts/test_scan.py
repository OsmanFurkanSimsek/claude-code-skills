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
