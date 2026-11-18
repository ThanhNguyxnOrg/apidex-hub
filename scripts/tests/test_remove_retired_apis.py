import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

from remove_retired_apis import apply_retirements, plan_retirements


class RetiredApiRemediationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "apis"
        self.root.mkdir()
        self.file = self.root / "identity.md"

    def tearDown(self):
        self.temp.cleanup()

    def report(self, *, name="Safe Place", docs="https://docs.example.com/safe", status=200,
               scope="provider-or-current-api", review=True, apis=None, signal_type="service_shutdown"):
        return {
            "shutdown_signals": [{
                "url": docs,
                "status": status,
                "error": None,
                "shutdown_signal": {
                    "type": signal_type,
                    "scope": scope,
                    "review_required": review,
                    "matched_text": "API will be permanently decommissioned",
                },
                "apis": apis if apis is not None else [{
                    "name": name, "file": "identity.md", "line": 3, "category": "Identity"
                }],
            }]
        }

    def test_removes_exact_legacy_five_column_row_and_preserves_neighbors(self):
        self.file.write_text(
            "## Identity\n"
            "| API Name | Description | Auth | HTTPS | Link |\n"
            "| **Safe Place** | Retired API | ApiKey | ✅ | [Docs](https://docs.example.com/safe) |\n"
            "| **Still Active** | Active API | No | ✅ | [Docs](https://docs.example.com/active) |\n",
            encoding="utf-8",
        )
        plan = plan_retirements(self.report(), self.root)
        self.assertEqual(len(plan), 1)
        self.assertEqual(plan[0]["line"], 3)
        applied = apply_retirements(plan, apis_dir=self.root)
        self.assertEqual(len(applied), 1)
        content = self.file.read_text(encoding="utf-8")
        self.assertNotIn("Safe Place", content)
        self.assertIn("Still Active", content)

    def test_removes_canonical_six_column_row_using_documentation_column(self):
        self.file.write_text(
            "## Identity\n"
            "| API Name | Description | Auth | HTTPS | API Endpoint | Documentation |\n"
            "| **Safe Place** | Retired API | ApiKey | ✅ | [Endpoint](https://api.example.com/v1) | [Docs](https://docs.example.com/safe) |\n",
            encoding="utf-8",
        )
        plan = plan_retirements(self.report(), self.root)
        self.assertEqual(len(plan), 1)
        apply_retirements(plan, apis_dir=self.root)
        self.assertNotIn("Safe Place", self.file.read_text(encoding="utf-8"))

    def test_rejects_shared_documentation_url_for_multiple_apis(self):
        self.file.write_text("| **Safe Place** | A | No | ✅ | [Docs](https://docs.example.com/safe) |\n", encoding="utf-8")
        report = self.report(apis=[
            {"name": "Safe Place", "file": "identity.md", "line": 1},
            {"name": "Other API", "file": "identity.md", "line": 2},
        ])
        with self.assertRaisesRegex(ValueError, "exactly one"):
            plan_retirements(report, self.root)

    def test_rejects_protected_or_inconclusive_documentation_fetch(self):
        self.file.write_text("| **Safe Place** | A | No | ✅ | [Docs](https://docs.example.com/safe) |\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "not conclusive"):
            plan_retirements(self.report(status=403), self.root)

    def test_rejects_external_or_legacy_scope(self):
        self.file.write_text("| **Safe Place** | A | No | ✅ | [Docs](https://docs.example.com/safe) |\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "did not mark"):
            plan_retirements(self.report(scope="external-service-reference", review=False), self.root)

    def test_rejects_unrecognized_or_missing_explicit_signal(self):
        self.file.write_text("| **Safe Place** | A | No | ✅ | [Docs](https://docs.example.com/safe) |\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "explicit lifecycle phrase"):
            plan_retirements(self.report(signal_type="unknown", review=True), self.root)

    def test_rejects_non_unique_or_missing_row_match(self):
        self.file.write_text(
            "| **Safe Place** | A | No | ✅ | [Docs](https://docs.example.com/other) |\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ValueError, "found 0"):
            plan_retirements(self.report(), self.root)

    def test_rejects_catalog_path_escape(self):
        self.file.write_text("| **Safe Place** | A | No | ✅ | [Docs](https://docs.example.com/safe) |\n", encoding="utf-8")
        report = self.report(apis=[{"name": "Safe Place", "file": "../README.md", "line": 1}])
        with self.assertRaisesRegex(ValueError, "escapes"):
            plan_retirements(report, self.root)

    def test_safety_cap_prevents_all_writes(self):
        self.file.write_text(
            "| **Safe Place** | A | No | ✅ | [Docs](https://docs.example.com/safe) |\n",
            encoding="utf-8",
        )
        plan = plan_retirements(self.report(), self.root)
        oversized = plan + [dict(plan[0], line=2)]
        with self.assertRaisesRegex(ValueError, "Safety brake"):
            apply_retirements(oversized, apis_dir=self.root, max_delete=1)
        self.assertIn("Safe Place", self.file.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
