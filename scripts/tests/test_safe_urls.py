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

    def read(self, size=-1):
        return b"response body"

    def close(self):
        self.closed = True


class FakeHTTPResponse:
    status = 200

    def __init__(self):
        from email.message import Message
        self.headers = Message()
        self.headers["Content-Type"] = "text/plain; charset=utf-8"

    def read(self, size=-1):
        return b"pinned response"


class FakeHTTPConnection:
    last_instance = None

    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.request_args = None
        FakeHTTPConnection.last_instance = self

    def request(self, method, path, headers=None):
        self.request_args = (method, path, headers or {})

    def getresponse(self):
        return FakeHTTPResponse()

    def close(self):
        pass


class SafeURLTests(unittest.TestCase):
    def setUp(self):
        self.public_resolver = patch(
            "safe_urls.socket.getaddrinfo",
            return_value=[
                (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443)),
            ],
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
        with patch(
            "safe_urls.socket.getaddrinfo",
            return_value=[
                (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443)),
                (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("10.0.0.4", 443)),
            ],
        ):
            with self.assertRaisesRegex(UnsafeURL, "non-public address"):
                validate_public_http_url("https://mixed.example/api")

    def test_nxdomain_has_a_distinct_error_type(self):
        with patch("safe_urls.socket.getaddrinfo", side_effect=socket.gaierror(socket.EAI_NONAME, "Name or service not known")):
            with self.assertRaises(DNSResolutionError):
                resolve_public_addresses("missing.example", 443)

    def test_transient_dns_failure_is_not_misreported_as_nxdomain(self):
        with patch("safe_urls.socket.getaddrinfo", side_effect=socket.gaierror(socket.EAI_AGAIN, "Temporary failure")):
            with self.assertRaisesRegex(UnsafeURL, "inconclusive"):
                validate_public_http_url("https://temporary.example/api")

    def test_default_client_connects_to_the_validated_ip_not_the_hostname(self):
        with patch("safe_urls.http.client.HTTPConnection", FakeHTTPConnection):
            response = safe_get("http://api.example.com/health")

        connection = FakeHTTPConnection.last_instance
        self.assertEqual(connection.host, "93.184.216.34")
        self.assertEqual(connection.port, 80)
        self.assertEqual(connection.request_args[0], "GET")
        self.assertEqual(connection.request_args[1], "/health")
        self.assertEqual(connection.request_args[2]["Host"], "api.example.com")
        self.assertEqual(response.text, "pinned response")

    def test_safe_browser_route_fulfills_from_the_pinned_client(self):
        class FakeRequest:
            url = "https://api.example.com/health"
            method = "GET"
            headers = {"user-agent": "test-agent", "accept": "text/html"}

        class FakeRoute:
            request = FakeRequest()
            fulfilled = None
            aborted = False

            def fulfill(self, **kwargs):
                self.fulfilled = kwargs

            def abort(self):
                self.aborted = True

            def continue_(self):
                raise AssertionError("remote browser request must not bypass the pinned client")

        route = FakeRoute()
        with patch("safe_urls.safe_get", return_value=FakeResponse(200, {"Content-Type": "text/plain"})):
            from safe_urls import safe_browser_route
            safe_browser_route(route)

        self.assertFalse(route.aborted)
        self.assertEqual(route.fulfilled["status"], 200)
        self.assertEqual(route.fulfilled["body"], b"response body")

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
        result = safe_get("https://api.example.com/start", requester=requester)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(calls, [
            "https://api.example.com/start",
            "https://cdn.example.com/final",
        ])


if __name__ == "__main__":
    unittest.main()
