"""Conservative provider/API lifecycle signal detection.

A retirement notice for one legacy endpoint or a third-party service mentioned in
documentation is not evidence that the catalog provider itself has shut down.
Signals are classified for review; this module never authorizes catalog deletion.
"""
from __future__ import annotations

from html import unescape
from html.parser import HTMLParser
import re
from urllib.parse import urlsplit


class _VisibleTextParser(HTMLParser):
    """Extract visible page text while ignoring scripts, styles and hidden metadata."""

    _IGNORED = frozenset({"script", "style", "noscript", "svg", "template"})

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._ignored_depth = 0

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag.lower() in self._IGNORED:
            self._ignored_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in self._IGNORED and self._ignored_depth:
            self._ignored_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self._ignored_depth:
            self.parts.append(data)


_SHUTDOWN_PATTERNS = (
    (
        "request_intake_closed",
        re.compile(
            r"\bno longer accepting (?:any )?(?:new )?(?:api )?(?:requests?|subscriptions?)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "service_shutdown",
        re.compile(
            r"\b(?:api|service|platform)\s+(?:has|have|is|was|will be)\s+"
            r"(?:been\s+)?(?:permanently\s+)?"
            r"(?:shut down|discontinued|retired|decommissioned|terminated)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "provider_shutdown",
        re.compile(
            r"\b(?:we|our company|the company)\s+(?:have|has)\s+shut down\b",
            re.IGNORECASE,
        ),
    ),
    (
        "service_operations_ended",
        re.compile(
            r"\b(?:api|service|platform)\s+(?:has|have)\s+"
            r"(?:ceased operations|ended operations)\b",
            re.IGNORECASE,
        ),
    ),
)

_NAMED_SUBJECT_RE = re.compile(
    r"(?P<subject>(?:(?-i:[A-Z][A-Za-z0-9&.+-]*\s+){1,4})(?i:API|service|platform))"
    r"\s+(?i:has|have|is|was|will be)\b",
)
_EXTERNAL_DOMAIN_RE = re.compile(r"\b(?:[a-z0-9-]+\.)+[a-z]{2,}\b", re.IGNORECASE)
_LEGACY_SCOPE_RE = re.compile(
    r"\b(?:legacy|old|previous|former|deprecated|obsolete)\b"
    r".{0,120}\b(?:api|apis|endpoint|endpoints|version|reporting)\b"
    r"|\b(?:api|apis|endpoint|endpoints)\b"
    r".{0,80}\b(?:legacy|old|previous|former|deprecated|obsolete)\b"
    r"|\b(?:v|version\s*)\d+(?:\.\d+)+\s+(?:api|endpoint)\b",
    re.IGNORECASE,
)
_GENERIC_TOKENS = frozenset({
    "a", "an", "and", "api", "apis", "app", "com", "company", "developer",
    "developers", "docs", "documentation", "endpoint", "endpoints", "io",
    "net", "org", "our", "platform", "provider", "service", "services",
    "the", "this", "www",
})


def visible_text(content: str) -> str:
    """Return normalized visible text from HTML or plain-text documentation."""
    parser = _VisibleTextParser()
    try:
        parser.feed(content or "")
        parser.close()
        extracted = " ".join(parser.parts)
    except Exception:
        extracted = content or ""
    return re.sub(r"\s+", " ", unescape(extracted)).strip()


def _identifier_tokens(value: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", str(value or "").lower())
        if token not in _GENERIC_TOKENS and len(token) > 1
    }


def _provider_tokens(documentation_url: str | None, provider_names) -> set[str]:
    tokens: set[str] = set()
    for name in provider_names or ():
        tokens.update(_identifier_tokens(name))
    if documentation_url:
        try:
            host = urlsplit(documentation_url).hostname or ""
        except ValueError:
            host = ""
        tokens.update(_identifier_tokens(host))
    return tokens


def _context_window(text: str, start: int, end: int) -> str:
    # Include adjacent sentence context because docs often introduce a legacy API
    # immediately before the sentence that says it was retired.
    return text[max(0, start - 360):min(len(text), end + 180)]


def _classify_scope(
    text: str,
    match: re.Match,
    documentation_url: str | None,
    provider_names,
) -> tuple[str, str | None]:
    context = _context_window(text, match.start(), match.end())
    if _LEGACY_SCOPE_RE.search(context):
        return "legacy-api", None

    provider_tokens = _provider_tokens(documentation_url, provider_names)
    prefix = text[max(0, match.start() - 110):match.start()]
    subject_match = _NAMED_SUBJECT_RE.search(prefix + match.group(0))
    if subject_match:
        subject_tokens = _identifier_tokens(subject_match.group("subject"))
        if subject_tokens and provider_tokens and not subject_tokens.intersection(provider_tokens):
            return "external-service-reference", subject_match.group("subject")

    # A docs page may quote a separate service's outage/retirement FAQ. Do not
    # attribute that notice to the catalog provider when the named domain is
    # unrelated to both the documentation host and the API/provider name.
    prefix_context = text[max(0, match.start() - 360):match.start()]
    domains = _EXTERNAL_DOMAIN_RE.findall(prefix_context)
    doc_host = ""
    if documentation_url:
        try:
            doc_host = (urlsplit(documentation_url).hostname or "").lower()
        except ValueError:
            pass
    for domain in domains:
        domain = domain.lower().strip(".")
        if doc_host and (domain == doc_host or domain.endswith("." + doc_host) or doc_host.endswith("." + domain)):
            continue
        domain_tokens = _identifier_tokens(domain)
        if domain_tokens and provider_tokens and not domain_tokens.intersection(provider_tokens):
            return "external-service-reference", domain

    return "provider-or-current-api", None


def detect_shutdown_notice(
    content: str,
    *,
    documentation_url: str | None = None,
    provider_names=(),
) -> dict | None:
    """Return the strongest lifecycle signal found in visible documentation.

    Signals scoped to the provider/current API require review. Legacy API/version
    notices and unrelated third-party references remain informational.
    """
    text = visible_text(content)
    if not text:
        return None

    candidates: list[tuple[int, str, re.Match]] = []
    for signal_type, pattern in _SHUTDOWN_PATTERNS:
        candidates.extend((match.start(), signal_type, match) for match in pattern.finditer(text))
    candidates.sort(key=lambda item: item[0])
    if not candidates:
        return None

    classified = []
    for _, signal_type, match in candidates:
        scope, subject = _classify_scope(text, match, documentation_url, provider_names)
        classified.append((scope == "provider-or-current-api", signal_type, match, scope, subject))

    # Prefer a real current-provider/current-API signal if a page also contains
    # a historical or unrelated reference.
    actionable = next((item for item in classified if item[0]), None)
    selected = actionable or classified[0]
    _, signal_type, match, scope, subject = selected
    start = max(0, match.start() - 140)
    end = min(len(text), match.end() + 180)
    return {
        "type": signal_type,
        "scope": scope,
        "review_required": scope == "provider-or-current-api",
        "matched_text": match.group(0),
        "subject": subject,
        "snippet": text[start:end],
    }
