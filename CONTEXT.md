# APIDex Hub — System Context & Domain Model

## 1. Domain Glossary

| Term | Definition |
|---|---|
| **API Entry** | A single public API or web scraper listed in the catalog, defined by: Name, Description, Auth requirement, HTTPS support, an optional explicitly verified API endpoint URL, and an official documentation URL. |
| **Category** | A markdown document under `apis/<category-slug>.md` grouping related APIs. Must contain an anchor tag header (`## <a id="slug"></a>EMOJI Title`) and the canonical 6-column table; legacy 5-column tables remain readable as documentation-only entries. |
| **Catalog** | The complete collection of all categories, aggregated into `site/src/data/apis.json` and summarized in `README.md`. |
| **Auth Scheme** | The authentication mechanism for an API: `No` (public/free, no key needed), `🔑 ApiKey` (requires an API key/token), or `🔐 OAuth` (requires OAuth 2.0 flow). |
| **API Endpoint Health** | The operational state of an explicitly recorded API Endpoint URL, checked by conservative HTTP classification and a browser recheck for non-success responses. Documentation URLs are checked separately and are never endpoint-health or endpoint-deletion evidence. |
| **Dead API Endpoint Candidate (Broken)** | An explicitly recorded API Endpoint URL classified as 404/410, parked/suspended, or DNS NXDOMAIN after the checker’s verification stages. Automated removal is not authorized until the cleanup PR independently revalidates the removed endpoint. A documentation URL returning 404/410 is never proof that the API is dead. |
| **Auto-Remediation** | The automated GitHub Actions process that removes only explicitly recorded API Endpoint rows that remain confirmed dead when the cleanup PR revalidates them, then regenerates website data and closes the linked Incident Issue after merge. |
| **Safety Brake** | A configurable threshold (`--max-delete`) in `remove_dead_links.py` preventing catastrophic deletion of APIs in case of widespread network or proxy outages. |
| **Provider Shutdown Signal** | Explicit current-provider/current-API lifecycle language found on a documentation page. It creates a lifecycle Issue; a focused bot PR is eligible only when the fetch succeeds and the signal maps to exactly one API row. Ambiguous/shared docs stay open for review. |
| **Documentation Inconclusive** | A documentation URL could not be conclusively fetched (for example 403/429, 5xx, TLS, timeout, DNS failure or WAF challenge). It is not proof that the provider shut down. |


## 2. Business & Data Integrity Rules

1. **Canonical 6-Column Markdown Format**:
   ```markdown
   | API Name | Description | Auth | HTTPS | API Endpoint | Documentation |
   | :--- | :--- | :---: | :---: | :--- | :--- |
   | **Example API** | Clear summary of API capabilities. | 🔑 ApiKey | ✅ | [Endpoint](https://api.example.com/v1/resource) | [Docs](https://example.com/docs) |
   ```
   The legacy 5-column format (`API Name | Description | Auth | HTTPS | Link`) remains supported as documentation-only: its `Link` is mapped to `documentation_url`, its endpoint is empty, and it is excluded from API endpoint monitoring and automated dead-endpoint deletion.
2. **Endpoint / documentation separation**: `API Endpoint` must be a documented API service or operation URL, never a company homepage, developer portal, landing page, or docs page. Do not infer endpoints from a documentation URL or hostname. Leave the endpoint cell blank until an official endpoint is verified.
2. **Escaped Pipe Rule**: Cells must NOT contain unescaped or raw `|` characters. Em-dashes (`—`) or forward slashes (`/`) must be used for titles containing subtitles to prevent breaking markdown column splitting.
3. **No Duplicate API Services**: Deduplicate by the underlying API/service identity, not by exact URL alone. Domain aliases, subdomains, redirects, alternate docs URLs, and different endpoints for the same API may be the same service; prefer one canonical official link and one best-fit category. Different providers offering similar functionality MUST remain separate entries. Distinct APIs/products from the same provider may also coexist when they provide meaningfully different capabilities.
4. **Link Anchor Standard**: Each category file must start with `## <a id="category-slug"></a>EMOJI Category Name`.

## 3. Automation Pipelines

- **`.github/workflows/link-checker.yml`**: Daily endpoint-health scan at 00:00 UTC and on PRs, plus a separate documentation lifecycle scan. It creates endpoint incidents and lifecycle issues, opens bot PRs for unambiguous API retirements, and applies the existing central Auto-merge label so required checks run before merge and issue closure.
- **`.github/workflows/script-tests.yml`**: Runs dependency-light Python regression tests for catalog automation scripts on pushes and pull requests.
- **PR link validation**: `scripts/check_pr_links.py` uses explicit pull-request base/head commits and repository-root Git commands. Missing refs or failed diffs are errors, not empty-success results.

- **`.github/workflows/deploy-website.yml`**: Builds and deploys the Vite/React catalog website to GitHub Pages upon changes to `main`.
- **`scripts/parse_readme.py`**: The authoritative single source of truth parser syncing `apis/*.md` into `site/src/data/apis.json`, `README.md`, and `site/index.html`.
- **Endpoint status rules**: 401/403/418/429 and WAF challenges are protected/inconclusive; 400/405/406 are unknown; 5xx, timeouts and TLS failures are not deletion evidence. Parked-domain/HTTP 200 pages are not healthy endpoints.
- **Provider shutdown rules**: Documentation pages are scanned for explicit shutdown language even when they return HTTP 200. These signals never count as endpoint death. A retirement becomes a PR candidate only after a successful fetch, explicit current-API classification, and a unique one-API-to-one-row mapping; the change is proposed on a bot branch and merged only through the central required-check/Auto-merge path.
- **SSRF protection**: `scripts/safe_urls.py` blocks localhost, private/reserved/link-local destinations and unsafe redirect hops in the HTTP and browser checkers.


## 4. Catalog Curation Priorities

1. **Free-first discovery**: Prefer genuinely free and open-data APIs, then useful freemium APIs with a meaningful usable free tier. When a popular paid API is found, actively look for reputable free/open-source alternatives before adding more paid listings. Never replace a free API with a paid provider merely because they cover the same topic.
2. **Similar topic is not a duplicate**: Keep different providers for the same subject (for example, multiple dog-data APIs, weather APIs, geocoding providers, or LLM providers). The catalog's value is choice and comparison across providers.
3. **Deduplicate the service, not the hostname**: Compare vendor/service identity, canonical docs, redirects, product branding, endpoint purpose, and aliases. `facebook.com` and `fb.com` may represent one service; distinct vendors like Facebook/Meta and another social provider are not duplicates merely because their features overlap. A provider can expose multiple distinct APIs; keep each when its capabilities are distinct.
4. **API endpoint health is separate from documentation health**: Only the explicit `API Endpoint` column is eligible for API probes and automated deletion. A missing, moved, blocked, or 404/410 Documentation URL must never delete an API entry. Treat 400/401/403/405/418/429, WAF responses, timeouts, SSL errors, and 5xx responses as inconclusive/protected. A 404/410 on a service root may be route-specific; prefer a documented operation-level endpoint and require corroboration before removal.
5. **Keep free alternatives visible**: When a free API is confirmed dead and must be removed, look for a currently maintained free API with comparable utility. Add the replacement as a separate provider while preserving other working free alternatives. Clearly describe API-key requirements and free-tier restrictions in the listing.
6. **Batch safety**: For large imports, check existing catalog names, normalized URLs, domain aliases, and underlying service names. Count candidates only after deduplication; do not inflate the KPI by adding aliases or multiple copies of the same service.
