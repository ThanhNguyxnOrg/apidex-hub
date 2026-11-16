"""
Improved Link Checker for apidex-hub

Key improvements:
- Cloudflare protection detection
- Random User-Agent rotation
- Smart error categorization
- Broken URLs list output for CI workflow comparison
"""

import os
import re
import requests
import random
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import json

from link_health import classify_http_status, looks_like_waf_challenge


def extract_links_from_readme(file_path='../README.md'):
    """Extract all API links from README.md"""
    # Get script directory and go up one level
    script_dir = os.path.dirname(os.path.abspath(__file__))
    readme_path = os.path.join(os.path.dirname(script_dir), 'README.md')

    # Use provided path if it exists, otherwise use computed path
    if not os.path.exists(file_path):
        file_path = readme_path

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = r'\[Link\]\((https?://[^\)]+)\)'
    links = re.findall(pattern, content)
    return links


def fake_user_agent():
    """Random User-Agent to avoid bot detection"""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    ]
    return random.choice(user_agents)


def has_cloudflare_protection(resp):
    """Detect challenge pages and common WAF signals without bypassing them."""
    code = resp.status_code
    server = resp.headers.get('Server', '').lower()
    body = (resp.text or '').lower()

    if looks_like_waf_challenge(body):
        return True

    if code in [403, 429, 503]:
        if 'cloudflare' in server:
            return True
        if 'cf-ray' in resp.headers or 'cf-cache-status' in resp.headers:
            return True
        if any(flag in body for flag in ('security check', 'ddos protection', 'ray id:', 'cf-spinner')):
            return True

    return False


def check_link(url, timeout=8, max_retries=2):
    """
    Check if a link is accessible with retry logic
    Returns: dict with status info
    """
    for attempt in range(max_retries):
        try:
            ua = fake_user_agent()
            if "sec.gov" in url:
                ua = "APIDexHub/1.0 (contact@thanhnguyxn.org)"
            headers = {
                'User-Agent': ua,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }

            response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
            code = response.status_code

            waf_detected = has_cloudflare_protection(response)
            state, note = classify_http_status(code, waf_detected=waf_detected)
            return {
                'url': url,
                'status': code,
                'state': state,
                'note': note,
            }

        except requests.exceptions.SSLError:
            # SSL errors could be temporary (cert renewal in progress) or permanent
            # Mark as warning to avoid false positives
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            return {'url': url, 'status': None, 'state': 'warning', 'note': 'SSL error (may be temporary cert issue)'}
        except requests.exceptions.Timeout:
            # Retry on timeout
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            return {'url': url, 'status': None, 'state': 'warning', 'note': 'Timeout after retries (slow server)'}
        except requests.exceptions.ConnectionError as e:
            # Retry on connection errors (might be temporary)
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            # After all retries, classify based on error type
            error_str = str(e).lower()
            if 'getaddrinfo' in error_str or 'name or service not known' in error_str or 'nodename nor servname' in error_str:
                # DNS resolution failed after retries = domain is dead
                return {'url': url, 'status': None, 'state': 'broken', 'note': 'DNS dead - domain does not exist'}
            if 'connection refused' in error_str or 'connection reset' in error_str:
                return {'url': url, 'status': None, 'state': 'warning', 'note': 'Connection refused (may be IP blocking)'}
            # Other connection errors -> warning (could be IP blocking)
            return {'url': url, 'status': None, 'state': 'warning', 'note': 'Connection issue (may be temporary)'}
        except requests.exceptions.TooManyRedirects:
            return {'url': url, 'status': None, 'state': 'warning', 'note': 'Too many redirects (may be geo blocking)'}
        except Exception as e:
            return {'url': url, 'status': None, 'state': 'warning', 'note': f'Unknown error: {type(e).__name__}'}

    # Should never reach here, but just in case
    return {'url': url, 'status': None, 'state': 'error', 'note': 'Max retries exceeded'}

