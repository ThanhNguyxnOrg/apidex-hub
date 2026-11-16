"""Detect explicit provider shutdown notices in API documentation content.

Signals are review evidence, not automatic deletion evidence. HTTP reachability and
API endpoint health remain separate checks.
"""
from __future__ import annotations

from html import unescape
from html.parser import HTMLParser
import re


class _VisibleTextParser(HTMLParser):
    """Extract visible page text while ignoring scripts, styles and hidden metadata."""

    _IGNORED = {"script", "style", "noscript", "svg"}

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


def detect_shutdown_notice(content: str) -> dict | None:
    """Return a matched provider-shutdown signal, or None when no strong phrase exists.

    Matches are intentionally conservative and must be reviewed by a maintainer.
    A signal never authorizes automatic catalog deletion by itself.
    """
    text = visible_text(content)
    if not text:
        return None

    for signal_type, pattern in _SHUTDOWN_PATTERNS:
        match = pattern.search(text)
        if match:
            start = max(0, match.start() - 140)
            end = min(len(text), match.end() + 180)
            return {
                "type": signal_type,
                "matched_text": match.group(0),
                "snippet": text[start:end],
            }
    return None
