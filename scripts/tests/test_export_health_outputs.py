import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

from export_health_outputs import append_github_outputs, load_results


class ExportHealthOutputsTests(unittest.TestCase):
    def _write_results(self, root: Path, data: dict) -> Path:
        path = root / "results.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        return path

    def _empty_states(self):
        return {
            "working": [],
            "protected": [],
            "warning": [],
            "error": [],
            "broken": [],
            "unknown": [],
        }

    def test_exports_counts_from_final_stage_two_results(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            reports = root / "reports"
            reports.mkdir()
            (reports / "broken_urls.txt").write_text(
                "https://dead.example/api | Example API - HTTP 404\n",
                encoding="utf-8",
            )
            data = self._empty_states()
            data["working"].append({"url": "https://api.example/ok"})
            data["protected"].append({"url": "https://api.example/locked"})
            data["broken"].append({"url": "https://dead.example/api"})
            results_path = self._write_results(root, data)
            output_path = root / "github-output.txt"

            append_github_outputs(load_results(results_path), reports, output_path)
            output = output_path.read_text(encoding="utf-8")

            self.assertIn("ok_count=1\n", output)
            self.assertIn("protected_count=1\n", output)
            self.assertIn("broken_count=1\n", output)
            self.assertIn("has_broken=true\n", output)
            self.assertIn("https://dead.example/api", output)

    def test_refuses_an_all_zero_scan(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            results_path = self._write_results(root, self._empty_states())
            with self.assertRaisesRegex(ValueError, "zero checked endpoints"):
                load_results(results_path)

    def test_refuses_a_missing_classification_bucket(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            data = self._empty_states()
            del data["unknown"]
            data["working"].append({"url": "https://api.example/ok"})
            results_path = self._write_results(root, data)
            with self.assertRaisesRegex(ValueError, "missing the 'unknown' list"):
                load_results(results_path)

    def test_refuses_result_items_without_endpoint_urls(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            data = self._empty_states()
            data["broken"].append({"name": "Missing URL"})
            results_path = self._write_results(root, data)
            with self.assertRaisesRegex(ValueError, "endpoint URL is required"):
                load_results(results_path)

    def test_missing_text_reports_produce_empty_multiline_outputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            reports = root / "reports"
            reports.mkdir()
            data = self._empty_states()
            data["working"].append({"url": "https://api.example/ok"})
            results_path = self._write_results(root, data)
            output_path = root / "github-output.txt"

            append_github_outputs(load_results(results_path), reports, output_path)
            output = output_path.read_text(encoding="utf-8")
            self.assertIn("broken_list<<APIDEX_", output)
            self.assertIn("unknown_list<<APIDEX_", output)


if __name__ == "__main__":
    unittest.main()
