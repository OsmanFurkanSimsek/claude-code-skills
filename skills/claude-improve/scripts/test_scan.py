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


def test_a_transcript_removed_during_the_scan_is_skipped(projects, monkeypatch):
    # 2026-10-18: an /insights run removed its own transcript after the listing, and the all-time skill count crashed
    real, gone = scan.glob.glob, str(projects / "projects" / "-work-proj" / "gone.jsonl")
    listing = os.path.join(str(projects / "projects"), "*", "*.jsonl")
    monkeypatch.setattr(scan.glob, "glob", lambda p, *a, **k: real(p, *a, **k) + ([gone] if p == listing else []))
    js = projects / "scan.json"
    monkeypatch.setattr(sys, "argv", ["scan.py", "--since", "2026-10-09 09:00", "--projects-dir", str(projects / "projects"),
                                      "--private-dir", str(projects / "addons"), "--out", str(projects / "scan.md"),
                                      "--json", str(js)])
    scan.main()
    assert json.loads(js.read_text(encoding="utf-8"))["sessions.count"] == 1


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
        user("2026-10-09T10:14:30Z", "Are you still active, or is it waiting for something?"),  # missed until 10-20
        tool("2026-10-09T10:15:00Z", "9", "Gone", {}),
        line(type="user", timestamp="2026-10-09T10:15:01Z", cwd="/work/proj",
             message={"role": "user", "content": [{"type": "tool_result", "tool_use_id": "t9", "is_error": True,
                      "content": "<tool_use_error>Error: No such tool available: Gone</tool_use_error>"}]}),
    ]
    with open(d / "s1.jsonl", "a", encoding="utf-8") as fh:
        fh.write("\n".join(rows) + "\n")
    md, m = run_scan(projects)
    assert m["owner.time_asks.count"] == 3
    assert m["owner.corrections.count"] == 2 and m["owner.corrections.voice.count"] == 1
    assert m["tool.err.no_such_tool.count"] == 1
    assert "Owner asks about the time left: 3. Calls to a tool that does not exist: 1" in md


def test_new_owner_keys_are_zero_when_nothing_matches(projects):
    _, m = run_scan(projects)
    for k in ("owner.time_asks", "owner.corrections", "owner.corrections.voice", "tool.err.no_such_tool",
              "reply.continue_ask_under_28pct"):
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
            user("2026-10-09T10:32:00Z", "the time table is fine"),               # no ask
            user("2026-10-09T10:33:00Z", "are you done working?"),               # missed until 10-21
            user("2026-10-09T10:34:00Z", "are you finished?"),
            user("2026-10-09T10:35:00Z", "are you doneness-checking it"),        # no ask
            user("2026-10-09T10:36:00Z", "are you working?"),                    # missed until 10-22
            user("2026-10-09T10:37:00Z", "are you workingmen")]                  # no ask
    with open(d / "s1.jsonl", "a", encoding="utf-8") as fh:
        fh.write("\n".join(rows) + "\n")
    _, m = run_scan(projects)
    assert m["owner.time_asks.count"] == 5


# ---- ledger CI-43: final replies that ask for "continue" under 28% (rules shared with the review-gate hook) ----
def say(ts, mid, text, tokens, entry="cli"):
    return line(type="assistant", timestamp=ts, cwd="/work/proj", entrypoint=entry,
                message={"id": mid, "model": "m", "content": [{"type": "text", "text": text}],
                         "usage": {"input_tokens": 5, "cache_read_input_tokens": tokens - 5}})


def end_turn(ts):
    return line(type="system", subtype="turn_duration", timestamp=ts, cwd="/work/proj", durationMs=1000)


def steps_reply(last):
    return "## Summary\nB1 is built.\n\n## What you should do\n\n" + last + "\n"


ASK = steps_reply("Nothing to do now. Next, when you type `continue`, I start B2 (tickets and reviews).")


def test_continue_asks_under_28pct_are_counted_on_final_replies(projects):
    d = projects / "projects" / "-work-proj"
    rows = [user("2026-10-09T10:40:00Z", "go"), say("2026-10-09T10:41:00Z", "c1", ASK, 150000),
            end_turn("2026-10-09T10:41:01Z"),                                                   # counted
            user("2026-10-09T10:50:00Z", "go"), say("2026-10-09T10:51:00Z", "c2", ASK, 300000),
            end_turn("2026-10-09T10:51:01Z"),                                                   # 30%: the handoff
            user("2026-10-09T11:00:00Z", "go"),
            say("2026-10-09T11:01:00Z", "c3", steps_reply("Nothing else. Your feedback \"don't ask me to say "
                                                          "continue\" is saved."), 150000),
            end_turn("2026-10-09T11:01:01Z"),                                                   # his words quoted
            user("2026-10-09T11:10:00Z", "go"),
            line(type="assistant", timestamp="2026-10-09T11:10:30Z", cwd="/work/proj",
                 message={"id": "c4", "model": "m", "usage": {"input_tokens": 1000},
                          "content": [{"type": "tool_use", "id": "q1", "name": "AskUserQuestion", "input": {}}]}),
            line(type="user", timestamp="2026-10-09T11:10:40Z", cwd="/work/proj",
                 message={"role": "user", "content": [{"type": "tool_result", "tool_use_id": "q1", "is_error": True,
                                                       "content": "The user doesn't want to proceed with this tool use."}]}),
            say("2026-10-09T11:11:00Z", "c5", ASK, 150000), end_turn("2026-10-09T11:11:01Z"),     # pop-up still open
            user("2026-10-09T11:20:00Z", "go"),
            say("2026-10-09T11:21:00Z", "c6", steps_reply("1. When your usage limit resets, type `continue`."), 150000),
            end_turn("2026-10-09T11:21:01Z"),                                                   # a reason of his own
            user("2026-10-09T11:30:00Z", "go"), say("2026-10-09T11:31:00Z", "c7", ASK, 150000)]   # no turn end yet
    (d / "ci43a-scan-test.jsonl").write_text("\n".join(rows) + "\n", encoding="utf-8")
    sdk = [user("2026-10-09T10:40:00Z", "go"), say("2026-10-09T10:41:00Z", "p1", ASK, 150000, entry="sdk-cli"),
           end_turn("2026-10-09T10:41:01Z")]                                                   # `claude -p`
    (d / "ci43b-scan-test.jsonl").write_text("\n".join(sdk) + "\n", encoding="utf-8")
    md, m = run_scan(projects)
    assert m["reply.continue_ask_under_28pct.count"] == 1
    assert m["reply.continue_ask_under_28pct.per_week"] > 0
    assert ('asked the owner to type "continue" while the context was under 28% (ledger CI-43): 1 - '
            '[proj ci43a-sc 10-09 10:41] 150K "Next, when you type `continue`, I start B2 (tickets and"') in md
    assert "reply.continue_ask_under_28pct.count" not in md            # raw counts live in the --json file only


