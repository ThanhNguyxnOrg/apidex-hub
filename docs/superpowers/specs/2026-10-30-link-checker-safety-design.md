# APIDex Hub Link Checker Safety Design

**Date:** 2026-10-30

## Intent

Protect the curated API catalog from destructive false positives while making pull-request link validation trustworthy. The daily checker should surface URL failures for human review; PR validation must inspect the actual `apis/` diff and must never report success after silently checking zero rows when API rows changed.

## Findings

1. `.github/workflows/link-checker.yml` runs the PR checker from `scripts/` (`cd scripts`), while `scripts/check_pr_links.py` runs Git commands with the relative pathspec `apis/`. Git therefore looks under `scripts/apis/`, gets an empty diff with exit code 0, and prints a false no-new-links success. Historical PR #26 and #27 logs show exactly this outcome despite API table additions.
2. The daily workflow automatically runs `scripts/remove_dead_links.py` after URL-level 404/410/NXDOMAIN results, then commits the deletions and closes the incident. A failed documentation URL is not sufficient evidence that the underlying API/service is retired; the repository's own contributor rules already say so.
3. `remove_dead_links.py` currently writes changes by default. A manual invocation can therefore mutate the catalog without an explicit apply switch.

## Approaches

- **A. Keep automatic deletion, add more retries/signals.** Better than a single attempt, but still risks deleting a live service whose documentation moved or is temporarily inaccessible. The checker cannot reliably establish service retirement from a docs URL.
- **B. Make link failures review-only; require explicit human application for catalog deletion.** Keep daily detection, reports, artifacts, and incident issues. Never delete catalog rows in the scheduled workflow. Make the remover dry-run by default and require `--apply` for mutations. This is the recommended approach because catalog integrity is more valuable than automatic cleanup.
- **C. Add a quarantine state to each API row.** This is not compatible with the existing five-column catalog schema without a broader data-model migration.

## Chosen Design

Use approach B. Keep the current two-stage checker and incident reporting. Replace the destructive remediation/auto-close behavior with a maintainer-review incident explaining that a URL failure is not proof of API retirement. Make `remove_dead_links.py` a dry-run tool unless `--apply` is passed, and evaluate the deletion safety threshold against candidate rows before writing.

For PR validation, derive the diff from explicit base/head commit SHAs supplied by the GitHub PR event. Run Git commands from the repository root derived from `__file__`, not the current working directory. Parse only the official documentation link in the fifth table column. Treat an added data row without a valid official URL as a validation error. Account for rows removed in the same PR so moving an API between category files is not falsely rejected as a duplicate. If the diff cannot be resolved, fail closed. A deletion-only change may pass with an explicit “no new links to check” report; it must not claim that links were verified.

## Goals

- No automated deletion of catalog entries from URL health results.
- No destructive behavior from `remove_dead_links.py` without explicit `--apply`.
- PR checks inspect the correct `apis/` paths even when invoked from `scripts/`.
- Changed API rows cannot silently bypass validation due to an empty or unresolved Git diff.
- Moving an existing API between categories does not trigger a false duplicate.
- Add dependency-light regression tests and run them in CI.

## Non-goals

- Do not modify API catalog entries or generated website data.
- Do not rewrite contributor commit history for issues #38/#39.
- Do not implement provider identity matching across different documentation URLs in this change.
- Do not claim a 404 proves an API is dead; service-level research remains a maintainer decision.

## Constraints

- Preserve the five-column Markdown catalog format.
- Keep `apis/` as the catalog source of truth.
- Do not locally regenerate `site/src/data/apis.json`, `README.md`, or `site/index.html`.
- Do not run website build commands.
