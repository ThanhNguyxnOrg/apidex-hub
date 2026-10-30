import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))
import remove_dead_links


class RemoveDeadLinksSafetyTests(unittest.TestCase):
    def test_file_removal_defaults_to_dry_run(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            api_file = root / "example.md"
            original = (
                "| API Name | Description | Auth | HTTPS | Link |\n"
                "| --- | --- | --- | --- | --- |\n"
                "| **Example API** | Example | No | ✅ | [Link](https://dead.example/docs) |\n"
            )
            api_file.write_text(original, encoding="utf-8")

            removed = remove_dead_links.remove_dead_links_from_file(
                api_file,
                {"https://dead.example/docs"},
                {"https://dead.example/docs"},
            )

            self.assertEqual(len(removed), 1)
            self.assertEqual(api_file.read_text(encoding="utf-8"), original)

    def _run_cli(self, root: Path, args: list[str]):
        scripts = root / "scripts"
        apis = root / "apis"
        scripts.mkdir(exist_ok=True)
        apis.mkdir(exist_ok=True)
        (scripts / "remove_dead_links.py").write_text(
            (SCRIPTS_DIR / "remove_dead_links.py").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        report = scripts / "broken_urls.txt"
        report.write_text(
            "https://dead.example/docs | Example API - HTTP 404\n",
            encoding="utf-8",
        )
        return subprocess.run(
            [sys.executable, str(scripts / "remove_dead_links.py"), "--report", str(report),
             "--apis-dir", str(apis), *args],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_cli_does_not_modify_catalog_without_apply_flag(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            apis = root / "apis"
            apis.mkdir()
            api_file = apis / "example.md"
            original = (
                "| API Name | Description | Auth | HTTPS | Link |\n"
                "| --- | --- | --- | --- | --- |\n"
                "| **Example API** | Example | No | ✅ | [Link](https://dead.example/docs) |\n"
            )
            api_file.write_text(original, encoding="utf-8")

            result = self._run_cli(root, [])

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(api_file.read_text(encoding="utf-8"), original)
            self.assertIn("dry-run", result.stdout.lower())

    def test_safety_brake_counts_rows_before_any_file_is_modified(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            apis = root / "apis"
            apis.mkdir()
            api_file = apis / "example.md"
            original = (
                "| API Name | Description | Auth | HTTPS | Link |\n"
                "| --- | --- | --- | --- | --- |\n"
                "| **Example API A** | A | No | ✅ | [Link](https://dead.example/docs) |\n"
                "| **Example API B** | B | No | ✅ | [Link](https://dead.example/docs) |\n"
            )
            api_file.write_text(original, encoding="utf-8")

            result = self._run_cli(root, ["--apply", "--max-delete", "1"])

            self.assertEqual(result.returncode, 2)
            self.assertIn("SAFETY BRAKE", result.stderr)
            self.assertEqual(api_file.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
