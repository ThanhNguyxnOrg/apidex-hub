# -*- coding: utf-8 -*-
"""Wave-2 catalog additions (2026-10-17): verified non-Apify APIs into existing categories.

- Verifies every candidate doc URL is alive (2xx/3xx or 401/403=protected-ok) before adding.
- Skips anything whose Name OR URL already exists anywhere in apis/.
- Inserts rows alphabetically into the target file.
"""
import re
import ssl
import sys
import urllib.request
from pathlib import Path

APIS = Path("apis")

CANDIDATES = [
    # (category-slug, name, description, auth, url)
    ("payments-billing", "dLocal", "Cross-border payment processing for emerging markets.", "\U0001f511 ApiKey", "https://docs.dlocal.com/"),
    ("payments-billing", "Flutterwave", "Pan-African payments infrastructure for cards, banks and mobile money.", "\U0001f511 ApiKey", "https://developer.flutterwave.com/"),
    ("payments-billing", "MoMo", "Vietnam Mobile Money and e-wallet payment API.", "\U0001f511 ApiKey", "https://developers.momo.vn/"),
    ("travel-tourism", "Duffel", "Modern flight and travel booking API.", "\U0001f511 ApiKey", "https://docs.duffel.com/"),
    ("travel-tourism", "Budget Your Trip", "Travel cost estimates by country and city.", "No", "https://www.budgetyourtrip.com/api"),
    ("travel-tourism", "Lufthansa", "Flight status, airport and schedules API.", "\U0001f511 ApiKey", "https://developer.lufthansa.com/"),
    ("travel-tourism", "Hotelbeds", "Global hotel inventory and booking API.", "\U0001f511 ApiKey", "https://developer.hotelbeds.com/"),
    ("math-computation", "Wolfram Cloud", "Compute with the full Mathematica language in the cloud.", "\U0001f511 ApiKey", "https://reference.wolframcloud.com/"),
    ("math-computation", "Mathpix", "OCR math, formulas and documents to LaTeX/Markdown.", "\U0001f511 ApiKey", "https://mathpix.com/docs/"),
    ("news", "BBC", "BBC News content and programme metadata.", "\U0001f511 ApiKey", "https://www.bbc.co.uk/developer"),
    ("news", "Feedly", "Read and organize feeds, streams and topics.", "\U0001f511 ApiKey", "https://feedly.com/i/developer"),
    ("news", "Webz.io", "Datasets of news and web articles with natural language filters.", "\U0001f511 ApiKey", "https://webz.io/"),
    ("business", "PeopleDataLabs", "Person and company data enrichment for B2B.", "\U0001f511 ApiKey", "https://www.peopledatalabs.com/"),
    ("business", "Xero", "Accounting, invoicing and banking data API.", "\U0001f51e OAuth", "https://developer.xero.com/documentation/api/accounting/overview"),
    ("business", "QuickBooks", "Intuit QuickBooks online accounting and finance API.", "\U0001f51e OAuth", "https://developer.intuit.com/app/developer/qbo/docs/api"),
    ("business", "BambooHR", "HR information system with employees, time off and reports.", "\U0001f511 ApiKey", "https://documentation.bamboohr.com/"),
    ("business", "EU VIES", "Check EU VAT registration numbers across member states.", "No", "https://ec.europa.eu/taxation_customs/vies/"),
    ("web-scraping-crawling", "Browserless", "Headless Chrome as a service for scraping and automation.", "\U0001f511 ApiKey", "https://docs.browserless.io/"),
    ("web-scraping-crawling", "Bright Data", "Proxy networks and ready-made datasets for web data.", "\U0001f511 ApiKey", "https://docs.brightdata.com/"),
    ("web-scraping-crawling", "Zyte", "Web scraping API with smart routing and anti-blocking.", "\U0001f511 ApiKey", "https://docs.zyte.com/"),
    ("web-scraping-crawling", "Diffbot", "Automatic extraction of entities and articles from any page.", "\U0001f511 ApiKey", "https://docs.diffbot.com/"),
    ("web-scraping-crawling", "ScrapingFish", "Headless browser rendering and rotating proxies for scraping.", "\U0001f511 ApiKey", "https://www.scrapingfish.com/docs"),
    ("backend-database", "MongoDB Atlas", "Data API for MongoDB Atlas clusters.", "\U0001f511 ApiKey", "https://www.mongodb.com/docs/atlas/api/"),
    ("backend-database", "NocoDB", "Turn any database into a smart spreadsheet with API.", "\U0001f511 ApiKey", "https://docs.nocodb.com/"),
    ("backend-database", "Baserow", "Open-source no-code database with REST API.", "\U0001f511 ApiKey", "https://baserow.io/docs"),
    ("backend-database", "Xata", "Serverless PostgreSQL-ready database with search built in.", "\U0001f511 ApiKey", "https://docs.xata.io/"),
    ("iot-smart-devices", "SmartThings", "Samsung SmartThings connected device control API.", "\U0001f511 ApiKey", "https://developer.smartthings.com/docs/api/public"),
    ("iot-smart-devices", "ESP RainMaker", "Espressif ESP32 device cloud with app and voice control.", "\U0001f511 ApiKey", "https://rainmaker.espressif.com/"),
    ("podcasts", "Apple Search", "Search podcasts, episodes, authors and countries.", "No", "https://performance-partners.apple.com/search-api"),
    ("podcasts", "Audiosearch", "Podcast discovery, transcripts and episode metadata.", "\U0001f511 ApiKey", "https://audiosearch.com/"),
    ("demographic-analysis", "Statistics Canada", "Canadian census, demographic and economic statistics.", "No", "https://www.statcan.gc.ca/eng/developers"),
    ("demographic-analysis", "Population (API Ninjas)", "Population data by country with historical records.", "\U0001f511 ApiKey", "https://api.ninjas.com/api/population"),
    ("date-time", "Abstract Time Zone", "Time zone, current time and date conversion API.", "\U0001f511 ApiKey", "https://www.abstractapi.com/api/time-zone-api"),
    ("date-time", "caldays", "Calendar days and date utilities over REST.", "No", "https://caldays.com/api"),
    ("qr-barcode", "TEC-IT", "Generate QR codes and barcodes in many formats.", "No", "https://www.tec-it.com/en/software/online-components/barcode-generator-api/overview"),
    ("qr-barcode", "QR Code (API Ninjas)", "Generate QR codes from text or URLs.", "\U0001f511 ApiKey", "https://api-ninjas.com/api/qrcode"),
    ("shopping", "eBay", "Marketplace listing, inventory and order management.", "\U0001f51e OAuth", "https://developer.ebay.com/"),
    ("shopping", "Walmart", "Marketplace items, inventory, orders and pricing.", "\U0001f511 ApiKey", "https://developer.walmart.com/"),
    ("shopping", "Target", "Roundel retail partner API for items and inventory.", "\U0001f511 ApiKey", "https://developers.target.com/"),
    ("shopping", "Rakuten", "Japanese marketplace items, search and ranking API.", "\U0001f511 ApiKey", "https://webservice.rakuten.co.jp/"),
    ("unofficial-community", "Duolingo", "Unofficial access to Duolingo streaks, XP and leagues.", "\U0001f511 ApiKey", "https://github.com/dyuk198/duolingo-api"),
    ("health", "WHO Global Health Observatory", "World Health Organization health indicator datasets.", "No", "https://www.who.int/data/gho/info/gho-odata-api"),
    ("cryptocurrency", "Messari", "Crypto asset profiles, metrics and market data.", "\U0001f511 ApiKey", "https://messari.io/api/docs"),
    ("cryptocurrency", "Mempool.space", "Bitcoin mempool, fees, blocks and Lightning network data.", "No", "https://mempool.space/docs/api"),
    ("finance", "SEC EDGAR", "U.S. public company filings, facts and financial statements.", "No", "https://www.sec.gov/edgar/sec-api-documentation"),
    ("development", "npm", "Package metadata, downloads and maintainers from the npm registry.", "No", "https://docs.npmjs.com/"),
    ("development", "PyPI", "JSON API for Python package metadata and releases.", "No", "https://warehouse.pypa.io/api-reference/"),
    ("development", "Crates.io", "Rust crate metadata, versions and download counts.", "No", "https://crates.io/data-access"),
    ("development", "Cloudflare", "DNS, zones, workers, analytics and security APIs.", "\U0001f511 ApiKey", "https://developers.cloudflare.com/api/"),
    ("phone-telephony", "Vonage", "SMS, voice, video and verification APIs.", "\U0001f511 ApiKey", "https://developer.vonage.com/"),
    ("security-validation", "Cloudflare DoH", "DNS-over-HTTPS JSON resolver on 1.1.1.1.", "No", "https://developers.cloudflare.com/1.1.1.1/encryption/dns-over-https/make-api-requests/dns-json/"),
    ("security-validation", "ICANN RDAP", "Registration Data Access Protocol for domains and IPs.", "No", "https://www.icann.org/rdap"),
    ("weather", "Open-Meteo", "Free non-commercial weather forecast API without API keys.", "No", "https://open-meteo.com/en/docs"),
    ("weather", "Pirate Weather", "Open-source friendly Dark Sky-compatible forecast API.", "\U0001f511 ApiKey", "https://pirateweather.net/en/latest/"),
    ("weather", "AerisWeather", "Global weather forecasts, history and alerts.", "\U0001f511 ApiKey", "https://developers.aerisweather.com/"),
    ("transportation", "NHTSA Recalls", "U.S. vehicle recall database by make, model and year.", "No", "https://api.nhtsa.gov/recalls"),
    ("government-civic", "EU Open Data Portal", "Search and access datasets published by EU institutions.", "No", "https://data.europa.eu/api/hub/search/"),
    ("government-civic", "Regulations.gov", "U.S. federal agency rulemaking dockets and comments.", "\U0001f511 ApiKey", "https://api.data.gov/services/regulations.gov"),
    ("tracking-logistics", "Ship24", "Universal parcel and shipment tracking across carriers.", "\U0001f511 ApiKey", "https://www.ship24.com/tracking-api"),
    ("books", "Poetry DB", "Database of poetry with poems, poets and lines.", "No", "https://poetrydb.org/index"),
    ("science", "DOAJ", "Directory of open access journals and articles.", "No", "https://doaj.org/api/docs"),
    ("science", "PubMed", "U.S. National Library of Medicine biomedical literature.", "No", "https://pubmed.ncbi.nlm.nih.gov/tools/"),
    ("environment-climate", "CO2 Signal", "Real-time carbon intensity of electricity by region.", "\U0001f511 ApiKey", "https://co2signal.com/"),
    ("environment-climate", "Electricity Maps", "Live carbon intensity and electricity source mix.", "\U0001f511 ApiKey", "https://static.electricitymaps.com/api/docs/index.html"),
    ("environment-climate", "WattTime", "Real-time and forecast marginal emissions data.", "\U0001f511 ApiKey", "https://www.watttime.org/api-documentation/"),
    ("food-drink", "Edamam", "Nutrition analysis, recipes and diet classification.", "\U0001f511 ApiKey", "https://developer.edamam.com/"),
    ("machine-learning", "Hugging Face Inference", "Serverless inference for thousands of open models.", "\U0001f511 ApiKey", "https://huggingface.co/docs/api/index"),
    ("jobs-career", "Remotive", "Remote job listings with full-text search.", "No", "https://remotive.com/api/remote-jobs"),
    ("blockchain-web3", "Covalent", "Unified blockchain data across 50+ networks.", "\U0001f511 ApiKey", "https://www.covalenthq.com/docs/"),
    ("blockchain-web3", "Blockchair", "Blockchain explorers and analytics for Bitcoin, Ethereum and more.", "\U0001f511 ApiKey", "https://blockchair.com/api"),
    ("open-source-projects", "ClearlyDefined", "Curated metadata and license scores for open-source components.", "No", "https://docs.clearlydefined.io/"),
    ("open-source-projects", "Libraries.io", "Dependency and package metadata for 40+ registries.", "\U0001f511 ApiKey", "https://libraries.io/api"),
    ("continuous-integration", "Codecov", "Upload and query code coverage reports.", "\U0001f511 ApiKey", "https://docs.codecov.com/docs"),
    ("continuous-integration", "Coveralls", "Pull coverage data from CI builds.", "\U0001f511 ApiKey", "https://docs.coveralls.io/api-overview"),
    ("cloud-storage-files", "pCloud", "Cloud storage with file, folder and sharing APIs.", "\U0001f511 ApiKey", "https://docs.pcloud.com/"),
    ("cloud-storage-files", "Internxt", "Privacy-focused cloud storage API.", "\U0001f511 ApiKey", "https://internxt.com/developers"),
    ("cloud-storage-files", "MEGA", "Cloud storage with end-to-end encryption.", "\U0001f511 ApiKey", "https://mega.io/developers"),
    ("email-sms", "ClickSend", "SMS, MMS, email, voice and fax messaging API.", "\U0001f511 ApiKey", "https://developers.clicksend.com/"),
    ("monitoring-observability", "Better Stack", "Uptime monitoring, incidents and on-call schedules.", "\U0001f511 ApiKey", "https://betterstack.com/docs/"),
    ("memes-fun", "Kanye Rest", "Random Kanye West quotes.", "No", "https://kanye.rest/"),
    ("geography-countries", "Countries Now", "Countries with population, cities, flags and coordinates.", "No", "https://harmansingh2002.github.io/CountriesNow-API/"),
    ("text-analysis-nlp", "MeaningCloud", "Text analysis for sentiment, topics and classification.", "\U0001f511 ApiKey", "https://www.meaningcloud.com/"),
    ("url-shorteners", "1pt", "Minimal URL shortener with analytics.", "No", "https://github.com/1pt-co/api/blob/main/README.md"),
]

