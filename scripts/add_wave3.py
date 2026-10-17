# -*- coding: utf-8 -*-
"""Wave-3 (2026-10-17): 5 new categories + additions to existing ones. All URLs verified via HTTP HEAD before this run."""
import re
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from add_wave2 import norm_url, APIS, ROW_RE

NEW_CATEGORIES = [
    # (slug, emoji, title, [rows])
    ("patents", "\U0001f4dc", "Patents & Prior Art", [
        ("EPO Open Patent Services", "European Patent Office search, family and legal status data.", "\U0001f51e OAuth", "https://developers.epo.org/"),
        ("Google Patents Public Data", "BigQuery dataset of worldwide patent publications.", "\U0001f51e OAuth", "https://cloud.google.com/bigquery/public-data"),
        ("PatentsView", "Searchable U.S. patent data with inventor and assignee analytics.", "No", "https://patentsview.org/apis/purpose"),
        ("The Lens", "Scholarly works and patent search with global coverage.", "\U0001f51e OAuth", "https://about.lens.org/lens-api/"),
        ("USPTO Open Data Portal", "U.S. patent and trademark datasets and API catalog.", "No", "https://developer.uspto.gov/api-catalog"),
    ]),
    ("vehicle", "\U0001f697", "Vehicle & Mobility", [
        ("CarVector", "Vehicle images rendered by make, model and year.", "\U0001f511 ApiKey", "https://carvector.io/docs"),
        ("Edmunds", "Vehicle specifications, reviews and True Market Value pricing.", "\U0001f511 ApiKey", "https://www.edmunds.com/developer/"),
        ("FIPE", "Brazilian vehicle reference prices by make and model.", "No", "https://deividfortuna.github.io/fipe/"),
        ("Fuelly", "Fuel economy and maintenance tracking for vehicles.", "\U0001f511 ApiKey", "https://www.fuelly.com/apidoc"),
        ("Mercedes-Benz", "Vehicle status, telemetry and digital key APIs.", "\U0001f51e OAuth", "https://developer.mercedes-benz.com/apis"),
        ("WhichTrim", "Vehicle trim and option decoding by VIN.", "\U0001f511 ApiKey", "https://whichtrim.com/developers/"),
    ]),
    ("fitness-wellness", "\U0001f4aa", "Fitness & Wellness", [
        ("FatSecret", "Nutrition database and food lookup with OAuth access.", "\U0001f51e OAuth", "https://platform.fatsecret.com/docs"),
        ("MapMyFitness", "Under Armour workout, route and activity tracking.", "\U0001f51e OAuth", "https://developer.mapmyfitness.com/"),
        ("MyFitnessPal", "Nutrition diary and food database integration.", "\U0001f511 ApiKey", "https://www.myfitnesspal.com/developer"),
        ("Polar OpenFlow", "Heart rate, training load and workout data from Polar devices.", "\U0001f51e OAuth", "https://www.polar.com/en/openflow"),
        ("WHOOP", "Strain, sleep and recovery physiology data.", "\U0001f51e OAuth", "https://developer.whoop.com/"),
        ("Withings", "Body scale, sleep sensor and activity tracker health data.", "\U0001f51e OAuth", "https://developer.withings.com/"),
    ]),
    ("reviews", "⭐", "Reviews & Ratings", [
        ("Amazon PA-API", "Product reviews, ratings and offers from the Amazon catalogue.", "\U0001f511 ApiKey", "https://webservices.amazon.com/paapi5/documentation/"),
        ("Bazaarvoice", " syndicated consumer ratings and reviews for retailers and brands.".strip(), "\U0001f511 ApiKey", "https://developer.bazaarvoice.com/"),
        ("PowerReviews", "Ratings, reviews and questions for products and services.", "\U0001f511 ApiKey", "https://developers.powerreviews.com/"),
        ("Reviews.io", "First-party business reviews with photo and Q&A support.", "\U0001f511 ApiKey", "https://developer.reviews.io/"),
        ("Sitejabber", "Customer reviews and business reputation data.", "\U0001f511 ApiKey", "https://api.sitejabber.com/v1/"),
        ("Trustpilot", "Business reviews, ratings and consumer trust data.", "\U0001f511 ApiKey", "https://developers.trustpilot.com/"),
    ]),
    ("networking-dns", "\U0001f310", "Networking, DNS & WHOIS", [
        ("Abstract IP Geolocation", "IP address geolocation, ASN and proxy detection.", "\U0001f511 ApiKey", "https://www.abstractapi.com/api/ip-geolocation-api"),
        ("DNSlytics", "DNS, IP and reverse IP lookups across the internet.", "\U0001f511 ApiKey", "https://dnslytics.com/api"),
        ("IP2Location", "IP to geolocation, ISP and proxy detection database.", "\U0001f511 ApiKey", "https://www.ip2location.com/web-service/ip2location"),
        ("IPinfo", "IP geolocation, ASN, company and privacy data.", "\U0001f511 ApiKey", "https://ipinfo.io/developers"),
        ("ipgeolocation", "Accurate geolocation with time zone and currency data.", "\U0001f511 ApiKey", "https://ipgeolocation.io/documentation.html"),
        ("WhoisXML API", "WHOIS and DNS data for any domain or IP address.", "\U0001f511 ApiKey", "https://whoisxmlapi.com/"),
    ]),
]

