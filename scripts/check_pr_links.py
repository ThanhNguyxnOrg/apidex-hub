#!/usr/bin/env python3
"""
scripts/check_pr_links.py — Check only NEWLY added or modified links in a Pull Request.
Bypasses full checking of the entire API catalog to run quickly and efficiently in PR CI pipelines.
Uses a hybrid checking mechanism: requests (Stage 1) -> Playwright (Stage 2) for WAF bypass.
Also checks for duplicate API URLs against the existing repository APIs.
"""

import subprocess
import re
import sys
import requests
from pathlib import Path
from playwright.sync_api import sync_playwright

def get_added_urls():
    # 1. Fetch main branch from origin to ensure origin/main exists in depth-1 clones
    subprocess.run(["git", "fetch", "origin", "main", "--depth=1"], capture_output=True)
    
    # 2. Run git diff against the apis/ directory
    res = subprocess.run(
        ["git", "diff", "origin/main...HEAD", "-U0", "--", "apis/"],
        capture_output=True,
        text=True
    )
    
    # Fallback to compare against 'main' if origin/main is not fetched or fails
    if res.returncode != 0:
        res = subprocess.run(
            ["git", "diff", "main...HEAD", "-U0", "--", "apis/"],
            capture_output=True,
            text=True
        )
    
    if res.returncode != 0:
        print("WARNING: Could not run git diff. Check if main branch is available.")
        return []

    added_lines = []
    for line in res.stdout.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            added_lines.append(line[1:]) # Strip leading '+'

    # Extract all http/https links from added markdown table rows
    urls = []
    url_pattern = re.compile(r'https?://[^\s)\]|]+')
    for line in added_lines:
        if '|' in line:  # Only parse links within markdown tables
            matches = url_pattern.findall(line)
            for m in matches:
                clean_url = m.strip()
                if clean_url not in urls:
                    urls.append(clean_url)
    return urls

def get_existing_urls_at_base():
    """
    Get all unique URLs currently existing in the apis/ directory on the main branch (base of PR).
    """
    # Fetch origin/main branch to ensure base exists
    subprocess.run(["git", "fetch", "origin", "main", "--depth=1"], capture_output=True)
    
    # List files in apis/ directory on base branch
    res = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", "origin/main", "apis/"],
        capture_output=True,
        text=True
    )
    
    base_branch = "origin/main"
    # Fallback to local main
    if res.returncode != 0 or not res.stdout.strip():
        res = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", "main", "apis/"],
            capture_output=True,
            text=True
        )
        base_branch = "main"
        
    if res.returncode != 0 or not res.stdout.strip():
        print("WARNING: Could not fetch base apis/ directory for duplicate check. Skipping duplicate validation.")
        return set()
        
    existing_urls = set()
    url_pattern = re.compile(r'https?://[^\s)\]|]+')
    
    files = res.stdout.splitlines()
    for file in files:
        show_res = subprocess.run(
            ["git", "show", f"{base_branch}:{file}"],
            capture_output=True,
            text=True
        )
        if show_res.returncode == 0:
            for line in show_res.stdout.splitlines():
                if '|' in line:
                    matches = url_pattern.findall(line)
                    for m in matches:
                        existing_urls.add(m.strip().lower())
    return existing_urls


def verify_with_playwright(browser, url):
    """
    Returns (is_working, status_code, note) using Playwright Chromium headless browser.
    """
    from playwright_stealth import stealth_sync
    context = None
    page = None
    try:
        context = browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        stealth_sync(page)
        
        last_response = [None]
        
        def handle_response(r):
            if r.frame == page.main_frame and r.request.resource_type == "document":
                last_response[0] = r
                
        page.on("response", handle_response)
        
        # Fast check: wait for response headers first (wait_until='commit')
        response = page.goto(url, wait_until='commit', timeout=8000)
        
        # Wait a bit for initial load
        page.wait_for_timeout(3000)
        
        # Check if there is a Cloudflare Turnstile challenge iframe
        has_cf_iframe = False
        try:
            for frame in page.frames:
                if "challenges.cloudflare.com" in frame.url:
                    has_cf_iframe = True
                    break
        except Exception:
            pass

        if has_cf_iframe:
            print(f"  [Playwright] Detected Cloudflare Challenge iframe for {url}. Attempting to solve...")
            try:
                clicked = False
                for frame in page.frames:
                    if "challenges.cloudflare.com" in frame.url:
                        checkbox = frame.locator('input[type="checkbox"], span.mark, .cb-i, #challenge-stage, .ctp-checkbox-label')
                        if checkbox.count() > 0:
                            checkbox.first.click(timeout=3000)
                            print("  [Playwright] Clicked Turnstile checkbox element.")
                            clicked = True
                            break
                
                # Fallback: click the iframe container directly
                if not clicked:
                    iframe_element = page.locator('iframe[src*="challenges.cloudflare.com"]')
                    if iframe_element.count() > 0:
                        iframe_element.first.click(timeout=3000)
                        print("  [Playwright] Clicked Turnstile iframe directly.")
            except Exception as e:
                print(f"  [Playwright] Click bypass failed: {e}")
                
            # Wait longer for redirect / page verification
            page.wait_for_timeout(5000)
        else:
            # Standard wait for redirect or load
            page.wait_for_timeout(2000)
            
        final_resp = last_response[0] if last_response[0] else response
        status = final_resp.status if final_resp else None
        
        if status and status < 400:
            page.close()
            context.close()
            return True, status, "Playwright: Verified working"
            
        # If status is >= 400, check if it is a WAF challenge
        title = page.title().lower()
        try:
            content = page.content().lower()
        except:
            content = ""
            
        is_waf_code = status in [403, 429, 503]
        if is_waf_code:
            cloudflare_indicators = ['just a moment', 'cloudflare', 'attention required', 'security check', 'ddos protection']
            if any(indicator in title or indicator in content for indicator in cloudflare_indicators):
                page.close()
                context.close()
                return False, status, "Playwright: Blocked by Cloudflare Challenge (unsolved)"
                
        page.close()
        context.close()
        return False, status, f"Playwright: Failed with HTTP {status if status else 'Unknown'}"
            
    except Exception as e:
        if page:
            try: page.close()
            except: pass
        if context:
            try: context.close()
            except: pass
        clean_err = str(e).replace('\n', ' ; ')
        return False, None, f"Playwright Exception: {clean_err}"

