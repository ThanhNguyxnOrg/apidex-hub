# ADR 0001: Hash Routing for GitHub Pages Compatibility

## Status
Accepted

## Context
APIDex Hub is hosted on GitHub Pages under the subpath `/apidex-hub/`. Currently, the app uses a manual `useState<View>` state machine in `App.tsx`, which prevents URL bookmarking, deep linking to categories, and breaks the browser back/forward buttons.
GitHub Pages is a static file host that does not support server-side routing fallbacks (e.g. rewrites to `/index.html`) without custom 404 tricks.

## Decision
We use `react-router` v7 with `HashRouter` (`/#/`, `/#/category/:slug`, `/#/favorites`).

## Consequences
- **Pros:**
  - 100% compatible with GitHub Pages static hosting under `/apidex-hub/`.
  - Zero risk of HTTP 404 on page reload or when sharing deep links like `https://thanhnguyxnorg.github.io/apidex-hub/#/category/weather`.
  - Browser back/forward buttons and history navigation work out of the box.
  - Minimal changes to existing components.
- **Cons:**
  - URLs contain `#` symbol (standard for GitHub Pages SPAs).
