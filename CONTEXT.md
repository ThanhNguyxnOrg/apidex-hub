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
3. **No Duplicate URLs**: An API documentation URL must belong to exactly one primary category (the most specific category). Duplicates across categories are strictly prohibited.
4. **Link Anchor Standard**: Each category file must start with `## <a id="category-slug"></a>EMOJI Category Name`.

## 3. Automation Pipelines

- **`.github/workflows/link-checker.yml`**: Daily link checker at 00:00 UTC and on PRs. Checks all links, posts results to Discussions (#6 Live Dashboard), creates Incident Issues on dead links, and auto-remediates them.
- **`.github/workflows/deploy-website.yml`**: Builds and deploys the Vite/React catalog website to GitHub Pages upon changes to `main`.
- **`scripts/parse_readme.py`**: The authoritative single source of truth parser syncing `apis/*.md` into `site/src/data/apis.json`, `README.md`, and `site/index.html`.
