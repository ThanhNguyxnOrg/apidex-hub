# -*- coding: utf-8 -*-
"""Wave-6 (2026-10-17): additions verified live via HTTP (200/308, 403=protected). None duplicate by URL or name."""
import re
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from add_wave2 import norm_url, APIS, ROW_RE

ADDITIONS = [
    ("tracking-logistics", "EasyPost", "Shipping rates, labels and tracking across major carriers.", "🔑 ApiKey", "https://docs.easypost.com/"),
    ("business", "Klaviyo", "Email and SMS marketing automation data API.", "🔑 ApiKey", "https://developers.klaviyo.com/"),
    ("business", "Zendesk", "Support tickets, users and macros for customer service teams.", "🔑 ApiKey", "https://developer.zendesk.com/"),
    ("business", "Pipedrive", "Sales CRM with deals, contacts and activity management.", "🔑 ApiKey", "https://developers.pipedrive.com/"),
    ("business", "Front App", "Shared inbox, chat and SMS conversations API for support teams.", "🔑 ApiKey", "https://developers.frontapp.com/"),
    ("dictionaries", "Free Dictionary", "Open REST dictionary with definitions and word lookups.", "No", "https://dictionaryapi.dev/"),
    ("development", "Koyeb", "Serverless container and deployment platform API.", "🔑 ApiKey", "https://www.koyeb.com/docs/api"),
    ("anti-malware", "AlienVault OTX", "Open threat intelligence feeds, indicators and pulses.", "🔑 ApiKey", "https://otx.alienvault.com/"),
    ("development", "App Store Connect", "Apple developer platform: builds, TestFlight, reviews and sales.", "🔑 ApiKey", "https://developer.apple.com/app-store-connect/api/"),
    ("development", "Google Play Developer", "Android publishing, in-app products and crash reporting.", "🔑 ApiKey", "https://developers.google.com/android-publisher"),
    ("science", "Figshare", "Open research outputs, datasets and institutional repository data.", "🔑 ApiKey", "https://docs.figshare.com/"),
    ("science", "Zenodo", "CERN open repository for research datasets with DOIs.", "🔑 ApiKey", "https://developers.zenodo.org/"),
    ("podcasts", "Podcast Index", "Open podcast index with feeds, episodes, and value-for-value data.", "🔑 ApiKey", "https://podcastindex.org/"),
]

ROW_TMPL = "| **{name}** | {desc} | {auth} | ✅ | [Link]({url}) |"


def read(fpath):
    return fpath.read_text(encoding="utf-8").splitlines()


def insert_rows(fpath, rows):
    lines = read(fpath)
    first = next(i for i, l in enumerate(lines) if l.startswith("| **"))
    last = len(lines) - 1 - lines[::-1].index(next(l for l in reversed(lines) if l.startswith("| **")))
    before = lines[:first]
    tail = lines[last + 1:]
    new = sorted([l for l in lines[first:last + 1]] + rows,
                 key=lambda l: ROW_RE.match(l).group(1).lower())
    fpath.write_text("\n".join(before + new + tail) + "\n", encoding="utf-8")
    return len(new)


def main():
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
        n = insert_rows(fpath, rows)
        print(f"  added to {fpath.stem}: +{len(rows)} -> {n}")
    print(f"ADDED={added} SKIPPED={skipped}")


if __name__ == "__main__":
    main()
