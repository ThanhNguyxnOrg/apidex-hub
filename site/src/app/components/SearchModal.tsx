import { useEffect, useMemo, useState } from "react";
import { Search, X, Shield, Lock, Globe } from "lucide-react";
import { categories } from "./data";
import { AuthBadge } from "./AuthBadge";
import { fuzzySearchApis } from "./searchIndex";
import { Highlight } from "./Highlight";
import { CategoryIcon } from "./categoryIcons";

export type FilterType = "all" | "no-auth" | "https";

export function SearchModal({
  open,
  onClose,
  onSelectCategory,
  initialFilter = "all",
}: {
  open: boolean;
  onClose: () => void;
  onSelectCategory: (slug: string) => void;
  initialFilter?: FilterType;
}) {
  const [query, setQuery] = useState("");
  const [filter, setFilter] = useState<FilterType>(initialFilter);

  useEffect(() => {
    if (!open) {
      setQuery("");
    } else {
      setFilter(initialFilter);
    }
  }, [open, initialFilter]);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    if (open) window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [open, onClose]);

  const grouped = useMemo(() => {
    const matchedApis = fuzzySearchApis(query, filter);
    const map = new Map<string, typeof matchedApis>();
    for (const api of matchedApis) {
      const arr = map.get(api.category) ?? [];
      arr.push(api);
      map.set(api.category, arr);
    }
    return Array.from(map.entries()).map(([slug, list]) => ({
      category: categories.find((c) => c.slug === slug),
      list,
    }));
  }, [query, filter]);

  if (!open) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-start justify-center px-4 pt-20 sm:pt-24 bg-black/60 backdrop-blur-md"
      style={{ animation: "fadeIn 0.15s ease-out" }}
      onClick={onClose}
      role="dialog"
      aria-modal="true"
      aria-label="Search APIs"
    >
      <div
        className="w-full max-w-2xl overflow-hidden rounded-2xl border border-border/80 bg-card/95 text-left shadow-2xl backdrop-blur-xl ring-1 ring-white/10"
        style={{ animation: "fadeInUp 0.2s cubic-bezier(0.16, 1, 0.3, 1)" }}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center gap-3 px-5 border-b border-border/80 h-16">
          <Search size={18} className="text-primary shrink-0" />
          <input
            autoFocus
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search 12,500+ APIs (e.g. stripe, weather, ai, cat)..."
            className="flex-1 bg-transparent outline-none text-foreground text-sm font-sans placeholder-muted-foreground/60"
            aria-label="Search query"
          />
          <button
            onClick={onClose}
            aria-label="Close search dialog"
            className="flex h-7 items-center gap-1.5 rounded-lg px-2.5 bg-muted/80 border border-border text-muted-foreground hover:text-foreground font-mono text-[11px] transition-colors focus-visible:ring-2 focus-visible:ring-primary outline-none"
          >
            ESC <X size={12} />
          </button>
        </div>

        {/* Filter Chips */}
        <div className="flex items-center gap-2 px-5 py-2.5 bg-muted/40 border-b border-border/80 text-xs select-none">
          <span className="text-muted-foreground mr-1.5 font-medium">Filter:</span>
          <button
            onClick={() => setFilter("all")}
            className={`flex items-center gap-1.5 px-3 py-1 rounded-full border transition-all duration-200 cursor-pointer text-xs ${
              filter === "all"
                ? "bg-primary/15 border-primary/40 text-primary font-semibold shadow-xs"
                : "border-border hover:bg-secondary text-muted-foreground hover:text-foreground"
            }`}
          >
            <Globe size={11} /> All APIs
          </button>
          <button
            onClick={() => setFilter("no-auth")}
            className={`flex items-center gap-1.5 px-3 py-1 rounded-full border transition-all duration-200 cursor-pointer text-xs ${
              filter === "no-auth"
                ? "bg-primary/15 border-primary/40 text-primary font-semibold shadow-xs"
                : "border-border hover:bg-secondary text-muted-foreground hover:text-foreground"
            }`}
          >
            <Shield size={11} /> No Auth
          </button>
          <button
            onClick={() => setFilter("https")}
            className={`flex items-center gap-1.5 px-3 py-1 rounded-full border transition-all duration-200 cursor-pointer text-xs ${
              filter === "https"
                ? "bg-primary/15 border-primary/40 text-primary font-semibold shadow-xs"
                : "border-border hover:bg-secondary text-muted-foreground hover:text-foreground"
            }`}
          >
            <Lock size={11} /> HTTPS
          </button>
        </div>

        <div className="max-h-[60vh] overflow-y-auto p-3">
          {grouped.length === 0 ? (
            <div className="px-4 py-14 text-center text-muted-foreground text-sm">
              No APIs found matching <span className="text-foreground font-semibold">"{query}"</span>
            </div>
          ) : (
            <>
              {!query && (
                <div className="px-3 py-2 text-muted-foreground/60 font-mono text-[10px] uppercase tracking-wider font-semibold">
                  Featured Recommendations
                </div>
              )}
              {grouped.map(({ category, list }) => (
                <div key={category?.slug} className="mb-4">
                  <button
                    onClick={() => {
                      if (category) {
                        onSelectCategory(category.slug);
                        onClose();
                      }
                    }}
                    className="flex w-full items-center gap-2.5 px-3 py-1.5 text-muted-foreground hover:text-foreground hover:bg-secondary/40 rounded-lg text-xs font-semibold uppercase tracking-wider transition-all"
                  >
                    {category && <CategoryIcon slug={category.slug} className="w-4 h-4 text-primary" />}
                    <span>{category?.name}</span>
                    <span className="ml-auto text-[10px] font-mono text-muted-foreground/70 lowercase">
                      /{category?.slug}
                    </span>
                  </button>
                  <div className="mt-1 space-y-1">
                    {list.map((api) => (
                      <a
                        key={api.name}
                        href={api.link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-3 rounded-xl px-3 py-2.5 hover:bg-secondary/60 border border-transparent hover:border-border/60 transition-all group"
                      >
                        <div className="min-w-0 flex-1">
                          <div className="font-bold text-foreground text-sm leading-snug group-hover:text-primary transition-colors">
                            <Highlight text={api.name} query={query} />
                          </div>
                          <div className="text-muted-foreground text-xs mt-1 truncate">
                            <Highlight text={api.description} query={query} />
                          </div>
                        </div>
                        <div className="shrink-0">
                          <AuthBadge type={api.auth} />
                        </div>
                      </a>
                    ))}
                  </div>
                </div>
              ))}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
