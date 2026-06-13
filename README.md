<!--
🚨 CRITICAL RULE FOR AI AGENTS:
Before making ANY changes to this repository, you MUST read and follow the instructions in [ai-instructions.md](./ai-instructions.md).
- ONLY modify README.md to add, remove, or edit API listings.
- DO NOT edit, update, or regenerate site/src/data/apis.json or site/index.html locally.
- DO NOT run build commands (npm run build, pnpm build, etc.) locally.
- Website generation is fully automated via GitHub Actions in CI/CD.
-->
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

## 📊 API Catalog

We maintain a curated database of **1,546+** free public APIs across **60** categories. You can browse the categories directly:

| Category | Category | Category |
| --- | --- | --- |
| [🐶 Animals](./apis/animals.md) | [🎮 Entertainment](./apis/entertainment.md) | [🔓 Open Source Projects](./apis/open-source-projects.md) |
| [🌸 Anime](./apis/anime.md) | [🌿 Environment & Climate](./apis/environment-climate.md) | [💭 Personality & Quotes](./apis/personality-quotes.md) |
| [🛡️ Anti-Malware](./apis/anti-malware.md) | [🎪 Events](./apis/events.md) | [📱 Phone & Telephony](./apis/phone-telephony.md) |
| [🔐 Authentication & Identity](./apis/authentication-identity.md) | [💰 Finance](./apis/finance.md) | [📷 Photography](./apis/photography.md) |
| [⛓️ Blockchain & Web3](./apis/blockchain-web3.md) | [🍔 Food & Drink](./apis/food-drink.md) | [🎙️ Podcasts](./apis/podcasts.md) |
| [📚 Books & Literature](./apis/books.md) | [🎮 Games & Comics](./apis/games-comics.md) | [📊 Public Data & Datasets](./apis/public-data.md) |
| [💼 Business](./apis/business.md) | [🌍 Geocoding](./apis/geocoding.md) | [🔬 Science & Space](./apis/science.md) |
| [📅 Calendar & Holidays](./apis/calendar-holidays.md) | [🌎 Geography & Countries](./apis/geography-countries.md) | [🔐 Security & Validation](./apis/security-validation.md) |
| [☁️ Cloud Storage & Files](./apis/cloud-storage-files.md) | [🏛️ Government & Civic](./apis/government-civic.md) | [🛍️ Shopping](./apis/shopping.md) |
| [⚙️ Continuous Integration](./apis/continuous-integration.md) | [❤️ Health](./apis/health.md) | [💬 Social](./apis/social.md) |
| [🪙 Cryptocurrency](./apis/cryptocurrency.md) | [🏠 IoT & Smart Devices](./apis/iot-smart-devices.md) | [⚽ Sports](./apis/sports.md) |
| [💱 Currency Exchange](./apis/currency-exchange.md) | [💼 Jobs & Career](./apis/jobs-career.md) | [📝 Text Analysis & NLP](./apis/text-analysis-nlp.md) |
| [✅ Data Validation](./apis/data-validation.md) | [🧠 Machine Learning](./apis/machine-learning.md) | [📦 Tracking & Logistics](./apis/tracking-logistics.md) |
| [👤 Demographic Analysis](./apis/demographic-analysis.md) | [🔢 Math & Computation](./apis/math-computation.md) | [🚆 Transportation](./apis/transportation.md) |
| [🎨 Design & Colors](./apis/design-colors.md) | [😂 Memes & Fun](./apis/memes-fun.md) | [✈️ Travel & Tourism](./apis/travel-tourism.md) |
| [💻 Development](./apis/development.md) | [🧪 Mock Data & Testing](./apis/mock-data-testing.md) | [⚠️ Unofficial & Community APIs](./apis/unofficial-community.md) |
| [📖 Dictionaries](./apis/dictionaries.md) | [📈 Monitoring & Observability](./apis/monitoring-observability.md) | [🔗 URL Shorteners](./apis/url-shorteners.md) |
| [📄 Documents & Productivity](./apis/documents-productivity.md) | [🏛️ Museums & Art](./apis/museums-art.md) | [🔧 Utilities & Tools](./apis/utilities-tools.md) |
| [🎓 Education](./apis/education.md) | [🎵 Music](./apis/music.md) | [📹 Video](./apis/video.md) |
| [📧 Email & SMS](./apis/email-sms.md) | [📰 News](./apis/news.md) | [🌤️ Weather](./apis/weather.md) |

*Note: The API database is automatically synchronized with our [Awesome Free APIs Website](https://thanhnguyxnorg.github.io/awesome-free-apis/).*


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