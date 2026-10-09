"""Tests for doctor_data.py: the config part is compared with the previous review's last pass, so a later review lists
only what moved, and a retry inside one review (the same Last run) never hides it.
Each test runs the script as a child with USERPROFILE/HOME pointing at a throwaway home folder (never the real one)."""
import json, os, subprocess, sys, tempfile, unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "doctor_data.py")
A, B, C = "2026-10-09 12:00", "2026-10-09 17:00", "2026-10-10 09:00"     # three Last run values = three reviews


def run(home, *extra, since=A):
    env = dict(os.environ, USERPROFILE=home, HOME=home, PYTHONUTF8="1")
    out = os.path.join(home, "out.md")
    proc = subprocess.run([sys.executable, "-I", SCRIPT, out, os.path.join(home, "proj"), since, *extra],
                          capture_output=True, text=True, env=env, encoding="utf-8")
    assert proc.returncode == 0, proc.stderr
    return proc.stdout


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f)


class DoctorData(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = self.tmp.name
        os.makedirs(os.path.join(self.home, "proj"))
        self.settings = os.path.join(self.home, ".claude", "settings.json")
        write_json(self.settings, {"permissions": {"defaultMode": "bypassPermissions"},
                                   "enabledPlugins": {"p1@m": True, "p2@m": False}})
        self.cj = os.path.join(self.home, ".claude.json")
        write_json(self.cj, {"installMethod": "native", "numStartups": 5,
                             "skillUsage": {"s-new": {"usageCount": 0}, "s-busy": {"usageCount": 50}},
                             "pluginUsage": {"p1@m": {"usageCount": 0}}})
        self.state = os.path.join(self.home, ".claude", "claude-improve-doctor-state.json")

    def tearDown(self):
        self.tmp.cleanup()

    def test_first_pass_is_full_and_saves_state(self):
        out = run(self.home)
        self.assertIn("no baseline yet", out)
        self.assertIn("s-busy: 50", out)
        self.assertTrue(os.path.exists(self.state))
        self.assertTrue(os.path.exists(os.path.join(self.home, "out.full.md")))

    def test_same_review_again_is_still_a_first_pass(self):
        run(self.home)
        self.assertIn("no baseline yet", run(self.home))

    def test_later_review_lists_only_what_moved(self):
        run(self.home, since=A)
        out = run(self.home, since=B)
        self.assertIn("- nothing moved", out)
        self.assertNotIn("s-busy", out)
        self.assertNotIn("no baseline", out)

    def test_retry_inside_one_review_does_not_hide_a_change(self):
        run(self.home, since=A)
        write_json(self.settings, {"permissions": {"defaultMode": "acceptEdits"}, "enabledPlugins": {}})
        first = run(self.home, since=B)
        again = run(self.home, since=B)                   # the same review, run a second time
        self.assertIn("acceptEdits", first)
        self.assertIn("acceptEdits", again)
        self.assertIn("nothing moved", run(self.home, since=C))   # the next review starts from what this one saw

    def test_seed_makes_this_pass_the_baseline_for_the_same_review(self):
        run(self.home, "--seed", since=A)
        out = run(self.home, since=A)
        self.assertIn("- nothing moved", out)
        write_json(self.cj, {"installMethod": "npm", "skillUsage": {}, "pluginUsage": {}})
        self.assertIn("installMethod", run(self.home, since=A))

    def test_counter_of_unused_extension_is_listed_busy_one_only_counted(self):
        run(self.home, since=A)
        write_json(self.cj, {"installMethod": "native", "numStartups": 9,
                             "skillUsage": {"s-new": {"usageCount": 3}, "s-busy": {"usageCount": 60}},
                             "pluginUsage": {"p1@m": {"usageCount": 0}}})
        out = run(self.home, since=B)
        self.assertIn("s-new: 0", out)           # old value of the moved counter
        self.assertIn("s-new: 3", out)
        self.assertNotIn("s-busy", out)
        self.assertIn("1 usage counters of extensions already in use moved up", out)
        self.assertNotIn("numStartups", out.split("## transcripts")[0].split("changed since")[1])

    def test_config_change_and_parse_error(self):
        run(self.home, since=A)
        write_json(self.settings, {"permissions": {"defaultMode": "acceptEdits"},
                                   "enabledPlugins": {"p1@m": True, "p2@m": False}})
        self.assertIn("acceptEdits", run(self.home, since=B))
        with open(self.settings, "w") as f:
            f.write("{ broken")
        self.assertIn("PARSE ERROR", run(self.home, since=C).split("## changed")[0])

    def test_enabled_plugin_with_zero_uses_is_listed_every_pass(self):
        ip = os.path.join(self.home, "plug", "p1")
        os.makedirs(os.path.join(ip, "skills", "do-thing"))
        with open(os.path.join(ip, "skills", "do-thing", "SKILL.md"), "w", encoding="utf-8") as f:
            f.write("---\nname: do-thing\ndescription: Does a thing\n---\nbody\n")
        write_json(os.path.join(self.home, ".claude", "plugins", "installed_plugins.json"),
                   {"plugins": {"p1@m": [{"installPath": ip}]}})
        first = run(self.home, since=A)
        self.assertIn("enabled plugins with 0 uses", first)
        self.assertIn("p1@m (", first.split("## changed")[0])
        second = run(self.home, since=B)
        self.assertIn("- nothing moved", second)                       # unchanged config is not re-listed ...
        self.assertIn("p1@m (", second.split("## changed")[0])         # ... but the unused plugin stays on the standing line

    def test_no_save_keeps_the_state(self):
        run(self.home, since=A)
        before = open(self.state, encoding="utf-8").read()
        write_json(self.cj, {"installMethod": "npm", "skillUsage": {}, "pluginUsage": {}})
        out = run(self.home, "--no-save", since=B)
        self.assertIn("installMethod", out)
        self.assertEqual(before, open(self.state, encoding="utf-8").read())

    def test_no_secrets_in_output(self):
        write_json(self.settings, {"env": {"APIFY_TOKEN": "SECRET-VALUE-123"}, "permissions": {}})
        out = run(self.home)
        full = open(os.path.join(self.home, "out.full.md"), encoding="utf-8").read()
        state = open(self.state, encoding="utf-8").read()
        self.assertNotIn("SECRET-VALUE-123", out + full + state)


if __name__ == "__main__":
    unittest.main()
