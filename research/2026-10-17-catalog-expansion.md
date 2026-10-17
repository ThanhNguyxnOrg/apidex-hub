# Catalog Expansion Research — 2026-10-17

Method: fetched the canonical public-apis README, apilist.fun, API Ninjas (sitemap + category pages) and APIs.guru; then HTTP-verified ~160 candidate documentation URLs (status codes shown as ✅200 / ⚠403 = exists but bot-blocked / ❌). URLs that could not be verified or are dead are excluded or flagged.

**⚠ Premise corrections found during research (repo state > task's count list):**
- `apis/date-time.md` **exists** with 3 entries (Sunrise-Sunset, TimeAPI.io, TimeZoneDB) — absent from the count list in the task.
- `apis/qr-barcode.md` **exists** with 3 entries (Barcode Lookup, Barcode Spider, goQR.me) — also absent from the count list.
- `apis/demographic-analysis.md` has **6 entries** (Agify, DataUSA, Genderize, Nationalize, US Census, World Bank), not 0.
- `apis/` glob returns **84 files**, not 82 (the two above are the difference).

---

## 1. Missing categories vs public-apis

Source: https://raw.githubusercontent.com/public-apis/public-apis/master/README.md — Index section lists **51 categories**:

Animals, Anime, Anti-Malware, Art & Design, Authentication & Authorization, Blockchain, Books, Business, Calendar, Cloud Storage & File Sharing, Continuous Integration, Cryptocurrency, Currency Exchange, Data Validation, Development, Dictionaries, Documents & Productivity, Email, Entertainment, Environment, Events, Finance, Food & Drink, Games & Comics, Geocoding, Government, Health, Jobs, Machine Learning, Music, News, Open Data, Open Source Projects, **Patent**, Personality, Phone, Photography, Programming, Science & Math, Security, Shopping, Social, **Sports & Fitness**, Test Data, Text Analysis, Tracking, Transportation, URL Shorteners, **Vehicle**, Video, Weather.

Mapping against apidex-hub's 84 files:

| public-apis category | apidex-hub equivalent | Status |
|---|---|---|
| Animals…Weather (48 of 51) | animals, anime, anti-malware, authentication-identity, blockchain-web3, books, business, calendar-holidays, cloud-storage-files, continuous-integration, cryptocurrency, currency-exchange, data-validation, development, dictionaries, documents-productivity, email-sms, entertainment, environment-climate, events, finance, food-drink, games-comics, geocoding, government-civic, health, jobs-career, machine-learning, music, news, public-data, open-source-projects, personality-quotes, phone-telephony, photography, science, security-validation, shopping, social, mock-data-testing, text-analysis-nlp, tracking-logistics, transportation, url-shorteners, video, weather | ✅ covered |
| **Patent** | — | ❌ **MISSING entirely** (upstream section has EPO, PatentsView, TIPO, USPTO — https://raw.githubusercontent.com/public-apis/public-apis/master/README.md L1876-1883) |
| **Vehicle** | — | ❌ **MISSING entirely** (upstream section has 15 entries incl. NHTSA, Mercedes-Benz, Smartcar, Kelley Blue Book — same README L2511-2529) |
| Art & Design | design-colors (21) + museums-art (1) | ⚠ **fragmented & underpopulated** — one upstream section split in two; museums side has only The Met |
| Sports & Fitness | sports (29) | ⚠ fitness/health-tracker subtopic absent (see §4 fitness-wellness) |

Conversely, apidex-hub covers topics public-apis does **not**: payments-billing, travel-tourism, museums-art, math-computation, podcasts, iot-smart-devices, demographic-analysis, education, ai-llm-models, mcp-servers, monitoring-observability, backend-database, web-scraping-crawling, and the22 apify-* scraper categories (verified from the 51-item index above — no such entries there).

## 2. Topic gaps from other directories

**apilist.fun** (https://apilist.fun/ — full category nav fetched):130+ categories. Topics it lists that apidex-hub has **no category for**:
- **Translation / Localization** (categories `translation`, `localization`, `languages`) — biggest genuine gap; also absent from public-apis' index.
- **Text-to-Speech / Voice / Audio** (`text-to-speech`, `voice`, `audio`) — apidex only has music + apify-ai.
- **Crime**, **Religion**, **Nutrition**, **Names**, **Postal**, **Gambling**, **Astrology**, **Q&A**, **Ratings/Recommendations**, **Charts/Visualizations**, **Avatars**, **Blogging**, **Bookmarks**, **Project Management**, **Invoicing**, **Webhooks**, **Mobile** — all present on apilist.fun, none in apidex-hub (https://apilist.fun/ nav).
- Reviews (`ratings`) — covered only as a candidate, see §4.

**API Ninjas** (https://api-ninjas.com/api — "Explore 100+ RESTful APIs with a single API key"; endpoint list extracted from https://api-ninjas.com/sitemap.xml, categories from https://api-ninjas.com/category/*): its 11 categories are Finance, Internet Technology, AI & Computer Vision, Animals, Entertainment, Health & Wellness, Places, Text, Transportation, **Tax**, Miscellaneous. Gaps vs apidex-hub:
- **Tax** (endpoints: `incometax`, `incometaxcalculator`, `salestax`, `salestaxcalculator`, `vat`, `vatvalidation`, `propertytax`) — apidex has no tax topic at all (closest: payments-billing/finance).
- **DNS/Whois/identity lookup plumbing**: `dnslookup`, `whois`, `domain`, `mxlookup`, `iplookup`, `urllookup`, `useragent` → networking-dns-whois proposal (§4).
- **Email hygiene**: `validateemail`, `disposableemailchecker` → email-validation proposal (§4).
- **Date/time utilities**: `timezone`, `worldtime`, `workingdays`, `dayinhistory`, `bankholidays` → thins out apidex's existing date-time file (§3).
- **Demographics**: `population`, `gdp`, `inflation`, `unemployment` → confirms demographic-analysis can grow beyond name-guessing APIs (§3).
- **Vehicle**: `vinlookup`, `motorcarrier`, `cars`, `evcharger`, `helicopter`, `aircraft` → vehicle proposal (§4).
- **Food/nutrition** (`recipe`, `caloriesburned`, `exercises`, `nutrition`, `cocktail`), **Lottery/Gambling** (`lottery`, `powerball`, `megamillions`), **Astrology** (`horoscope`) — thin/absent in apidex.
- Apidex already matches their finance, animals, places/geocoding, text, weather, transportation angles.

**APIs.guru** (https://apis.guru/ — "Wikipedia for Web APIs. Directory of REST API definitions", backed by https://github.com/APIs-guru/openapi-directory; machine list at https://api.apis.guru/v2/list.json ✅): different mission — it catalogs **OpenAPI spec files** per provider (Google, Stripe, Twilio, AWS-class enterprise APIs), not curated free-API topics. Gap for apidex: no "spec/directory discovery" angle (could be a cross-link, not a category); no topic it covers that apidex lacks outright.

## 3. Underpopulated categories — famous missing APIs

All URLs HTTP-verified today unless noted. Auth column suggestion given in brackets.

### payments-billing (6: Lemon Squeezy, Paddle, PayOS, PayPal, Razorpay, Stripe)
Missing giants — add:
- **Stripe** ✅ https://docs.stripe.com/api — *already present* (listed for reference) → add **Square** ✅ https://developer.squareup.com/reference/square [OAuth]
- **Braintree** ✅ https://developer.paypal.com/braintree/docs [ApiKey]
- **Mercado Pago** ✅ https://www.mercadopago.com/developers/en/docs [ApiKey]
- **Adyen** ✅ https://docs.adyen.com/api-explorer/ [ApiKey]
- **Mollie** ✅ https://docs.mollie.com/ [ApiKey]
- **dLocal** ✅ https://docs.dlocal.com/ [ApiKey]
- **Flutterwave** ✅ https://developer.flutterwave.com/ [ApiKey]
- **MoMo** ✅ https://developers.momo.vn/ [ApiKey] (relevant for VN market next to PayOS)
- **Paystack** ⚠403 https://paystack.com/docs/ [ApiKey]

### travel-tourism (5: Amadeus, CityBikes, TimeZoneDB, US Border Wait Times, Wikivoyage)
- **Kiwi Tequila** ✅ https://tequila.kiwi.com/ [ApiKey]
- **Duffel** ✅ https://docs.duffel.com/ [ApiKey]
- **Aviationstack** ✅ https://aviationstack.com/ [ApiKey]
- **Transport for London** ✅ https://api.tfl.gov.uk/ [No]
- **Transitland** ✅ https://www.transit.land/documentation/ [ApiKey]
- **Budget Your Trip** ✅ https://www.budgetyourtrip.com/api [No]
- **Lufthansa** ✅ https://developer.lufthansa.com/ [ApiKey]
- **Hotelbeds** ✅ https://developer.hotelbeds.com/ [ApiKey]
- **Rome2rio** ⚠403 https://www.rome2rio.com/documentation [ApiKey]
- Housekeeping: **TimeZoneDB sits in this file but is a date/time API** — it is also referenced in date-time.md; move/keep in one place.

### museums-art (1: Metropolitan Museum)
- **Art Institute of Chicago** ✅ https://api.artic.edu/docs/ [No]
- **Cleveland Museum of Art** ✅ https://www.clevelandart.org/open-access-api [No]
- **Rijksmuseum** ✅ https://data.rijksmuseum.nl/ [ApiKey]
- **Harvard Art Museums** ✅ https://github.com/harvardartmuseums/api-docs [ApiKey]
- **Europeana** ⚠403 https://pro.europeana.eu/page/search [ApiKey]
- **Smithsonian Open Access** ✅ https://github.com/Smithsonian/smithsonian-openaccess (root api.si.edu ⚠403) [ApiKey]
- **Cooper Hewitt** ⚠403 https://collection.cooperhewitt.org/api [OAuth]
- **National Gallery of Art** ✅ https://github.com/NationalGalleryOfArt/opendata [No]
- **Tate** ✅ https://github.com/tategallery/collection [No]
- Not verified → do not add: Louvre (https://collections.louvre.fr/ loads but no public API docs found), Coolblue (e-commerce, not a museum API).

### math-computation (2: math.js, Unit Converter)
- **Wolfram|Alpha** ✅ https://products.wolframalpha.com/api [ApiKey]
- **Wolfram Cloud** ✅ https://reference.wolframcloud.com/ [OAuth/ApiKey]
- **Mathpix** ✅ https://mathpix.com/docs/ (math OCR/formula recognition) [ApiKey]
- ⚠ **Numbers API (numbersapi.com) appears DEFUNCT**: HTTP404 on `/` and `/42`, TLS cert CN invalid (verified via direct fetch and via proxy). Do not add.

### news (9: Currents, Dev.to, GNews, HN/Algolia, NewsAPI, NewsAPI.ai, NewsData.io, Guardian, TheNewsAPI)
- **The New York Times** ✅ https://developer.nytimes.com/ [ApiKey/OAuth]
- **BBC** ✅ https://www.bbc.co.uk/developer [ApiKey]
- **Mediastack** ✅ https://mediastack.com/ [ApiKey]
- **Feedly** ✅ https://feedly.com/i/developer [OAuth]
- **Webz.io** ✅ https://webz.io/ [ApiKey]
- **Chronicling America (Library of Congress)** ⚠403 https://chroniclingamerica.loc.gov/about/api/ [No]
- ⚠ **Event Registry == NewsAPI.ai**: https://eventregistry.org/news_api resolves to the NewsAPI.ai product which is **already in news.md** — don't duplicate.
- Aylien (docs.aylien.com) no longer resolves — skip.

### business (7: Domainsdb, Charity Search, Clearbit Logo, Freelancer, Gmail, Google Analytics, SwiftKanban)
- **Hunter** ✅ https://hunter.io/api [ApiKey]
- **Apollo** ✅ https://docs.apollo.io/ [ApiKey]
- **OpenCorporates** ✅ https://knowledge.opencorporates.com/knowledge-base/api-documentation/ [ApiKey]
- **PeopleDataLabs** ✅ https://www.peopledatalabs.com/ [ApiKey]
- **Xero** ✅ https://developer.xero.com/documentation/api/accounting/overview [OAuth]
- **QuickBooks (Intuit)** ✅ https://developer.intuit.com/app/developer/qbo/docs/api [OAuth]
- **BambooHR** ✅ https://documentation.bamboohr.com/ [ApiKey]
- **EU VAT VIES** ✅ https://ec.europa.eu/taxation_customs/vies/ [No]
- Crunchbase: could not verify any current docs URL (console.crunchbase.com does not resolve) — skip until URL confirmed.

### web-scraping-crawling (7: Exa AI, Firecrawl, Jina Reader, ScraperAPI, ScrapingBee, Tavily, ZenRows)
- **ScrapingAnt** ✅ https://www.scrapingant.com/ [ApiKey]
- **Browserless** ✅ https://docs.browserless.io/ [ApiKey]
- **Bright Data** ✅ https://docs.brightdata.com/ [ApiKey]
- **ScrapFly** ✅ https://scrapfly.io/docs/ [ApiKey]
- **Zyte** ✅ https://docs.zyte.com/ [ApiKey]
- **Diffbot** ✅ https://docs.diffbot.com/ [ApiKey]
- **ScrapingFish** ✅ https://www.scrapingfish.com/docs [ApiKey]
- Oxylabs: docs subdomain does not resolve (docs.oxylabs.com ENOTFOUND; oxylabs.io/documentation →404) — skip or find new URL first.

### backend-database (7: Appwrite, Convex, Neon, PlanetScale, Supabase, Turso, Upstash)
- **Firebase** ✅ https://firebase.google.com/docs/reference [ApiKey]
- **Airtable** ✅ https://airtable.com/developers/web/api/introduction [OAuth]
- **PocketBase** ✅ https://pocketbase.io/docs/ [No]
- **MongoDB Atlas** ✅ https://www.mongodb.com/docs/atlas/api/ [ApiKey]
- **NocoDB** ✅ https://docs.nocodb.com/ [ApiKey]
- **Baserow** ✅ https://baserow.io/docs [ApiKey]
- **Xata** ✅ https://docs.xata.io/ [ApiKey]

### iot-smart-devices (8: Adafruit IO, Arduino IoT, Blynk, Home Assistant, IFTTT, Particle, ThingsBoard, Tuya)
- **Philips Hue** ✅ https://developers.meethue.com/ [OAuth]
- **SmartThings** ✅ https://developer.smartthings.com/docs/api/public [OAuth]
- **ThingSpeak** ⚠403 https://www.mathworks.com/help/thingspeak/rest-api.html [ApiKey]
- **Shelly** ✅ https://shelly-api-docs.shelly.cloud/ [No/ApiKey]
- **ESP RainMaker** ✅ https://rainmaker.espressif.com/ [ApiKey]

### podcasts (9: Acast, Audioboom, Buzzsprout, Fountain, fyyd, gpodder, Podbean, Podcast Index, Taddy)
- **Listen Notes** ⚠403 https://www.listennotes.com/api/ [ApiKey]
- **Apple Podcasts / iTunes Search** ✅ https://performance-partners.apple.com/search-api [No]
- **Podchaser** ⚠403 https://www.podchaser.com/developers [OAuth]
- **Audiosearch** ✅ https://audiosearch.com/developers [ApiKey]
- Spreaker (developer.spreaker.com) no longer resolves — skip.

### demographic-analysis (6 actual: Agify, DataUSA, Genderize, Nationalize, US Census, World Bank)
- **IPUMS** ⚠403 https://ipums.org/support/api [ApiKey]
- **Statistics Canada** ✅ https://www.statcan.gc.ca/eng/developers [No]
- **OECD SDMX** ⚠403 https://sdmx.oecd.org/ [No]
- **Eurostat dissemination API** ✅ reachable at https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/ (query returned400 = endpoint alive; official docs page moved and could not be located — cite endpoint base)
- **API Ninjas Population** ✅ https://api.ninjas.com/api/population [ApiKey]
- UN data.un.org loads ✅ but webservices doc path is dead — skip.

### (bonus) date-time (3 actual) and qr-barcode (3 actual)
date-time add: **Astronomy API** ✅ https://docs.astronomyapi.com/ [ApiKey] · **Abstract Time Zone** ✅ https://www.abstractapi.com/api/time-zone-api [ApiKey] · **caldays** ✅ https://caldays.com/api [No] · **World Time API** (worldtimeapi.org) — endpoint socket-closes intermittently; add with caveat or skip.
qr-barcode add: **TEC-IT Barcode Generator** ✅ https://www.tec-it.com/en/software/online-components/barcode-generator-api/overview [No] · **DynaPictures** ✅ https://dynapictures.com/docs [ApiKey] · **QRickit** ⚠403 https://qrickit.com/api/ [No] · **API Ninjas QR code** ✅ https://api-ninjas.com/api/qrcode [ApiKey].

## 4. Proposed new categories

Ten proposals, each with ≥5 verified, genuinely usable free/freemium APIs. Format per file: `| **Name** | Description. | No/🔑 ApiKey/🔐 OAuth | ✅ | [Link](https://...) |` — **no raw pipes inside cells** (this is the constraint used by existing files, e.g. `apis/payments-billing.md`).

**1. `gaming.md` — Gaming & Interactive Entertainment.** Rationale: Steam/Twitch/Riot data powers companion apps, alerts, stats sites; apidex's games-comics (77) is lore/trivia-focused, not platform APIs.
- Steam Web API ✅ https://partner.steamgames.com/doc/webapi [No]
- Twitch Helix ✅ https://dev.twitch.tv/docs/api/ [OAuth]
- Riot Games ✅ https://developer.riotgames.com/ [ApiKey]
- IGDB ✅ https://api-docs.igdb.com/ [ApiKey]
- RAWG ✅ https://rawg.io/apidocs [ApiKey]
- Blizzard Battle.net ✅ https://develop.battle.net/documentation [OAuth]
- PokéAPI ✅ https://pokeapi.co/ [No]
- Hypixel ✅ https://api.hypixel.net/ [ApiKey]
- PUBG ⚠403 https://developer.pubg.com/ [ApiKey]

**2. `cinema-tv.md` — Cinema & TV.** Rationale: entertainment.md (15) is generic; movie/TV metadata is one of the most-used free API topics (watchlists, media apps).
- TMDB ✅ https://developer.themoviedb.org/docs [ApiKey]
- OMDb ✅ http://www.omdbapi.com/ [ApiKey]
- TVmaze ✅ https://www.tvmaze.com/api [No]
- Trakt ✅ https://trakt.docs.apiary.io/ [ApiKey]
- TheTVDB v4 ✅ https://thetvdb.github.io/v4-api/ [ApiKey]
- Watchmode ✅ https://api.watchmode.com/ [ApiKey]
- Simkl ✅ https://simkl.com/developer/ [OAuth]

**3. `translation-localization.md` — Translation & Localization.** Rationale: top-3 missing topic vs apilist.fun; needed by every product with non-English users; absent from public-apis' index too (source §1).
- DeepL ✅ https://developers.deepl.com/ [ApiKey]
- LibreTranslate ✅ https://libretranslate.com/docs/ [No]
- Google Cloud Translation ✅ https://cloud.google.com/translate/docs/reference/rest [OAuth]
- Microsoft Translator ✅ https://learn.microsoft.com/en-us/azure/ai-services/translator/ [ApiKey]
- Amazon Translate ✅ https://docs.aws.amazon.com/translate/ [OAuth]
- ModernMT ✅ https://www.modernmt.com/api/ [ApiKey]
- MyMemory ✅ https://api.mymemory.translated.net/ [No]

**4. `email-validation.md` — Email Validation & Verification.** Rationale: split from email-sms (sending); API Ninjas and apilist.fun both treat it as distinct; essential for signups/lead-gen quality.
- ZeroBounce ✅ https://www.zerobounce.net/docs/ [ApiKey]
- NeverBounce ✅ https://developers.neverbounce.com/ [ApiKey]
- Abstract Email Verification ✅ https://www.abstractapi.com/api/email-verification-validation-api [ApiKey]
- Emailable ✅ https://emailable.com/docs/ [ApiKey]
- Kickbox ✅ https://docs.kickbox.com/ [ApiKey]
- Validator.pizza ✅ https://validator.pizza/ [No]

**5. `networking-dns-whois.md` — Networking, DNS & WHOIS.** Rationale: API Ninjas dedicates endpoints to `dnslookup`/`whois`/`mxlookup`/`iplookup`; essential for security, SEO and domain tooling; no apidex category covers it.
- Cloudflare DNS-over-HTTPS ✅ https://developers.cloudflare.com/1.1.1.1/encryption/dns-over-https/make-api-requests/dns-json/ [No]
- ICANN RDAP ✅ https://www.icann.org/rdap [No]
- Shodan ✅ https://developer.shodan.io/ [ApiKey]
- SecurityTrails ⚠403 https://securitytrails.com/corp/apidocs [ApiKey]
- IPinfo ✅ https://ipinfo.io/developers [ApiKey]
- WhoisXML API ✅ https://whoisxmlapi.com/ [ApiKey]

**6. `wikipedia-encyclopedic.md` — Wikipedia & Encyclopedic Knowledge.** Rationale: structured-knowledge building block for RAG/assistants; apidex has Wikivoyage buried in travel but no Wikipedia/Wikidata home.
- Wikipedia/MediaWiki Action API ✅ https://www.mediawiki.org/wiki/API:Main_page [No]
- Wikidata ✅ https://www.wikidata.org/w/api.php [No]
- DBpedia ✅ https://www.dbpedia.org/resources/linked-data/ [No]
- Wikimedia Enterprise ✅ https://enterprise.wikimedia.com/ [ApiKey]
- Fandom (Wikia) ✅ https://developer.fandom.com/ (⚠403 to bots) [OAuth]

**7. `fitness-wellness.md` — Fitness & Wellness.** Rationale: public-apis' "Sports & Fitness" maps only to apidex `sports` (29, data feeds); wearable/workout/nutrition APIs are missing entirely (also matches API Ninjas `health-wellness`).
- Strava ✅ https://strava.github.io/api/ [OAuth]
- Fitbit ✅ https://dev.fitbit.com/ [OAuth]
- WHOOP ✅ https://developer.whoop.com/ [OAuth]
- Withings ✅ https://developer.withings.com/ [OAuth]
- wger (exercise/nutrition DB) ✅ https://wger.de/en/software/api [ApiKey]
- Nutritionix ✅ https://developer.nutritionix.com/ [ApiKey]
- FatSecret ✅ https://platform.fatsecret.com/docs [OAuth]

**8. `reviews.md` — Reviews & Ratings.** Rationale: apilist.fun has `ratings`; product/marketplace apps need review aggregation; nothing in apidex covers it (shopping/seo don't).
- Yelp Fusion ✅ https://docs.developer.yelp.com/docs/fusion-intro [OAuth]
- Trustpilot ✅ https://developers.trustpilot.com/ [ApiKey]
- Google Places ✅ https://developers.google.com/maps/documentation/places/web-service/ [ApiKey]
- Reviews.io ✅ https://developer.reviews.io/ [ApiKey]
- Amazon PA-API ✅ https://webservices.amazon.com/paapi5/documentation/ [ApiKey]

**9. `patents-research.md` — Patents & Prior Art.** Rationale: fills the **exact "Patent" hole vs public-apis** (§1); R&D/competitive-intel users, not covered anywhere in apidex.
- USPTO Open Data Portal ✅ https://developer.uspto.gov/api-catalog [No]
- EPO Open Patent Services ✅ https://developers.epo.org/ [OAuth]
- PatentsView ✅ https://patentsview.org/apis/purpose [No]
- The Lens ✅ https://about.lens.org/lens-api/ [OAuth/ApiKey]
- Google Patents Public Data (BigQuery) ✅ https://cloud.google.com/bigquery/public-data [OAuth]

**10. `vehicle-mobility.md` — Vehicle & Mobility.** Rationale: fills the **exact "Vehicle" hole vs public-apis** (§1,15 upstream entries); 6/6 candidate URLs verified.
- NHTSA vPIC (VIN decode) ✅ https://vpic.nhtsa.dot.gov/api/ [No]
- NHTSA Recalls ✅ https://api.nhtsa.gov/recalls/recallsByVehicle?make=honda&model=civic&modelYear=2020 [No]
- Smartcar ✅ https://smartcar.com/docs/ [OAuth]
- Mercedes-Benz ✅ https://developer.mercedes-benz.com/apis [OAuth]
- FIPE (Brazil vehicle prices) ✅ https://deividfortuna.github.io/fipe/ [No]
- WhichTrim ✅ https://whichtrim.com/developers/ [ApiKey]
- CarVector ✅ https://carvector.io/docs [ApiKey]

**Runners-up (also pass ≥5, pick if expanding beyond10):**
- `sustainability-esg.md`: Climatiq ✅ https://docs.climatiq.io/ · Carbon Interface ✅ https://docs.carboninterface.com/ · WattTime ✅ https://www.watttime.org/api-documentation/ · CO2 Signal ✅ https://co2signal.com/ · Electricity Maps ✅ https://static.electricitymaps.com/api/docs/index.html
- `opensource-license.md`: GitHub Licenses ✅ https://docs.github.com/en/rest/licenses · deps.dev ✅ https://docs.deps.dev/api/v3alpha/ · ClearlyDefined ✅ https://docs.clearlydefined.io/ · Libraries.io ✅ https://libraries.io/api · FOSSA ✅ https://docs.fossa.io/
- `date-time` and `qr-barcode`: **already exist** — treat as populate (§3), don't create.

**Evaluated and rejected (<5 good free APIs or wrong fit):**
- *qna-forum*: only Stack Exchange + Discourse official; Quora/Zhihu/V2EX have no public API.
- *chess*: only Chess.com + Lichess (FIDE has none) → fold into games-comics instead.
- *fashion-apparel*: only Shopify Storefront/eBay/Walmart — generic commerce, duplicates shopping.md.
- *real-estate (non-Apify)*: Zillow/Redfin/Rightmove have no free public API (Bridge is partner-only); vacation-rental (Guesty/Lodgify) niche → keep in apify-real-estate for now.
- *regex-lookup*: no real public APIs (regex101 etc. are apps) → utilities-tools.
- *telecom-esim*: Airalo/eSIM providers expose only partner APIs → phone-telephony.
- *design-inspiration*: Dribbble + Behance (both OAuth, restrictive) only → design-colors.
- *books-reading*: books.md already15 entries incl. Google Books/Open Library/Gutendex.

**Format constraints (from existing files, e.g. `apis/payments-billing.md`, `apis/museums-art.md`):** file starts `## <a id="kebab-id"></a>Emoji Title`, then header `| API Name | Description | Auth | HTTPS | Link |`, then rows exactly `| **Name** | Description. | No/🔑 ApiKey/🔐 OAuth | ✅ | [Link](https://...) |`, ends with `[⬆ Back to Table of Contents](../README.md#table-of-contents)`. No raw `|` inside any cell; description ends with a period.

## 5. Sources

**Primary directories fetched**
- https://raw.githubusercontent.com/public-apis/public-apis/master/README.md (51-category index; Patent L1876, Vehicle L2511 sections)
- https://apilist.fun/ (130+ category navigation)
- https://api-ninjas.com/api · https://api-ninjas.com/sitemap.xml (163 endpoints,11 categories) · https://api-ninjas.com/category/finance (category pattern)
- https://apis.guru/ · https://api.apis.guru/v2/list.json · https://github.com/APIs-guru/openapi-directory

**Verified API docs URLs (HTTP200 today)** — payments: https://docs.stripe.com/api · https://developer.squareup.com/reference/square · https://developer.paypal.com/braintree/docs · https://www.mercadopago.com/developers/en/docs · https://docs.dlocal.com/ · https://docs.adyen.com/api-explorer/ · https://docs.mollie.com/ · https://developer.flutterwave.com/ · https://developers.momo.vn/ ; travel: https://tequila.kiwi.com/ · https://docs.duffel.com/ · https://aviationstack.com/ · https://api.tfl.gov.uk/ · https://www.transit.land/documentation/ · https://www.budgetyourtrip.com/api · https://developer.lufthansa.com/ · https://developer.hotelbeds.com/ ; museums: https://api.artic.edu/docs/ · https://www.clevelandart.org/open-access-api · https://data.rijksmuseum.nl/ · https://github.com/harvardartmuseums/api-docs · https://github.com/Smithsonian/smithsonian-openaccess · https://github.com/NationalGalleryOfArt/opendata · https://github.com/tategallery/collection ; math: https://products.wolframalpha.com/api · https://reference.wolframcloud.com/ · https://mathpix.com/docs/ ; news: https://developer.nytimes.com/ · https://www.bbc.co.uk/developer · https://mediastack.com/ · https://feedly.com/i/developer · https://webz.io/ ; business: https://hunter.io/api · https://docs.apollo.io/ · https://knowledge.opencorporates.com/knowledge-base/api-documentation/ · https://www.peopledatalabs.com/ · https://developer.xero.com/documentation/api/accounting/overview · https://developer.intuit.com/app/developer/qbo/docs/api · https://documentation.bamboohr.com/ · https://ec.europa.eu/taxation_customs/vies/ ; scraping: https://www.scrapingant.com/ · https://docs.browserless.io/ · https://docs.brightdata.com/ · https://scrapfly.io/docs/ · https://docs.zyte.com/ · https://docs.diffbot.com/ · https://www.scrapingfish.com/docs ; backend: https://firebase.google.com/docs/reference · https://airtable.com/developers/web/api/introduction · https://pocketbase.io/docs/ · https://www.mongodb.com/docs/atlas/api/ · https://docs.nocodb.com/ · https://baserow.io/docs · https://docs.xata.io/ ; iot: https://developers.meethue.com/ · https://developer.smartthings.com/docs/api/public · https://shelly-api-docs.shelly.cloud/ · https://rainmaker.espressif.com/ ; podcasts: https://performance-partners.apple.com/search-api · https://audiosearch.com/ ; demographics: https://www.statcan.gc.ca/eng/developers · https://api.ninjas.com/api/population ; gaming: https://partner.steamgames.com/doc/webapi (verified via proxy) · https://dev.twitch.tv/docs/api/ · https://developer.riotgames.com/ · https://api-docs.igdb.com/ · https://rawg.io/apidocs · https://develop.battle.net/documentation · https://pokeapi.co/ · https://api.hypixel.net/ ; cinema: https://developer.themoviedb.org/docs · http://www.omdbapi.com/ · https://www.tvmaze.com/api · https://trakt.docs.apiary.io/ · https://thetvdb.github.io/v4-api/ · https://api.watchmode.com/ · https://simkl.com/developer/ ; translation: https://developers.deepl.com/ · https://libretranslate.com/docs/ · https://cloud.google.com/translate/docs/reference/rest · https://learn.microsoft.com/en-us/azure/ai-services/translator/ · https://docs.aws.amazon.com/translate/ · https://www.modernmt.com/api/ · https://api.mymemory.translated.net/ ; email: https://www.zerobounce.net/docs/ · https://developers.neverbounce.com/ · https://www.abstractapi.com/api/email-verification-validation-api · https://emailable.com/docs/ · https://docs.kickbox.com/ · https://validator.pizza/ ; networking: https://developers.cloudflare.com/1.1.1.1/encryption/dns-over-https/make-api-requests/dns-json/ · https://www.icann.org/rdap · https://developer.shodan.io/ · https://ipinfo.io/developers · https://whoisxmlapi.com/ ; wiki: https://www.mediawiki.org/wiki/API:Main_page · https://www.wikidata.org/w/api.php · https://www.dbpedia.org/resources/linked-data/ · https://enterprise.wikimedia.com/ ; fitness: https://strava.github.io/api/ · https://dev.fitbit.com/ · https://developer.whoop.com/ · https://developer.withings.com/ · https://wger.de/en/software/api · https://developer.nutritionix.com/ · https://platform.fatsecret.com/docs ; reviews: https://docs.developer.yelp.com/docs/fusion-intro · https://developers.trustpilot.com/ · https://developers.google.com/maps/documentation/places/web-service/ · https://developer.reviews.io/ · https://webservices.amazon.com/paapi5/documentation/ ; patents: https://developer.uspto.gov/api-catalog · https://www.uspto.gov/learning-and-resources/open-data-and-mobility · https://developers.epo.org/ · https://patentsview.org/apis/purpose · https://about.lens.org/lens-api/ · https://cloud.google.com/bigquery/public-data · https://tiponet.tipo.gov.tw/Gazette/OpenData/OD/OD05.aspx?QryDS=API00 ; vehicle: https://vpic.nhtsa.dot.gov/api/ · https://api.nhtsa.gov/recalls/recallsByVehicle?make=honda&model=civic&modelYear=2020 · https://smartcar.com/docs/ · https://developer.mercedes-benz.com/apis · https://deividfortuna.github.io/fipe/ · https://whichtrim.com/developers/ · https://carvector.io/docs ; runners-up: https://docs.climatiq.io/ · https://docs.carboninterface.com/ · https://www.watttime.org/api-documentation/ · https://co2signal.com/ · https://static.electricitymaps.com/api/docs/index.html · https://docs.github.com/en/rest/licenses · https://docs.deps.dev/api/v3alpha/ · https://docs.clearlydefined.io/ · https://libraries.io/api · https://docs.fossa.io/ ; misc/section3: https://www.abstractapi.com/api/time-zone-api · https://docs.astronomyapi.com/ · https://caldays.com/api · https://sunrise-sunset.org/api · https://timeapi.io/swagger/index.html · https://timezonedb.com/api · http://goqr.me/api/ · https://www.tec-it.com/en/software/online-components/barcode-generator-api/overview · https://dynapictures.com/docs · https://api-ninjas.com/api/qrcode · http://www.barcodespider.com/api · https://www.barcodelookup.com/developers · https://datahelpdesk.worldbank.org/knowledgebase/topics/125589 · https://datausa.io/about/api/ · https://developers.google.com/books/ · https://www.si.edu/opendata/documentation (403)

**Found dead / unusable (do not add)** — numbersapi.com (404 + invalid TLS cert), developer.spreaker.com (NXDOMAIN), docs.aylien.com (NXDOMAIN), docs.oxylabs.com (NXDOMAIN), oxylabs.io/documentation (404), console.crunchbase.com (NXDOMAIN), eventregistry.org/news_api (= NewsAPI.ai, already present), carqueryapi.com (unreachable), europa.eu/taxation_customs/vies is fine but https://ec.europa.eu/eurostat/web/developers (404), https://data.un.org/webservices/ (404), aeroapi.flightaware.com/docs (404).

**Repo files consulted**: apis/payments-billing.md, apis/museums-art.md, apis/travel-tourism.md, apis/news.md, apis/business.md, apis/web-scraping-crawling.md, apis/backend-database.md, apis/iot-smart-devices.md, apis/podcasts.md, apis/math-computation.md, apis/date-time.md, apis/qr-barcode.md, apis/demographic-analysis.md.
