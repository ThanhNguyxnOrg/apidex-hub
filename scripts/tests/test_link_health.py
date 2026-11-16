import unittest
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

from link_health import classify_http_status, classify_playwright_result


class ApiHealthClassificationTests(unittest.TestCase):
    def test_successful_responses_are_working(self):
        for status in (200, 201, 202, 204, 206):
            with self.subTest(status=status):
                self.assertEqual(classify_http_status(status)[0], "working")

    def test_access_controls_and_rate_limits_are_protected(self):
        for status in (401, 403, 418, 429):
            with self.subTest(status=status):
                state, note = classify_http_status(status)
                self.assertEqual(state, "protected")
                self.assertIn("not confirmed", note)

    def test_client_errors_are_not_counted_as_healthy_or_dead(self):
        for status in (400, 405, 406):
            with self.subTest(status=status):
                self.assertEqual(classify_http_status(status)[0], "unknown")

    def test_only_not_found_and_gone_are_dead_candidates(self):
        self.assertEqual(classify_http_status(404)[0], "broken")
        self.assertEqual(classify_http_status(410)[0], "broken")
        self.assertEqual(classify_http_status(422)[0], "unknown")

    def test_server_failures_are_not_dead(self):
        for status in (500, 502, 503, 504, 520, 527):
            with self.subTest(status=status):
                self.assertIn(classify_http_status(status)[0], {"warning", "error"})

    def test_stage_two_unknown_exception_does_not_preserve_dead_state(self):
        self.assertEqual(
            classify_playwright_result(None, "Playwright Exception: unexpected browser error"),
            "unknown",
        )

    def test_stage_two_dns_nxdomain_is_a_dead_candidate(self):
        self.assertEqual(
            classify_playwright_result(None, "Playwright Exception: DNSResolutionError: hostname does not exist"),
            "broken",
        )

    def test_stage_two_transient_errors_are_inconclusive(self):
        self.assertEqual(classify_playwright_result(None, "Timeout 12000ms exceeded"), "warning")
        self.assertEqual(classify_playwright_result(503, "Cloudflare origin error"), "protected")
        self.assertEqual(classify_playwright_result(502, "Bad gateway"), "error")

    def test_http_200_waf_challenge_is_not_counted_as_working(self):
        self.assertEqual(
            classify_playwright_result(200, "Playwright: WAF challenge detected; endpoint availability is not confirmed"),
            "protected",
        )

    def test_stage_two_confirms_only_explicit_dead_indicators(self):
        self.assertEqual(classify_playwright_result(404, "HTTP 404"), "broken")
        self.assertEqual(classify_playwright_result(410, "HTTP 410"), "broken")
        self.assertEqual(classify_playwright_result(None, "net::ERR_NAME_NOT_RESOLVED"), "broken")

    def test_stage_two_client_errors_are_unknown(self):
        for status in (400, 405, 406):
            with self.subTest(status=status):
                self.assertEqual(classify_playwright_result(status, "HTTP client error"), "unknown")


if __name__ == "__main__":
    unittest.main()
