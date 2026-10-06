import { useMemo, useState } from "react";
import { ArrowLeft, ArrowUpDown, LayoutGrid, List } from "lucide-react";
import { apis, categories, type Api, type Category } from "./data";
import { ApiCard } from "./ApiCard";
import { AuthBadge, HttpsBadge } from "./AuthBadge";
import { categoryDescriptions } from "./categoryDescriptions";
import { CategoryIcon } from "./categoryIcons";

export function CategoryDetail({
  category,
  onBack,
  onSelectCategory,
  onOpenDetail,
}: {
  category: Category;
  onBack: () => void;
  onSelectCategory: (c: Category) => void;
  onOpenDetail?: (api: Api) => void;
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
      <aside className="hidden w-64 shrink-0 lg:block">
        <div className="sticky top-24">
          <button
            onClick={onBack}
            className="mb-4 flex items-center gap-2 text-muted-foreground hover:text-foreground text-xs font-semibold uppercase tracking-wider transition-colors cursor-pointer"
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
                  className={`flex w-full items-center justify-between gap-2.5 rounded-xl px-3 py-2 transition-all cursor-pointer ${
                    active
                      ? "bg-primary/10 text-primary font-semibold border border-primary/20"
                      : "text-muted-foreground hover:text-foreground hover:bg-secondary border border-transparent"
                  }`}
                  style={{ fontSize: 13 }}
                >
                  <span className="flex items-center gap-2.5 truncate">
                    <CategoryIcon slug={c.slug} className={`w-4 h-4 shrink-0 ${active ? "text-primary" : "text-muted-foreground"}`} />
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
          className="mb-4 flex items-center gap-2 lg:hidden text-muted-foreground hover:text-foreground text-xs font-semibold uppercase tracking-wider transition-colors cursor-pointer"
        >
          <ArrowLeft size={14} /> Back
        </button>

        <div className="mb-8 flex items-center gap-4">
          <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-secondary border border-border text-primary shadow-sm">
            <CategoryIcon slug={category.slug} className="w-7 h-7" />
          </div>
          <div>
            <h1 className="text-3xl font-extrabold tracking-tight text-foreground">
              {category.name}
            </h1>
            <p className="text-muted-foreground mt-2 text-sm max-w-[560px]">
              {categoryDescriptions[category.slug] ?? `${category.count} APIs curated in this sector.`}
            </p>
          </div>
        </div>

        {/* Stats Row */}
        <div className="mb-8 grid grid-cols-2 gap-3 sm:grid-cols-4">
          {statCards.map((sc) => (
            <div
              key={sc.l}
              className="rounded-2xl border border-border bg-card p-4 transition-all"
            >
              <div className={`text-2xl font-black tracking-tight ${sc.colorClass}`}>
                {sc.v}
              </div>
              <div className="text-muted-foreground font-mono text-[11px] uppercase tracking-wider font-semibold mt-1">
                {sc.l}
              </div>
            </div>
          ))}
        </div>

        {/* Filter and View Toolbar */}
        <div className="mb-6 flex flex-wrap items-center justify-between gap-4 border-b border-border pb-4">
          <div className="flex flex-wrap items-center gap-1.5">
            {(
              [
                { id: "all", label: "All" },
                { id: "none", label: "No Auth" },
                { id: "apiKey", label: "API Key" },
                { id: "oauth", label: "OAuth" },
              ] as const
            ).map((f) => (
              <button
                key={f.id}
                onClick={() => setFilter(f.id)}
                className={`rounded-full px-3 py-1 font-mono text-xs font-semibold transition-all cursor-pointer ${
                  filter === f.id
                    ? "bg-primary text-primary-foreground shadow-xs"
                    : "border border-border bg-card text-muted-foreground hover:bg-secondary hover:text-foreground"
                }`}
              >
                {f.label}
              </button>
            ))}
          </div>

          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              <ArrowUpDown size={14} className="text-muted-foreground" />
              <select
                value={sort}
                onChange={(e) => setSort(e.target.value as any)}
                className="rounded-lg border border-border bg-card px-2.5 py-1 text-xs text-foreground outline-none cursor-pointer"
              >
                <option value="default">Default order</option>
                <option value="featured">Featured first</option>
                <option value="az">A → Z</option>
                <option value="za">Z → A</option>
              </select>
            </div>

            <div className="flex rounded-lg border border-border bg-card p-0.5">
              <button
                onClick={() => setView("cards")}
                aria-label="Cards view"
                className={`rounded-md p-1.5 transition-colors cursor-pointer ${
                  view === "cards" ? "bg-primary/10 text-primary" : "text-muted-foreground hover:bg-secondary hover:text-foreground"
                }`}
              >
                <LayoutGrid size={14} />
              </button>
              <button
                onClick={() => setView("list")}
                aria-label="List view"
                className={`rounded-md p-1.5 transition-colors cursor-pointer ${
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
              <ApiCard key={api.name} api={api} onOpenDetail={onOpenDetail} />
            ))}
          </div>
        ) : (
          <div className="overflow-hidden rounded-2xl border border-border bg-card shadow-sm">
            {items.map((api, idx) => (
              <div
                key={api.name}
                onClick={() => {
                  if (onOpenDetail) onOpenDetail(api);
                  else window.open(api.link, "_blank", "noopener,noreferrer");
                }}
                className={`flex items-center gap-4 px-6 py-4 transition-colors hover:bg-secondary/40 cursor-pointer ${
                  idx === 0 ? "" : "border-t border-border/60"
                }`}
              >
                <div className="min-w-0 flex-1">
                  <div className="font-bold text-foreground text-sm leading-snug hover:text-primary transition-colors">
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
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
