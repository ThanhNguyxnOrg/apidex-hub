# Scripts & Tools

This directory contains utility scripts for maintaining the apidex-hub repository.

## 📁 Contents

### `check_links.py`
**Link checker with improved accuracy**

Checks all API links in the apis/ directory and categorizes them:
- ✅ **Working** - HTTP 200-204, APIs are functional
- 🛡️ **Protected** - HTTP 403/429 (bot protection, API still works)
- ⚠️ **Warnings** - Timeouts, SSL issues (temporary, not dead)
- 🔶 **Errors** - Server errors (500s, may be temporary)
- ❌ **Broken** - 404, DNS failure (truly dead)

**Features:**
- Retry logic with exponential backoff
- Realistic browser User-Agent
- Session pooling for efficiency
- Categorized results to reduce false positives

**Usage:**
```bash
cd scripts
python check_links.py
```

**Output:**
- Console: Real-time progress with categorization
- File: `link_check_report.txt` with detailed results

**Important Notes:**
- **403/429 errors** = Bot protection, NOT broken APIs
- **Timeouts** = Slow servers, NOT necessarily dead
- Only remove links showing **404/DNS failures**

---

## 🎯 Best Practices

### When to Remove an API:
- ✅ **404 Not Found** + verified in browser
- ✅ **DNS failure** (domain doesn't resolve)
- ✅ **Official shutdown announcement**
- ✅ **Service confirmed dead** (e.g., FTX collapse)

### When NOT to Remove:
- ❌ **403 Forbidden** - Usually bot protection
- ❌ **429 Rate Limited** - API is working, just busy
- ❌ **Timeouts** - May be slow, not dead
- ❌ **SSL errors** - Certificate issue, not service dead

Always manually verify in a browser before removing!
