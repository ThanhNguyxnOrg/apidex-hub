import tempfile
import unittest
from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

from shutdown_detection import detect_shutdown_notice
from check_shutdown_signals import fetch_documentation, parse_documentation_targets
from unittest.mock import patch


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

    def test_documentation_monitor_detects_shutdown_notice_on_http_200(self):
        class FakeResponse:
            headers = {}
            def __enter__(self):
                return self
            def __exit__(self, exc_type, exc, traceback):
                return False
            def read(self, limit):
                return (
                    b"<html><body><h1>Service shutdown</h1>"
                    b"<p>As of June 5, 2026, we are no longer accepting new requests or subscriptions.</p>"
                    b"</body></html>"
                )
            def getcode(self):
                return 200
            def geturl(self):
                return "https://status.example.com/shutdown"

        with patch("check_shutdown_signals.safe_urlopen", return_value=FakeResponse()):
            result = fetch_documentation("https://status.example.com/shutdown")

        self.assertEqual(result["status"], 200)
        self.assertIsNone(result["error"])
        self.assertEqual(result["shutdown_signal"]["type"], "request_intake_closed")

    def test_detects_provider_shutdown_language(self):
        signal = detect_shutdown_notice("<p>Our API service has been discontinued.</p>")
        self.assertIsNotNone(signal)
        self.assertEqual(signal["type"], "service_shutdown")


    def test_legacy_api_retirement_is_informational_not_provider_shutdown(self):
        signal = detect_shutdown_notice(
            "The old file.io API has been retired; use the current upload API instead.",
            documentation_url="https://www.file.io",
            provider_names=["File.io"],
        )
        self.assertIsNotNone(signal)
        self.assertEqual(signal["scope"], "legacy-api")
        self.assertFalse(signal["review_required"])

    def test_named_third_party_service_shutdown_is_not_attributed_to_provider(self):
        signal = detect_shutdown_notice(
            "Since the Mozilla Location Service was decommissioned in 2024, "
            "Linux users can use this endpoint as an alternative.",
            documentation_url="https://ip.app",
            provider_names=["Ip.app"],
        )
        self.assertIsNotNone(signal)
        self.assertEqual(signal["scope"], "external-service-reference")
        self.assertFalse(signal["review_required"])

    def test_worldtimeapi_reference_is_not_attributed_to_timezone_worldtime(self):
        signal = detect_shutdown_notice(
            "Is worldtimeapi.org coming back? Its notice says the service has shut down "
            "and gives no return date.",
            documentation_url="https://www.timezone.io/docs/worldtimeapi",
            provider_names=["Timezone WorldTime"],
        )
        self.assertIsNotNone(signal)
        self.assertEqual(signal["scope"], "external-service-reference")
        self.assertFalse(signal["review_required"])

    def test_current_api_decommission_still_requires_review_near_replacement_link(self):
        signal = detect_shutdown_notice(
            "WARNING - This API will be permanently decommissioned the 12th of April. "
            "For an alternative we recommend using https://geosureglobal.com/.",
            documentation_url="https://raw.githubusercontent.com/amadeus4dev/spec.json",
            provider_names=["Safe Place"],
        )
        self.assertIsNotNone(signal)
        self.assertEqual(signal["scope"], "provider-or-current-api")
        self.assertTrue(signal["review_required"])

    def test_ignores_shutdown_words_in_script_and_style(self):
        content = """
        <style>.banner:after { content: "API has shut down"; }</style>
        <script>const message = "We are no longer accepting new requests";</script>
        <p>Welcome to the developer documentation.</p>
        """
        self.assertIsNone(detect_shutdown_notice(content))

    def test_ignores_unrendered_template_content(self):
        content = "<template><p>Our API service has been discontinued.</p></template>"
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
