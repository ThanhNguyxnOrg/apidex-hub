import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

from pr_validation import (
    classify_link_result,
    find_duplicate_urls,
    normalize_url,
    parse_api_diff,
    read_pr_diff,
    select_pr_urls_to_validate,
)


class ApiDiffParsingTests(unittest.TestCase):
    def test_extracts_only_official_link_column(self):
        diff = """diff --git a/apis/example.md b/apis/example.md
--- a/apis/example.md
+++ b/apis/example.md
@@ -1,0 +2 @@
+| **Example API** | Supports links like https://description.example | No | ✅ | [Link](https://docs.example.com/api) |
"""
        added, removed, malformed = parse_api_diff(diff)
        self.assertEqual(added, ["https://docs.example.com/api"])
        self.assertEqual(removed, [])
        self.assertEqual(malformed, [])

    def test_rejects_added_data_row_without_official_link(self):
        diff = """diff --git a/apis/example.md b/apis/example.md
--- a/apis/example.md
+++ b/apis/example.md
@@ -1,0 +2 @@
+| **Broken Entry** | Has no official link | No | ✅ | N/A |
"""
        added, removed, malformed = parse_api_diff(diff)
        self.assertEqual(added, [])
        self.assertEqual(removed, [])
        self.assertEqual(len(malformed), 1)

    def test_ignores_markdown_header_and_separator(self):
        diff = """diff --git a/apis/example.md b/apis/example.md
--- a/apis/example.md
+++ b/apis/example.md
@@ -1,0 +2,2 @@
+| API Name | Description | Auth | HTTPS | Link |
+| :--- | :--- | :---: | :---: | :---: |
"""
        added, removed, malformed = parse_api_diff(diff)
        self.assertEqual((added, removed, malformed), ([], [], []))

    def test_removed_url_is_not_reported_as_duplicate_when_moved(self):
        duplicates = find_duplicate_urls(
            added_urls=["https://docs.example.com/api"],
            removed_urls=["https://docs.example.com/api/"],
            existing_urls=["https://docs.example.com/api"],
        )
        self.assertEqual(duplicates, [])

    def test_detects_duplicate_against_existing_service_url(self):
        duplicates = find_duplicate_urls(
            added_urls=["https://docs.example.com/api/"],
            removed_urls=[],
            existing_urls=["https://docs.example.com/api"],
        )
        self.assertEqual(duplicates, ["https://docs.example.com/api/"])

    def test_still_detects_duplicate_when_only_one_of_two_existing_rows_is_removed(self):
        duplicates = find_duplicate_urls(
            added_urls=["https://docs.example.com/api"],
            removed_urls=["https://docs.example.com/api"],
            existing_urls=["https://docs.example.com/api", "https://docs.example.com/api/"],
        )
        self.assertEqual(duplicates, ["https://docs.example.com/api"])

    def test_detects_duplicate_added_twice_in_same_pr(self):
        duplicates = find_duplicate_urls(
            added_urls=[
                "https://docs.example.com/api",
                "https://docs.example.com/api/",
            ],
            removed_urls=[],
            existing_urls=[],
        )
        self.assertEqual(len(duplicates), 1)

    def test_normalizes_host_case_and_trailing_slash_but_preserves_query(self):
        self.assertEqual(
            normalize_url("HTTPS://Docs.Example.com/API/?version=2#overview"),
            "https://docs.example.com/API?version=2",
        )
        self.assertNotEqual(
            normalize_url("https://docs.example.com/api?v=1"),
            normalize_url("https://docs.example.com/api?v=2"),
        )

    def test_only_confirmed_not_found_and_dns_are_broken(self):
        self.assertEqual(classify_link_result(404), "broken")
        self.assertEqual(classify_link_result(410), "broken")
        self.assertEqual(classify_link_result(None, "net::ERR_NAME_NOT_RESOLVED"), "broken")

    def test_access_controls_and_transient_responses_are_inconclusive(self):
        for status in (401, 403, 418, 429, 500, 502, 503, 504, None):
            with self.subTest(status=status):
                self.assertEqual(classify_link_result(status, "temporary failure"), "inconclusive")

    def test_successful_http_status_is_working(self):
        self.assertEqual(classify_link_result(200), "working")
        self.assertEqual(classify_link_result(302), "working")


