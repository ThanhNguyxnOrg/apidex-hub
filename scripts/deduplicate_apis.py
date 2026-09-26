#!/usr/bin/env python3
"""
scripts/deduplicate_apis.py — Deduplicate API listings across apis/*.md.

Assigns each unique API/scraper to its single best primary category:
- Non-Apify public APIs get top priority over Apify files.
- Specialized Apify categories (e.g. mcp-servers, ecommerce, social-media, real-estate, jobs)
  get higher priority than generic catch-all categories (developer-tools, automation, other).
- Duplicates within the same file are also eliminated.
"""

import os
import re
import glob
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse

# Category priority (higher = more specific/preferred category)
CATEGORY_PRIORITY = {
    # Apify categories
    'apify-mcp-servers': 80,
    'apify-agents': 75,
    'apify-real-estate': 70,
    'apify-travel': 70,
    'apify-jobs': 70,
    'apify-videos': 70,
    'apify-news': 70,
    'apify-seo-tools': 70,
    'apify-ecommerce': 65,
    'apify-social-media': 65,
    'apify-lead-generation': 60,
    'apify-business': 60,
    'apify-ai': 55,
    'apify-open-source': 50,
    'apify-developer-tools': 30,
    'apify-automation': 20,
    'apify-other': 10,
}

def get_category_priority(cat_name: str) -> int:
    """Non-apify categories default to 100 (highest priority)."""
    return CATEGORY_PRIORITY.get(cat_name, 100)

def canonical_url_key(url: str) -> str:
    """Normalize URL for duplicate detection (ignore trailing slash and affiliate query params)."""
    url_clean = url.strip()
    # Remove ?fpr=... affiliate param for comparison
    url_clean = re.sub(r'[\?&]fpr=[^&#]+', '', url_clean)
    # If ? is trailing, remove it
    url_clean = url_clean.rstrip('?').rstrip('/')
    return url_clean.lower()

def main():
    repo_root = Path(__file__).resolve().parent.parent
    apis_dir = repo_root / 'apis'

    all_entries = []
    url_map = defaultdict(list)

    md_files = sorted(list(apis_dir.glob('*.md')))
    print(f"Scanning {len(md_files)} markdown files in {apis_dir}...")

    for file_path in md_files:
        cat_name = file_path.stem
        lines = file_path.read_text(encoding='utf-8').splitlines()

        for idx, line in enumerate(lines):
            line_str = line.strip()
            if line_str.startswith('|') and '[Link]' in line_str:
                m_url = re.search(r'\[Link\]\((https?://[^\)]+)\)', line_str)
                m_name = re.search(r'\|\s*\*\*([^\*]+)\*\*', line_str)
                if m_url and m_name:
                    url = m_url.group(1).strip()
                    name = m_name.group(1).strip()
                    parts = [p.strip() for p in line_str.split('|')]
                    parts = [p for p in parts if p]
                    desc = parts[1] if len(parts) >= 2 else ""

                    canon_key = canonical_url_key(url)
                    entry = {
                        'cat': cat_name,
                        'file_path': file_path,
                        'line_idx': idx,
                        'line': line,
                        'url': url,
                        'canon_key': canon_key,
                        'name': name,
                        'desc_len': len(desc),
                    }
                    all_entries.append(entry)
                    url_map[canon_key].append(entry)

    total_before = len(all_entries)
    unique_count = len(url_map)
    print(f"Total API entries before: {total_before}")
    print(f"Unique APIs (canonical):  {unique_count}")
    print(f"Duplicates to remove:     {total_before - unique_count}")

    # Pick single winning entry for each canonical URL
    winning_entries = set()
    for canon_key, entries in url_map.items():
        # Sort by category priority descending, then desc length descending
        best = max(
            entries,
            key=lambda e: (
                get_category_priority(e['cat']),
                e['desc_len']
            )
        )
        winning_entries.add((best['cat'], best['canon_key']))

    # Now rewrite each file keeping only its winning entries
    total_written = 0
    cat_stats = {}

    for file_path in md_files:
        cat_name = file_path.stem
        lines = file_path.read_text(encoding='utf-8').splitlines()

        new_lines = []
        count_kept = 0
        count_removed = 0

        for line in lines:
            line_str = line.strip()
            if line_str.startswith('|') and '[Link]' in line_str:
                m_url = re.search(r'\[Link\]\((https?://[^\)]+)\)', line_str)
                if m_url:
                    canon_key = canonical_url_key(m_url.group(1).strip())
                    if (cat_name, canon_key) in winning_entries:
                        # Prevent duplicate within the same file if any
                        winning_entries.remove((cat_name, canon_key))
                        new_lines.append(line)
                        count_kept += 1
                    else:
                        count_removed += 1
                    continue
            new_lines.append(line)

        cat_stats[cat_name] = (count_kept, count_removed)
        total_written += count_kept
        file_path.write_text('\n'.join(new_lines) + '\n', encoding='utf-8')

    print(f"\nSuccessfully rewritten all files!")
    print(f"Total APIs retained: {total_written} (expected {unique_count})")
    assert total_written == unique_count, f"Mismatch: {total_written} vs {unique_count}"

    print("\nSummary of deduplication across top categories:")
    for cat, (kept, removed) in sorted(cat_stats.items(), key=lambda x: x[1][1], reverse=True)[:15]:
        print(f"  {cat:25}: kept {kept:5}, removed {removed:5}")

if __name__ == '__main__':
    main()
