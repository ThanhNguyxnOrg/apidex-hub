import tempfile
import unittest
from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

from shutdown_detection import detect_shutdown_notice
from check_shutdown_signals import parse_documentation_targets


class ShutdownDetectionTests(unittest.TestCase):
    def test_detects_explicit_api_shutdown_notice_in_html(self):
        content = """
        <html><head><title>NewsDataHub has shut down</title></head>
        <body>
          <h1>NewsDataHub has shut down.</h1>
          <p>As of June 5, 2026, we are no longer accepting new requests or subscriptions.</p>
        </body></html>
        """
        signal = detect_shutdown_notice(content)
        self.assertIsNotNone(signal)
        self.assertEqual(signal["type"], "request_intake_closed")
        self.assertIn("no longer accepting new requests", signal["matched_text"].lower())

    def test_detects_provider_shutdown_language(self):
        signal = detect_shutdown_notice("<p>Our API service has been discontinued.</p>")
        self.assertIsNotNone(signal)
        self.assertEqual(signal["type"], "service_shutdown")

    def test_ignores_shutdown_words_in_script_and_style(self):
        content = """
        <style>.banner:after { content: "API has shut down"; }</style>
        <script>const message = "We are no longer accepting new requests";</script>
        <p>Welcome to the developer documentation.</p>
        """
        self.assertIsNone(detect_shutdown_notice(content))

    def test_does_not_treat_local_shutdown_instructions_as_provider_shutdown(self):
        content = "<p>To shut down your local development server, press Ctrl+C.</p>"
        self.assertIsNone(detect_shutdown_notice(content))

    def test_legacy_and_canonical_rows_both_expose_docs_urls(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "news.md").write_text(
                '## <a id="news"></a>📰 News\n'
                '| API Name | Description | Auth | HTTPS | Link |\n'
                '| --- | --- | --- | --- | --- |\n'
                '| **Legacy News** | Example | No | ✅ | [Link](https://docs.example.com/legacy) |\n'
                '| API Name | Description | Auth | HTTPS | API Endpoint | Documentation |\n'
                '| --- | --- | --- | --- | --- | --- |\n'
                '| **Canonical API** | Example | No | ✅ | [Endpoint](https://api.example.com/v1) | [Docs](https://docs.example.com/canonical) |\n'
                '| **Docs Only** | Example | No | ✅ |  | [Docs](https://docs.example.com/only) |\n',
                encoding="utf-8",
            )
            targets = parse_documentation_targets(root)
            urls = {item["url"] for item in targets}
            self.assertEqual(
                urls,
                {
                    "https://docs.example.com/legacy",
                    "https://docs.example.com/canonical",
                    "https://docs.example.com/only",
                },
            )
            self.assertNotIn("https://api.example.com/v1", urls)

    def test_documentation_urls_are_deduplicated_but_keep_all_api_names(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "news.md").write_text(
                '## <a id="news"></a>📰 News\n'
                '| API Name | Description | Auth | HTTPS | Link |\n'
                '| --- | --- | --- | --- | --- |\n'
                '| **Provider API A** | A | No | ✅ | [Link](https://docs.example.com/provider) |\n'
                '| **Provider API B** | B | No | ✅ | [Link](https://docs.example.com/provider) |\n',
                encoding="utf-8",
            )
            targets = parse_documentation_targets(root)
            self.assertEqual(len(targets), 1)
            self.assertEqual(
                {api["name"] for api in targets[0]["apis"]},
                {"Provider API A", "Provider API B"},
            )


if __name__ == "__main__":
    unittest.main()
