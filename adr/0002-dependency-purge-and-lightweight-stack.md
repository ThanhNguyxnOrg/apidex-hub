# ADR 0002: Dependency Purge and Lightweight Frontend Stack

## Status
Accepted

## Context
APIDex Hub `site/package.json` had 40+ packages installed, including `@mui/material`, 17 `@radix-ui/*` packages, `recharts`, `react-dnd`, `motion`, `sonner`, `vaul`, and `cmdk`. None of these packages were imported in the codebase. This caused bundle bloat, slow installation, and cluttered dependency trees.

## Decision
Remove all 35+ unused dependencies. Retain only:
- Core: `react`, `react-dom`, `react-router`
- Icons: `lucide-react`
- Utilities: `clsx`, `tailwind-merge`, `class-variance-authority`, `tw-animate-css`
- Search: `fuse.js` (~8KB)

## Consequences
- Cuts node_modules size by over 60%.
- Eliminates unused JavaScript evaluation overhead.
- Synchronizes with `pnpm-lock.yaml` so CI `pnpm install --frozen-lockfile` runs faster and reliably.
