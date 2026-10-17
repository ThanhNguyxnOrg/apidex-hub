# -*- coding: utf-8 -*-
"""Wave-4 (2026-10-17):
1) Remove 8 accidental same-service duplicate rows (1 API listed twice).
2) Merge date-time.md into calendar-holidays.md (slug kept, title widened).
3) Relocate TIPO -> patents, WolframAlpha -> math-computation.
4) Add 9 newly verified APIs.
All doc URLs were HTTP-verified before this script ran."""
import re
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from add_wave2 import norm_url, APIS, ROW_RE

# ---------- 1. dedupe removals: (file, names to drop) ----------
REMOVE = [
    ("sports", ["CricketData"]),           # keep first occurrence only
    ("public-data", ["Nager.Date", "TimeZoneDB", "World Bank"]),  # homes in calendar-holidays / demographic-analysis
    ("development", ["Neon", "ScraperApi"]),  # homes: backend-database / web-scraping-crawling
    ("travel-tourism", ["Opentripmap"]),    # home: geocoding
    ("monitoring-observability", ["Better Stack (Logtail)"]),  # same product as Better Stack
    ("science", ["Wolfram Short Answers"]),  # same products.wolframalpha.com as WolframAlpha
]

RENAME = [  # (file, old name, new name)
    ("government-civic", "Open Government, Mexico", "INEGI"),  # 2nd row points at inegi.org.mx
]

# ---------- 2. merge date-time into calendar-holidays ----------
MERGE_FROM = "date-time"
MERGE_INTO = "calendar-holidays"

# ---------- 3. relocations: (name, from, to) ----------
MOVE = [
    ("TIPO", "public-data", "patents"),
    ("WolframAlpha", "machine-learning", "math-computation"),
]

# ---------- 4. additions ----------
ADDITIONS = [
    ("qr-barcode", "QR Server", "Generate QR codes as PNG/SVG from any text or URL.", "No", "https://api.qrserver.com/v1/create-qr-code/"),
    ("url-shorteners", "T.LY", "Short links with click analytics and QR codes.", "🔑 ApiKey", "https://t.ly/api"),
    ("reviews", "Glassdoor", "Employer reviews, salaries and interview insights.", "🔑 ApiKey", "https://www.glassdoor.com/developer"),
    ("development", "Can I Use", "Browser support tables for web platform features.", "No", "https://caniuse.com/api"),
    ("music", "Apple Music", "Catalog search, playlists and user libraries.", "🔑 ApiKey", "https://developer.apple.com/documentation/applemusicapi"),
    ("education", "Stack Exchange", "Questions and answers across 180+ Stack Exchange sites.", "No", "https://api.stackexchange.com/docs"),
    ("networking-dns", "BGP Tools", "BGP, ASN, prefix and domain intelligence lookups.", "🔑 ApiKey", "https://bgp.tools/"),
    ("networking-dns", "Shodan InternetDB", "Free passively-collected port and host data for any IP.", "No", "https://internetdb.shodan.io/"),
]

ROW_TMPL = "| **{name}** | {desc} | {auth} | ✅ | [Link]({url}) |"


def read(fpath):
    return fpath.read_text(encoding="utf-8").splitlines()


def split_table(lines):
    rows = [i for i, l in enumerate(lines) if l.startswith("| **")]
    if not rows:
        raise RuntimeError("no rows")
    return rows[0], rows[-1]


def write_rows(fpath, all_lines):
    fpath.write_text("\n".join(all_lines) + "\n", encoding="utf-8")


def main():
    # 1. removals
    for slug, names in REMOVE:
        fpath = APIS / f"{slug}.md"
        lines = read(fpath)
        seen = set()
        out, dropped = [], []
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

    # rename
    for slug, old, new in RENAME:
        fpath = APIS / f"{slug}.md"
        lines = read(fpath)
        hit = False
        # rename only the SECOND occurrence (first is datos.gob.mx)
        idxs = [i for i, l in enumerate(lines) if l.startswith(f"| **{old}**")]
        if len(idxs) != 2:
            raise RuntimeError(f"{slug}: expected 2 rows named {old}, got {len(idxs)}")
        i = idxs[1]
        lines[i] = lines[i].replace(f"**{old}**", f"**{new}**", 1)
        write_rows(fpath, lines)
        print(f"  renamed {slug}: row2 {old} -> {new}")

    # 2. merge date-time into calendar-holidays
    src = APIS / f"{MERGE_FROM}.md"
    dst = APIS / f"{MERGE_INTO}.md"
    src_lines = read(src)
    moving = [l for l in src_lines if l.startswith("| **")]
    dst_lines = read(dst)
    first, last = split_table(dst_lines)
    before = dst_lines[:first]
    tail = dst_lines[last + 1:]
    new_rows = sorted([l for l in dst_lines[first:last + 1]] + moving,
                      key=lambda l: ROW_RE.match(l).group(1).lower())
    before = [l.replace("📅 Calendar & Holidays", "📅 Calendar, Holidays & Time")
              if l.startswith("## ") else l for l in before]
    write_rows(dst, before + new_rows + tail)
    src.unlink()
    print(f"  merged {MERGE_FROM} -> {MERGE_INTO}: +{len(moving)} rows, deleted {MERGE_FROM}.md")

    # 3. relocations
    for name, frm, to in MOVE:
        srcf = APIS / f"{frm}.md"
        lines = read(srcf)
        row = None
        out = []
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
        before = dlines[:first]
        tail = dlines[last + 1:]
        rows = sorted([l for l in dlines[first:last + 1]] + [row],
                      key=lambda l: ROW_RE.match(l).group(1).lower())
        write_rows(dstf, before + rows + tail)
        print(f"  moved {name}: {frm} -> {to}")

    # 4. additions (dedupe by name+URL against current catalog)
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
        before = lines[:first]
        tail = lines[last + 1:]
        new = sorted([l for l in lines[first:last + 1]] + rows,
                     key=lambda l: ROW_RE.match(l).group(1).lower())
        write_rows(fpath, before + new + tail)
        print(f"  added to {fpath.stem}: +{len(rows)} -> {len(new)} rows")

    print(f"\nADDED={added} SKIPPED={skipped}")


if __name__ == "__main__":
    main()
