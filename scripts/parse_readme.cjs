const fs = require('fs');
const path = require('path');

function parseCategoryHeader(line) {
    const match = line.trim().match(/^##\s+(?:<a\s+id="([^"]+)"\s*>\s*<\/a>\s*)?(\S+)\s+(.+)$/);
    if (match) {
        const anchor = match[1] || "";
        const emoji = match[2];
        const name = match[3].trim();
        return {
            id: anchor || name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, ''),
            emoji: emoji,
            name: name
        };
    }
    return null;
}

function parseApiRow(line) {
    let parts = line.split('|').map(p => p.trim());
    if (parts[0] === '') parts.shift();
    if (parts[parts.length - 1] === '') parts.pop();
    
    if (parts.length < 5) return null;
    
    const nameRaw = parts[0];
    const description = parts[1];
    const authRaw = parts[2];
    const httpsRaw = parts[3];
    const linkRaw = parts[4];
    
    const name = nameRaw.replace(/\*\*(.+?)\*\*/g, '$1').trim();
    if (!name || name.startsWith('---') || name.startsWith(':---') || name === 'API Name' || name === 'Name') {
        return null;
    }
    
    let auth = "No";
    const authLower = authRaw.toLowerCase();
    if (authLower.includes("oauth") || authRaw.includes("🔐")) {
        auth = "OAuth";
    } else if (authLower.includes("apikey") || authLower.includes("api key") || authRaw.includes("🔑")) {
        auth = "apiKey";
    }
    
    const httpsLower = httpsRaw.toLowerCase();
    const https = httpsRaw.includes("✅") || httpsLower.includes("yes") || httpsLower.includes("true");
    
    const linkMatch = linkRaw.match(/\[.*?\]\((.*?)\)/);
    const link = linkMatch ? linkMatch[1] : "";
    
    return {
        name,
        description,
        auth,
        https,
        link
    };
}

function parseReadme(readmeDir) {
    const files = fs.readdirSync(readmeDir)
        .filter(f => f.endsWith('.md'))
        .sort();
    
    const contentParts = [];
    for (const file of files) {
        contentParts.push(fs.readFileSync(path.join(readmeDir, file), 'utf8'));
    }
    const content = contentParts.join('\n\n');
    const lines = content.split('\n');
    
    const categories = [];
    let currentCategory = null;
    const skipSections = new Set(["general-api-usage-guide", "general api usage guide"]);
    
    for (const line of lines) {
        const stripped = line.trim();
        
        if (stripped.startsWith('## ')) {
            const cat = parseCategoryHeader(stripped);
            if (cat) {
                const catIdLower = cat.id.toLowerCase();
                const catNameLower = cat.name.toLowerCase();
                if (skipSections.has(catIdLower) || catNameLower.includes('table of contents') || catNameLower.includes('usage guide') || catNameLower.includes('code examples')) {
                    currentCategory = null;
                    continue;
                }
                cat.apis = [];
                categories.push(cat);
                currentCategory = cat;
            } else {
                currentCategory = null;
            }
            continue;
        }
        
        if (currentCategory && stripped.startsWith('|')) {
            const api = parseApiRow(stripped);
            if (api) {
                currentCategory.apis.push(api);
            }
        }
    }
    
    const totalApis = categories.reduce((sum, cat) => sum + cat.apis.length, 0);
    const totalCategories = categories.length;
    const noAuthCount = categories.reduce((sum, cat) => sum + cat.apis.filter(api => api.auth === 'No').length, 0);
    const apiKeyCount = categories.reduce((sum, cat) => sum + cat.apis.filter(api => api.auth === 'apiKey').length, 0);
    const oauthCount = categories.reduce((sum, cat) => sum + cat.apis.filter(api => api.auth === 'OAuth').length, 0);
    const httpsCount = categories.reduce((sum, cat) => sum + cat.apis.filter(api => api.https).length, 0);
    const httpsPct = totalApis > 0 ? Math.round((httpsCount / totalApis) * 100) : 0;
    
    const output = {
        meta: {
            generated_at: new Date().toISOString(),
            source: "README.md",
            total_apis: totalApis,
            total_categories: totalCategories,
            no_auth_count: noAuthCount,
            api_key_count: apiKeyCount,
            oauth_count: oauthCount,
            https_count: httpsCount,
            https_percentage: httpsPct
        },
        categories: []
    };
    
    for (const cat of categories) {
        output.categories.push({
            id: cat.id,
            emoji: cat.emoji,
            name: cat.name,
            api_count: cat.apis.length,
            apis: cat.apis
        });
    }
    
    return output;
}

const repoRoot = path.resolve(__dirname, '..');
const readmeDir = path.join(repoRoot, 'apis');
const outputPath = path.join(repoRoot, 'site/src/data/apis.json');

console.log(`Parsing ${readmeDir}...`);
const data = parseReadme(readmeDir);

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, JSON.stringify(data, null, 2), 'utf8');
console.log(`Generated ${outputPath}`);

const totalApis = data.meta.total_apis;
const totalCategories = data.meta.total_categories;

// Update site/index.html
const indexHtmlPath = path.join(repoRoot, 'site/index.html');
if (fs.existsSync(indexHtmlPath)) {
    console.log(`Updating count in ${indexHtmlPath}...`);
    try {
        const content = fs.readFileSync(indexHtmlPath, 'utf8');
        const updatedContent = content.replace(/\b[\d,]+(?:\+)?(?=\s+[pP]ublic\s+[aA][pP][iI]s)/gi, totalApis.toLocaleString());
        fs.writeFileSync(indexHtmlPath, updatedContent, 'utf8');
        console.log(`  Successfully updated index.html with ${totalApis.toLocaleString()} APIs`);
    } catch (e) {
        console.warn(`  WARNING: Failed to update index.html: ${e}`);
    }
}

// Update README.md
const readmePath = path.join(repoRoot, 'README.md');
if (fs.existsSync(readmePath)) {
    console.log(`Updating count in ${readmePath}...`);
    try {
        let content = fs.readFileSync(readmePath, 'utf8');
        content = content.replace(
            /(\bdatabase of \*\*)[\d,]+(?:\+)?(?=\*\* public endpoints across \*\*)/,
            `$1${totalApis.toLocaleString()}`
        );
        content = content.replace(
            /(public endpoints across \*\*)[\d,]+(?=\*\* categories)/,
            `$1${totalCategories}`
        );
        fs.writeFileSync(readmePath, content, 'utf8');
        console.log(`  Successfully updated README.md with ${totalApis.toLocaleString()} APIs and ${totalCategories} categories`);
    } catch (e) {
        console.warn(`  WARNING: Failed to update README.md: ${e}`);
    }
}

console.log(`Done!`);
console.log(`  ${data.meta.total_apis} APIs across ${data.meta.total_categories} categories`);
console.log(`  ${data.meta.no_auth_count} require no auth`);
console.log(`  ${data.meta.api_key_count} require apiKey`);
console.log(`  ${data.meta.oauth_count} require OAuth`);
console.log(`  ${data.meta.https_percentage}% use HTTPS`);
