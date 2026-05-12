# 🚀 Awesome Dev APIs

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A curated collection of awesome free APIs for developers. Open source and community-driven.
> This repository aims to provide a comprehensive collection of free and freemium APIs to help you build your next project.

<div align="center">

[![GitHub Stars](https://img.shields.io/github/stars/ThanhNguyxnOrg/awesome-free-apis?style=social)](https://github.com/ThanhNguyxnOrg/awesome-free-apis/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/ThanhNguyxnOrg/awesome-free-apis?style=social)](https://github.com/ThanhNguyxnOrg/awesome-free-apis/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/ThanhNguyxnOrg/awesome-free-apis)](https://github.com/ThanhNguyxnOrg/awesome-free-apis/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/ThanhNguyxnOrg/awesome-free-apis)](https://github.com/ThanhNguyxnOrg/awesome-free-apis/pulls)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Maintained](https://img.shields.io/badge/Maintained-Yes-brightgreen?style=flat-square)](https://github.com/ThanhNguyxnOrg/awesome-free-apis)
[![Visitors](https://api.visitorbadge.io/api/visitors?path=ThanhNguyxn%2Fawesome-free-apis&countColor=%23263759&style=flat)](https://visitorbadge.io/status?path=ThanhNguyxn%2Fawesome-free-apis)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-support-FFDD00?style=flat-square&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/thanhnguyxn)

</div>

---

## 📚 Code Examples

> **✨ New!** Check out [practical code examples](examples/) showing how to use popular APIs from this collection.  
> Includes Python & JavaScript examples for Pokemon, Cryptocurrency, AI Chat, and more!

---

## <a id="general-api-usage-guide"></a>📘 General API Usage Guide

> **👋 New to APIs?** Don't worry! This guide will help you understand the basics and get started quickly.

---

### 💡 What is an API?

**API** stands for **Application Programming Interface**. It's a way for different applications to communicate with each other.

```
┌─────────┐      ┌─────────┐      ┌─────────┐
│   YOU   │ ───▶│   API   │ ───▶ │ SERVER  │
│  (App)  │ ◀───│ (Waiter)│ ◀─── │(Kitchen)│
└─────────┘      └─────────┘      └─────────┘
   Request         Process          Response
```

**Think of it like a restaurant:**
- 🙋 **You** (the app) place an order
- 🍽️ **Waiter** (the API) takes your request to the kitchen
- 👨‍🍳 **Kitchen** (the server) prepares your food (data)
- ✨ The waiter brings it back to you!

---

### 📝 Authentication Methods

Different APIs have different ways to verify who you are:

| Method | Icon | Description | Example |
|--------|------|-------------|---------|
| **No Auth** | 🌐 | Open for everyone - just call it! | Weather APIs, public data |
| **API Key** | 🔑 | Secret code you get when registering | `?api_key=abc123` or `Authorization: abc123` |
| **OAuth** | 🔐 | Secure login (like "Login with Google") | Social media integrations |

**💡 Pro Tip:** Always keep your API keys secret! Never commit them to GitHub.

---

### 📡 HTTP Request Methods

Learn the common ways to interact with APIs:

| Method | Icon | Purpose | Real-World Example |
|--------|------|---------|-------------------|
| `GET` | 📥 | **Retrieve** data | Get a list of cat pictures |
| `POST` | 📤 | **Create** new data | Upload a new photo |
| `PUT` | ✏️ | **Replace** existing data | Update entire user profile |
| `PATCH` | 🔧 | **Modify** specific fields | Change just your username |
| `DELETE` | 🗑️ | **Remove** data | Delete a comment |

**Example GET Request:**
```bash
curl https://api.example.com/cats
```

**Example POST Request:**
```bash
curl -X POST https://api.example.com/cats \
  -H "Content-Type: application/json" \
  -d '{"name":"Fluffy","age":3}'
```

---

### 🚦 HTTP Status Codes

The API responds with a status code to tell you what happened:

#### ✅ Success Codes (2xx)
| Code | Icon | Meaning |
|------|------|---------|
| `200` | ✅ | **OK** - Request succeeded! |
| `201` | 🎉 | **Created** - New resource created! |
| `204` | 📭 | **No Content** - Success but no data to return |

#### ⚠️ Client Error Codes (4xx)
| Code | Icon | Meaning | What to Do |
|------|------|---------|-----------|
| `400` | ❌ | **Bad Request** - Invalid syntax | Check your request format |
| `401` | 🔒 | **Unauthorized** - Authentication required | Add your API key |
| `403` | 🚫 | **Forbidden** - You don't have permission | Check your access rights |
| `404` | 🔍 | **Not Found** - Resource doesn't exist | Verify the URL |
| `429` | 🐌 | **Too Many Requests** - Rate limit hit | Wait and try again |

#### 🔴 Server Error Codes (5xx)
| Code | Icon | Meaning |
|------|------|---------|
| `500` | 💥 | **Internal Server Error** - API is broken |
| `503` | 🔧 | **Service Unavailable** - API is down |

---

### 🛠️ Essential Tools for Testing APIs

| Tool | Best For | Platform | Free? |
|------|----------|----------|-------|
| [**Postman**](https://www.postman.com/) | 🎯 Complete API testing & documentation | Desktop/Web | ✅ Yes (free tier) |
| [**Thunder Client**](https://www.thunderclient.com/) | ⚡ Lightweight testing in VS Code | VS Code Extension | ✅ Yes |
| [**cURL**](https://curl.se/) | 💻 Command-line requests | Terminal | ✅ Yes (built-in) |
| [**Insomnia**](https://insomnia.rest/) | 🎨 Beautiful UI for API testing | Desktop | ✅ Yes |

---

### 🚀 Quick Start Example

Let's try a real API call! Here's how to get a random cat fact:

**1️⃣ Using cURL (Terminal):**
```bash
curl https://catfact.ninja/fact
```

**2️⃣ Using JavaScript (Browser):**
```javascript
fetch('https://catfact.ninja/fact')
  .then(response => response.json())
  .then(data => console.log(data.fact));
```

**3️⃣ Using Python:**
```python
import requests
response = requests.get('https://catfact.ninja/fact')
print(response.json()['fact'])
```

**📦 Expected Response:**
```json
{
  "fact": "Cats have 32 muscles in each ear.",
  "length": 38
}
```

---

### 📚 Additional Resources

- 📖 [What is REST API?](https://www.redhat.com/en/topics/api/what-is-a-rest-api) - RedHat Guide
- 🎓 [HTTP Status Codes Cheat Sheet](https://httpstatuses.com/) - Quick reference
- 🧪 [JSONPlaceholder](https://jsonplaceholder.typicode.com/) - Free fake API for practice
- 💬 [API Best Practices](https://stackoverflow.blog/2020/03/02/best-practices-for-rest-api-design/) - Stack Overflow Blog

---

## 📖 Table of Contents

- [📘 General Usage Guide](#general-api-usage-guide)
- [🐶 Animals](#animals)
- [🌸 Anime](#anime)
- [🛡️ Anti-Malware](#anti-malware)
- [🔐 Authentication & Identity](#authentication-identity)
- [📚 Books & Literature](#books)
- [⛓️ Blockchain & Web3](#blockchain-web3)
- [🪙 Cryptocurrency](#cryptocurrency)
- [☁️ Cloud Storage & Files](#cloud-storage-files)
- [💻 Development](#development)
- [⚙️ Continuous Integration](#continuous-integration)
- [📝 Text Analysis & NLP](#text-analysis-nlp)
- [🏠 IoT & Smart Devices](#iot-smart-devices)
- [🔓 Open Source Projects](#open-source-projects)
- [📖 Dictionaries](#dictionaries)
- [🎓 Education](#education)
- [📅 Calendar & Holidays](#calendar-holidays)
- [📊 Public Data & Datasets](#public-data)
- [📧 Email & SMS](#email-sms)
- [📱 Phone & Telephony](#phone-telephony)
- [🎮 Entertainment](#entertainment)
- [🎪 Events](#events)
- [🎙️ Podcasts](#podcasts)
- [💭 Personality & Quotes](#personality-quotes)
- [💰 Finance](#finance)
- [💱 Currency Exchange](#currency-exchange)
- [🍔 Food & Drink](#food-drink)
- [🎮 Games & Comics](#games-comics)
- [🌍 Geocoding](#geocoding)
- [❤️ Health](#health)
- [🧠 Machine Learning](#machine-learning)
- [🧪 Mock Data & Testing](#mock-data-testing)
- [🎵 Music](#music)
- [📰 News](#news)
- [📸 Photography](#photography)
- [🔬 Science](#science)
- [🔒 Security & Validation](#security-validation)
- [✅ Data Validation](#data-validation)
- [🛍️ Shopping](#shopping)
- [🔧 Utilities & Tools](#utilities-tools)
- [🔗 URL Shorteners](#url-shorteners)
- [💬 Social](#social)
- [⚽ Sports](#sports)
- [🎨 Design & Colors](#design-colors)
- [🌎 Geography & Countries](#geography-countries)
- [🚆 Transportation](#transportation)
- [📦 Tracking & Logistics](#tracking-logistics)
- [🌿 Environment & Climate](#environment-climate)
- [🏛️ Government & Civic](#government-civic)
- [📹 Video](#video)
- [🔢 Math & Computation](#math-computation)
- [⚠️ Unofficial & Community APIs](#unofficial-community)
- [😂 Memes & Fun](#memes-fun)
- [💼 Jobs & Career](#jobs-career)
- [🌤️ Weather](#weather)
- [💼 Business](#business)
- [📄 Documents & Productivity](#documents-productivity)
- [👤 Demographic Analysis](#demographic-analysis)
- [🏛️ Museums & Art](#museums-art)
- [📈 Monitoring & Observability](#monitoring-observability)

---

## <a id="animals"></a>🐶 Animals

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **AdoptAPet** | Resource to help get pets adopted. | 🔑 ApiKey | ✅ | [Link](https://www.adoptapet.com/public/apis/pet_list.html) |
| **Axolotl** | Collection of axolotl pictures and facts. | No | ✅ | [Link](https://theaxolotlapi.netlify.app/) |
| **Cat Facts** | Daily cat facts. | No | ✅ | [Link](https://alexwohlbruck.github.io/cat-facts/) |
| **Cataas** | Cat as a service (cats pictures and gifs). | No | ✅ | [Link](https://cataas.com/) |
| **Cats** | Pictures of cats from Tumblr. | 🔑 ApiKey | ✅ | [Link](https://docs.thecatapi.com/) |
| **Dog API v2** | Dog breeds and image endpoints for apps and bots. | No | ✅ | [Link](https://dogapi.dog/docs/api-v2) |
| **Dog CEO** | Dog breeds and random dog images. | No | ✅ | [Link](https://dog.ceo/dog-api/) |
| **Dog Facts** | Random dog facts. | No | ✅ | [Link](https://dukengn.github.io/Dog-facts-API/) |
| **eBird** | Retrieve recent or notable birding observations within a region. | 🔑 ApiKey | ✅ | [Link](https://documenter.getpostman.com/view/664302/S1ENwy59) |
| **FishWatch** | Information and pictures about individual fish species. | No | ✅ | [Link](https://www.fishwatch.gov/developers) |
| **HTTP Cat** | Cat for every HTTP Status. | No | ✅ | [Link](https://http.cat/) |
| **HTTP Dog** | Dogs for every HTTP response status code. | No | ✅ | [Link](https://http.dog/) |
| **IUCN** | IUCN Red List of Threatened Species. | 🔑 ApiKey | No | [Link](http://apiv3.iucnredlist.org/api/v3/docs) |
| **PlaceBear** | Placeholder bear pictures. | No | ✅ | [Link](https://placebear.com/) |
| **PlaceDog** | Placeholder Dog pictures. | No | ✅ | [Link](https://place.dog) |
| **RandomDog** | Random pictures of dogs. | No | ✅ | [Link](https://random.dog/woof.json) |
| **RandomDuck** | Random pictures of ducks. | No | ✅ | [Link](https://random-d.uk/api) |
| **RandomFox** | Random pictures of foxes. | No | ✅ | [Link](https://randomfox.ca/floof/) |
| **RescueGroups** | Adoption. | No | ✅ | [Link](https://userguide.rescuegroups.org/display/APIDG/API+Developers+Guide+Home) |
| **Shibe.Online** | Random pictures of Shiba Inu, cats or birds. | No | ✅ | [Link](http://shibe.online/) |
| **The Cat API** | Images of cats (great for testing image grids). | 🔑 ApiKey | ✅ | [Link](https://thecatapi.com/) |
| **The Dog API** | Images and data about dogs. | 🔑 ApiKey | ✅ | [Link](https://thedogapi.com/) |
| **TheCatDB** | Cat breeds and facts database. | 🔑 ApiKey | ✅ | [Link](https://www.thecatapi.com/) |
| **WoRMS** | Marine species taxonomy and classification data. | No | ✅ | [Link](https://www.marinespecies.org/rest/) |
| **xeno-canto** | Bird sounds from around the world. | No | ✅ | [Link](https://xeno-canto.org/explore/api) |
| **TheCatAPI** | Random cat images, breeds, and facts. | 🔑 ApiKey | ✅ | [Link](https://api.thecatapi.com/) |
| **TheDogAPI** | Random dog images, breeds, and facts. | 🔑 ApiKey | ✅ | [Link](https://api.thedogapi.com/) |


[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="anime"></a>🌸 Anime

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **AniAPI** | Anime discovery, streaming & syncing with trackers. | 🔐 OAuth | ✅ | [Link](https://aniapi.com/docs/) |
| **AniDB** | Anime Database. | 🔑 ApiKey | No | [Link](https://wiki.anidb.net/HTTP_API_Definition) |
| **AniList** | GraphQL anime and manga database (**No Auth**). | No | ✅ | [Link](https://anilist.gitbook.io/anilist-apiv2-docs/) |
| **AnimeChan** | Random anime quotes (**No Auth**). | No | ✅ | [Link](https://animechan.xyz/docs) |
| **AnimeFacts** | Anime facts (over 100+). | No | ✅ | [Link](https://chandan-02.github.io/anime-facts-rest-api/) |
| **AnimeNewsNetwork** | Anime industry news. | No | ✅ | [Link](https://www.animenewsnetwork.com/encyclopedia/api.php) |
| **Catboy** | Neko images, funny GIFs & more. | No | ✅ | [Link](https://catboys.com/api) |
| **Danbooru Anime** | Thousands of anime artist database. | 🔑 ApiKey | ✅ | [Link](https://danbooru.donmai.us/wiki_pages/help:api) |
| **Jikan** | Unofficial MyAnimeList API. | No | ✅ | [Link](https://jikan.moe) |
| **Kitsu** | Anime and Manga Database. | 🔐 OAuth | ✅ | [Link](https://kitsu.docs.apiary.io/) |
| **Kitsu Anime** | Discover anime and manga (**No Auth**). | No | ✅ | [Link](https://kitsu.docs.apiary.io/#) |
| **MangaDex** | Manga catalog, chapters, and covers (**No Auth**). | No | ✅ | [Link](https://api.mangadex.org/docs/) |
| **Mangapi** | Translate manga pages. | 🔑 ApiKey | ✅ | [Link](https://rapidapi.com/pierre.carcellermeunier/api/mangapi3/) |
| **NekosBest** | Neko Images & Anime GIFs. | No | ✅ | [Link](https://docs.nekos.best) |
| **Shikimori** | Anime and Manga Database. | 🔐 OAuth | ✅ | [Link](https://shikimori.one/api/doc) |
| **Studio Ghibli** | Resources from Studio Ghibli films. | No | ✅ | [Link](https://ghibliapi.vercel.app) |
| **Trace Moe** | Anime Scene Search Engine. | No | ✅ | [Link](https://soruly.github.io/trace.moe-api/#/) |
| **Waifu.im** | API for serving anime images (versatile query options). | No | ✅ | [Link](https://waifu.im/) |
| **Waifu.pics** | Image sharing platform for anime images. | No | ✅ | [Link](https://waifu.pics/docs) |



[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="anti-malware"></a>🛡️ Anti-Malware

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **AbuseIPDB** | IP/Domain/URL reputation. | 🔑 ApiKey | ✅ | [Link](https://docs.abuseipdb.com/) |
| **AlienVault OTX** | IP/Domain/URL reputation. | 🔑 ApiKey | ✅ | [Link](https://otx.alienvault.com/api) |
| **CAPEsandbox** | Malware analysis. | 🔑 ApiKey | ✅ | [Link](https://capev2.readthedocs.io/en/latest/usage/api.html) |
| **Google Safe Browsing** | Google Link/Domain reputation. | 🔑 ApiKey | ✅ | [Link](https://developers.google.com/safe-browsing/) |
| **Hybrid Analysis** | Malware sample lookup and sandbox reports. | 🔑 ApiKey | ✅ | [Link](https://www.hybrid-analysis.com/docs/api/v2) |
| **MalShare** | Malware analysis. | 🔑 ApiKey | ✅ | [Link](https://malshare.com/doc.php) |
| **MalwareBazaar** | Malware analysis. | 🔑 ApiKey | ✅ | [Link](https://bazaar.abuse.ch/api/) |
| **ThreatFox** | IOC database (malware C2, URLs, hashes) from abuse.ch. | No | ✅ | [Link](https://threatfox.abuse.ch/api/) |
| **NoPhishy** | Link/Domain reputation. | 🔑 ApiKey | ✅ | [Link](https://rapidapi.com/Amiichu/api/exerra-phishing-check/) |
| **PhishTank** | Community phishing URL database and reputation (Cisco Talos). | 🔑 ApiKey | ✅ | [Link](https://phishtank.org/api_info.php) |
| **Scanii** | File/Link/Domain reputation. | 🔑 ApiKey | ✅ | [Link](https://docs.scanii.com/) |
| **URLhaus** | Link/Domain reputation. | No | ✅ | [Link](https://urlhaus-api.abuse.ch/) |
| **URLScan.io** | Link/Domain reputation. | 🔑 ApiKey | ✅ | [Link](https://urlscan.io/about-api/) |
| **VirusTotal** | File/URL analysis. | 🔑 ApiKey | ✅ | [Link](https://www.virustotal.com/en/documentation/public-api/) |
| **Web of Trust** | IP/Domain/URL reputation. | 🔑 ApiKey | ✅ | [Link](https://support.mywot.com/hc/en-us/sections/360004477734-API-) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="authentication-identity"></a>🔐 Authentication & Identity

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Descope** | Customer identity and authentication flows. | 🔑 ApiKey | ✅ | [Link](https://docs.descope.com/api/) |
| **Frontegg** | Authentication, user management, and multi-tenant identity. | 🔑 ApiKey | ✅ | [Link](https://developers.frontegg.com/) |
| **FusionAuth** | Identity and access management platform. | 🔑 ApiKey | ✅ | [Link](https://fusionauth.io/docs/apis/) |
| **GetOTP** | OTP verification and passwordless login APIs. | 🔑 ApiKey | ✅ | [Link](https://otp.dev/en/docs/) |
| **Keycloak** | Open-source identity and access management APIs. | No | ✅ | [Link](https://www.keycloak.org/docs-api/latest/rest-api/index.html) |
| **Kinde** | Authentication platform for modern apps. | 🔐 OAuth | ✅ | [Link](https://kinde.com/docs/developer-tools/) |
| **Logto** | Open-source auth infrastructure and identity APIs. | 🔑 ApiKey | ✅ | [Link](https://docs.logto.io/) |
| **Magic** | Passwordless authentication and wallet login. | 🔑 ApiKey | ✅ | [Link](https://magic.link/docs/api) |
| **Micro User Service** | User management and authentication. | 🔑 ApiKey | ✅ | [Link](https://m3o.com/user) |
| **MojoAuth** | Passwordless authentication API and OTP flows. | 🔑 ApiKey | ✅ | [Link](https://mojoauth.com/docs/api) |
| **Ory** | Identity, session, and authorization APIs. | No | ✅ | [Link](https://www.ory.sh/docs/reference/api) |
| **Permit.io** | Authorization and policy management APIs for RBAC/ABAC. | 🔑 ApiKey | ✅ | [Link](https://docs.permit.io/) |
| **Stytch** | Authentication APIs for passwords, OTP, magic links, and OAuth. | 🔑 ApiKey | ✅ | [Link](https://stytch.com/docs/api) |
| **SuperTokens** | Open-source auth solution for session and user management. | No | ✅ | [Link](https://supertokens.com/docs) |
| **WorkOS** | Enterprise SSO, SCIM, and user management APIs. | 🔑 ApiKey | ✅ | [Link](https://workos.com/docs/reference) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="books"></a>📚 Books & Literature

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **A Bíblia Digital** | Do not worry about managing the multiple versions of the Bible. | 🔑 ApiKey | ✅ | [Link](https://www.abibliadigital.com.br/en) |
| **Bhagavad Gita** | Open Source Shrimad Bhagavad Gita API including 21+ authors translation in Sa... | 🔑 ApiKey | ✅ | [Link](https://docs.bhagavadgitaapi.in) |
| **Bhagavad Gita telugu** | Bhagavad Gita API in telugu and odia languages. | No | ✅ | [Link](https://gita-api.vercel.app) |
| **Bible API** | Free Bible text in multiple versions (**No Auth**). | No | ✅ | [Link](https://bible-api.com/) |
| **Bookcover** | Book cover images by ISBN (**No Auth**). | No | ✅ | [Link](http://openlibrary.org/dev/docs/api/covers) |
| **Ganjoor** | Classic Persian poetry works including access to related manuscripts, recitat... | 🔐 OAuth | ✅ | [Link](https://api.ganjoor.net) |
| **Goodreads** | Book reviews and ratings metadata. | 🔑 ApiKey | ✅ | [Link](https://www.goodreads.com/api) |
| **Google Books** | Search and preview books. | 🔐 OAuth | ✅ | [Link](https://developers.google.com/books/) |
| **ISBNdb** | ISBN book database. | 🔑 ApiKey | ✅ | [Link](https://isbndb.com/apidocs/v2) |
| **Open Library** | Fetch data about millions of books and covers. | No | ✅ | [Link](https://openlibrary.org/developers/api) |
| **Penguin Publishing** | Book data. | No | ✅ | [Link](http://www.penguinrandomhouse.biz/webservices/rest/) |
| **Quran** | RESTful Quran API with multiple languages. | No | ✅ | [Link](https://quran.api-docs.io/) |
| **Quran Cloud** | Quran text, translations, and recitations. | No | ✅ | [Link](https://alquran.cloud/api) |
| **The Bible API** | Bible metadata and translations for apps. | 🔑 ApiKey | ✅ | [Link](https://docs.api.bible) |
| **Thirukkural** | 1330 Thirukkural poems and explanation in Tamil and English. | No | ✅ | [Link](https://api-thirukkural.web.app/) |
| **Wolne Lektury** | API for obtaining information about e-books available on the WolneLektury.pl ... | No | ✅ | [Link](https://wolnelektury.pl/api/) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="blockchain-web3"></a>⛓️ Blockchain & Web3

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Ankr RPC** | Multi-chain RPC infrastructure for Web3 apps. | 🔑 ApiKey | ✅ | [Link](https://www.ankr.com/rpc/) |
| **Bitquery** | Onchain GraphQL APIs & DEX APIs. | 🔑 ApiKey | ✅ | [Link](https://graphql.bitquery.io/ide) |
| **BlockCypher** | Blockchain data APIs for Bitcoin, Litecoin, Dogecoin, and Dash. | 🔑 ApiKey | ✅ | [Link](https://www.blockcypher.com/dev/bitcoin/) |
| **BscScan** | BNB Chain explorer and contract data APIs. | 🔑 ApiKey | ✅ | [Link](https://bscscan.com/apis) |
| **Chainbase** | Unified blockchain data API across multiple chains. | 🔑 ApiKey | ✅ | [Link](https://docs.chainbase.com/) |
| **Chainlink** | Developer resources for decentralized oracle data. | No | ✅ | [Link](https://chain.link/developer-resources) |
| **Chainpoint** | Chainpoint is a global network for anchoring data to the Bitcoin blockchain. | No | ✅ | [Link](https://tierion.com/chainpoint/) |
| **GoldRush (Covalent)** | Multichain data APIs for blockchain transaction and token data. | 🔑 ApiKey | ✅ | [Link](https://goldrush.dev/) |
| **dRPC** | Distributed RPC provider for EVM and non-EVM chains. | 🔑 ApiKey | ✅ | [Link](https://drpc.org/docs) |
| **Etherscan** | Ethereum explorer and smart contract data APIs. | 🔑 ApiKey | ✅ | [Link](https://docs.etherscan.io/) |
| **FreeRPC** | Free public RPC endpoints for many blockchains. | No | ✅ | [Link](https://www.freerpc.com/) |
| **GetBlock** | Blockchain node infrastructure via unified API. | 🔑 ApiKey | ✅ | [Link](https://getblock.io/) |
| **Helium** | Helium is a global, distributed network of Hotspots that create public, long-... | No | ✅ | [Link](https://docs.helium.com/api/blockchain/introduction/) |
| **Helius** | Solana infrastructure APIs for transactions, NFTs, and webhooks. | 🔑 ApiKey | ✅ | [Link](https://docs.helius.dev/) |
| **Infura** | Scalable Ethereum, IPFS, and Web3 APIs. | 🔑 ApiKey | ✅ | [Link](https://docs.infura.io/) |
| **Nownodes** | Multi-chain RPC and blockchain access APIs. | 🔑 ApiKey | ✅ | [Link](https://nownodes.io/) |
| **QuickNode** | Multi-chain RPC infrastructure and blockchain APIs. | 🔑 ApiKey | ✅ | [Link](https://www.quicknode.com/docs) |
| **Solscan** | Solana data APIs for addresses, tokens, and transactions. | 🔑 ApiKey | ✅ | [Link](https://pro-api.solscan.io/pro-api-docs/v2.0) |
| **Steem** | Blockchain-based blogging and social media website. | No | No | [Link](https://developers.steem.io/) |
| **Tatum** | Blockchain infrastructure and wallet APIs for many chains. | 🔑 ApiKey | ✅ | [Link](https://apidoc.tatum.io/) |
| **The Graph** | GraphQL indexing protocol for querying blockchain data. | 🔑 ApiKey | ✅ | [Link](https://thegraph.com/docs/en/subgraphs/querying/introduction/) |
| **thirdweb** | Developer tooling APIs for smart contracts and wallets. | 🔑 ApiKey | ✅ | [Link](https://portal.thirdweb.com/typescript/v5) |
| **Watchdata** | Multi-chain wallet, NFT, and node APIs. | 🔑 ApiKey | ✅ | [Link](https://docs.watchdata.io/) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="cryptocurrency"></a>🪙 Cryptocurrency

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **1inch** | API for querying the 1inch protocol. | No | ✅ | [Link](https://1inch.io/api/) |
| **Alchemy** | Ethereum API. | 🔑 ApiKey | ✅ | [Link](https://docs.alchemy.com/) |
| **Bitcambio** | Get the list of all traded assets in the exchange. | No | ✅ | [Link](https://nova.bitcambio.com.br/api/v3/docs#a-public) |
| **Bitfinex** | Exchange for Trading Cryptocurrencies. | 🔑 ApiKey | ✅ | [Link](https://docs.bitfinex.com/docs) |
| **Bitmex** | Exchange for Trading Cryptocurrencies. | 🔑 ApiKey | ✅ | [Link](https://www.bitmex.com/app/apiOverview) |
| **Block** | Bitcoin Payment, Wallet & Transaction Data. | 🔑 ApiKey | ✅ | [Link](https://block.io/docs/basic) |
| **Blockchain** | Bitcoin Payment, Wallet & Transaction Data. | 🔑 ApiKey | ✅ | [Link](https://www.blockchain.com/api) |
| **blockfrost Cardano** | Interaction with the Cardano mainnet and several testnets. | 🔑 ApiKey | ✅ | [Link](https://blockfrost.io/) |
| **Brave NewCoin** | Real-time and historic crypto data from more than 200+ exchanges. | 🔑 ApiKey | ✅ | [Link](https://bravenewcoin.com/developers) |
| **BtcTurk** | Real-time cryptocurrency data, graphs and API that allows buy&sell. | 🔑 ApiKey | ✅ | [Link](https://docs.btcturk.com/) |
| **CoinAPI** | Market Data API. | 🔑 ApiKey | ✅ | [Link](https://docs.coinapi.io/) |
| **Coinbase** | Bitcoin, Bitcoin Cash, Litecoin and Ethereum. | 🔑 ApiKey | ✅ | [Link](https://developers.coinbase.com) |
| **Coinbase Pro** | Cryptocurrency Trading Platform. | 🔑 ApiKey | ✅ | [Link](https://docs.pro.coinbase.com/#api) |
| **CoinCap** | Real-time cryptocurrency market data (**No Auth**). | No | ✅ | [Link](https://docs.coincap.io/) |
| **CoinDCX** | Cryptocurrency Trading Platform. | 🔑 ApiKey | ✅ | [Link](https://docs.coindcx.com/) |
| **CoinGecko** | Cryptocurrency prices, market cap, exchange rates. | No | ✅ | [Link](http://www.coingecko.com/api) |
| **Coinigy** | Interacting with Coinigy Accounts and Exchange Directly. | 🔑 ApiKey | ✅ | [Link](https://coinigy.docs.apiary.io) |
| **Coinlayer** | Real-time Crypto Exchange Rates. | 🔑 ApiKey | ✅ | [Link](https://coinlayer.com) |
| **Coinlore** | Cryptocurrency prices and market data (**No Auth**). | No | ✅ | [Link](https://www.coinlore.com/cryptocurrency-data-api) |
| **CoinMarketCap** | Cryptocurrency prices, market cap, exchange rates. | 🔑 ApiKey | ✅ | [Link](https://coinmarketcap.com/api/) |
| **CoinPaprika** | Cryptocurrency market data (**No Auth, generous limits**). | No | ✅ | [Link](https://api.coinpaprika.com/) |
| **CoinRanking** | Live Cryptocurrency data. | 🔑 ApiKey | ✅ | [Link](https://developers.coinranking.com/api/documentation) |
| **Coinremitter** | Cryptocurrencies Payment & Prices. | 🔑 ApiKey | ✅ | [Link](https://coinremitter.com/docs) |
| **CoinStats** | Crypto Tracker. | No | ✅ | [Link](https://documenter.getpostman.com/view/5734027/RzZ6Hzr3?version=latest) |
| **CryptAPI** | Cryptocurrency Payment Processor. | No | ✅ | [Link](https://docs.cryptapi.io/) |
| **CryptoCompare** | Cryptocurrencies Comparison. | No | ✅ | [Link](https://www.cryptocompare.com/api) |
| **dYdX** | Decentralized cryptocurrency exchange. | 🔑 ApiKey | ✅ | [Link](https://docs.dydx.exchange/) |
| **EXMO** | Cryptocurrencies exchange based in UK. | 🔑 ApiKey | ✅ | [Link](https://documenter.getpostman.com/view/10287440/SzYXWKPi) |
| **Gateio** | Exchange for Trading Cryptocurrencies. | 🔑 ApiKey | ✅ | [Link](https://www.gate.io/api2) |
| **Gemini** | Exchange for Trading Cryptocurrencies. | No | ✅ | [Link](https://docs.gemini.com/rest-api/) |
| **Hirak Exchange Rates** | Exchange rates between 162 currency & 300 crypto currency update each 5 min, ... | 🔑 ApiKey | ✅ | [Link](https://rates.hirak.site/) |
| **Huobi** | Seychelles based cryptocurrency exchange. | 🔑 ApiKey | ✅ | [Link](https://huobiapi.github.io/docs/spot/v1/en/) |
| **icy.tools** | GraphQL based NFT API. | 🔑 ApiKey | ✅ | [Link](https://developers.icy.tools/) |
| **INFURA Ethereum** | Interaction with the Ethereum mainnet and several testnets. | 🔑 ApiKey | ✅ | [Link](https://infura.io/product/ethereum) |
| **Kraken** | Exchange for Trading Cryptocurrencies. | 🔑 ApiKey | ✅ | [Link](https://docs.kraken.com/rest/) |
| **KuCoin** | Exchange for Trading Cryptocurrencies. | 🔑 ApiKey | ✅ | [Link](https://docs.kucoin.com/) |
| **Mempool** | Bitcoin API. | No | ✅ | [Link](https://mempool.space/api) |
| **MercadoBitcoin** | Brazilian Cryptocurrency Information. | No | ✅ | [Link](https://api.mercadobitcoin.net/api/v4/docs) |
| **Messari** | Crypto research and data. | 🔑 ApiKey | ✅ | [Link](https://messari.io/api) |
| **Mobula** | On-chain crypto data and wallet analytics. | 🔑 ApiKey | ✅ | [Link](https://docs.mobula.io/) |
| **Moralis** | Web3 wallet, NFT, and DeFi data. | 🔑 ApiKey | ✅ | [Link](https://docs.moralis.io/) |
| **Nexchange** | Automated cryptocurrency exchange service. | No | No | [Link](https://nexchange2.docs.apiary.io/) |
| **NovaDax** | NovaDAX API to access all market data, trading management endpoints. | 🔑 ApiKey | ✅ | [Link](https://doc.novadax.com/en-US/#introduction) |
| **Poloniex** | Exchange for Trading Cryptocurrencies. | 🔑 ApiKey | ✅ | [Link](https://docs.poloniex.com) |
| **Solana JSON RPC** | Provides various endpoints to interact with the Solana Blockchain. | No | ✅ | [Link](https://docs.solana.com/developing/clients/jsonrpc-api) |
| **Technical Analysis** | Cryptocurrency prices and technical analysis. | 🔑 ApiKey | ✅ | [Link](https://technical-analysis-api.com) |
| **VALR** | Cryptocurrency Exchange based in South Africa. | 🔑 ApiKey | ✅ | [Link](https://docs.valr.com/) |
| **WorldCoinIndex** | Cryptocurrencies Prices. | 🔑 ApiKey | ✅ | [Link](https://www.worldcoinindex.com/apiservice) |
| **ZMOK** | Ethereum JSON RPC API and Web3 provider. | No | ✅ | [Link](https://zmok.io) |


[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="cloud-storage-files"></a>☁️ Cloud Storage & Files

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Backblaze B2** | Cloud object storage API with S3-compatible endpoints. | 🔑 ApiKey | ✅ | [Link](https://www.backblaze.com/apidocs/introduction-to-the-s3-compatible-api) |
| **Box** | Cloud content management and file storage API. | 🔐 OAuth | ✅ | [Link](https://developer.box.com/reference/) |
| **Cloudflare R2** | S3-compatible object storage API without egress fees. | 🔑 ApiKey | ✅ | [Link](https://developers.cloudflare.com/r2/api/s3/api/) |
| **ddownload** | File Sharing and Storage. | 🔑 ApiKey | ✅ | [Link](https://ddownload.com/api) |
| **Dropbox** | File storage and sharing APIs. | 🔐 OAuth | ✅ | [Link](https://www.dropbox.com/developers/documentation/http/documentation) |
| **File.io** | Super simple file sharing, convenient, anonymous and secure. | No | ✅ | [Link](https://www.file.io) |
| **Filebase** | S3-compatible object storage backed by decentralized networks. | 🔑 ApiKey | ✅ | [Link](https://docs.filebase.com/api-documentation) |
| **Filestack** | File uploads, processing, and content delivery APIs. | 🔑 ApiKey | ✅ | [Link](https://www.filestack.com/docs/api/) |
| **GoFile** | File hosting and management APIs. | 🔑 ApiKey | ✅ | [Link](https://gofile.io/api) |
| **Google Drive** | File storage, sharing, and metadata APIs. | 🔐 OAuth | ✅ | [Link](https://developers.google.com/drive/api) |
| **Gyazo** | Image upload and screenshot APIs. | 🔑 ApiKey | ✅ | [Link](https://gyazo.com/api/docs) |
| **ImageKit** | Image and media upload, optimization, and delivery APIs. | 🔑 ApiKey | ✅ | [Link](https://imagekit.io/docs/api-reference/) |
| **ImgBB** | Simple image upload API with free tier. | 🔑 ApiKey | ✅ | [Link](https://api.imgbb.com/) |
| **OneDrive** | File Sharing and Storage. | 🔐 OAuth | ✅ | [Link](https://developer.microsoft.com/onedrive) |
| **OneDrive (Microsoft Graph)** | OneDrive file and folder APIs via Microsoft Graph. | 🔐 OAuth | ✅ | [Link](https://learn.microsoft.com/en-us/graph/api/resources/onedrive) |
| **Pantry** | Free JSON storage for small projects. | No | ✅ | [Link](https://getpantry.cloud/) |
| **Pastebin** | Plain Text Storage. | 🔑 ApiKey | ✅ | [Link](https://pastebin.com/doc_api) |
| **Pinata** | IPFS pinning and decentralized file storage APIs. | 🔑 ApiKey | ✅ | [Link](https://docs.pinata.cloud/) |
| **Quip** | File Sharing and Storage for groups. | 🔑 ApiKey | ✅ | [Link](https://quip.com/dev/automation/documentation) |
| **Storj** | Decentralized cloud object storage APIs. | 🔑 ApiKey | ✅ | [Link](https://docs.storj.io/) |
| **The Null Pointer** | No-bullshit file hosting and URL shortening service. | No | ✅ | [Link](https://0x0.st) |
| **Uploadcare** | File uploads, media processing, and delivery APIs. | 🔑 ApiKey | ✅ | [Link](https://uploadcare.com/docs/api_reference/) |
| **UploadThing** | File upload infrastructure for modern web apps. | 🔑 ApiKey | ✅ | [Link](https://docs.uploadthing.com/) |
| **Web3 Storage** | File Sharing and Storage for Free with 1TB Space. | 🔑 ApiKey | ✅ | [Link](https://web3.storage/) |
| **Web3.Storage** | Decentralized storage API built on IPFS/Filecoin. | 🔑 ApiKey | ✅ | [Link](https://web3.storage/docs/) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="development"></a>💻 Development

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **24 Pull Requests** | Project to promote open source collaboration during December. | No | ✅ | [Link](https://24pullrequests.com/api) |
| **Abstract API** | Suite of useful APIs (IP geolocation, holidays, exchange rates). | 🔑 ApiKey | ✅ | [Link](https://www.abstractapi.com/) |
| **Abstract Screenshot** | Take a screenshot of any website. | 🔑 ApiKey | ✅ | [Link](https://www.abstractapi.com/website-screenshot-api) |
| **Agify.io** | Predict the age of a person based on their name. | No | ✅ | [Link](https://agify.io) |
| **Airtable** | API for cloud collaboration database (free tier available). | 🔑 ApiKey | ✅ | [Link](https://airtable.com/developers/web/api/introduction) |
| **Apache Superset** | Dashboarding and query platform APIs. | 🔑 ApiKey | ✅ | [Link](https://superset.apache.org/docs/api/) |
| **API Grátis** | Multiples services and public APIs. | No | ✅ | [Link](https://apigratis.com.br/) |
| **ApicAgent** | Extract device details from user-agent string. | No | ✅ | [Link](https://www.apicagent.com) |
| **ApiFlash** | Chrome based screenshot API. | 🔑 ApiKey | ✅ | [Link](https://apiflash.com/) |
| **APILayer** | Marketplace for various APIs. | 🔑 ApiKey | ✅ | [Link](https://apilayer.com/) |
| **APIs.guru** | Wikipedia for Web APIs. | No | ✅ | [Link](https://apis.guru/api-doc/) |
| **Appwrite** | Open source backend server (database, auth, storage, functions). | 🔑 ApiKey | ✅ | [Link](https://appwrite.io/docs) |
| **Auth0** | Authentication and authorization platform (free tier). | 🔐 OAuth | ✅ | [Link](https://auth0.com/docs/api) |
| **Aviationstack** | Real-time flight status and global aviation data. | 🔑 ApiKey | ✅ | [Link](https://aviationstack.com/) |
| **Azure DevOps** | DevOps tools. | 🔑 ApiKey | ✅ | [Link](https://docs.microsoft.com/en-us/rest/api/azure/devops) |
| **Base** | Building quick backends. | 🔑 ApiKey | ✅ | [Link](https://www.base-api.io/) |
| **Bitbucket** | Git solution. | 🔐 OAuth | ✅ | [Link](https://developer.atlassian.com/bitbucket/api/2/reference/) |
| **Blagues API** | French jokes API with categories (dev, dark, global, etc.). | 🔑 ApiKey | ✅ | [Link](https://www.blagues-api.fr/) |
| **Blitapp** | Schedule screenshots of web pages and sync them to your cloud. | 🔑 ApiKey | ✅ | [Link](https://blitapp.com/api/) |
| **Browshot** | Easily make screenshots of web pages in any screen size, as any device. | 🔑 ApiKey | ✅ | [Link](https://browshot.com/api/documentation) |
| **CDNJS** | Library info. | No | ✅ | [Link](https://api.cdnjs.com/libraries/jquery) |
| **Changelogs.md** | Structured changelog metadata from open source projects. | No | ✅ | [Link](https://changelogs.md) |
| **Clerk** | User management and authentication (free tier). | 🔑 ApiKey | ✅ | [Link](https://clerk.com/docs/reference/backend-api) |
| **Cloudflare Radar** | Internet traffic, routing, and outage insights (free tier). | 🔑 ApiKey | ✅ | [Link](https://developers.cloudflare.com/radar/) |
| **Cloudinary** | Image and video management API. | 🔑 ApiKey | ✅ | [Link](https://cloudinary.com/documentation/image_upload_api_reference) |
| **Codacy** | Code quality and security analysis. | 🔑 ApiKey | ✅ | [Link](https://api.codacy.com/api/api-docs) |
| **Codeforces** | Get access to Codeforces data. | 🔑 ApiKey | ✅ | [Link](https://codeforces.com/apiHelp) |
| **CodeSandbox** | Online code editor API. | 🔑 ApiKey | ✅ | [Link](https://codesandbox.io/docs) |
| **Contentful Images** | Used to retrieve and apply transformations to images. | 🔑 ApiKey | ✅ | [Link](https://www.contentful.com/developers/docs/references/images-api/) |
| **Databricks** | Lakehouse workspace, jobs, and cluster APIs. | 🔑 ApiKey | ✅ | [Link](https://docs.databricks.com/api/workspace/introduction) |
| **DigitalOcean Status** | Status of all DigitalOcean services. | No | ✅ | [Link](https://status.digitalocean.com/api) |
| **Docker Hub** | Interact with Docker Hub. | 🔑 ApiKey | ✅ | [Link](https://docs.docker.com/docker-hub/api/latest/) |
| **DomainDb Info** | Domain name search to find all domains containing particular words/phrases/etc. | No | ✅ | [Link](https://api.domainsdb.info/) |
| **EmailJS** | Send emails directly from JavaScript (**Free tier**). | 🔑 ApiKey | ✅ | [Link](https://www.emailjs.com/docs/) |
| **ExtendsClass JSON Storage** | A simple JSON store API. | No | ✅ | [Link](https://extendsclass.com/json-storage.html) |
| **Firebase** | Google's mobile/web app development platform. | 🔑 ApiKey | ✅ | [Link](https://firebase.google.com/docs/reference/rest) |
| **Genderize.io** | Predict the gender of a person based on their name. | No | ✅ | [Link](https://genderize.io) |
| **Ghost** | Get Published content into your Website, App or other embedded media. | 🔑 ApiKey | ✅ | [Link](https://ghost.org/) |
| **GitHub** | Make use of GitHub data. | 🔐 OAuth | ✅ | [Link](https://docs.github.com/en/free-pro-team@latest/rest) |
| **Gitlab** | Automate GitLab. | 🔐 OAuth | ✅ | [Link](https://docs.gitlab.com/ee/api/) |
| **Glitterly** | Image generation API. | 🔑 ApiKey | ✅ | [Link](https://developers.glitterly.app) |
| **Google Calendar** | Create, view, or update calendar events. | 🔐 OAuth | ✅ | [Link](https://developers.google.com/calendar/api) |
| **Google Docs** | Create and edit documents. | 🔐 OAuth | ✅ | [Link](https://developers.google.com/docs/api/reference/rest) |
| **Google Firebase** | Google's mobile application development platform that helps build, improve, a... | 🔑 ApiKey | ✅ | [Link](https://firebase.google.com/docs) |
| **Google Fonts** | Metadata for all families served by Google Fonts. | 🔑 ApiKey | ✅ | [Link](https://developers.google.com/fonts/docs/developer_api) |
| **Google Keep** | API to read, write, and format Google Keep notes. | 🔐 OAuth | ✅ | [Link](https://developers.google.com/keep/api/reference/rest) |
| **Google Sheets** | Read and write to Google Sheets. | 🔐 OAuth | ✅ | [Link](https://developers.google.com/sheets/api/reference/rest) |
| **Google Slides** | API to read, write, and format Google Slides presentations. | 🔐 OAuth | ✅ | [Link](https://developers.google.com/slides/api/reference/rest) |
| **Gorest** | Online REST API for Testing and Prototyping. | 🔐 OAuth | ✅ | [Link](https://gorest.co.in/) |
| **Hackerearth** | For compiling and running code in several languages. | 🔑 ApiKey | ✅ | [Link](https://www.hackerearth.com/docs/wiki/developers/v4/) |
| **Hasura** | GraphQL and REST API Engine with built in Authorization. | 🔑 ApiKey | ✅ | [Link](https://hasura.io/opensource/) |
| **Heroku** | PaaS. | 🔐 OAuth | ✅ | [Link](https://devcenter.heroku.com/articles/platform-api-reference/) |
| **host-t.com** | Basic DNS query via HTTP GET request. | No | ✅ | [Link](https://host-t.com) |
| **Host.io** | Domains Data. | 🔑 ApiKey | ✅ | [Link](https://host.io) |
| **HTTP2.Pro** | Test endpoints for client and server HTTP/2 protocol support. | No | ✅ | [Link](https://http2.pro/doc/api) |
| **Hunter** | Email Verifier. | 🔑 ApiKey | ✅ | [Link](https://hunter.io/api) |
| **IBM Text to Speech** | Convert text to speech. | 🔑 ApiKey | ✅ | [Link](https://cloud.ibm.com/docs/text-to-speech/getting-started.html) |
| **Icanhazepoch** | Get Epoch time. | No | ✅ | [Link](https://icanhazepoch.com) |
| **Icanhazip** | IP Address API. | No | ✅ | [Link](https://major.io/icanhazip-com-faq/) |
| **Image-Charts** | Generate charts, QR codes and graph images. | No | ✅ | [Link](https://documentation.image-charts.com/) |
| **import.io** | Retrieve structured data from a website or RSS feed. | 🔑 ApiKey | ✅ | [Link](http://api.docs.import.io/) |
| **Instatus** | Status page and incident management API. | 🔑 ApiKey | ✅ | [Link](https://instatus.com/help/api) |
| **ip-fast.com** | IP address, country and city. | No | ✅ | [Link](https://ip-fast.com/docs/) |
| **IP2Location** | IP geolocation database (**Free tier**). | 🔑 ApiKey | ✅ | [Link](https://www.ip2location.com/web-service/ip2location) |
| **IP2WHOIS Information Lookup** | WHOIS domain name lookup. | 🔑 ApiKey | ✅ | [Link](https://www.ip2whois.com/) |
| **ipfind.io** | Geographic location of an IP address or any domain name along with some other... | 🔑 ApiKey | ✅ | [Link](https://ipfind.io) |
| **IPGeolocation** | IP geolocation and timezone API (**Free tier: 30k/month**). | 🔑 ApiKey | ✅ | [Link](https://ipgeolocation.io/) |
| **IPinfo** | IP Address Information. | No | ✅ | [Link](https://ipinfo.io/developers) |
| **Ipstack** | Locate and identify website visitors by IP address. | 🔑 ApiKey | ✅ | [Link](https://ipstack.com/) |
| **JSON 2 JSONP** | Convert JSON to JSONP (on-the-fly) for easy cross-domain data requests using ... | No | ✅ | [Link](https://json2jsonp.com/) |
| **JSONbin.io** | Free JSON storage. | 🔑 ApiKey | ✅ | [Link](https://jsonbin.io) |
| **Judge0 CE** | Online code execution system. | 🔑 ApiKey | ✅ | [Link](https://ce.judge0.com/) |
| **Kroki** | Creates diagrams from textual descriptions. | No | ✅ | [Link](https://kroki.io) |
| **Logs.to** | Generate logs. | 🔑 ApiKey | ✅ | [Link](https://logs.to/) |
| **MAC address vendor lookup** | Retrieve vendor details and other information regarding a given MAC address o... | 🔑 ApiKey | ✅ | [Link](https://macaddress.io/api) |
| **Mailboxlayer** | Email verification and validation. | 🔑 ApiKey | ✅ | [Link](https://mailboxlayer.com/) |
| **Micro DB** | Simple database service. | 🔑 ApiKey | ✅ | [Link](https://m3o.com/db) |
| **Mintlify** | For programmatically generating documentation for code. | 🔑 ApiKey | ✅ | [Link](https://docs.mintlify.com) |
| **MY IP** | Get IP address information. | No | ✅ | [Link](https://www.myip.com/api-docs/) |
| **Nationalize.io** | Predict the nationality of a person based on their name. | No | ✅ | [Link](https://nationalize.io) |
| **Neon** | Serverless Postgres database (free tier). | 🔑 ApiKey | ✅ | [Link](https://neon.tech/docs/reference/api-reference) |
| **Netlify** | Netlify API. | 🔐 OAuth | ✅ | [Link](https://docs.netlify.com/api/get-started/) |
| **NetworkCalc** | Network calculators, including subnets, DNS, binary, and security tools. | No | ✅ | [Link](https://networkcalc.com/api/docs) |
| **Notion** | Access to Notion workspace data via API. | 🔐 OAuth | ✅ | [Link](https://developers.notion.com/) |
| **Novu** | Open-source notification infrastructure. | 🔑 ApiKey | ✅ | [Link](https://docs.novu.co/api-reference/overview) |
| **Numverify** | Phone number validation. | 🔑 ApiKey | ✅ | [Link](https://numverify.com/) |
| **Open Page Rank** | API for calculating and comparing metrics of different websites using Page Ra... | 🔑 ApiKey | ✅ | [Link](https://www.domcop.com/openpagerank/) |
| **OpenAPIHub** | The All-in-one API Platform. | 🔑 ApiKey | ✅ | [Link](https://hub.openapihub.com/) |
| **OpenGraphr** | Really simple API to retrieve Open Graph data from an URL. | 🔑 ApiKey | ✅ | [Link](https://opengraphr.com/docs/1.0/overview) |
| **oyyi** | API for Fake Data, image/video conversion, optimization, pdf optimization and... | No | ✅ | [Link](https://oyyi.xyz/docs/1.0) |
| **PageCDN** | Public API for javascript, css and font libraries on PageCDN. | 🔑 ApiKey | ✅ | [Link](https://pagecdn.com/docs/public-api) |
| **Pdflayer** | HTML to PDF conversion. | 🔑 ApiKey | ✅ | [Link](https://pdflayer.com/) |
| **PocketBase** | Open source backend (database, auth, files). | 🔑 ApiKey | ✅ | [Link](https://pocketbase.io/docs/api-records/) |
| **Positionstack** | Forward & Reverse Geocoding. | 🔑 ApiKey | ✅ | [Link](https://positionstack.com/) |
| **PostHog** | Open-source product analytics (free tier). | 🔑 ApiKey | ✅ | [Link](https://posthog.com/docs/api) |
| **Postman** | Tool for testing APIs. | 🔑 ApiKey | ✅ | [Link](https://www.postman.com/postman/workspace/postman-public-workspace/documentation/12959542-c8142d51-e97c-46b6-bd77-52bb66712c9a) |
| **ProxyCrawl** | Scraping and crawling anticaptcha service. | 🔑 ApiKey | ✅ | [Link](https://proxycrawl.com) |
| **ProxyKingdom** | Rotating Proxy API that produces a working proxy on every request. | 🔑 ApiKey | ✅ | [Link](https://proxykingdom.com) |
| **Pusher Beams** | Push notifications for Android & iOS. | 🔑 ApiKey | ✅ | [Link](https://pusher.com/beams) |
| **QR code** | Create an easy to read QR code and URL shortener. | No | ✅ | [Link](https://www.qrtag.net/api/) |
| **Qrcode Monkey** | Integrate custom and unique looking QR codes into your system or workflow. | No | ✅ | [Link](https://www.qrcode-monkey.com/qr-code-api-with-logo/) |
| **QuickChart** | Generate charts and QR codes. | No | ✅ | [Link](https://quickchart.io/) |
| **Railway** | Modern deployment platform API. | 🔑 ApiKey | ✅ | [Link](https://docs.railway.app/reference/public-api) |
| **Redash** | Query, dashboards, and data source automation API. | 🔑 ApiKey | ✅ | [Link](https://redash.io/help/user-guide/integrations-and-api/api) |
| **Rejax** | Reverse AJAX service to notify clients. | 🔑 ApiKey | ✅ | [Link](https://rejax.io/) |
| **Render** | Cloud platform API for apps and databases. | 🔑 ApiKey | ✅ | [Link](https://api-docs.render.com/reference/introduction) |
| **RSS feed to JSON** | Returns RSS feed in JSON format using feed URL. | No | ✅ | [Link](https://rss-to-json-serverless-api.vercel.app) |
| **SavePage.io** | A free, RESTful API used to screenshot any desktop, or mobile website. | 🔑 ApiKey | ✅ | [Link](https://www.savepage.io) |
| **ScrapeNinja** | Scraping API with Chrome fingerprint and residential proxies. | 🔑 ApiKey | ✅ | [Link](https://scrapeninja.net) |
| **ScraperApi** | Easily build scalable web scrapers. | 🔑 ApiKey | ✅ | [Link](https://www.scraperapi.com) |
| **scraperBox** | Undetectable web scraping API. | 🔑 ApiKey | ✅ | [Link](https://scraperbox.com/) |
| **scrapestack** | Real-time, Scalable Proxy & Web Scraping REST API. | 🔑 ApiKey | ✅ | [Link](https://scrapestack.com/) |
| **ScrapingAnt** | Headless Chrome scraping with a simple API. | 🔑 ApiKey | ✅ | [Link](https://scrapingant.com) |
| **ScrapingDog** | Proxy API for Web scraping. | 🔑 ApiKey | ✅ | [Link](https://www.scrapingdog.com/) |
| **ScreenshotAPI.net** | Create pixel-perfect website screenshots. | 🔑 ApiKey | ✅ | [Link](https://screenshotapi.net/) |
| **Screenshotlayer** | Website screenshots. | 🔑 ApiKey | ✅ | [Link](https://screenshotlayer.com/) |
| **Serialif Color** | Color conversion, complementary, grayscale and contrasted text. | No | ✅ | [Link](https://color.serialif.com/) |
| **Serpstack** | Real-Time Google Search Results. | 🔑 ApiKey | ✅ | [Link](https://serpstack.com/) |
| **Sheetsu** | Easy google sheets integration. | 🔑 ApiKey | ✅ | [Link](https://sheetsu.com/) |
| **SHOUTCLOUD** | ALL-CAPS AS A SERVICE. | No | No | [Link](http://shoutcloud.io/) |
| **Smartsheet** | Spreadsheet-style project management API. | 🔐 OAuth | ✅ | [Link](https://smartsheet.redoc.ly/) |
| **SonarQube** | SonarQube REST APIs to detect bugs, code smells & security vulnerabilities. | 🔐 OAuth | ✅ | [Link](https://sonarcloud.io/web_api) |
| **StackExchange** | Q&A forum for developers. | 🔐 OAuth | ✅ | [Link](https://api.stackexchange.com/) |
| **Statically** | A free CDN for developers. | No | ✅ | [Link](https://statically.io/) |
| **Supabase** | Open source Firebase alternative (database, auth, storage). | 🔑 ApiKey | ✅ | [Link](https://supabase.com/docs/guides/api) |
| **Supportivekoala** | Autogenerate images with template. | 🔑 ApiKey | ✅ | [Link](https://developers.supportivekoala.com/) |
| **Trello** | Project boards and workflow automation APIs. | 🔐 OAuth | ✅ | [Link](https://developers.trello.com/) |
| **Upstash** | Serverless Redis and Kafka (free tier). | 🔑 ApiKey | ✅ | [Link](https://upstash.com/docs/redis/overall/getstarted) |
| **Userstack** | User-Agent String Analysis. | 🔑 ApiKey | ✅ | [Link](https://userstack.com/) |
| **UUID Generator** | Generate UUIDs (v1, v3, v4, v5). | No | ✅ | [Link](https://www.uuidgenerator.net/api) |
| **Vercel** | Deployment platform API. | 🔑 ApiKey | ✅ | [Link](https://vercel.com/docs/rest-api/endpoints) |
| **Web Scraper** | Web scraping service (ScrapingBee). | 🔑 ApiKey | ✅ | [Link](https://www.scrapingbee.com/documentation/) |
| **WebScraping.AI** | Web Scraping API with built-in proxies and JS rendering. | 🔑 ApiKey | ✅ | [Link](https://webscraping.ai/) |
| **ZenRows** | Web Scraping API that bypasses anti-bot solutions while offering JS rendering... | 🔑 ApiKey | ✅ | [Link](https://www.zenrows.com/) |
| **GitHub REST API** | Access GitHub data — repos, users, gists, and more (**No Auth for public data**). | No | ✅ | [Link](https://docs.github.com/en/rest) |


| **Microlink** | Extract metadata, take screenshots, and generate PDFs from any URL. | No | ✅ | [Link](https://microlink.io/docs/api/getting-started/overview) |
| **Doppler** | Secrets management platform for developers. | 🔑 ApiKey | ✅ | [Link](https://docs.doppler.com/reference/api) |
| **Fly.io** | Global app deployment platform. | 🔑 ApiKey | ✅ | [Link](https://fly.io/docs/machines/api/) |
| **Gitea** | Self-hosted Git service with REST API. | 🔐 OAuth | ✅ | [Link](https://docs.gitea.com/api/1.20/) |
| **Linear** | Modern issue tracking for software teams. | 🔑 ApiKey | ✅ | [Link](https://developers.linear.app/docs) |
| **Turso** | SQLite-based edge database platform. | 🔑 ApiKey | ✅ | [Link](https://docs.turso.tech/) |


[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="continuous-integration"></a>⚙️ Continuous Integration

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **AppVeyor** | CI/CD builds API (free for OSS). | 🔑 ApiKey | ✅ | [Link](https://www.appveyor.com/docs/api/) |
| **Azure DevOps Health** | Resource health helps you diagnose and get support when an Azure issue impact... | 🔑 ApiKey | No | [Link](https://docs.microsoft.com/en-us/rest/api/resourcehealth) |
| **Bitrise** | Build tool and processes integrations to create efficient development pipelines. | 🔑 ApiKey | ✅ | [Link](https://api-docs.bitrise.io/) |
| **Buddy** | The fastest continuous integration and continuous delivery platform. | 🔐 OAuth | ✅ | [Link](https://buddy.works/docs/api/getting-started/overview) |
| **Buildkite** | Pipeline and build automation API. | 🔑 ApiKey | ✅ | [Link](https://buildkite.com/docs/apis/rest-api) |
| **CircleCI** | CI pipelines, workflows, and artifacts API. | 🔑 ApiKey | ✅ | [Link](https://circleci.com/docs/api/v2/) |
| **Codeship** | Codeship is a Continuous Integration Platform in the cloud. | 🔑 ApiKey | ✅ | [Link](https://docs.cloudbees.com/docs/cloudbees-codeship/latest/api-overview/) |
| **Drone** | CI pipeline API for Drone server. | 🔑 ApiKey | ✅ | [Link](https://docs.drone.io/api/) |
| **Jenkins** | Automation server remote API. | 🔑 ApiKey | ✅ | [Link](https://www.jenkins.io/doc/book/using/remote-access-api/) |
| **Semaphore** | CI/CD projects, workflows, and jobs API. | 🔑 ApiKey | ✅ | [Link](https://docs.semaphoreci.com/reference/api) |
| **TeamCity** | Build server REST API. | 🔑 ApiKey | ✅ | [Link](https://www.jetbrains.com/help/teamcity/rest/teamcity-rest-api-documentation.html) |
| **Travis CI** | Sync your GitHub projects with Travis CI to test your code in minutes. | 🔑 ApiKey | ✅ | [Link](https://docs.travis-ci.com/api/) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="text-analysis-nlp"></a>📝 Text Analysis & NLP

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Cloudmersive Natural Language Processing** | Natural language processing and text analysis. | 🔑 ApiKey | ✅ | [Link](https://www.cloudmersive.com/nlp-api) |
| **AssemblyAI** | Speech-to-text and audio intelligence API. | 🔑 ApiKey | ✅ | [Link](https://www.assemblyai.com/docs) |
| **Code Detection API** | Detect, label, format and enrich the code in your app or in your data pipeline. | 🔐 OAuth | ✅ | [Link](https://codedetectionapi.runtime.dev) |
| **Dandelion** | Entity extraction and text analytics API. | 🔑 ApiKey | ✅ | [Link](https://dandelion.eu/docs/api/) |
| **DeepL** | Translation and multilingual text API. | 🔑 ApiKey | ✅ | [Link](https://developers.deepl.com/docs) |
| **Detect Language** | Detects text language. | 🔑 ApiKey | ✅ | [Link](https://detectlanguage.com/) |
| **Eden AI** | Unified NLP APIs across providers. | 🔑 ApiKey | ✅ | [Link](https://docs.edenai.co) |
| **ELI** | Natural Language Processing Tools for Thai Language. | 🔑 ApiKey | ✅ | [Link](https://nlp.insightera.co.th/docs/v1.0) |
| **Google Cloud Natural** | Natural language understanding technology, including sentiment, entity and sy... | 🔑 ApiKey | ✅ | [Link](https://cloud.google.com/natural-language/docs/) |
| **Hirak OCR** | Image to text -text recognition- from image more than 100 language, accurate,... | 🔑 ApiKey | ✅ | [Link](https://ocr.hirak.site/) |
| **Hirak Translation** | Translate between 21 of most used languages, accurate, unlimited requests. | 🔑 ApiKey | ✅ | [Link](https://translate.hirak.site/) |
| **LanguageTool** | Grammar and style checking API. | No | ✅ | [Link](https://languagetool.org/http-api/swagger-ui/#/) |
| **Lecto Translation** | Translation API with free tier and reasonable prices. | 🔑 ApiKey | ✅ | [Link](https://rapidapi.com/lecto-lecto-default/api/lecto-translation/) |
| **LibreTranslate** | Free and open-source translation API (**Self-hosted, No Auth**). | No | ✅ | [Link](https://libretranslate.com/) |
| **ParallelDots** | Sentiment and NLP analysis APIs. | 🔑 ApiKey | ✅ | [Link](https://komprehend.io/) |
| **Sapling** | Grammar correction and writing APIs. | 🔑 ApiKey | ✅ | [Link](https://sapling.ai/docs/) |
| **Semantria** | Text Analytics with sentiment analysis, categorization & named entity extraction. | 🔐 OAuth | ✅ | [Link](https://semantria.readme.io/docs) |
| **TextRazor** | NLP extraction and classification API. | 🔑 ApiKey | ✅ | [Link](https://www.textrazor.com/docs/rest) |
| **Tisane** | Text Analytics with focus on detection of abusive content and law enforcement... | 🔐 OAuth | ✅ | [Link](https://tisane.ai/) |
| **Watson Natural Language Understanding** | Natural language processing for advanced text analysis. | 🔐 OAuth | ✅ | [Link](https://cloud.ibm.com/apidocs/natural-language-understanding/natural-language-understanding) |
| **Wit.ai** | Intent/entity extraction for text/voice. | 🔑 ApiKey | ✅ | [Link](https://wit.ai/docs/http/20240304/) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="iot-smart-devices"></a>🏠 IoT & Smart Devices

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Adafruit IO** | IoT feed/data API with free tier. | 🔑 ApiKey | ✅ | [Link](https://io.adafruit.com/api/docs/) |
| **Arduino IoT** | Arduino IoT Cloud API. | 🔑 ApiKey | ✅ | [Link](https://www.arduino.cc/reference/en/iot/) |
| **Blynk** | IoT device control from cloud. | 🔑 ApiKey | ✅ | [Link](https://docs.blynk.io/) |
| **Blynk-Cloud** | Control IoT Devices from Blynk IoT Cloud. | 🔑 ApiKey | No | [Link](https://blynkapi.docs.apiary.io/#) |
| **Home Assistant** | Self-hosted home automation REST API. | 🔑 ApiKey | ✅ | [Link](https://developers.home-assistant.io/docs/api/rest/) |
| **IFTTT** | IFTTT Connect API. | No | ✅ | [Link](https://platform.ifttt.com/docs/connect_api) |
| **Particle Cloud** | IoT device management and data API. | 🔑 ApiKey | ✅ | [Link](https://docs.particle.io/reference/cloud-apis/api/) |
| **ThingsBoard** | Open-source IoT platform REST API. | 🔑 ApiKey | ✅ | [Link](https://thingsboard.io/docs/reference/rest-api/) |
| **Tuya Cloud** | Smart device management APIs. | 🔑 ApiKey | ✅ | [Link](https://developer.tuya.com/en/docs/cloud/) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="open-source-projects"></a>🔓 Open Source Projects

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Countly** | Countly web analytics. | No | No | [Link](https://api.count.ly/reference) |
| **Creative Commons Catalog** | Search among openly licensed and public domain works. | 🔐 OAuth | ✅ | [Link](https://api.creativecommons.engineering/) |
| **deps.dev** | Open package/dependency intelligence by Google. | No | ✅ | [Link](https://docs.deps.dev/api/) |
| **Drupal.org** | Drupal.org. | No | ✅ | [Link](https://www.drupal.org/drupalorg/docs/api) |
| **ecosyste.ms** | Open source ecosystem data APIs. | No | ✅ | [Link](https://docs.ecosyste.ms/) |
| **GitHub Contribution Chart Generator** | Create an image of your GitHub contributions. | No | ✅ | [Link](https://github-contributions.vercel.app) |
| **Metabase** | An open source Business Intelligence server to share data and analytics insid... | No | ✅ | [Link](https://www.metabase.com/) |
| **Packagist** | PHP package repository API. | No | ✅ | [Link](https://packagist.org/apidoc) |
| **PyPI JSON API** | Python package metadata API. | No | ✅ | [Link](https://docs.pypi.org/api/json/) |
| **Repology** | Package version tracking across repos. | No | ✅ | [Link](https://repology.org/api) |
| **RubyGems** | Ruby package repository API. | No | ✅ | [Link](https://guides.rubygems.org/rubygems-org-api) |
| **Shields.io** | Quality metadata badges for open source projects (**No Auth**). | No | ✅ | [Link](https://shields.io/) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="dictionaries"></a>📖 Dictionaries

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Chinese Character Web** | Chinese character definitions and pronunciations. | No | No | [Link](http://ccdb.hemiola.com/) |
| **Chinese Text Project** | Online open-access digital library for pre-modern Chinese texts. | No | ✅ | [Link](https://ctext.org/tools/api) |
| **Collins** | Bilingual Dictionary and Thesaurus Data. | 🔑 ApiKey | ✅ | [Link](https://api.collinsdictionary.com/api/v1/documentation/html/) |
| **Datamuse** | Word-finding query engine (**No Auth**). | No | ✅ | [Link](https://www.datamuse.com/api/) |
| **Free Dictionary API** | Free English dictionary API. | No | ✅ | [Link](https://dictionaryapi.dev/) |
| **Lingua Robot** | Word definitions and language detection (**No Auth**). | No | ✅ | [Link](https://www.linguarobot.io/) |
| **Merriam-Webster** | Dictionary and thesaurus. | 🔑 ApiKey | ✅ | [Link](https://dictionaryapi.com/) |
| **Oxford Dictionaries** | English dictionary and language data. | 🔑 ApiKey | ✅ | [Link](https://developer.oxforddictionaries.com/) |
| **Purgomalum** | Profanity filter API. | No | ✅ | [Link](https://www.purgomalum.com/) |
| **Synonyms API** | Find synonyms for any word. | No | ✅ | [Link](https://api-ninjas.com/api/thesaurus) |
| **Urban Dictionary** | Slang dictionary. | No | ✅ | [Link](https://api.urbandictionary.com/v0/define?term=api) |
| **Wiktionary API** | Open dictionary and thesaurus data. | No | ✅ | [Link](https://en.wiktionary.org/w/api.php) |
| **Wordnik** | Dictionary Data. | 🔑 ApiKey | ✅ | [Link](https://developer.wordnik.com) |
| **Words** | Definitions and synonyms for more than 150,000 words. | 🔑 ApiKey | ✅ | [Link](https://www.wordsapi.com/docs/) |
| **WordsAPI** | Word definitions, synonyms, antonyms. | 🔑 ApiKey | ✅ | [Link](https://www.wordsapi.com/) |


[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="education"></a>🎓 Education

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Calendarific** | Worldwide holidays for 230+ countries. | 🔑 ApiKey | ✅ | [Link](https://calendarific.com/api-documentation) |
| **CORE API** | Open access research paper metadata. | 🔑 ApiKey | ✅ | [Link](https://api.core.ac.uk/docs/v3) |
| **Crossref** | Scholarly article metadata (**No Auth**). | No | ✅ | [Link](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) |
| **edX API** | Online course catalog. | 🔐 OAuth | ✅ | [Link](https://courses.edx.org/api-docs/) |
| **Khan Academy** | Khan Academy educational content. | 🔐 OAuth | ✅ | [Link](https://khanacademy.org/api-docs) |
| **OpenAlex** | Open catalog of scholarly papers (**No Auth**). | No | ✅ | [Link](https://docs.openalex.org/) |
| **Periodic Table** | Chemical element data. | No | ✅ | [Link](https://api-ninjas.com/api/periodictable) |
| **Semantic Scholar** | Scholarly papers and citation graph data. | No | ✅ | [Link](https://api.semanticscholar.org/api-docs/) |
| **Universities List** | List of universities worldwide. | No | ✅ | [Link](http://universities.hipolabs.com/) |
| **Wikidata** | Structured knowledge base (**No Auth**). | No | ✅ | [Link](https://www.wikidata.org/wiki/Wikidata:Data_access) |
| **Wikipedia API** | Free encyclopedia data and content (**No Auth**). | No | ✅ | [Link](https://www.mediawiki.org/wiki/API:Main_page) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="calendar-holidays"></a>📅 Calendar & Holidays

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Checkiday - National Holiday API** | Industry-leading Holiday API. Over 5,000 holidays and thousands of descriptio... | 🔑 ApiKey | ✅ | [Link](https://apilayer.com/marketplace/checkiday-api) |
| **Church Calendar** | Catholic liturgical calendar. | No | No | [Link](http://calapi.inadiutorium.cz/) |
| **Czech Namedays Calendar** | Lookup for a name and returns nameday date. | No | No | [Link](https://svatky.adresa.info) |
| **Festivo Public Holidays** | Public holidays and observance data API. | 🔑 ApiKey | ✅ | [Link](https://docs.getfestivo.com/docs/products/public-holidays-api/intro) |
| **Hebrew Calendar** | Convert between Gregorian and Hebrew, fetch Shabbat and Holiday times, etc. | No | No | [Link](https://www.hebcal.com/home/developer-apis) |
| **HolidayAPI** | Holidays and observances by country and date. | 🔑 ApiKey | ✅ | [Link](https://holidayapi.com/) |
| **LectServe** | Protestant liturgical calendar. | No | No | [Link](http://www.lectserve.com) |
| **Namedays Calendar** | Nameday lookups by date and locale. | No | ✅ | [Link](https://nameday.abalin.net/) |
| **Non-Working Days** | Non-working day and holiday checks. | No | ✅ | [Link](https://isdayoff.ru/) |
| **Public Holidays** | Data on national, regional, and religious holidays via API. | 🔑 ApiKey | ✅ | [Link](https://www.abstractapi.com/holidays-api) |
| **TimeAPI.io** | Current time, timezone, and holiday info for any region. | No | ✅ | [Link](https://timeapi.io/swagger/index.html) |
| **UK Bank Holidays** | Official UK bank holiday dataset API. | No | ✅ | [Link](https://www.gov.uk/bank-holidays.json) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="public-data"></a>📊 Public Data & Datasets

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Archive.org** | The Internet Archive. | No | ✅ | [Link](https://archive.readme.io/docs) |
| **Black History Facts** | Contribute or search one of the largest black history fact databases on the web. | 🔑 ApiKey | ✅ | [Link](https://www.blackhistoryapi.io/docs) |
| **BotsArchive** | JSON formatted details about Telegram Bots available in database. | No | ✅ | [Link](https://botsarchive.com/docs.html) |
| **Callook.info** | United States ham radio callsigns. | No | ✅ | [Link](https://callook.info) |
| **CARTO** | Location Information Prediction. | 🔑 ApiKey | ✅ | [Link](https://carto.com/) |
| **CollegeScoreCard.ed.gov** | Data on higher education institutions in the United States. | No | ✅ | [Link](https://collegescorecard.ed.gov/data/) |
| **Data.gov** | US Government open data. | No | ✅ | [Link](https://api.data.gov/) |
| **Enigma Public** | Broadest collection of public data. | 🔑 ApiKey | ✅ | [Link](https://developers.enigma.com/docs) |
| **EPO** | European patent search system api. | 🔐 OAuth | ✅ | [Link](https://developers.epo.org/) |
| **Eurostat** | European Union statistics database (**No Auth**). | No | ✅ | [Link](https://ec.europa.eu/eurostat/web/main/data/web-services) |
| **French Address Search** | Address search via the French Government. | No | ✅ | [Link](https://geo.api.gouv.fr/adresse) |
| **GENESIS** | Federal Statistical Office Germany. | 🔐 OAuth | ✅ | [Link](https://www.destatis.de/EN/Service/OpenData/api-webservice.html) |
| **Joshua Project** | People groups of the world with the fewest followers of Christ. | 🔑 ApiKey | ✅ | [Link](https://api.joshuaproject.net/) |
| **Kaggle** | Create and interact with Datasets, Notebooks, and connect with Kaggle. | 🔑 ApiKey | ✅ | [Link](https://www.kaggle.com/docs/api) |
| **LinkPreview** | Get JSON formatted summary with title, description and preview image for any ... | 🔑 ApiKey | ✅ | [Link](https://www.linkpreview.net) |
| **Microlink.io** | Extract structured data from any website. | No | ✅ | [Link](https://microlink.io) |
| **Nager.Date** | Public holidays for 100+ countries (**No Auth, no rate limit**). | No | ✅ | [Link](https://date.nager.at/Api) |
| **Nasdaq Data Link** | Stock market data. | 🔑 ApiKey | ✅ | [Link](https://docs.data.nasdaq.com/) |
| **Nobel Prize** | Open data about nobel prizes and events. | No | ✅ | [Link](https://www.nobelprize.org/about/developer-zone-2/) |
| **Open Data Minneapolis** | Spatial (GIS) and non-spatial city data for Minneapolis. | No | ✅ | [Link](https://opendata.minneapolismn.gov/) |
| **openAFRICA** | Large datasets repository of African open data. | No | ✅ | [Link](https://africaopendata.org/) |
| **OpenCorporates** | Data on corporate entities and directors in many countries. | 🔑 ApiKey | ✅ | [Link](http://api.opencorporates.com/documentation/API-Reference) |
| **OpenHolidays API** | Public and school holidays worldwide (**No Auth**). | No | ✅ | [Link](https://www.openholidaysapi.org/) |
| **OpenSanctions** | Data on international sanctions, crime and politically exposed persons. | No | ✅ | [Link](https://www.opensanctions.org/docs/api/) |
| **PatentsView** | API is intended to explore and visualize trends/patterns across the US innova... | No | ✅ | [Link](https://patentsview.org/apis/purpose) |
| **PeakMetrics** | News articles and public datasets. | 🔑 ApiKey | ✅ | [Link](https://rapidapi.com/peakmetrics-peakmetrics-default/api/peakmetrics-news) |
| **Recreation Information Database** | Recreational areas, federal lands, historic sites, museums, and other attract... | 🔑 ApiKey | ✅ | [Link](https://ridb.recreation.gov/) |
| **Socrata Open Data** | Access government and public sector data. | No | ✅ | [Link](https://dev.socrata.com/) |
| **TimeZoneDB** | Time zone data and conversion (**No Auth**). | No | ✅ | [Link](https://timezonedb.com/api) |
| **TIPO** | Taiwan patent search system api. | 🔑 ApiKey | ✅ | [Link](https://tiponet.tipo.gov.tw/Gazette/OpenData/OD/OD05.aspx?QryDS=API00) |
| **Umeå Open Data** | Open data of the city Umeå in northen Sweden. | No | ✅ | [Link](https://opendata.umea.se/api/) |
| **University of Oslo** | Courses, lecture videos, detailed information for courses etc. for the Univer... | No | ✅ | [Link](https://data.uio.no/) |
| **UPC database** | More than 1.5 million barcode numbers from all around the world. | 🔑 ApiKey | ✅ | [Link](https://upcdatabase.org/api) |
| **Urban Observatory** | The largest set of publicly available real time urban data in the UK. | No | No | [Link](https://urbanobservatory.ac.uk) |
| **US Census** | US demographics, economics, housing data. | 🔑 ApiKey | ✅ | [Link](https://www.census.gov/data/developers/data-sets.html) |
| **USDA FoodData** | Nutritional data for food products. | 🔑 ApiKey | ✅ | [Link](https://fdc.nal.usda.gov/api-guide.html) |
| **USPTO** | US patent data and applications (**No Auth**). | No | ✅ | [Link](https://developer.uspto.gov/api-catalog) |
| **World Bank** | Global development data. | No | ✅ | [Link](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="email-sms"></a>📧 Email & SMS

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Cloudmersive Validate** | Validate email addresses, phone numbers, VAT numbers and domain names. | 🔑 ApiKey | ✅ | [Link](https://cloudmersive.com/validate-api) |
| **Disify** | Validate and detect disposable and temporary email addresses. | No | ✅ | [Link](https://www.disify.com/) |
| **DropMail** | GraphQL API for creating and managing ephemeral e-mail inboxes. | No | ✅ | [Link](https://dropmail.me/api/#live-demo) |
| **Email Validation** | Validate email addresses for deliverability and spam. | 🔑 ApiKey | ✅ | [Link](https://www.abstractapi.com/email-verification-validation-api) |
| **Guerrilla Mail** | Disposable temporary Email addresses. | No | ✅ | [Link](https://www.guerrillamail.com/GuerrillaMailAPI.html) |
| **ImprovMX** | API for free email forwarding service. | 🔑 ApiKey | ✅ | [Link](https://improvmx.com/api) |
| **Kickbox** | Email verification API. | No | ✅ | [Link](https://open.kickbox.com/) |
| **mail.gw** | 10 Minute Mail. | No | ✅ | [Link](https://docs.mail.gw) |
| **mail.tm** | Temporary Email Service. | No | ✅ | [Link](https://docs.mail.tm) |
| **MailboxValidator** | Validate email address to improve deliverability. | 🔑 ApiKey | ✅ | [Link](https://www.mailboxvalidator.com/api-email-free) |
| **MailCheck.ai** | Prevent users to sign up with temporary email addresses. | No | ✅ | [Link](https://www.mailcheck.ai/#documentation) |
| **Mailchimp** | Email marketing and audience management APIs. | 🔑 ApiKey | ✅ | [Link](https://mailchimp.com/developer/) |
| **Mailgun** | Email service for developers (free tier). | 🔑 ApiKey | ✅ | [Link](https://documentation.mailgun.com/) |
| **Mailjet** | Transactional email and marketing API. | 🔑 ApiKey | ✅ | [Link](https://www.mailjet.com/) |
| **Mailtrap** | Email testing and sending API. | 🔑 ApiKey | ✅ | [Link](https://api-docs.mailtrap.io/) |
| **Brevo (Sendinblue)** | Transactional email, SMS, and marketing automation. | 🔑 ApiKey | ✅ | [Link](https://developers.brevo.com/) |
| **Loops** | Transactional and marketing email for SaaS apps. | 🔑 ApiKey | ✅ | [Link](https://loops.so/docs/api-reference) |
| **OneSignal** | Push notifications platform (free tier). | 🔑 ApiKey | ✅ | [Link](https://documentation.onesignal.com/reference) |
| **Postmark** | Transactional email delivery for web apps. | 🔑 ApiKey | ✅ | [Link](https://postmarkapp.com/developer) |
| **Pushover** | Simple push notifications API. | 🔑 ApiKey | ✅ | [Link](https://pushover.net/api) |
| **Resend** | Modern email API for developers (free tier). | 🔑 ApiKey | ✅ | [Link](https://resend.com/docs/api-reference/introduction) |
| **SendGrid** | Email delivery service (free tier: 100/day). | 🔑 ApiKey | ✅ | [Link](https://docs.sendgrid.com/api-reference) |
| **Tomba** | Email finder and verifier API. | 🔑 ApiKey | ✅ | [Link](https://tomba.io/api) |
| **Twilio** | SMS, voice, and messaging (trial credits). | 🔑 ApiKey | ✅ | [Link](https://www.twilio.com/docs/usage/api) |
| **Verifier** | Verifies that a given email is real. | 🔑 ApiKey | ✅ | [Link](https://verifier.meetchopra.com/docs#/) |
| **Vonage (Nexmo)** | SMS and voice APIs (trial credits). | 🔑 ApiKey | ✅ | [Link](https://developer.vonage.com/api) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="phone-telephony"></a>📱 Phone & Telephony

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **46elks** | SMS and voice telephony API. | 🔑 ApiKey | ✅ | [Link](https://46elks.com/docs) |
| **Apifonica** | Voice call automation API. | 🔑 ApiKey | ✅ | [Link](https://www.apifonica.com/docs/voice-api/) |
| **Bandwidth** | Voice, messaging, and phone number APIs. | 🔑 ApiKey | ✅ | [Link](https://dev.bandwidth.com/docs/) |
| **MessageBird** | SMS and omnichannel messaging APIs. | 🔑 ApiKey | ✅ | [Link](https://developers.messagebird.com/api/) |
| **NeutrinoAPI Phone Validate** | Phone validation and carrier lookup. | 🔑 ApiKey | ✅ | [Link](https://www.neutrinoapi.com/api/phone-validate/) |
| **Phone Validation** | Validate phone numbers globally. | 🔑 ApiKey | ✅ | [Link](https://www.abstractapi.com/phone-validation-api) |
| **Plivo** | Voice and SMS communication APIs. | 🔑 ApiKey | ✅ | [Link](https://www.plivo.com/docs/home) |
| **Sinch** | SMS, voice, and verification APIs. | 🔑 ApiKey | ✅ | [Link](https://developers.sinch.com/) |
| **Telnyx** | Telephony, messaging, and SIP APIs. | 🔑 ApiKey | ✅ | [Link](https://developers.telnyx.com/api-reference/overview) |
| **Textbelt** | Lightweight SMS sending API. | 🔑 ApiKey | ✅ | [Link](https://www.textbelt.com/) |
| **Veriphone** | Phone number validation & carrier lookup. | 🔑 ApiKey | ✅ | [Link](https://veriphone.io) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="entertainment"></a>🎮 Entertainment

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Activities when get bored** | Random suggestions for activities. | No | ✅ | [Link](https://rapidapi.com/bored/api/bored-api/) |
| **Biriyani As A Service** | Biriyani images placeholder. | No | ✅ | [Link](https://biriyani.anoram.com/) |
| **FOAAS** | Fuck Off As A Service. | No | No | [Link](http://www.foaas.com/) |
| **Fun Fact** | A simple HTTPS api that can randomly select and return a fact from the FFA da... | No | ✅ | [Link](https://api.aakhilv.me) |
| **Meme Maker** | REST API for create your own meme. | No | ✅ | [Link](https://mememaker.github.io/API/) |
| **OMDb** | Open Movie Database. | 🔑 ApiKey | ✅ | [Link](http://www.omdbapi.com/) |
| **Quiz API** | Random trivia questions (**No Auth**). | No | ✅ | [Link](https://quizapi.io/) |
| **Simkl** | Movies, TV, Anime metadata. | 🔑 ApiKey | ✅ | [Link](https://simkl.com/apidoc/) |
| **StreamElements** | Twitch/YouTube live streaming data & overlays. | 🔑 ApiKey | ✅ | [Link](https://dev.streamelements.com/) |
| **TheTVDB** | TV database with episodes and artwork. | 🔑 ApiKey | ✅ | [Link](https://thetvdb.github.io/v4-api/) |
| **TMDb** | The Movie Database. | 🔑 ApiKey | ✅ | [Link](https://developers.themoviedb.org/3) |
| **Trakt** | TV and Movie tracking. | 🔐 OAuth | ✅ | [Link](https://trakt.docs.apiary.io/) |
| **Trivia API** | Trivia questions in various categories (**No Auth**). | No | ✅ | [Link](https://the-trivia-api.com/) |
| **TVmaze** | TV shows and episode data (**No Auth**). | No | ✅ | [Link](https://www.tvmaze.com/api) |
| **Watchmode** | Streaming availability. | 🔑 ApiKey | ✅ | [Link](https://api.watchmode.com/) |
| **Bored API** | Get random activity suggestions when you are bored (**No Auth**). | No | ✅ | [Link](https://bored-api.appbrewery.com/) |


[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="events"></a>🎪 Events

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Eventbrite** | Find events. | 🔐 OAuth | ✅ | [Link](https://www.eventbrite.com/platform/api/) |
| **Eventyay** | Open-source event management API. | No | ✅ | [Link](https://api.eventyay.com/) |
| **Luma** | Event creation and attendee APIs. | 🔑 ApiKey | ✅ | [Link](https://docs.luma.com/reference/getting-started) |
| **OpenAgenda** | Event agenda and discovery API. | 🔑 ApiKey | ✅ | [Link](https://developers.openagenda.com/) |
| **PredictHQ** | Event intelligence and impact API. | 🔑 ApiKey | ✅ | [Link](https://docs.predicthq.com/) |
| **pretix** | Ticketing and event operations API. | 🔑 ApiKey | ✅ | [Link](https://docs.pretix.eu/dev/api/index.html) |
| **SeatGeek** | Search events, venues and performers. | 🔑 ApiKey | ✅ | [Link](https://platform.seatgeek.com/) |
| **Sessionize** | CFP sessions and speakers API. | No | ✅ | [Link](https://sessionize.com/playbook/api/) |
| **Ti.to** | Event ticketing and registrations API. | 🔑 ApiKey | ✅ | [Link](https://ti.to/docs/api) |
| **Ticket Tailor** | Ticketing and order management API. | 🔑 ApiKey | ✅ | [Link](https://developers.tickettailor.com/) |
| **Ticketmaster** | Search events, attractions, or venues. | 🔑 ApiKey | ✅ | [Link](http://developer.ticketmaster.com/products-and-docs/apis/getting-started/) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="podcasts"></a>🎙️ Podcasts

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Acast** | Podcast platform and publisher APIs. | 🔑 ApiKey | ✅ | [Link](https://developers.acast.com/) |
| **Audioboom** | Podcast metadata and episode endpoints. | No | ✅ | [Link](https://api.audioboom.com/) |
| **Buzzsprout** | Podcast hosting and episodes API. | 🔑 ApiKey | ✅ | [Link](https://www.buzzsprout.com/api) |
| **Fountain** | Podcast app developer API resources. | No | ✅ | [Link](https://fountain.fm/developer) |
| **fyyd** | Podcast search and metadata API. | No | ✅ | [Link](https://api.fyyd.de/) |
| **gpodder.net** | Podcast sync and subscriptions API. | No | ✅ | [Link](https://gpoddernet.readthedocs.io/en/latest/api/index.html) |
| **Podbean** | Podcast hosting and distribution API. | 🔐 OAuth | ✅ | [Link](https://developers.podbean.com/) |
| **Podcast Index** | Open podcast data and search. | 🔑 ApiKey | ✅ | [Link](https://podcastindex-org.github.io/docs-api/) |
| **Taddy** | GraphQL podcast search and metadata API. | 🔑 ApiKey | ✅ | [Link](https://taddy.org/developers) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="personality-quotes"></a>💭 Personality & Quotes

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Affirmations.dev** | Daily affirmations API. | No | ✅ | [Link](https://www.affirmations.dev/) |
| **API-Ninjas Quotes** | Curated quotes API. | 🔑 ApiKey | ✅ | [Link](https://api-ninjas.com/api/quotes) |
| **DummyJSON Quotes** | Fake quotes dataset API. | No | ✅ | [Link](https://dummyjson.com/docs/quotes) |
| **FavQs.com** | FavQs allows you to collect, discover and share your favorite quotes. | 🔑 ApiKey | ✅ | [Link](https://favqs.com/api) |
| **Forismatic** | Inspirational Quotes. | No | No | [Link](http://forismatic.com/en/api/) |
| **Quotable** | Random quotes with authors, tags, and pagination (**No Auth**). | No | ✅ | [Link](https://github.com/lukePeavey/quotable) |
| **Quotes on Design** | Inspirational Quotes. | No | ✅ | [Link](https://quotesondesign.com/api/) |
| **They Said So Quotes** | Quotes Trusted by many fortune brands around the world. | No | ✅ | [Link](https://theysaidso.com/api/) |
| **Traitify** | Assess, collect and analyze Personality. | No | ✅ | [Link](https://app.traitify.com/developer) |
| **Udemy(instructor)** | API for instructors on Udemy. | 🔑 ApiKey | ✅ | [Link](https://www.udemy.com/developers/instructor/) |
| **Type.fit Quotes** | Collection of inspirational quotes (**No Auth**). | No | ✅ | [Link](https://type.fit/api/quotes) |


[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="finance"></a>💰 Finance

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Aletheia** | Insider trading data, earnings call analysis, financial statements, and more. | 🔑 ApiKey | ✅ | [Link](https://aletheiaapi.com/) |
| **Alpaca** | Commission-free stock trading. | 🔑 ApiKey | ✅ | [Link](https://alpaca.markets/docs/api-references/) |
| **Alpha Vantage** | Realtime and historical stock data. | 🔑 ApiKey | ✅ | [Link](https://www.alphavantage.co/) |
| **Banco do Brasil** | All Banco do Brasil financial transaction APIs. | 🔐 OAuth | ✅ | [Link](https://developers.bb.com.br/home) |
| **Bank Data API** | Instant IBAN and SWIFT number validation across the globe. | 🔑 ApiKey | ✅ | [Link](https://apilayer.com/marketplace/bank_data-api) |
| **Billplz** | Payment platform. | 🔑 ApiKey | ✅ | [Link](https://www.billplz.com/api) |
| **Binlist** | BIN/IIN Lookup. | No | ✅ | [Link](https://binlist.net/) |
| **Boleto.Cloud** | A api to generate boletos in Brazil. | 🔑 ApiKey | ✅ | [Link](https://boleto.cloud/) |
| **Citi** | All Citigroup account and statement data APIs. | 🔑 ApiKey | ✅ | [Link](https://sandbox.developerhub.citi.com/api-catalog-list) |
| **CoinDesk** | Bitcoin Price Index (BPI) data (**No Auth**). | No | ✅ | [Link](https://www.coindesk.com/coindesk-api) |
| **Econdb** | Global macroeconomic data. | No | ✅ | [Link](https://www.econdb.com/api/) |
| **Fed Treasury** | U.S. Department of the Treasury Data. | No | ✅ | [Link](https://fiscaldata.treasury.gov/api-documentation/) |
| **Finage** | Finage is a stock, currency, cryptocurrency, indices, and ETFs real-time & hi... | 🔑 ApiKey | ✅ | [Link](https://finage.co.uk) |
| **Financial Modeling Prep** | Stock market data. | 🔑 ApiKey | ✅ | [Link](https://site.financialmodelingprep.com/developer/docs) |
| **Finnhub** | Stock market data. | 🔑 ApiKey | ✅ | [Link](https://finnhub.io/docs/api) |
| **Front Accounting APIs** | Front accounting is multilingual and multicurrency software for small businesses. | 🔐 OAuth | ✅ | [Link](https://frontaccounting.com/fawiki/index.php?n=Devel.SimpleAPIModule) |
| **Hotstoks** | Stock market data powered by SQL. | 🔑 ApiKey | ✅ | [Link](https://hotstoks.com?utm_source=public-apis) |
| **IG** | Spreadbetting and CFD Market Data. | 🔑 ApiKey | ✅ | [Link](https://labs.ig.com/gettingstarted) |
| **Indian Mutual Fund** | Get complete history of India Mutual Funds Data. | No | ✅ | [Link](https://www.mfapi.in/) |
| **Intrinio** | A wide selection of financial data feeds. | 🔑 ApiKey | ✅ | [Link](https://intrinio.com/) |
| **Klarna** | Payments. | 🔑 ApiKey | ✅ | [Link](https://docs.klarna.com/api/) |
| **Marketstack** | Real-time, intraday and historical market data. | 🔑 ApiKey | ✅ | [Link](https://marketstack.com/) |
| **MercadoPago** | Payments. | 🔑 ApiKey | ✅ | [Link](https://www.mercadopago.com.br/developers/es/reference) |
| **Mono** | Connect with users’ bank accounts and access transaction data in Africa. | 🔑 ApiKey | ✅ | [Link](https://mono.co/) |
| **Moov** | The Moov API makes it simple for platforms to send, receive, and store money. | 🔑 ApiKey | ✅ | [Link](https://docs.moov.io/api/) |
| **OpenFIGI** | Equity, index, futures, options symbology from Bloomberg LP. | 🔑 ApiKey | ✅ | [Link](https://www.openfigi.com/api) |
| **Plaid** | Connect bank accounts. | 🔑 ApiKey | ✅ | [Link](https://www.plaid.com/docs) |
| **Polygon** | Stock market data. | 🔑 ApiKey | ✅ | [Link](https://polygon.io/) |
| **Portfolio Optimizer** | Portfolio analysis and optimization. | No | ✅ | [Link](https://portfoliooptimizer.io/) |
| **Razorpay IFSC** | Indian Financial Systems Code (Bank Branch Codes) | No | ✅ | [Link](https://razorpay.com/docs/) |
| **SEC EDGAR Data** | API to access annual reports of public US companies. | No | ✅ | [Link](https://www.sec.gov/edgar/sec-api-documentation) |
| **SmartAPI** | Gain access to set of <SmartAPI> and create end-to-end broking services. | 🔑 ApiKey | ✅ | [Link](https://smartapi.angelbroking.com/) |
| **Square** | Payments, checkout, and commerce APIs. | 🔐 OAuth | ✅ | [Link](https://developer.squareup.com/reference/square) |
| **StockData** | Real-Time, Intraday & Historical Market Data, News and Sentiment API. | 🔑 ApiKey | ✅ | [Link](https://www.StockData.org) |
| **Stripe** | Payments. | 🔑 ApiKey | ✅ | [Link](https://stripe.com/docs/api) |
| **Tax Data API** | Tax rates and validation. | 🔑 ApiKey | ✅ | [Link](https://apilayer.com/marketplace/tax_data-api) |
| **Tradier** | US equity/option market data (delayed, intraday, historical) | 🔐 OAuth | ✅ | [Link](https://developer.tradier.com) |
| **Tiingo** | Financial data, news, and fundamentals API. | 🔑 ApiKey | ✅ | [Link](https://www.tiingo.com/documentation/general/overview) |
| **Twelve Data** | Stock market data (real-time & historical) | 🔑 ApiKey | ✅ | [Link](https://twelvedata.com/) |
| **Wise** | International money transfers and currency exchange. | 🔐 OAuth | ✅ | [Link](https://docs.wise.com/api-docs) |
| **VAT Validation** | Validate VAT numbers and calculate VAT rates. | 🔑 ApiKey | ✅ | [Link](https://www.abstractapi.com/vat-validation-rates-api) |
| **WallstreetBets** | WallstreetBets Stock Comments Sentiment Analysis. | No | ✅ | [Link](https://dashboard.nbshare.io/apps/reddit/api/) |
| **YNAB** | Budgeting & Planning. | 🔐 OAuth | ✅ | [Link](https://api.youneedabudget.com/) |
| **Zoho Books** | Online accounting software, built for your business. | 🔐 OAuth | ✅ | [Link](https://www.zoho.com/books/api/v3/) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="currency-exchange"></a>💱 Currency Exchange

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **1Forge** | Forex currency market data. | 🔑 ApiKey | ✅ | [Link](https://1forge.com/forex-data-api/api-documentation) |
| **Amdoren** | Free currency API with over 150 currencies. | 🔑 ApiKey | ✅ | [Link](https://www.amdoren.com/currency-api/) |
| **Bank of Canada Valet** | Free central-bank exchange/economic series API. | No | ✅ | [Link](https://www.bankofcanada.ca/valet/docs) |
| **Bank of Russia** | Exchange rates and currency conversion. | No | ✅ | [Link](https://www.cbr.ru/development/SXML/) |
| **CurrencyAPI** | Real-time currency rates and conversion. | 🔑 ApiKey | ✅ | [Link](https://currencyapi.com/) |
| **CurrencyBeacon** | Real-time and historical exchange rates. | 🔑 ApiKey | ✅ | [Link](https://currencybeacon.com/api-documentation) |
| **CurrencyConverterAPI** | Free currency converter. | 🔑 ApiKey | ✅ | [Link](https://currencyconverterapi.com/docs) |
| **CurrencyFreaks** | Exchange rates and currency conversion API. | 🔑 ApiKey | ✅ | [Link](https://currencyfreaks.com/) |
| **Currencylayer** | Exchange rates and currency conversion. | 🔑 ApiKey | ✅ | [Link](https://currencylayer.com/) |
| **CurrencyScoop** | Real-time and historical currency rates JSON API. | 🔑 ApiKey | ✅ | [Link](https://currencyscoop.com/api-documentation) |
| **Czech National Bank** | A collection of exchange rates. | No | ✅ | [Link](https://www.cnb.cz/cs/financni_trhy/devizovy_trh/kurzy_devizoveho_trhu/denni_kurz.xml) |
| **ECB Data API** | Public ECB data API for exchange rates. | No | ✅ | [Link](https://data.ecb.europa.eu/help/api/data) |
| **Economia.Awesome** | Portuguese free currency prices and conversion with no rate limits. | No | ✅ | [Link](https://docs.awesomeapi.com.br/api-de-moedas) |
| **ExchangeRate-API** | Currency exchange rate conversion data. | No | ✅ | [Link](https://www.exchangerate-api.com/docs/free) |
| **Exchangerate.host** | Foreign exchange & crypto rates. | 🔑 ApiKey | ✅ | [Link](https://exchangerate.host/) |
| **Exchangeratesapi** | Exchange rates and currency conversion. | 🔑 ApiKey | ✅ | [Link](https://exchangeratesapi.io/) |
| **Fixer** | Exchange rates and currency conversion. | 🔑 ApiKey | ✅ | [Link](https://fixer.io/) |
| **Frankfurter** | Open source exchange rates API. | No | ✅ | [Link](https://www.frankfurter.app/) |
| **FreeCurrencyAPI** | Free currency conversion API. | 🔑 ApiKey | ✅ | [Link](https://freecurrencyapi.com/docs) |
| **National Bank of Poland** | Official exchange rates from NBP. | No | ✅ | [Link](https://api.nbp.pl/en.html) |
| **Open Exchange Rates** | Currency conversion and exchange rates. | 🔑 ApiKey | ✅ | [Link](https://docs.openexchangerates.org/) |
| **VATComply** | VAT rates and FX conversion data. | No | ✅ | [Link](https://www.vatcomply.com) |
| **ExchangeRate.host** | Free foreign exchange and crypto rates (**No Auth**). | No | ✅ | [Link](https://exchangerate.host/) |


[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="food-drink"></a>🍔 Food & Drink

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **BaconMockup** | Resizable bacon placeholder images. | No | ✅ | [Link](https://baconmockup.com/) |
| **Chomp** | Data about various grocery products and foods. | 🔑 ApiKey | ✅ | [Link](https://chompthis.com/api/) |
| **Coffee** | Random coffee images (**No Auth**). | No | ✅ | [Link](https://coffee.alexflipnote.dev/) |
| **Edamam Recipe** | Recipe search and nutrition analysis. | 🔑 ApiKey | ✅ | [Link](https://developer.edamam.com/edamam-recipe-api) |
| **Edamam recipes** | Recipe Search. | 🔑 ApiKey | ✅ | [Link](https://developer.edamam.com/edamam-docs-recipe-api) |
| **Fruityvice** | Data about all kinds of fruit. | No | ✅ | [Link](https://www.fruityvice.com) |
| **Ninjas Recipe** | Recipe search with nutrition data. | 🔑 ApiKey | ✅ | [Link](https://api-ninjas.com/api/recipe) |
| **Open Brewery DB** | Brewery database worldwide. | No | ✅ | [Link](https://www.openbrewerydb.org/) |
| **Open Food Facts** | Food product data. | No | ✅ | [Link](https://world.openfoodfacts.org/data) |
| **Punk API** | BrewDog beer recipes and data (community fork). | No | ✅ | [Link](https://punkapi-alxiw.amvera.io/v3/) |
| **Spoonacular** | Food, recipes, and nutrition data. | 🔑 ApiKey | ✅ | [Link](https://spoonacular.com/food-api) |
| **Tasty** | Recipes from Tasty (via RapidAPI). | 🔑 ApiKey | ✅ | [Link](https://rapidapi.com/apidojo/api/tasty/) |
| **TheCocktailDB** | Open database for drinks and cocktails. | 🔑 ApiKey | ✅ | [Link](https://www.thecocktaildb.com/api.php) |
| **TheMealDB** | Open source database of recipes from around the world. | 🔑 ApiKey | ✅ | [Link](https://www.themealdb.com/api.php) |
| **Untappd** | Social beer sharing. | 🔐 OAuth | ✅ | [Link](https://untappd.com/api/docs) |
| **What's on the menu?** | NYPL human-transcribed historical menu collection. | 🔑 ApiKey | No | [Link](http://nypl.github.io/menus-api/) |
| **WhiskyHunter** | Past online whisky auctions statistical data. | No | ✅ | [Link](https://whiskyhunter.net/api/) |
| **Yelp Fusion** | Business and restaurant reviews. | 🔑 ApiKey | ✅ | [Link](https://docs.developer.yelp.com/) |
| **Zestful** | Parse recipe ingredients. | 🔑 ApiKey | ✅ | [Link](https://zestfuldata.com/) |
| **Zomato** | Restaurant search and reviews. | 🔑 ApiKey | ✅ | [Link](https://developers.zomato.com/api) |


[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="games-comics"></a>🎮 Games & Comics

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Animal Crossing: New Horizons** | API for critters, fossils, art, music, furniture and villagers. | No | ✅ | [Link](http://acnhapi.com/) |
| **Balldontlie** | NBA players, teams, games & stats (**No Auth**). | No | ✅ | [Link](https://www.balldontlie.io/) |
| **Battle.net** | Blizzard games data. | 🔐 OAuth | ✅ | [Link](https://develop.battle.net/documentation/guides/getting-started) |
| **BoardGameGeek** | Board games database. | No | ✅ | [Link](https://boardgamegeek.com/wiki/page/BGG_XML_API2) |
| **Brawl Stars** | Game data. | 🔑 ApiKey | ✅ | [Link](https://developer.brawlstars.com) |
| **CheapShark** | Steam/PC Game Prices and Deals. | No | ✅ | [Link](https://www.cheapshark.com/api) |
| **Chess.com** | Chess player stats and games. | No | ✅ | [Link](https://www.chess.com/news/view/published-data-api) |
| **Chuck Norris Database** | Jokes. | No | No | [Link](http://www.icndb.com/api/) |
| **Clash of Clans** | Game data. | 🔑 ApiKey | ✅ | [Link](https://developer.clashofclans.com) |
| **Clash Royale** | Game data. | 🔑 ApiKey | ✅ | [Link](https://developer.clashroyale.com) |
| **Comic Vine** | Comics. | No | ✅ | [Link](https://comicvine.gamespot.com/api/documentation) |
| **Cross Universe** | Cross Universe Card Data. | No | ✅ | [Link](https://crossuniverse.psychpsyo.com/apiDocs.html) |
| **Deck of Cards** | Deck of cards. | No | No | [Link](http://deckofcardsapi.com/) |
| **Destiny The Game** | Bungie Platform API. | 🔑 ApiKey | ✅ | [Link](https://bungie-net.github.io/multi/index.html) |
| **Digimon** | Digimon information. | No | ✅ | [Link](https://digimon-api.vercel.app/) |
| **Digimon TCG** | Search for Digimon cards in digimoncard.io. | No | ✅ | [Link](https://documenter.getpostman.com/view/14059948/TzecB4fH) |
| **Disney** | Information of Disney characters. | No | ✅ | [Link](https://disneyapi.dev) |
| **Dota 2** | Game data. | 🔑 ApiKey | ✅ | [Link](https://docs.opendota.com/) |
| **Dungeons and Dragons** | 5th Edition SRD. | No | ✅ | [Link](https://www.dnd5eapi.co/docs/) |
| **Dungeons and Dragons (Alternate)** | Includes all monsters and spells from the SRD (System Reference Document) as ... | No | ✅ | [Link](https://open5e.com/) |
| **Elden Ring API** | Elden Ring game data (**No Auth**). | No | ✅ | [Link](https://docs.eldenring.fanapis.com/) |
| **Eve Online** | Game data. | 🔐 OAuth | ✅ | [Link](https://esi.evetech.net/) |
| **FFXIV Collect** | Final Fantasy XIV data on collectables. | No | ✅ | [Link](https://ffxivcollect.com/) |
| **Final Fantasy XIV** | Game data. | No | ✅ | [Link](https://xivapi.com/) |
| **Fortnite** | Game data. | 🔑 ApiKey | ✅ | [Link](https://fortnitetracker.com/site-api) |
| **Free to Play Games** | Database of free-to-play games (**No Auth**). | No | ✅ | [Link](https://www.freetogame.com/api-doc) |
| **FunTranslations** | Translate Text into funny languages. | No | ✅ | [Link](https://api.funtranslations.com/) |
| **GamerPower** | Free games, loot, and giveaways (**No Auth**). | No | ✅ | [Link](https://www.gamerpower.com/api-read) |
| **GDBrowser** | Easy way to use the Geometry Dash Servers. | No | ✅ | [Link](https://gdbrowser.com/api) |
| **Genshin Impact** | Game data. | No | ✅ | [Link](https://genshin.dev) |
| **Giant Bomb** | Video Games. | 🔑 ApiKey | ✅ | [Link](https://www.giantbomb.com/api/) |
| **Guild Wars 2** | Game data. | 🔑 ApiKey | ✅ | [Link](https://wiki.guildwars2.com/wiki/API:Main) |
| **Halo** | Halo 5 and Halo Wars 2 Information. | 🔑 ApiKey | ✅ | [Link](https://developer.haloapi.com/) |
| **Hearthstone** | Hearthstone Cards Information. | 🔑 ApiKey | ✅ | [Link](http://hearthstoneapi.com/) |
| **Humble Bundle** | Humble Bundle's current bundles. | 🔑 ApiKey | ✅ | [Link](https://rapidapi.com/Ziggoto/api/humble-bundle) |
| **Humor** | Humor, Jokes, and Memes. | 🔑 ApiKey | ✅ | [Link](https://humorapi.com) |
| **Hypixel** | Minecraft server data. | 🔑 ApiKey | ✅ | [Link](https://api.hypixel.net/) |
| **IGDB.com** | Game database. | 🔑 ApiKey | ✅ | [Link](https://api-docs.igdb.com) |
| **Jokes One** | Joke of the day and large category of jokes accessible via REST API. | 🔑 ApiKey | ✅ | [Link](https://jokes.one/api/joke/) |
| **Lichess** | Chess data. | 🔐 OAuth | ✅ | [Link](https://lichess.org/api) |
| **Magic The Gathering** | Magic The Gathering Game Information. | No | No | [Link](http://magicthegathering.io/) |
| **Magic: The Gathering** | MTG card data. | No | ✅ | [Link](https://docs.magicthegathering.io/) |
| **Marvel** | Comics data. | 🔑 ApiKey | ✅ | [Link](https://developer.marvel.com) |
| **Minecraft Server Status** | Server status. | No | ✅ | [Link](https://api.mcsrvstat.us) |
| **MLB** | Major League Baseball scores and statistics. | No | ✅ | [Link](https://appac.github.io/mlb-data-api-docs/) |
| **MMO API** | MMORPG and RPG game items, achievements, characters. | 🔑 ApiKey | ✅ | [Link](https://raider.io/api) |
| **MMO Games** | MMO Games Database, News and Giveaways. | No | ✅ | [Link](https://www.mmobomb.com/api) |
| **mod.io** | Cross Platform Mod API. | 🔑 ApiKey | ✅ | [Link](https://docs.mod.io) |
| **Monster Hunter World** | MHW items, monsters, weapons, armor data (**No Auth**). | No | ✅ | [Link](https://docs.mhw-db.com/) |
| **Open Trivia** | Trivia questions. | No | ✅ | [Link](https://opentdb.com/api_config.php) |
| **Overwatch API** | Overwatch 2 player stats and heroes (**No Auth**). | No | ✅ | [Link](https://overfast-api.tekrop.fr/) |
| **Path of Exile** | Path of Exile Game Information. | 🔐 OAuth | ✅ | [Link](https://www.pathofexile.com/developer/docs) |
| **PlayerDB** | Query Minecraft, Steam and XBox Accounts. | No | ✅ | [Link](https://playerdb.co/) |
| **Pokéapi** | Pokémon data. | No | ✅ | [Link](https://pokeapi.co) |
| **PokéAPI v2** | Comprehensive Pokémon data (**No Auth, 300M+ requests/month**). | No | ✅ | [Link](https://pokeapi.co/docs/v2) |
| **Pokémon TCG** | Pokémon TCG Information. | No | ✅ | [Link](https://pokemontcg.io) |
| **Psychonauts** | Psychonauts World Characters Information and PSI Powers. | No | ✅ | [Link](https://psychonauts-api.netlify.app/) |
| **PUBG** | Game data. | 🔑 ApiKey | ✅ | [Link](https://developer.pubg.com/) |
| **RAWG** | Video games database (500k+ games). | 🔑 ApiKey | ✅ | [Link](https://rawg.io/apidocs) |
| **Rick and Morty** | Show data. | No | ✅ | [Link](https://rickandmortyapi.com) |
| **Riot Games** | League of Legends data. | 🔑 ApiKey | ✅ | [Link](https://developer.riotgames.com/) |
| **RuneScape** | RuneScape and OSRS RPGs information. | No | ✅ | [Link](https://runescape.wiki/w/Application_programming_interface) |
| **Scryfall** | Magic: The Gathering card search. | No | ✅ | [Link](https://scryfall.com/docs/api) |
| **SpaceTradersAPI** | A playable inter-galactic space trading MMOAPI. | 🔐 OAuth | ✅ | [Link](https://spacetraders.io?rel=pub-apis) |
| **Steam** | Steam Web API documentation. | 🔑 ApiKey | ✅ | [Link](https://steamapi.xpaw.me/) |
| **SuperHeroes** | All SuperHeroes and Villains data from all universes under a single API. | 🔑 ApiKey | ✅ | [Link](https://superheroapi.com) |
| **Tarkov API** | Escape from Tarkov items, quests, maps (**No Auth**). | No | ✅ | [Link](https://tarkov.dev/api/) |
| **Tebex** | Tebex API for information about game purchases. | 🔑 ApiKey | ✅ | [Link](https://docs.tebex.io/plugin/) |
| **TETR.IO** | TETR.IO Tetra Channel API. | No | ✅ | [Link](https://tetr.io/about/api/) |
| **Universalis** | Final Fantasy XIV market board data. | No | ✅ | [Link](https://universalis.app/docs/index.html) |
| **Valorant** | Valorant game data (unofficial). | No | ✅ | [Link](https://valorant-api.com/) |
| **Warface (non-official)** | Official API proxy with better data structure and more features. | No | ✅ | [Link](https://api.wfstats.cf) |
| **Wargaming.net** | Wargaming.net info and stats. | 🔑 ApiKey | ✅ | [Link](https://developers.wargaming.net/) |
| **xkcd** | Retrieve xkcd comics as JSON. | No | ✅ | [Link](https://xkcd.com/json.html) |
| **Yu-Gi-Oh!** | Yu-Gi-Oh! card data. | No | ✅ | [Link](https://ygoprodeck.com/api-guide/) |
| **Harry Potter API** | Harry Potter characters, spells, and houses (**No Auth**). | No | ✅ | [Link](https://hp-api.onrender.com/) |
| **SWAPI (py4e)** | Star Wars API — people, planets, starships (**No Auth**, community mirror). | No | ✅ | [Link](https://swapi.py4e.com/) |


[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="geocoding"></a>🌍 Geocoding

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Actinia Grass GIS** | Actinia is an open source REST API for geographical data that uses GRASS GIS. | 🔑 ApiKey | ✅ | [Link](https://actinia-org.github.io/actinia-core/) |
| **adresse.data.gouv.fr** | Address database of France, geocoding and reverse. | No | ✅ | [Link](https://adresse.data.gouv.fr) |
| **Airtel IP** | IP Geolocation API. Collecting data from multiple sources. | No | ✅ | [Link](https://sys.airtel.lv/ip2country/1.1.1.1/?full=true) |
| **Apiip** | Get location information by IP address. | 🔑 ApiKey | ✅ | [Link](https://apiip.net/) |
| **Battuta** | A (country/region/city) in-cascade location API. | 🔑 ApiKey | No | [Link](http://battuta.medunes.net) |
| **BigDataCloud** | Provides fast and accurate IP geolocation APIs along with security checks and... | 🔑 ApiKey | ✅ | [Link](https://www.bigdatacloud.com/docs) |
| **Bing Maps** | Maps, geocoding, and routing APIs. | 🔑 ApiKey | ✅ | [Link](https://www.microsoft.com/maps/) |
| **bng2latlong** | Convert British OSGB36 easting and northing (British National Grid) to WGS84 ... | No | ✅ | [Link](https://www.getthedata.com/bng2latlong) |
| **Cep.la** | Brazil RESTful API to find information about streets, zip codes, neighborhood... | No | No | [Link](http://cep.la/) |
| **CitySDK** | Open APIs for select European cities. | No | ✅ | [Link](http://www.citysdk.eu/citysdk-toolkit/) |
| **Ducks Unlimited** | API explorer that gives a query URL with a JSON response of locations and cities. | No | ✅ | [Link](https://gis.ducks.org/datasets/du-university-chapters/api) |
| **Geoapify** | Forward and reverse geocoding, address autocomplete. | 🔑 ApiKey | ✅ | [Link](https://www.geoapify.com/api/geocoding-api/) |
| **Geocod.io** | Address geocoding / reverse geocoding in bulk. | 🔑 ApiKey | ✅ | [Link](https://www.geocod.io/) |
| **Geocode.xyz** | Provides worldwide forward/reverse geocoding, batch geocoding and geoparsing. | No | ✅ | [Link](https://geocode.xyz/api) |
| **Geocodify.com** | Worldwide geocoding, geoparsing and autocomplete for addresses. | 🔑 ApiKey | ✅ | [Link](https://geocodify.com/) |
| **Geocodio** | Geocoding and reverse geocoding for US/Canada. | 🔑 ApiKey | ✅ | [Link](https://www.geocod.io/docs/) |
| **GeoDataSource** | Geocoding of city name by using latitude and longitude coordinates. | 🔑 ApiKey | ✅ | [Link](https://www.geodatasource.com/web-service) |
| **GeoDB Cities** | Get global city, region, and country data. | 🔑 ApiKey | ✅ | [Link](http://geodb-cities-api.wirefreethought.com/) |
| **GeographQL** | A Country, State, and City GraphQL API. | No | ✅ | [Link](https://geographql.netlify.app) |
| **Geokeo** | Geokeo geocoding service- with 2500 free api requests daily. | No | ✅ | [Link](https://geokeo.com) |
| **geoPlugin** | IP geolocation and currency conversion. | No | ✅ | [Link](https://www.geoplugin.com) |
| **Google Earth Engine** | A cloud-based platform for planetary-scale environmental data analysis. | 🔑 ApiKey | ✅ | [Link](https://developers.google.com/earth-engine/) |
| **Google Maps** | Create/customize digital maps based on Google Maps data. | 🔑 ApiKey | ✅ | [Link](https://developers.google.com/maps/) |
| **HelloSalut** | Get hello translation following user language. | No | ✅ | [Link](https://fourtonfish.com/project/hellosalut-api/) |
| **Hirak IP to Country** | Ip to location with country code, currency code & currency name, fast respons... | 🔑 ApiKey | ✅ | [Link](https://iplocation.hirak.site/) |
| **IBGE** | Aggregate services of IBGE (Brazilian Institute of Geography and Statistics) | No | ✅ | [Link](https://servicodados.ibge.gov.br/api/docs/) |
| **IP 2 Country** | Map an IP to a country. | No | ✅ | [Link](https://ip2country.info) |
| **IP Address Details** | Find geolocation with ip address. | No | ✅ | [Link](https://ipinfo.io/) |
| **IP Geolocation** | Geolocate website visitors from their IPs. | 🔑 ApiKey | ✅ | [Link](https://www.abstractapi.com/ip-geolocation-api) |
| **IP Vigilante** | Free IP Geolocation API. | No | ✅ | [Link](https://www.ipvigilante.com/) |
| **IP-API** | IP to location. | No | No | [Link](https://ip-api.com/docs) |
| **IP2Proxy** | Detect proxy and VPN using IP address. | 🔑 ApiKey | ✅ | [Link](https://www.ip2location.com/web-service/ip2proxy) |
| **ipapi.co** | Find IP address location information. | No | ✅ | [Link](https://ipapi.co/api/#introduction) |
| **ipapi.com** | Real-time Geolocation & Reverse IP Lookup REST API. | 🔑 ApiKey | ✅ | [Link](https://ipapi.com/) |
| **IPGEO** | Unlimited free IP Address API with useful information. | No | ✅ | [Link](https://api.techniknews.net/ipgeo/) |
| **IPInfoDB** | Free Geolocation tools and APIs for country, region, city and time zone looku... | 🔑 ApiKey | ✅ | [Link](https://www.ipinfodb.com/api) |
| **Kakao Maps** | Kakao Maps provide multiple APIs for Korean maps. | 🔑 ApiKey | ✅ | [Link](https://apis.map.kakao.com) |
| **keycdn IP Location Finder** | Get the IP geolocation data through the simple REST API. All the responses ar... | 🔑 ApiKey | ✅ | [Link](https://tools.keycdn.com/geo) |
| **LocationIQ** | Geocoding and maps (free tier: 5000 req/day). | 🔑 ApiKey | ✅ | [Link](https://locationiq.com/docs) |
| **Longdo Map** | Interactive map with detailed places and information portal in Thailand. | 🔑 ApiKey | ✅ | [Link](https://map.longdo.com/docs/) |
| **Mapbox** | Maps and geocoding. | 🔑 ApiKey | ✅ | [Link](https://docs.mapbox.com/) |
| **MapQuest** | To access tools and resources to map the world. | 🔑 ApiKey | ✅ | [Link](https://developer.mapquest.com/) |
| **Nominatim** | OpenStreetMap Geocoding. | No | ✅ | [Link](https://nominatim.org/release-docs/latest/api/Overview/) |
| **One Map, Singapore** | Singapore Land Authority REST API services for Singapore addresses. | 🔑 ApiKey | ✅ | [Link](https://www.onemap.gov.sg/docs/) |
| **OnWater** | Determine if a lat/lon is on water or land. | No | ✅ | [Link](https://onwater.io/) |
| **Open Topo Data** | Elevation and ocean depth for a latitude and longitude. | No | ✅ | [Link](https://www.opentopodata.org) |
| **OpenCage** | Forward and reverse geocoding using open data. | 🔑 ApiKey | ✅ | [Link](https://opencagedata.com) |
| **OpenStreetMap** | Map data. | 🔐 OAuth | ✅ | [Link](http://wiki.openstreetmap.org/wiki/API) |
| **OpenTripMap** | Tourist attractions and points of interest worldwide. | 🔑 ApiKey | ✅ | [Link](https://dev.opentripmap.org/docs) |
| **Pinball Map** | A crowdsourced map of public pinball machines. | No | ✅ | [Link](https://pinballmap.com/api/v1/docs) |
| **Radar** | Geocoding, geofencing, routing, and maps. | 🔑 ApiKey | ✅ | [Link](https://radar.com/documentation/api) |
| **Postali** | Mexico Zip Codes API. | No | ✅ | [Link](https://postali.app/api) |
| **PostcodeData.nl** | Provide geolocation data based on postcode for Dutch addresses. | No | No | [Link](http://api.postcodedata.nl/v1/postcode/?postcode=1211EP&streetnumber=60&ref=domeinnaam.nl&type=json) |
| **Postcodes.io** | Postcode lookup & Geolocation for the UK. | No | ✅ | [Link](https://postcodes.io) |
| **Rwanda Locations** | Rwanda Provences, Districts, Cities, Capital City, Sector, cells, villages an... | No | ✅ | [Link](https://rapidapi.com/victorkarangwa4/api/rwanda) |
| **Telize** | Telize offers location information from any IP address. | 🔑 ApiKey | ✅ | [Link](https://rapidapi.com/fcambus/api/telize/) |
| **TomTom** | Maps, Directions, Places and Traffic APIs. | 🔑 ApiKey | ✅ | [Link](https://developer.tomtom.com/) |
| **Uebermaps** | Discover and share maps with friends. | 🔑 ApiKey | ✅ | [Link](https://uebermaps.com/api/v2) |
| **US ZipCode** | Validate and append data for any US ZipCode. | 🔑 ApiKey | ✅ | [Link](https://www.smarty.com/docs/cloud/us-zipcode-api) |
| **Utah AGRC** | Utah Web API for geocoding Utah addresses. | 🔑 ApiKey | ✅ | [Link](https://api.mapserv.utah.gov) |
| **ViaCep** | Brazil RESTful zip codes API. | No | ✅ | [Link](https://viacep.com.br) |
| **What3Words** | Three words as rememberable and unique coordinates worldwide. | 🔑 ApiKey | ✅ | [Link](https://what3words.com) |
| **Yandex.Maps Geocoder** | Use geocoding to get an object's coordinates from its address. | 🔑 ApiKey | ✅ | [Link](https://yandex.com/dev/maps/geocoder) |
| **ZipCodeAPI** | US zip code distance, radius and location API. | 🔑 ApiKey | ✅ | [Link](https://www.zipcodeapi.com) |
| **Zippopotam.us** | Postal/zip code lookup for 60+ countries (**No Auth**). | No | ✅ | [Link](https://api.zippopotam.us/) |
| **Ziptastic** | Get the country, state, and city of any US zip-code. | No | ✅ | [Link](https://ziptasticapi.com/) |
| **Geocode.maps.co** | Free geocoding and reverse geocoding (**No Auth**). | No | ✅ | [Link](https://geocode.maps.co/) |


[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="health"></a>❤️ Health

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **BMI Calculator** | Calculate BMI and other metrics. | 🔑 ApiKey | ✅ | [Link](https://rapidapi.com/navii/api/bmi-calculator/) |
| **ClinicalTrials.gov** | Clinical trials database (**No Auth**). | No | ✅ | [Link](https://clinicaltrials.gov/data-api/api) |
| **CMS.gov** | Access to the data from the CMS - medicare.gov. | 🔑 ApiKey | ✅ | [Link](https://data.cms.gov/provider-data/) |
| **Coronavirus** | HTTP API for Latest Covid-19 Data. | No | ✅ | [Link](https://pipedream.com/@pravin/http-api-for-latest-wuhan-coronavirus-data-2019-ncov-p_G6CLVM/readme) |
| **Coronavirus in the UK** | UK Government coronavirus data, including deaths and cases by region. | No | ✅ | [Link](https://coronavirus.data.gov.uk/details/developers-guide) |
| **Covid Tracking Project** | Covid-19  data for the US. | No | ✅ | [Link](https://covidtracking.com/data/api/version-2) |
| **Covid-19 Datenhub** | Maps, datasets, applications and more in the context of COVID-19. | No | ✅ | [Link](https://npgeo-corona-npgeo-de.hub.arcgis.com) |
| **Covid-19 Government Response** | Government measures tracker to fight against the Covid-19 pandemic. | No | ✅ | [Link](https://covidtracker.bsg.ox.ac.uk) |
| **Covid-19 India** | Covid 19 statistics state and district wise about cases, vaccinations, recove... | No | ✅ | [Link](https://data.covid19india.org/) |
| **Covid-19 JHU CSSE** | Open-source API for exploring Covid19 cases based on JHU CSSE. | No | ✅ | [Link](https://nuttaphat.com/covid19-api/) |
| **COVID-19 Tracker Canada** | Details on Covid-19 cases across Canada. | No | ✅ | [Link](https://api.covid19tracker.ca/docs/1.0/overview) |
| **Dataflow Kit COVID-19** | COVID-19 live statistics into sites per hour. | No | ✅ | [Link](https://covid-19.dataflowkit.com) |
| **Disease.sh** | COVID-19 and disease statistics (**No Auth**). | No | ✅ | [Link](https://disease.sh/) |
| **Edamam Nutrition** | Nutrition analysis. | 🔑 ApiKey | ✅ | [Link](https://developer.edamam.com/edamam-nutrition-api) |
| **ExerciseDB** | Exercise data with images and animations. | 🔑 ApiKey | ✅ | [Link](https://rapidapi.com/justin-WFnsXH_t6/api/exercisedb) |
| **FoodData Central** | National Nutrient Database for Standard Reference. | 🔑 ApiKey | ✅ | [Link](https://fdc.nal.usda.gov/) |
| **Healthcare.gov** | Educational content about the US Health Insurance Marketplace. | No | ✅ | [Link](https://www.healthcare.gov/developers/) |
| **HealthData.gov** | Public US health datasets and data portal. | No | ✅ | [Link](https://healthdata.gov/) |
| **Humanitarian Data Exchange** | Humanitarian Data Exchange (HDX) is open platform for sharing data across cri... | No | ✅ | [Link](https://data.humdata.org/) |
| **Infermedica** | NLP based symptom checker and patient triage API for health diagnosis from text. | 🔑 ApiKey | ✅ | [Link](https://developer.infermedica.com/docs/) |
| **LAPIS** | SARS-CoV-2 genomic sequences from public sources. | No | ✅ | [Link](https://cov-spectrum.ethz.ch/public) |
| **Lexigram** | NLP that extracts mentions of clinical concepts from text, gives access to cl... | 🔑 ApiKey | ✅ | [Link](https://docs.lexigram.io/) |
| **MyVaccination** | Vaccination data for Malaysia. | No | ✅ | [Link](https://documenter.getpostman.com/view/16605343/Tzm8GG7u) |
| **NPI Registry** | US healthcare provider registry search. | No | ✅ | [Link](https://clinicaltables.nlm.nih.gov/apidoc/npi_org/v3/doc.html) |
| **NPPES** | National Plan & Provider Enumeration System, info on healthcare providers reg... | No | ✅ | [Link](https://npiregistry.cms.hhs.gov/registry/help-api) |
| **Nutritionix** | Nutrition database. | 🔑 ApiKey | ✅ | [Link](https://developer.nutritionix.com/) |
| **Open Data NHS Scotland** | Medical reference data and statistics by Public Health Scotland. | No | ✅ | [Link](https://www.opendata.nhs.scot) |
| **OpenFDA** | Public FDA data about drugs, devices, and foods. | No | ✅ | [Link](https://open.fda.gov/apis/) |
| **Orion Health** | Medical platform which allows the development of applications for different h... | 🔐 OAuth | ✅ | [Link](https://developer.orionhealth.io/) |
| **PubChem** | Chemical compound data. | No | ✅ | [Link](https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest) |
| **RxNav** | Drug vocabularies and interaction data. | No | ✅ | [Link](https://lhncbc.nlm.nih.gov/RxNav/APIs/index.html) |
| **WGER** | Open source workout manager API. | No | ✅ | [Link](https://wger.de/en/software/api) |
| **WHO GHO** | World Health Organization health data (**No Auth**). | No | ✅ | [Link](https://www.who.int/data/gho/info/gho-odata-api) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="machine-learning"></a>🧠 Machine Learning

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **AI For Thai** | Free Various Thai AI API. | 🔑 ApiKey | ✅ | [Link](https://aiforthai.in.th/index.php) |
| **AI21 Labs** | Powerful language models (free tier). | 🔑 ApiKey | ✅ | [Link](https://docs.ai21.com/) |
| **Anthropic Claude** | Access Claude AI models (offers free trial credits). | 🔑 ApiKey | ✅ | [Link](https://www.anthropic.com/api) |
| **Clarifai** | Computer Vision. | 🔐 OAuth | ✅ | [Link](https://docs.clarifai.com/api-guide/api-overview) |
| **Cloudmersive** | Image Recognition. | 🔑 ApiKey | ✅ | [Link](https://www.cloudmersive.com/image-recognition-and-processing-api) |
| **Cohere** | NLP and text generation models (free trial tier). | 🔑 ApiKey | ✅ | [Link](https://docs.cohere.com/) |
| **DeepAI** | Simple APIs for image generation and text processing. | 🔑 ApiKey | ✅ | [Link](https://deepai.org/api-docs) |
| **Deepcode** | AI for code review. | No | ✅ | [Link](https://www.deepcode.ai) |
| **Deepgram** | Speech-to-text and audio intelligence. | 🔑 ApiKey | ✅ | [Link](https://deepgram.com/) |
| **DeepSeek** | Powerful reasoning AI models with free API tier. | 🔑 ApiKey | ✅ | [Link](https://platform.deepseek.com/) |
| **Dialogflow** | Conversational AI. | 🔑 ApiKey | ✅ | [Link](https://cloud.google.com/dialogflow/docs/) |
| **ElevenLabs** | AI voice generation and text-to-speech. | 🔑 ApiKey | ✅ | [Link](https://elevenlabs.io/docs/api-reference) |
| **EXUDE-API** | Used for the primary ways for filtering the stopping, stemming words from the... | No | ✅ | [Link](http://uttesh.com/exude-api/) |
| **Fal.ai** | Run AI models in serverless GPU (image/video generation). | 🔑 ApiKey | ✅ | [Link](https://fal.ai/docs) |
| **Fireworks AI** | Fast inference for open-source LLMs. | 🔑 ApiKey | ✅ | [Link](https://docs.fireworks.ai/) |
| **Cerebras Inference** | Extremely fast LLM inference platform. | 🔑 ApiKey | ✅ | [Link](https://inference-docs.cerebras.ai/) |
| **Google Gemini** | Google's latest multimodal AI models. | 🔑 ApiKey | ✅ | [Link](https://ai.google.dev/) |
| **Groq** | Ultra-fast LLM inference API. | 🔑 ApiKey | ✅ | [Link](https://groq.com/) |
| **Hirak FaceAPI** | Face detection, face recognition with age estimation/gender estimation, accur... | 🔑 ApiKey | ✅ | [Link](https://faceapi.hirak.site/) |
| **Hugging Face** | Access thousands of models for NLP, vision, and audio. | 🔑 ApiKey | ✅ | [Link](https://huggingface.co/docs/api-inference/index) |
| **Ideogram** | Text-to-image generation with strong typography. | 🔑 ApiKey | ✅ | [Link](https://developer.ideogram.ai/) |
| **Imagga** | Image Recognition. | 🔑 ApiKey | ✅ | [Link](https://imagga.com/) |
| **Inferdo** | Computer Vision services like Facial detection, Image labeling, NSFW classifi... | 🔑 ApiKey | ✅ | [Link](https://rapidapi.com/user/inferdo) |
| **Irisnet** | Realtime content moderation API that blocks or blurs unwanted images in real-... | 🔑 ApiKey | ✅ | [Link](https://irisnet.de/api/) |
| **Keen IO** | Data Analytics. | 🔑 ApiKey | ✅ | [Link](https://keen.io/) |
| **Languagelayer** | Language detection. | 🔑 ApiKey | ✅ | [Link](https://languagelayer.com/) |
| **LiveKit** | Realtime audio, video, and data infrastructure. | 🔑 ApiKey | ✅ | [Link](https://docs.livekit.io/) |
| **Luma Dream Machine** | Text-to-video generation API. | 🔑 ApiKey | ✅ | [Link](https://docs.lumalabs.ai/) |
| **MessengerX.io** | A FREE API for developers to build and monetize personalized ML based chat apps. | 🔑 ApiKey | ✅ | [Link](https://messengerx.rtfd.io) |
| **Mistral AI** | High-performance open-source LLMs (free tier available). | 🔑 ApiKey | ✅ | [Link](https://docs.mistral.ai/) |
| **NLP Cloud** | NLP. | 🔑 ApiKey | ✅ | [Link](https://nlpcloud.io) |
| **OpenAI** | Access GPT models (offers free trial credits). | 🔑 ApiKey | ✅ | [Link](https://platform.openai.com/docs) |
| **Perplexity AI** | AI-powered search and answers (limited free tier). | 🔑 ApiKey | ✅ | [Link](https://docs.perplexity.ai/) |
| **Perspective** | NLP API to return probability that if text is toxic, obscene, insulting or th... | 🔑 ApiKey | ✅ | [Link](https://perspectiveapi.com) |
| **Recraft** | AI image generation API with style controls. | 🔑 ApiKey | ✅ | [Link](https://www.recraft.ai/docs) |
| **Replicate** | Run AI models via API (pay-as-you-go, free credits). | 🔑 ApiKey | ✅ | [Link](https://replicate.com/docs) |
| **Roboflow** | Computer Vision. | 🔑 ApiKey | ✅ | [Link](https://universe.roboflow.com) |
| **Runway ML** | Generative AI for video and image. | 🔑 ApiKey | ✅ | [Link](https://docs.dev.runwayml.com/) |
| **SkyBiometry** | Face Detection, Face Recognition and Face Grouping. | 🔑 ApiKey | ✅ | [Link](https://skybiometry.com/documentation/) |
| **Stability AI** | Image generation (Stable Diffusion). | 🔑 ApiKey | ✅ | [Link](https://platform.stability.ai/docs/api-reference) |
| **Suno AI** | AI music generation API. | 🔑 ApiKey | ✅ | [Link](https://suno.com/) |
| **Tavily** | AI-powered search API for agents. | 🔑 ApiKey | ✅ | [Link](https://tavily.com/) |
| **Time Door** | A time series analysis API. | 🔑 ApiKey | ✅ | [Link](https://timedoor.io) |
| **Together AI** | Fast inference for open-source LLMs (free credits). | 🔑 ApiKey | ✅ | [Link](https://docs.together.ai/) |
| **Vapi** | Voice AI agent platform for developers. | 🔑 ApiKey | ✅ | [Link](https://docs.vapi.ai/) |
| **Twinword Sentiment Analysis** | Sentiment analysis, emotion analysis, and more. | 🔑 ApiKey | ✅ | [Link](https://www.twinword.com/api/sentiment-analysis.php) |
| **Unplugg** | Forecasting API for timeseries data. | 🔑 ApiKey | ✅ | [Link](https://unplu.gg/test_api.html) |
| **WolframAlpha** | Computational Knowledge. | 🔑 ApiKey | ✅ | [Link](https://products.wolframalpha.com/api/) |
| **xAI Grok** | xAI's Grok model API (free tier available). | 🔑 ApiKey | ✅ | [Link](https://x.ai/api) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="mock-data-testing"></a>🧪 Mock Data & Testing

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Bacon Ipsum** | A Meatier Lorem Ipsum Generator. | No | ✅ | [Link](https://baconipsum.com/json-api/) |
| **Beeceptor** | Mock REST APIs in seconds (**No Auth**). | No | ✅ | [Link](https://beeceptor.com/) |
| **DummyJSON** | Fake REST API with products, users, todos, and more (**No Auth**). | No | ✅ | [Link](https://dummyjson.com/) |
| **Fake Store API** | Free fake e-commerce API for testing (products, carts, users). | No | ✅ | [Link](https://fakestoreapi.com/) |
| **FakeJSON** | Service to generate test and fake data. | 🔑 ApiKey | ✅ | [Link](https://fakejson.com) |
| **GeneradorDNI** | Data generator API. Profiles, vehicles, banks and cards, etc. | 🔑 ApiKey | ✅ | [Link](https://api.generadordni.es) |
| **Httpbin** | HTTP request and response testing (**No Auth**). | No | ✅ | [Link](https://httpbin.org/) |
| **ItsThisForThat** | Generate Random startup ideas. | No | ✅ | [Link](https://itsthisforthat.com/api.php) |
| **JSONPlaceholder** | Free fake API for testing and prototyping (posts, comments, users). | No | ✅ | [Link](https://jsonplaceholder.typicode.com/) |
| **Mailsac** | Disposable Email. | 🔑 ApiKey | ✅ | [Link](https://mailsac.com/docs/api) |
| **MockAPI.io** | Create custom mock REST APIs with fake data. | 🔑 ApiKey | ✅ | [Link](https://mockapi.io/docs) |
| **Mockaroo** | Generate custom realistic test data in JSON, CSV, SQL. | 🔑 ApiKey | ✅ | [Link](https://www.mockaroo.com/) |
| **Postman Echo** | Test REST clients with echo endpoint (**No Auth**). | No | ✅ | [Link](https://www.postman-echo.com/) |
| **Randommer** | Random data generator. | 🔑 ApiKey | ✅ | [Link](https://randommer.io/randommer-api) |
| **RandomUser.me** | Generate random user data (like Lorem Ipsum, but for people). | No | ✅ | [Link](https://randomuser.me/) |
| **ReqRes** | A hosted REST-API ready to respond to your AJAX requests. | No | ✅ | [Link](https://reqres.in/) |
| **SampleAPIs** | Playground for RESTful and GraphQL endpoints (**No Auth**). | No | ✅ | [Link](https://api.sampleapis.com/) |
| **This Person Does not Exist** | Generates real-life faces of people who do not exist. | No | ✅ | [Link](https://thispersondoesnotexist.com) |
| **What The Commit** | Random commit message generator. | No | No | [Link](http://whatthecommit.com/index.txt) |
| **Yes No** | Generate yes or no randomly. | No | ✅ | [Link](https://yesno.wtf/api) |
| **JokeAPI v2** | Programming, dark, pun, and miscellaneous jokes with filters (**No Auth**). | No | ✅ | [Link](https://v2.jokeapi.dev/) |


[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="music"></a>🎵 Music

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **7digital** | Api of Music store 7digital. | 🔐 OAuth | ✅ | [Link](https://docs.7digital.com/reference) |
| **AI Mastering** | Automated Music Mastering. | 🔑 ApiKey | ✅ | [Link](https://aimastering.com/api_docs/) |
| **Audiomack** | Music streaming. | 🔐 OAuth | ✅ | [Link](https://www.audiomack.com/data-api/docs) |
| **Bandcamp** | API of Music store Bandcamp. | 🔐 OAuth | ✅ | [Link](https://bandcamp.com/developer) |
| **Bandsintown** | Music Events. | No | ✅ | [Link](https://app.swaggerhub.com/apis/Bandsintown/PublicAPI/3.0.0) |
| **Deezer** | Music streaming. | 🔐 OAuth | ✅ | [Link](https://developers.deezer.com/api) |
| **Discogs** | Music database. | 🔐 OAuth | ✅ | [Link](https://www.discogs.com/developers/) |
| **Freesound** | Music Samples. | 🔑 ApiKey | ✅ | [Link](https://freesound.org/docs/api/) |
| **Genius** | Lyrics and knowledge. | 🔐 OAuth | ✅ | [Link](https://docs.genius.com/) |
| **Genrenator** | Music genre generator. | No | ✅ | [Link](https://binaryjazz.us/genrenator-api/) |
| **iTunes Search** | Search iTunes store for music, movies, apps (**No Auth**). | No | ✅ | [Link](https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/) |
| **Jamendo** | Free music licensing and streaming. | 🔐 OAuth | ✅ | [Link](https://developer.jamendo.com/v3.0) |
| **KKBOX** | Get music libraries, playlists, charts, and perform out of KKBOX's platform. | 🔐 OAuth | ✅ | [Link](https://developer.kkbox.com) |
| **LastFm** | Music database. | 🔑 ApiKey | ✅ | [Link](https://www.last.fm/api) |
| **ListenBrainz** | Open-source music stats and listening history. | 🔑 ApiKey | ✅ | [Link](https://listenbrainz.readthedocs.io/en/latest/users/api/) |
| **Lyrics.ovh** | Simple lyrics search API (**No Auth**). | No | ✅ | [Link](https://lyricsovh.docs.apiary.io/) |
| **Mixcloud** | Music streaming. | 🔐 OAuth | ✅ | [Link](https://www.mixcloud.com/developers/) |
| **MusicBrainz** | Music database. | No | ✅ | [Link](https://musicbrainz.org/doc/Development/XML_Web_Service/Version_2) |
| **Musixmatch** | Lyrics. | 🔑 ApiKey | ✅ | [Link](https://developer.musixmatch.com/) |
| **Openwhyd** | Download curated playlists of streaming tracks (YouTube, SoundCloud, etc...) | No | ✅ | [Link](https://openwhyd.github.io/openwhyd/API) |
| **Phishin** | A web-based archive of legal live audio recordings of the improvisational roc... | 🔑 ApiKey | ✅ | [Link](https://phish.in/api-docs) |
| **Radio Browser** | Community database of internet radio stations (**No Auth**). | No | ✅ | [Link](https://api.radio-browser.info/) |
| **Setlist.fm** | Concert setlist data. | 🔑 ApiKey | ✅ | [Link](https://api.setlist.fm/docs/1.0/index.html) |
| **Shazam (RapidAPI)** | Music recognition and track details. | 🔑 ApiKey | ✅ | [Link](https://rapidapi.com/apidojo/api/shazam) |
| **Songkick** | Music Events. | 🔑 ApiKey | ✅ | [Link](https://www.songkick.com/developer/) |
| **Songlink / Odesli** | Get all the services on which a song is available. | 🔑 ApiKey | ✅ | [Link](https://www.notion.so/API-d0ebe08a5e304a55928405eb682f6741) |
| **Songsterr** | Provides guitar, bass and drums tabs and chords. | No | ✅ | [Link](https://www.songsterr.com/a/wa/api/) |
| **SoundCloud** | Music streaming. | 🔐 OAuth | ✅ | [Link](https://developers.soundcloud.com/docs/api/guide) |
| **Spotify** | Music streaming. | 🔐 OAuth | ✅ | [Link](https://beta.developer.spotify.com/documentation/web-api/) |
| **TasteDive** | Similar artist API (also works for movies and TV shows) | 🔑 ApiKey | ✅ | [Link](https://tastedive.com/read/api) |
| **TheAudioDB** | Music metadata, charts, and more. | 🔑 ApiKey | ✅ | [Link](https://www.theaudiodb.com/api) |


[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="news"></a>📰 News

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Currents** | Latest news. | 🔑 ApiKey | ✅ | [Link](https://currentsapi.services/en) |
| **Dev.to** | Developer community articles (**No Auth**). | No | ✅ | [Link](https://developers.forem.com/api) |
| **GNews** | Global news search. | 🔑 ApiKey | ✅ | [Link](https://gnews.io/) |
| **NewsAPI** | Headlines and articles. | 🔑 ApiKey | ✅ | [Link](https://newsapi.org/) |
| **NewsAPI.ai** | AI-powered news API. | 🔑 ApiKey | ✅ | [Link](https://newsapi.ai/) |
| **NewsData.io** | News search and tracking. | 🔑 ApiKey | ✅ | [Link](https://newsdata.io/) |
| **The Guardian** | Guardian articles. | 🔑 ApiKey | ✅ | [Link](https://open-platform.theguardian.com/) |
| **TheNewsAPI** | Global news API. | 🔑 ApiKey | ✅ | [Link](https://www.thenewsapi.com/) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="photography"></a>📷 Photography

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **apilayer mediastack** | Free, Simple REST API for Live News & Blog Articles. | 🔑 ApiKey | ✅ | [Link](https://mediastack.com/) |
| **APITemplate.io** | Dynamically generate images and PDFs from templates with a simple API. | 🔑 ApiKey | ✅ | [Link](https://apitemplate.io) |
| **Art Institute of Chicago** | Museum artwork data (**No Auth**). | No | ✅ | [Link](https://api.artic.edu/docs/) |
| **Associated Press** | Search for news and metadata from Associated Press. | 🔑 ApiKey | ✅ | [Link](https://developer.ap.org/) |
| **Bannerbear** | Auto-generate images and videos programmatically. | 🔑 ApiKey | ✅ | [Link](https://developers.bannerbear.com/) |
| **CheetahO** | Photo optimization and resize. | 🔑 ApiKey | ✅ | [Link](https://cheetaho.com/docs/getting-started/) |
| **Chronicling America** | Provides access to millions of pages of historic US newspapers from the Libra... | No | No | [Link](http://chroniclingamerica.loc.gov/about/api/) |
| **Dagpi** | Image manipulation and processing. | 🔑 ApiKey | ✅ | [Link](https://dagpi.xyz) |
| **DynaPictures** | Generate Hundreds of Personalized Images in Minutes. | 🔑 ApiKey | ✅ | [Link](https://dynapictures.com/docs/) |
| **Flickr** | Photo sharing and management. | 🔑 ApiKey | ✅ | [Link](https://www.flickr.com/services/api/) |
| **Getty Images** | Build applications using the world's most powerful imagery. | 🔐 OAuth | ✅ | [Link](http://developers.gettyimages.com/en/) |
| **Giphy** | GIFs. | 🔑 ApiKey | ✅ | [Link](https://developers.giphy.com/docs/) |
| **Google Photos** | Integrate Google Photos with your apps or devices. | 🔐 OAuth | ✅ | [Link](https://developers.google.com/photos) |
| **Image Upload** | Image Optimization. | 🔑 ApiKey | ✅ | [Link](https://apilayer.com/marketplace/image_upload-api) |
| **Imgix** | Real-time image processing and optimization. | 🔑 ApiKey | ✅ | [Link](https://docs.imgix.com/) |
| **Imgur** | Images. | 🔐 OAuth | ✅ | [Link](https://apidocs.imgur.com/) |
| **MarketAux** | Live stock market news with tagged tickers + sentiment and stats JSON API. | 🔑 ApiKey | ✅ | [Link](https://www.marketaux.com/) |
| **Met Museum** | Metropolitan Museum of Art collection (**No Auth**). | No | ✅ | [Link](https://metmuseum.github.io/) |
| **NASA Image Library** | NASA's image and video library (**No Auth**). | No | ✅ | [Link](https://images.nasa.gov/docs/images.nasa.gov_api_docs.pdf) |
| **New York Times** | The New York Times Developer Network. | 🔑 ApiKey | ✅ | [Link](https://developer.nytimes.com/) |
| **NewsData** | News data API for live-breaking news and headlines from reputed  news sources. | 🔑 ApiKey | ✅ | [Link](https://newsdata.io/docs) |
| **NewsX** | Get or Search Latest Breaking News with ML Powered Summaries 🤖. | 🔑 ApiKey | ✅ | [Link](https://rapidapi.com/machaao-inc-machaao-inc-default/api/newsx/) |
| **ObjectCut** | Image Background removal. | 🔑 ApiKey | ✅ | [Link](https://objectcut.com/) |
| **Pexels** | Free stock photos. | 🔑 ApiKey | ✅ | [Link](https://www.pexels.com/api/) |
| **PhotoRoom** | Remove background from images. | 🔑 ApiKey | ✅ | [Link](https://www.photoroom.com/api/) |
| **Picsum Photos** | The Lorem Ipsum for photos. | No | ✅ | [Link](https://picsum.photos/) |
| **Pixabay** | Free stock photos and videos. | 🔑 ApiKey | ✅ | [Link](https://pixabay.com/api/docs/) |
| **Placeholder** | Custom placeholder images (**No Auth**). | No | ✅ | [Link](https://placeholder.com/) |
| **PlaceKeanu** | Resizable Keanu Reeves placeholder images with grayscale and young Keanu options. | No | ✅ | [Link](https://placekeanu.com/) |
| **Remove.bg** | AI background removal from images. | 🔑 ApiKey | ✅ | [Link](https://www.remove.bg/api) |
| **ReSmush.it** | Photo optimization. | No | No | [Link](https://resmush.it/api) |
| **shutterstock** | Stock Photos and Videos. | 🔐 OAuth | ✅ | [Link](https://api-reference.shutterstock.com/) |
| **Sirv** | Image management solutions like optimization, manipulation, hosting. | 🔑 ApiKey | ✅ | [Link](https://apidocs.sirv.com/) |
| **Spaceflight News** | Spaceflight related news 🚀. | No | ✅ | [Link](https://spaceflightnewsapi.net) |
| **Trove** | Search through the National Library of Australia collection of 1000s of digit... | 🔑 ApiKey | ✅ | [Link](https://trove.nla.gov.au/about/create-something/using-api) |
| **Unsplash** | High-quality photos. | 🔐 OAuth | ✅ | [Link](https://unsplash.com/developers) |
| **Wallhaven** | Wallpapers. | 🔑 ApiKey | ✅ | [Link](https://wallhaven.cc/help/api) |
| **Webdam** | Images. | 🔐 OAuth | ✅ | [Link](https://www.damsuccess.com/hc/en-us/articles/202134055-REST-API) |
| **DiceBear** | Generate unique avatar images from any seed string (**No Auth**). | No | ✅ | [Link](https://www.dicebear.com/introduction/) |


[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="science"></a>🔬 Science & Space

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **arcsecond.io** | Multiple astronomy data sources. | No | ✅ | [Link](https://api.arcsecond.io/) |
| **arXiv** | Scientific paper search and metadata (**No Auth**). | No | ✅ | [Link](https://arxiv.org/help/api) |
| **Astronomy API** | Astronomy calculations and celestial data. | 🔑 ApiKey | ✅ | [Link](https://astronomyapi.com/) |
| **CelesTrak** | Satellite orbital data (TLE) and space situational awareness. | No | ✅ | [Link](https://celestrak.org/) |
| **CORE** | Access the world's Open Access research papers. | 🔑 ApiKey | ✅ | [Link](https://core.ac.uk/services#api) |
| **GBIF** | Global biodiversity occurrence data (**No Auth**). | No | ✅ | [Link](https://www.gbif.org/developer/summary) |
| **isEven (humor)** | Check if a number is even. | No | ✅ | [Link](https://isevenapi.xyz/) |
| **ISRO** | ISRO Space Crafts Information. | No | ✅ | [Link](https://isro.vercel.app) |
| **ISS Location** | Real-time International Space Station location (**No Auth**). | No | ✅ | [Link](http://open-notify.org/Open-Notify-API/ISS-Location-Now/) |
| **ITIS** | Integrated Taxonomic Information System. | No | ✅ | [Link](https://www.itis.gov/ws_description.html) |
| **Launch Library** | Rocket launch schedules and information. | No | ✅ | [Link](https://thespacedevs.com/llapi) |
| **Materials Platform for Data Science** | Curated experimental data for materials science. | 🔑 ApiKey | ✅ | [Link](https://mpds.io) |
| **Minor Planet Center** | Asterank.com Information. | No | No | [Link](http://www.asterank.com/mpc) |
| **NASA ADS** | NASA Astrophysics Data System. | 🔐 OAuth | ✅ | [Link](https://ui.adsabs.harvard.edu/help/api/api-docs.html) |
| **NASA API** | Access NASA data, including Astronomy Picture of the Day (APOD). | 🔑 ApiKey | ✅ | [Link](https://api.nasa.gov/) |
| **NOAA Tides & Currents** | US tides, currents, and water level data. | No | ✅ | [Link](https://api.tidesandcurrents.noaa.gov/api/prod/) |
| **Newton** | Symbolic and arithmetic math calculator API (**No Auth**). | No | ✅ | [Link](https://newton.vercel.app/) |
| **Noctua** | REST API used to access NoctuaSky features. | No | ✅ | [Link](https://api.noctuasky.com/api/v1/swaggerdoc/) |
| **Numbers** | Number of the day, random number, number facts and anything else you want to ... | 🔑 ApiKey | ✅ | [Link](https://math.tools/api/numbers/) |
| **Open Notify** | ISS astronauts, current location, etc. | No | No | [Link](http://open-notify.org/Open-Notify-API/) |
| **Open Science Framework** | Open source research management platform. | 🔐 OAuth | ✅ | [Link](https://developer.osf.io/) |
| **People in Space** | Current number of people in space (**No Auth**). | No | ✅ | [Link](http://open-notify.org/Open-Notify-API/People-In-Space/) |
| **Purple Air** | Real Time Air Quality Monitoring. | No | ✅ | [Link](https://www2.purpleair.com/) |
| **SHARE** | A free, open, dataset about research and scholarly activities. | No | ✅ | [Link](https://share.osf.io/api/v2/) |
| **Solar System OpenData** | Solar system planets and moons data (**No Auth**). | No | ✅ | [Link](https://api.le-systeme-solaire.net/en/) |
| **TLE** | Satellite information. | No | ✅ | [Link](https://tle.ivanstanojevic.me/#/docs) |
| **USGS Earthquake** | Real-time earthquake data (**No Auth**). | No | ✅ | [Link](https://earthquake.usgs.gov/fdsnws/event/1/) |
| **USGS Water Services** | Water quality and level info for rivers and lakes. | No | ✅ | [Link](https://waterservices.usgs.gov/) |
| **Where the ISS at** | Real-time ISS position, velocity and visibility (**No Auth**). | No | ✅ | [Link](https://wheretheiss.at/w/developer) |
| **Wolfram Short Answers** | Computational knowledge answers. | 🔑 ApiKey | ✅ | [Link](https://products.wolframalpha.com/short-answers-api/documentation) |
| **SpaceX API** | SpaceX launches, rockets, capsules, and Starlink data (**No Auth**). | No | ✅ | [Link](https://github.com/r-spacex/SpaceX-API) |
| **Launch Library 2** | Upcoming and historical rocket launches worldwide (**No Auth**). | No | ✅ | [Link](https://thespacedevs.com/llapi) |
| **Where the ISS at?** | Real-time International Space Station position tracking (**No Auth**). | No | ✅ | [Link](https://wheretheiss.at/w/developer) |
| **Sunrise Sunset** | Sunrise and sunset times for any location (**No Auth**). | No | ✅ | [Link](https://sunrise-sunset.org/api) |


[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="security-validation"></a>🔐 Security & Validation

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **BinaryEdge** | Provide access to BinaryEdge 40fy scanning platform. | 🔑 ApiKey | ✅ | [Link](https://docs.binaryedge.io/api-v2.html) |
| **BitWarden** | Best open-source password manager. | 🔐 OAuth | ✅ | [Link](https://bitwarden.com/help/api/) |
| **Bugcrowd** | Bugcrowd API for interacting and tracking the reported issues programmatically. | 🔑 ApiKey | ✅ | [Link](https://docs.bugcrowd.com/api/getting-started/) |
| **Censys** | Search engine for Internet connected host and devices. | 🔑 ApiKey | ✅ | [Link](https://search.censys.io/api) |
| **CertSpotter** | Certificate transparency monitoring. | No | ✅ | [Link](https://sslmate.com/certspotter/api/) |
| **Cloudflare Turnstile** | Privacy-first CAPTCHA alternative. | 🔑 ApiKey | ✅ | [Link](https://developers.cloudflare.com/turnstile/) |
| **Complete Criminal Checks** | Provides data of offenders from all U.S. States and Pureto Rico. | 🔑 ApiKey | ✅ | [Link](https://completecriminalchecks.com/Developers) |
| **EmailRep** | Email address threat and risk prediction. | No | ✅ | [Link](https://docs.emailrep.io/) |
| **FilterLists** | Lists of filters for adblockers and firewalls. | No | ✅ | [Link](https://filterlists.com) |
| **FingerprintJS Pro** | Fraud detection API offering highly accurate browser fingerprinting. | 🔑 ApiKey | ✅ | [Link](https://dev.fingerprintjs.com/docs) |
| **FraudLabs Pro** | Screen order information using AI to detect frauds. | 🔑 ApiKey | ✅ | [Link](https://www.fraudlabspro.com/developer/api/screen-order) |
| **FullHunt** | Attack surface discovery and monitoring. | 🔑 ApiKey | ✅ | [Link](https://api-docs.fullhunt.io/) |
| **Google reCAPTCHA** | Bot protection and CAPTCHA service. | 🔑 ApiKey | ✅ | [Link](https://developers.google.com/recaptcha) |
| **GreyNoise** | Query IPs in the GreyNoise dataset and retrieve a subset of the full IP conte... | 🔑 ApiKey | ✅ | [Link](https://docs.greynoise.io/reference) |
| **HackerOne** | The industry’s first hacker API that helps increase productivity towards crea... | 🔑 ApiKey | ✅ | [Link](https://api.hackerone.com/) |
| **HaveIBeenPwned** | Check if email or password has been compromised in a data breach. | 🔑 ApiKey | ✅ | [Link](https://haveibeenpwned.com/API/v3) |
| **IP Quality Score** | IP reputation, fraud prevention, and email validation. | 🔑 ApiKey | ✅ | [Link](https://www.ipqualityscore.com/documentation/overview) |
| **LoginRadius** | Managed User Authentication Service. | 🔑 ApiKey | ✅ | [Link](https://www.loginradius.com/docs/) |
| **Mozilla Observatory** | Website security analysis (**No Auth**). | No | ✅ | [Link](https://observatory.mozilla.org/) |
| **MSRC** | Microsoft vulnerability and CVRF data feeds. | No | ✅ | [Link](https://msrc.microsoft.com/report/developer) |
| **MXToolbox** | Domain, DNS, and blacklist lookups. | 🔑 ApiKey | ✅ | [Link](https://mxtoolbox.com/restapi.aspx) |
| **National Vulnerability Database** | U.S. National Vulnerability Database. | No | ✅ | [Link](https://nvd.nist.gov/vuln/Data-Feeds/JSON-feed-changelog) |
| **OSV** | Open source vulnerability database and API (**No Auth**). | No | ✅ | [Link](https://google.github.io/osv.dev/) |
| **PhishStats** | Phishing database. | No | ✅ | [Link](https://phishstats.info/) |
| **Privacy.com** | Generate merchant-specific and one-time use credit card numbers that link bac... | 🔑 ApiKey | ✅ | [Link](https://privacy.com/developer/docs) |
| **Pulsedive** | Scan, search and collect threat intelligence data in real-time. | 🔑 ApiKey | ✅ | [Link](https://pulsedive.com/api/) |
| **SecurityTrails** | Domain and DNS intelligence. | 🔑 ApiKey | ✅ | [Link](https://securitytrails.com/corp/api) |
| **Shodan** | Internet-connected devices search engine. | 🔑 ApiKey | ✅ | [Link](https://developer.shodan.io/) |
| **Spyse** | Access data on all Internet assets and build powerful attack surface manageme... | 🔑 ApiKey | ✅ | [Link](https://spyse-dev.readme.io/reference/quick-start) |
| **UK Police** | UK Police data. | No | ✅ | [Link](https://data.police.uk/docs/) |
| **VulDB** | VulDB API allows to initiate queries for one or more items along with transac... | 🔑 ApiKey | ✅ | [Link](https://vuldb.com/?doc.api) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="data-validation"></a>✅ Data Validation

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Byteplant Email Validator** | Email validation API. | 🔑 ApiKey | ✅ | [Link](https://www.email-validator.net/api.html) |
| **DeBounce** | Email validation API with free credits. | 🔑 ApiKey | ✅ | [Link](https://developers.debounce.com/) |
| **Emailable** | Email verification API with free tier. | 🔑 ApiKey | ✅ | [Link](https://emailable.com/docs/api) |
| **Lob.com** | US Address Verification. | 🔑 ApiKey | ✅ | [Link](https://lob.com/) |
| **Neutrino Email Validate** | Email syntax/DNS/disposable checks. | 🔑 ApiKey | ✅ | [Link](https://www.neutrinoapi.com/api/email-validate/) |
| **US Autocomplete** | Enter address data quickly with real-time address suggestions. | 🔑 ApiKey | ✅ | [Link](https://www.smarty.com/docs/cloud/us-autocomplete-pro-api) |
| **US Extract** | Extract postal addresses from any text including emails. | 🔑 ApiKey | ✅ | [Link](https://www.smarty.com/products/apis/us-extract-api) |
| **US Street Address** | Validate and append data for any US postal address. | 🔑 ApiKey | ✅ | [Link](https://www.smarty.com/docs/cloud/us-street-api) |
| **vatlayer** | VAT number validation. | 🔑 ApiKey | ✅ | [Link](https://vatlayer.com/documentation) |
| **Verifalia** | Email verification API. | 🔑 ApiKey | ✅ | [Link](https://verifalia.com/developers) |
| **ZeroBounce** | Email validation and scoring. | 🔑 ApiKey | ✅ | [Link](https://www.zerobounce.net/docs/email-validation-api-quickstart/v2-get-api-usage/) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="shopping"></a>🛍️ Shopping

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Barcode Lookup** | Product data from UPC/EAN barcodes. | 🔑 ApiKey | ✅ | [Link](https://www.barcodelookup.com/api) |
| **Best Buy** | Retail data. | 🔑 ApiKey | ✅ | [Link](https://bestbuyapis.github.io/api-documentation/#overview) |
| **Digi-Key** | Retrieve price and inventory of electronic components as well as place orders. | 🔐 OAuth | ✅ | [Link](https://www.digikey.com/en/resources/api-solutions) |
| **eBay** | Auction and retail. | 🔐 OAuth | ✅ | [Link](https://developer.ebay.com/) |
| **Etsy** | E-commerce. | 🔐 OAuth | ✅ | [Link](https://www.etsy.com/developers/documentation/getting_started/api_basics) |
| **Flipkart Marketplace** | Product listing management, Order Fulfilment in the Flipkart Marketplace. | 🔐 OAuth | ✅ | [Link](https://seller.flipkart.com/api-docs/FMSAPI.html) |
| **Lazada** | Retrieve product ratings and seller performance metrics. | 🔑 ApiKey | ✅ | [Link](https://open.lazada.com/doc/doc.htm) |
| **Mercadolibre** | E-commerce. | 🔑 ApiKey | ✅ | [Link](https://developers.mercadolibre.cl/es_ar/api-docs-es) |
| **Octopart** | Electronic part data for manufacturing, design, and sourcing. | 🔑 ApiKey | ✅ | [Link](https://octopart.com/api/v4/reference) |
| **OLX Poland** | Integrate with local sites by posting, managing adverts and communicating wit... | 🔑 ApiKey | ✅ | [Link](https://developer.olx.pl/api/doc#section/) |
| **Rappi** | Manage orders from Rappi's app. | 🔐 OAuth | ✅ | [Link](https://dev-portal.rappi.com/) |
| **Shopee** | E-commerce. | 🔑 ApiKey | ✅ | [Link](https://open.shopee.com/documents?version=1) |
| **Shopify Storefront** | Headless commerce GraphQL API for custom storefronts. | 🔑 ApiKey | ✅ | [Link](https://shopify.dev/docs/api/storefront) |
| **Tokopedia** | Tokopedia's Official API for integration of various services from Tokopedia. | 🔐 OAuth | ✅ | [Link](https://developer.tokopedia.com/openapi/guide/#/) |
| **WooCommerce** | E-commerce. | 🔑 ApiKey | ✅ | [Link](https://woocommerce.github.io/woocommerce-rest-api-docs/) |
| **Makeup API** | Search makeup products by brand, type, price (**No Auth**). | No | ✅ | [Link](http://makeup-api.herokuapp.com/) |


[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="utilities-tools"></a>🔧 Utilities & Tools

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Cal.com** | Open source scheduling API (Calendly alternative). | 🔑 ApiKey | ✅ | [Link](https://cal.com/docs/api-reference) |
| **Carbon Screenshot** | Create beautiful images of code snippets. | No | ✅ | [Link](https://carbon.now.sh/) |
| **Country.is** | Get country from IP address (**No Auth**). | No | ✅ | [Link](https://country.is/) |
| **DiceBear Avatars** | Generate random SVG avatars (**No Auth**). | No | ✅ | [Link](https://www.dicebear.com/) |
| **DuckDuckGo Instant Answer** | Quick, concise answers for definitions, calculations, and conversions. | No | ✅ | [Link](https://duckduckgo.com/api) |
| **FakerAPI** | Generate fake data for testing (**No Auth, 1000 req/day**). | No | ✅ | [Link](https://fakerapi.it/en) |
| **ipify** | A simple public IP address API (**No Auth**). | No | ✅ | [Link](https://www.ipify.org/) |
| **JSONLint** | JSON validation API. | No | ✅ | [Link](https://jsonlint.com/) |
| **PDF.co** | PDF generation, conversion and manipulation. | 🔑 ApiKey | ✅ | [Link](https://apidocs.pdf.co/) |
| **Pravatar** | Placeholder avatar images (**No Auth**). | No | ✅ | [Link](https://pravatar.cc/) |
| **QR Code Generator** | Dynamic QR code generation API. | No | ✅ | [Link](https://goqr.me/api/) |
| **Random.org** | True random numbers, strings, sequences from atmospheric noise. | 🔑 ApiKey | ✅ | [Link](https://api.random.org/json-rpc/4) |
| **RoboHash** | Generate unique robot/monster avatars (**No Auth**). | No | ✅ | [Link](https://robohash.org/) |
| **Text Art API** | Generate text-based art (**No Auth**). | No | ✅ | [Link](http://patorjk.com/software/taag/) |
| **UI Avatars** | Generate avatar placeholders from initials (**No Auth, 28M+ daily requests**). | No | ✅ | [Link](https://ui-avatars.com/) |
| **URLBox** | Website screenshot API. | 🔑 ApiKey | ✅ | [Link](https://www.urlbox.io/) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="url-shorteners"></a>🔗 URL Shorteners

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Bitly** | URL shortener and link management. | 🔐 OAuth | ✅ | [Link](http://dev.bitly.com/get_started.html) |
| **BL.INK** | URL shortener and branded link management. | 🔑 ApiKey | ✅ | [Link](https://bl.ink/developers) |
| **CleanURI** | URL shortener service. | No | ✅ | [Link](https://cleanuri.com/docs) |
| **Clico** | URL shortener service. | 🔑 ApiKey | ✅ | [Link](https://cli.com/swagger-ui/index.html?configUrl=/v3/api-docs/swagger-config) |
| **Cutt.ly** | URL shortener service. | 🔑 ApiKey | ✅ | [Link](https://cutt.ly/api-documentation/cuttly-links-api) |
| **Drivet URL Shortener** | Shorten a long URL easily and fast. | No | ✅ | [Link](https://wiki.drivet.xyz/en/url-shortener/add-links) |
| **Dub** | Open-source short links and analytics. | 🔑 ApiKey | ✅ | [Link](https://dub.co/docs/api-reference/introduction) |
| **Free Url Shortener** | Free URL Shortener offers a powerful API to interact with other sites. | No | ✅ | [Link](https://ulvis.net/developer.html) |
| **Git.io** | Git.io URL shortener. | No | ✅ | [Link](https://github.blog/2011-11-10-git-io-github-url-shortener/) |
| **is.gd** | Simple free URL shortening API. | No | ✅ | [Link](https://is.gd/apishorteningreference.php) |
| **Mgnet.me** | Torrent URL shorten API. | No | ✅ | [Link](http://mgnet.me/api.html) |
| **Polr** | Open-source URL shortener API. | No | ✅ | [Link](https://docs.polrproject.org/en/latest/developer-guide/api/) |
| **Rebrandly** | URL shortener API. | 🔑 ApiKey | ✅ | [Link](https://developers.rebrandly.com/docs) |
| **Shlink** | Self-hosted URL shortener with REST API. | 🔑 ApiKey | ✅ | [Link](https://shlink.io/documentation/api-docs/) |
| **Short.io** | URL shortener with analytics. | 🔑 ApiKey | ✅ | [Link](https://developers.short.io/) |
| **Shrtcode** | URl Shortener with multiple Domains. | No | ✅ | [Link](https://shrtco.de/docs) |
| **Tiny.cc** | Link shortening and management API. | 🔑 ApiKey | ✅ | [Link](https://tiny.cc/api-docs) |
| **TinyURL** | URL shortener API (**No Auth**). | No | ✅ | [Link](https://tinyurl.com/app/dev) |
| **UrlBae** | Simple and efficient short link creation. | 🔑 ApiKey | ✅ | [Link](https://urlbae.com/developers) |
| **v.gd** | Free URL shortener API service. | No | ✅ | [Link](https://v.gd/apishorteningreference.php) |
| **YOURLS** | Self-hosted shortener with extensible API. | 🔑 ApiKey | ✅ | [Link](https://yourls.org/#API) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="social"></a>💬 Social

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Ayrshare** | Social media APIs to post, get analytics, and manage multiple users social me... | 🔑 ApiKey | ✅ | [Link](https://www.ayrshare.com) |
| **Blogger** | The Blogger APIs allows client applications to view and update Blogger content. | 🔐 OAuth | ✅ | [Link](https://developers.google.com/blogger/) |
| **Bluesky** | Decentralized social network API (AT Protocol). | 🔑 ApiKey | ✅ | [Link](https://docs.bsky.app/) |
| **Discord** | Chat platform. | 🔐 OAuth | ✅ | [Link](https://discord.com/developers/docs/intro) |
| **Disqus** | Communicate with Disqus data. | 🔐 OAuth | ✅ | [Link](https://disqus.com/api/docs/auth/) |
| **Facebook** | Social network. | 🔐 OAuth | ✅ | [Link](https://developers.facebook.com/) |
| **Foursquare** | Interact with Foursquare users and places (geolocation-based checkins, photos... | 🔐 OAuth | ✅ | [Link](https://developer.foursquare.com/) |
| **Fuck Off as a Service** | Asks someone to fuck off. | No | ✅ | [Link](https://www.foaas.com) |
| **Full Contact** | Get Social Media profiles and contact Information. | 🔐 OAuth | ✅ | [Link](https://docs.fullcontact.com/) |
| **Gravatar** | WordPress avatar service. | No | ✅ | [Link](https://gravatar.com/site/implement/images/) |
| **Hashnode** | A blogging platform built for developers. | No | ✅ | [Link](https://hashnode.com) |
| **Instagram** | Photo sharing. | 🔐 OAuth | ✅ | [Link](https://www.instagram.com/developer/) |
| **Kakao** | Kakao Login, Share on KakaoTalk, Social Plugins and more. | 🔐 OAuth | ✅ | [Link](https://developers.kakao.com/) |
| **LINE** | Messaging app. | 🔐 OAuth | ✅ | [Link](https://developers.line.biz/en/) |
| **LinkedIn** | Professional network. | 🔐 OAuth | ✅ | [Link](https://docs.microsoft.com/en-us/linkedin/?context=linkedin/context) |
| **Mastodon** | Decentralized microblogging platform. | 🔐 OAuth | ✅ | [Link](https://docs.joinmastodon.org/api/) |
| **Meetup.com** | Data about Meetups from Meetup.com. | 🔑 ApiKey | ✅ | [Link](https://www.meetup.com/api/guide) |
| **Microsoft Graph** | Access the data and intelligence in Microsoft 365, Windows 10, and Enterprise... | 🔐 OAuth | ✅ | [Link](https://docs.microsoft.com/en-us/graph/api/overview) |
| **Microsoft Teams** | Team collaboration platform. | 🔐 OAuth | ✅ | [Link](https://docs.microsoft.com/en-us/graph/teams-concept-overview) |
| **NAVER** | NAVER Login, Share on NAVER, Social Plugins and more. | 🔐 OAuth | ✅ | [Link](https://developers.naver.com/main/) |
| **Open Collective** | Get Open Collective data. | No | ✅ | [Link](https://docs.opencollective.com/help/developers/api) |
| **Pinterest** | Visual discovery. | 🔐 OAuth | ✅ | [Link](https://developers.pinterest.com/) |
| **Product Hunt** | The best new products in tech. | 🔐 OAuth | ✅ | [Link](https://api.producthunt.com/v2/docs) |
| **Reddit** | Social news. | 🔐 OAuth | ✅ | [Link](https://www.reddit.com/dev/api) |
| **Slack** | Team communication. | 🔐 OAuth | ✅ | [Link](https://api.slack.com/) |
| **Snapchat** | Photo and video sharing. | 🔐 OAuth | ✅ | [Link](https://developers.snap.com/) |
| **TamTam** | Bot API to interact with TamTam. | 🔑 ApiKey | ✅ | [Link](https://dev.tamtam.chat/) |
| **Telegram** | Messaging app. | 🔑 ApiKey | ✅ | [Link](https://core.telegram.org/bots/api) |
| **Telegram MTProto** | Read and write Telegram data. | 🔐 OAuth | ✅ | [Link](https://core.telegram.org/api#getting-started) |
| **Telegraph** | Create attractive blogs easily, to share. | 🔑 ApiKey | ✅ | [Link](https://telegra.ph/api) |
| **Threads** | Meta's microblogging platform. | 🔐 OAuth | ✅ | [Link](https://developers.facebook.com/docs/threads) |
| **TikTok** | Video sharing. | 🔐 OAuth | ✅ | [Link](https://developers.tiktok.com/doc/login-kit-web) |
| **Trash Nothing** | A freecycling community with thousands of free items posted every day. | 🔐 OAuth | ✅ | [Link](https://trashnothing.com/developer) |
| **Tumblr** | Microblogging platform. | 🔐 OAuth | ✅ | [Link](https://www.tumblr.com/docs/en/api/v2) |
| **Twitch** | Live streaming. | 🔐 OAuth | ✅ | [Link](https://dev.twitch.tv/docs) |
| **Twitter** | Microblogging. | 🔐 OAuth | ✅ | [Link](https://developer.twitter.com/en/docs) |
| **Viber** | Messaging app. | 🔑 ApiKey | ✅ | [Link](https://developers.viber.com/) |
| **vk** | Read and write vk data. | 🔐 OAuth | ✅ | [Link](https://vk.com/dev/sites) |
| **WhatsApp** | Messaging app. | 🔐 OAuth | ✅ | [Link](https://developers.facebook.com/docs/whatsapp) |
| **YouTube** | Video sharing platform. | 🔐 OAuth | ✅ | [Link](https://developers.google.com/youtube/v3) |
| **Zalo** | Messaging and social platform. | 🔐 OAuth | ✅ | [Link](https://developers.zalo.me/) |
| **Hacker News** | Y Combinator's Hacker News stories, comments, and user data (**No Auth**). | No | ✅ | [Link](https://github.com/HackerNews/API) |
| **Lemmy** | Decentralized link aggregation and discussion platform API. | No | ✅ | [Link](https://lemmy.ml/) |
| **Matrix** | Open standard for decentralized, real-time communication. | 🔑 ApiKey | ✅ | [Link](https://spec.matrix.org/latest/) |
| **Nostr** | Decentralized social protocol — censorship-resistant notes and messaging. | No | ✅ | [Link](https://github.com/nostr-protocol/nostr) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="sports"></a>⚽ Sports

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **API-Football** | Football (soccer) live scores, fixtures, stats. | 🔑 ApiKey | ✅ | [Link](https://www.api-football.com/documentation-v3) |
| **API-Sports** | Multi-sport live data (free tier). | 🔑 ApiKey | ✅ | [Link](https://api-sports.io/) |
| **Cloudbet** | Official Cloudbet API provides real-time sports odds and betting API to place... | 🔑 ApiKey | ✅ | [Link](https://www.cloudbet.com/api/) |
| **CollegeFootballData.com** | Unofficial detailed American college football statistics, records, and result... | 🔑 ApiKey | ✅ | [Link](https://collegefootballdata.com) |
| **CricketData** | Live cricket scores and statistics. | 🔑 ApiKey | ✅ | [Link](https://cricketdata.org/) |
| **Fitbit** | Fitbit Information. | 🔐 OAuth | ✅ | [Link](https://dev.fitbit.com/) |
| **Football** | A simple Open Source Football API to get squads’ stats, best scorers and more. | 🔑 ApiKey | ✅ | [Link](https://rapidapi.com/GiulianoCrescimbeni/api/football98/) |
| **Football (Soccer) Videos** | Embed codes for goals and highlights from Premier League, Bundesliga, Serie A... | No | ✅ | [Link](https://www.scorebat.com/video-api/) |
| **Football Prediction** | Football match predictions. | 🔑 ApiKey | ✅ | [Link](https://boggio-analytics.com/fp-api/) |
| **Football-Data.org** | Football data and statistics (**Free tier**). | 🔑 ApiKey | ✅ | [Link](https://www.football-data.org/documentation/quickstart) |
| **JCDecaux Bike** | JCDecaux's self-service bicycles. | 🔑 ApiKey | ✅ | [Link](https://developer.jcdecaux.com/) |
| **NBA Data** | All NBA Stats DATA, Games, Livescore, Standings, Statistics. | 🔑 ApiKey | ✅ | [Link](https://rapidapi.com/api-sports/api/api-nba/) |
| **NBA Stats** | Current and historical NBA Statistics. | No | ✅ | [Link](https://any-api.com/nba_com/nba_com/docs/API_Description) |
| **NHL API** | NHL hockey statistics and schedules. | No | ✅ | [Link](https://gitlab.com/dword4/nhlapi/-/blob/master/new-api.md) |
| **NHL Records and Stats** | NHL historical data and statistics. | No | ✅ | [Link](https://gitlab.com/dword4/nhlapi) |
| **Oddsmagnet** | Odds history from multiple UK bookmakers. | No | ✅ | [Link](https://data.oddsmagnet.com) |
| **OpenF1** | Real-time Formula 1 race data (**No Auth**). | No | ✅ | [Link](https://openf1.org/) |
| **OpenLigaDB** | Crowd sourced sports league results. | No | ✅ | [Link](https://www.openligadb.de) |
| **PandaScore** | Esports data and statistics. | 🔑 ApiKey | ✅ | [Link](https://developers.pandascore.co/) |
| **Premier League Standings** | All Current Premier League Standings and Statistics. | 🔑 ApiKey | ✅ | [Link](https://rapidapi.com/heisenbug/api/premier-league-live-scores/) |
| **SofaScore** | Live sports scores and stats. | No | ✅ | [Link](https://api.sofascore.com/) |
| **Sportmonks Football** | Football score/schedule, news api, tv channels, stats, history, display stand... | 🔑 ApiKey | ✅ | [Link](https://docs.sportmonks.com/football/) |
| **Squiggle** | Fixtures, results and predictions for Australian Football League matches. | No | ✅ | [Link](https://api.squiggle.com.au) |
| **Strava** | Connect with athletes, activities and more. | 🔐 OAuth | ✅ | [Link](https://strava.github.io/api/) |
| **TheSportsDB** | Open crowd-sourced sports data and artwork. | 🔑 ApiKey | ✅ | [Link](https://www.thesportsdb.com/api.php) |
| **Tredict** | Get and set activities, health data and more. | 🔐 OAuth | ✅ | [Link](https://www.tredict.com/blog/oauth_docs/) |
| **ESPN** | Unofficial ESPN API for NFL, NBA, MLB, NHL scores and schedules (**No Auth**). | No | ✅ | [Link](https://gist.github.com/akeaswaran/b48b02f1c94f873c6655e7129910fc3b) |
| **Jolpica F1** | Formula 1 race results, standings, and historical data (**No Auth**). | No | ✅ | [Link](https://api.jolpi.ca/ergast/f1/) |
| **MLB Stats API** | Official Major League Baseball statistics and game data (**No Auth**). | No | ✅ | [Link](https://statsapi.mlb.com/docs/) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="design-colors"></a>🎨 Design & Colors

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Behance** | Creative work showcase. | 🔑 ApiKey | ✅ | [Link](https://www.behance.net/dev) |
| **Brandfetch** | Company logos and brand assets. | 🔑 ApiKey | ✅ | [Link](https://docs.brandfetch.com/) |
| **Colormind** | AI-powered color palette generator (**No Auth**). | No | ✅ | [Link](http://colormind.io/api-access/) |
| **ColourLovers** | Get various patterns, palettes and images. | No | No | [Link](http://www.colourlovers.com/api) |
| **Cooper Hewitt** | Smithsonian Design Museum. | 🔑 ApiKey | ✅ | [Link](https://collection.cooperhewitt.org/api) |
| **Dribbble** | Design community and portfolio. | 🔐 OAuth | ✅ | [Link](https://developer.dribbble.com/) |
| **Europeana** | European Museum and Galleries content. | 🔑 ApiKey | ✅ | [Link](https://pro.europeana.eu/resources/apis/search) |
| **Font Awesome** | Icon library and toolkit APIs. | 🔑 ApiKey | ✅ | [Link](https://fontawesome.com/docs/apis) |
| **Icon Horse** | Favicon grabber API. | No | ✅ | [Link](https://icon.horse/) |
| **Iconfinder** | Icons. | 🔑 ApiKey | ✅ | [Link](https://developer.iconfinder.com) |
| **Icons8** | Icons (find "search icon" hyperlink in page) | No | ✅ | [Link](https://img.icons8.com/) |
| **Logo.dev** | Company logos and brand asset API. | 🔑 ApiKey | ✅ | [Link](https://www.logo.dev/) |
| **LogoKit** | Brand, stock, and crypto logo API. | 🔑 ApiKey | ✅ | [Link](https://docs.logokit.com/) |
| **Lordicon** | Icons with predone Animations. | No | ✅ | [Link](https://lordicon.com/) |
| **Noun Project** | Icons. | 🔐 OAuth | No | [Link](http://api.thenounproject.com/index.html) |
| **PHP-Noise** | Noise Background Image Generator. | No | ✅ | [Link](https://php-noise.com/) |
| **Pixel Encounter** | SVG Icon Generator. | No | ✅ | [Link](https://pixelencounter.com/api) |
| **Placeholder.com** | Simple placeholder image service (**No Auth**). | No | ✅ | [Link](https://placehold.co/) |
| **SVG Repo** | Free SVG icons and vectors. | No | ✅ | [Link](https://www.svgrepo.com/) |
| **The Color API** | Color conversion, schemes, and naming (**No Auth**). | No | ✅ | [Link](https://www.thecolorapi.com/) |
| **Word Cloud** | Easily create word clouds. | 🔑 ApiKey | ✅ | [Link](https://wordcloudapi.com/) |
| **Random Color API** | Generate random colors with hex, RGB, and HSL values (**No Auth**). | No | ✅ | [Link](https://x-colors.yurace.pro/) |
| **EmojiHub** | Random emoji data organized by category and group (**No Auth**). | No | ✅ | [Link](https://github.com/cheatsnake/emojihub) |


[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="geography-countries"></a>🌎 Geography & Countries

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Country State City** | Countries, states, and cities database. | 🔑 ApiKey | ✅ | [Link](https://countrystatecity.in/) |
| **CountryLayer** | Country data including flags and borders. | 🔑 ApiKey | ✅ | [Link](https://countrylayer.com/) |
| **Flagpedia** | Country flags in SVG and PNG (**No Auth**). | No | ✅ | [Link](https://flagpedia.net/download/api) |
| **GeoJS** | IP geolocation and geo data (**No Auth**). | No | ✅ | [Link](https://www.geojs.io/) |
| **GeoNames** | Worldwide geographical database (free registration). | No | ✅ | [Link](https://www.geonames.org/export/web-services.html) |
| **IPGeolocation Timezone** | Timezone data by coordinates. | 🔑 ApiKey | ✅ | [Link](https://ipgeolocation.io/timezone-api.html) |
| **Open Elevation** | Elevation data for any coordinates. | No | ✅ | [Link](https://open-elevation.com/) |
| **REST Countries** | Comprehensive country data (flags, capitals, currencies) (**No Auth**). | No | ✅ | [Link](https://restcountries.com/) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="transportation"></a>🚆 Transportation

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **ADS-B Exchange** | Flight tracking data. | No | ✅ | [Link](https://www.adsbexchange.com/data/) |
| **airportsapi** | Get name and website-URL for airports by ICAO code. | No | ✅ | [Link](https://airport-web.appspot.com/api/docs/) |
| **AIS Hub** | Real-time data of any marine and inland vessel equipped with AIS tracking system. | 🔑 ApiKey | No | [Link](http://www.aishub.net/api) |
| **Amadeus for Developers** | Travel Search - Limited usage. | 🔐 OAuth | ✅ | [Link](https://developers.amadeus.com/self-service) |
| **AZ511** | Access traffic data from the ADOT API. | 🔑 ApiKey | ✅ | [Link](https://www.az511.com/developers/doc) |
| **FlightAware** | Real-time and historical flight tracking data. | 🔑 ApiKey | ✅ | [Link](https://www.flightaware.com/commercial/aeroapi/) |
| **BART** | Bay Area Rapid Transit. | 🔑 ApiKey | ✅ | [Link](http://api.bart.gov) |
| **BC Ferries** | Sailing times and capacities for BC Ferries. | No | ✅ | [Link](https://www.bcferriesapi.ca) |
| **BIC-Boxtech** | Container technical detail for the global container fleet. | 🔐 OAuth | ✅ | [Link](https://docs.bic-boxtech.org/) |
| **Boston MBTA Transit** | Stations and predicted arrivals for MBTA. | 🔑 ApiKey | ✅ | [Link](https://www.mbta.com/developers/v3-api) |
| **Brazilian Vehicles and Prices** | Vehicles information from Fundação Instituto de Pesquisas Econômicas - Fipe. | No | ✅ | [Link](https://deividfortuna.github.io/fipe/) |
| **Citybikes** | Bike sharing station data worldwide. | No | ✅ | [Link](https://api.citybik.es/v2/) |
| **Compare Flight Prices** | API for comparing flight prices across platforms. | 🔑 ApiKey | ✅ | [Link](https://rapidapi.com/obryan-software-obryan-software-default/api/compare-flight-prices/) |
| **CTS** | CTS Realtime API. | 🔑 ApiKey | ✅ | [Link](https://api.cts-strasbourg.eu/) |
| **Grab** | Track deliveries, ride fares, payments and loyalty points. | 🔐 OAuth | ✅ | [Link](https://developer.grab.com/docs/) |
| **GraphHopper** | Route planning and optimization. | 🔑 ApiKey | ✅ | [Link](https://docs.graphhopper.com/) |
| **GTFS Realtime** | Public transit real-time data standard. | No | ✅ | [Link](https://gtfs.org/) |
| **Helipaddy sites** | Helicopter and passenger drone landing site directory, Helipaddy data and muc... | 🔑 ApiKey | ✅ | [Link](https://helipaddy.com/api/) |
| **HERE Maps** | Mapping, routing, and traffic (free tier). | 🔑 ApiKey | ✅ | [Link](https://developer.here.com/) |
| **Icelandic APIs** | Open APIs that deliver services in or regarding Iceland. | No | ✅ | [Link](http://docs.apis.is/) |
| **Izi** | Audio guide for travellers. | 🔑 ApiKey | ✅ | [Link](http://api-docs.izi.travel/) |
| **Kelley Blue Book** | Vehicle info, pricing, configuration, plus much more. | 🔑 ApiKey | ✅ | [Link](http://developer.kbb.com/#!/data/1-Default) |
| **Land Transport Authority DataMall, Singapore** | Singapore transport information. | 🔑 ApiKey | No | [Link](https://datamall.lta.gov.sg/content/dam/datamall/datasets/LTA_DataMall_API_User_Guide.pdf) |
| **MBTA v3** | Boston transit routes and predictions. | No | ✅ | [Link](https://api-v3.mbta.com/) |
| **Mercedes-Benz** | Telematics data, remotely access vehicle functions, car configurator, locate ... | 🔑 ApiKey | ✅ | [Link](https://developer.mercedes-benz.com/apis) |
| **Metro Lisboa** | Delays in subway lines. | No | No | [Link](http://app.metrolisboa.pt/status/getLinhas.php) |
| **MTA** | NYC subway real-time feed APIs. | No | ✅ | [Link](https://api.mta.info/#/subwayRealTimeFeeds) |
| **Navitia** | The open API for building cool stuff with transport data. | 🔑 ApiKey | ✅ | [Link](https://doc.navitia.io/) |
| **NHTSA** | NHTSA Product Information Catalog and Vehicle Listing. | No | ✅ | [Link](https://vpic.nhtsa.dot.gov/api/) |
| **Open Charge Map** | Global public registry of electric vehicle charging locations. | 🔑 ApiKey | ✅ | [Link](https://openchargemap.org/site/develop/api) |
| **OpenRouteService** | Directions, geocoding, isochrones. | 🔑 ApiKey | ✅ | [Link](https://openrouteservice.org/) |
| **OpenSky Network** | Flight tracking. | No | ✅ | [Link](https://openskynetwork.github.io/opensky-api/) |
| **Railway Transport for France** | SNCF public API. | 🔑 ApiKey | ✅ | [Link](https://www.digital.sncf.com/startup/api) |
| **REFUGE Restrooms** | Provides safe restroom access for transgender, intersex and gender nonconform... | No | ✅ | [Link](https://www.refugerestrooms.org/api/docs/#!/restrooms) |
| **Sabre for Developers** | Travel Search - Limited usage. | 🔑 ApiKey | ✅ | [Link](https://developer.sabre.com) |
| **Schiphol Airport** | Schiphol. | 🔑 ApiKey | ✅ | [Link](https://developer.schiphol.nl/) |
| **Smartcar** | Lock and unlock vehicles and get data like odometer reading and location. Wor... | 🔐 OAuth | ✅ | [Link](https://smartcar.com/docs/) |
| **Tankerkoenig** | German realtime gas/diesel prices. | 🔑 ApiKey | ✅ | [Link](https://creativecommons.tankerkoenig.de/swagger/) |
| **Transitland** | Global transit data aggregator (**No Auth**). | No | ✅ | [Link](https://www.transit.land/documentation) |
| **Transport for Atlanta, US** | Marta. | No | No | [Link](http://www.itsmarta.com/app-developer-resources.aspx) |
| **Transport for Auckland, New Zealand** | Auckland Transport. | No | ✅ | [Link](https://dev-portal.at.govt.nz/) |
| **Transport for Belgium** | The iRail API is a third-party API for Belgian public transport by train. | No | ✅ | [Link](https://docs.irail.be/) |
| **Transport for Bordeaux, France** | Bordeaux Métropole public transport and more (France) | 🔑 ApiKey | ✅ | [Link](https://opendata.bordeaux-metropole.fr/explore/) |
| **Transport for Budapest, Hungary** | Budapest public transport API. | No | ✅ | [Link](https://bkkfutar.docs.apiary.io) |
| **Transport for Chicago, US** | Chicago Transit Authority (CTA) | 🔑 ApiKey | No | [Link](http://www.transitchicago.com/developers/) |
| **Transport for Czech Republic** | Czech transport API. | No | ✅ | [Link](https://www.chaps.cz/eng/products/idos-internet) |
| **Transport for Finland** | Finnish transport API. | No | ✅ | [Link](https://digitransit.fi/en/developers/) |
| **Transport for Grenoble, France** | Grenoble public transport. | No | No | [Link](https://www.mobilites-m.fr/pages/opendata/OpenDataApi.html) |
| **Transport for Hessen, Germany** | RMV API (Public Transport in Hessen) | No | ✅ | [Link](https://opendata.rmv.de/site/start.html) |
| **Transport for Honolulu, US** | Honolulu Transportation Information. | 🔑 ApiKey | No | [Link](http://hea.thebus.org/api_info.asp) |
| **Transport for Lisbon, Portugal** | Data about buses routes, parking and traffic. | 🔑 ApiKey | ✅ | [Link](https://emel.city-platform.com/opendata/) |
| **Transport for London** | Public transport data. | 🔑 ApiKey | ✅ | [Link](https://api.tfl.gov.uk) |
| **Transport for Los Angeles, US** | Data about positions of Metro vehicles in real time and travel their routes. | No | ✅ | [Link](https://developer.metro.net/api/) |
| **Transport for Manchester, England** | TfGM transport network data. | 🔑 ApiKey | ✅ | [Link](https://developer.tfgm.com/) |
| **Transport for Norway** | Transport APIs and dataset for Norway. | No | ✅ | [Link](https://developer.entur.org/) |
| **Transport for Ottawa, Canada** | OC Transpo API. | 🔑 ApiKey | ✅ | [Link](https://www.octranspo.com/en/plan-your-trip/travel-tools/developers) |
| **Transport for Paris, France** | RATP Open Data API. | No | No | [Link](http://data.ratp.fr/api/v1/console/datasets/1.0/search/) |
| **Transport for Philadelphia, US** | SEPTA APIs. | No | No | [Link](http://www3.septa.org/hackathon/) |
| **Transport for Sao Paulo, Brazil** | SPTrans. | 🔐 OAuth | No | [Link](http://www.sptrans.com.br/desenvolvedores/api-do-olho-vivo-guia-de-referencia/documentacao-api/) |
| **Transport for Spain** | Public trains of Spain. | No | ✅ | [Link](https://data.renfe.com/api/1/util/snippet/api_info.html?resource_id=a2368cff-1562-4dde-8466-9635ea3a572a) |
| **Transport for Sweden** | Public Transport consumer. | 🔐 OAuth | ✅ | [Link](https://www.trafiklab.se/api) |
| **Transport for Switzerland** | Official Swiss Public Transport Open Data. | 🔑 ApiKey | ✅ | [Link](https://opentransportdata.swiss/en/) |
| **Transport for The Netherlands** | NS, only trains. | 🔑 ApiKey | No | [Link](http://www.ns.nl/reisinformatie/ns-api) |
| **Transport for Toronto, Canada** | TTC. | No | ✅ | [Link](https://myttc.ca/developers) |
| **Transport for UK** | Transport API and dataset for UK. | 🔑 ApiKey | ✅ | [Link](https://developer.transportapi.com) |
| **Transport for United States** | NextBus API. | No | No | [Link](https://retro.umoiq.com/xmlFeedDocs/NextBusXMLFeed.pdf) |
| **Transport for Vancouver, Canada** | TransLink. | 🔐 OAuth | ✅ | [Link](https://developer.translink.ca/) |
| **Transport for Washington, US** | Washington Metro transport API. | 🔐 OAuth | ✅ | [Link](https://developer.wmata.com/) |
| **transport.rest** | Community maintained, developer-friendly public transport API. | No | ✅ | [Link](https://transport.rest) |
| **Tripadvisor** | Rating content for a hotel, restaurant, attraction or destination. | 🔑 ApiKey | ✅ | [Link](https://tripadvisor-content-api.readme.io/reference/overview) |
| **Uber** | Uber ride requests and price estimation. | 🔐 OAuth | ✅ | [Link](https://developer.uber.com/products) |
| **Velib metropolis, Paris, France** | Velib Open Data API. | No | ✅ | [Link](https://www.velib-metropole.fr/donnees-open-data-gbfs-du-service-velib-metropole) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="tracking-logistics"></a>📦 Tracking & Logistics

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **17TRACK** | Shipment tracking API with free quota. | 🔑 ApiKey | ✅ | [Link](https://asset.17track.net/api/document/v2_en/index.html) |
| **Aftership** | API to update, manage and track shipment efficiently. | 🔑 ApiKey | ✅ | [Link](https://developers.aftership.com/reference/quick-start) |
| **Correios** | Integration to provide information and prepare shipments using Correio's serv... | 🔑 ApiKey | ✅ | [Link](https://cws.correios.com.br/ajuda) |
| **DHL Shipment Tracking** | DHL package tracking API. | 🔑 ApiKey | ✅ | [Link](https://developer.dhl.com/api-reference/shipment-tracking) |
| **FedEx Tracking** | FedEx package tracking API. | 🔑 ApiKey | ✅ | [Link](https://developer.fedex.com/api/en-us/catalog/track.html) |
| **Pixela** | API for recording and tracking habits or effort, routines. | 🔑 ApiKey | ✅ | [Link](https://pixe.la) |
| **PostalPinCode** | API for getting Pincode details in India. | No | ✅ | [Link](http://www.postalpincode.in/Api-Details) |
| **Postmon** | An API to query Brazilian ZIP codes and orders easily, quickly and free. | No | No | [Link](http://postmon.com.br) |
| **PostNord** | Provides information about parcels in transport for Sweden and Denmark. | 🔑 ApiKey | No | [Link](https://developer.postnord.com/api) |
| **Shippo** | Shipping API with free test mode. | 🔑 ApiKey | ✅ | [Link](https://docs.goshippo.com/) |
| **USPS Track & Confirm** | USPS tracking API. | 🔑 ApiKey | ✅ | [Link](https://www.usps.com/business/web-tools-apis/track-and-confirm-api.htm) |
| **WeCanTrack** | Automatically place subids in affiliate links to attribute affiliate conversi... | 🔑 ApiKey | ✅ | [Link](https://docs.wecantrack.com) |
| **WhatPulse** | Small application that measures your keyboard/mouse usage. | No | ✅ | [Link](https://developer.whatpulse.org/#web-api) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="environment-climate"></a>🌿 Environment & Climate

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **AQICN** | World air quality index data. | No | ✅ | [Link](https://aqicn.org/api/) |
| **BreezoMeter Pollen** | Daily Forecast pollen conditions data for a specific location. | 🔑 ApiKey | ✅ | [Link](https://docs.breezometer.com/api-documentation/pollen-api/v2/) |
| **Carbon Interface** | CO2 emissions for flights, shipping, and energy. | 🔑 ApiKey | ✅ | [Link](https://docs.carboninterface.com/) |
| **Climatiq** | Carbon footprint calculations API. | 🔑 ApiKey | ✅ | [Link](https://www.climatiq.io/docs) |
| **CO2 Offset** | API calculates and validates the carbon footprint. | No | ✅ | [Link](https://co2offset.io/api.html) |
| **Danish data service Energi** | Open energy data from Energinet to society. | No | ✅ | [Link](https://www.energidataservice.dk/) |
| **Global Forest Watch** | Deforestation and forest monitoring data. | 🔑 ApiKey | ✅ | [Link](https://www.globalforestwatch.org/help/developers/) |
| **GrünstromIndex** | Green Power Index for Germany (Grünstromindex/GSI) | No | No | [Link](https://gruenstromindex.de/) |
| **IQAir** | Air quality and weather data. | 🔑 ApiKey | ✅ | [Link](https://www.iqair.com/air-pollution-data-api) |
| **Luchtmeetnet** | Predicted and actual air quality components for The Netherlands (RIVM) | No | ✅ | [Link](https://api-docs.luchtmeetnet.nl/) |
| **NOAA Climate Data Online** | Historical climate and weather data. | 🔑 ApiKey | ✅ | [Link](https://www.ncdc.noaa.gov/cdo-web/webservices/v2) |
| **OpenWeatherMap Air Pollution** | Air quality index and pollutant data. | 🔑 ApiKey | ✅ | [Link](https://openweathermap.org/api/air-pollution) |
| **PM2.5 Open Data Portal** | Open low-cost PM2.5 sensor data. | No | ✅ | [Link](https://pm25.lass-net.org/#apis) |
| **PurpleAir** | Real-time air quality sensor data. | 🔑 ApiKey | ✅ | [Link](https://api.purpleair.com/) |
| **PVWatts** | Energy production photovoltaic (PV) energy systems. | 🔑 ApiKey | ✅ | [Link](https://developer.nrel.gov/docs/solar/pvwatts/v6/) |
| **Srp Energy** | Hourly usage energy report for Srp customers. | 🔑 ApiKey | ✅ | [Link](https://srpenergy-api-client-python.readthedocs.io/en/latest/api.html) |
| **UK Carbon Intensity** | The Official Carbon Intensity API for Great Britain developed by National Grid. | No | ✅ | [Link](https://carbon-intensity.github.io/api-definitions/#carbon-intensity-api-v1-0-0) |
| **WaterQuality (EPA)** | US water quality monitoring data. | No | ✅ | [Link](https://www.waterqualitydata.us/) |
| **Website Carbon** | API to estimate the carbon footprint of loading web pages. | No | ✅ | [Link](https://api.websitecarbon.com/) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="government-civic"></a>🏛️ Government & Civic

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Bank Negara Malaysia Open Data** | Malaysia Central Bank Open Data. | No | ✅ | [Link](https://apikijangportal.bnm.gov.my/) |
| **BCLaws** | Access to the laws of British Columbia. | No | No | [Link](https://www.bclaws.gov.bc.ca/civix/template/complete/api/index.html) |
| **Brazil** | Community driven API for Brazil Public Data. | No | ✅ | [Link](https://brasilapi.com.br/) |
| **Brazil Central Bank Open Data** | Brazil Central Bank Open Data. | No | ✅ | [Link](https://dadosabertos.bcb.gov.br/) |
| **Brazil Receita WS** | Consult companies by CNPJ for Brazilian companies. | No | ✅ | [Link](https://www.receitaws.com.br/) |
| **Brazilian Chamber of Deputies Open Data** | Provides legislative information in Apis XML and JSON, as well as files in va... | No | ✅ | [Link](https://dadosabertos.camara.leg.br/swagger/api.html) |
| **City, Berlin** | Berlin(DE) City Open Data. | No | ✅ | [Link](https://daten.berlin.de/) |
| **City, Gdańsk** | Gdańsk (PL) City Open Data. | No | ✅ | [Link](https://ckan.multimediagdansk.pl/en) |
| **City, Gdynia** | Gdynia (PL) City Open Data. | No | No | [Link](http://otwartedane.gdynia.pl/en/api_doc.html) |
| **City, Helsinki** | Helsinki(FI) City Open Data. | No | ✅ | [Link](https://hri.fi/en_gb/) |
| **City, Lviv** | Lviv(UA) City Open Data. | No | ✅ | [Link](https://opendata.city-adm.lviv.ua/) |
| **City, Nantes Open Data** | Nantes(FR) City Open Data. | 🔑 ApiKey | ✅ | [Link](https://data.nantesmetropole.fr/pages/home/) |
| **City, New York Open Data** | New York (US) City Open Data. | No | ✅ | [Link](https://opendata.cityofnewyork.us/) |
| **City, Toronto Open Data** | Toronto (CA) City Open Data. | No | ✅ | [Link](https://open.toronto.ca/) |
| **Code.gov** | The primary platform for Open Source and code sharing for the U.S. Federal Go... | 🔑 ApiKey | ✅ | [Link](https://code.gov) |
| **Colorado Information Marketplace** | Colorado State Government Open Data. | No | ✅ | [Link](https://data.colorado.gov/) |
| **Congress.gov** | US legislation and congressional records. | No | ✅ | [Link](https://api.congress.gov/) |
| **Data USA** | US Public Data. | No | ✅ | [Link](https://datausa.io/about/api/) |
| **data.europa.eu** | EU open data portal API. | No | ✅ | [Link](https://data.europa.eu/en) |
| **Data.parliament.uk** | Contains live datasets including information about petitions, bills, MP votes... | No | No | [Link](https://explore.data.parliament.uk/?learnmore=Members) |
| **Deutscher Bundestag DIP** | This API provides read access to DIP entities (e.g. activities, persons, prin... | 🔑 ApiKey | ✅ | [Link](https://dip.bundestag.de/documents/informationsblatt_zur_dip_api_v01.pdf) |
| **District of Columbia Open Data** | Contains D.C. government public datasets, including crime, GIS, financial dat... | No | ✅ | [Link](http://opendata.dc.gov/pages/using-apis) |
| **EPA** | Web services and data sets from the US Environmental Protection Agency. | No | ✅ | [Link](https://www.epa.gov/developers/data-data-products#apis) |
| **FBI Wanted** | Access information on the FBI Wanted program. | No | ✅ | [Link](https://www.fbi.gov/wanted/api) |
| **Federal Register** | US federal rules and notices data. | No | ✅ | [Link](https://www.federalregister.gov/developers/documentation/api/v1) |
| **Gazette Data, UK** | UK official public record API. | 🔐 OAuth | ✅ | [Link](https://www.thegazette.co.uk/data) |
| **Google Civic Information** | US voting and representative information. | 🔑 ApiKey | ✅ | [Link](https://developers.google.com/civic-information) |
| **Gun Policy** | International firearm injury prevention and policy. | 🔑 ApiKey | ✅ | [Link](https://www.gunpolicy.org/api) |
| **Interpol Red Notices** | Access and search Interpol Red Notices. | No | ✅ | [Link](https://interpol.api.bund.dev/) |
| **Istanbul (İBB) Open Data** | Data sets from the İstanbul Metropolitan Municipality (İBB) | No | ✅ | [Link](https://data.ibb.gov.tr) |
| **National Park Service, US** | Data from the US National Park Service. | 🔑 ApiKey | ✅ | [Link](https://www.nps.gov/subjects/developer/) |
| **Open Government, ACT** | Australian Capital Territory Open Data. | No | ✅ | [Link](https://www.data.act.gov.au/) |
| **Open Government, Argentina** | Argentina Government Open Data. | No | ✅ | [Link](https://datos.gob.ar/) |
| **Open Government, Australia** | Australian Government Open Data. | No | ✅ | [Link](https://www.data.gov.au/) |
| **Open Government, Austria** | Austria Government Open Data. | No | ✅ | [Link](https://www.data.gv.at/) |
| **Open Government, Belgium** | Belgium Government Open Data. | No | ✅ | [Link](https://data.gov.be/) |
| **Open Government, Canada** | Canadian Government Open Data. | No | No | [Link](http://open.canada.ca/en) |
| **Open Government, Colombia** | Colombia Government Open Data. | No | No | [Link](https://www.dane.gov.co/) |
| **Open Government, Cyprus** | Cyprus Government Open Data. | No | ✅ | [Link](https://data.gov.cy/?language=en) |
| **Open Government, Czech Republic** | Czech Republic Government Open Data. | No | ✅ | [Link](https://data.gov.cz/english/) |
| **Open Government, Denmark** | Denmark Government Open Data. | No | ✅ | [Link](https://www.opendata.dk/) |
| **Open Government, Finland** | Finland Government Open Data. | No | ✅ | [Link](https://www.avoindata.fi/en) |
| **Open Government, France** | French Government Open Data. | 🔑 ApiKey | ✅ | [Link](https://www.data.gouv.fr/) |
| **Open Government, Greece** | Greece Government Open Data. | 🔐 OAuth | ✅ | [Link](https://data.gov.gr/) |
| **Open Government, India** | Indian Government Open Data. | 🔑 ApiKey | ✅ | [Link](https://data.gov.in/) |
| **Open Government, Ireland** | Ireland Government Open Data. | No | ✅ | [Link](https://data.gov.ie/pages/developers) |
| **Open Government, Italy** | Italy Government Open Data. | No | ✅ | [Link](https://www.dati.gov.it/) |
| **Open Government, Korea** | Korea Government Open Data. | 🔑 ApiKey | ✅ | [Link](https://www.data.go.kr/) |
| **Open Government, Lithuania** | Lithuania Government Open Data. | No | ✅ | [Link](https://data.gov.lt/public/api/1) |
| **Open Government, Luxembourg** | Luxembourgish Government Open Data. | 🔑 ApiKey | ✅ | [Link](https://data.public.lu) |
| **Open Government, Mexico** | Mexican Statistical Government Open Data. | No | ✅ | [Link](https://www.inegi.org.mx/datos/) |
| **Open Government, Netherlands** | Netherlands Government Open Data. | No | ✅ | [Link](https://data.overheid.nl/en/ondersteuning/data-publiceren/api) |
| **Open Government, New South Wales** | New South Wales Government Open Data. | 🔑 ApiKey | ✅ | [Link](https://api.nsw.gov.au/) |
| **Open Government, New Zealand** | New Zealand Government Open Data. | No | ✅ | [Link](https://www.data.govt.nz/) |
| **Open Government, Norway** | Norwegian Government Open Data. | No | ✅ | [Link](https://data.norge.no/dataservices) |
| **Open Government, Peru** | Peru Government Open Data. | No | ✅ | [Link](https://www.datosabiertos.gob.pe/) |
| **Open Government, Poland** | Poland Government Open Data. | No | ✅ | [Link](https://dane.gov.pl/en) |
| **Open Government, Portugal** | Portugal Government Open Data. | No | ✅ | [Link](https://dados.gov.pt/en/docapi/) |
| **Open Government, Queensland Government** | Queensland Government Open Data. | No | ✅ | [Link](https://www.data.qld.gov.au/) |
| **Open Government, Slovakia** | Slovakia Government Open Data. | No | ✅ | [Link](https://data.gov.sk/en/) |
| **Open Government, Slovenia** | Slovenia Government Open Data. | No | ✅ | [Link](https://podatki.gov.si/) |
| **Open Government, South Australian Government** | South Australian Government Open Data. | No | ✅ | [Link](https://data.sa.gov.au/) |
| **Open Government, Spain** | Spain Government Open Data. | No | ✅ | [Link](https://datos.gob.es/en) |
| **Open Government, Sweden** | Sweden Government Open Data. | No | ✅ | [Link](https://www.dataportal.se/en/dataservice/91_29789/api-for-the-statistical-database) |
| **Open Government, Switzerland** | Switzerland Government Open Data. | No | ✅ | [Link](https://handbook.opendata.swiss/de/content/nutzen/api-nutzen.html) |
| **Open Government, Taiwan** | Taiwan Government Open Data. | No | ✅ | [Link](https://data.gov.tw/) |
| **Open Government, Thailand** | Thailand Government Open Data. | 🔑 ApiKey | ✅ | [Link](https://data.go.th/) |
| **Open Government, UK** | UK Government Open Data. | No | ✅ | [Link](https://data.gov.uk/) |
| **Open Government, USA** | United States Government Open Data. | No | ✅ | [Link](https://www.data.gov/) |
| **Open Government, Victoria State Government** | Victoria State Government Open Data. | No | ✅ | [Link](https://www.data.vic.gov.au/) |
| **Open Government, West Australia** | West Australia Open Data. | No | ✅ | [Link](https://data.wa.gov.au/) |
| **Open States** | US state legislature data. | 🔑 ApiKey | ✅ | [Link](https://docs.openstates.org/) |
| **OpenFEC** | US Federal Election Commission data. | No | ✅ | [Link](https://api.open.fec.gov/developers/) |
| **OpenSecrets** | US political finance transparency data. | 🔑 ApiKey | ✅ | [Link](https://www.opensecrets.org/open-data/api) |
| **Represent by Open North** | Find Canadian Government Representatives. | No | ✅ | [Link](https://represent.opennorth.ca/) |
| **UK Companies House** | UK Companies House Data from the UK government. | 🔐 OAuth | ✅ | [Link](https://developer.company-information.service.gov.uk/) |
| **UK Parliament** | UK parliamentary data and members. | No | ✅ | [Link](https://members-api.parliament.uk/index.html) |
| **USASpending** | US federal spending data API. | No | ✅ | [Link](https://api.usaspending.gov/) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="video"></a>📹 Video

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **An API of Ice And Fire** | Game Of Thrones API. | No | ✅ | [Link](https://anapioficeandfire.com/) |
| **api.video** | Video hosting, encoding, and live streaming. | 🔑 ApiKey | ✅ | [Link](https://docs.api.video/) |
| **Cloudflare Stream** | Video streaming and delivery. | 🔑 ApiKey | ✅ | [Link](https://developers.cloudflare.com/stream/) |
| **Czech Television** | TV programme of Czech TV. | No | No | [Link](http://www.ceskatelevize.cz/xml/tv-program/) |
| **Dailymotion** | Video platform and publishing API. | 🔐 OAuth | ✅ | [Link](https://developers.dailymotion.com/api/) |
| **Final Space** | Final Space API. | No | ✅ | [Link](https://finalspaceapi.com/docs/) |
| **Game of Thrones Quotes** | Some Game of Thrones quotes. | No | ✅ | [Link](https://gameofthronesquotes.xyz/) |
| **IMDb API** | Movie, serial and cast information. | 🔑 ApiKey | ✅ | [Link](https://imdbapi.dev/) |
| **JSON2Video** | Create and edit videos programmatically: watermarks,resizing,slideshows,voice... | 🔑 ApiKey | ✅ | [Link](https://json2video.com) |
| **Mux** | Video infrastructure and analytics. | 🔑 ApiKey | ✅ | [Link](https://docs.mux.com/) |
| **Openverse** | Search openly-licensed media. | No | ✅ | [Link](https://api.openverse.org/v1/) |
| **PeerTube** | Federated video platform API. | No | ✅ | [Link](https://docs.joinpeertube.org/api-rest-reference.html) |
| **SponsorBlock** | Crowdsourced YouTube sponsor segments and skip timestamps (**No Auth**). | No | ✅ | [Link](https://wiki.sponsor.ajay.app/w/API_Docs) |
| **STAPI** | Information on all things Star Trek. | No | No | [Link](http://stapi.co) |
| **Stream** | Czech internet television, films, series and online videos for free. | No | ✅ | [Link](https://api.stream.cz/graphiql) |
| **Stromberg Quotes** | Returns Stromberg quotes and more. | No | ✅ | [Link](https://www.stromberg-api.de/) |
| **SWAPI GraphQL** | Star Wars GraphQL API. | No | ✅ | [Link](https://graphql.org/swapi-graphql) |
| **The Lord of the Rings** | The Lord of the Rings API. | 🔑 ApiKey | ✅ | [Link](https://the-one-api.dev/) |
| **The Vampire Diaries** | TV Show Data. | 🔑 ApiKey | ✅ | [Link](https://vampire-diaries-api.netlify.app/) |
| **ThronesApi** | Game Of Thrones Characters Data with imagery. | No | ✅ | [Link](https://thronesapi.com/) |
| **TVDB** | Television data. | 🔑 ApiKey | ✅ | [Link](https://thetvdb.com/api-information) |
| **uNoGS** | Unofficial Netflix Online Global Search, Search all netflix regions in one place. | 🔑 ApiKey | ✅ | [Link](https://rapidapi.com/unogs/api/unogsng) |
| **Vimeo** | Video hosting and sharing platform. | 🔐 OAuth | ✅ | [Link](https://developer.vimeo.com/) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="math-computation"></a>🔢 Math & Computation

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **math.js** | Mathematical expression evaluation API. | No | ✅ | [Link](https://api.mathjs.org/) |
| **Unit Converter** | Convert between various units. | No | ✅ | [Link](https://api-ninjas.com/api/convertcurrency) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="unofficial-community"></a>⚠️ Unofficial & Community APIs

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Bibliogram** | Instagram front-end (read-only, no login required) ⚠️ **Many instances down**. | No | ✅ | [Link](https://bibliogram.art/) |
| **Instaloader** | Instagram scraper (posts, stories, profiles). | No | ✅ | [Link](https://instaloader.github.io/) |
| **Invidious** | Privacy-focused YouTube front-end and API (no tracking, no ads). | No | ✅ | [Link](https://docs.invidious.io/api/) |
| **NewPipe Extractor** | YouTube, SoundCloud, PeerTube data extraction library. | No | ✅ | [Link](https://teamnewpipe.github.io/NewPipeExtractor/javadoc/) |
| **Piped** | Alternative YouTube API (privacy-respecting, no Google tracking). | No | ✅ | [Link](https://docs.piped.video/docs/api-documentation/) |
| **Rimgo** | Imgur alternative front-end (privacy-respecting). | No | ✅ | [Link](https://codeberg.org/video-prize-ranch/rimgo) |
| **Scribe** | Medium alternative front-end (no tracking, no paywall). | No | ✅ | [Link](https://sr.ht/~edwardloveall/Scribe/) |
| **Searx/SearxNG** | Meta search engine with JSON API (aggregates results). | No | ✅ | [Link](https://docs.searxng.org/dev/search_api.html) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="memes-fun"></a>😂 Memes & Fun

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Advice Slip** | Generate random advice slips (**No Auth**, great for simple widgets). | No | ✅ | [Link](https://api.adviceslip.com/) |
| **Affirmations** | Get random positive affirmations (**No Auth**). | No | ✅ | [Link](https://www.affirmations.dev/) |
| **Breaking Bad Quotes** | Random Breaking Bad quotes (**No Auth**). | No | ✅ | [Link](https://breakingbadquotes.xyz/) |
| **Chuck Norris Jokes** | Random Chuck Norris jokes (**No Auth**). | No | ✅ | [Link](https://api.chucknorris.io/) |
| **Corporate BS Generator** | Generate corporate jargon (**No Auth**). | No | ✅ | [Link](https://corporatebs-generator.sameerkumar.website/) |
| **Dad Jokes** | Random dad jokes (**No Auth**). | No | ✅ | [Link](https://icanhazdadjoke.com/api) |
| **Evil Insult** | Random multilingual insults (**No Auth**). | No | ✅ | [Link](https://evilinsult.com/api) |
| **Fun Translations** | Translate text to Yoda, Pirate, etc. | 🔑 ApiKey | ✅ | [Link](https://funtranslations.com/api) |
| **Imgflip** | Get popular meme templates to create your own memes (**No Auth**). | No | ✅ | [Link](https://api.imgflip.com/) |
| **JokeAPI** | Jokes in various categories (**No Auth**). | No | ✅ | [Link](https://jokeapi.dev/) |
| **Kanye.rest** | Random Kanye West quotes (**No Auth**). | No | ✅ | [Link](https://api.kanye.rest/) |
| **Numbers API** | Fun facts about numbers (**No Auth**). | No | ✅ | [Link](http://numbersapi.com/) |
| **Random Dog Facts** | Random dog facts API (**No Auth**). | No | ✅ | [Link](https://kinduff.github.io/dog-api/) |
| **Tronald Dump** | Random Donald Trump quotes (**No Auth**). | No | ✅ | [Link](https://tronalddump.io/) |
| **Useless Facts** | Random useless facts (**No Auth**). | No | ✅ | [Link](https://uselessfacts.jsph.pl/) |
| **Zen Quotes** | Random inspirational quotes (**No Auth**). | No | ✅ | [Link](https://zenquotes.io/) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="jobs-career"></a>💼 Jobs & Career

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Adzuna** | Job board aggregator with salary data. | 🔑 ApiKey | ✅ | [Link](https://developer.adzuna.com/overview) |
| **Arbeitnow** | Free remote job board API. | No | ✅ | [Link](https://documenter.getpostman.com/view/18545278/UVJbJdKh) |
| **Arbeitsamt** | API for the "Arbeitsamt", which is a german Job board aggregator. | 🔐 OAuth | ✅ | [Link](https://jobsuche.api.bund.dev/) |
| **Careerjet** | Job search engine. | 🔑 ApiKey | No | [Link](https://www.careerjet.com/partners/api/) |
| **DevITjobs UK** | Jobs with GraphQL. | No | ✅ | [Link](https://devitjobs.uk/job_feed.xml) |
| **Findwork** | Job board. | 🔑 ApiKey | ✅ | [Link](https://findwork.dev/developers/) |
| **Himalayas** | Remote jobs API and company data. | No | ✅ | [Link](https://himalayas.app/api) |
| **Jobicy** | Remote job listings feed API. | No | ✅ | [Link](https://jobicy.com/jobs-rss-feed) |
| **Jobs2Careers** | Job aggregator. | 🔑 ApiKey | ✅ | [Link](http://api.jobs2careers.com/api/spec.pdf) |
| **Jooble** | Job search engine. | 🔑 ApiKey | ✅ | [Link](https://jooble.org/api/about) |
| **JSearch** | Job search API (via RapidAPI). | 🔑 ApiKey | ✅ | [Link](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch) |
| **Juju** | Job search engine. | 🔑 ApiKey | No | [Link](http://www.juju.com/publisher/spec/) |
| **Reed** | UK job board API. | 🔑 ApiKey | ✅ | [Link](https://www.reed.co.uk/developers) |
| **Remoteok** | API for remote jobs (often used for job board projects). | No | ✅ | [Link](https://remoteok.com/api) |
| **The Muse** | Job search and company data. | 🔑 ApiKey | ✅ | [Link](https://www.themuse.com/developers/api/v2) |
| **Upwork** | Freelance job board and management system. | 🔐 OAuth | ✅ | [Link](https://developers.upwork.com/) |
| **USAJOBS** | US government job listings. | 🔑 ApiKey | ✅ | [Link](https://developer.usajobs.gov/) |
| **WhatJobs** | Job search engine. | 🔑 ApiKey | ✅ | [Link](https://www.whatjobs.com/affiliates) |
| **ZipRecruiter** | Job search app and website. | 🔑 ApiKey | ✅ | [Link](https://www.ziprecruiter.com/publishers) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="weather"></a>🌤️ Weather

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **7Timer!** | Weather forecast. | No | No | [Link](http://www.7timer.info/doc.php?lang=en) |
| **7Timer! Weather** | Astronomical and meteorological forecasts (**No Auth**). | No | ✅ | [Link](http://www.7timer.info/doc.php) |
| **AccuWeather** | Weather forecast. | 🔑 ApiKey | ✅ | [Link](https://developer.accuweather.com/apis) |
| **Aemet** | Weather and forecast data from Spain. | 🔑 ApiKey | ✅ | [Link](https://opendata.aemet.es/centrodedescargas/inicio) |
| **Air Quality (OpenAQ)** | Global air quality data (**No Auth**). | No | ✅ | [Link](https://docs.openaq.org/) |
| **APIXU** | Weather. | 🔑 ApiKey | ✅ | [Link](https://www.apixu.com/doc/request.aspx) |
| **AviationWeather** | NOAA aviation weather forecasts and observations. | No | ✅ | [Link](https://www.aviationweather.gov/dataserver) |
| **ColorfulClouds** | Weather. | 🔑 ApiKey | ✅ | [Link](https://open.caiyunapp.com/ColorfulClouds_Weather_API) |
| **Euskalmet** | Meteorological data of the Basque Country. | 🔑 ApiKey | ✅ | [Link](https://opendata.euskadi.eus/api-euskalmet/-/api-de-euskalmet/) |
| **Foreca** | Weather. | 🔐 OAuth | ✅ | [Link](https://developer.foreca.com) |
| **HG Weather** | Provides weather forecast data for cities in Brazil. | 🔑 ApiKey | ✅ | [Link](https://hgbrasil.com/status/weather) |
| **Hong Kong Obervatory** | Provide weather information, earthquake information, and climate data. | No | ✅ | [Link](https://www.hko.gov.hk/en/abouthko/opendata_intro.htm) |
| **Meteoblue** | Weather forecasts and history. | 🔑 ApiKey | ✅ | [Link](https://content.meteoblue.com/en/business-solutions/weather-apis) |
| **Meteomatics** | High-resolution weather API with global coverage. | 🔑 ApiKey | ✅ | [Link](https://www.meteomatics.com/en/api/getting-started/) |
| **Meteorologisk Institutt** | Weather and climate data. | 🔑 ApiKey | ✅ | [Link](https://api.met.no/weatherapi/documentation) |
| **Micro Weather** | Real time weather forecasts and historic data. | 🔑 ApiKey | ✅ | [Link](https://m3o.com/weather/api) |
| **ODWeather** | Weather and weather webcams. | No | No | [Link](http://api.oceandrivers.com/static/docs.html) |
| **Oikolab** | 70+ years of global, hourly historical and forecast weather data from NOAA an... | 🔑 ApiKey | ✅ | [Link](https://docs.oikolab.com) |
| **Open-Meteo** | Open-source weather API (**No API key required**). | No | ✅ | [Link](https://open-meteo.com/) |
| **openSenseMap** | Data from Personal Weather Stations called senseBoxes. | No | ✅ | [Link](https://api.opensensemap.org/) |
| **OpenUV** | Real-time UV Index Forecast. | 🔑 ApiKey | ✅ | [Link](https://www.openuv.io) |
| **OpenWeatherMap** | Weather forecast. | 🔑 ApiKey | ✅ | [Link](https://openweathermap.org/api) |
| **QWeather** | Location-based weather data. | 🔑 ApiKey | ✅ | [Link](https://dev.qweather.com/en/) |
| **RainViewer** | Weather radar. | No | ✅ | [Link](https://www.rainviewer.com/api.html) |
| **Storm Glass** | Global marine weather from multiple sources. | 🔑 ApiKey | ✅ | [Link](https://stormglass.io/) |
| **Sunrise-Sunset** | Sunrise and sunset times for any location (**No Auth**). | No | ✅ | [Link](https://sunrise-sunset.org/api) |
| **Tomorrow** | Weather API Powered by Proprietary Technology. | 🔑 ApiKey | ✅ | [Link](https://docs.tomorrow.io) |
| **US Weather** | US National Weather Service. | No | ✅ | [Link](https://www.weather.gov/documentation/services-web-api) |
| **Visual Crossing** | Global weather data and forecasts. | 🔑 ApiKey | ✅ | [Link](https://www.visualcrossing.com/weather-api) |
| **WeatherAPI** | Weather forecast. | 🔑 ApiKey | ✅ | [Link](https://www.weatherapi.com/) |
| **Weatherbit** | Weather forecast. | 🔑 ApiKey | ✅ | [Link](https://www.weatherbit.io/api) |
| **Weatherstack** | Real-time & historical world weather data. | 🔑 ApiKey | ✅ | [Link](https://weatherstack.com/) |
| **Yandex.Weather** | Assesses weather condition in specific locations. | 🔑 ApiKey | ✅ | [Link](https://yandex.com/dev/weather/) |


[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="business"></a>💼 Business

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Charity Search** | Non-profit charity data. | 🔑 ApiKey | No | [Link](http://charityapi.orghunter.com/) |
| **Clearbit Logo** | Search for company logos and embed them in your projects. | 🔑 ApiKey | ✅ | [Link](https://clearbit.com/docs#logo-api) |
| **Domainsdb.info** | Registered Domain Names Search. | No | ✅ | [Link](https://domainsdb.info/) |
| **Freelancer** | Hire freelancers to get work done. | 🔐 OAuth | ✅ | [Link](https://developers.freelancer.com) |
| **Gmail** | Flexible, RESTful access to the user's inbox. | 🔐 OAuth | ✅ | [Link](https://developers.google.com/gmail/api/) |
| **Google Analytics** | Collect, configure and analyze your data to reach the right audience. | 🔐 OAuth | ✅ | [Link](https://developers.google.com/analytics/) |
| **markerapi** | Trademark Search. | No | No | [Link](https://markerapi.com) |
| **SwiftKanban** | Kanban software, Visualize Work, Increase Organizations Lead Time, Throughput... | 🔑 ApiKey | ✅ | [Link](https://www.digite.com/knowledge-base/swiftkanban/article/api-for-swift-kanban-web-services/#restapi) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="documents-productivity"></a>📄 Documents & Productivity

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Api2Convert** | Online File Conversion API. | 🔑 ApiKey | ✅ | [Link](https://www.api2convert.com/) |
| **Asana** | Programmatic access to all data in your asana system. | 🔑 ApiKey | ✅ | [Link](https://developers.asana.com/docs) |
| **ClickUp** | ClickUp is a robust, cloud-based project management tool for boosting product... | 🔐 OAuth | ✅ | [Link](https://clickup.com/api) |
| **Clockify** | Clockify's REST-based API can be used to push/pull data to/from it & integrat... | 🔑 ApiKey | ✅ | [Link](https://clockify.me/developers-api) |
| **CloudConvert** | Online file converter for audio, video, document, ebook, archive, image, spre... | 🔑 ApiKey | ✅ | [Link](https://cloudconvert.com/api/v2) |
| **Cloudmersive Document and Data Conversion** | HTML/URL to PDF/PNG, Office documents to PDF, image conversion. | 🔑 ApiKey | ✅ | [Link](https://cloudmersive.com/convert-api) |
| **Code::Stats** | Automatic time tracking for programmers. | 🔑 ApiKey | ✅ | [Link](https://codestats.net/api-docs) |
| **CraftMyPDF** | Generate PDF documents from templates with a drop-and-drop editor and a simpl... | 🔑 ApiKey | ✅ | [Link](https://craftmypdf.com) |
| **Docusign** | Electronic signature and agreement API. | 🔐 OAuth | ✅ | [Link](https://developers.docusign.com/) |
| **Dropbox Sign (HelloSign)** | E-signature API for documents and agreements. | 🔑 ApiKey | ✅ | [Link](https://developers.hellosign.com/api) |
| **Flowdash** | Automate business workflows. | 🔑 ApiKey | ✅ | [Link](https://docs.flowdash.com/docs/api-introduction) |
| **Html2PDF** | HTML/URL to PDF. | 🔑 ApiKey | ✅ | [Link](https://html2pdf.app/) |
| **iLovePDF** | Convert, merge, split, extract text and add page numbers for PDFs. Free for 2... | 🔑 ApiKey | ✅ | [Link](https://developer.ilovepdf.com/) |
| **JIRA** | JIRA is a proprietary issue tracking product that allows bug tracking and agi... | 🔐 OAuth | ✅ | [Link](https://developer.atlassian.com/server/jira/platform/rest-apis/) |
| **Mattermost** | An open source platform for developer collaboration. | 🔐 OAuth | ✅ | [Link](https://api.mattermost.com/) |
| **PandaDoc** | DocGen and eSignatures API. | 🔑 ApiKey | ✅ | [Link](https://developers.pandadoc.com) |
| **Podio** | File sharing and productivity. | 🔐 OAuth | ✅ | [Link](https://developers.podio.com) |
| **Restpack** | Provides screenshot, HTML to PDF and content extraction APIs. | 🔑 ApiKey | ✅ | [Link](https://restpack.io/) |
| **Smart Image Enhancement API** | Performs image upscaling by adding detail to images through multiple super-re... | 🔑 ApiKey | ✅ | [Link](https://apilayer.com/marketplace/image_enhancement-api) |
| **Todoist** | Todo Lists. | 🔐 OAuth | ✅ | [Link](https://developer.todoist.com) |
| **Vector Express v2.0** | Free vector file converting API. | No | ✅ | [Link](https://vector.express) |
| **WakaTime** | Automated time tracking leaderboards for programmers. | No | ✅ | [Link](https://wakatime.com/developers) |
| **Zube** | Full stack project management. | 🔐 OAuth | ✅ | [Link](https://zube.io/docs/api) |

[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="demographic-analysis"></a>👤 Demographic Analysis


| Name | Description | Auth | HTTPS | Link |
|------|-------------|------|-------|------|
| **Genderize** | Predict the gender of a name (**No Auth**). | No | ✅ | [Link](https://genderize.io/) |
| **Nationalize** | Predict the nationality of a name (**No Auth**). | No | ✅ | [Link](https://nationalize.io/) |
| **Agify** | Predict the age of a name (**No Auth**). | No | ✅ | [Link](https://agify.io/) |


[⬆ Back to Table of Contents](#-table-of-contents)



## <a id="museums-art"></a>🏛️ Museums & Art


| Name | Description | Auth | HTTPS | Link |
|------|-------------|------|-------|------|
| **Metropolitan Museum** | Access 5,000 years of art from The Met collection (**No Auth**). | No | ✅ | [Link](https://metmuseum.github.io/) |


[⬆ Back to Table of Contents](#-table-of-contents)

## <a id="monitoring-observability"></a>📈 Monitoring & Observability

| API Name | Description | Auth | HTTPS | Link |
| :--- | :--- | :---: | :---: | :---: |
| **Axiom** | Event data platform for logs, traces, and metrics. | 🔑 ApiKey | ✅ | [Link](https://axiom.co/docs/restapi/introduction) |
| **Better Stack (Logtail)** | Uptime monitoring, logs, and incident management. | 🔑 ApiKey | ✅ | [Link](https://betterstack.com/docs/uptime/api/) |
| **Checkly** | API and browser synthetic monitoring for developers. | 🔑 ApiKey | ✅ | [Link](https://www.checklyhq.com/docs/cli/) |
| **Datadog** | Cloud monitoring, logs, metrics, and APM. | 🔑 ApiKey | ✅ | [Link](https://docs.datadoghq.com/api/latest/) |
| **Grafana Cloud** | Managed metrics, logs, and traces platform. | 🔑 ApiKey | ✅ | [Link](https://grafana.com/docs/grafana-cloud/developer-resources/api-reference/) |
| **Honeycomb** | Observability for distributed systems and microservices. | 🔑 ApiKey | ✅ | [Link](https://docs.honeycomb.io/api/) |
| **New Relic** | Full-stack application performance monitoring. | 🔑 ApiKey | ✅ | [Link](https://docs.newrelic.com/docs/apis/intro-apis/introduction-new-relic-apis/) |
| **OpenTelemetry** | Open-source observability framework for telemetry data. | No | ✅ | [Link](https://opentelemetry.io/docs/) |
| **PagerDuty** | Incident response and on-call scheduling platform. | 🔑 ApiKey | ✅ | [Link](https://developer.pagerduty.com/api-reference/) |
| **Pingdom** | Website and infrastructure uptime monitoring. | 🔑 ApiKey | ✅ | [Link](https://docs.pingdom.com/api/) |
| **Prometheus** | Open-source metrics-based monitoring query API. | No | ✅ | [Link](https://prometheus.io/docs/prometheus/latest/querying/api/) |
| **Raygun** | Crash reporting and real user monitoring. | 🔑 ApiKey | ✅ | [Link](https://raygun.com/documentation/api/) |
| **Sentry** | Application error tracking and performance monitoring. | 🔑 ApiKey | ✅ | [Link](https://docs.sentry.io/api/) |
| **UptimeRobot** | Website, port, and keyword uptime monitoring. | 🔑 ApiKey | ✅ | [Link](https://uptimerobot.com/api/) |
| **Zabbix** | Open-source enterprise monitoring and alerting. | 🔑 ApiKey | ✅ | [Link](https://www.zabbix.com/documentation/current/manual/api) |

[⬆ Back to Table of Contents](#-table-of-contents)


## 🤝 Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](./CONTRIBUTING.md) before opening a pull request.

You can also use the GitHub issue templates to suggest new APIs, report bugs, or request improvements.

## 🛡️ Code of Conduct

This project follows the [Code of Conduct](./CODE_OF_CONDUCT.md). Please be respectful and constructive.

## 📄 License

This project is licensed under the [MIT License](./LICENSE).

---

## 📈 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=ThanhNguyxnOrg/awesome-free-apis&type=Date)](https://star-history.com/#ThanhNguyxnOrg/awesome-free-apis&Date)

---

<div align="center">

**Don't forget to ⭐ this repo if you found it useful!**

</div>
