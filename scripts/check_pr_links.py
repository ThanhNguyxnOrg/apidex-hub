#!/usr/bin/env python3
"""Validate catalog URLs and enforce endpoint-only automated API row removals.

The checker uses explicit base/head commits and repository-root Git commands. Access
controls and transient failures are reported as inconclusive, never as proof of death.
"""

import os
import re
import sys
from pathlib import Path

import requests
from playwright.sync_api import sync_playwright

from shutdown_detection import detect_shutdown_notice
from link_health import looks_like_parked_domain, looks_like_waf_challenge
from safe_urls import DNSResolutionError, UnsafeURL, safe_browser_route, safe_get, validate_public_http_url
from pr_validation import (
    classify_link_result,
    find_duplicate_urls,
    normalize_url,
    removal_validation_key,
    parse_api_diff,
    read_existing_api_urls,
    read_pr_diff,
    select_pr_urls_to_validate,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def verify_with_playwright(browser, url: str) -> tuple[int | None, str]:
    """Retry a candidate URL in Chromium and return its final document status."""
    context = None
    page = None
    last_response = [None]
    try:
        validate_public_http_url(url)
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent=USER_AGENT,
        )
        page = context.new_page()

        page.route("**/*", safe_browser_route)
        page.on(
            "response",
            lambda response: last_response.__setitem__(0, response)
            if response.frame == page.main_frame and response.request.resource_type == "document"
            else None,
        )
        response = page.goto(url, wait_until="domcontentloaded", timeout=12000)
        final_response = last_response[0] or response
        status = final_response.status if final_response else None
        title = page.title().lower()
        content = page.content().lower()
        parked_indicators = (
            "domain parking", "buy this domain", "domain for sale", "hugedomains",
            "sedo.com", "hosting suspended", "account suspended", "website is suspended",
        )
        if any(term in title or term in content for term in parked_indicators):
            return 404, "Playwright: parked domain or suspended hosting detected"
        shutdown_signal = detect_shutdown_notice(title + " " + content)
        if shutdown_signal:
            return status, "Explicit provider shutdown notice (manual review only): " + shutdown_signal["matched_text"]
        if looks_like_waf_challenge(title + " " + content):
            return status if status in {401, 403, 418, 429, 503} else 403, "Playwright: WAF challenge detected; endpoint availability is not confirmed"
        return status, f"Playwright: final document HTTP {status if status is not None else 'unknown'}"
    except Exception as error:
        message = re.sub(r"\s+", " ", str(error)).strip()
        return None, f"Playwright exception: {message}"
    finally:
        if page:
            try:
                page.close()
            except Exception:
                pass
        if context:
            try:
                context.close()
            except Exception:
                pass


def check_url(browser, url: str) -> tuple[str, int | None, str]:
    """Return working, broken, or inconclusive; only corroborated death fails CI."""
    try:
        response = safe_get(
            url,
            headers={
                "User-Agent": "APIDexHub-LinkChecker/2.0 (+https://github.com/ThanhNguyxnOrg/apidex-hub)",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            },
            timeout=12,
        )
        if looks_like_parked_domain(response.text):
            return "broken", response.status_code, "Parked domain or suspended hosting detected in response body"
        shutdown_signal = detect_shutdown_notice(response.text)
        if shutdown_signal:
            return (
                "shutdown_signal",
                response.status_code,
                "Explicit provider shutdown notice (manual review only): "
                f"{shutdown_signal['matched_text']}",
            )
        if looks_like_waf_challenge(response.text):
            return "inconclusive", response.status_code, "WAF or bot-challenge page; API availability is not confirmed"
        state = classify_link_result(response.status_code, response.text)
        if state == "working":
            return state, response.status_code, "HTTP request succeeded"
        if state == "inconclusive":
            return state, response.status_code, "Access restricted, rate limited, or server failure; requires review"
        stage_one_note = f"Stage 1 returned HTTP {response.status_code}"
    except DNSResolutionError as error:
        stage_one_note = f"Stage 1 DNS NXDOMAIN: {error}"
    except UnsafeURL as error:
        return "inconclusive", None, f"Unsafe URL or redirect blocked: {error}"
    except requests.RequestException as error:
        stage_one_note = f"Stage 1 request failed: {type(error).__name__}"

    status, stage_two_note = verify_with_playwright(browser, url)
    state = classify_link_result(status, stage_two_note)
    note = f"{stage_one_note}; {stage_two_note}"
    return state, status, note