ADDITIONS = [
    ("text-analysis-nlp", "Amazon Translate", "Neural machine translation service.", "\U0001f51e OAuth", "https://docs.aws.amazon.com/translate/"),
    ("text-analysis-nlp", "Google Cloud Translation", "Google's machine translation API (v2 and v3).", "\U0001f511 ApiKey", "https://cloud.google.com/translate/docs/reference/rest"),
    ("text-analysis-nlp", "Microsoft Translator", "Text translation with transliteration and detection.", "\U0001f511 ApiKey", "https://learn.microsoft.com/en-us/azure/ai-services/translator/"),
    ("text-analysis-nlp", "ModernMT", "Adaptive machine translation that learns from edits.", "\U0001f511 ApiKey", "https://www.modernmt.com/api/"),
    ("text-analysis-nlp", "MyMemory", "Free translation memory API with public corpora.", "No", "https://api.mymemory.translated.net/"),
    ("data-validation", "Abstract Email Verification", "Email validation, scoring and deliverability checks.", "\U0001f511 ApiKey", "https://www.abstractapi.com/api/email-verification-validation-api"),
    ("data-validation", "Kickbox", "Email verification and deliverability testing.", "\U0001f511 ApiKey", "https://docs.kickbox.com/"),
    ("data-validation", "NeverBounce", "Real-time email verification and list cleaning.", "\U0001f511 ApiKey", "https://developers.neverbounce.com/"),
    ("data-validation", "Validator.pizza", "Free single and bulk email validation.", "No", "https://validator.pizza/"),
    ("news", "GNews", "News search API with topic and location filters.", "\U0001f511 ApiKey", "https://gnews.io/"),
    ("news", "NewsData", "News aggregation across 80k+ sources in 80+ languages.", "\U0001f511 ApiKey", "https://newsdata.io/"),
    ("news", "Spaceflight News API", "Articles and updates about spaceflight and astronomy.", "No", "https://api.spaceflightnewsapi.net/v4/docs/"),
    ("payments-billing", "GoCardless", "Direct debit and recurring bank payments.", "\U0001f51e OAuth", "https://developer.gocardless.com/"),
    ("payments-billing", "Lemon Squeezy", "Merchant of record with billing, taxes and licenses.", "\U0001f51e OAuth", "https://docs.lemonsqueezy.com/"),
    ("payments-billing", "Mastercard", "Payments, accounts and pricing APIs for Mastercard.", "\U0001f51e OAuth", "https://developer.mastercard.com/"),
    ("payments-billing", "Payoneer", "Cross-border payouts and receivables for marketplaces.", "\U0001f511 ApiKey", "https://developer.payoneer.com/"),
    ("payments-billing", "Paystack", "Online payments for Nigerian and African businesses.", "\U0001f511 ApiKey", "https://paystack.com/docs/"),
    ("payments-billing", "Plaid", "Bank account linking, balances and transactions.", "\U0001f51e OAuth", "https://plaid.com/docs/"),
    ("payments-billing", "Razorpay", "Indian payments, subscriptions and payouts.", "\U0001f511 ApiKey", "https://razorpay.com/docs/"),
    ("iot-smart-devices", "ThingSpeak", "IoT analytics platform for device data channels.", "\U0001f511 ApiKey", "https://api.thingspeak.com/"),
    ("travel-tourism", "Rome2rio", "Multi-modal transport routes between any two places.", "\U0001f511 ApiKey", "https://www.rome2rio.com/documentation"),
    ("museums-art", "National Gallery of Art", "Open data on the NGA art collection and exhibitions.", "No", "https://github.com/NationalGalleryOfArt/opendata"),
    ("museums-art", "Tate", "Collection API for Tate galleries in the UK.", "No", "https://github.com/tategallery/collection"),
    ("finance", "Tiingo", "Stock, ETF and index time series with fundamentals.", "\U0001f511 ApiKey", "https://www.tiingo.com/"),
]

