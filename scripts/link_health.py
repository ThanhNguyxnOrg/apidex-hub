"""Shared conservative classification for API endpoint health checks."""
from __future__ import annotations


def looks_like_waf_challenge(content: str) -> bool:
    """Detect common bot-challenge pages without attempting to bypass them."""
    lowered = (content or "").lower()
    return any(marker in lowered for marker in (
        "just a moment",
        "attention required",
        "checking your browser",
        "verify you are human",
        "challenge-platform",
        "cf-chl-",
        "captcha challenge",
    ))


def classify_http_status(status: int | None, *, waf_detected: bool = False) -> tuple[str, str]:
    """Classify an HTTP response without treating access restrictions as health."""
    if waf_detected:
        return "protected", "WAF or bot-protection response; availability is not confirmed"
    if status is None:
        return "unknown", "No HTTP status was received"
    if 200 <= status < 300:
        return "working", "Successful HTTP response"
    if status in {401, 403, 418, 429}:
        return "protected", f"Access restricted or rate limited (HTTP {status}); availability is not confirmed"
    if status in {400, 405, 406}:
        return "unknown", f"HTTP {status}; endpoint health is not confirmed"
    if status in {404, 410}:
        return "broken", f"HTTP {status}; endpoint may be gone and requires independent confirmation"
    if status == 503:
        return "warning", "Service unavailable (HTTP 503); may be temporary"
    if status in {500, 502, 504} or 520 <= status <= 527:
        return "error", f"Server error (HTTP {status}); may be temporary"
    if 500 <= status < 600:
        return "error", f"Server error (HTTP {status}); may be temporary"
    return "unknown", f"Unclassified HTTP status {status}; availability is not confirmed"


def classify_playwright_result(status: int | None, note: str = "") -> str:
    """Classify Stage 2 without preserving an earlier 'broken' result on exceptions."""
    lowered = (note or "").lower()
    if any(term in lowered for term in (
        "parked domain", "suspended hosting", "err_name_not_resolved",
        "dns_probe_finished_nxdomain", "nxdomain", "dnsresolutionerror",
        "name or service not known", "nodename nor servname",
    )):
        return "broken"
    if any(term in lowered for term in ("cloudflare", "waf", "challenge", "captcha")):
        return "protected"
    if status in {401, 403, 418, 429}:
        return "protected"
    if status in {404, 410}:
        return "broken"
    if status in {400, 405, 406}:
        return "unknown"
    if status == 503 and any(term in lowered for term in ("cloudflare", "waf", "challenge")):
        return "protected"
    if status is not None and 200 <= status < 400:
        return "working"
    if status is not None and 500 <= status < 600:
        return "error"
    if any(term in lowered for term in (
        "timeout", "err_connection_refused", "err_connection_reset",
        "err_ssl", "err_cert", "connection closed",
    )):
        return "warning"
    if any(term in lowered for term in ("cloudflare", "blocked by", "waf", "turnstile", "bot protection")):
        return "protected"
    return "unknown"
