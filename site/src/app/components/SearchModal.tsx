import { useEffect, useMemo, useState } from "react";
import { Search, X, Shield, Lock, Globe } from "lucide-react";
import { apis, categories } from "./data";
import { AuthBadge } from "./AuthBadge";

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
    const q = query.trim().toLowerCase();
    let baseApis = apis;
    if (filter === "no-auth") {
      baseApis = apis.filter((a) => a.auth === "none");
    } else if (filter === "https") {
      baseApis = apis.filter((a) => a.https);
    }

    const filtered = q
      ? baseApis.filter(
          (a) =>
            a.name.toLowerCase().includes(q) ||
            a.description.toLowerCase().includes(q) ||
            a.category.toLowerCase().includes(q)
        ).slice(0, 100)
      : baseApis.filter((a) => a.featured);
    const map = new Map<string, typeof apis>();
    for (const api of filtered) {
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
      className="fixed inset-0 z-50 flex items-start justify-center px-4 pt-24 bg-black/60 backdrop-blur-sm"
      style={{
        animation: "fadeIn 0.15s ease-out",
      }}
      onClick={onClose}
    >
      <div
        className="w-full max-w-2xl overflow-hidden rounded-2xl border border-border bg-card text-left shadow-2xl"
        style={{
          animation: "fadeInUp 0.2s ease-out",
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center gap-3 px-5 border-b border-border h-15">
          <Search size={18} className="text-muted-foreground" />
          <input
            autoFocus
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search APIs by name, description, or category..."
            className="flex-1 bg-transparent outline-none text-foreground text-sm font-sans placeholder-muted-foreground/60"
          />
          <button
            onClick={onClose}
            className="flex h-7 items-center gap-1 rounded-lg px-2 bg-muted border border-border text-muted-foreground hover:text-foreground font-mono text-[10px] transition-colors"
          >
            ESC <X size={12} />
          </button>
        </div>

        {/* Filter Chips */}
        <div className="flex items-center gap-2 px-5 py-2.5 bg-muted/30 border-b border-border text-xs select-none">
          <span className="text-muted-foreground mr-1.5 font-medium">Filter:</span>
          <button
            onClick={() => setFilter("all")}
            className={`flex items-center gap-1.5 px-3 py-1 rounded-full border transition-all duration-200 cursor-pointer ${
              filter === "all"
                ? "bg-primary/10 border-primary/30 text-primary font-semibold"
                : "border-border hover:bg-secondary text-muted-foreground hover:text-foreground"
            }`}
          >
            <Globe size={11} /> All APIs
          </button>
          <button
            onClick={() => setFilter("no-auth")}
            className={`flex items-center gap-1.5 px-3 py-1 rounded-full border transition-all duration-200 cursor-pointer ${
              filter === "no-auth"
                ? "bg-primary/10 border-primary/30 text-primary font-semibold"
                : "border-border hover:bg-secondary text-muted-foreground hover:text-foreground"
            }`}
          >
            <Shield size={11} /> No Auth
          </button>
          <button
            onClick={() => setFilter("https")}
            className={`flex items-center gap-1.5 px-3 py-1 rounded-full border transition-all duration-200 cursor-pointer ${
              filter === "https"
                ? "bg-primary/10 border-primary/30 text-primary font-semibold"
                : "border-border hover:bg-secondary text-muted-foreground hover:text-foreground"
            }`}
          >
            <Lock size={11} /> HTTPS
          </button>
        </div>

        <div className="max-h-[60vh] overflow-y-auto p-3">
          {grouped.length === 0 ? (
            <div className="px-4 py-12 text-center text-muted-foreground text-sm">
              No APIs match "{query}"
            </div>
          ) : (
            <>
              {!query && (
                <div className="px-3 py-2 text-muted-foreground/50 font-mono text-[10px] uppercase tracking-wider font-semibold">
                  Featured
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
                    className="flex w-full items-center gap-2 px-3 py-1.5 text-muted-foreground hover:text-foreground hover:bg-secondary/40 rounded-lg text-xs font-semibold uppercase tracking-wider transition-all"
                  >
                    <span>{category?.emoji}</span>
                    <span>{category?.name}</span>
                  </button>
                  <div className="mt-1 space-y-0.5">
                    {list.map((api) => (
                      <a
                        key={api.name}
                        href={api.link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-3 rounded-xl px-3 py-2.5 hover:bg-secondary/60 transition-colors"
                      >
                        <div className="min-w-0 flex-1">
                          <div className="font-bold text-foreground text-sm leading-snug">
                            {api.name}
                          </div>
                          <div className="text-muted-foreground text-xs mt-1 truncate">
                            {api.description}
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
