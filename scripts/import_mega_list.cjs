const fs = require('fs');
const path = require('path');
const readline = require('readline');

// Category mapping from API-mega-list to apidex-hub
const categoryMapping = {
    'agents-apis-697': { file: 'apify-agents.md', id: 'apify-agents', name: 'Apify Agents', emoji: '🤖' },
    'ai-apis-1208': { file: 'apify-ai.md', id: 'apify-ai', name: 'Apify AI', emoji: '🧠' },
    'automation-apis-4825': { file: 'apify-automation.md', id: 'apify-automation', name: 'Apify Automation', emoji: '⚙️' },
    'business-apis-2': { file: 'apify-business.md', id: 'apify-business', name: 'Apify Business', emoji: '💼' },
    'developer-tools-apis-2652': { file: 'apify-developer-tools.md', id: 'apify-developer-tools', name: 'Apify Developer Tools', emoji: '💻' },
    'ecommerce-apis-2440': { file: 'apify-ecommerce.md', id: 'apify-ecommerce', name: 'Apify Ecommerce', emoji: '🛍️' },
    'integrations-apis-890': { file: 'apify-integrations.md', id: 'apify-integrations', name: 'Apify Integrations', emoji: '🔌' },
    'jobs-apis-848': { file: 'apify-jobs.md', id: 'apify-jobs', name: 'Apify Jobs', emoji: '💼' },
    'lead-generation-apis-3452': { file: 'apify-lead-generation.md', id: 'apify-lead-generation', name: 'Apify Lead Generation', emoji: '🎯' },
    'mcp-servers-apis-131': { file: 'apify-mcp-servers.md', id: 'apify-mcp-servers', name: 'Apify MCP Servers', emoji: '🧩' },
    'news-apis-590': { file: 'apify-news.md', id: 'apify-news', name: 'Apify News', emoji: '📰' },
    'open-source-apis-768': { file: 'apify-open-source.md', id: 'apify-open-source', name: 'Apify Open Source', emoji: '🔓' },
    'other-apis-1297': { file: 'apify-other.md', id: 'apify-other', name: 'Apify Other', emoji: '⚠️' },
    'real-estate-apis-851': { file: 'apify-real-estate.md', id: 'apify-real-estate', name: 'Apify Real Estate', emoji: '🏡' },
    'seo-tools-apis-710': { file: 'apify-seo-tools.md', id: 'apify-seo-tools', name: 'Apify SEO Tools', emoji: '🔍' },
    'social-media-apis-3268': { file: 'apify-social-media.md', id: 'apify-social-media', name: 'Apify Social Media', emoji: '💬' },
    'travel-apis-397': { file: 'apify-travel.md', id: 'apify-travel', name: 'Apify Travel', emoji: '✈️' },
    'videos-apis-979': { file: 'apify-videos.md', id: 'apify-videos', name: 'Apify Videos', emoji: '📹' }
};

const repoRoot = path.resolve(__dirname, '..');
const apisDir = path.join(repoRoot, 'apis');
const tempMegaListDir = path.join(repoRoot, 'scripts/temp_mega_list');

// Regular expression to parse row in API-mega-list READMEs
// Format: | [API Name](https://apify.com/...) | Description |
const rowRegex = /^\|\s*\[([^\]]+)\]\((https?:\/\/[^\)]+)\)\s*\|\s*([^\|]+)\s*\|/;

// Helper to normalize and update affiliate link
function normalizeUrl(urlStr, affToken = 'thanhnguyxn') {
    try {
        const url = new URL(urlStr);
        url.searchParams.set('fpr', affToken);
        return url.toString();
    } catch (e) {
        return urlStr;
    }
}

// Extract base URL path for comparison (ignoring params)
function getBaseUrl(urlStr) {
    try {
        const url = new URL(urlStr);
        return `${url.protocol}//${url.hostname}${url.pathname}`.toLowerCase();
    } catch (e) {
        return urlStr.toLowerCase();
    }
}

