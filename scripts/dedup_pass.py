# -*- coding: utf-8 -*-
"""Dedup pass (2026-10-17, approved design):
1. Remove 28 same-service double-listed rows (keep the row with the better docs URL).
2. Rename Apify actors whose exact name collides with an official (non-apify) row -> append ' (Apify)'.
Same-domain multi-product rows (Google, Abstract, Smarty, End-points) are intentionally KEPT.
Footer-safe row surgery; keep-row existence verified before each deletion.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from add_wave2 import APIS, ROW_RE


def block_bounds(lines):
    start = next(i for i, l in enumerate(lines) if l.startswith("| **"))
    end = start
    while end + 1 < len(lines) and lines[end + 1].startswith("| **"):
        end += 1
    return start, end


def read_rows(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    start, end = block_bounds(lines)
    return lines, start, end


def write_rows(path, lines, start, block_rows, tail):
    block_rows = sorted(block_rows, key=lambda l: ROW_RE.match(l).group(1).lower())
    path.write_text("\n".join(lines[:start] + block_rows + tail) + "\n", encoding="utf-8")


def remove_row(slug, name, url_sub, keep_slug, keep_name):
    """Delete (slug, name, url-sub) only if keep-row exists in keep_slug file."""
    kp = APIS / f"{keep_slug}.md"
    klines, ks, ke = read_rows(kp)
    keep_ok = any(
        ROW_RE.match(l) and ROW_RE.match(l).group(1).strip() == keep_name
        for l in klines[ks:ke + 1]
    )
    if not keep_ok:
        print(f"  !! keep-row missing, ABORT delete: {keep_slug}/{keep_name}")
        return False

    p = APIS / f"{slug}.md"
    lines, s, e = read_rows(p)
    block = lines[s:e + 1]
    target = None
    for l in block:
        m = ROW_RE.match(l)
        if m and m.group(1).strip() == name and url_sub in l:
            target = l
            break
    if target is None:
        print(f"  !! not found (already gone?): {slug}/{name}")
        return False
    block.remove(target)
    write_rows(p, lines, s, block, lines[e + 1:])
    print(f"  removed {slug}/{name} (keep {keep_slug}/{keep_name})")
    return True


def main():
    # (file, name-to-remove, url-snippet-guard, keep-file, keep-name)
    REMOVALS = [
        ("animals", "TheCatAPI", "api.thecatapi.com", "animals", "The Cat API"),
        ("animals", "TheCatDB", "thecatapi.com", "animals", "The Cat API"),
        ("cloud-storage-files", "Web3 Storage", "web3.storage/", "cloud-storage-files", "Web3.Storage"),
        ("cryptocurrency", "Mempool", "mempool.space/api", "cryptocurrency", "Mempool.space"),
        ("development", "StackExchange", "api.stackexchange.com/", "education", "Stack Exchange"),
        ("development", "Google Firebase", "firebase.google.com/docs", "development", "Firebase"),
        ("development", "GitHub REST API", "docs.github.com/en/rest", "development", "GitHub"),
        ("government-civic", "Data USA", "datausa.io/about/api/", "demographic-analysis", "DataUSA"),
        ("government-civic", "EU Open Data Portal", "data.europa.eu/api/hub", "government-civic", "data.europa.eu"),
        ("government-civic", "OpenStates", "openstates.org/", "government-civic", "Open States"),
        ("geocoding", "Geocod.io", "geocod.io/", "geocoding", "Geocodio"),
        ("geocoding", "IP Address Details", "ipinfo.io/", "networking-dns", "IPinfo"),
        ("science", "Purple Air", "www2.purpleair.com", "environment-climate", "PurpleAir"),
        ("memes-fun", "Kanye.rest", "api.kanye.rest", "memes-fun", "Kanye Rest"),
        ("games-comics", "FunTranslations", "api.funtranslations.com", "memes-fun", "Fun Translations"),
        ("games-comics", "Magic The Gathering", "magicthegathering.io", "games-comics", "Magic: The Gathering"),
        ("memes-fun", "Zen Quotes", "zenquotes.io/", "personality-quotes", "ZenQuotes"),
        ("photography", "NewsData", "newsdata.io/docs", "news", "NewsData.io"),
        ("security-validation", "National Vulnerability Database", "nvd.nist.gov/vuln", "security-validation", "NVD"),
        ("social", "LINE Messaging", "developers.line.biz", "social", "LINE"),
        ("shopping", "Mercadolibre", "mercadolibre.cl", "shopping", "Mercado Libre"),
        ("finance", "MercadoPago", "mercadopago.com.br", "payments-billing", "Mercado Pago"),
        ("transportation", "Amadeus for Developers", "developers.amadeus.com", "travel-tourism", "Amadeus"),
        ("dictionaries", "Words", "wordsapi.com/docs", "dictionaries", "WordsAPI"),
        ("personality-quotes", "DummyJSON Quotes", "dummyjson.com/docs/quotes", "mock-data-testing", "DummyJSON"),
        ("photography", "DiceBear", "dicebear.com/introduction", "utilities-tools", "DiceBear Avatars"),
        ("public-data", "Microlink.io", "microlink.io", "development", "Microlink"),
    ]
    removed = 0
    for r in REMOVALS:
        removed += 1 if remove_row(*r) else 0

    # PokeAPI v2 (mojibake name): remove any games-comics row with URL pokeapi.co/api/v2
    p = APIS / "games-comics.md"
    lines, s, e = read_rows(p)
    block = lines[s:e + 1]
    target = [l for l in block if "pokeapi.co/api/v2" in l]
    if target:
        block.remove(target[0])
        write_rows(p, lines, s, block, lines[e + 1:])
        removed += 1
        print("  removed games-comics/PokeAPI v2 row")
    else:
        print("  !! pokeapi[df] v2 row not found")

    # 2. Apify actors with exact-name collisions vs official rows -> append ' (Apify)'
    official_names = {}
    for f in APIS.glob("*.md"):
        if f.stem.startswith("apify"):
            continue
        for l in f.read_text(encoding="utf-8").splitlines():
            m = ROW_RE.match(l)
            if m:
                official_names[m.group(1).strip().lower()] = m.group(1).strip()

    renames = []
    for f in APIS.glob("apify-*.md"):
        lines = f.read_text(encoding="utf-8").splitlines()
        s, e = block_bounds(lines)
        block = lines[s:e + 1]
        changed = False
        for i, l in enumerate(block):
            m = ROW_RE.match(l)
            if not m:
                continue
            nm = m.group(1).strip()
            if nm.lower() in official_names and not nm.endswith("(Apify)"):
                new_line = l.replace(f"| **{nm}** |", f"| **{nm} (Apify)** |", 1)
                if new_line != l:
                    block[i] = new_line
                    renames.append((f.stem, nm))
                    changed = True
        if changed:
            write_rows(f, lines, s, block, lines[e + 1:])

    print("\nREMOVED =", removed)
    print("RENAMED apify actors:")
    for slug, nm in renames:
        print(f"   {slug}: {nm} -> {nm} (Apify)")


if __name__ == "__main__":
    main()
