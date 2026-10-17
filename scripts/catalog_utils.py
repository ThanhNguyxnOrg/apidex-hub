# -*- coding: utf-8 -*-
"""Shared helpers for catalog maintenance waves (athing used by every wave script).

Invariants:
- `apis/*.md` is the source of truth; table rows must stay inside the contiguous
  row block that ends right before the blank line + back-link footer — inserting
  (or sorting) a row after that footer breaks scripts/parse_readme.py.
- `norm_url()` intentionally lowercases and rewrites https:// -> http://. That
  exact normalization has driven every dedupe decision in this repo's history;
  do NOT change it without re-auditing all URL comparisons.

Run wave scripts with the repo root as working directory.
"""
import re
import ssl
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APIS = ROOT / "apis"

ROW_RE = re.compile(r"^\| \*\*(.+?)\*\*")
ROW_TMPL = "| **{name}** | {desc} | {auth} | ✅ | [Link]({url}) |"


def norm_url(u: str) -> str:
    return u.rstrip("/").lower().replace("https://", "http://")


def url_alive(url: str) -> bool:
    """Cheap urllib liveness probe. NOTE: on this Windows machine urllib gives
    false DNS/SSL negatives for some hosts — prefer PowerShell Invoke-WebRequest
    for verdicts; this only exists as a fallback utility."""
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (apidex-hub-linkcheck)"})
    try:
        with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
            return r.status < 400
    except urllib.error.HTTPError as e:
        return e.code in (401, 403, 405)  # protected but alive
    except Exception as e:
        print(f"    !! fetch error {e!r}")
        return False


def collect_index():
    """Existing names (lowercased) + normalized URLs across apis/*.md row lines.
    This is the dedupe basis: exact-name (case-insensitive) and norm_url match."""
    names, urls = set(), set()
    for f in APIS.glob("*.md"):
        for line in f.read_text(encoding="utf-8").splitlines():
            if not line.startswith("| **"):
                continue
            m = ROW_RE.match(line)
            if m:
                names.add(m.group(1).strip().lower())
            for u in re.findall(r"\((https?://[^)]+)\)", line):
                urls.add(norm_url(u))
    return names, urls


def insert_rows(fpath, rows):
    """Footer-safe insert: extend the contiguous row block before the footer and
    re-sort that block alphabetically. Returns new block size."""
    lines = fpath.read_text(encoding="utf-8").splitlines()
    idx = [i for i, l in enumerate(lines) if l.startswith("| **")]
    first, last = idx[0], idx[-1]
    new = sorted(lines[first:last + 1] + rows, key=lambda l: ROW_RE.match(l).group(1).lower())
    fpath.write_text("\n".join(lines[:first] + new + lines[last + 1:]) + "\n", encoding="utf-8")
    return len(new)
