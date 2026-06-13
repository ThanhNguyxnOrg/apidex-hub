import { useEffect, useMemo, useState } from "react";
import { Search, X } from "lucide-react";
import { apis, categories } from "./data";
import { AuthBadge } from "./AuthBadge";

export function SearchModal({
  open,
  onClose,
  onSelectCategory,
}: {
  open: boolean;
  onClose: () => void;
  onSelectCategory: (slug: string) => void;
}) {
  const [query, setQuery] = useState("");

  useEffect(() => {
    if (!open) setQuery("");
  }, [open]);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    if (open) window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [open, onClose]);

  const grouped = useMemo(() => {
    const q = query.trim().toLowerCase();
    const filtered = q
      ? apis.filter(
          (a) =>
            a.name.toLowerCase().includes(q) ||
            a.description.toLowerCase().includes(q) ||
            a.category.toLowerCase().includes(q)
        )
      : apis.filter((a) => a.featured);
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
  }, [query]);

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
