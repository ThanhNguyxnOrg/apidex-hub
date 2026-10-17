# -*- coding: utf-8 -*-
"""Wave-10 repair: 
1. education.md has Udemy(instructor) stray row AFTER the footer (partial-move crash) -> re-home inside table block.
2. Actually insert the 62 wave-10 rows (add_wave10.py printed success but never appended - loop bug).
3. Complete the Yelp Fusion move food-drink -> reviews (blocked by the crash).
All inserts are footer-safe: rows go INSIDE the contiguous table block; manifest/footer tail preserved.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from add_wave2 import norm_url, APIS, ROW_RE
from add_wave10 import ADDITIONS, ROW_TMPL, MOVES


def block_bounds(lines):
    start = next(i for i, l in enumerate(lines) if l.startswith("| **"))
    end = start
    while end + 1 < len(lines) and lines[end + 1].startswith("| **"):
        end += 1
    return start, end


def block_rows(lines):
    return [l for l in lines if ROW_RE.match(l)]


def write_sorted_block(fpath, extra_rows):
    """Sort existing table block + append extra_rows inside it. Stray rows beyond footer get re-homed."""
    lines = fpath.read_text(encoding="utf-8").splitlines()
    start, end = block_bounds(lines)
    block = lines[start:end + 1]
    tail = lines[end + 1:]
    strays = [l for l in tail if ROW_RE.match(l)]
    if strays:
        print(f"  re-homing {len(strays)} stray row(s) in {fpath.stem}")
        tail = [l for l in tail if not ROW_RE.match(l)]
    rows = block + (extra_rows or []) + strays
    new = sorted(rows, key=lambda l: ROW_RE.match(l).group(1).lower())
    fpath.write_text("\n".join(lines[:start] + new + tail) + "\n", encoding="utf-8")
    return len(new)


def remove_row(fpath, token):
    lines = fpath.read_text(encoding="utf-8").splitlines()
    rows = block_rows(lines)
    target = [l for l in rows if token.lower() in ROW_RE.match(l).group(1).lower()]
    if not target:
        return None
    lines.remove(target[0])
    fpath.write_text("\n".join(lines) + "\n", encoding="utf-8")
    write_sorted_block(fpath, [])
    return target[0]


def insert_row(fpath, row):
    lines = fpath.read_text(encoding="utf-8").splitlines()
    existing = block_rows(lines)
    token = ROW_RE.match(row).group(1).strip().lower()
    if any(token in ROW_RE.match(l).group(1).strip().lower() for l in existing):
        return "dup"
    write_sorted_block(fpath, [row])
    return "ok"


def main():
    existing_names, existing_urls = set(), set()
    for f in APIS.glob("*.md"):
        for line in f.read_text(encoding="utf-8").splitlines():
            m = ROW_RE.match(line)
            if m:
                existing_names.add(m.group(1).strip().lower())
                for u in re.findall(r"\((https?://[^)]+)\)", line):
                    existing_urls.add(norm_url(u))

    # 1+2: all ADDITIONS into their files (footer-safe), then per-file sort incorporates everything
    per_file, added, skipped = {}, 0, 0
    for slug, name, desc, auth, url in ADDITIONS:
        if name.lower() in existing_names or norm_url(url) in existing_urls:
            skipped += 1
            print(f"  skip dup: {name}")
            continue
        existing_names.add(name.lower()); existing_urls.add(norm_url(url))
        per_file.setdefault(APIS / f"{slug}.md", []).append(
            ROW_TMPL.format(name=name, desc=desc, auth=auth, url=url))
        added += 1

    for fpath, rows in per_file.items():
        write_sorted_block(fpath, rows)
        print(f"  {fpath.stem}: +{len(rows)}")
    print(f"ADDED={added} SKIPPED={skipped}")

    # 3: moves
    for src, token, dst in MOVES:
        found = [(f.name, l) for f in APIS.glob("*.md")
                 for l in block_rows(f.read_text(encoding="utf-8").splitlines())
                 if token.lower() in ROW_RE.match(l).group(1).lower()]
        if any(name == dst + ".md" for name, _ in found):
            print(f"  already in {dst}: {token} -> skip")
            continue
        srcfile, row = found[0]
        remove_row(APIS / srcfile, token)
        ok = insert_row(APIS / f"{dst}.md", row)
        print(f"  moved {token}: {src} -> {dst} ({ok})")


if __name__ == "__main__":
    main()
