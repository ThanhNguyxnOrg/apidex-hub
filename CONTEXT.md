# 📖 APIDex Hub — Ubiquitous Domain Context & Architecture

> **Purpose:** Living glossary, domain concepts, and architectural invariants for APIDex Hub.  
> **Skill:** `grill-with-docs` · `anti-ui-slop` · `ponytail`

---

## 🏛️ Core Domain Concepts

| Term | Ubiquitous Definition | Source of Truth |
|---|---|---|
| **API Entry** | A single public API record consisting of `name`, `description`, `auth`, `https`, `link`, and assigned `category`. | Markdown tables inside `apis/*.md` |
| **Category** | A thematic cluster of APIs (e.g. `weather`, `machine-learning`). Identified by `slug` (derived from markdown file name/header anchor). | Directory `apis/*.md` (78 categories) |
| **Auth Type** | Authentication requirement: `none` (No key needed), `apiKey` (API Key required), or `oauth` (OAuth 2.0 flow). | Parsed from markdown column 3 |
| **Health Status** | Link availability verified by link-checker: `verified` (200 OK), `down` (4xx/5xx/timeout), `unchecked`. | Link checker workflow & report |
| **Live Health Dashboard** | A single persistent GitHub Issue labeled `daily-report,automated` that is never closed, updated dynamically every midnight. | `.github/workflows/link-checker.yml` |

---

## ⚙️ Invariant Pipelines (DO NOT BREAK)

### 1. Data Ingestion Pipeline (Markdown → JSON)
```
apis/*.md  ──(git push)──>  .github/workflows/deploy-website.yml
                                     │
                                     ▼
                      python scripts/parse_readme.py
                                     │
                                     ▼
                         site/src/data/apis.json
                                     │
                                     ▼
                            Vite Build (pnpm)
```
- **Rule:** Frontend code MUST consume `site/src/data/apis.json` dynamically via `site/src/app/components/data.ts`.
- **Category Resilience:** Any new `.md` added to `apis/` will automatically appear in categories without manual code edits. Category icon mapping must have a fallback icon so unknown slugs never crash the UI.

### 2. GitHub Pages Deployment Pipeline
```
site/ (Vite)  ──pnpm build──>  docs/ (repo root)  ──peaceiris/actions-gh-pages──>  gh-pages branch
```
- **Rule:** Vite `base` is configured to `/apidex-hub/`.
- **Routing Invariant:** GitHub Pages does not support server-side routing fallback without 404 hacks. Therefore, client-side routing MUST use `HashRouter` (`/#/category/:slug`, `/#/favorites`, `/#/`) to guarantee direct URLs and page refreshes work reliably.
- **Lockfile Invariant:** CI executes `pnpm install --frozen-lockfile`. Any dependency modification in `site/package.json` must update `site/pnpm-lock.yaml`.

---

## 📑 Architecture Decision Log Reference

Architectural decisions are tracked in `adr/`:
- `adr/0001-hash-routing-for-github-pages.md`
- `adr/0002-dependency-purge-and-lightweight-stack.md`
- `adr/0003-fuse-js-for-fuzzy-search.md`