ROW_TMPL = "| **{name}** | {desc} | {auth} | ✅ | [Link]({url}) |"


def insert_rows(fpath: Path, rows):
    lines = fpath.read_text(encoding="utf-8").splitlines()
    head = [l for l in lines if l.startswith("| **")]
    if not head:
        raise RuntimeError(f"no table rows in {fpath}")
    before = lines[: lines.index(head[0])]
    last = len(lines) - 1 - lines[::-1].index(head[-1])
    tail = lines[last + 1:]
    new_rows = sorted(head + rows, key=lambda l: ROW_RE.match(l).group(1).lower())
    fpath.write_text("\n".join(before + new_rows + tail) + "\n", encoding="utf-8")
    return len(new_rows)


def main():
    names, urls = set(), set()
    for f in APIS.glob("*.md"):
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.startswith("| **"):
                m = ROW_RE.match(line)
                if m:
                    names.add(m.group(1).strip().lower())
                for u in re.findall(r"\((https?://[^)]+)\)", line):
                    urls.add(norm_url(u))

    added = skipped = 0
    per_file = {}
    for slug, name, desc, auth, url in ADDITIONS:
        if name.lower() in names or norm_url(url) in urls:
            skipped += 1
            print(f"  skip dup: {name}")
            continue
        names.add(name.lower())
        urls.add(norm_url(url))
        per_file.setdefault(APIS / f"{slug}.md", []).append(ROW_TMPL.format(name=name, desc=desc, auth=auth, url=url))
        added += 1

    for slug, emoji, title, entries in NEW_CATEGORIES:
        fpath = APIS / f"{slug}.md"
        if fpath.exists():
            print(f"  !! {slug} already exists, skipping create")
            continue
        rows = []
        for name, desc, auth, url in entries:
            if name.lower() in names or norm_url(url) in urls:
                print(f"  skip dup in new cat: {name}")
                continue
            names.add(name.lower())
            urls.add(norm_url(url))
            rows.append(ROW_TMPL.format(name=name, desc=desc, auth=auth, url=url))
            added += 1
        content = (
            f'## <a id="{slug}"></a>{emoji} {title}\n\n'
            "| API Name | Description | Auth | HTTPS | Link |\n"
            "| :--- | :--- | :---: | :---: | :---: |\n"
            + "\n".join(rows) + "\n\n"
            "[⬅️ Back to Table of Contents](../README.md#table-of-contents)\n"
        )
        fpath.write_text(content, encoding="utf-8")
        print(f"  created {slug}.md with {len(rows)} rows")

    for fpath, rows in per_file.items():
        n = insert_rows(fpath, rows)
        print(f"  updated {fpath.name}: +{len(rows)} -> {n} rows")

    print(f"\nADDED={added} SKIP_DUP={skipped}")


if __name__ == "__main__":
    main()