def parse_apis_from_dir(dir_path='../apis'):
    """Return only explicitly declared API endpoints; never probe documentation URLs."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    resolved_path = os.path.join(os.path.dirname(script_dir), 'apis')
    if not os.path.exists(dir_path):
        dir_path = resolved_path

    apis = []
    if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
        return apis

    files = sorted([f for f in os.listdir(dir_path) if f.endswith('.md')])
    for file in files:
        file_path = os.path.join(dir_path, file)
        with open(file_path, 'r', encoding='utf-8') as handle:
            content = handle.read()

        category_match = re.search(
            r'^##\s+(?:<a\s+id="[^"]+"\s*>\s*</a>\s*)?(\S+)\s+(.+)$',
            content,
            re.MULTILINE,
        )
        category = category_match.group(2).strip() if category_match else file.replace('.md', '').capitalize()

        for line in content.splitlines():
            stripped = line.strip()
            if not (stripped.startswith('|') and stripped.endswith('|')):
                continue
            cells = [part.strip() for part in stripped[1:-1].split('|')]
            if len(cells) != 6 or not cells[0]:
                continue
            if cells[0].strip('* ').lower() in {'api name', 'name'}:
                continue
            if all(re.fullmatch(r':?-{3,}:?', cell.replace(' ', '')) for cell in cells):
                continue

            endpoint_match = re.search(
                r'\[[^\]]+\]\((https?://[^)]+)\)',
                cells[4],
                re.IGNORECASE,
            )
            if not endpoint_match:
                continue

            name = re.sub(r'\*\*(.+?)\*\*', r'\1', cells[0]).strip()
            docs_match = re.search(
                r'\[[^\]]+\]\((https?://[^)]+)\)',
                cells[5],
                re.IGNORECASE,
            )
            apis.append({
                'name': name,
                'category': category,
                'url': endpoint_match.group(1).strip(),
                'documentation_url': docs_match.group(1).strip() if docs_match else '',
            })
    return apis


def main():
    print("API Endpoint Health Checker")
    print("=" * 80)

    # Extract all APIs
    apis = parse_apis_from_dir()
    if not apis:
        raise SystemExit('ERROR: No explicit API Endpoint URLs are recorded. Refusing to publish an all-zero health report or close incidents.')
    
    # Extract unique URLs to optimize checking
    unique_urls = sorted(list(set(api['url'] for api in apis)))

    print(f"Found {len(apis)} total API endpoints ({len(unique_urls)} unique URLs)")
    print(f"Checking links...\n")

    # Check unique links with threading
    url_results = {}
    with ThreadPoolExecutor(max_workers=60) as executor:
        future_to_url = {executor.submit(check_link, url): url for url in unique_urls}

        completed = 0
        for future in as_completed(future_to_url):
            result = future.result()
            completed += 1
            url_results[result['url']] = result

            # Display with icons
            icons = {
                'working': '[OK]',
                'protected': '[PROTECTED]',
                'warning': '[WARN]',
                'error': '[ERR]',
                'broken': '[DEAD]',
                'unknown': '[?]'
            }
            state = result['state']
            icon = icons.get(state, '?')
            status_str = f"HTTP {result['status']}" if result['status'] else "N/A"
            print(f"[{completed}/{len(unique_urls)}] {icon:12} {status_str:12} {result['note']}")
            print(f"    {result['url']}")

    # Map check results back to all APIs
    results = {
        'working': [],
        'protected': [],
        'warning': [],
        'error': [],
        'broken': [],
        'unknown': []
    }
    
    for api in apis:
        url_res = url_results.get(api['url'])
        if url_res:
            state = url_res['state']
            results[state].append({
                'name': api['name'],
                'category': api['category'],
                'url': api['url'],
                'status': url_res['status'],
                'state': state,
                'note': url_res['note']
            })

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    total_working = len(results['working'])

    print(f"[OK] Working: {total_working}")
    print(f"[PROTECTED] Access restricted / WAF (availability unconfirmed): {len(results['protected'])}")
    print(f"[WARN] Warnings: {len(results['warning'])}")
    print(f"[ERR] Errors: {len(results['error'])}")
    print(f"[DEAD] Broken: {len(results['broken'])}")
    print(f"[?] Unknown: {len(results['unknown'])}")
    print(f"\nConfirmed successful responses: {total_working}/{len(apis)}")
    print(f"Protected/inconclusive responses: {len(results['protected'])}")

    # Show only truly broken APIs
    if results['broken']:
        print("\n" + "=" * 80)
        print("TRULY BROKEN API ENDPOINTS (Manual Review Needed)")
        print("=" * 80)
        for r in sorted(results['broken'], key=lambda x: x['name']):
            print(f"\n[DEAD] {r['name']} ({r['category']})")
            print(f"       URL: {r['url']}")
            print(f"       {r['note']}")

    # Save report
    script_dir = os.path.dirname(os.path.abspath(__file__))
    report_path = os.path.join(script_dir, 'link_check_report.txt')
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("API ENDPOINT HEALTH REPORT\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Date: {now}\n")
        f.write(f"Total: {len(apis)}\n")
        f.write(f"Working: {len(results['working'])}\n")
        f.write(f"Protected: {len(results['protected'])}\n")
        f.write(f"Warnings: {len(results['warning'])}\n")
        f.write(f"Errors: {len(results['error'])}\n")
        f.write(f"Broken: {len(results['broken'])}\n")
        f.write(f"Unknown: {len(results['unknown'])}\n\n")

        if results['broken']:
            f.write("BROKEN APIS:\n")
            f.write("-" * 80 + "\n")
            for r in sorted(results['broken'], key=lambda x: x['name']):
                f.write(f"\n{r['name']} ({r['category']})\n  -> URL: {r['url']}\n  -> Note: {r['note']}\n")

        if results['error']:
            f.write("\nERROR APIS:\n")
            f.write("-" * 80 + "\n")
            for r in sorted(results['error'], key=lambda x: x['name']):
                f.write(f"\n{r['name']} ({r['category']})\n  -> URL: {r['url']}\n  -> Note: {r['note']}\n")

        if results['unknown']:
            f.write("\nUNKNOWN APIS:\n")
            f.write("-" * 80 + "\n")
            for r in sorted(results['unknown'], key=lambda x: x['name']):
                f.write(f"\n{r['name']} ({r['category']})\n  -> URL: {r['url']}\n  -> Note: {r['note']}\n")

        if results['warning']:
            f.write("\nWARNING APIS:\n")
            f.write("-" * 80 + "\n")
            for r in sorted(results['warning'], key=lambda x: x['name']):
                f.write(f"\n{r['name']} ({r['category']})\n  -> URL: {r['url']}\n  -> Note: {r['note']}\n")

    # Save broken URLs list formatted as: URL | Name (Category) - Reason
    broken_list_path = os.path.join(script_dir, 'broken_urls.txt')
    with open(broken_list_path, 'w', encoding='utf-8') as f:
        for r in sorted(results['broken'], key=lambda x: x['url']):
            f.write(f"{r['url']} | {r['name']} ({r['category']}) - {r['note']}\n")

    # Save error URLs list formatted as: URL | Name (Category) - Reason
    error_list_path = os.path.join(script_dir, 'error_urls.txt')
    with open(error_list_path, 'w', encoding='utf-8') as f:
        for r in sorted(results['error'], key=lambda x: x['url']):
            f.write(f"{r['url']} | HTTP {r['status']} | {r['name']} ({r['category']}) - {r['note']}\n")

    # Save warning URLs list
    warning_list_path = os.path.join(script_dir, 'warning_urls.txt')
    with open(warning_list_path, 'w', encoding='utf-8') as f:
        for r in sorted(results['warning'], key=lambda x: x['url']):
            status_str = f"HTTP {r['status']}" if r['status'] else "N/A"
            f.write(f"{r['url']} | {status_str} | {r['name']} ({r['category']}) - {r['note']}\n")

    # Save unknown URLs list
    unknown_list_path = os.path.join(script_dir, 'unknown_urls.txt')
    with open(unknown_list_path, 'w', encoding='utf-8') as f:
        for r in sorted(results['unknown'], key=lambda x: x['url']):
            status_str = f"HTTP {r['status']}" if r['status'] else "N/A"
            f.write(f"{r['url']} | {status_str} | {r['name']} ({r['category']}) - {r['note']}\n")

    # Save protected URLs list
    protected_list_path = os.path.join(script_dir, 'protected_urls.txt')
    with open(protected_list_path, 'w', encoding='utf-8') as f:
        for r in sorted(results['protected'], key=lambda x: x['url']):
            status_str = f"HTTP {r['status']}" if r['status'] else "N/A"
            f.write(f"{r['url']} | {status_str} | {r['name']} ({r['category']}) - {r['note']}\n")

    # Save queue for Playwright verification
    verify_queue_path = os.path.join(script_dir, 'verify_queue.json')
    verify_queue = []
    # Browser rechecks transient and potentially dead responses; protected responses stay inconclusive.
    for state in ['broken', 'error', 'warning', 'unknown']:
        verify_queue.extend(results[state])
    
    with open(verify_queue_path, 'w', encoding='utf-8') as f:
        json.dump(verify_queue, f, indent=2)

    # Dump full results so Stage 2 can update categories and rewrite reports
    results_json_path = os.path.join(script_dir, 'results.json')
    with open(results_json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print(f"\nReport saved to: link_check_report.txt")
    print(f"Verify Queue list: verify_queue.json ({len(verify_queue)} endpoint checks for Stage 2)")
    print("\nNote: 401/403/418 access restrictions and 429 rate limits are not proof of availability or death.")

    return 0


if __name__ == "__main__":
    exit(main())