// Function to read all existing links in apidex-hub
function getExistingLinks() {
    const existing = new Set();
    const files = fs.readdirSync(apisDir).filter(f => f.endsWith('.md'));
    for (const file of files) {
        const content = fs.readFileSync(path.join(apisDir, file), 'utf8');
        const lines = content.split('\n');
        for (const line of lines) {
            // Match [Link](URL)
            const match = line.match(/\[Link\]\((https?:\/\/[^\)]+)\)/);
            if (match) {
                existing.add(getBaseUrl(match[1]));
            }
        }
    }
    return existing;
}

// Check link accessibility
async function checkLink(url, timeout = 6000) {
    try {
        const controller = new AbortController();
        const id = setTimeout(() => controller.abort(), timeout);
        const res = await fetch(url, {
            method: 'GET',
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            },
            signal: controller.signal
        });
        clearTimeout(id);
        
        // 404, 410 mean dead link. Other status codes (like 403, 429, 503) might be rate limited / Cloudflare, but the page exists.
        if (res.status === 404 || res.status === 410) {
            return { ok: false, status: res.status, reason: 'Not Found' };
        }
        return { ok: true, status: res.status };
    } catch (e) {
        if (e.name === 'AbortError') {
            return { ok: false, reason: 'Timeout' };
        }
        // If DNS fails or connection refused
        const msg = e.message.toLowerCase();
        if (msg.includes('getaddrinfo') || msg.includes('econnrefused') || msg.includes('fetch failed')) {
            return { ok: false, reason: 'Connection Failure' };
        }
        return { ok: true, note: `Error: ${e.message} - keeping` }; // Assume it might be temporary/WAF
    }
}

// Concurrent link checker
async function checkAllLinks(urls, batchSize = 30) {
    const results = {};
    for (let i = 0; i < urls.length; i += batchSize) {
        const batch = urls.slice(i, i + batchSize);
        console.log(`Checking link batch ${Math.floor(i / batchSize) + 1}/${Math.ceil(urls.length / batchSize)} (${batch.length} URLs)...`);
        
        const promises = batch.map(async (url) => {
            const check = await checkLink(url);
            results[url] = check;
        });
        
        await Promise.all(promises);
        // Delay between batches to prevent severe rate limiting
        await new Promise(r => setTimeout(r, 100));
    }
    return results;
}

// Parse a README.md file from API-mega-list folder
function parseMegaListReadme(filePath) {
    const apis = [];
    if (!fs.existsSync(filePath)) return apis;
    const content = fs.readFileSync(filePath, 'utf8');
    const lines = content.split('\n');
    for (const line of lines) {
        const match = line.trim().match(rowRegex);
        if (match) {
            const name = match[1].trim();
            const link = match[2].trim();
            const desc = match[3].trim();
            
            apis.push({
                name,
                link,
                description: desc
            });
        }
    }
    return apis;
}

