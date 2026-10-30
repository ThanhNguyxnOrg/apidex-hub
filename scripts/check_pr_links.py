#!/usr/bin/env python3
"""Validate only API documentation links introduced or changed by a pull request.

The checker uses explicit base/head commits and repository-root Git commands. Access
controls and transient failures are reported as inconclusive, never as proof of death.
"""

import os
import re
import sys
from pathlib import Path

import requests
from playwright.sync_api import sync_playwright

from pr_validation import (
    classify_link_result,
    find_duplicate_urls,
    normalize_url,
    parse_api_diff,
    read_existing_api_urls,
    read_pr_diff,
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
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent=USER_AGENT,
        )
        page = context.new_page()
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
        response = requests.get(
            url,
            headers={
                "User-Agent": "APIDexHub-LinkChecker/2.0 (+https://github.com/ThanhNguyxnOrg/apidex-hub)",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            },
            timeout=12,
            allow_redirects=True,
        )
        state = classify_link_result(response.status_code)
        if state == "working":
            return state, response.status_code, "HTTP request succeeded"
        if state == "inconclusive":
            return state, response.status_code, "Access restricted, rate limited, or server failure; requires review"
        stage_one_note = f"Stage 1 returned HTTP {response.status_code}"
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
) -> str:
    lines = [
        "PR API LINK CHECK REPORT",
        "=" * 80,
        "",
        f"API files changed: {len(changed_paths)}",
        f"New API documentation URLs: {len(added_urls)}",
        f"Removed API documentation URLs: {len(removed_urls)}",
        f"Working: {len(working)}",
        f"Broken (confirmed 404/410 or DNS NXDOMAIN): {len(broken)}",
        f"Inconclusive (access restriction, timeout, or server failure): {len(inconclusive)}",
        f"Duplicate URLs: {len(duplicates)}",
        f"Malformed API rows: {len(malformed_rows)}",
        "",
    ]
    if not added_urls and removed_urls:
        lines.append("No new documentation URLs were introduced. This PR removes or moves existing API rows; no URL health check is claimed.")
    elif not added_urls:
        lines.append("No new API documentation URLs were found in the changed API files.")
    for title, items in (
        ("BROKEN URLS", broken),
        ("INCONCLUSIVE URLS — MAINTAINER REVIEW", inconclusive),
    ):
        if items:
            lines.extend(["", title, "-" * 80])
            lines.extend(f"- {url} | HTTP {status if status is not None else 'N/A'} | {note}" for url, status, note in items)
    if duplicates:
        lines.extend(["", "DUPLICATE OFFICIAL DOCUMENTATION URLS", "-" * 80])
        lines.extend(f"- {url}" for url in duplicates)
    if malformed_rows:
        lines.extend(["", "MALFORMED ADDED API ROWS", "-" * 80])
        lines.extend(f"- {row}" for row in malformed_rows)
    if not broken and not duplicates and not malformed_rows:
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
        added_urls, removed_urls, malformed_rows = parse_api_diff(diff_text)
        existing_urls = read_existing_api_urls(base_ref, REPO_ROOT)
    except RuntimeError as error:
        print(f"ERROR: PR API diff validation could not run: {error}", file=sys.stderr)
        return 2

    duplicates = find_duplicate_urls(added_urls, removed_urls, existing_urls)
    duplicate_keys = {normalize_url(url) for url in duplicates}
    urls_to_check = []
    seen = set()
    for url in added_urls:
        key = normalize_url(url)
        if key not in seen and key not in duplicate_keys:
            urls_to_check.append(url)
            seen.add(key)

    working: list[tuple[str, int | None, str]] = []
    broken: list[tuple[str, int | None, str]] = []
    inconclusive: list[tuple[str, int | None, str]] = []

    if urls_to_check:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            try:
                for url in urls_to_check:
                    state, status, note = check_url(browser, url)
                    item = (url, status, note)
                    if state == "working":
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
        duplicates, malformed_rows,
    )
    print(report)
    if broken or duplicates or malformed_rows:
        print("PR validation failed. Fix confirmed dead URLs, duplicate links, or malformed API rows before merging.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