def test_continue_rules_read_the_turn_like_the_hook():
    rows = [json.loads(say("2026-10-09T10:41:00Z", "c1", "Working on it.", 150000)),
            json.loads(user("2026-10-09T10:42:00Z", "go")), json.loads(say("2026-10-09T10:43:00Z", "c2", ASK, 150000))]
    slim = [scan.slim_row(r) for r in rows]
    assert scan.turn_parts(slim) == [ASK]                              # the turn starts at his message
    assert scan.context_used(slim, "ci43-no-such-session") == (150000, scan.CONT_WINDOW)
    assert scan.continue_hit(scan.turn_parts(slim), slim, "ci43-no-such-session") == (
        150000, "Next, when you type `continue`, I start B2 (tickets and")


# ---- CI-51 follow-up (2026-10-18): the count agrees with the hook's rule 3 and reads past a quoted line ----
STOPPING = "Save everything to the project.md. Tell me when I can close the terminal because I will stop working."


def queued(ts, text):
    return line(type="attachment", timestamp=ts, cwd="/work/proj",
                attachment={"type": "queued_command", "prompt": text, "commandMode": "prompt", "origin": {"kind": "human"}})


def test_continue_after_he_says_he_is_stopping_is_not_counted(projects):
    d = projects / "projects" / "-work-proj"
    rows = [user("2026-10-09T10:40:00Z", "go"), say("2026-10-09T10:41:00Z", "c1", ASK, 150000),
            end_turn("2026-10-09T10:41:01Z"),                                                   # counted
            user("2026-10-09T10:50:00Z", STOPPING), say("2026-10-09T10:51:00Z", "c2", ASK, 150000),
            end_turn("2026-10-09T10:51:01Z"),                                                   # he is stopping
            user("2026-10-09T11:00:00Z", "Build the page."), tool("2026-10-09T11:00:30Z", "c3", "Bash", {"command": "x"}),
            queued("2026-10-09T11:00:40Z", "Bugünlük bu kadar, her şeyi kaydet."),
            say("2026-10-09T11:01:00Z", "c4", ASK, 150000), end_turn("2026-10-09T11:01:01Z"),     # queued while working
            user("2026-10-09T11:10:00Z", "Stop asking me questions and keep going."),
            say("2026-10-09T11:11:00Z", "c5", ASK, 150000), end_turn("2026-10-09T11:11:01Z")]     # no stop: counted
    (d / "ci51b-scan-test.jsonl").write_text("\n".join(rows) + "\n", encoding="utf-8")
    _, m = run_scan(projects)
    assert m["reply.continue_ask_under_28pct.count"] == 2


def test_his_last_message_reads_typed_and_queued_messages_like_the_hook():
    rows = [json.loads(user("2026-10-09T10:40:00Z", STOPPING)), json.loads(say("2026-10-09T10:41:00Z", "c1", "ok", 9))]
    assert scan.his_last_message([scan.slim_row(r) for r in rows]) == STOPPING
    rows += [json.loads(queued("2026-10-09T10:42:00Z", "<command-name>/btw</command-name><command-args>go on with B4"
                                                        "</command-args>"))]
    assert scan.his_last_message([scan.slim_row(r) for r in rows]) == "go on with B4"
    note = json.loads(user("2026-10-09T10:43:00Z", "<task-notification><task-id>a</task-id></task-notification>"))
    assert scan.his_last_message([scan.slim_row(r) for r in rows + [note]]) == "go on with B4"


def test_a_continue_ask_after_a_quoted_line_is_counted():
    quote = steps_reply("1. Read Alex's note:\n> The numbers look right.\n2. Then type `continue` and I write the mail.")
    slim = [scan.slim_row(json.loads(r)) for r in (user("2026-10-09T10:42:00Z", "go"),
                                                    say("2026-10-09T10:43:00Z", "c2", quote, 150000))]
    assert scan.continue_hit(scan.turn_parts(slim), slim, "ci43-no-such-session") == (
        150000, "Then type `continue` and I write the mail.")
    assert scan.NOT_STEP_TEXT.sub("", "> quoted\nx\n```\n> in code\ny\n```\nz") == "\nx\n\nz"
