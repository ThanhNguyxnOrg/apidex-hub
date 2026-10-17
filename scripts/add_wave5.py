# -*- coding: utf-8 -*-
"""Wave-5 (2026-10-17):
1) Dedupe: TheDogAPI (same service listed twice in animals), Spaceflight News (news + photography).
2) Relocate Fitbit/Strava/Tredict from sports -> fitness-wellness (wearable/fitness homes).
3) Add 5 newly verified APIs.
All doc URLs HTTP-verified before this script ran."""
import re
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from add_wave2 import norm_url, APIS, ROW_RE

REMOVE = [
    ("animals", ["The Dog API"]),  # same service as TheDogAPI (thedogapi.com)
    ("photography", ["Spaceflight News"]),  # home: news
]

MOVE = [
    ("Fitbit", "sports", "fitness-wellness"),
    ("Strava", "sports", "fitness-wellness"),
    ("Tredict", "sports", "fitness-wellness"),
]

ADDITIONS = [
    ("books", "Gutendex", "Project Gutenberg book catalogue as JSON.", "No", "https://gutendex.com/"),
    ("science", "Europe PMC", "Biomedical and life science literature search.", "No", "https://www.ebi.ac.uk/europepmc/webservices/rest/search"),
    ("museums-art", "Victoria and Albert Museum", "V&A collection objects, images and exhibitions.", "No", "https://api.vam.ac.uk/v2/objects/search"),
    ("museums-art", "Wikimedia Commons", "Freely usable images, media and general media files.", "No", "https://commons.wikimedia.org/w/api.php"),
    ("math-computation", "Desmos API", "Graphing calculator embed and computation API.", "No", "https://www.desmos.com/api"),
    ("patents", "Espacenet", "European patent publication search and full documents.", "🔑 ApiKey", "https://worldwide.espacenet.com/"),
]

ROW_TMPL = "| **{name}** | {desc} | {auth} | ✅ | [Link]({url}) |"


def read(fpath):
    return fpath.read_text(encoding="utf-8").splitlines()


def split_table(lines):
    rows = [i for i, l in enumerate(lines) if l.startswith("| **")]
    if not rows:
        raise RuntimeError("no rows")
    return rows[0], rows[-1]


def write_rows(fpath, lines):
    fpath.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    # 1. dedupe removals
    for slug, names in REMOVE:
        fpath = APIS / f"{slug}.md"
        lines = read(fpath)
        seen, out, dropped = set(), [], []
        for l in lines:
            if l.startswith("| **"):
                n = ROW_RE.match(l).group(1).strip()
                if n in names and n not in seen:
                    seen.add(n)
                    dropped.append(n)
                    continue
            out.append(l)
        missing = set(names) - set(dropped)
        if missing:
            raise RuntimeError(f"{slug}: cannot drop {missing}")
        write_rows(fpath, out)
        print(f"  deduped {slug}: dropped {dropped}")

    # 2. relocations
    for name, frm, to in MOVE:
        srcf = APIS / f"{frm}.md"
        lines = read(srcf)
        row, out = None, []
        for l in lines:
            if l.startswith(f"| **{name}**") and row is None:
                row = l
            else:
                out.append(l)
        if row is None:
            raise RuntimeError(f"{frm}: row {name} not found")
        write_rows(srcf, out)
        dstf = APIS / f"{to}.md"
        dlines = read(dstf)
        first, last = split_table(dlines)
        new = sorted([l for l in dlines[first:last + 1]] + [row],
                     key=lambda l: ROW_RE.match(l).group(1).lower())
        write_rows(dstf, dlines[:first] + new + dlines[last + 1:])
        print(f"  moved {name}: {frm} -> {to}")

    # 3. additions
    names, urls = set(), set()
    for f in APIS.glob("*.md"):
        for line in read(f):
            if line.startswith("| **"):
                m = ROW_RE.match(line)
                if m:
                    names.add(m.group(1).strip().lower())
                for u in re.findall(r"\((https?://[^)]+)\)", line):
                    urls.add(norm_url(u))

    per_file = {}
    added = skipped = 0
    for slug, name, desc, auth, url in ADDITIONS:
        if name.lower() in names or norm_url(url) in urls:
            skipped += 1
            print(f"  skip dup: {name}")
            continue
        names.add(name.lower())
        urls.add(norm_url(url))
        per_file.setdefault(APIS / f"{slug}.md", []).append(
            ROW_TMPL.format(name=name, desc=desc, auth=auth, url=url))
        added += 1

    for fpath, rows in per_file.items():
        lines = read(fpath)
        first, last = split_table(lines)
        new = sorted([l for l in lines[first:last + 1]] + rows,
                     key=lambda l: ROW_RE.match(l).group(1).lower())
        write_rows(fpath, lines[:first] + new + lines[last + 1:])
        print(f"  added to {fpath.stem}: +{len(rows)} -> {len(new)} rows")

    print(f"\nADDED={added} SKIPPED={skipped}")


if __name__ == "__main__":
    main()
