# ADR 0003: Fuse.js for Fuzzy Search and Query Scoring

## Status
Accepted

## Context
APIDex Hub indexes 12,500+ public APIs. The legacy search implementation used naive case-insensitive `.includes()` substring matching with no typo tolerance, no weighting between name and description, and no visual match highlighting.

## Decision
Integrate `fuse.js` (~8KB gzipped) configured with:
- Multi-field weighting (`name`: 3, `description`: 1, `category`: 0.5)
- Fuzzy threshold (`0.35`)
- Match index retention for query highlight wrapping (`<mark>`)

## Consequences
- Fast client-side fuzzy searching on dataset.
- Typo-tolerant discovery with visually highlighted query matches.
- Minimal impact on final JavaScript bundle size (+8KB).
