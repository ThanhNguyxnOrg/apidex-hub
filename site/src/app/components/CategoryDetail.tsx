import { useMemo, useState } from "react";
import { ArrowLeft, ArrowUpDown, LayoutGrid, List } from "lucide-react";
import { apis, categories, type Category } from "./data";
import { ApiCard } from "./ApiCard";
import { AuthBadge, HttpsBadge } from "./AuthBadge";
import { categoryDescriptions } from "./categoryDescriptions";

export function CategoryDetail({
  category,
  onBack,
  onSelectCategory,
}: {
  category: Category;
  onBack: () => void;
  onSelectCategory: (c: Category) => void;
}) {
  const [view, setView] = useState<"cards" | "list">("cards");
  const [filter, setFilter] = useState<"all" | "none" | "apiKey" | "oauth">("all");
  const [sort, setSort] = useState<"default" | "az" | "za" | "featured">("default");

  const items = useMemo(() => {
    let base = apis.filter((a) => a.category === category.slug);
    if (filter !== "all") base = base.filter((a) => a.auth === filter);
    const sorted = [...base];
    if (sort === "az") sorted.sort((a, b) => a.name.localeCompare(b.name));
    else if (sort === "za") sorted.sort((a, b) => b.name.localeCompare(a.name));
    else if (sort === "featured")
      sorted.sort((a, b) => Number(!!b.featured) - Number(!!a.featured));
    return sorted;
  }, [category.slug, filter, sort]);

  const stats = useMemo(() => {
    const list = apis.filter((a) => a.category === category.slug);
    return {
      total: category.count,
      noAuth: list.filter((a) => a.auth === "none").length,
      apiKey: list.filter((a) => a.auth === "apiKey").length,
      oauth: list.filter((a) => a.auth === "oauth").length,
    };
  }, [category]);

  const statCards = [
    { v: stats.total, l: "Total APIs", colorClass: "text-blue-500" },
    { v: stats.noAuth, l: "No Auth", colorClass: "text-emerald-500" },
    { v: stats.apiKey, l: "API Key", colorClass: "text-amber-500" },
    { v: stats.oauth, l: "OAuth", colorClass: "text-rose-500" },
  ];

  return (
    <div className="mx-auto flex max-w-7xl gap-8 px-6 py-10 text-left">
      {/* Sidebar */}
      <aside className="hidden w-60 shrink-0 lg:block">
        <div className="sticky top-24">
          <button
            onClick={onBack}
            className="mb-4 flex items-center gap-2 text-muted-foreground hover:text-foreground text-xs font-semibold uppercase tracking-wider transition-colors"
          >
            <ArrowLeft size={14} /> All categories
          </button>
          <div className="rounded-2xl p-2.5 max-h-[70vh] overflow-y-auto border border-border bg-card shadow-sm">
            {categories.map((c) => {
              const active = c.slug === category.slug;
              return (
                <button
                  key={c.slug}
                  onClick={() => onSelectCategory(c)}
                  className={`flex w-full items-center justify-between gap-2 rounded-xl px-3 py-2 transition-all ${
                    active
                      ? "bg-primary/10 text-primary font-semibold border border-primary/20"
                      : "text-muted-foreground hover:text-foreground hover:bg-secondary border border-transparent"
                  }`}
                  style={{ fontSize: 13 }}
                >
                  <span className="flex items-center gap-2 truncate">
                    <span>{c.emoji}</span>
                    <span className="truncate">{c.name}</span>
                  </span>
                  <span className={`font-mono text-xs ${active ? "text-primary" : "text-muted-foreground/60"}`}>
                    {c.count}
                  </span>
                </button>
              );
            })}
          </div>
        </div>
      </aside>

      {/* Content */}
      <div className="min-w-0 flex-1">
        <button
          onClick={onBack}
          className="mb-4 flex items-center gap-2 lg:hidden text-muted-foreground hover:text-foreground text-xs font-semibold uppercase tracking-wider transition-colors"
        >
          <ArrowLeft size={14} /> Back
        </button>

        <div className="mb-8 flex items-center gap-4">
          <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-secondary border border-border text-3xl shadow-sm">
            {category.emoji}
          </div>
          <div>
            <h1 className="text-3xl font-extrabold tracking-tight text-foreground">
              {category.name}
            </h1>
            <p className="text-muted-foreground mt-2 text-sm max-w-[560px]">
              {categoryDescriptions[category.slug] ?? `${category.count} APIs in this category`}
            </p>
          </div>
        </div>

        {/* Category stats grid */}
        <div className="mb-8 grid grid-cols-2 gap-4 sm:grid-cols-4">
          {statCards.map((s) => (
            <div key={s.l} className="rounded-2xl p-5 border border-border bg-card shadow-sm">
              <div className={`text-3xl font-extrabold tracking-tight ${s.colorClass}`}>
                {s.v}
              </div>
              <div className="text-xs text-muted-foreground font-mono tracking-wider uppercase mt-2">
                {s.l}
              </div>
            </div>
          ))}
        </div>

        {/* Controls bar */}
        <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
          <div className="flex flex-wrap items-center gap-2">
            {(["all", "none", "apiKey", "oauth"] as const).map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`rounded-full px-3.5 py-1.5 border font-mono text-[11px] font-semibold transition-all ${
                  filter === f
                    ? "bg-primary text-primary-foreground border-primary shadow-sm"
                    : "bg-card text-muted-foreground border-border hover:bg-secondary hover:text-foreground"
                }`}
              >
                {f === "all" ? "All" : f === "none" ? "No Auth" : f === "apiKey" ? "API Key" : "OAuth"}
              </button>
            ))}
          </div>
          
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 rounded-xl px-3 py-1.5 border border-border bg-card text-foreground text-xs shadow-sm">
              <ArrowUpDown size={12} className="text-muted-foreground" />
              <select
                value={sort}
                onChange={(e) => setSort(e.target.value as typeof sort)}
                className="bg-transparent outline-none font-mono font-medium text-foreground cursor-pointer"
              >
                <option value="default" className="bg-card text-foreground">Default</option>
                <option value="featured" className="bg-card text-foreground">Featured</option>
                <option value="az" className="bg-card text-foreground">A → Z</option>
                <option value="za" className="bg-card text-foreground">Z → A</option>
              </select>
            </div>
            
            <div className="flex rounded-xl p-1 border border-border bg-card shadow-sm">
              <button
                onClick={() => setView("cards")}
                className={`flex h-7.5 w-7.5 items-center justify-center rounded-lg transition-colors ${
                  view === "cards" ? "bg-primary/10 text-primary" : "text-muted-foreground hover:bg-secondary hover:text-foreground"
                }`}
              >
                <LayoutGrid size={14} />
              </button>
              <button
                onClick={() => setView("list")}
                className={`flex h-7.5 w-7.5 items-center justify-center rounded-lg transition-colors ${
                  view === "list" ? "bg-primary/10 text-primary" : "text-muted-foreground hover:bg-secondary hover:text-foreground"
                }`}
              >
                <List size={14} />
              </button>
            </div>
          </div>
        </div>

        {items.length === 0 ? (
          <div className="rounded-2xl p-16 text-center border-2 border-dashed border-border text-muted-foreground bg-card/50">
            No APIs match this filter yet.
          </div>
        ) : view === "cards" ? (
          <div className="grid gap-4 sm:grid-cols-2">
            {items.map((api) => (
              <ApiCard key={api.name} api={api} />
            ))}
          </div>
        ) : (
          <div className="overflow-hidden rounded-2xl border border-border bg-card shadow-sm">
            {items.map((api, idx) => (
              <a
                key={api.name}
                href={api.link}
                target="_blank"
                rel="noopener noreferrer"
                className={`flex items-center gap-4 px-6 py-4 transition-colors hover:bg-secondary/40 ${
                  idx === 0 ? "" : "border-t border-border/60"
                }`}
              >
                <div className="min-w-0 flex-1">
                  <div className="font-bold text-foreground text-sm leading-snug">
                    {api.name}
                  </div>
                  <div className="text-muted-foreground text-xs mt-1 truncate">
                    {api.description}
                  </div>
                </div>
                <div className="flex shrink-0 items-center gap-1.5">
                  <AuthBadge type={api.auth} />
                  <HttpsBadge https={api.https} />
                </div>
              </a>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
