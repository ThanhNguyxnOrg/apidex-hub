"""Pure helpers for safe validation of APIDex API catalog pull requests."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

_API_LINK_RE = re.compile(r"\[Link\]\((https?://[^)]+)\)", re.IGNORECASE)


def find_repository_root(start: Path) -> Path:
    """Find the Git repository root from a file or nested working directory."""
    current = Path(start).resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists():
            return candidate
    raise RuntimeError(f"Could not locate a Git repository above {start}")


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown Git error"
        raise RuntimeError(f"Git command failed ({' '.join(args)}): {detail}")
    return result.stdout


def read_pr_diff(base_ref: str, head_ref: str, repo_root: Path) -> tuple[list[str], str]:
    """Read changed API files and their diff, independent of the caller's CWD."""
    if not base_ref or not head_ref:
        raise RuntimeError("Both base and head commit refs are required for PR validation")
    root = find_repository_root(Path(repo_root))
    for ref_name, ref in (("base", base_ref), ("head", head_ref)):
        resolved = _git(root, "rev-parse", "--verify", f"{ref}^{{commit}}").strip()
        if not re.fullmatch(r"[0-9a-fA-F]{40,64}", resolved):
            raise RuntimeError(f"The PR {ref_name} ref did not resolve to a commit: {ref}")

    paths_text = _git(root, "diff", "--name-only", "--diff-filter=ACMR", base_ref, head_ref, "--", "apis/")
    paths = sorted(path for path in paths_text.splitlines() if path.startswith("apis/"))
    diff = _git(root, "diff", "--no-ext-diff", "--unified=0", base_ref, head_ref, "--", "apis/")
    return paths, diff


def normalize_url(url: str) -> str:
    """Normalize URL host and trailing slash without discarding meaningful queries."""
    try:
        parts = urlsplit(url.strip())
        if parts.scheme.lower() not in {"http", "https"} or not parts.hostname:
            return url.strip()
        host = parts.hostname.lower()
        port = parts.port
        if port and not ((parts.scheme.lower() == "https" and port == 443) or (parts.scheme.lower() == "http" and port == 80)):
            host = f"{host}:{port}"
        if parts.username or parts.password:
            return url.strip()
        path = parts.path.rstrip("/")
        normalized_path = path or "/"
        if normalized_path != "/":
            normalized_path = normalized_path.rstrip("/")
        return urlunsplit((parts.scheme.lower(), host, normalized_path, parts.query, ""))
    except ValueError:
        return url.strip()


def _split_table_row(line: str) -> list[str] | None:
    stripped = line.strip()
    if not (stripped.startswith("|") and stripped.endswith("|")):
        return None
    return [cell.strip() for cell in stripped[1:-1].split("|")]


def _is_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells)


def _parse_data_row(line: str) -> tuple[str | None, str | None]:
    """Return (URL, error); both are None for non-data rows."""
    cells = _split_table_row(line)
    if cells is None:
        return None, None
    if cells and cells[0].strip("* ").lower() in {"api name", "name"}:
        return None, None
    if _is_separator_row(cells):
        return None, None
    if not cells or not cells[0] or cells[0].startswith("---"):
        return None, None
    if len(cells) != 5:
        return None, f"Expected 5 table columns, found {len(cells)}: {line.strip()}"
    match = _API_LINK_RE.search(cells[4])
    if not match:
        return None, f"Missing official [Link](https://...) in the fifth column: {line.strip()}"
    return match.group(1).strip(), None


def parse_api_diff(diff_text: str) -> tuple[list[str], list[str], list[str]]:
    """Parse added/removed API URLs and malformed added API rows from a unified diff."""
    added: list[str] = []
    removed: list[str] = []
    malformed: list[str] = []
    in_hunk = False
    for line in diff_text.splitlines():
        if line.startswith("@@"):
            in_hunk = True
            continue
        if not in_hunk or line.startswith(("+++", "---", "\\")) or not line:
            continue
        if line[0] not in "+-":
            continue
        url, error = _parse_data_row(line[1:])
        if line[0] == "+":
            if error:
                malformed.append(error)
            elif url:
                added.append(url)
        elif url:
            removed.append(url)
    return added, removed, malformed


def parse_api_document(content: str) -> list[str]:
    """Extract official docs links from the standard five-column catalog rows."""
    urls: list[str] = []
    for line in content.splitlines():
        url, _error = _parse_data_row(line)
        if url:
            urls.append(url)
    return urls


def find_duplicate_urls(
    added_urls: list[str], removed_urls: list[str], existing_urls: list[str]
) -> list[str]:
    """Detect URL duplicates, accounting for entries removed in the same PR."""
    removed = {normalize_url(url) for url in removed_urls}
    existing = {normalize_url(url) for url in existing_urls} - removed
    seen_added: set[str] = set()
    duplicates: list[str] = []
    reported: set[str] = set()
    for url in added_urls:
        normalized = normalize_url(url)
        if (normalized in existing or normalized in seen_added) and normalized not in reported:
            duplicates.append(url)
            reported.add(normalized)
        seen_added.add(normalized)
    return duplicates


def read_existing_api_urls(base_ref: str, repo_root: Path) -> list[str]:
    """Read API URLs on the PR base revision, never the working-tree contents."""
    root = find_repository_root(Path(repo_root))
    tracked = _git(root, "ls-tree", "-r", "--name-only", base_ref, "--", "apis/")
    urls: list[str] = []
    for path in tracked.splitlines():
        if not path.startswith("apis/") or not path.endswith(".md"):
            continue
        content = _git(root, "show", f"{base_ref}:{path}")
        urls.extend(parse_api_document(content))
    return urls


def classify_link_result(status: int | None, note: str = "") -> str:
    """Classify URL health conservatively: only clear 404/410 or NXDOMAIN are broken."""
    lowered = note.lower()
    if any(marker in lowered for marker in ("err_name_not_resolved", "dns_probe_finished_nxdomain", "nxdomain", "name resolution failed")):
        return "broken"
    if status is not None and 200 <= status < 400:
        return "working"
    if status in {404, 410}:
        return "broken"
    return "inconclusive"
