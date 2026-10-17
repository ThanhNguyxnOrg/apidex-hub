# -*- coding: utf-8 -*-
"""Wave-11 (2026-10-17): additions verified live via HTTP (200/429-protected-alive/405-GET-retested VND below). Dedupe by URL+name at run time."""
import re
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from add_wave2 import norm_url, APIS, ROW_RE

ADDITIONS = [
    ("finance", "EODHD", "End-of-day and intraday stock market data across 60+ exchanges.", "🔑 ApiKey", "https://eodhd.com/"),
    ("finance", "OpenFIGI", "Free mapping between FIGI identifiers and financial instruments.", "🔑 ApiKey", "https://www.openfigi.com/"),
    ("development", "Storyblok", "Headless CMS REST and GraphQL APIs.", "🔑 ApiKey", "https://www.storyblok.com/docs/api"),
    ("development", "Strapi", "Headless CMS: REST/GraphQL endpoints for any Strapi project.", "🔑 ApiKey", "https://docs.strapi.io/"),
    ("development", "Contentful", "Headless content platform APIs.", "🔑 ApiKey", "https://www.contentful.com/developers/docs/"),
    ("development", "Ghost Content API", "Public content endpoints for Ghost publications.", "🔑 ApiKey", "https://ghost.org/docs/content-api/"),
    ("security-validation", "CIRCL CVE", "Community CVE/MKE vulnerability search with CVSS and CPE data.", "No", "https://cve.circl.lu/"),
    ("security-validation", "MalwareBazaar", "Abuse.ch malware samples repository and API.", "No", "https://bazaar.abuse.ch/browse/"),
    ("security-validation", "ThreatFox", "Abuse.ch threat-indicator sharing platform (IOCs).", "No", "https://threatfox.abuse.ch/"),
    ("security-validation", "URLScan", "URL sandboxing with page screenshots, scans and results.", "🔑 ApiKey", "https://urlscan.io/"),
    ("public-data", "Wayback Machine", "Internet Archive snapshots and CDX index API.", "No", "https://web.archive.org/"),
    ("geocoding", "Open-Elevation", "Free world-wide open elevation (height) lookups.", "No", "https://www.open-elevation.com/"),
    ("geocoding", "LocationIQ", "Geocoding/reverse geocoding plus maps APIs.", "🔑 ApiKey", "https://locationiq.com/"),
    ("cryptocurrency", "CoinCap", "Real-time crypto market data via REST & WebSocket.", "No", "https://coincap.io/"),
    ("cryptocurrency", "Blockchain.com Data", "Bitcoin blockchain data: blocks, addresses, transactions.", "🔑 ApiKey", "https://www.blockchain.com/explorer/api"),
    ("jobs-career", "Himalayas", "Open remote-jobs search API with company filters.", "No", "https://himalayas.app/jobs/api"),
    ("utilities-tools", "TimeAPI", "Time zone lookups, conversions and daylight-saving data.", "No", "https://timeapi.io/"),
    ("email-sms", "Mailgun", "Transactional email API with validation and routes.", "🔑 ApiKey", "https://www.mailgun.com/"),
    ("email-sms", "SendGrid", "Email delivery API, templates and webhooks (Twilio).", "🔑 ApiKey", "https://sendgrid.com/"),
    ("payments-billing", "Adyen", "Payments platform API for online and in-person checkout.", "🔑 ApiKey", "https://docs.adyen.com/"),
    ("games-comics", "Riot Games", "League of Legends, Valorant and TFT developer APIs.", "🔑 ApiKey", "https://developer.riotgames.com/"),
    ("health", "RxNav", "NLM drug normalization: RXCUI, NDC interactions and names.", "No", "https://lhncbc.nlm.nih.gov/RxNav/APIs/"),
    ("government-civic", "USAspending", "US federal spending data: awards, recipients and contracts.", "No", "https://www.usaspending.gov/"),
    ("government-civic", "OpenFEC", "Federal Election Commission filings and candidates data.", "🔑 ApiKey", "https://api.open.fec.gov/developers/"),
    ("text-analysis-nlp", "TextRazor", "Entity extraction, tagging and relation NLP API.", "🔑 ApiKey", "https://www.textrazor.com/"),
    ("machine-learning", "Weights & Biases", "Experiment tracking REST API for ML projects.", "🔑 ApiKey", "https://docs.wandb.ai/"),
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
