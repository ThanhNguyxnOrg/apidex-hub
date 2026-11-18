#!/usr/bin/env python3
"""Create a narrowly scoped plan for explicitly retired API catalog rows.

This automation is intentionally stricter than the documentation signal detector:
only a successful documentation fetch, an explicit current-provider/current-API
signal, and an unambiguous one-API-to-one-documentation-row mapping are eligible.
Ambiguous/shared documentation URLs remain open for maintainer review.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


_LINK_RE = re.compile(r"\[[^\]]+\]\((https?://[^)]+)\)", re.IGNORECASE)
_ALLOWED_SIGNAL_TYPES = frozenset({
    "request_intake_closed",
    "service_shutdown",
    "provider_shutdown",
    "service_operations_ended",
})


def _row_cells(line: str) -> list[str] | None:
    stripped = line.strip()
    if not (stripped.startswith("|") and stripped.endswith("|")):
        return None
    cells = [cell.strip().replace(r"\|", "|") for cell in re.split(r"(?<!\\)\|", stripped)]
    if cells and not cells[0]:
        cells.pop(0)
    if cells and not cells[-1]:
        cells.pop()
    return cells


def _api_name(cell: str) -> str:
    return re.sub(r"\*\*(.+?)\*\*", r"\1", cell).strip()


def _documentation_url(cells: list[str]) -> str | None:
    if len(cells) == 5:
        docs_cell = cells[4]
    elif len(cells) == 6:
        docs_cell = cells[5]
    else:
        return None
    match = _LINK_RE.search(docs_cell)
    return match.group(1).strip() if match else None


def plan_retirements(report: dict, apis_dir: str | Path = "apis") -> list[dict]:
    """Return exact row deletions, rejecting the entire report if any target is unsafe."""
    root = Path(apis_dir).resolve()
    if not root.is_dir():
        raise ValueError(f"API catalog directory does not exist: {root}")

    signals = report.get("shutdown_signals")
    if not isinstance(signals, list) or not signals:
        return []

    plan: list[dict] = []
    seen: set[tuple[Path, int]] = set()
    for index, item in enumerate(signals, 1):
        status = item.get("status")
        if not isinstance(status, int) or not 200 <= status < 400 or item.get("error"):
            raise ValueError(f"Signal {index}: documentation fetch is not conclusive (HTTP {status!r}).")

        signal = item.get("shutdown_signal") or {}
        if signal.get("scope") != "provider-or-current-api" or signal.get("review_required") is not True:
            raise ValueError(f"Signal {index}: lifecycle classifier did not mark this as current-provider/current-API.")
        if signal.get("type") not in _ALLOWED_SIGNAL_TYPES or not signal.get("matched_text"):
            raise ValueError(f"Signal {index}: no recognized explicit lifecycle phrase was supplied.")

        apis = item.get("apis")
        if not isinstance(apis, list) or len(apis) != 1:
            count = len(apis) if isinstance(apis, list) else 0
            raise ValueError(
                f"Signal {index}: documentation URL maps to {count} catalog APIs; automatic removal requires exactly one."
            )

        api = apis[0]
        name = str(api.get("name") or "").strip()
        relative_file = str(api.get("file") or "").strip()
        docs_url = str(item.get("url") or "").strip()
        if not name or not relative_file or not docs_url:
            raise ValueError(f"Signal {index}: missing API name, catalog file, or documentation URL metadata.")

        candidate_path = Path(relative_file)
        if not candidate_path.is_absolute():
            if candidate_path.parts and candidate_path.parts[0] == root.name:
                candidate_path = (root.parent / candidate_path).resolve()
            else:
                candidate_path = (root / candidate_path).resolve()
        else:
            candidate_path = candidate_path.resolve()
        if candidate_path != root and root not in candidate_path.parents:
            raise ValueError(f"Signal {index}: catalog path escapes the apis directory: {relative_file!r}.")
        if not candidate_path.is_file():
            raise ValueError(f"Signal {index}: catalog file does not exist: {candidate_path}.")

        lines = candidate_path.read_text(encoding="utf-8").splitlines(keepends=True)
        matches: list[int] = []
        for line_number, line in enumerate(lines, 1):
            cells = _row_cells(line)
            if not cells or len(cells) not in (5, 6):
                continue
            if _api_name(cells[0]).casefold() != name.casefold():
                continue
            if _documentation_url(cells) != docs_url:
                continue
            matches.append(line_number)

        if len(matches) != 1:
            raise ValueError(
                f"Signal {index}: expected one exact catalog row for {name!r} and its documentation URL; found {len(matches)}."
            )

        row_number = matches[0]
        metadata_line = api.get("line")
        if metadata_line is not None and metadata_line != row_number:
            print(
                f"Signal {index}: catalog row moved from line {metadata_line} to {row_number}; exact identity matched.",
                file=sys.stderr,
            )

        key = (candidate_path, row_number)
        if key in seen:
            continue
        seen.add(key)
        plan.append({
            "name": name,
            "file": candidate_path,
            "line": row_number,
            "documentation_url": docs_url,
            "signal": str(signal.get("matched_text")),
        })

    return plan


def apply_retirements(plan: list[dict], *, apis_dir: str | Path = "apis", max_delete: int = 25) -> list[dict]:
    """Remove planned rows after enforcing a small batch safety cap."""
    if max_delete < 1:
        raise ValueError("--max-delete must be at least 1.")
    if len(plan) > max_delete:
        raise ValueError(f"Safety brake: {len(plan)} API rows exceed --max-delete={max_delete}; no files changed.")

    grouped: dict[Path, set[int]] = {}
    for item in plan:
        grouped.setdefault(Path(item["file"]), set()).add(int(item["line"]))

    for path, line_numbers in grouped.items():
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        for line_number in sorted(line_numbers, reverse=True):
            del lines[line_number - 1]
        path.write_text("".join(lines), encoding="utf-8", newline="\n")

    return [
        {key: value for key, value in item.items() if key != "file"} | {"file": str(item["file"])}
        for item in plan
    ]


def _write_summary(items: list[dict], *, applied: bool, reason: str = "") -> None:
    scripts_dir = Path("scripts")
    scripts_dir.mkdir(parents=True, exist_ok=True)
    serializable = [{**item, "file": str(item["file"])} for item in items]
    payload = {
        "count": len(serializable),
        "applied": applied,
        "reason": reason,
        "retired": serializable if applied else [],
    }
    (scripts_dir / "retired_api_summary.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    title = "Removed retired API rows" if applied else "DRY RUN — retired API rows requiring validation"
    lines = [title, ""]
    if reason:
        lines.extend([f"Safety review: {reason}", ""])
    lines.extend(["| # | API | File | Documentation |", "|---:|---|---|---|"])
    for index, item in enumerate(serializable, 1):
        lines.append(f"| {index} | {item['name']} | {item['file']} | {item['documentation_url']} |")
    if not serializable:
        lines.append("No unambiguous retired API rows were found.")
    (scripts_dir / "retired_api_summary.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Plan or apply exact catalog removals for explicitly retired APIs.")
    parser.add_argument("--report", default="scripts/shutdown_signals.json", help="JSON report from check_shutdown_signals.py")
    parser.add_argument("--apis-dir", default="apis", help="Catalog Markdown directory")
    parser.add_argument("--apply", action="store_true", help="Apply removals; without this flag the command is a dry run")
    parser.add_argument("--max-delete", type=int, default=25, help="Maximum rows eligible in one workflow run")
    args = parser.parse_args()

    try:
        report = json.loads(Path(args.report).read_text(encoding="utf-8"))
        plan = plan_retirements(report, args.apis_dir)
        if not plan:
            _write_summary([], applied=False, reason="No eligible current-provider/current-API rows.")
            print("No eligible lifecycle removals. Existing lifecycle issue remains open for review.")
            return 0
        if args.apply:
            applied = apply_retirements(plan, apis_dir=args.apis_dir, max_delete=args.max_delete)
            _write_summary(applied, applied=True)
            print(f"Applied {len(applied)} exact retired API row removal(s).")
        else:
            _write_summary(plan, applied=False)
            print(f"DRY RUN: {len(plan)} unambiguous retired API row(s); no files changed.")
        return 0
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as error:
        _write_summary([], applied=False, reason=str(error))
        print(f"REMEDIATION WITHHELD: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
