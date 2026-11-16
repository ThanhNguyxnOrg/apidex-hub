"""DNS-pinned public HTTP clients for repository-controlled URL checks.

Every request resolves the destination, rejects all non-public DNS answers, and
connects to one validated IP literal. HTTP Host and TLS SNI/certificate validation
continue to use the original hostname. Redirects are followed manually and each
new destination is resolved and pinned independently.
"""
from __future__ import annotations

import http.client
import ipaddress
import socket
import ssl
from urllib.error import URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import Request


class UnsafeURL(ValueError):
    """Raised when a URL is malformed or points at a non-public destination."""


class DNSResolutionError(UnsafeURL):
    """Raised when a public hostname does not exist in DNS."""


_BLOCKED_SUFFIXES = (
    ".localhost", ".local", ".internal", ".lan",
    ".home", ".home.arpa", ".test", ".invalid",
)
_REDIRECT_CODES = {301, 302, 303, 307, 308}
_MAX_RESPONSE_BYTES = 2 * 1024 * 1024


def resolve_public_addresses(host: str, port: int) -> tuple[str, ...]:
    """Resolve a host and reject the whole destination if any answer is non-public."""
    try:
        records = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    except socket.gaierror as error:
        permanent_codes = {
            getattr(socket, "EAI_NONAME", None),
            getattr(socket, "EAI_NODATA", None),
        }
        if error.errno in permanent_codes:
            raise DNSResolutionError(f"Hostname does not exist in DNS: {host}") from error
        raise UnsafeURL(f"DNS lookup was inconclusive for {host}: {error}") from error

    addresses = tuple(sorted({record[4][0].split("%", 1)[0] for record in records}))
    if not addresses:
        raise DNSResolutionError(f"Hostname did not resolve: {host}")

    for address in addresses:
        try:
            parsed_address = ipaddress.ip_address(address)
        except ValueError as error:
            raise UnsafeURL(f"Resolver returned an invalid IP for {host}") from error
        if not parsed_address.is_global:
            raise UnsafeURL(
                f"Hostname {host} resolves to a non-public address: {parsed_address}"
            )

    return addresses


def _parse_public_url(url: str) -> tuple[str, str, int, str, str]:
    if not isinstance(url, str) or not url.strip():
        raise UnsafeURL("URL must be a non-empty string")

    value = url.strip()
    try:
        parts = urlsplit(value)
        scheme = parts.scheme.lower()
        hostname = parts.hostname
        port = parts.port
    except ValueError as error:
        raise UnsafeURL(f"Malformed URL: {error}") from error

    if scheme not in {"http", "https"}:
        raise UnsafeURL(f"Only HTTP(S) URLs are allowed: {scheme or 'missing scheme'}")
    if not hostname:
        raise UnsafeURL("URL must contain a hostname")
    if parts.username is not None or parts.password is not None:
        raise UnsafeURL("URLs containing username/password credentials are not allowed")

    host = hostname.rstrip(".").lower()
    if not host or host == "localhost" or any(host.endswith(suffix) for suffix in _BLOCKED_SUFFIXES):
        raise UnsafeURL(f"Local or reserved hostname is not allowed: {host}")

    try:
        ip_literal = ipaddress.ip_address(host)
    except ValueError:
        ip_literal = None

    target_port = port or (443 if scheme == "https" else 80)
    if ip_literal is not None:
        if not ip_literal.is_global:
            raise UnsafeURL(f"Non-public IP address is not allowed: {ip_literal}")
        addresses = (str(ip_literal),)
        tls_name = str(ip_literal)
    else:
        try:
            ascii_host = host.encode("idna").decode("ascii")
        except UnicodeError as error:
            raise UnsafeURL(f"Invalid internationalized hostname: {host}") from error
        addresses = resolve_public_addresses(ascii_host, target_port)
        tls_name = ascii_host

    path = parts.path or "/"
    if parts.query:
        path += "?" + parts.query
    host_header = parts.netloc
    return scheme, host, target_port, path, addresses[0] + "|" + tls_name + "|" + host_header


def validate_public_http_url(url: str) -> str:
    """Validate HTTP(S) and require every DNS answer to be globally routable."""
    _parse_public_url(url)
    return url.strip()


class _PinnedHTTPSConnection(http.client.HTTPSConnection):
    """HTTPS connection to a pinned IP while validating TLS against the URL hostname."""

    def __init__(self, hostname: str, port: int, connect_ip: str, timeout: int):
        super().__init__(hostname, port, timeout=timeout, context=ssl.create_default_context())
        self._connect_ip = connect_ip
        self._tls_hostname = hostname

    def connect(self) -> None:
        raw_socket = socket.create_connection(
            (self._connect_ip, self.port),
            self.timeout,
            self.source_address,
        )
        self.sock = self._context.wrap_socket(
            raw_socket,
            server_hostname=self._tls_hostname,
        )


