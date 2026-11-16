import socket
import sys
from pathlib import Path
import unittest
from unittest.mock import patch

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

from safe_urls import DNSResolutionError, UnsafeURL, resolve_public_addresses, safe_get, validate_public_http_url


class FakeResponse:
    def __init__(self, status_code, headers=None):
        self.status_code = status_code
        self.headers = headers or {}
        self.closed = False

    def close(self):
        self.closed = True


class SafeURLTests(unittest.TestCase):
    def setUp(self):
        self.public_resolver = patch(
            "safe_urls.resolve_public_addresses",
            return_value=("93.184.216.34",),
        )
        self.public_resolver.start()
        self.addCleanup(self.public_resolver.stop)

    def test_accepts_public_http_and_https(self):
        self.assertEqual(
            validate_public_http_url("https://api.example.com/v1"),
            "https://api.example.com/v1",
        )
        self.assertEqual(
            validate_public_http_url("http://api.example.com/v1"),
            "http://api.example.com/v1",
        )

    def test_rejects_non_http_schemes_and_credentials(self):
        for url in (
            "file:///etc/passwd",
            "ftp://example.com/file",
            "https://user:pass@example.com/api",
            "https:///missing-host",
        ):
            with self.subTest(url=url):
                with self.assertRaises(UnsafeURL):
                    validate_public_http_url(url)

    def test_rejects_loopback_private_link_local_and_reserved_ip_literals(self):
        for address in (
            "127.0.0.1",
            "10.0.0.8",
            "172.16.0.10",
            "192.168.1.10",
            "169.254.169.254",
            "::1",
            "fc00::1",
            "fe80::1",
        ):
            with self.subTest(address=address):
                with self.assertRaises(UnsafeURL):
                    validate_public_http_url("http://[" + address + "]" if ":" in address else "http://" + address)

    def test_rejects_local_and_reserved_hostnames(self):
        for hostname in (
            "localhost",
            "printer.local",
            "metadata.google.internal",
            "router.home.arpa",
            "example.test",
        ):
            with self.subTest(hostname=hostname):
                with self.assertRaises(UnsafeURL):
                    validate_public_http_url("https://" + hostname + "/")

    def test_rejects_hostnames_with_any_non_public_dns_answer(self):
        with patch("safe_urls.resolve_public_addresses", return_value=("93.184.216.34", "10.0.0.4")):
            with self.assertRaisesRegex(UnsafeURL, "non-public address"):
                validate_public_http_url("https://mixed.example/api")

    def test_nxdomain_has_a_distinct_error_type(self):
        with patch("safe_urls.socket.getaddrinfo", side_effect=socket.gaierror(socket.EAI_NONAME, "Name or service not known")):
            with self.assertRaises(DNSResolutionError):
                resolve_public_addresses("missing.example", 443)

    def test_rejects_dns_failure(self):
        with patch("safe_urls.resolve_public_addresses", side_effect=socket.gaierror("NXDOMAIN")):
            with self.assertRaises(UnsafeURL):
                validate_public_http_url("https://missing.example/api")

    def test_safe_get_checks_redirect_destinations(self):
        responses = [
            FakeResponse(302, {"Location": "http://127.0.0.1/admin"}),
        ]
        def requester(*args, **kwargs):
            return responses.pop(0)
        with self.assertRaises(UnsafeURL):
            safe_get("https://api.example.com/start", requester=requester)
        self.assertTrue(responses == [])

    def test_safe_get_follows_only_public_redirects(self):
        responses = [
            FakeResponse(302, {"Location": "https://cdn.example.com/final"}),
            FakeResponse(200),
        ]
        calls = []
        def requester(url, **kwargs):
            calls.append(url)
            return responses.pop(0)
        with patch("safe_urls.resolve_public_addresses", return_value=("93.184.216.34",)):
            result = safe_get("https://api.example.com/start", requester=requester)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(calls, [
            "https://api.example.com/start",
            "https://cdn.example.com/final",
        ])


if __name__ == "__main__":
    unittest.main()
