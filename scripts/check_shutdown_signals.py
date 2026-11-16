#!/usr/bin/env python3
"""Scan catalog documentation links for explicit provider shutdown notices.

The scan includes legacy 5-column rows and canonical 6-column rows. Documentation
availability and shutdown notices are reported separately from API endpoint health.
A documentation failure or shutdown phrase never triggers automatic row deletion.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from html import unescape
from http.client import HTTPException
from pathlib import Path
import json
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from shutdown_detection import detect_shutdown_notice

_LINK_RE = re.compile(r"\[[^\]]+\]\((https?://[^)]+)\)", re.IGNORECASE)
_CATEGORY_RE = re.compile(
    r"^##\s+(?:<a\b[^>]*>\s*</a>\s*)?\S+\s+(.+)$",
    re.MULTILINE,
)
_USER_AGENT = "APIDexHub-DocumentationMonitor/1.0 (+https://github.com/ThanhNguyxnOrg/apidex-hub)"
_MAX_BODY_BYTES = 1_000_000


def _row_cells(line: str) -> list[str] | None:
    stripped = line.strip()
    if not (stripped.startswith("|") and stripped.endswith("|")):
        return None
    cells = [cell.strip().replace(r"\|", "|") for cell in re.split(r"(?<!\\)\|", stripped)]
    if cells and not cells[0]:
        cells.pop(0)
    if cells and not cells[-1]:
        cells.pop()
    return cells


def parse_documentation_targets(apis_dir: str | Path = "apis") -> list[dict]:
    """Extract documentation URLs from both supported catalog row formats."""
    root = Path(apis_dir)
    if not root.is_dir():
        raise FileNotFoundError(f"API catalog directory does not exist: {root}")

    grouped: dict[str, dict] = {}
    for path in sorted(root.glob("*.md")):
        content = path.read_text(encoding="utf-8")
        category_match = _CATEGORY_RE.search(content)
        category = category_match.group(1).strip() if category_match else path.stem.replace("-", " ").title()

        for line_number, line in enumerate(content.splitlines(), 1):
            cells = _row_cells(line)
            if not cells or len(cells) not in (5, 6):
                continue
            if cells[0].strip("* ").lower() in {"api name", "name"}:
                continue
            if all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells):
                continue

            name = re.sub(r"\*\*(.+?)\*\*", r"\1", cells[0]).strip()
            if not name:
                continue
            documentation_cell = cells[4] if len(cells) == 5 else cells[5]
            match = _LINK_RE.search(documentation_cell)
            if not match:
                continue

            url = match.group(1).strip()
            item = grouped.setdefault(url, {
                "url": url,
                "apis": [],
            })
            item["apis"].append({
                "name": name,
                "category": category,
                "file": str(path).replace("\\", "/"),
                "line": line_number,
            })

    return [grouped[url] for url in sorted(grouped)]


def _decode_body(body: bytes, headers) -> str:
    charset = "utf-8"
    try:
        charset = headers.get_content_charset() or "utf-8"
    except Exception:
        pass
    try:
        return body.decode(charset, errors="replace")
    except LookupError:
        return body.decode("utf-8", errors="replace")


def fetch_documentation(url: str, timeout: int = 12) -> dict:
    """Fetch a docs page and inspect its body even when the HTTP status is an error."""
    request = Request(
        url,
        headers={
            "User-Agent": _USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/json,text/plain,*/*;q=0.8",
        },
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read(_MAX_BODY_BYTES)
            headers = response.headers
            status = response.getcode()
            final_url = response.geturl()
    except HTTPError as error:
        body = error.read(_MAX_BODY_BYTES)
        headers = error.headers
        status = error.code
        final_url = error.geturl()
    except (URLError, TimeoutError, HTTPException, OSError) as error:
        return {
            "url": url,
            "status": None,
            "final_url": url,
            "error": f"{type(error).__name__}: {str(error)[:240]}",
            "shutdown_signal": None,
        }

    text = _decode_body(body, headers)
    signal = detect_shutdown_notice(text)
    return {
        "url": url,
        "status": status,
        "final_url": final_url,
        "error": None,
        "shutdown_signal": signal,
    }


def scan_documentation(apis_dir: str | Path = "apis", workers: int = 12) -> dict:
    targets = parse_documentation_targets(apis_dir)
    results: list[dict] = []

    with ThreadPoolExecutor(max_workers=max(1, workers)) as executor:
        futures = {
            executor.submit(fetch_documentation, target["url"]): target
            for target in targets
        }
        for future in as_completed(futures):
            target = futures[future]
            try:
                result = future.result()
            except Exception as error:
                result = {
                    "url": target["url"],
                    "status": None,
                    "final_url": target["url"],
                    "error": f"{type(error).__name__}: {str(error)[:240]}",
                    "shutdown_signal": None,
                }
            result["apis"] = target["apis"]
            results.append(result)

    results.sort(key=lambda item: item["url"])
    signals = []
    inconclusive = []
    reachable = 0
    for result in results:
        status = result["status"]
        if result["shutdown_signal"]:
            signals.append(result)
        if result["error"] or status is None or status >= 400:
            inconclusive.append(result)
        elif 200 <= status < 400:
            reachable += 1

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_documentation_links": len(targets),
        "reachable_documentation_links": reachable,
        "inconclusive_documentation_links": len(inconclusive),
        "shutdown_signal_count": len(signals),
        "shutdown_signals": signals,
        "inconclusive": inconclusive,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan API documentation links for provider shutdown notices.")
    parser.add_argument("--apis-dir", default="apis", help="Catalog Markdown directory")
    parser.add_argument("--output", default="", help="Optional JSON report path")
    parser.add_argument("--workers", type=int, default=12)
    args = parser.parse_args()
    if args.workers < 1 or args.workers > 32:
        parser.error("--workers must be between 1 and 32")

    try:
        report = scan_documentation(args.apis_dir, args.workers)
    except (OSError, ValueError) as error:
        print(f"ERROR: documentation scan could not start: {error}", file=sys.stderr)
        return 2

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(
        "Documentation scan complete: "
        f"{report['total_documentation_links']} unique docs URLs, "
        f"{report['reachable_documentation_links']} reachable, "
        f"{report['shutdown_signal_count']} shutdown signals, "
        f"{report['inconclusive_documentation_links']} inconclusive."
    )
    for item in report["shutdown_signals"]:
        names = ", ".join(api["name"] for api in item["apis"])
        signal = item["shutdown_signal"]
        print(f"[SHUTDOWN SIGNAL] {names} | {item['url']} | {signal['matched_text']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