class SafeResponse:
    """Small requests/urllib-compatible response wrapper backed by a bounded body."""

    def __init__(self, status: int, headers, body: bytes, url: str):
        self.status_code = status
        self.headers = headers
        self._body = body
        self.url = url
        self._closed = False

    @property
    def text(self) -> str:
        charset = None
        try:
            charset = self.headers.get_content_charset()
        except AttributeError:
            pass
        if not charset:
            charset = "utf-8"
        try:
            return self._body.decode(charset, errors="replace")
        except LookupError:
            return self._body.decode("utf-8", errors="replace")

    def read(self, size: int = -1) -> bytes:
        return self._body if size is None or size < 0 else self._body[:size]

    def getcode(self) -> int:
        return self.status_code

    def geturl(self) -> str:
        return self.url

    def close(self) -> None:
        self._closed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return False


def _request_pinned(
    url: str,
    *,
    headers: dict | None,
    timeout: int,
    method: str = "GET",
) -> SafeResponse:
    scheme, host, port, path, packed = _parse_public_url(url)
    connect_ip, tls_hostname, host_header = packed.split("|", 2)

    request_headers = dict(headers or {})
    request_headers["Host"] = host_header
    request_headers["Connection"] = "close"
    request_headers["Accept-Encoding"] = "identity"

    if scheme == "https":
        connection = _PinnedHTTPSConnection(tls_hostname, port, connect_ip, timeout)
    else:
        connection = http.client.HTTPConnection(connect_ip, port, timeout=timeout)

    try:
        connection.request(method, path, headers=request_headers)
        response = connection.getresponse()
        body = response.read(_MAX_RESPONSE_BYTES)
        result = SafeResponse(response.status, response.headers, body, url)
        return result
    except (OSError, http.client.HTTPException, ssl.SSLError) as error:
        import requests
        raise requests.RequestException(
            f"{type(error).__name__}: {error}"
        ) from error
    finally:
        connection.close()


def safe_get(
    url: str,
    *,
    headers: dict | None = None,
    timeout: int = 12,
    max_redirects: int = 5,
    requester=None,
):
    """GET a public URL, pin each connection to a validated IP, and check redirects."""
    if max_redirects < 0:
        raise ValueError("max_redirects cannot be negative")

    current_url = validate_public_http_url(url)
    for redirect_number in range(max_redirects + 1):
        response = (
            requester(
                current_url,
                headers=headers or {},
                timeout=timeout,
                allow_redirects=False,
            )
            if requester is not None
            else _request_pinned(current_url, headers=headers, timeout=timeout)
        )
        if response.status_code not in _REDIRECT_CODES:
            return response

        location = response.headers.get("Location")
        if not location:
            return response

        next_url = validate_public_http_url(urljoin(current_url, location))
        response.close()
        if redirect_number == max_redirects:
            raise UnsafeURL(f"Too many redirects while checking {url}")
        current_url = next_url

    raise UnsafeURL(f"Too many redirects while checking {url}")


def safe_browser_route(route) -> None:
    """Fulfil browser requests through the DNS-pinned client instead of Chromium DNS."""
    request = route.request
    scheme = request.url.split(":", 1)[0].lower()
    if scheme in {"data", "blob", "about"}:
        route.continue_()
        return

    if request.method.upper() not in {"GET", "HEAD"}:
        route.abort()
        return

    response = None
    try:
        safe_headers = {
            key: value
            for key, value in request.headers.items()
            if key.lower() in {"accept", "accept-language", "user-agent"}
        }
        response = safe_get(
            request.url,
            headers=safe_headers,
            timeout=12,
            method=request.method.upper(),
        )
        headers = {}
        for key, value in response.headers.items():
            lowered = key.lower()
            if lowered in {
                "connection", "content-encoding", "content-length",
                "transfer-encoding", "set-cookie", "location",
            }:
                continue
            headers[key] = value
        route.fulfill(
            status=response.status_code,
            headers=headers,
            body=response.read(),
        )
    except (UnsafeURL, OSError, http.client.HTTPException, ssl.SSLError):
        route.abort()
    finally:
        if response is not None:
            response.close()


def safe_urlopen(request: Request, *, timeout: int = 12):
    """Open a urllib Request using the same DNS-pinned, redirect-safe HTTP client."""
    method = request.get_method()
    headers = dict(request.header_items())
    return safe_get(request.full_url, headers=headers, timeout=timeout, method=method)
