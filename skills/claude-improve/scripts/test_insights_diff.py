"""Tests for insights_diff.py: a facet is new when it was written after the report the previous review saw, so a
session that ended between two reports is judged once (never skipped, never twice).
Each test builds a throwaway usage-data folder with controlled file times; the real one is never touched."""
import json, os, subprocess, sys, tempfile, time, unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "insights_diff.py")
A, B, C = "2026-10-09 12:00", "2026-10-09 17:00", "2026-10-10 09:00"     # three Last run values = three reviews
T0 = time.time() - 10 * 3600     # base time for file times; one "hour" below = 3600 s


class InsightsDiff(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = self.tmp.name
        self.usage = os.path.join(self.d, "usage-data")
        for sub in ("facets", "session-meta"):
            os.makedirs(os.path.join(self.usage, sub))
        self.state = os.path.join(self.d, "state.json")

    def tearDown(self):
        self.tmp.cleanup()

    def report(self, name, hour):
        p = os.path.join(self.usage, name)
        with open(p, "w", encoding="utf-8") as f:
            f.write("<html><body><p>5 messages across 2 sessions</p></body></html>")
        os.utime(p, (T0 + hour * 3600, T0 + hour * 3600))

    def session(self, sid, last_msg, facet_hour, project="C:/work/app"):
        with open(os.path.join(self.usage, "session-meta", sid + ".json"), "w", encoding="utf-8") as f:
            json.dump({"session_id": sid, "project_path": project, "start_time": last_msg,
                       "user_message_timestamps": [last_msg]}, f)
        if facet_hour is not None:
            p = os.path.join(self.usage, "facets", sid + ".json")
            with open(p, "w", encoding="utf-8") as f:
                json.dump({"outcome": "mostly_achieved", "friction_counts": {"x": 1}, "friction_detail": "detail " + sid}, f)
            os.utime(p, (T0 + facet_hour * 3600, T0 + facet_hour * 3600))

    def run_diff(self, since, *extra):
        out = os.path.join(self.d, "diff.md")
        proc = subprocess.run([sys.executable, "-I", SCRIPT, "--since", since, "--out", out, "--usage-dir", self.usage,
                               "--state", self.state, *extra], capture_output=True, text=True, encoding="utf-8")
        assert proc.returncode == 0, proc.stderr
        return open(out, encoding="utf-8").read()

    def test_first_pass_uses_session_time(self):
        self.report("report-2026-10-09-100000.html", 1)
        self.session("old00000", "2026-10-09T06:00:00Z", 1)       # before A: left out
        self.session("new00000", "2026-10-09T13:00:00Z", 1)       # after A: listed
        out = self.run_diff(A)
        self.assertIn("new00000", out)
        self.assertNotIn("old00000", out)
        self.assertIn("No state yet", out)

    def test_session_between_two_reports_is_judged_once_in_the_next_review(self):
        self.report("report-2026-10-09-100000.html", 1)
        self.session("early000", "2026-10-09T09:00:00Z", 1)        # analysed in report 1
        self.run_diff(A)                                           # review 1 saw report 1
        # a session ends at 15:00 UTC (between review 1 and review 2); report 2 is made later and analyses it
        self.session("gap00000", "2026-10-09T15:00:00Z", 5)
        self.report("report-2026-10-09-200000.html", 5.5)
        out = self.run_diff(B)                                     # review 2
        self.assertIn("gap00000", out)                             # not skipped, although its last message is before B
        self.assertNotIn("early000", out)                          # not twice
        self.assertIn("New /insights analyses since the report the last review saw", out)

    def test_retry_inside_one_review_lists_the_same_facets_again(self):
        self.report("report-2026-10-09-100000.html", 1)
        self.run_diff(A)
        self.session("gap00000", "2026-10-09T15:00:00Z", 5)
        self.report("report-2026-10-09-200000.html", 5.5)
        first = self.run_diff(B)
        again = self.run_diff(B)
        self.assertIn("gap00000", first)
        self.assertIn("gap00000", again)
        self.assertNotIn("gap00000", self.run_diff(C))              # the next review has judged it

    def test_same_report_in_two_reviews_lists_nothing_new(self):
        self.report("report-2026-10-09-100000.html", 1)
        self.session("s0000000", "2026-10-09T13:00:00Z", 1)
        self.run_diff(A)
        self.run_diff(B)
        out = self.run_diff(C)
        self.assertNotIn("s0000000", out)

    def test_seed_marks_the_newest_report_as_seen(self):
        self.report("report-2026-10-09-100000.html", 1)
        self.session("s0000000", "2026-10-09T13:00:00Z", 1)
        self.run_diff(A, "--seed")
        self.assertNotIn("s0000000", self.run_diff(A))

    def test_test_runs_and_no_save(self):
        self.report("report-2026-10-09-100000.html", 1)
        self.session("tmp00000", "2026-10-09T13:00:00Z", 1, project="C:/Users/x/AppData/Local/Temp/claude/scratch")
        out = self.run_diff(A, "--no-save")
        self.assertNotIn("tmp00000", out)
        self.assertFalse(os.path.exists(self.state))


if __name__ == "__main__":
    unittest.main()
