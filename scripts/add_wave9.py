# -*- coding: utf-8 -*-
"""Wave-9 (2026-10-17): additions verified live (200/308/403-405 protected-alive retested with GET). None duplicate by URL or name."""
import re
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from add_wave2 import norm_url, APIS, ROW_RE

ADDITIONS = [
    ("games-comics", "YGOPRODeck", "Yu-Gi-Oh! card database with prices, banlist and artwork.", "No", "https://ygoprodeck.com/api-guide/"),
    ("security-validation", "NVD", "U.S. National Vulnerability Database with CVE feeds and search.", "No", "https://nvd.nist.gov/developers"),
    ("security-validation", "Vulners", "Vulnerability intelligence with exploit and CVE archive search.", "🔑 ApiKey", "https://vulners.com/"),
    ("design-colors", "Fontshare", "Free shared-font catalogue API by Indian Type Foundry.", "No", "https://api.fontshare.com/"),
    ("design-colors", "Canva Connect", "Design automation: assets, brand kits and exports.", "🔐 OAuth", "https://www.canva.dev/docs/connect/"),
    ("social", "LINE Messaging", "LINE messenger bots, pushes and webhooks.", "🔑 ApiKey", "https://developers.line.biz/en/docs/"),
    ("text-analysis-nlp", "Lingva", "Open, privacy-friendly Google Translate front-end API.", "No", "https://lingva.ml/"),
    ("web-scraping-crawling", "SerpApi", "Production-ready Google and other SERP scraping API.", "🔑 ApiKey", "https://serpapi.com/"),
    ("web-scraping-crawling", "Kagi", "Kagi Search API for paid web search results.", "🔑 ApiKey", "https://help.kagi.com/kagi/api/search.html"),
    ("web-scraping-crawling", "SerpHouse", "Search engine results scraping across Google and Bing.", "🔑 ApiKey", "https://serphouse.com/"),
    ("networking-dns", "Whoapi", "Domain availability, whois and DNS interrogation API.", "🔑 ApiKey", "https://whoapi.com/"),
]

ROW_TMPL = "| **{name}** | {desc} | {auth} | ✅ | [Link]({url}) |"


def insert_rows(fpath, rows):
    lines = fpath.read_text(encoding="utf-8").splitlines()
    idx = [i for i, l in enumerate(lines) if l.startswith("| **")]
    first, last = idx[0], idx[-1]
    new = sorted(lines[first:last + 1] + rows, key=lambda l: ROW_RE.match(l).group(1).lower())
    fpath.write_text("\n".join(lines[:first] + new + lines[last + 1:]) + "\n", encoding="utf-8")
    return len(new)


def main():
    names, urls = set(), set()
    for f in APIS.glob("*.md"):
        for line in f.read_text(encoding="utf-8").splitlines():
            m = ROW_RE.match(line)
            if m:
                names.add(m.group(1).strip().lower())
                for u in re.findall(r"\((https?://[^)]+)\)", line):
                    urls.add(norm_url(u))

    per_file, added, skipped = {}, 0, 0
    for slug, name, desc, auth, url in ADDITIONS:
        if name.lower() in names or norm_url(url) in urls:
            skipped += 1
            print(f"  skip dup: {name}")
            continue
        names.add(name.lower()); urls.add(norm_url(url))
        per_file.setdefault(APIS / f"{slug}.md", []).append(ROW_TMPL.format(name=name, desc=desc, auth=auth, url=url))
        added += 1

    for fpath, rows in per_file.items():
        insert_rows(fpath, rows)
        print(f"  {fpath.stem}: +{len(rows)}")
    print(f"ADDED={added} SKIPPED={skipped}")


if __name__ == "__main__":
    main()
