# -*- coding: utf-8 -*-
"""Wave-10 moves: rescue 2 mis-slotted rows found by deep-research.
Udemy(instructor): personality-quotes -> education ; Yelp Fusion: food-drink -> reviews."""
import re
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from add_wave2 import APIS, ROW_RE

MOVES = [
    ("personality-quotes", "Udemy(instructor)", "education"),
    ("food-drink", "Yelp Fusion", "reviews"),
]


def sort_block(fpath):
    lines = fpath.read_text(encoding="utf-8").splitlines()
    idx = [i for i, l in enumerate(lines) if l.startswith("| **")]
    first, last = idx[0], idx[-1]
    new = sorted(lines[first:last + 1], key=lambda l: ROW_RE.match(l).group(1).lower())
    fpath.write_text("\n".join(lines[:first] + new + lines[last + 1:]) + "\n", encoding="utf-8")
    return len(new)


def main():
    for src, token, dst in MOVES:
        sp = APIS / f"{src}.md"
        dp = APIS / f"{dst}.md"
        slines = sp.read_text(encoding="utf-8").splitlines()
        match = [l for l in slines if ROW_RE.match(l) and token.lower() in ROW_RE.match(l).group(1).lower()]
        if not match:
            print(f"  !! not found in {src}: {token}")
            continue
        row = match[0]
        dlines = dp.read_text(encoding="utf-8").splitlines()
        if any(token.lower() in ROW_RE.match(l).group(1).lower() for l in dlines if ROW_RE.match(l)):
            print(f"  !! already in {dst}: {token} -> skipping")
            continue
        slines = [l for l in slines if l != row]
        sp.write_text("\n".join(slines) + "\n", encoding="utf-8")
        sort_block(sp)
        dlines.append(row)
        dp.write_text("\n".join(dlines) + "\n", encoding="utf-8")
        sort_block(dp)
        print(f"  moved {token}: {src} -> {dst}")


if __name__ == "__main__":
    main()
