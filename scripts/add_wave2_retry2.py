# -*- coding: utf-8 -*-
"""Wave-2 retry #2: URLs verified alive via PowerShell GET (python SSL/DNS quirks were false negatives)."""
import sys
sys.path.insert(0, "scripts")
from add_wave2 import norm_url, APIS, ROW_RE
import re

RETRIES = [
    ("news", "BBC", "BBC News content and programme metadata.", "\U0001f511 ApiKey", "https://www.bbc.co.uk/developer"),
    ("demographic-analysis", "Population (API Ninjas)", "Population data by country with historical records.", "\U0001f511 ApiKey", "https://api-ninjas.com/api/population"),
    ("development", "Crates.io", "Rust crate metadata, versions and download counts.", "No", "https://doc.rust-lang.org/cargo/reference/registry-web-api.html"),
    ("geography-countries", "Countries Now", "Countries with population, cities, flags and coordinates.", "No", "https://countriesnow.space/"),
    ("government-civic", "Regulations.gov", "U.S. federal agency rulemaking dockets and comments.", "\U0001f511 ApiKey", "https://www.regulations.gov/developers"),
    ("cryptocurrency", "Messari", "Crypto asset profiles, metrics and market data.", "\U0001f511 ApiKey", "https://messari.io/api/docs"),
    ("cloud-storage-files", "pCloud", "Cloud storage with file, folder and sharing APIs.", "\U0001f511 ApiKey", "https://docs.pcloud.com/"),
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
    names.add(name.lower())
    urls.add(norm_url(url))
    per_file.setdefault(APIS / f"{slug}.md", []).append(
        f"| **{name}** | {desc} | {auth} | ✅ | [Link]({url}) |"
    )
    print(f"  add: {name}")

for fpath, rows in per_file.items():
    lines = fpath.read_text(encoding="utf-8").splitlines()
    head = [l for l in lines if l.startswith("| **")]
    others_before = lines[: lines.index(head[0])]
    last_row_idx = len(lines) - 1 - lines[::-1].index(head[-1])
    tail = lines[last_row_idx + 1:]
    new_rows = sorted(head + rows, key=lambda l: ROW_RE.match(l).group(1).lower())
    fpath.write_text("\n".join(others_before + new_rows + tail) + "\n", encoding="utf-8")
    print(f"  updated {fpath.name}: +{len(rows)} -> {len(new_rows)} rows")

print(f"RETRY2 ADDED={sum(len(v) for v in per_file.values())}")