class RepositoryDiffTests(unittest.TestCase):
    def test_requires_both_commit_refs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            with self.assertRaisesRegex(RuntimeError, "Both base and head"):
                read_pr_diff("", "HEAD", root)

    def test_reads_apis_diff_when_called_from_scripts_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            scripts = root / "scripts"
            apis = root / "apis"
            scripts.mkdir()
            apis.mkdir()
            (apis / "example.md").write_text(
                "| API Name | Description | Auth | HTTPS | Link |\n"
                "| --- | --- | --- | --- | --- |\n",
                encoding="utf-8",
            )
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.com"], check=True)
            subprocess.run(["git", "-C", str(root), "add", "apis"], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-qm", "base"], check=True)
            base = subprocess.check_output(
                ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
            ).strip()

            with (apis / "example.md").open("a", encoding="utf-8") as file:
                file.write(
                    "| **Example API** | Example | No | ✅ | "
                    "[Link](https://docs.example.com/api) |\n"
                )
            subprocess.run(["git", "-C", str(root), "add", "apis"], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-qm", "add API"], check=True)
            head = subprocess.check_output(
                ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
            ).strip()

            paths, diff = read_pr_diff(base, head, scripts)
            self.assertEqual(paths, ["apis/example.md"])
            self.assertIn("https://docs.example.com/api", diff)


class AutomatedRemovalValidationTests(unittest.TestCase):
    def test_removed_urls_are_revalidated_only_for_agent_remediation_prs(self):
        added, removed = select_pr_urls_to_validate(
            ["https://docs.example.com/new"],
            ["https://docs.example.com/dead"],
            validate_removals=False,
        )
        self.assertEqual(added, ["https://docs.example.com/new"])
        self.assertEqual(removed, [])

        added, removed = select_pr_urls_to_validate(
            ["https://docs.example.com/new"],
            ["https://docs.example.com/dead"],
            validate_removals=True,
        )
        self.assertEqual(added, ["https://docs.example.com/new"])
        self.assertEqual(removed, ["https://docs.example.com/dead"])

    def test_a_url_moved_in_the_same_pr_is_validated_as_an_addition(self):
        added, removed = select_pr_urls_to_validate(
            ["https://docs.example.com/api/"],
            ["https://docs.example.com/api"],
            validate_removals=True,
        )
        self.assertEqual(added, ["https://docs.example.com/api/"])
        self.assertEqual(removed, [])

class LinkCheckerWorkflowSafetyTests(unittest.TestCase):
    def setUp(self):
        self.workflow = (
            Path(__file__).resolve().parents[2] / ".github" / "workflows" / "link-checker.yml"
        ).read_text(encoding="utf-8")

    def test_untrusted_report_values_are_passed_through_environment(self):
        self.assertIn("BROKEN_LIST: ${{ steps.check.outputs.broken_list }}", self.workflow)
        self.assertIn("const list = String(process.env.BROKEN_LIST || '').trim();", self.workflow)
        self.assertIn("const currentBrokenList = String(process.env.BROKEN_LIST || '').trim();", self.workflow)
        self.assertNotIn("const list = `${{ steps.check.outputs.broken_list }}`.trim();", self.workflow)
        self.assertNotIn("const currentBrokenList = `${{ steps.check.outputs.broken_list }}`.trim();", self.workflow)

    def test_bot_cleanup_prs_revalidate_removals_and_refresh_from_latest_main_scan(self):
        checker = (
            Path(__file__).resolve().parents[2] / "scripts" / "check_pr_links.py"
        ).read_text(encoding="utf-8")
        self.assertIn("APIDEX_VALIDATE_REMOVALS: ${{ startsWith(github.head_ref, 'agent-remediation/dead-api-incident-') }}", self.workflow)
        self.assertIn('validate_removals = os.environ.get("APIDEX_VALIDATE_REMOVALS", "").strip().lower() == "true"', checker)
        self.assertIn('urls_to_check = added_to_check + removed_to_check', checker)
        self.assertIn('if state == "broken":', checker)
        self.assertIn('git reset --hard origin/main', self.workflow)
        self.assertIn('git push --force-with-lease=', self.workflow)
        self.assertNotIn('git push origin main', self.workflow)
    def test_incident_reference_and_safety_cap_survive_pr_body_rendering(self):
        self.assertIn(r"match(/Closes\s+#(\d+)/i)", self.workflow)
        self.assertIn(r"\`--max-delete 500\`", self.workflow)

    def test_github_script_report_variables_are_at_step_scope_not_action_inputs(self):
        self.assertIn(
            "        uses: actions/github-script@v7\\n"
            "        env:\\n"
            "          BROKEN_COUNT: ${{ steps.check.outputs.broken_count }}\\n"
            "          BROKEN_LIST: ${{ steps.check.outputs.broken_list }}\\n"
            "        with:\\n"
            "          github-token: ${{ steps.app-token.outputs.token }}\\n"
            "          script: |",
            self.workflow,
        )
        self.assertIn(
            "        uses: actions/github-script@v7\\n"
            "        env:\\n"
            "          HAS_BROKEN: ${{ steps.check.outputs.has_broken }}\\n"
            "          ALREADY_RESOLVED: ${{ steps.auto-remediate.outputs.no_changes }}\\n"
            "        with:\\n"
            "          github-token: ${{ steps.app-token.outputs.token }}\\n"
            "          script: |",
            self.workflow,
        )
        self.assertNotIn(
            "        with:\\n"
            "          github-token: ${{ steps.app-token.outputs.token }}\\n"
            "          env:\\n",
            self.workflow,
        )

class DivergentHistoryTests(unittest.TestCase):
    def test_main_only_api_additions_are_not_misread_as_cleanup_deletions(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            apis = root / "apis"
            apis.mkdir()
            catalog = apis / "catalog.md"
            catalog.write_text(
                "| Dead API | Example | No | ✅ | [Link](https://dead.example.com) |\n"
                "| Stable API | Example | No | ✅ | [Link](https://stable.example.com) |\n",
                encoding="utf-8",
            )
            subprocess.run(["git", "init", "-q", "-b", "main", str(root)], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.com"], check=True)
            subprocess.run(["git", "-C", str(root), "add", "apis"], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-qm", "base"], check=True)

            subprocess.run(["git", "-C", str(root), "checkout", "-qb", "cleanup"], check=True)
            catalog.write_text(
                "| Stable API | Example | No | ✅ | [Link](https://stable.example.com) |\n",
                encoding="utf-8",
            )
            subprocess.run(["git", "-C", str(root), "add", "apis"], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-qm", "remove dead API"], check=True)

            subprocess.run(["git", "-C", str(root), "checkout", "main"], check=True)
            with catalog.open("a", encoding="utf-8") as file:
                file.write("| Healthy New API | Example | No | ✅ | [Link](https://healthy.example.com) |\n")
            subprocess.run(["git", "-C", str(root), "add", "apis"], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-qm", "add healthy API on main"], check=True)

            paths, diff = read_pr_diff("main", "cleanup", root)
            added, removed, malformed = parse_api_diff(diff)
            self.assertEqual(paths, ["apis/catalog.md"])
            self.assertEqual(added, [])
            self.assertEqual(removed, ["https://dead.example.com"])
            self.assertNotIn("https://healthy.example.com", removed)
            self.assertEqual(malformed, [])


if __name__ == "__main__":
    unittest.main()
