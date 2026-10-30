import subprocess
import tempfile
import unittest
from pathlib import Path

from pr_validation import (
    find_duplicate_urls,
    normalize_url,
    parse_api_diff,
    read_pr_diff,
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


class RepositoryDiffTests(unittest.TestCase):
    def test_reads_apis_diff_when_called_from_scripts_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            scripts = root / "scripts"
            apis = root / "apis"
            scripts.mkdir()
            apis.mkdir()
            (apis / "example.md").write_text(
                "| API Name | Description | Auth | HTTPS | Link |\\n"
                "| --- | --- | --- | --- | --- |\\n",
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
                    "[Link](https://docs.example.com/api) |\\n"
                )
            subprocess.run(["git", "-C", str(root), "add", "apis"], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-qm", "add API"], check=True)
            head = subprocess.check_output(
                ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
            ).strip()

            paths, diff = read_pr_diff(base, head, root / "scripts")
            self.assertEqual(paths, ["apis/example.md"])
            self.assertIn("https://docs.example.com/api", diff)


if __name__ == "__main__":
    unittest.main()
