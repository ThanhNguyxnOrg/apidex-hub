# API Maintenance Scripts

These scripts maintain the APIDex catalog. The Markdown files under `apis/` are the source of truth; generated website data and counts are synchronized by `scripts/parse_readme.py`.

## Monitoring model

APIDex deliberately separates two different questions:

1. **API endpoint health** — does an explicitly recorded API Endpoint respond?
2. **Provider lifecycle and documentation health** — does the official documentation page contain an explicit shutdown notice, and can the reference page be reached?

A documentation URL is never silently treated as an API endpoint. Legacy 5-column rows remain documentation-only and are included in the documentation monitor, but not in API endpoint probes.

## Scripts

| Script | Responsibility |
|---|---|
| `check_links.py` | Stage 1 HTTP check of unique, explicit API Endpoint URLs from canonical 6-column rows |
| `verify_links_playwright.py` | Stage 2 browser recheck of broken, warning, error and unknown endpoint responses |
| `check_pr_links.py` | PR diff validation, duplicate detection and endpoint verification; bot cleanup PRs also revalidate removed endpoint URLs |
| `link_health.py` | Shared conservative HTTP, WAF and parked-domain classification |
| `safe_urls.py` | Rejects non-public destinations and validates every HTTP redirect before a checker follows it |
| `check_shutdown_signals.py` | Scans documentation URLs from both legacy 5-column and canonical 6-column rows for explicit provider shutdown notices |
| `shutdown_detection.py` | Extracts visible page text and detects conservative provider-lifecycle phrases |
| `export_health_outputs.py` | Validates final Stage 2 JSON and writes collision-safe GitHub Actions outputs |
| `remove_dead_links.py` | Dry-run-by-default cleanup of explicitly confirmed dead API Endpoint rows |
| `parse_readme.py` | Generates `site/src/data/apis.json` and updates catalog counts in `README.md` and `site/index.html` |
| `gen_readme_table.py` | Regenerates the category index table in `README.md` |

## Endpoint result categories

| State | Meaning | Automated deletion? |
|---|---|---|
| `working` | HTTP 2xx response | No |
| `protected` | 401/403/418/429 or detected WAF/bot challenge; availability is not confirmed | No |
| `warning` | Timeout, TLS/connection issue or temporary 503 | No |
| `error` | HTTP 5xx service/server failure | No |
| `unknown` | Unclassified response or client error such as 400/405/406 | No |
| `broken` | HTTP 404/410, parked/suspended domain, or confirmed DNS NXDOMAIN | Candidate only; the cleanup PR must revalidate it |

The checker does not solve or bypass Cloudflare/Turnstile challenges. A challenge page—even one returning HTTP 200—is protected/inconclusive, not a healthy API response. Redirects to localhost, private, reserved or link-local addresses are blocked.

## Provider shutdown signals

A documentation page may continue returning HTTP 200 after its provider has shut down. The documentation monitor therefore inspects visible page content for explicit lifecycle language such as “no longer accepting new requests” or “API has been discontinued”.

A shutdown signal:
- creates or updates a separate maintainer-review Issue;
- appears separately in the Live Health Discussion;
- does **not** become a broken endpoint result;
- does **not** authorize automatic catalog deletion.

A maintainer confirms the provider statement and then makes a focused catalog change. Documentation 404/403/429, network failures and WAF pages are inconclusive—not shutdown evidence.

## Incident and remediation lifecycle

1. The scheduled/push scan checks explicit API Endpoint cells and produces final Stage 2 JSON.
2. Only confirmed broken endpoint candidates create or update an incident Issue.
3. The remediation job removes candidate rows on a dedicated bot branch and opens or updates one cleanup PR referencing the Issue.
4. The cleanup PR rechecks every removed API Endpoint URL. If an endpoint recovers, becomes protected, returns a transient error, or cannot be verified, the removal is blocked.
5. Central required checks must pass before the existing Auto-merge policy may merge the cleanup PR.
6. The PR's `Closes #N` reference closes the incident after a successful merge. The post-merge scan refreshes the Discussion.
7. If a later successful scan finds no endpoints still confirmed dead, pending cleanup Auto-merge is disabled and its `automerge` label is removed. If other results remain inconclusive, the PR and Issue stay open for human review; only a fully conclusive clean scan closes the stale incident.

The dashboard is updated only after both endpoint and documentation scans succeed. A failed or incomplete scan must never publish a green/zero report.

## Local usage

Run from the repository root:

```bash
python scripts/check_links.py
python scripts/verify_links_playwright.py
python scripts/check_shutdown_signals.py --output scripts/shutdown_signals.json
python -m unittest discover -s scripts/tests -v
python -m py_compile scripts/*.py
```

`check_links.py` must run before `verify_links_playwright.py`; Stage 2 consumes `scripts/results.json` written by Stage 1. `remove_dead_links.py` is dry-run by default and requires an explicit `--apply` flag. Never use documentation URLs as removal candidates.
