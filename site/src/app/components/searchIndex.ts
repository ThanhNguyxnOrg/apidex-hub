import Fuse from "fuse.js";
import { apis, type Api } from "./data";

export const searchIndex = new Fuse<Api>(apis, {
  keys: [
    { name: "name", weight: 3 },
    { name: "description", weight: 1.5 },
    { name: "category", weight: 0.8 },
  ],
  threshold: 0.35,
  distance: 100,
  minMatchCharLength: 2,
  includeMatches: true,
});

export function fuzzySearchApis(
  query: string,
  filter: "all" | "no-auth" | "https" = "all"
): Api[] {
  let list = apis;
  if (filter === "no-auth") list = list.filter((a) => a.auth === "none");
  if (filter === "https") list = list.filter((a) => a.https);

  if (!query || !query.trim()) {
    return list.slice(0, 50);
  }

  const results = searchIndex.search(query.trim());
  let filtered = results.map((r) => r.item);

  if (filter === "no-auth") filtered = filtered.filter((a) => a.auth === "none");
  if (filter === "https") filtered = filtered.filter((a) => a.https);

  return filtered.slice(0, 50);
}
