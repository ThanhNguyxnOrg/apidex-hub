#!/usr/bin/env python3
"""
parse_readme.py — Parse README.md → apis.json for the Awesome Free APIs website.

Auto-extracts:
  - All categories (name, emoji, id, anchor)
  - All APIs per category (name, description, auth, https, link)
  - Global stats (total APIs, total categories, no-auth count, https percentage)

Usage:
  python scripts/parse_readme.py
  python scripts/parse_readme.py --readme README.md --output website/data/apis.json
"""

import re
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone


def parse_category_header(line: str):
    """Extract category info from a markdown header like: ## <a id="animals"></a>🐶 Animals"""
    # Match: ## <a id="..."></a>EMOJI Name
    match = re.match(
        r'^##\s+(?:<a\s+id="([^"]+)"\s*>\s*</a>\s*)?(\S+)\s+(.+)$',
        line.strip()
    )
    if match:
        anchor = match.group(1) or ""
        emoji = match.group(2)
        name = match.group(3).strip()
        return {
            "id": anchor or re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-'),
            "emoji": emoji,
            "name": name,
        }
    return None


def parse_api_row(line: str):
    """Extract API info from a markdown table row."""
    # Split by | and clean up
    parts = [p.strip() for p in line.split('|')]
    # Remove empty first/last from leading/trailing |
    parts = [p for p in parts if p]

    if len(parts) < 5:
        return None

    name_raw, description, auth_raw, https_raw, link_raw = parts[0], parts[1], parts[2], parts[3], parts[4]

    # Extract name (remove bold **)
    name = re.sub(r'\*\*(.+?)\*\*', r'\1', name_raw).strip()
    if not name or name.startswith('---') or name.startswith(':---') or name == 'API Name' or name == 'Name':
        return None

    # Extract auth type (case-insensitive check)
    auth_raw_lower = auth_raw.lower()
    if "oauth" in auth_raw_lower or "🔐" in auth_raw:
        auth = "OAuth"
    elif "apikey" in auth_raw_lower or "🔑" in auth_raw or "api key" in auth_raw_lower:
        auth = "apiKey"
    else:
        auth = "No"

    # Extract HTTPS (case-insensitive check)
    https_raw_lower = https_raw.lower()
    https = "✅" in https_raw or "yes" in https_raw_lower or "true" in https_raw_lower

    # Extract link URL
    link_match = re.search(r'\[.*?\]\((.*?)\)', link_raw)
    link = link_match.group(1) if link_match else ""

    return {
        "name": name,
        "description": description,
        "auth": auth,
        "https": https,
        "link": link,
    }


def parse_readme(readme_path: str):
    """Parse the entire README.md or a directory of markdown files and return structured data."""
    path = Path(readme_path)
    if path.is_dir():
        md_files = sorted(list(path.glob('*.md')))
        content_parts = []
        for f in md_files:
            content_parts.append(f.read_text(encoding='utf-8'))
        content = '\n\n'.join(content_parts)
    else:
        content = path.read_text(encoding='utf-8')
        
    lines = content.split('\n')

    categories = []
    current_category = None

    # Sections to skip (not API categories)
    skip_sections = {
        "general-api-usage-guide", "general api usage guide",
    }

    for line in lines:
        stripped = line.strip()

        # Check for category header (## level)
        if stripped.startswith('## '):
            cat = parse_category_header(stripped)
            if cat:
                # Skip non-API sections
                cat_id_lower = cat['id'].lower()
                cat_name_lower = cat['name'].lower()
                if cat_id_lower in skip_sections or 'table of contents' in cat_name_lower or 'usage guide' in cat_name_lower or 'code examples' in cat_name_lower:
                    current_category = None
                    continue

                cat['apis'] = []
                categories.append(cat)
                current_category = cat
            else:
                current_category = None
            continue

        # Parse API table rows
        if current_category and stripped.startswith('|'):
            api = parse_api_row(stripped)
            if api:
                current_category['apis'].append(api)

    # Calculate stats
    total_apis = sum(len(cat['apis']) for cat in categories)
    total_categories = len(categories)
    no_auth_count = sum(
        1 for cat in categories for api in cat['apis'] if api['auth'] == 'No'
    )
    https_count = sum(
        1 for cat in categories for api in cat['apis'] if api['https']
    )
    https_pct = round((https_count / total_apis * 100)) if total_apis > 0 else 0

    # Build output
    output = {
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source": "README.md",
            "total_apis": total_apis,
            "total_categories": total_categories,
            "no_auth_count": no_auth_count,
            "https_count": https_count,
            "https_percentage": https_pct,
        },
        "categories": []
    }

    for cat in categories:
        output["categories"].append({
            "id": cat['id'],
            "emoji": cat['emoji'],
            "name": cat['name'],
            "api_count": len(cat['apis']),
            "apis": cat['apis'],
        })

    return output


def main():
    parser = argparse.ArgumentParser(description='Parse README.md or apis directory → apis.json')
    parser.add_argument('--readme', default='apis', help='Path to README.md or apis directory')
    parser.add_argument('--output', default='website/data/apis.json', help='Output JSON path')
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent

    # Resolve paths
    readme_path = Path(args.readme)
    if not readme_path.is_absolute():
        readme_path = repo_root / args.readme

    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = repo_root / args.output

    if not readme_path.exists():
        print(f"ERROR: README not found at {readme_path}")
        return 1

    print(f"Parsing {readme_path}...")
    data = parse_readme(str(readme_path))

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    total_apis = data['meta']['total_apis']
    
    # Update index.html dynamically with the parsed count
    index_path = repo_root / 'site/index.html'
    if index_path.exists():
        print(f"Updating count in {index_path}...")
        try:
            content = index_path.read_text(encoding='utf-8')
            updated_content = re.sub(
                r'\b\d+\+(?=\s+[fF]ree\s+[pP]ublic)',
                f"{total_apis}+",
                content
            )
            index_path.write_text(updated_content, encoding='utf-8')
            print(f"  Successfully updated index.html with {total_apis}+ APIs")
        except Exception as e:
            print(f"  WARNING: Failed to update index.html: {e}")
    else:
        print(f"  WARNING: index.html not found at {index_path}")

    # Update README.md dynamically with the parsed count and category count
    readme_file_path = repo_root / 'README.md'
    if readme_file_path.exists():
        print(f"Updating count in {readme_file_path}...")
        try:
            content = readme_file_path.read_text(encoding='utf-8')
            total_categories = data['meta']['total_categories']
            updated_content = re.sub(
                r'(\bdatabase of \*\*)[\d,]+\+(?=\*\* free public APIs across \*\*)',
                f"\\g<1>{total_apis:,}+",
                content
            )
            updated_content = re.sub(
                r'(free public APIs across \*\*)[\d,]+(?=\*\* categories)',
                f"\\g<1>{total_categories}",
                updated_content
            )
            readme_file_path.write_text(updated_content, encoding='utf-8')
            print(f"  Successfully updated README.md with {total_apis}+ APIs and {total_categories} categories")
        except Exception as e:
            print(f"  WARNING: Failed to update README.md: {e}")
    else:
        print(f"  WARNING: README.md not found at {readme_file_path}")

    meta = data['meta']
    print(f"Done! Generated {output_path}")
    print(f"  {meta['total_apis']} APIs across {meta['total_categories']} categories")
    print(f"  {meta['no_auth_count']} require no auth")
    print(f"  {meta['https_percentage']}% use HTTPS")

    return 0


if __name__ == '__main__':
    exit(main())
