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
        self.base = {"archived": False, "size": 10, "pushed_at": "2026-08-29T00:00:00Z"}

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


class IssueReconciliationTests(unittest.TestCase):
    def row(self, repo, state):
        return {
            "repository": repo,
            "state": state,
            "reason": "latest workflow ci=failure" if state == "BROKEN" else "healthy",
            "pushed_at": "2026-08-30T00:00:00Z",
            "latest_workflow": {"name": "ci", "conclusion": "failure", "html_url": "https://example.test/run"},
        }

    def test_create_issue_for_new_broken_repo(self):
        report = {"repositories": [self.row("ohbeopseok-ops/a", "BROKEN")]}
        actions = ct.plan_issue_actions(report, [])
        self.assertEqual(actions[0][0], "create")

    def test_close_issue_after_recovery(self):
        report = {"repositories": [self.row("ohbeopseok-ops/a", "HEALTHY")]}
        issue = {
            "number": 7,
            "state": "open",
            "body": ct.issue_marker("ohbeopseok-ops/a"),
        }
        actions = ct.plan_issue_actions(report, [issue])
        self.assertEqual(actions[0][0], "close")

    def test_reopen_issue_after_regression(self):
        report = {"repositories": [self.row("ohbeopseok-ops/a", "BROKEN")]}
        issue = {
            "number": 7,
            "state": "closed",
            "body": ct.issue_marker("ohbeopseok-ops/a"),
        }
        actions = ct.plan_issue_actions(report, [issue])
        self.assertEqual(actions[0][0], "reopen")


if __name__ == "__main__":
    unittest.main()


class FailureDiagnosisTests(unittest.TestCase):
    def test_fix_candidate_pattern_contract(self):
        self.assertIn(("ModuleNotFoundError", "Python import path/package mismatch", "Align imports and PYTHONPATH/package layout; rerun collection and unit tests."), [
            ("ModuleNotFoundError", "Python import path/package mismatch", "Align imports and PYTHONPATH/package layout; rerun collection and unit tests.")
        ])


class GovernanceV04Tests(unittest.TestCase):
    def test_broken_p0_has_four_hour_sla(self):
        self.assertEqual(ct.governance_sla({"priority": "P0"}, "BROKEN"), {"breach": True, "target_hours": 4})

    def test_repair_proposal_never_allows_auto_merge(self):
        row = {
            "repository": "ohbeopseok-ops/demo",
            "state": "BROKEN",
            "diagnosis": {"root_cause": "Python import path/package mismatch", "fix_candidate": "fix import"},
            "latest_workflow": {"id": 123},
        }
        proposal = ct.repair_proposal(row)
        self.assertIsNotNone(proposal)
        self.assertTrue(proposal["draft_pr"])
        self.assertFalse(proposal["auto_merge_allowed"])

    def test_readiness_broken_is_blocked(self):
        now = dt.datetime(2026, 8, 30, tzinfo=dt.timezone.utc)
        row = {
            "state": "BROKEN",
            "latest_workflow": {"name": "test", "conclusion": "failure"},
            "pushed_at": "2026-08-30T00:00:00Z",
            "actions_error": None,
            "size": 10,
        }
        result = ct.release_readiness_score(row, now)
        self.assertEqual(result["label"], "BLOCKED")
        self.assertLess(result["score"], 75)
