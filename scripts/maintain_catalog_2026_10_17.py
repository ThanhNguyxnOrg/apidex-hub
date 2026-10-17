# -*- coding: utf-8 -*-
"""
One-off catalog maintenance script (2026-10-17):
 1. Move misfiled entries to their proper categories.
 2. Populate empty/underpopulated categories with well-known public APIs.
 3. Create new categories: date-time, qr-barcode.
 4. Alphabetize every apis/*.md table.
 5. Regenerate the README catalog table (3-column grid).
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APIS = ROOT / "apis"

BACK_LINK = "[⬆ Back to Table of Contents](../README.md#table-of-contents)\n"

def read(f): return (APIS / f).read_text(encoding="utf-8")
def write(f, t): (APIS / f).write_text(t, encoding="utf-8", newline="\n")

def find_row(text, name):
    for line in text.split("\n"):
        m = re.match(r"^\|\s*\*\*(.+?)\*\*", line.strip())
        if m and m.group(1) == name:
            return line
    raise SystemExit(f"ROW NOT FOUND: {name}")

# ---------- 0. NEW CATEGORY FILES (before moves) ----------
def new_category(cid, emoji, title, rows):
    body = f'## <a id="{cid}"></a>{emoji} {title}\n\n'
    body += "| API Name | Description | Auth | HTTPS | Link |\n| :--- | :--- | :---: | :---: | :---: |\n"
    body += "\n".join(rows) + "\n\n" + BACK_LINK + "\n"
    write(cid + ".md", body)

new_category("date-time", "🕒", "Date & Time", [
    "| **Sunrise-Sunset.org** | Sunrise and sunset times for any latitude/longitude and date (**No Auth**). | No | ✅ | [Link](https://sunrise-sunset.org/api) |",
    "| **World Time API** | Current time for any IANA time zone worldwide (**No Auth**). | No | ✅ | [Link](http://worldtimeapi.org/) |",
])

new_category("qr-barcode", "🔳", "QR & Barcode", [
    "| **Barcode Lookup** | Look up product data from a barcode number, or generate barcodes. | 🔑 ApiKey | ✅ | [Link](https://www.barcodelookup.com/developers) |",
    "| **Barcode Spider** | Barcode lookup and product search API (**No Auth**). | No | ✅ | [Link](http://www.barcodespider.com/api) |",
    "| **goQR.me** | Free QR code and barcode generator/scanner returning images or SVG (**No Auth**). | No | ✅ | [Link](http://goqr.me/api/) |",
])

# ---------- 1. MOVES ----------
MOVES = [
    ("design-colors.md", "museums-art.md", ["Harvard Art Museums", "Europeana", "Cooper Hewitt"]),
    ("travel-tourism.md", "date-time.md", ["TimeZoneDB"]),
    ("calendar-holidays.md", "date-time.md", ["TimeAPI.io"]),
    ("utilities-tools.md", "qr-barcode.md", ["QR Code Generator"]),
]
for src, dst, names in MOVES:
    s = read(src)
    d = read(dst)
    for n in names:
        row = find_row(s, n)
        s = "\n".join(l for l in s.split("\n") if l != row) + "\n"
        write(src, s)
        idx = d.rindex(BACK_LINK.rstrip("\n"))
        d = d[:idx] + row + "\n\n" + d[idx:]
    write(dst, d)

# ---------- 2. (moved to section 0) ----------

# ---------- 3. APPEND WELL-KNOWN APIs ----------
ADDS = {
    "museums-art.md": [
        "| **Art Institute of Chicago** | Open access artworks, images, and metadata from one of the largest art museums in the US (**No Auth**). | No | ✅ | [Link](https://api.artic.edu/docs/) |",
        "| **Cleveland Museum of Art** | Open access API for the museum's collection of art objects (**No Auth**). | No | ✅ | [Link](https://openaccess-api.clevelandart.org/) |",
        "| **Rijksmuseum** | Collection data and high-resolution images from the Dutch national museum (**No Auth**). | No | ✅ | [Link](https://data.rijksmuseum.nl/object-metadata/api/) |",
        "| **Smithsonian Institution** | Access millions of records and images from 21 museums and research centers (**No Auth**). | No | ✅ | [Link](https://api.si.edu/) |",
    ],
    "demographic-analysis.md": [
        "| **Agify.io** | Predict age distribution from a person's name (**No Auth**). | No | ✅ | [Link](https://agify.io/) |",
        "| **DataUSA** | Open US public data on demographics, economy, and geography (**No Auth**). | No | ✅ | [Link](https://datausa.io/api/) |",
        "| **Genderize.io** | Predict gender from a person's name with locale support (**No Auth**). | No | ✅ | [Link](https://genderize.io/) |",
        "| **Nationalize.io** | Predict country of nationality from a person's name (**No Auth**). | No | ✅ | [Link](https://nationalize.io/) |",
        "| **US Census Bureau** | Official demographic, economic, and housing data for the United States (**No Auth**). | No | ✅ | [Link](https://api.census.gov/) |",
        "| **World Bank** | Development indicators and population data for countries worldwide (**No Auth**). | No | ✅ | [Link](https://datahelpdesk.worldbank.org/knowledgebase/topics/125589) |",
    ],
    "payments-billing.md": [
        "| **Adyen** | Global payment processing platform covering online, mobile, and in-store payments. | 🔑 ApiKey | ✅ | [Link](https://docs.adyen.com/api-explorer/) |",
        "| **Braintree** | PayPal-owned payment gateway supporting subscriptions and marketplace payouts. | 🔑 ApiKey | ✅ | [Link](https://developer.paypal.com/braintree/docs) |",
        "| **Mercado Pago** | Payment platform for Latin America supporting checkout, subscriptions, and QR payments. | 🔑 ApiKey | ✅ | [Link](https://www.mercadopago.com/developers/en/docs) |",
        "| **Mollie** | European payment gateway with iDEAL, Bancontact, cards, and subscriptions. | 🔑 ApiKey | ✅ | [Link](https://docs.mollie.com/) |",
        "| **Square** | Point-of-sale, payments, catalog, and seller APIs for businesses of all sizes. | 🔑 ApiKey | ✅ | [Link](https://developer.squareup.com/reference/square) |",
    ],
    "news.md": [
        "| **Mediastack** | Live news and blog headlines from 7500+ sources with keyword filtering. | 🔑 ApiKey | ✅ | [Link](https://mediastack.com/) |",
        "| **The New York Times** | Articles, reviews, and bestseller lists from the NYT archive and current coverage. | 🔑 ApiKey | ✅ | [Link](https://developer.nytimes.com/) |",
    ],
    "business.md": [
        "| **Apollo.io** | B2B contact and company database with enrichment and people search. | 🔑 ApiKey | ✅ | [Link](https://docs.apollo.io/) |",
        "| **Hunter.io** | Find and verify professional email addresses connected to companies. | 🔑 ApiKey | ✅ | [Link](https://hunter.io/api) |",
    ],
    "backend-database.md": [
        "| **Sanity** | Structured content platform with a fully queryable hosted dataset via GROQ. | 🔑 ApiKey | ✅ | [Link](https://www.sanity.io/docs/) |",
        "| **Strapi** | Open-source headless CMS exposing a REST or GraphQL API for your content. | 🔑 ApiKey | ✅ | [Link](https://docs.strapi.io/) |",
    ],
    "web-scraping-crawling.md": [
        "| **BrowseAI** | No-code robots to extract structured data from any website without proxies. | 🔑 ApiKey | ✅ | [Link](https://www.browse.ai/docs) |",
        "| **Scrapfly** | Web scraping API with anti-bot bypass, rendering, and residential proxies. | 🔑 ApiKey | ✅ | [Link](https://scrapfly.io/docs/) |",
    ],
    "podcasts.md": [
        "| **Listen Notes** | Search engine API for 3 million+ podcasts and 300 million+ episodes. | 🔑 ApiKey | ✅ | [Link](https://www.listennotes.com/api/) |",
        "| **Podchaser** | Podcast credits, ratings, reviews, and list data. | 🔑 ApiKey | ✅ | [Link](https://api.podchaser.com/docs) |",
    ],
    "iot-smart-devices.md": [
        "| **Philips Hue** | Control lights, scenes, sensors, and entertainment areas of a Hue bridge. | 🔑 ApiKey | ✅ | [Link](https://developers.meethue.com/) |",
        "| **Shelly** | Control and monitor Shelly smart relays, plugs, and sensors over the cloud API. | 🔑 ApiKey | ✅ | [Link](https://shelly-api-docs.shelly.cloud/) |",
    ],
    "travel-tourism.md": [
        "| **Kiwi Tequila** | Flight search, pricing, and booking APIs powering Kiwi.com's travel platform. | 🔑 ApiKey | ✅ | [Link](https://tequila.kiwi.com/) |",
        "| **Opentripmap** | Places of interest, attractions, and travel guides by coordinates (**No Auth**). | No | ✅ | [Link](https://opentripmap.io/docs) |",
    ],
    "math-computation.md": [
        "| **Numbers API** | Fun math facts about any number or date (**No Auth**). | No | ✅ | [Link](http://numbersapi.com/) |",
    ],
}
for fname, rows in ADDS.items():
    t = read(fname)
    # insert before back link
    idx = t.rindex(BACK_LINK.rstrip("\n"))
    t = t[:idx] + "\n".join(rows) + "\n\n" + t[idx:]
    write(fname, t)

# ---------- 4. ALPHABETIZE ALL FILES ----------
def sort_file(f):
    t = (APIS / f).read_text(encoding="utf-8")
    lines = t.split("\n")
    rows, idxs = [], []
    for i, l in enumerate(lines):
        s = l.strip()
        if s.startswith("|") and re.search(r"\]\(https?://", s) and re.match(r"^\|\s*\*\*", s):
            rows.append(l); idxs.append(i)
    if len(rows) < 2: return
    def key(r):
        m = re.match(r"^\|\s*\*\*(.+?)\*\*", r.strip())
        return m.group(1).lower()
    rows_sorted = sorted(rows, key=key)
    for i, r in zip(idxs, rows_sorted):
        lines[i] = r
    (APIS / f).write_text("\n".join(lines), encoding="utf-8", newline="\n")

for f in sorted(p.name for p in APIS.glob("*.md")):
    sort_file(f)

# ---------- 5. REGENERATE README TABLE ----------
cats = []
for p in sorted(APIS.glob("*.md")):
    head = p.read_text(encoding="utf-8").split("\n")[0]
    m = re.match(r'^##\s+(?:<a\s+id="([^"]+)"\s*>\s*</a>\s*)?(\S+)\s+(.+)$', head.strip())
    if m:
        cats.append((m.group(3).strip(), m.group(2), m.group(1) or p.stem, p.name))
cats.sort(key=lambda c: c[0].lower())

readme = (ROOT / "README.md").read_text(encoding="utf-8")
table_lines = ["| Category | Category | Category |", "| --- | --- | --- |"]
for i in range(0, len(cats), 3):
    chunk = cats[i:i+3]
    cells = [f"[{e} {n}](./apis/{fn})" for n, e, _, fn in chunk]
    while len(cells) < 3:
        cells.append("")
    table_lines.append("| " + " | ".join(cells) + " |")
new_table = "\n".join(table_lines)

pattern = re.compile(r"\| Category \| Category \| Category \|\n\| --- \| --- \| --- \|(?:\n\|[^\n]*)*")
if not pattern.search(readme):
    raise SystemExit("README table pattern not found")
readme = pattern.sub(new_table, readme, count=1)
(ROOT / "README.md").write_text(readme, encoding="utf-8", newline="\n")

print(f"OK: {len(cats)} categories in README table")
