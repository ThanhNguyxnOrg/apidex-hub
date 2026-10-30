#!/usr/bin/env python3
"""Manually remove reviewed dead API links from the Markdown catalog.

This tool is dry-run by default. A maintainer must pass --apply after confirming
that a failed documentation URL is not merely moved, temporarily unavailable,
or protected by an access-control layer.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


def normalize_url(url: str) -> str:
    """Normalize host casing, default ports and trailing slashes only."""
    if not url:
        return ""
    try:
        parts = urlsplit(url.strip())
        if parts.scheme.lower() not in {"http", "https"} or not parts.hostname:
            return url.strip()
        host = parts.hostname.lower()
        port = parts.port
        if port and not ((parts.scheme.lower() == "https" and port == 443) or (parts.scheme.lower() == "http" and port == 80)):
            host = f"{host}:{port}"
        path = parts.path.rstrip("/") or "/"
        return urlunsplit((parts.scheme.lower(), host, path, parts.query, ""))
    except ValueError:
        return url.strip()


def load_dead_urls(file_path: Path):
    """Load reported URLs and retain query strings when comparing entries."""
    if not file_path.exists():
        print(f"Warning: {file_path} does not exist.")
        return set(), set(), {}
    raw_urls, normalized_urls, url_metadata = set(), set(), {}
    with file_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("|", 1)
            url = parts[0].strip()
            reason = parts[1].strip() if len(parts) > 1 else ""
            if url.startswith(("http://", "https://")):
                raw_urls.add(url)
                normalized_urls.add(normalize_url(url))
                url_metadata[url] = reason
    return raw_urls, normalized_urls, url_metadata


def extract_url_from_row(line: str):
    """Extract only the official documentation URL in the fifth table column."""
    stripped = line.strip()
    if not (stripped.startswith("|") and stripped.endswith("|")):
        return None
    cells = [cell.strip() for cell in stripped[1:-1].split("|")]
    if len(cells) != 5:
        return None
    match = re.search(r"\[Link\]\((https?://[^)]+)\)", cells[4], re.IGNORECASE)
    return match.group(1).strip() if match else None


def extract_api_name_from_row(line: str) -> str:
    match = re.search(r"\|\s*\*\*([^*]+)\*\*", line)
    if match:
        return match.group(1).strip()
    parts = [part.strip() for part in line.split("|") if part.strip()]
    return parts[0] if parts else "Unknown API"


def is_table_data_row(line: str) -> bool:
    stripped = line.strip()
    if not (stripped.startswith("|") and stripped.endswith("|")):
        return False
    content_without_pipes = stripped.replace("|", "").replace("-", "").replace(":", "").strip()
    return bool(content_without_pipes) and extract_url_from_row(line) is not None


def remove_dead_links_from_file(
    file_path: Path,
    raw_dead_urls: set,
    normalized_dead_urls: set,
    dry_run: bool = True,
):
    """Collect candidate rows; writes only when dry_run=False is explicit."""
    with file_path.open("r", encoding="utf-8") as handle:
        lines = handle.readlines()
    new_lines, removed_items = [], []
    raw_without_trailing_slash = {url.rstrip("/") for url in raw_dead_urls}
    for line in lines:
        if not is_table_data_row(line):
            new_lines.append(line)
            continue
        target_url = extract_url_from_row(line)
        target_norm = normalize_url(target_url)
        matches = (
            target_url in raw_dead_urls
            or target_url.rstrip("/") in raw_without_trailing_slash
            or target_norm in normalized_dead_urls
        )
        if not matches:
            new_lines.append(line)
            continue
        try:
            relative_file = str(file_path.relative_to(Path.cwd()))
        except ValueError:
            relative_file = file_path.name
        removed_items.append({
            "name": extract_api_name_from_row(line),
            "url": target_url,
            "file": relative_file,
        })
    if removed_items and not dry_run:
        file_path.write_text("".join(new_lines), encoding="utf-8", newline="\n")
    return removed_items


def _write_summary(all_candidates, applied: bool, safety_brake: bool = False):
    scripts_dir = Path("scripts")
    scripts_dir.mkdir(parents=True, exist_ok=True)
    summary = {
        "count": len(all_candidates),
        "applied": applied,
        "safety_brake_triggered": safety_brake,
        "removed": all_candidates if applied else [],
        "candidates": all_candidates,
    }
    (scripts_dir / "removed_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    with (scripts_dir / "removed_summary.md").open("w", encoding="utf-8") as handle:
        if all_candidates:
            title = "Removed API rows" if applied else "DRY RUN — API rows requiring maintainer review"
            handle.write(f"{title}\n\n| # | API Name | File | URL |\n|---|---|---|---|\n")
            for index, item in enumerate(all_candidates, 1):
                handle.write(
                    f"| {index} | {item['name']} | {item['file']} | {item['url']} |\n"
                )
        else:
            handle.write("No matching API rows found.\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Review and optionally remove API rows whose documentation URLs are confirmed dead."
    )
    parser.add_argument("--report", default="scripts/broken_urls.txt", help="Path to reviewed broken URL report")
    parser.add_argument("--apis-dir", default="apis", help="Directory containing API Markdown files")
    parser.add_argument(
        "--apply", action="store_true",
        help="Apply deletions. Without this flag the command is always a dry run.",
    )
    parser.add_argument(
        "--max-delete", type=int, default=500,
        help="Safety brake: maximum number of matching API rows allowed in one apply operation (0 disables the brake).",
    )
    args = parser.parse_args()
    if args.max_delete < 0:
        parser.error("--max-delete must be zero or greater")

    report_path, apis_dir = Path(args.report), Path(args.apis_dir)
    if not apis_dir.is_dir():
        print(f"Error: API directory {apis_dir} does not exist.", file=sys.stderr)
        return 1

    raw_dead_urls, normalized_dead_urls, _metadata = load_dead_urls(report_path)
    if not raw_dead_urls:
        print("No dead URLs found in report. Nothing to review.")
        _write_summary([], applied=False)
        return 0

    files = sorted(apis_dir.glob("*.md"))
    candidates_by_file = {
        path: remove_dead_links_from_file(path, raw_dead_urls, normalized_dead_urls, dry_run=True)
        for path in files
    }
    all_candidates = [item for items in candidates_by_file.values() for item in items]
    print(f"Found {len(raw_dead_urls)} unique reported URLs matching {len(all_candidates)} catalog row(s).")

    if args.apply and args.max_delete > 0 and len(all_candidates) > args.max_delete:
        print(
            f"SAFETY BRAKE TRIGGERED: {len(all_candidates)} candidate rows exceed "
            f"--max-delete={args.max_delete}; no files were changed.",
            file=sys.stderr,
        )
        _write_summary(all_candidates, applied=False, safety_brake=True)
        return 2

    if not args.apply:
        print("DRY-RUN: no catalog files were changed. Review the candidate report, then rerun with --apply to confirm.")
        _write_summary(all_candidates, applied=False)
        return 0

    applied_items = []
    for path, candidates in candidates_by_file.items():
        if not candidates:
            continue
        written = remove_dead_links_from_file(
            path, raw_dead_urls, normalized_dead_urls, dry_run=False
        )
        applied_items.extend(written)
        print(f"  - Removed {len(written)} reviewed row(s) from {path.name}")

    _write_summary(applied_items, applied=True)
    if applied_items:
        print("Updating derived catalog data with scripts/parse_readme.py...")
        result = subprocess.run(
            [sys.executable, "scripts/parse_readme.py", "--readme", str(apis_dir),
             "--output", "site/src/data/apis.json"],
            capture_output=True, text=True, check=False,
        )
        if result.returncode == 0:
            print("Successfully refreshed derived catalog files.")
        else:
            print(f"Warning: catalog regeneration failed: {result.stderr.strip()}", file=sys.stderr)
            return result.returncode
    print(f"Applied {len(applied_items)} reviewed deletion(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
