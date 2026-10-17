# -*- coding: utf-8 -*-
"""Fix follow-ups after maintain_catalog run (2026-10-17):
 - collapse blank lines inside markdown tables
 - repair dead/duplicate links introduced by the batch
"""
import re
from pathlib import Path

APIS = Path(__file__).resolve().parent.parent / "apis"

# --- 1. link fixes (dead or duplicate) ---
FIXES = {
    "museums-art.md": [
        ("[Link](https://data.rijksmuseum.nl/object-metadata/api/)", "[Link](https://data.rijksmuseum.nl/)"),
        ("[Link](https://api.si.edu/)", "[Link](https://api.si.edu/openaccess/api/v1.0/)"),
    ],
    "demographic-analysis.md": [
        ("[Link](https://datausa.io/api/)", "[Link](https://datausa.io/)"),
    ],
    "podcasts.md": [
        ("[Link](https://api.podchaser.com/docs)", "[Link](https://podchaser.com/developers)"),
    ],
    "math-computation.md": [
        # Numbers API is dead (404/SSL) - remove the row entirely
        ("| **Numbers API** | Fun math facts about any number or date (**No Auth**). | No | ✅ | [Link](http://numbersapi.com/) |\n", ""),
    ],
    "travel-tourism.md": [
        ("[Link](https://opentripmap.io/docs)", "[Link](https://dev.opentripmap.com/docs)"),
    ],
    "qr-barcode.md": [
        # duplicate of goQR.me (same URL) - remove
        ("| **QR Code Generator** | Dynamic QR code generation API. | No | ✅ | [Link](https://goqr.me/api/) |\n", ""),
    ],
    "web-scraping-crawling.md": [
        ("[Link](https://www.browse.ai/docs)", "[Link](https://docs.browse.ai/api/)"),
    ],
}

for fname, pairs in FIXES.items():
    p = APIS / fname
    t = p.read_text(encoding="utf-8")
    for old, new in pairs:
        if old not in t:
            print(f"WARN not found in {fname}: {old[:60]}")
            continue
        t = t.replace(old, new)
    p.write_text(t, encoding="utf-8", newline="\n")

# --- 2. collapse blank lines between table rows, in every file ---
def collapse_table_blanks(path: Path):
    lines = path.read_text(encoding="utf-8").split("\n")
    changed = False
    out = []
    for line in lines:
        if out and line.strip() == "" and out[-1].strip().startswith("|") :
            # peek: only collapse if a table row follows
            changed = True
            continue
        out.append(line)
    if changed:
        path.write_text("\n".join(out), encoding="utf-8", newline="\n")
    return changed

n = 0
for f in sorted(APIS.glob("*.md")):
    if collapse_table_blanks(f):
        n += 1
print(f"collapsed blanks in {n} files")

# --- 3. re-alphabetize the two touched files (rows shifted) ---
def sort_file(path: Path):
    lines = path.read_text(encoding="utf-8").split("\n")
    rows, idxs = [], []
    for i, l in enumerate(lines):
        s = l.strip()
        if s.startswith("|") and re.search(r"\]\(https?://", s) and re.match(r"^\|\s*\*\*", s):
            rows.append(l); idxs.append(i)
    if len(rows) < 2:
        return
    rows_sorted = sorted(rows, key=lambda r: re.match(r"^\|\s*\*\*(.+?)\*\*", r.strip()).group(1).lower())
    for i, r in zip(idxs, rows_sorted):
        lines[i] = r
    path.write_text("\n".join(lines), encoding="utf-8", newline="\n")

for f in ["museums-art.md", "demographic-analysis.md", "podcasts.md", "math-computation.md", "travel-tourism.md", "qr-barcode.md"]:
    sort_file(APIS / f)

# --- 4. duplicate URL global scan ---
from collections import defaultdict
url_map = defaultdict(list)
for f in sorted(APIS.glob("*.md")):
    for line in f.read_text(encoding="utf-8").split("\n"):
        m = re.search(r"\]\((https?://[^)]+)\)", line)
        nm = re.match(r"^\|\s*\*\*(.+?)\*\*", line.strip())
        if m and nm:
            url_map[m.group(1).rstrip("/").lower()].append((nm.group(1), f.stem))
dups = {k: v for k, v in url_map.items() if len(v) > 1}
print("duplicate URLs:", len(dups))
for k, v in dups.items():
    print(" ", k, "->", v)
