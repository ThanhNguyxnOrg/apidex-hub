#!/usr/bin/env python3
"""
parse_readme.py — Parse README.md → apis.json for the APIDex Hub website.

Auto-extracts:
  - All categories (name, emoji, id, anchor)
  - All APIs per category (name, description, auth, https, link)
  - Global stats (total APIs, total categories, no-auth count, https percentage)

Usage:
  python scripts/parse_readme.py
  python scripts/parse_readme.py --readme apis --output site/src/data/apis.json
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
    """Parse a 5-column legacy row or canonical 6-column API/documentation row."""
    parts = [p.strip().replace(r'\|', '—') for p in re.split(r'(?<!\\)\|', line)]
    # Remove only the delimiter cells. Preserve an empty API Endpoint cell.
    if parts and parts[0] == "":
        parts.pop(0)
    if parts and parts[-1] == "":
        parts.pop()

    if len(parts) not in (5, 6):
        return None

    name_raw, description, auth_raw, https_raw = parts[0], parts[1], parts[2], parts[3]
    if len(parts) == 5:
        endpoint_raw, documentation_raw = "", parts[4]
    else:
        endpoint_raw, documentation_raw = parts[4], parts[5]

    name = re.sub(r'\*\*(.+?)\*\*', r'\1', name_raw).strip()
    if not name or name.startswith('---') or name.startswith(':---') or name == 'API Name' or name == 'Name':
        return None

    auth_raw_lower = auth_raw.lower()
    if "oauth" in auth_raw_lower or "🔐" in auth_raw:
        auth = "OAuth"
    elif "apikey" in auth_raw_lower or "🔑" in auth_raw or "api key" in auth_raw_lower:
        auth = "apiKey"
    else:
        auth = "No"

    https_raw_lower = https_raw.lower()
    https = "✅" in https_raw or "yes" in https_raw_lower or "true" in https_raw_lower

    endpoint_match = re.search(r'\[[^\]]+\]\((https?://[^)]+)\)', endpoint_raw, re.IGNORECASE)
    docs_match = re.search(r'\[[^\]]+\]\((https?://[^)]+)\)', documentation_raw, re.IGNORECASE)
    endpoint = endpoint_match.group(1).strip() if endpoint_match else ""
    documentation_url = docs_match.group(1).strip() if docs_match else ""

    return {
        "name": name,
        "description": description,
        "auth": auth,
        "https": https,
        "endpoint": endpoint,
        "documentation_url": documentation_url,
        "link": documentation_url,
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
    api_key_count = sum(
        1 for cat in categories for api in cat['apis'] if api['auth'] == 'apiKey'
    )
    oauth_count = sum(
        1 for cat in categories for api in cat['apis'] if api['auth'] == 'OAuth'
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
            "api_key_count": api_key_count,
            "oauth_count": oauth_count,
            "https_count": https_count,
            "https_percentage": https_pct,
            "api_endpoint_count": sum(1 for cat in categories for api in cat["apis"] if api.get("endpoint")),
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
    parser.add_argument('--output', default='site/src/data/apis.json', help='Output JSON path')
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

    # Keep the previous generated_at when the parsed data is unchanged.
    # parse_readme() stamps the current time on every run, so without
    # this the output file differs on every run and the deploy workflow
    # commits a timestamp-only change. Real data changes still get a
    # fresh timestamp (and a commit).
    try:
        previous = json.loads(output_path.read_text(encoding='utf-8'))
    except (FileNotFoundError, ValueError, OSError):
        previous = None
    if isinstance(previous, dict):
        previous_meta = previous.get('meta', {})
        if isinstance(previous_meta, dict):
            old_meta = {k: v for k, v in previous_meta.items() if k != 'generated_at'}
            new_meta = {k: v for k, v in data['meta'].items() if k != 'generated_at'}
            if old_meta == new_meta and previous.get('categories') == data.get('categories'):
                data['meta']['generated_at'] = previous_meta.get(
                    'generated_at', data['meta']['generated_at']
                )
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
                r'\b[\d,]+(?:\+)?(?=\s+[pP]ublic\s+[aA][pP][iI]s)',
                f"{total_apis:,}",
                content,
                flags=re.IGNORECASE
            )
            index_path.write_text(updated_content, encoding='utf-8')
            print(f"  Successfully updated index.html with {total_apis:,} APIs")
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
                r'(\bdatabase of \*\*)[\d,]+(?:\+)?(?=\*\* public endpoints across \*\*)',
                f"\\g<1>{total_apis:,}",
                content
            )
            updated_content = re.sub(
                r'(public endpoints across \*\*)[\d,]+(?=\*\* categories)',
                f"\\g<1>{total_categories}",
                updated_content
            )
            readme_file_path.write_text(updated_content, encoding='utf-8')
            print(f"  Successfully updated README.md with {total_apis:,} APIs and {total_categories} categories")
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
