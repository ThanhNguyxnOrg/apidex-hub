# APIDex Hub — System Context & Domain Model

## 1. Domain Glossary

| Term | Definition |
|---|---|
| **API Entry** | A single public API or web scraper listed in the catalog, defined by: Name, Description, Auth requirement, HTTPS support, and official documentation URL. |
| **Category** | A markdown document under `apis/<category-slug>.md` grouping related APIs. Must contain an anchor tag header (`## <a id="slug"></a>EMOJI Title`) and a standard 5-column markdown table. |
| **Catalog** | The complete collection of all categories, aggregated into `site/src/data/apis.json` and summarized in `README.md`. |
| **Auth Scheme** | The authentication mechanism for an API: `No` (public/free, no key needed), `🔑 ApiKey` (requires an API key/token), or `🔐 OAuth` (requires OAuth 2.0 flow). |
| **Link Health** | The operational state of a documentation URL, checked with HTTP/CLI requests and a headless Playwright browser. URL reachability is not proof that the underlying API is live or retired. |
| **Broken URL Candidate** | A documentation URL that returned HTTP 404/410 or DNS NXDOMAIN and requires maintainer investigation; this does not automatically mean the API service is retired. |
| **Manual Removal** | The `scripts/remove_dead_links.py` helper, which defaults to dry-run and only changes API Markdown files when a maintainer explicitly passes `--apply`. Derived website files are regenerated only as part of that intentional manual operation. |
| **Safety Brake** | A configurable `--max-delete` threshold in `remove_dead_links.py` that counts candidate catalog rows before any file is modified. |


## 2. Business & Data Integrity Rules

1. **Strict 5-Column Markdown Format**:
   ```markdown
   | API Name | Description | Auth | HTTPS | Link |
   | :--- | :--- | :---: | :---: | :---: |
   | **Example API** | Clear summary of API capabilities. | 🔑 ApiKey | ✅ | [Link](https://example.com/docs) |
   ```
2. **Escaped Pipe Rule**: Cells must NOT contain unescaped or raw `|` characters. Em-dashes (`—`) or forward slashes (`/`) must be used for titles containing subtitles to prevent breaking markdown column splitting.
3. **No Duplicate API Services**: Deduplicate by the underlying API/service identity, not by exact URL alone. Domain aliases, subdomains, redirects, alternate docs URLs, and different endpoints for the same API may be the same service; prefer one canonical official link and one best-fit category. Different providers offering similar functionality MUST remain separate entries. Distinct APIs/products from the same provider may also coexist when they provide meaningfully different capabilities.
4. **Link Anchor Standard**: Each category file must start with `## <a id="category-slug"></a>EMOJI Category Name`.

## 3. Automation Pipelines

- **`.github/workflows/link-checker.yml`**: Daily link checker at 00:00 UTC and on PRs. Checks links, posts results to Discussions (#6 Live Dashboard), and creates maintainer-review Incident Issues. It never edits or deletes API catalog rows.
- **`.github/workflows/script-tests.yml`**: Runs dependency-light Python regression tests for catalog automation scripts on pushes and pull requests.
- **PR link validation**: `scripts/check_pr_links.py` uses explicit pull-request base/head commits and repository-root Git commands. Missing refs or failed diffs are errors, not empty-success results.

- **`.github/workflows/deploy-website.yml`**: Builds and deploys the Vite/React catalog website to GitHub Pages upon changes to `main`.
- **`scripts/parse_readme.py`**: The authoritative single source of truth parser syncing `apis/*.md` into `site/src/data/apis.json`, `README.md`, and `site/index.html`.


## 4. Catalog Curation Priorities

1. **Free-first discovery**: Prefer genuinely free and open-data APIs, then useful freemium APIs with a meaningful usable free tier. When a popular paid API is found, actively look for reputable free/open-source alternatives before adding more paid listings. Never replace a free API with a paid provider merely because they cover the same topic.
2. **Similar topic is not a duplicate**: Keep different providers for the same subject (for example, multiple dog-data APIs, weather APIs, geocoding providers, or LLM providers). The catalog's value is choice and comparison across providers.
3. **Deduplicate the service, not the hostname**: Compare vendor/service identity, canonical docs, redirects, product branding, endpoint purpose, and aliases. `facebook.com` and `fb.com` may represent one service; distinct vendors like Facebook/Meta and another social provider are not duplicates merely because their features overlap. A provider can expose multiple distinct APIs; keep each when its capabilities are distinct.
4. **Dead-link handling is conservative**: A single failed request is not proof that an API is dead. Treat 403/401/429, bot protection, timeouts, SSL errors, and 5xx responses as inconclusive unless corroborated. If an official docs URL returns 404, search for moved official docs, a new endpoint, or a maintained free replacement before deleting the listing. Remove only when the service/link is confirmed unavailable and no valid canonical URL can be found.
5. **Keep free alternatives visible**: When a free API is confirmed dead and must be removed, look for a currently maintained free API with comparable utility. Add the replacement as a separate provider while preserving other working free alternatives. Clearly describe API-key requirements and free-tier restrictions in the listing.
6. **Batch safety**: For large imports, check existing catalog names, normalized URLs, domain aliases, and underlying service names. Count candidates only after deduplication; do not inflate the KPI by adding aliases or multiple copies of the same service.
