# -*- coding: utf-8 -*-
"""Wave-3 follow-up: relocate existing rows into their new topical categories (no duplicates)."""
import re
from pathlib import Path

APIS = Path("apis")
ROW_RE = re.compile(r"^\| \*\*(.+?)\*\*")

# (from_slug, [names to move], to_slug)
MOVES = [
    ("public-data", ["EPO", "PatentsView", "USPTO"], "patents"),
    ("transportation", ["Mercedes-Benz", "NHTSA", "NHTSA Recalls", "Smartcar", "Brazilian Vehicles and Prices"], "vehicle"),
    ("development", ["IP2Location", "IPGeolocation", "IPinfo"], "networking-dns"),
]

# rename FIPE row title when it lands in vehicle
RENAMES = {"Brazilian Vehicles and Prices": "FIPE"}


def rows_of(fpath):
    lines = fpath.read_text(encoding="utf-8").splitlines()
    return lines


def main():
    for from_slug, names, to_slug in MOVES:
        src = APIS / f"{from_slug}.md"
        dst = APIS / f"{to_slug}.md"
        src_lines = rows_of(src)
        dst_lines = rows_of(dst)
        moved = []
        keep = []
        for l in src_lines:
            if l.startswith("| **"):
                m = ROW_RE.match(l)
                n = m.group(1).strip() if m else None
                if n in names:
                    if n in RENAMES:
                        l = l.replace(f"**{n}**", f"**{RENAMES[n]}**", 1)
                    moved.append(l)
                else:
                    keep.append(l)
            else:
                keep.append(l)
        if len(moved) != len(names):
            missing = set(names) - {ROW_RE.match(l).group(1).strip() for l in moved}
            raise RuntimeError(f"{from_slug}: failed to find {missing}")
        src.write_text("\n".join(keep) + "\n", encoding="utf-8")

        d_head = [l for l in dst_lines if l.startswith("| **")]
        d_before = dst_lines[: dst_lines.index(d_head[0])]
        d_last = len(dst_lines) - 1 - dst_lines[::-1].index(d_head[-1])
        d_tail = dst_lines[d_last + 1:]
        new_rows = sorted(d_head + moved, key=lambda l: ROW_RE.match(l).group(1).lower())
        dst.write_text("\n".join(d_before + new_rows + d_tail) + "\n", encoding="utf-8")
        print(f"moved {len(moved)} rows {from_slug} -> {to_slug}: {[ROW_RE.match(l).group(1) for l in moved]}")


if __name__ == "__main__":
    main()
