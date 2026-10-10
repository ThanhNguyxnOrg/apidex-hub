#!/usr/bin/env python3
"""
scripts/remove_dead_links.py — Automatically remove dead API links from markdown files.

Reads a list of broken URLs (e.g. from broken_urls.txt), finds the matching table rows
across apis/*.md, deletes those lines while preserving table and markdown formatting,
and invokes parse_readme.py to update the catalog statistics and website data.
"""

import os
import re
import sys
import json
import argparse
import subprocess
from pathlib import Path
from urllib.parse import urlsplit


def normalize_url(url: str) -> str:
    """Normalize URL by stripping query parameters and trailing slash for comparison."""
    if not url:
        return ""
    try:
        parts = urlsplit(url.strip())
        path = parts.path.rstrip('/')
        return f"{parts.scheme}://{parts.netloc}{path}".lower()
    except Exception:
        return url.strip().rstrip('/').lower()


def load_dead_urls(file_path: Path):
    """
    Parse dead URLs from broken_urls.txt.
    Supports lines like:
      - https://example.com/api
      - https://example.com/api | Name (Category) - Reason
    """
    if not file_path.exists():
        print(f"Warning: {file_path} does not exist.")
        return set(), set(), {}

    raw_urls = set()
    normalized_urls = set()
    url_metadata = {}

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split("|")
            url = parts[0].strip()
            reason = parts[1].strip() if len(parts) > 1 else ""

            if url.startswith("http://") or url.startswith("https://"):
                raw_urls.add(url)
                norm = normalize_url(url)
                if norm:
                    normalized_urls.add(norm)
                url_metadata[url] = reason

    return raw_urls, normalized_urls, url_metadata


def extract_url_from_row(line: str):
    """Extract target URL from a markdown table row like: [Link](https://...)"""
    match = re.search(r'\[(?:Link|[^\]]+)\]\((https?://[^)]+)\)', line, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


def extract_api_name_from_row(line: str) -> str:
    """Extract bold API name from row: | **Name** | ..."""
    match = re.search(r'\|\s*\*\*([^*]+)\*\*', line)
    if match:
        return match.group(1).strip()
    # Fallback to first column content
    parts = [p.strip() for p in line.split("|") if p.strip()]
    if parts:
        return parts[0]
    return "Unknown API"


def is_table_data_row(line: str) -> bool:
    """Ensure the line is an actual data row, not a header or separator."""
    stripped = line.strip()
    if not (stripped.startswith("|") and stripped.endswith("|")):
        return False
    # Check for separator (| --- | --- |)
    content_without_pipes = stripped.replace("|", "").replace("-", "").replace(":", "").strip()
    if not content_without_pipes:
        return False
    # Check that it contains a link (headers and separators do not have markdown links)
    if not re.search(r'\[(?:Link|[^\]]+)\]\((https?://[^)]+)\)', line, re.IGNORECASE):
        return False
    return True


def remove_dead_links_from_file(file_path: Path, raw_dead_urls: set, normalized_dead_urls: set, dry_run: bool = False):
    """Scan and remove dead API rows from a markdown file."""
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    removed_items = []

    for line in lines:
        if not is_table_data_row(line):
            new_lines.append(line)
            continue

        target_url = extract_url_from_row(line)
        if not target_url:
            new_lines.append(line)
            continue

        # Match check: exact match, stripped trailing slash, or normalized without query params
        is_match = False
        target_norm = normalize_url(target_url)

        if target_url in raw_dead_urls:
            is_match = True
        elif target_url.rstrip("/") in {u.rstrip("/") for u in raw_dead_urls}:
            is_match = True
        elif target_norm in normalized_dead_urls:
            is_match = True

        if is_match:
            api_name = extract_api_name_from_row(line)
            removed_items.append({
                "name": api_name,
                "url": target_url,
                "file": str(file_path.relative_to(Path.cwd()) if file_path.is_relative_to(Path.cwd()) else file_path.name)
            })
        else:
            new_lines.append(line)

    if removed_items and not dry_run:
        with open(file_path, "w", encoding="utf-8", newline="\n") as f:
            f.writelines(new_lines)

    return removed_items


def main():
    parser = argparse.ArgumentParser(description="Remove dead API links from markdown files.")
    parser.add_argument("--report", default="scripts/broken_urls.txt", help="Path to broken URLs file")
    parser.add_argument("--apis-dir", default="apis", help="Directory containing API markdown files")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without modifying files")
    parser.add_argument("--max-delete", type=int, default=500, help="Safety brake: maximum number of dead URLs allowed to auto-remove in one run (0 to disable brake)")
    args = parser.parse_args()

    report_path = Path(args.report)
    apis_dir = Path(args.apis_dir)

    if not apis_dir.exists():
        print(f"Error: Directory {apis_dir} does not exist.", file=sys.stderr)
        sys.exit(1)

    raw_dead_urls, normalized_dead_urls, url_metadata = load_dead_urls(report_path)
    if not raw_dead_urls and not normalized_dead_urls:
        print("No dead URLs found in report. Nothing to remove.")
        # Write empty summary
        summary = {"count": 0, "removed": []}
        with open("scripts/removed_summary.json", "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
        return

    print(f"Found {len(raw_dead_urls)} unique dead URLs to process.")

    if args.max_delete > 0 and len(raw_dead_urls) > args.max_delete:
        print(f"🛑 SAFETY BRAKE TRIGGERED: {len(raw_dead_urls)} dead URLs detected, exceeding --max-delete limit of {args.max_delete}!", file=sys.stderr)
        print("Aborting automatic deletion to prevent mass removal during network outages.", file=sys.stderr)
        summary = {
            "count": 0,
            "safety_brake_triggered": True,
            "detected_count": len(raw_dead_urls),
            "removed": []
        }
        with open("scripts/removed_summary.json", "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
        sys.exit(2)

    all_removed = []
    modified_files = set()

    for md_file in sorted(apis_dir.glob("*.md")):
        removed = remove_dead_links_from_file(md_file, raw_dead_urls, normalized_dead_urls, dry_run=args.dry_run)
        if removed:
            all_removed.extend(removed)
            modified_files.add(md_file)
            print(f"  - Removed {len(removed)} API(s) from {md_file.name}")

    print(f"\nTotal APIs removed: {len(all_removed)} across {len(modified_files)} file(s).")

    # Save summary report for GitHub Actions
    summary = {
        "count": len(all_removed),
        "removed": all_removed
    }
    with open("scripts/removed_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # Write human-readable markdown table
    with open("scripts/removed_summary.md", "w", encoding="utf-8") as f:
        if all_removed:
            f.write("| # | API Name | File | Dead URL |\n|---|---|---|---|\n")
            for i, item in enumerate(all_removed, 1):
                f.write(f"| {i} | {item['name']} | `{item['file']}` | {item['url']} |\n")
        else:
            f.write("No APIs removed.\n")

    if all_removed and not args.dry_run:
        print("\nUpdating API catalog statistics with scripts/parse_readme.py...")
        res = subprocess.run(
            [sys.executable, "scripts/parse_readme.py", "--readme", str(apis_dir), "--output", "site/src/data/apis.json"],
            capture_output=True,
            text=True
        )
        if res.returncode == 0:
            print("Successfully refreshed README.md, site/index.html, and site/src/data/apis.json.")
        else:
            print(f"Warning: Failed to update catalog: {res.stderr}", file=sys.stderr)


if __name__ == "__main__":
    main()
