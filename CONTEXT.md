# APIDex Hub — System Context & Domain Model

## 1. Domain Glossary

| Term | Definition |
|---|---|
| **API Entry** | A single public API or web scraper listed in the catalog, defined by: Name, Description, Auth requirement, HTTPS support, and official documentation URL. |
| **Category** | A markdown document under `apis/<category-slug>.md` grouping related APIs. Must contain an anchor tag header (`## <a id="slug"></a>EMOJI Title`) and a standard 5-column markdown table. |
| **Catalog** | The complete collection of all categories, aggregated into `site/src/data/apis.json` and summarized in `README.md`. |
| **Auth Scheme** | The authentication mechanism for an API: `No` (public/free, no key needed), `🔑 ApiKey` (requires an API key/token), or `🔐 OAuth` (requires OAuth 2.0 flow). |
| **Link Health** | The operational state of an API endpoint, verified in a two-stage automated pipeline: Stage 1 (Fast HTTP/CLI check) and Stage 2 (Headless Playwright browser verification to bypass Cloudflare/WAF bot challenges). |
| **Dead API (Broken)** | An endpoint confirmed dead via HTTP 404, HTTP 410, or NXDOMAIN (DNS failure). |
| **Auto-Remediation** | The automated GitHub Actions process (`scripts/remove_dead_links.py`) that safely excises confirmed dead links from markdown tables, recalculates catalog counts, updates website JSON, commits, pushes, and closes Incident Issues. |
| **Safety Brake** | A configurable threshold (`--max-delete`) in `remove_dead_links.py` preventing catastrophic deletion of APIs in case of widespread network or proxy outages. |

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

- **`.github/workflows/link-checker.yml`**: Daily link checker at 00:00 UTC and on PRs. Checks all links, posts results to Discussions (#6 Live Dashboard), creates Incident Issues on dead links, and auto-remediates them.
- **`.github/workflows/deploy-website.yml`**: Builds and deploys the Vite/React catalog website to GitHub Pages upon changes to `main`.
- **`scripts/parse_readme.py`**: The authoritative single source of truth parser syncing `apis/*.md` into `site/src/data/apis.json`, `README.md`, and `site/index.html`.


## 4. Catalog Curation Priorities

1. **Free-first discovery**: Prefer genuinely free and open-data APIs, then useful freemium APIs with a meaningful usable free tier. When a popular paid API is found, actively look for reputable free/open-source alternatives before adding more paid listings. Never replace a free API with a paid provider merely because they cover the same topic.
2. **Similar topic is not a duplicate**: Keep different providers for the same subject (for example, multiple dog-data APIs, weather APIs, geocoding providers, or LLM providers). The catalog's value is choice and comparison across providers.
3. **Deduplicate the service, not the hostname**: Compare vendor/service identity, canonical docs, redirects, product branding, endpoint purpose, and aliases. `facebook.com` and `fb.com` may represent one service; distinct vendors like Facebook/Meta and another social provider are not duplicates merely because their features overlap. A provider can expose multiple distinct APIs; keep each when its capabilities are distinct.
4. **Dead-link handling is conservative**: A single failed request is not proof that an API is dead. Treat 403/401/429, bot protection, timeouts, SSL errors, and 5xx responses as inconclusive unless corroborated. If an official docs URL returns 404, search for moved official docs, a new endpoint, or a maintained free replacement before deleting the listing. Remove only when the service/link is confirmed unavailable and no valid canonical URL can be found.
5. **Keep free alternatives visible**: When a free API is confirmed dead and must be removed, look for a currently maintained free API with comparable utility. Add the replacement as a separate provider while preserving other working free alternatives. Clearly describe API-key requirements and free-tier restrictions in the listing.
6. **Batch safety**: For large imports, check existing catalog names, normalized URLs, domain aliases, and underlying service names. Count candidates only after deduplication; do not inflate the KPI by adding aliases or multiple copies of the same service.

## 5. Non-Negotiable Keep-Existing Policy (Read Before Any Catalog Edit)

**Default action: ADD; do not replace or remove a working API.**
- A healthy API remains in the catalog even if a free, cheaper, faster, newer, or more popular alternative exists.
- Do not replace a paid API with a free API, a free API with a paid API, or one provider with another just because they share a topic or use case. Add the alternative as another entry so users can choose.
- Being paid is not a failure state. Pricing, popularity, overlap, or a preference for free tools is never by itself a reason to delete or rename an existing working listing.
- Preserve existing API names, official URLs, and entries unless the service is confirmed unavailable, the listing is a true duplicate of the same service/API, the official URL has moved, or the user explicitly requests a change. Prefer updating a stale URL/description in place for the same service over deleting it.

### What “duplicate” actually means
- **True duplicate / alias:** Two rows identify the same underlying service and same API/capability, with only a hostname alias, redirect, mirror, alternate docs URL, or equivalent endpoint difference. Example: `facebook.com` and `fb.com` for the same Facebook service; keep one canonical listing for that same service/API.
- **NOT a duplicate:** Different providers offering similar functionality. Keep all healthy options, even if they are in the same category and solve the same problem (for example, multiple LLM inference providers, weather providers, geocoders, email services, search APIs, or stock-data providers).
- **NOT automatically a duplicate:** Different APIs/products from the same provider. Keep both when the API, product, endpoint purpose, data, or deployment model is meaningfully distinct. Sharing a vendor or hostname alone is insufficient to merge rows.
- Before merging anything, compare provider identity, service/product name, API purpose and capabilities, canonical documentation, redirects, and the actual endpoint. Never deduplicate by category/topic, hostname alone, or superficial name similarity.

### Required decision process
1. Audit the existing row first. Verify the actual service and current official docs; do not infer that it is dead from a single link-check result.
2. If it works, **keep it**. If a comparable free or open-source option exists, add that option as a separate row.
3. If it is paid but still works, keep it and describe verified pricing/free-tier conditions accurately; add free alternatives separately.
4. If a documentation URL moved, update the link to the canonical official docs for the same API. Do not treat a moved docs page as a reason to replace the API with a different product.
5. Remove a row only for a confirmed duplicate of the same service/API or a confirmed unavailable service after checking for a moved/canonical URL. A 404 on docs alone is insufficient. 401/403/429, bot protection, timeouts, SSL errors, and 5xx are inconclusive unless independently corroborated.
6. If a genuinely dead API must be removed, preserve every other working entry and, where useful, add a free replacement as a new row. Do not remove other providers offering similar functionality.

### Required pre-commit diff audit
- Compare the change against the base revision. The number of API rows must not go down as a side effect of an “add alternatives” task.
- For any existing row deleted, renamed, or having its URL changed, document the exact reason and evidence. If it was working and the user did not request that change, restore it before committing.
- Check for hostname aliases and exact same-service duplicates without flagging legitimate competitors as duplicates.
- Never claim an API was verified working/dead unless the available evidence supports that claim. Distinguish a permanent free tier, a limited free tier, self-hosted open source, and one-time trial credits.
- Use provider-official pricing/docs pages to verify free-tier limits. Do not describe trial credits or a paid-only product as permanently free.
