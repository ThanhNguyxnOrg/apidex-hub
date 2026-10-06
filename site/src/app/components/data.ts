import apiData from "../../data/apis.json";

// ── Types ──────────────────────────────────────────────
export type AuthType = "none" | "apiKey" | "oauth";

export interface Api {
  name: string;
  description: string;
  auth: AuthType;
  https: boolean;
  link: string;
  category: string; // slug matching category.id
  featured?: boolean;
}

export interface Category {
  name: string;
  emoji: string;
  slug: string;
  count: number;
  description?: string;
}

// ── Featured list (curated popular APIs) ───────────────
const FEATURED_NAMES = new Set([
  "GitHub",
  "Stripe",
  "OpenAI",
  "Spotify",
  "NASA",
  "PokeAPI",
  "CoinGecko",
  "Unsplash",
  "OpenWeatherMap",
  "TMDB",
  "Google Maps",
  "Twilio",
  "JSONPlaceholder",
  "Dog CEO",
]);

// ── Exclude non-API sections ───────────────────────────
const EXCLUDE_IDS = new Set([
  "contributing",
  "code-of-conduct",
  "license",
  "star-history",
  "general-api-usage-guide",
]);

// ── Auth mapping (README format → component format) ────
function mapAuth(raw: string): AuthType {
  const lower = raw.toLowerCase();
  if (lower === "oauth") return "oauth";
  if (lower === "apikey") return "apiKey";
  return "none"; // "No" or anything else
}

// ── Build categories ───────────────────────────────────
export const categories: Category[] = (apiData.categories as any[])
  .filter((c) => !EXCLUDE_IDS.has(c.id) && c.api_count > 0)
  .map((c) => ({
    name: c.name,
    emoji: c.emoji,
    slug: c.id,
    count: c.api_count,
  }));

// ── Build flat API list ────────────────────────────────
export const apis: Api[] = (apiData.categories as any[])
  .filter((c) => !EXCLUDE_IDS.has(c.id) && c.api_count > 0)
  .flatMap((c) =>
    (c.apis as any[]).map((a) => ({
      name: a.name,
      description: a.description,
      auth: mapAuth(a.auth),
      https: a.https,
      link: a.link,
      category: c.id,
      featured: FEATURED_NAMES.has(a.name),
    }))
  );

// ── Stats from JSON meta ───────────────────────────────
export const stats = {
  total: apiData.meta.total_apis,
  categories: categories.length,
  noAuth: apiData.meta.no_auth_count,
  apiKey: apiData.meta.api_key_count || 0,
  oauth: apiData.meta.oauth_count || 0,
  httpsCount: apiData.meta.https_count || 0,
  httpsPercent: apiData.meta.https_percentage,
};
