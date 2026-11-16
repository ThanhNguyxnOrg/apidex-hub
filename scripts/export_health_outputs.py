#!/usr/bin/env python3
"""Export structured API health results as safe GitHub Actions step outputs."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
import uuid

STATES = ("working", "protected", "warning", "error", "broken", "unknown")
LIST_FILES = {
    "broken_list": "broken_urls.txt",
    "error_list": "error_urls.txt",
    "warning_list": "warning_urls.txt",
    "unknown_list": "unknown_urls.txt",
    "protected_list": "protected_urls.txt",
}


def load_results(path: str | Path) -> dict[str, list]:
    """Load final Stage 2 results and reject incomplete or empty scans."""
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Could not read final API health results: {error}") from error

    if not isinstance(payload, dict):
        raise ValueError("Final API health results must be a JSON object.")

    for state in STATES:
        if not isinstance(payload.get(state), list):
            raise ValueError(f"Final API health results are missing the '{state}' list.")
        for index, item in enumerate(payload[state]):
            if not isinstance(item, dict) or not isinstance(item.get("url"), str) or not item["url"].strip():
                raise ValueError(f"Invalid {state} result at index {index}: an endpoint URL is required.")

    if sum(len(payload[state]) for state in STATES) == 0:
        raise ValueError("Final API health results contain zero checked endpoints; refusing to publish an empty dashboard.")

    return payload


def build_scalar_outputs(results: dict[str, list]) -> dict[str, str]:
    """Build stable summary outputs from the final classified endpoint records."""
    counts = {state: len(results[state]) for state in STATES}
    return {
        "broken_count": str(counts["broken"]),
        "ok_count": str(counts["working"]),
        "protected_count": str(counts["protected"]),
        "warn_count": str(counts["warning"]),
        "err_count": str(counts["error"]),
        "unknown_count": str(counts["unknown"]),
        "has_broken": "true" if counts["broken"] else "false",
    }


def append_github_outputs(
    results: dict[str, list],
    reports_dir: str | Path,
    output_path: str | Path,
) -> None:
    """Append scalar and multiline output values using collision-resistant delimiters."""
    report_root = Path(reports_dir)
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    with destination.open("a", encoding="utf-8", newline="\n") as output:
        for key, value in build_scalar_outputs(results).items():
            output.write(f"{key}={value}\n")

        for key, filename in LIST_FILES.items():
            report_path = report_root / filename
            try:
                value = report_path.read_text(encoding="utf-8")
            except FileNotFoundError:
                value = ""
            delimiter = "APIDEX_" + uuid.uuid4().hex
            output.write(f"{key}<<{delimiter}\n")
            output.write(value)
            if value and not value.endswith("\n"):
                output.write("\n")
            output.write(f"{delimiter}\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export final Stage 2 API health data to GitHub Actions outputs."
    )
    parser.add_argument("--results", required=True, help="Path to the final results.json file")
    parser.add_argument("--reports-dir", required=True, help="Directory containing the URL list report files")
    parser.add_argument(
        "--output",
        default=os.environ.get("GITHUB_OUTPUT", ""),
        help="GitHub Actions output file (defaults to GITHUB_OUTPUT)",
    )
    args = parser.parse_args()

    if not args.output:
        parser.error("--output or the GITHUB_OUTPUT environment variable is required")

    try:
        results = load_results(args.results)
        append_github_outputs(results, args.reports_dir, args.output)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    except OSError as error:
        print(f"ERROR: Could not write GitHub Actions outputs: {error}", file=sys.stderr)
        return 2

    counts = build_scalar_outputs(results)
    print(
        "Exported final API health outputs: "
        f"{counts['ok_count']} working, {counts['protected_count']} protected, "
        f"{counts['warn_count']} warnings, {counts['err_count']} errors, "
        f"{counts['unknown_count']} unknown, {counts['broken_count']} broken."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
