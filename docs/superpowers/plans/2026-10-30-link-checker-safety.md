# APIDex Hub Link Checker Safety Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prevent automatic API catalog deletions from URL-level failures and make PR link validation fail closed when API rows are not actually inspected.

**Architecture:** Add a small pure-Python validation module for parsing API table rows from Git diffs, normalizing official documentation URLs, and accounting for rows moved within a PR. Update the PR checker to use explicit commit refs and repository-root Git execution. Change daily incidents to human review only and make the removal utility dry-run by default.

**Tech Stack:** Python 3.11 standard library (`unittest`, `subprocess`, `pathlib`, `urllib.parse`), GitHub Actions, existing Requests/Playwright validation.

**Spec:** `docs/superpowers/specs/2026-10-30-link-checker-safety-design.md`

## Global Constraints

- Preserve the five-column Markdown catalog format.
- Keep `apis/` as the catalog source of truth.
- Never edit generated website files or run website build commands.
- Do not automatically remove catalog rows from daily link-check results.
- `remove_dead_links.py` must not mutate files unless `--apply` is explicitly supplied.
- Git commands in PR validation must run from the repository root, independent of the caller's working directory.
- PR diff refs must be validated; unresolved diffs are failures, not empty success.

## Review Focus

- Workflow invoked from `scripts/`: test that the real Git diff sees `apis/` additions from that working directory.
- PR changes move an API between category files: the removed row must be subtracted from base duplicates.
- New table row has a missing/malformed official link: validation must fail rather than silently skip.
- Git base/head commit is missing: checker must fail with a useful diagnostic.
- Removal utility invoked without `--apply`: source Markdown files must remain byte-for-byte unchanged.

---

### Task 1: Reliable PR diff parsing and regression tests

**Files:**
- Create: `scripts/pr_validation.py`
- Create: `scripts/tests/test_pr_validation.py`
- Modify: `scripts/check_pr_links.py`

**Interfaces:**
- `pr_validation.read_pr_diff(base_ref: str, head_ref: str, repo_root: Path) -> tuple[list[str], str]` returns changed API paths and the unified diff; raises `RuntimeError` when refs/diff cannot be read.
- `pr_validation.parse_api_diff(diff_text: str) -> tuple[list[str], list[str], list[str]]` returns added official URLs, removed official URLs, and malformed added-row diagnostics.
- `pr_validation.parse_api_document(text: str) -> list[str]` extracts official URLs from existing five-column API rows.
- `pr_validation.find_duplicate_urls(added_urls, removed_urls, existing_urls) -> list[str]` catches duplicates while allowing rows removed in the same PR to be re-added elsewhere.

- [ ] **Step 1: Write regression tests** for repository-root diff execution, official-link extraction from the fifth column, malformed added rows, moved-row duplicate accounting, duplicate additions within a PR, and URL normalization.
- [ ] **Step 2: Run tests and observe the expected failures** before implementing the module.
- [ ] **Step 3: Implement the pure validation helpers** in `scripts/pr_validation.py`.
- [ ] **Step 4: Update `check_pr_links.py`** to use `APIDEX_DIFF_BASE` and `APIDEX_DIFF_HEAD`, validate refs, run Git with `cwd=REPO_ROOT`, reject malformed rows, and report deletion-only changes accurately.
- [ ] **Step 5: Run the regression tests and Python compilation**; verify the fixture test fails on the original working-directory behavior and passes with the root-based implementation.
- [ ] **Step 6: Commit** as `fix(ci): validate PR API diffs from repository root`.

### Task 2: Remove destructive daily remediation and gate manual cleanup

**Files:**
- Modify: `.github/workflows/link-checker.yml`
- Modify: `scripts/remove_dead_links.py`
- Create/extend: `scripts/tests/test_remove_dead_links.py`

**Interfaces:**
- `remove_dead_links_from_file(..., dry_run=True)` must default to no mutation.
- CLI flag `--apply` explicitly enables writing.
- The `--max-delete` safety brake is evaluated against the total candidate rows before any file is modified.

- [ ] **Step 1: Write tests** proving the default remover call does not mutate, explicit apply does, and the safety brake prevents all writes when candidate rows exceed the configured limit.
- [ ] **Step 2: Run tests and observe expected failures** against the current unsafe defaults.
- [ ] **Step 3: Implement dry-run-by-default and explicit `--apply`** with a preflight candidate count.
- [ ] **Step 4: Remove the automatic remediation and auto-close steps** from the daily workflow. Keep incident creation and reporting, and update issue/dashboard language to say URL failures require maintainer verification and do not prove service retirement.
- [ ] **Step 5: Run the full script test suite** and inspect the workflow diff for remaining destructive steps.
- [ ] **Step 6: Commit** as `fix(automation): require maintainer approval before API removal`.

### Task 3: CI wiring and repository guidance

**Files:**
- Create: `.github/workflows/script-tests.yml`
- Modify: `.github/workflows/link-checker.yml`
- Modify: `.github/ai-instructions.md`
- Modify: `CONTEXT.md`

- [ ] **Step 1: Add a dependency-light Python unittest workflow** for pushes and pull requests touching `scripts/**` or the test workflow.
- [ ] **Step 2: Pass the PR base SHA and checked-out merge SHA** to `check_pr_links.py`.
- [ ] **Step 3: Update context documentation** to describe incidents as review candidates and removal as an explicit manual operation.
- [ ] **Step 4: Run tests, compile all changed Python scripts, and check YAML syntax** (using available validation tools).
- [ ] **Step 5: Commit** as `test(ci): add regression coverage for catalog automation`.

## Verification Commands

- `python -m unittest discover -s scripts/tests -v`
- `python -m py_compile scripts/check_pr_links.py scripts/pr_validation.py scripts/remove_dead_links.py`
- GitHub Actions: Script Tests + Link Checker PR validation

