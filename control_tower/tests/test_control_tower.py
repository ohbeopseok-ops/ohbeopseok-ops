import datetime as dt
import importlib.util
import pathlib
import unittest

MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "control_tower.py"
SPEC = importlib.util.spec_from_file_location("control_tower", MODULE_PATH)
ct = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ct)


class ClassificationTests(unittest.TestCase):
    def setUp(self):
        self.now = dt.datetime(2026, 8, 30, tzinfo=dt.timezone.utc)
        self.base = {
            "archived": False,
            "size": 10,
            "pushed_at": "2026-08-29T00:00:00Z",
        }

    def test_broken_wins_for_nonempty_repo(self):
        state, _ = ct.classify(self.base, {"name": "ci", "conclusion": "failure"}, self.now)
        self.assertEqual(state, "BROKEN")

    def test_empty(self):
        repo = dict(self.base, size=0)
        state, _ = ct.classify(repo, None, self.now)
        self.assertEqual(state, "EMPTY")

    def test_archive(self):
        repo = dict(self.base, archived=True)
        state, _ = ct.classify(repo, None, self.now)
        self.assertEqual(state, "ARCHIVE")

    def test_active(self):
        state, _ = ct.classify(self.base, {"name": "ci", "conclusion": "success"}, self.now)
        self.assertEqual(state, "ACTIVE")

    def test_stale(self):
        repo = dict(self.base, pushed_at="2026-01-01T00:00:00Z")
        state, _ = ct.classify(repo, None, self.now)
        self.assertEqual(state, "STALE")


if __name__ == "__main__":
    unittest.main()
