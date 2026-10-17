# -*- coding: utf-8 -*-
"""Wave-10 (2026-10-17): 62 additions from deep-research gap list (public-apis/api-ninjas/apilist diff),
re-deduped against CURRENT repo (waves 6-9 applied). Plus 2 fixes: Udemy -> education, Yelp Fusion -> reviews."""
import re
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from add_wave2 import norm_url, APIS, ROW_RE

ADDITIONS = [
    ("math-computation", "OEIS", "Integer-sequence entries, terms and metadata as JSON from the OEIS encyclopedia.", "No", "https://oeis.org/search?fmt=json&q=A000045"),
    ("math-computation", "CodeCogs FX Equation", "Server-side LaTeX equation rendering to PNG/SVG images.", "No", "https://fxeditor.codecogs.com/docs/1-fxtexserver_api.php"),
    ("qr-barcode", "Orca Scan", "Free barcode image generation across retail 1D/2D formats.", "No", "https://orcascan.com/guides/free-barcode-image-api-0e4a4fa6"),
    ("qr-barcode", "OpenQR", "Branded QR codes with colors, logos and scan analytics.", "🔑 ApiKey", "https://openqr.uk/api"),
    ("qr-barcode", "QR Code Crafter", "GET-based QR generation with downloadable images.", "No", "https://qrcodecrafter.com/qr-code-api"),
    ("qr-barcode", "QRX", "Stylized QR code generator with SVG output.", "No", "https://qrx.codes/developers"),
    ("fitness-wellness", "Hevy", "Workout-tracking REST API: routines, exercises, logs, webhooks.", "🔑 ApiKey", "https://api.hevyapp.com/docs"),
    ("fitness-wellness", "Free Exercise DB", "Open dataset of 800+ exercises with images.", "No", "https://github.com/yuhonas/free-exercise-db"),
    ("podcasts", "Podscan", "Search millions of podcasts; transcripts and verbatim search.", "🔑 ApiKey", "https://podscan.fm/api"),
    ("podcasts", "Transistor", "Podcast hosting API: shows, episodes, analytics, subscribers.", "🔑 ApiKey", "https://developers.transistor.fm"),
    ("podcasts", "Simplecast", "Hosting and analytics API for shows and episodes.", "🔑 ApiKey", "https://docs.simplecast.com"),
    ("tracking-logistics", "UPS", "Rating, tracking and shipping APIs from the UPS Developer Kit.", "🔑 ApiKey", "https://www.ups.com/upsdeveloperkit"),
    ("tracking-logistics", "Australia Post", "Shipping, tracking and address validation for AU/International.", "🔑 ApiKey", "https://developers.auspost.com.au"),
    ("tracking-logistics", "PostNL", "Dutch parcel labeling and tracking services.", "🔑 ApiKey", "https://developer.postnl.nl"),
    ("tracking-logistics", "Royal Mail", "UK parcel shipping, manifest and tracking APIs.", "🔑 ApiKey", "https://developer.royalmail.net"),
    ("tracking-logistics", "ShipEngine", "Multi-carrier labels, rates and tracking in one API.", "🔑 ApiKey", "https://www.shipengine.com/docs/"),
    ("travel-tourism", "Viator", "Tours & activities search, availability and booking.", "🔑 ApiKey", "https://docs.viator.com"),
    ("travel-tourism", "Travel Risk API", "Country-level travel-safety scores and advisories.", "No", "https://travelriskapi.com/docs"),
    ("travel-tourism", "themeParks API", "Live wait times and schedules for Disney, Universal and more.", "No", "https://www.themeparks.wiki/"),
    ("education", "Moodle Web Services", "LMS external functions: courses, users, grades.", "🔑 ApiKey", "https://docs.moodle.org/dev/Web_services"),
    ("education", "Blackboard Learn", "Blackboard Learn REST APIs and developer portal.", "🔐 OAuth", "https://developer.blackboard.com"),
    ("education", "Unpaywall", "Find open-access full text by DOI.", "No", "https://unpaywall.org/products/api"),
    ("museums-art", "Walters Art Museum", "Full open-access museum collection with images.", "🔑 ApiKey", "https://api.thewalters.org"),
    ("museums-art", "Artsy", "1M+ artworks, artists, auctions and galleries.", "🔐 OAuth", "https://developers.artsy.net"),
    ("museums-art", "MoMA Collection", "Complete MoMA collection dataset with image URLs.", "No", "https://github.com/MuseumofModernArt/collection"),
    ("museums-art", "BnF Gallica", "French digitized heritage search and retrieval API portal.", "No", "https://api.bnf.fr/"),
    ("museums-art", "Brooklyn Museum", "Open-access collection records and images.", "🔑 ApiKey", "https://www.brooklynmuseum.org/opencollection/api"),
    ("iot-smart-devices", "Nest Device Access", "Cameras, thermostats and doorbells via Google SDM API.", "🔐 OAuth", "https://developers.google.com/nest/device-access"),
    ("iot-smart-devices", "openHAB", "Self-hosted home automation server REST API.", "🔑 ApiKey", "https://www.openhab.org/docs/configuration/restdocs.html"),
    ("iot-smart-devices", "Homey", "Device control on the Homey smart-home hub.", "🔑 ApiKey", "https://homey.app/en-us/developer/"),
    ("iot-smart-devices", "Frigate", "Self-hosted NVR: cameras, events, clips and streams.", "No", "https://docs.frigate.video/integrations/api/"),
    ("iot-smart-devices", "Domoticz", "Self-hosted home-automation JSON API.", "🔑 ApiKey", "https://wiki.domoticz.com/Domoticz_API/JSON_URL%27s"),
    ("iot-smart-devices", "Hubitat", "Local hub Maker API for device control.", "🔑 ApiKey", "https://docs2.hubitat.com/en/home"),
    ("networking-dns", "RIPEstat Data API", "ASN, prefix, BGP and WHOIS routing data.", "No", "https://stat.ripe.net/docs/data-api/ripestat-data-api"),
    ("networking-dns", "ipwhois.io", "Free IP geolocation with timezone and currency.", "No", "https://ipwhois.io/documentation"),
    ("networking-dns", "Google Public DNS DoH", "Resolve DNS records over HTTPS via 8.8.8.8.", "No", "https://developers.google.com/speed/public-dns/docs/doh"),
    ("reviews", "Google Business Profile", "Listings management and customer reviews on Google.", "🔐 OAuth", "https://developers.google.com/my-business"),
    ("business", "HubSpot", "CRM APIs for contacts, deals, marketing and automation.", "🔐 OAuth", "https://developers.hubspot.com"),
    ("business", "Salesforce", "World's #1 CRM REST and Bulk APIs.", "🔐 OAuth", "https://developer.salesforce.com/"),
    ("business", "Intercom", "Customer messaging, support and CRM APIs.", "🔐 OAuth", "https://developers.intercom.com/"),
    ("business", "monday.com", "Work OS API: boards, items and automations.", "🔐 OAuth", "https://developer.monday.com/"),
    ("business", "BuiltWith", "Website technology profiler: stacks, hosting, analytics.", "🔑 ApiKey", "https://api.builtwith.com"),
    ("authentication-identity", "Okta", "Enterprise IAM, SSO and user management.", "🔐 OAuth", "https://developer.okta.com/"),
    ("authentication-identity", "Amazon Cognito", "AWS user pools and federated identity.", "🔐 OAuth", "https://docs.aws.amazon.com/cognito/latest/developerguide/what-is-amazon-cognito.html"),
    ("authentication-identity", "Zitadel", "Open-source IAM with OIDC/SAML and multi-tenancy.", "🔑 ApiKey", "https://zitadel.com/docs"),
    ("authentication-identity", "authentik", "Open-source identity provider with SSO and flows.", "🔑 ApiKey", "https://docs.goauthentik.io/"),
    ("authentication-identity", "Hanko", "Passkey-first open-source authentication API.", "🔑 ApiKey", "https://docs.hanko.io/"),
    ("authentication-identity", "OneLogin", "Cloud SSO, MFA and directory sync.", "🔐 OAuth", "https://developers.onelogin.com/"),
    ("authentication-identity", "Ping Identity", "Enterprise SSO, MFA and adaptive identity APIs.", "🔐 OAuth", "https://developer.pingidentity.com/"),
    ("open-source-projects", "NuGet Server API", ".NET package index and search APIs.", "No", "https://learn.microsoft.com/en-us/nuget/api/overview"),
    ("open-source-projects", "Go Module Proxy", "GOPROXY endpoints: modules, versions and @latest info.", "No", "https://proxy.golang.org"),
    ("open-source-projects", "Hackage", "Haskell package repository data API.", "No", "https://hackage.haskell.org/api"),
    ("open-source-projects", "Homebrew Formulae", "JSON API for Homebrew formulas and casks.", "No", "https://formulae.brew.sh/docs/api/"),
    ("backend-database", "PostgREST", "Serve any Postgres schema as a REST API.", "No", "https://postgrest.org/en/stable/references/api/"),
    ("backend-database", "SurrealDB", "Multi-model database with HTTP and RPC interfaces.", "🔑 ApiKey", "https://surrealdb.com/docs"),
    ("backend-database", "Directus", "Open-source data platform wrapping any SQL database.", "🔑 ApiKey", "https://directus.com/docs/"),
    ("backend-database", "SeaTable", "Spreadsheet-database hybrid REST API.", "🔑 ApiKey", "https://api.seatable.com/reference/introduction"),
    ("backend-database", "Kintone", "Low-code platform REST APIs for apps and records.", "🔑 ApiKey", "https://kintone.dev/en/"),
    ("continuous-integration", "Coolify", "Self-hosted deployment platform: apps, servers, deployments API.", "🔑 ApiKey", "https://coolify.io/docs/api/overview"),
    ("unofficial-community", "Nitter", "Privacy-focused Twitter/X front-end with RSS feeds.", "No", "https://github.com/zedeus/nitter"),
    ("unofficial-community", "Redlib", "Privacy front-end for Reddit (LibReddit successor).", "No", "https://github.com/redlib-org/redlib"),
    ("unofficial-community", "yt-dlp", "De-facto open-source media extraction for YouTube and more.", "No", "https://github.com/yt-dlp/yt-dlp"),
]

# (source_slug, name_token, dest_slug)
MOVES = [
    ("personality-quotes", "Udemy(instructor)", "education"),
    ("food-drink", "Yelp Fusion", "reviews"),
]

ROW_TMPL = "| **{name}** | {desc} | {auth} | ✅ | [Link]({url}) |"


def sort_block(fpath):
    lines = fpath.read_text(encoding="utf-8").splitlines()
    idx = [i for i, l in enumerate(lines) if l.startswith("| **")]
    first, last = idx[0], idx[-1]
    new = sorted(lines[first:last + 1], key=lambda l: ROW_RE.match(l).group(1).lower())
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
        sort_block(fpath)
        print(f"  {fpath.stem}: +{len(rows)}")

    print(f"ADDED={added} SKIPPED={skipped}")


if __name__ == "__main__":
    main()
