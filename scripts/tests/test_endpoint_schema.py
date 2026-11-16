import tempfile
import unittest
from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

import types
sys.modules.setdefault("requests", types.ModuleType("requests"))

from check_links import parse_apis_from_dir
from parse_readme import parse_api_row


class ApiEndpointSchemaTests(unittest.TestCase):
    def test_legacy_five_column_link_is_documentation_only(self):
        row = "| **Legacy API** | Example | No | ✅ | [Link](https://docs.example.com/api) |"
        parsed = parse_api_row(row)
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed["endpoint"], "")
        self.assertEqual(parsed["documentation_url"], "https://docs.example.com/api")
        self.assertEqual(parsed["link"], "https://docs.example.com/api")

    def test_six_column_row_preserves_blank_endpoint_and_documentation(self):
        row = "| **Unverified API** | Example | OAuth | ✅ |  | [Docs](https://docs.example.com/api) |"
        parsed = parse_api_row(row)
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed["endpoint"], "")
        self.assertEqual(parsed["documentation_url"], "https://docs.example.com/api")

    def test_six_column_row_parses_endpoint_separately_from_documentation(self):
        row = "| **Verified API** | Example | OAuth | ✅ | [Endpoint](https://api.example.com/v1/items) | [Docs](https://docs.example.com/api) |"
        parsed = parse_api_row(row)
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed["endpoint"], "https://api.example.com/v1/items")
        self.assertEqual(parsed["documentation_url"], "https://docs.example.com/api")
        self.assertEqual(parsed["link"], "https://docs.example.com/api")

    def test_protected_responses_are_not_reported_as_confirmed_healthy(self):
        root = Path(__file__).resolve().parents[2]
        checker = (root / "scripts" / "check_links.py").read_text(encoding="utf-8")
        health = (root / "scripts" / "link_health.py").read_text(encoding="utf-8")
        verifier = (root / "scripts" / "verify_links_playwright.py").read_text(encoding="utf-8")
        workflow = (root / ".github" / "workflows" / "link-checker.yml").read_text(encoding="utf-8")

        self.assertIn("Confirmed successful responses:", checker)
        self.assertIn("Protected/inconclusive responses:", checker)
        self.assertNotIn("APIs still work", checker)
        self.assertIn("availability is not confirmed", health)
        self.assertIn("not treated as confirmed working or dead", verifier)
        self.assertIn("availability not confirmed", workflow)
        self.assertIn("these do not count as confirmed healthy", workflow)
        self.assertNotIn("HTTP 403/429 — bot protection (API still works)", workflow)

    def test_health_checker_never_probes_legacy_or_documentation_only_rows(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "finance.md").write_text(
                '## <a id="finance"></a>💰 Finance\n\n'
                "| API Name | Description | Auth | HTTPS | Link |\n"
                "| --- | --- | --- | --- | --- |\n"
                "| **Legacy API** | Example | No | ✅ | [Link](https://docs.example.com/legacy) |\n"
                "| API Name | Description | Auth | HTTPS | API Endpoint | Documentation |\n"
                "| --- | --- | --- | --- | --- | --- |\n"
                "| **No Endpoint** | Example | OAuth | ✅ |  | [Docs](https://docs.example.com/only-docs) |\n"
                "| **Has Endpoint** | Example | OAuth | ✅ | [Endpoint](https://api.example.com/v1) | [Docs](https://docs.example.com/endpoint) |\n",
                encoding="utf-8",
            )
            entries = parse_apis_from_dir(str(root))
            self.assertEqual(len(entries), 1)
            self.assertEqual(entries[0]["name"], "Has Endpoint")
            self.assertEqual(entries[0]["url"], "https://api.example.com/v1")
            self.assertEqual(entries[0]["documentation_url"], "https://docs.example.com/endpoint")


if __name__ == "__main__":
    unittest.main()
