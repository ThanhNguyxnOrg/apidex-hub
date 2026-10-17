# -*- coding: utf-8 -*-
"""Wave-13b (2026-10-17): integrate round-2 deep-research gap list (61 items).

Skipped (conflict with earlier pass: portal-only, not API docs):
  PATENTSCOPE (patentscope.wipo.int), KIPRIS (kipris.or.kr) — landing pages.
Every URL below was HTTP-verified by the research agent (200/308/401/403/405).
Dedupe via catalog_utils.collect_index (exact name + norm_url).
"""
import sys

sys.path.insert(0, "scripts")
from catalog_utils import APIS, ROW_TMPL, collect_index, insert_rows, norm_url

ADDITIONS = [
    ("math-computation", "Sudoku", "Generate Sudoku boards by difficulty with solve and verify support.", "🔑 ApiKey", "https://api-ninjas.com/api/sudoku"),
    ("math-computation", "Unit Conversion", "Convert between 300+ units across 19 measurement categories.", "🔑 ApiKey", "https://api-ninjas.com/api/unitconversion"),
    ("math-computation", "CycleCalcs", "Astronomy calculations: sun and moon times, phases and planets.", "No", "https://www.cyclecalcs.com/api.html"),
    ("math-computation", "Open Ephemeris", "High-precision planetary positions, transits and aspects.", "🔑 ApiKey", "https://openephemeris.com/docs"),
    ("math-computation", "Nerdulator", "Derive numbers, dates and colors from a single input value.", "No", "https://nerdulator.com/api"),
    ("qr-barcode", "Barcode", "Generate EAN-13, UPC, Code 128 and multi-format barcode images.", "🔑 ApiKey", "https://api-ninjas.com/api/barcode"),
    ("qr-barcode", "GeraCode", "Free barcode images for EAN-13, UPC-A, Code 128, ITF-14 and QR.", "No", "https://www.geracodigo.com.br/api-codigo-de-barras"),
    ("qr-barcode", "Labelixa", "Render and validate Zebra ZPL label barcodes to PNG and PDF.", "🔑 ApiKey", "https://labelixa.com/docs/api"),
    ("qr-barcode", "TheQRCode", "Create QR codes for URLs, WiFi, vCards, email and SMS.", "No", "https://theqrcode.io/qr-code-api"),
    ("qr-barcode", "QR Code by LifeStep", "QR codes as PNG or SVG with size, border and color options.", "No", "https://qr.lifestep.io"),
    ("reviews", "Foursquare Places", "Current Foursquare Places API: POIs, venue tips and reviews.", "🔑 ApiKey", "https://docs.foursquare.com/"),
    ("reviews", "Pangolinfo", "Amazon product reviews and ratings across marketplaces.", "🔑 ApiKey", "https://docs.pangolinfo.com"),
    ("networking-dns", "HackerTarget", "Security scans: Nmap, DNS recon, whois and traceroute.", "No", "https://hackertarget.com/api/"),
    ("networking-dns", "ipregistry", "IP geolocation, threat and company data in a single call.", "🔑 ApiKey", "https://ipregistry.co/docs"),
    ("networking-dns", "ipdata", "IP geolocation with ASN, carrier and threat intelligence.", "🔑 ApiKey", "https://docs.ipdata.co/"),
    ("networking-dns", "Netlas", "Search internet-connected hosts, domains and devices.", "🔑 ApiKey", "https://netlas.io/apidocs"),
    ("networking-dns", "RDAP", "Standardized registration data lookups for domains and IPs.", "No", "https://rdap.org/"),
    ("networking-dns", "ipapi", "IP geolocation, ASN and lookup over HTTPS GET.", "No", "https://ipapi.co/api/"),
    ("travel-tourism", "Skyscanner", "Official flight search and pricing for affiliates and partners.", "🔑 ApiKey", "https://developers.skyscanner.net/docs/intro"),
    ("travel-tourism", "Travelpayouts", "Flight and hotel price data with affiliate commission stats.", "🔑 ApiKey", "https://support.travelpayouts.com/hc/en-us/articles/203954203"),
    ("travel-tourism", "TripIt", "Read and organize travel itineraries from TripIt accounts.", "🔐 OAuth", "https://www.tripit.com/api"),
    ("travel-tourism", "Furkot", "Access trip plans, stops and routes for Furkot users.", "🔐 OAuth", "https://help.furkot.com/widgets/furkot-api.html"),
    ("travel-tourism", "Travel Impact Model", "Flight carbon estimates under Google's TIM methodology.", "🔑 ApiKey", "https://developers.google.com/travel/impact-model"),
    ("education", "CollegeScorecard", "US higher-ed institutions: costs, admissions and outcomes.", "No", "https://collegescorecard.ed.gov/data/"),
    ("education", "BigBlueButton", "Create video classrooms and fetch recordings for e-learning.", "No", "https://docs.bigbluebutton.org/development/api/"),
    ("education", "Google Classroom", "Manage courses, rosters and coursework in Google Classroom.", "🔐 OAuth", "https://developers.google.com/classroom"),
    ("museums-art", "Wellcome Collection", "Search archives, images and manuscripts via REST and GraphQL.", "No", "https://developers.wellcomecollection.org/"),
    ("museums-art", "Auckland Museum", "Open metadata for Auckland Museum's collection objects.", "No", "https://api.aucklandmuseum.com/"),
    ("museums-art", "National Palace Museum Open Data", "Taipei NPM open data on artifacts and artwork images.", "No", "https://theme.npm.edu.tw/opendata/"),
    ("museums-art", "Library of Congress", "Search LOC collections: photos, maps, audio and manuscripts.", "No", "https://www.loc.gov/apis/"),
    ("museums-art", "National Archives Discovery", "Search UK archives: records, people, places and images.", "No", "https://discovery.nationalarchives.gov.uk/API"),
    ("fitness-wellness", "Oura", "Sleep, readiness and activity metrics from Oura Ring.", "🔑 ApiKey", "https://cloud.ouraring.com/v2/docs"),
    ("fitness-wellness", "Garmin Connect", "Health and activity data for Garmin Connect users.", "🔐 OAuth", "https://developer.garmin.com/gc-developer-program/health-api/"),
    ("fitness-wellness", "Mindbody", "Class schedules, bookings and clients for fitness studios.", "🔑 ApiKey", "https://developers.mindbodyonline.com/"),
    ("fitness-wellness", "Exercises", "Search 1300+ exercises by type, muscle and difficulty.", "🔑 ApiKey", "https://api-ninjas.com/api/exercises"),
    ("fitness-wellness", "Zepp", "Fitness and health data from Zepp/Amazfit devices.", "🔐 OAuth", "https://developer.zepp.com/"),
    ("tracking-logistics", "Bring", "Norwegian Post Group parcels and freight: labels and tracking.", "🔑 ApiKey", "https://developer.bring.com/"),
    ("tracking-logistics", "ShipStation", "Order routing, labels and shipment tracking across carriers.", "🔑 ApiKey", "https://www.shipstation.com/docs/api/"),
    ("tracking-logistics", "Onfleet", "Last-mile delivery dispatch, routing and live tracking.", "🔑 ApiKey", "https://docs.onfleet.com/"),
    ("business", "Zoho CRM", "Records, modules and workflows in Zoho CRM.", "🔐 OAuth", "https://www.zoho.com/crm/developer/docs/api/v6/"),
    ("business", "Attio", "CRM objects, records and notes with a modern REST API.", "🔐 OAuth", "https://docs.attio.com/"),
    ("business", "Basecamp", "Projects, to-dos, chats and documents in Basecamp 3.", "🔐 OAuth", "https://github.com/basecamp/bc3-api"),
    ("business", "Freshdesk", "Tickets, agents and knowledge base for Freshdesk support.", "🔑 ApiKey", "https://developers.freshdesk.com/api/"),
    ("business", "Close CRM", "Leads, contacts and deals in Close CRM.", "🔑 ApiKey", "https://developer.close.com/"),
    ("authentication-identity", "Firebase Auth", "Sign-up, sign-in and token verification REST endpoints.", "🔑 ApiKey", "https://firebase.google.com/docs/reference/rest/auth"),
    ("authentication-identity", "Corbado", "Passkey-first authentication APIs.", "🔑 ApiKey", "https://docs.corbado.com/"),
    ("authentication-identity", "Duo Security", "Manage MFA devices, policies and logs (Admin API).", "🔑 ApiKey", "https://duo.com/docs/adminapi"),
    ("unofficial-community", "ytmusicapi", "Unofficial YouTube Music client: search, playlists, library.", "No", "https://ytmusicapi.readthedocs.io/"),
    ("unofficial-community", "4chan API", "JSON API for 4chan boards, threads and posts.", "No", "https://github.com/4chan/4chan-API"),
    ("unofficial-community", "pytrends", "Unofficial Google Trends data downloads.", "No", "https://github.com/GeneralMills/pytrends"),
    ("backend-database", "Parse Server", "Open-source BaaS with REST API for data, auth and files.", "🔑 ApiKey", "https://docs.parseplatform.org/rest/guide/"),
    ("backend-database", "Firebase Realtime Database", "Low-latency JSON document GET/PUT/PATCH REST endpoints.", "No", "https://firebase.google.com/docs/reference/rest/database"),
    ("backend-database", "Meilisearch", "Fast search engine with REST index and document APIs.", "🔑 ApiKey", "https://www.meilisearch.com/docs"),
    ("continuous-integration", "Buildbot", "REST/JSON API for builds, builders and changes.", "No", "https://docs.buildbot.net/latest/developer/rest.html"),
    ("continuous-integration", "Octopus Deploy", "Deployment automation with REST API for projects and releases.", "🔑 ApiKey", "https://octopus.com/docs/api-and-integration/api"),
    ("continuous-integration", "Concourse", "Pipeline-based CI REST API reference for builds and jobs.", "No", "https://concourse-ci.org/internals.html"),
    ("open-source-projects", "Maven Central", "Search artifacts in Maven Central's public registry.", "No", "https://central.sonatype.org/search/"),
    ("open-source-projects", "MetaCPAN", "Search Perl distributions via the MetaCPAN API.", "No", "https://github.com/metacpan/metacpan-api/blob/master/docs/API-docs.md"),
    ("open-source-projects", "Open VSX", "Search and access VS Code extensions from the Open VSX registry.", "No", "https://open-vsx.org/"),
]


def main():
    names, urls = collect_index()
    per_file, added, skipped = {}, 0, 0
    for slug, name, desc, auth, url in ADDITIONS:
        if name.lower() in names or norm_url(url) in urls:
            skipped += 1
            print(f"  skip dup: {name}")
            continue
        names.add(name.lower())
        urls.add(norm_url(url))
        per_file.setdefault(APIS / f"{slug}.md", []).append(
            ROW_TMPL.format(name=name, desc=desc, auth=auth, url=url)
        )
        added += 1
    for fpath, rows in per_file.items():
        insert_rows(fpath, rows)
        print(f"  {fpath.stem}: +{len(rows)}")
    print(f"ADDED={added} SKIPPED={skipped}")


if __name__ == "__main__":
    main()
