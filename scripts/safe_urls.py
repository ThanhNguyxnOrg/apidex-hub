"""Public-URL guards for repository-controlled HTTP checks.

These checks reject non-public destinations and validate every HTTP redirect.
They are defense in depth; callers should still run inside restricted CI egress.
"""
from __future__ import annotations

from functools import lru_cache
import ipaddress
import socket
from urllib.error import URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


class UnsafeURL(ValueError):
    """Raised when a URL is malformed or points at a non-public destination."""


_BLOCKED_SUFFIXES = (
    ".localhost",
    ".local",
    ".internal",
    ".lan",
    ".home",
    ".home.arpa",
    ".test",
    ".invalid",
)


@lru_cache(maxsize=4096)
def resolve_public_addresses(host: str, port: int) -> tuple[str, ...]:
    """Resolve a hostname once and return every address supplied by the resolver."""
    records = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    addresses = tuple(sorted({record[4][0].split("%", 1)[0] for record in records}))
    if not addresses:
        raise UnsafeURL(f"Hostname did not resolve: {host}")
    return addresses


def validate_public_http_url(url: str) -> str:
    """Validate HTTP(S), reject userinfo/local names, and require globally routable IPs."""
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

    if ip_literal is not None:
        if not ip_literal.is_global:
            raise UnsafeURL(f"Non-public IP address is not allowed: {ip_literal}")
        return value

    try:
        ascii_host = host.encode("idna").decode("ascii")
    except UnicodeError as error:
        raise UnsafeURL(f"Invalid internationalized hostname: {host}") from error

    target_port = port or (443 if scheme == "https" else 80)
    try:
        addresses = resolve_public_addresses(ascii_host, target_port)
    except (OSError, socket.gaierror, UnsafeURL) as error:
        raise UnsafeURL(f"Could not safely resolve {ascii_host}: {error}") from error

    for address in addresses:
        try:
            parsed_address = ipaddress.ip_address(address)
        except ValueError as error:
            raise UnsafeURL(f"Resolver returned an invalid IP for {ascii_host}") from error
        if not parsed_address.is_global:
            raise UnsafeURL(
                f"Hostname {ascii_host} resolves to a non-public address: {parsed_address}"
            )

    return value


def safe_get(url: str, *, headers: dict | None = None, timeout: int = 12, max_redirects: int = 5, requester=None):
    """Perform a GET while validating the destination before every redirect hop."""
    if max_redirects < 0:
        raise ValueError("max_redirects cannot be negative")

    if requester is None:
        import requests
        requester = requests.get

    current_url = validate_public_http_url(url)
    for redirect_number in range(max_redirects + 1):
        response = requester(
            current_url,
            headers=headers or {},
            timeout=timeout,
            allow_redirects=False,
        )
        if response.status_code not in {301, 302, 303, 307, 308}:
            return response

        location = response.headers.get("Location")
        if not location:
            return response

        next_url = urljoin(current_url, location)
        try:
            next_url = validate_public_http_url(next_url)
        except UnsafeURL:
            response.close()
            raise

        response.close()
        if redirect_number == max_redirects:
            raise UnsafeURL(f"Too many redirects while checking {url}")
        current_url = next_url

    raise UnsafeURL(f"Too many redirects while checking {url}")


class _SafeRedirectHandler(HTTPRedirectHandler):
    """urllib redirect handler that validates the next destination."""

    def redirect_request(self, request, file_pointer, code, message, headers, new_url):
        target = validate_public_http_url(urljoin(request.full_url, new_url))
        return super().redirect_request(
            request, file_pointer, code, message, headers, target
        )


def safe_urlopen(request: Request, *, timeout: int = 12):
    """Open a urllib request with initial-URL and redirect validation."""
    validate_public_http_url(request.full_url)
    opener = build_opener(_SafeRedirectHandler())
    try:
        return opener.open(request, timeout=timeout)
    except UnsafeURL:
        raise
    except URLError as error:
        if isinstance(error.reason, UnsafeURL):
            raise error.reason
        raise