def check_url(browser, url):
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    if "sec.gov" in url:
        ua = "AwesomeFreeApis/1.0 (contact@thanhnguyxn.org)"
    headers = {
        'User-Agent': ua,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    
    # Stage 1: Fast HTTP request
    try:
        res = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        if res.status_code < 400:
            print(f"  🟢 [GET] {url} - Status {res.status_code} (Working)")
            return True, res.status_code, "GET request successful"
        else:
            print(f"  ⚠️ [GET] {url} returned HTTP {res.status_code}. Retrying with Playwright...")
    except Exception as e:
        print(f"  ⚠️ [GET] {url} failed: {e}. Retrying with Playwright...")
        
    # Stage 2: Playwright fallback
    is_ok, status, note = verify_with_playwright(browser, url)
    if is_ok:
        print(f"  🟢 [Playwright] {url} - Status {status} ({note})")
    else:
        print(f"  🔴 [FAILED] {url} - Status {status} ({note})")
    return is_ok, status, note


def save_pr_report(added_urls, failed_links, duplicate_links):
    script_dir = Path(__file__).resolve().parent
    report_path = script_dir / 'pr_link_check_report.txt'
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("PR NEW LINK CHECK REPORT\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total New Links Checked: {len(added_urls)}\n")
        f.write(f"Working: {len(added_urls) - len(failed_links) - len(duplicate_links)}\n")
        f.write(f"Duplicate: {len(duplicate_links)}\n")
        f.write(f"Broken: {len(failed_links)}\n\n")
        
        if duplicate_links:
            f.write("❌ DUPLICATE LINKS FOUND (Already exists in repository):\n")
            f.write("-" * 80 + "\n")
            for url in duplicate_links:
                f.write(f"- {url} | Status: DUPLICATE | Error: API already listed in the repository\n")
            f.write("\n")
            
        if failed_links:
            f.write("❌ BROKEN LINKS FOUND:\n")
            f.write("-" * 80 + "\n")
            for url, status, note in failed_links:
                f.write(f"- {url} | Status: {status} | Error: {note}\n")
        
        if not failed_links and not duplicate_links:
            f.write("🟢 All new links are working, unique, and verified!\n")

def main():
    print("=== Identifying New APIs Added in PR ===")
    added_urls = get_added_urls()
    
    if not added_urls:
        print("Done! No new API links were added to the apis/ directory in this Pull Request.")
        # Write empty pass report
        save_pr_report([], [], [])
        return 0
        
    print(f"Found {len(added_urls)} new API link(s) to verify:")
    for url in added_urls:
        print(f" - {url}")
        
    print("\n=== Checking for Duplicate APIs ===")
    existing_urls = get_existing_urls_at_base()
    duplicate_links = []
    unique_added_urls = []
    
    for url in added_urls:
        if url.lower() in existing_urls:
            print(f"  ❌ [DUPLICATE] {url} - already exists in the repository")
            duplicate_links.append(url)
        else:
            unique_added_urls.append(url)
        
    print("\n=== Verifying New Links ===")
    failed_links = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for url in unique_added_urls:
            is_ok, status, note = check_url(browser, url)
            if not is_ok:
                failed_links.append((url, status, note))
        browser.close()
            
    print("\n=== Result Summary ===")
    save_pr_report(added_urls, failed_links, duplicate_links)
    
    has_errors = False
    if duplicate_links:
        print(f"❌ Duplicate API(s) detected! {len(duplicate_links)} link(s) already exist in the repository.")
        has_errors = True
    if failed_links:
        print(f"❌ Broken API(s) detected! {len(failed_links)} link(s) failed validation.")
        has_errors = True
        
    if has_errors:
        print("\nPlease fix these issues before merging the Pull Request.")
        return 1
    else:
        print("🟢 All new API links are verified, unique, and working correctly!")
        return 0

if __name__ == "__main__":
    sys.exit(main())