ROW_RE = re.compile(r"^\| \*\*(.+?)\*\*")


def norm_url(u: str) -> str:
    return u.rstrip("/").lower().replace("https://", "http://")


def url_alive(url: str) -> bool:
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (apidex-hub-linkcheck)"})
    try:
        with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
            return r.status < 400
    except urllib.error.HTTPError as e:
        return e.code in (401, 403, 405)  # protected but alive
    except Exception as e:
        print(f"    !! fetch error {e!r}")
        return False


def main():
    # existing index
    names, urls = set(), set()
    for f in APIS.glob("*.md"):
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.startswith("| **"):
                m = ROW_RE.match(line)
                if m:
                    names.add(m.group(1).strip().lower())
                for u in re.findall(r"\((https?://[^)]+)\)", line):
                    urls.add(norm_url(u))

    added, skipped_dup, dead = 0, 0, 0
    per_file = {}
    for slug, name, desc, auth, url in CANDIDATES:
        fpath = APIS / f"{slug}.md"
        if not fpath.exists():
            print(f"  !! missing file {slug}")
            sys.exit(1)
        if name.lower() in names or norm_url(url) in urls:
            skipped_dup += 1
            print(f"  skip dup: {name}")
            continue
        print(f"  check: {name} -> {url}", flush=True)
        if not url_alive(url):
            dead += 1
            print(f"  DEAD: {name} {url}")
            continue
        names.add(name.lower())
        urls.add(norm_url(url))
        per_file.setdefault(fpath, []).append(
            f"| **{name}** | {desc} | {auth} | ✅ | [Link]({url}) |"
        )
        added += 1

    for fpath, rows in per_file.items():
        lines = fpath.read_text(encoding="utf-8").splitlines()
        head = [l for l in lines if l.startswith("| **")]
        others_before = [l for l in lines[: lines.index(head[0])]]
        # rebuild: everything before first row, then sorted rows, then tail after last row
        last_row_idx = len(lines) - 1 - lines[::-1].index(head[-1])
        tail = lines[last_row_idx + 1:]
        new_rows = sorted(head + rows, key=lambda l: ROW_RE.match(l).group(1).lower())
        fpath.write_text("\n".join(others_before + new_rows + tail) + "\n", encoding="utf-8")
        print(f"  updated {fpath.name}: +{len(rows)} -> {len(new_rows)} rows")

    print(f"\nADDED={added} SKIP_DUP={skipped_dup} DEAD={dead}")


if __name__ == "__main__":
    main()