def write_report(
    changed_paths: list[str],
    added_urls: list[str],
    removed_urls: list[str],
    working: list[tuple[str, int | None, str]],
    broken: list[tuple[str, int | None, str]],
    inconclusive: list[tuple[str, int | None, str]],
    duplicates: list[str],
    malformed_rows: list[str],
    confirmed_dead_removals: list[tuple[str, int | None, str]] | None = None,
    unconfirmed_removals: list[tuple[str, int | None, str]] | None = None,
    shutdown_signals: list[tuple[str, int | None, str]] | None = None,
) -> str:
    lines = [
        "PR API LINK CHECK REPORT",
        "=" * 80,
        "",
        f"API files changed: {len(changed_paths)}",
        f"New catalog URLs checked: {len(added_urls)}",
        f"Removed API endpoint URLs: {len(removed_urls)}",
        f"Working: {len(working)}",
        f"Broken (404/410 or DNS NXDOMAIN): {len(broken)}",
        f"Provider shutdown signals (manual review): {len(shutdown_signals or [])}",
        f"Inconclusive (access restriction, timeout, or server failure): {len(inconclusive)}",
        f"Duplicate URLs: {len(duplicates)}",
        f"Malformed API rows: {len(malformed_rows)}",
        "",
    ]
    if not added_urls and removed_urls:
        lines.append("No new endpoint URLs were introduced. Legacy documentation-only row removals are not valid automated API-remediation candidates.")
    elif not added_urls:
        lines.append("No new catalog URLs were introduced; no API endpoint health claim was made for this PR.")
    for title, items in (
        ("BROKEN URLS", broken),
        ("INCONCLUSIVE URLS — MAINTAINER REVIEW", inconclusive),
    ):
        if items:
            lines.extend(["", title, "-" * 80])
            lines.extend(f"- {url} | HTTP {status if status is not None else 'N/A'} | {note}" for url, status, note in items)
    if confirmed_dead_removals:
        lines.extend(["", "REMOVED URLS REVALIDATED AS CONFIRMED DEAD", "-" * 80])
        lines.extend(f"- {url} | HTTP {status if status is not None else 'N/A'} | {note}" for url, status, note in confirmed_dead_removals)
    if unconfirmed_removals:
        lines.extend(["", "REMOVALS NO LONGER CONFIRMED DEAD — BLOCKED", "-" * 80])
        lines.extend(f"- {url} | HTTP {status if status is not None else 'N/A'} | {note}" for url, status, note in unconfirmed_removals)
    if shutdown_signals:
        lines.extend(["", "PROVIDER SHUTDOWN SIGNALS — MANUAL REVIEW ONLY", "-" * 80])
        lines.extend(f"- {url} | HTTP {status if status is not None else 'N/A'} | {note}" for url, status, note in shutdown_signals)
    if duplicates:
        lines.extend(["", "DUPLICATE OFFICIAL DOCUMENTATION URLS", "-" * 80])
        lines.extend(f"- {url}" for url in duplicates)
    if malformed_rows:
        lines.extend(["", "MALFORMED ADDED API ROWS", "-" * 80])
        lines.extend(f"- {row}" for row in malformed_rows)
    if not broken and not duplicates and not malformed_rows and not shutdown_signals:
        lines.extend(["", "Validation result: no confirmed broken links, duplicate URLs, or malformed added rows."])
        if inconclusive:
            lines.append("Note: inconclusive URLs were not counted as working; review them before relying on their availability.")
    report = "\n".join(lines) + "\n"
    (Path(__file__).resolve().parent / "pr_link_check_report.txt").write_text(report, encoding="utf-8")
    return report


def main() -> int:
    base_ref = os.environ.get("APIDEX_DIFF_BASE", "").strip()
    head_ref = os.environ.get("APIDEX_DIFF_HEAD", "").strip()
    if not base_ref or not head_ref:
        print(
            "ERROR: APIDEX_DIFF_BASE and APIDEX_DIFF_HEAD are required. "
            "The PR checker will not infer refs or treat an unresolved diff as empty.",
            file=sys.stderr,
        )
        return 2

    try:
        changed_paths, diff_text = read_pr_diff(base_ref, head_ref, REPO_ROOT)
        validate_removals = os.environ.get("APIDEX_VALIDATE_REMOVALS", "").strip().lower() == "true"
        added_urls, removed_urls, malformed_rows = parse_api_diff(
            diff_text, validate_removals=validate_removals
        )
        existing_urls = read_existing_api_urls(base_ref, REPO_ROOT)
    except RuntimeError as error:
        print(f"ERROR: PR API diff validation could not run: {error}", file=sys.stderr)
        return 2

    duplicates = find_duplicate_urls(added_urls, removed_urls, existing_urls)
    duplicate_keys = {normalize_url(url) for url in duplicates}
    added_to_check, removed_to_check = select_pr_urls_to_validate(
        added_urls, removed_urls, validate_removals=validate_removals
    )
    added_to_check = [url for url in added_to_check if normalize_url(url) not in duplicate_keys]
    urls_to_check = added_to_check + removed_to_check
    removed_keys = {removal_validation_key(url) for url in removed_to_check}

    working: list[tuple[str, int | None, str]] = []
    broken: list[tuple[str, int | None, str]] = []
    inconclusive: list[tuple[str, int | None, str]] = []
    confirmed_dead_removals: list[tuple[str, int | None, str]] = []
    unconfirmed_removals: list[tuple[str, int | None, str]] = []
    shutdown_signals: list[tuple[str, int | None, str]] = []

    if urls_to_check:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            try:
                for url in urls_to_check:
                    state, status, note = check_url(browser, url)
                    item = (url, status, note)
                    if removal_validation_key(url) in removed_keys:
                        if state == "broken":
                            confirmed_dead_removals.append(item)
                        else:
                            unconfirmed_removals.append(item)
                    elif state == "shutdown_signal":
                        shutdown_signals.append(item)
                    elif state == "working":
                        working.append(item)
                    elif state == "broken":
                        broken.append(item)
                    else:
                        inconclusive.append(item)
                    print(f"[{state.upper()}] {url} — {note}")
            finally:
                browser.close()

    report = write_report(
        changed_paths, added_urls, removed_urls, working, broken, inconclusive,
        duplicates, malformed_rows, confirmed_dead_removals, unconfirmed_removals,
        shutdown_signals,
    )
    print(report)
    if broken or duplicates or malformed_rows or unconfirmed_removals or shutdown_signals:
        print(
            "PR validation failed. Fix confirmed dead additions, duplicate links, malformed rows, "
            "or removals that are no longer confirmed dead. Provider shutdown signals are review-only and require a separate maintainer decision before merging.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
