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
    """
    Detect Cloudflare or similar bot protection
    """
    code = resp.status_code
    server = resp.headers.get('Server', '').lower()

    cloudflare_flags = [
        'cloudflare',
        'security check',
        'please wait...',
        'checking your browser',
        'ddos protection',
        'ray id:',
        '_cf_chl',
        'cf-spinner',
        'just a moment'
    ]

    # Only check if status code is typical for WAF (403, 429, 503, or CF 52x errors)
    is_waf_code = code in [403, 429, 503] or (520 <= code <= 527)
    if not is_waf_code:
        return False

    # Check Server header
    if 'cloudflare' in server:
        return True

    # Check Cloudflare specific headers
    if 'cf-ray' in resp.headers or 'cf-cache-status' in resp.headers:
        return True

    # Check HTML content
    html = resp.text.lower()
    if any(flag in html for flag in cloudflare_flags):
        return True

    return False


def check_link(url, timeout=15, max_retries=3):
    """
    Check if a link is accessible with retry logic
    Returns: dict with status info
    """
    for attempt in range(max_retries):
        try:
            ua = fake_user_agent()
            if "sec.gov" in url:
                ua = "AwesomeFreeApis/1.0 (contact@thanhnguyxn.org)"
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

            # Check for bot protection
            if code >= 400 and has_cloudflare_protection(response):
                return {
                    'url': url,
                    'status': code,
                    'state': 'protected',
                    'note': 'Bot protection (Cloudflare/similar) - API likely works'
                }

            # Interpret status codes
            # Note: 3xx won't appear here because allow_redirects=True
            # follows redirects automatically. The final status is what we get.
            if code in [200, 201, 202, 204]:
                return {'url': url, 'status': code, 'state': 'working', 'note': 'OK'}
            elif code == 429:
                return {'url': url, 'status': code, 'state': 'warning', 'note': 'Rate limited (HTTP 429)'}
            elif code == 401:
                return {'url': url, 'status': code, 'state': 'protected', 'note': 'Unauthorized (HTTP 401) - access restricted'}
            elif code == 403:
                return {'url': url, 'status': code, 'state': 'protected', 'note': 'Forbidden (HTTP 403) - restricted access'}

            elif code in [400, 405, 406]:
                return {'url': url, 'status': code, 'state': 'working', 'note': 'API up (Invalid request/Method)'}
            elif code == 404:
                return {'url': url, 'status': code, 'state': 'broken', 'note': 'Not found - likely dead'}
            elif code == 410:
                return {'url': url, 'status': code, 'state': 'broken', 'note': 'Gone - confirmed dead'}
            elif code in [500, 502, 504, 521, 522, 523]:
                return {'url': url, 'status': code, 'state': 'error', 'note': 'Server error (may be temporary)'}
            elif code == 503:
                # 503 could be Cloudflare or temporary, treat as warning
                if has_cloudflare_protection(response):
                    return {'url': url, 'status': code, 'state': 'protected', 'note': 'Cloudflare protection (503)'}
                return {'url': url, 'status': code, 'state': 'warning', 'note': 'Service unavailable (503) - may be temporary'}
            else:
                return {'url': url, 'status': code, 'state': 'unknown', 'note': f'HTTP {code}'}

        except requests.exceptions.SSLError:
            # SSL errors could be temporary (cert renewal in progress) or permanent
            # Mark as warning to avoid false positives
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            return {'url': url, 'status': None, 'state': 'warning', 'note': 'SSL error (may be temporary cert issue)'}
        except requests.exceptions.Timeout:
            # Retry on timeout
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            return {'url': url, 'status': None, 'state': 'warning', 'note': 'Timeout after retries (slow server)'}
        except requests.exceptions.ConnectionError as e:
            # Retry on connection errors (might be temporary)
            if attempt < max_retries - 1:
                time.sleep(2)
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
    """Parse all APIs from the apis/ directory"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    resolved_path = os.path.join(os.path.dirname(script_dir), 'apis')
    if not os.path.exists(dir_path):
        dir_path = resolved_path
        
    apis = []
    
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        files = sorted([f for f in os.listdir(dir_path) if f.endswith('.md')])
        for file in files:
            file_path = os.path.join(dir_path, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract category name and emoji
            cat_match = re.search(r'^##\s+(?:<a\s+id="[^"]+"\s*>\s*</a>\s*)?(\S+)\s+(.+)$', content, re.MULTILINE)
            category = cat_match.group(2).strip() if cat_match else file.replace('.md', '').capitalize()
            
            lines = content.split('\n')
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('|'):
                    parts = [p.strip() for p in stripped.split('|')]
                    if parts[0] == '': parts.pop(0)
                    if parts and parts[-1] == '': parts.pop()
                    
                    if len(parts) >= 5:
                        name_raw = parts[0]
                        name = re.sub(r'\*\*(.+?)\*\*', r'\1', name_raw).strip()
                        if not name or name.startswith('---') or name.startswith(':---') or name == 'API Name' or name == 'Name':
                            continue
                        
                        link_raw = parts[4]
                        link_match = re.search(r'\[Link\]\((https?://[^\)]+)\)', link_raw)
                        if link_match:
                            url = link_match.group(1).strip()
                            apis.append({
                                'name': name,
                                'category': category,
                                'url': url
                            })
    return apis


def main():
    print("Link Checker (based on public-apis approach)")
    print("=" * 80)

    # Extract all APIs
    apis = parse_apis_from_dir()
    
    # Extract unique URLs to optimize checking
    unique_urls = sorted(list(set(api['url'] for api in apis)))

    print(f"Found {len(apis)} total APIs ({len(unique_urls)} unique URLs)")
    print(f"Checking links...\n")

    # Check unique links with threading
    url_results = {}
    with ThreadPoolExecutor(max_workers=15) as executor:
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

    total_ok = len(results['working']) + len(results['protected'])

    print(f"[OK] Working: {len(results['working'])}")
    print(f"[PROTECTED] Bot protection (403/429): {len(results['protected'])}")
    print(f"[WARN] Warnings: {len(results['warning'])}")
    print(f"[ERR] Errors: {len(results['error'])}")
    print(f"[DEAD] Broken: {len(results['broken'])}")
    print(f"[?] Unknown: {len(results['unknown'])}")
    
    if len(apis) > 0:
        print(f"\nHealthy: {total_ok}/{len(apis)} ({total_ok/len(apis)*100:.1f}%)")
    else:
        print(f"\nHealthy: {total_ok}/0 (0.0%)")

    # Show only truly broken APIs
    if results['broken']:
        print("\n" + "=" * 80)
        print("TRULY BROKEN APIS (Manual Review Needed)")
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
        f.write("LINK CHECK REPORT (API-mapped)\n")
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
    # Add all non-working APIs to the queue to be double-checked by Playwright
    for state in ['broken', 'error', 'warning', 'protected']:
        verify_queue.extend(results[state])
    
    with open(verify_queue_path, 'w', encoding='utf-8') as f:
        json.dump(verify_queue, f, indent=2)

    # Dump full results so Stage 2 can update categories and rewrite reports
    results_json_path = os.path.join(script_dir, 'results.json')
    with open(results_json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print(f"\nReport saved to: link_check_report.txt")
    print(f"Verify Queue list: verify_queue.json ({len(verify_queue)} APIs for Stage 2)")
    print("\nNote: 403/429 (Protected) = Bot protection - APIs still work!")

    return 0


if __name__ == "__main__":
    exit(main())
