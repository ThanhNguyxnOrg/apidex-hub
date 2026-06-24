<!--
🚨 CRITICAL RULE FOR AI AGENTS:
Before making ANY changes to this repository, you MUST read and follow the instructions in [ai-instructions.md](./.github/ai-instructions.md).
- ONLY modify files inside the apis/ directory to add, remove, or edit API listings.
- DO NOT edit, update, or regenerate site/src/data/apis.json or site/index.html locally.
- DO NOT run build commands (npm run build, pnpm build, etc.) locally.
- Website generation is fully automated via GitHub Actions in CI/CD.
-->
# 🚀 APIDex Hub

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A curated collection of awesome public APIs and web scrapers for developers. Open source and community-driven.
> This repository aims to provide a comprehensive collection of public endpoints, APIs, and scraping solutions to help you build your next project.

<div align="center">

[![GitHub Stars](https://img.shields.io/github/stars/ThanhNguyxnOrg/apidex-hub?style=social)](https://github.com/ThanhNguyxnOrg/apidex-hub/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/ThanhNguyxnOrg/apidex-hub?style=social)](https://github.com/ThanhNguyxnOrg/apidex-hub/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/ThanhNguyxnOrg/apidex-hub)](https://github.com/ThanhNguyxnOrg/apidex-hub/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/ThanhNguyxnOrg/apidex-hub)](https://github.com/ThanhNguyxnOrg/apidex-hub/pulls)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Maintained](https://img.shields.io/badge/Maintained-Yes-brightgreen?style=flat-square)](https://github.com/ThanhNguyxnOrg/apidex-hub)
[![Visitors](https://api.visitorbadge.io/api/visitors?path=ThanhNguyxn%2Fapidex-hub&countColor=%23263759&style=flat)](https://visitorbadge.io/status?path=ThanhNguyxn%2Fapidex-hub)
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
| **Apify Key** | 🔑 | Token required to run Apify scrapers/actors | `Authorization: Bearer apify_api_...` |

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

## <a name="table-of-contents"></a>📊 API Catalog

We maintain a curated database of **31,938** public endpoints across **78** categories. You can browse the categories directly:

| Category | Category | Category |
| --- | --- | --- |
| [🐶 Animals](./apis/animals.md) | [🌸 Anime](./apis/anime.md) | [🛡️ Anti-Malware](./apis/anti-malware.md) |
| [🤖 Apify Agents](./apis/apify-agents.md) | [🧠 Apify AI](./apis/apify-ai.md) | [⚙️ Apify Automation](./apis/apify-automation.md) |
| [💼 Apify Business](./apis/apify-business.md) | [💻 Apify Developer Tools](./apis/apify-developer-tools.md) | [🛍️ Apify Ecommerce](./apis/apify-ecommerce.md) |
| [🔌 Apify Integrations](./apis/apify-integrations.md) | [💼 Apify Jobs](./apis/apify-jobs.md) | [🎯 Apify Lead Generation](./apis/apify-lead-generation.md) |
| [🧩 Apify MCP Servers](./apis/apify-mcp-servers.md) | [📰 Apify News](./apis/apify-news.md) | [🔓 Apify Open Source](./apis/apify-open-source.md) |
| [⚠️ Apify Other](./apis/apify-other.md) | [🏡 Apify Real Estate](./apis/apify-real-estate.md) | [🔍 Apify SEO Tools](./apis/apify-seo-tools.md) |
| [💬 Apify Social Media](./apis/apify-social-media.md) | [✈️ Apify Travel](./apis/apify-travel.md) | [📹 Apify Videos](./apis/apify-videos.md) |
| [🔐 Authentication & Identity](./apis/authentication-identity.md) | [⛓️ Blockchain & Web3](./apis/blockchain-web3.md) | [📚 Books & Literature](./apis/books.md) |
| [💼 Business](./apis/business.md) | [📅 Calendar & Holidays](./apis/calendar-holidays.md) | [☁️ Cloud Storage & Files](./apis/cloud-storage-files.md) |
| [⚙️ Continuous Integration](./apis/continuous-integration.md) | [🪙 Cryptocurrency](./apis/cryptocurrency.md) | [💱 Currency Exchange](./apis/currency-exchange.md) |
| [✅ Data Validation](./apis/data-validation.md) | [👤 Demographic Analysis](./apis/demographic-analysis.md) | [🎨 Design & Colors](./apis/design-colors.md) |
| [💻 Development](./apis/development.md) | [📖 Dictionaries](./apis/dictionaries.md) | [📄 Documents & Productivity](./apis/documents-productivity.md) |
| [🎓 Education](./apis/education.md) | [📧 Email & SMS](./apis/email-sms.md) | [🎮 Entertainment](./apis/entertainment.md) |
| [🌿 Environment & Climate](./apis/environment-climate.md) | [🎪 Events](./apis/events.md) | [💰 Finance](./apis/finance.md) |
| [🍔 Food & Drink](./apis/food-drink.md) | [🎮 Games & Comics](./apis/games-comics.md) | [🌍 Geocoding](./apis/geocoding.md) |
| [🌎 Geography & Countries](./apis/geography-countries.md) | [🏛️ Government & Civic](./apis/government-civic.md) | [❤️ Health](./apis/health.md) |
| [🏠 IoT & Smart Devices](./apis/iot-smart-devices.md) | [💼 Jobs & Career](./apis/jobs-career.md) | [🧠 Machine Learning](./apis/machine-learning.md) |
| [🔢 Math & Computation](./apis/math-computation.md) | [😂 Memes & Fun](./apis/memes-fun.md) | [🧪 Mock Data & Testing](./apis/mock-data-testing.md) |
| [📈 Monitoring & Observability](./apis/monitoring-observability.md) | [🏛️ Museums & Art](./apis/museums-art.md) | [🎵 Music](./apis/music.md) |
| [📰 News](./apis/news.md) | [🔓 Open Source Projects](./apis/open-source-projects.md) | [💭 Personality & Quotes](./apis/personality-quotes.md) |
| [📱 Phone & Telephony](./apis/phone-telephony.md) | [📷 Photography](./apis/photography.md) | [🎙️ Podcasts](./apis/podcasts.md) |
| [📊 Public Data & Datasets](./apis/public-data.md) | [🔬 Science & Space](./apis/science.md) | [🔐 Security & Validation](./apis/security-validation.md) |
| [🛍️ Shopping](./apis/shopping.md) | [💬 Social](./apis/social.md) | [⚽ Sports](./apis/sports.md) |
| [📝 Text Analysis & NLP](./apis/text-analysis-nlp.md) | [📦 Tracking & Logistics](./apis/tracking-logistics.md) | [🚆 Transportation](./apis/transportation.md) |
| [✈️ Travel & Tourism](./apis/travel-tourism.md) | [⚠️ Unofficial & Community APIs](./apis/unofficial-community.md) | [🔗 URL Shorteners](./apis/url-shorteners.md) |
| [🔧 Utilities & Tools](./apis/utilities-tools.md) | [📹 Video](./apis/video.md) | [🌤️ Weather](./apis/weather.md) |

*Note: The API database is automatically synchronized with our [APIDex Hub Website](https://thanhnguyxnorg.github.io/apidex-hub/).*


## 🤝 Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](./.github/CONTRIBUTING.md) before opening a pull request.

You can also use the GitHub issue templates to suggest new APIs, report bugs, or request improvements.

## 🛡️ Code of Conduct

This project follows the [Code of Conduct](./.github/CODE_OF_CONDUCT.md). Please be respectful and constructive.

## 📄 License

This project is licensed under the [MIT License](./LICENSE).

---

## 📈 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=ThanhNguyxnOrg/apidex-hub&type=Date)](https://star-history.com/#ThanhNguyxnOrg/apidex-hub&Date)

---

<div align="center">

**Don't forget to ⭐ this repo if you found it useful!**

</div>