# -*- coding: utf-8 -*-
"""Retry the wave-2 URLs that failed (likely transient network errors) with alternates."""
import sys
sys.path.insert(0, "scripts")
from add_wave2 import url_alive, norm_url, APIS, ROW_RE
import re

RETRIES = [
    ("news", "BBC", "BBC News content and programme metadata.", "\U0001f511 ApiKey", "https://www.bbc.co.uk/developers"),
    ("demographic-analysis", "Population (API Ninjas)", "Population data by country with historical records.", "\U0001f511 ApiKey", "https://api.ninjas.com/api/population"),
    ("shopping", "Target", "Roundel retail partner API for items and inventory.", "\U0001f511 ApiKey", "https://developers.target.com/apis"),
    ("unofficial-community", "Duolingo", "Unofficial access to Duolingo streaks, XP and leagues.", "No", "https://github.com/mikimisbr/duolingo-api-docs"),
    ("cryptocurrency", "Messari", "Crypto asset profiles, metrics and market data.", "\U0001f511 ApiKey", "https://messari.io/api/docs"),
    ("development", "Crates.io", "Rust crate metadata, versions and download counts.", "No", "https://crates.io/data-access"),
    ("weather", "Pirate Weather", "Open-source friendly Dark Sky-compatible forecast API.", "\U0001f511 ApiKey", "https://pirateweather.net/"),
    ("weather", "AerisWeather", "Global weather forecasts, history and alerts.", "\U0001f511 ApiKey", "https://developers.aerisweather.com/"),
    ("government-civic", "Regulations.gov", "U.S. federal agency rulemaking dockets and comments.", "\U0001f511 ApiKey", "https://api.data.gov/services/regulations.gov"),
    ("science", "PubMed E-utilities", "U.S. National Library of Medicine biomedical literature.", "No", "https://www.ncbi.nlm.nih.gov/books/NBK25501/"),
    ("continuous-integration", "Coveralls", "Pull coverage data from CI builds.", "\U0001f511 ApiKey", "https://docs.coveralls.io/"),
    ("cloud-storage-files", "pCloud", "Cloud storage with file, folder and sharing APIs.", "\U0001f511 ApiKey", "https://docs.pcloud.com/"),
    ("geography-countries", "Countries Now", "Countries with population, cities, flags and coordinates.", "No", "https://harmansingh2002.github.io/CountriesNow-API/"),
    ("text-analysis-nlp", "MeaningCloud", "Text analysis for sentiment, topics and classification.", "\U0001f511 ApiKey", "https://www.meaningcloud.com/"),
]

names, urls = set(), set()
for f in APIS.glob("*.md"):
    for line in f.read_text(encoding="utf-8").splitlines():
        if line.startswith("| **"):
            m = ROW_RE.match(line)
            if m:
                names.add(m.group(1).strip().lower())
            for u in re.findall(r"\((https?://[^)]+)\)", line):
                urls.add(norm_url(u))

per_file = {}
for slug, name, desc, auth, url in RETRIES:
    if name.lower() in names or norm_url(url) in urls:
        print(f"  skip dup: {name}")
        continue
    print(f"  retry: {name} -> {url}", flush=True)
    if not url_alive(url):
        print(f"  STILL DEAD: {name}")
        continue
    names.add(name.lower())
    urls.add(norm_url(url))
    per_file.setdefault(APIS / f"{slug}.md", []).append(
        f"| **{name}** | {desc} | {auth} | ✅ | [Link]({url}) |"
    )

for fpath, rows in per_file.items():
    lines = fpath.read_text(encoding="utf-8").splitlines()
    head = [l for l in lines if l.startswith("| **")]
    others_before = lines[: lines.index(head[0])]
    last_row_idx = len(lines) - 1 - lines[::-1].index(head[-1])
    tail = lines[last_row_idx + 1:]
    new_rows = sorted(head + rows, key=lambda l: ROW_RE.match(l).group(1).lower())
    fpath.write_text("\n".join(others_before + new_rows + tail) + "\n", encoding="utf-8")
    print(f"  updated {fpath.name}: +{len(rows)} -> {len(new_rows)} rows")

print(f"RETRY ADDED={sum(len(v) for v in per_file.values())}")
