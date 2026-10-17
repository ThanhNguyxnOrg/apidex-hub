# -*- coding: utf-8 -*-
"""One-off: regenerate README 3-column category table from apis/*.md (2026-10-17)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APIS = ROOT / "apis"

cats = []
for p in sorted(APIS.glob("*.md")):
    head = p.read_text(encoding="utf-8").split("\n")[0]
    m = re.match(r'^##\s+(?:<a\s+id="([^"]+)"\s*>\s*</a>\s*)?(\S+)\s+(.+)$', head.strip())
    if m:
        cats.append((m.group(3).strip(), m.group(2), m.group(1) or p.stem, p.name))
cats.sort(key=lambda c: c[0].lower())

lines = ["| Category | Category | Category |", "| --- | --- | --- |"]
for i in range(0, len(cats), 3):
    chunk = cats[i:i + 3]
    cells = [f"[{e} {n}](./apis/{fn})" for n, e, _, fn in chunk]
    while len(cells) < 3:
        cells.append("")
    lines.append("| " + " | ".join(cells) + " |")
new_table = "\n".join(lines)

readme = (ROOT / "README.md").read_text(encoding="utf-8")
pattern = re.compile(r"\| Category \| Category \| Category \|\n\| --- \| --- \| --- \|(?:\n\|[^\n]*)*")
assert pattern.search(readme), "table not found"
readme = pattern.sub(new_table, readme, count=1)
(ROOT / "README.md").write_text(readme, encoding="utf-8", newline="\n")
print("OK categories:", len(cats))