// Parse all target directories and build a clean API list per category
async function main() {
    console.log("Starting Apify API Mega List Import...");
    
    // 1. Gather all existing links for deduplication
    console.log("Reading existing API links for deduplication...");
    const existingLinks = getExistingLinks();
    console.log(`Found ${existingLinks.size} existing APIs in local repo.`);
    
    // 2. Parse all categories from temp_mega_list
    const newApisByCategory = {};
    let totalParsed = 0;
    
    for (const [folderName, catInfo] of Object.entries(categoryMapping)) {
        const readmePath = path.join(tempMegaListDir, folderName, 'README.md');
        if (!fs.existsSync(readmePath)) {
            console.warn(`Category readme not found: ${readmePath}`);
            continue;
        }
        
        const parsed = parseMegaListReadme(readmePath);
        console.log(`Parsed ${parsed.length} APIs from ${folderName}`);
        
        // Filter out duplicates and normalize affiliate links
        const filtered = [];
        for (const api of parsed) {
            const normalizedLink = normalizeUrl(api.link);
            const baseLink = getBaseUrl(normalizedLink);
            
            if (existingLinks.has(baseLink)) {
                // Skip if already in the target repo
                continue;
            }
            
            filtered.push({
                name: api.name,
                link: normalizedLink,
                description: `(Apify Scraper) ${api.description}`
            });
        }
        
        newApisByCategory[folderName] = filtered;
        totalParsed += filtered.length;
    }
    
    console.log(`Total new unique APIs parsed: ${totalParsed}`);
    
    // 3. Gather all unique URLs to check
    const uniqueUrlsToCheckSet = new Set();
    for (const apis of Object.values(newApisByCategory)) {
        for (const api of apis) {
            uniqueUrlsToCheckSet.add(api.link);
        }
    }
    const uniqueUrlsToCheck = Array.from(uniqueUrlsToCheckSet);
    console.log(`Total unique URLs to verify: ${uniqueUrlsToCheck.length}`);
    
    // 4. Run concurrent link check
    console.log("Verifying URLs... This may take a few minutes...");
    const checkResults = await checkAllLinks(uniqueUrlsToCheck);
    
    // Filter out broken links
    let totalWorking = 0;
    let totalBroken = 0;
    const workingUrls = new Set();
    
    for (const [url, result] of Object.entries(checkResults)) {
        if (result.ok) {
            workingUrls.add(url);
            totalWorking++;
        } else {
            totalBroken++;
        }
    }
    console.log(`Link verification summary: ${totalWorking} working/protected URLs, ${totalBroken} broken URLs.`);
    
    // 5. Merge valid APIs into target files
    console.log("Merging valid new APIs into category markdown files...");
    
    for (const [folderName, catInfo] of Object.entries(categoryMapping)) {
        const apis = newApisByCategory[folderName] || [];
        const validApis = apis.filter(api => workingUrls.has(api.link));
        
        if (validApis.length === 0) {
            console.log(`No new valid APIs for category ${catInfo.name}`);
            continue;
        }
        
        const targetFilePath = path.join(apisDir, catInfo.file);
        let header = '';
        let existingApis = [];
        
        if (fs.existsSync(targetFilePath)) {
            // Read existing category file
            const fileContent = fs.readFileSync(targetFilePath, 'utf8');
            const lines = fileContent.split('\n');
            let foundTableHeader = false;
            
            for (let i = 0; i < lines.length; i++) {
                const line = lines[i].trim();
                if (line.startsWith('## <a id=')) {
                    header = lines.slice(0, i + 1).join('\n') + '\n';
                }
                
                // Parse API rows from the existing table
                if (line.startsWith('|')) {
                    // Split and clean parts
                    let parts = line.split('|').map(p => p.trim());
                    if (parts[0] === '') parts.shift();
                    if (parts[parts.length - 1] === '') parts.pop();
                    
                    if (parts.length >= 5) {
                        const nameRaw = parts[0];
                        const name = nameRaw.replace(/\*\*(.+?)\*\*/g, '$1').trim();
                        if (name && !name.startsWith('---') && name !== 'API Name' && name !== 'Name') {
                            const desc = parts[1];
                            const auth = parts[2];
                            const https = parts[3];
                            const linkRaw = parts[4];
                            const linkMatch = linkRaw.match(/\[Link\]\((.*?)\)/);
                            const link = linkMatch ? linkMatch[1] : '';
                            
                            existingApis.push({ name, description: desc, auth, https, link });
                        }
                    }
                }
            }
            
            if (!header) {
                header = `## <a id="${catInfo.id}"></a>${catInfo.emoji} ${catInfo.name}\n`;
            }
        } else {
            // Create brand new header
            header = `## <a id="${catInfo.id}"></a>${catInfo.emoji} ${catInfo.name}\n`;
        }
        
        // Combine, deduplicate, and sort
        const combinedMap = new Map();
        
        // Add existing
        for (const api of existingApis) {
            combinedMap.set(api.name.toLowerCase(), api);
        }
        
        // Add new Apify APIs
        for (const api of validApis) {
            // Check if name or normalized link already exists in combined list
            const key = api.name.toLowerCase();
            if (!combinedMap.has(key)) {
                combinedMap.set(key, {
                    name: api.name,
                    description: api.description,
                    auth: '🔑 Apify Key',
                    https: '✅',
                    link: api.link
                });
            }
        }
        
        // Sort alphabetically by name
        const sortedApis = Array.from(combinedMap.values()).sort((a, b) => {
            return a.name.localeCompare(b.name, 'en', { sensitivity: 'base' });
        });
        
        // Reconstruct markdown table
        let tableContent = '\n| API Name | Description | Auth | HTTPS | Link |\n';
        tableContent += '| :--- | :--- | :---: | :---: | :---: |\n';
        for (const api of sortedApis) {
            // Format name in bold
            tableContent += `| **${api.name}** | ${api.description} | ${api.auth} | ${api.https} | [Link](${api.link}) |\n`;
        }
        
        tableContent += '\n[⬆ Back to Table of Contents](../README.md#table-of-contents)\n';
        
        // Write file
        const finalContent = header + tableContent;
        fs.writeFileSync(targetFilePath, finalContent, 'utf8');
        console.log(`Successfully updated/created ${catInfo.file} with ${sortedApis.length} total APIs.`);
    }
    
    // 6. Reconstruct the Table of Contents in README.md
    console.log("Updating Table of Contents in README.md...");
    const readmePath = path.join(repoRoot, 'README.md');
    if (fs.existsSync(readmePath)) {
        let content = fs.readFileSync(readmePath, 'utf8');
        
        // Find existing files in apis/ directory to construct sorted list of categories
        const files = fs.readdirSync(apisDir).filter(f => f.endsWith('.md')).sort();
        const categories = [];
        for (const file of files) {
            const fileContent = fs.readFileSync(path.join(apisDir, file), 'utf8');
            const lines = fileContent.split('\n');
            for (const line of lines) {
                if (line.trim().startsWith('## <a id=')) {
                    const match = line.trim().match(/^##\s+(?:<a\s+id="([^"]+)"\s*>\s*<\/a>\s*)?(\S+)\s+(.+)$/);
                    if (match) {
                        const id = match[1];
                        const emoji = match[2];
                        const name = match[3].trim();
                        categories.push({ file, id, emoji, name });
                        break;
                    }
                }
            }
        }
        
        // Construct 3-column table markdown
        let toc = '| Category | Category | Category |\n| --- | --- | --- |\n';
        for (let i = 0; i < categories.length; i += 3) {
            const cols = [];
            for (let j = 0; j < 3; j++) {
                if (i + j < categories.length) {
                    const cat = categories[i + j];
                    cols.push(`[${cat.emoji} ${cat.name}](./apis/${cat.file})`);
                } else {
                    cols.push('');
                }
            }
            toc += `| ${cols.join(' | ')} |\n`;
        }
        
        // Replace TOC in README.md
        // Find table between ## <a name="table-of-contents"></a>📊 API Catalog and the Contributing section
        const startMarker = '## <a name="table-of-contents"></a>📊 API Catalog';
        const endMarker = '## 🤝 Contributing';
        
        const startIndex = content.indexOf(startMarker);
        const endIndex = content.indexOf(endMarker);
        
        if (startIndex !== -1 && endIndex !== -1) {
            const pre = content.substring(0, startIndex + startMarker.length);
            const post = content.substring(endIndex);
            
            // Construct catalog section
            const catalogSection = `\n\nWe maintain a curated database of **0** free public APIs across **0** categories. You can browse the categories directly:\n\n${toc}\n*Note: The API database is automatically synchronized with our [APIDex Hub Website](https://thanhnguyxnorg.github.io/apidex-hub/).*\n\n\n`;
            
            content = pre + catalogSection + post;
            fs.writeFileSync(readmePath, content, 'utf8');
            console.log("Successfully updated README.md Table of Contents.");
        } else {
            console.warn("Could not find Table of Contents section markers in README.md.");
        }
    }
    
    // 7. Cleanup temp folder
    console.log("Cleaning up temp folder...");
    try {
        fs.rmSync(tempMegaListDir, { recursive: true, force: true });
        console.log("Temp folder deleted.");
    } catch (e) {
        console.warn(`Failed to delete temp folder: ${e.message}`);
    }
    
    console.log("Import process complete.");
}

main().catch(e => {
    console.error("Fatal error during import:", e);
});
