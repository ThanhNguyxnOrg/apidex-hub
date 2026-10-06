import { useState, useMemo } from "react";
import { categories, type Category } from "./data";
import { CategoryIcon } from "./categoryIcons";
import { Search, X, Layers } from "lucide-react";

function CategoryCard({
  c,
  idx,
  active,
  onSelect,
}: {
  c: Category;
  idx: number;
  active: boolean;
  onSelect: (c: Category) => void;
}) {
  const [coords, setCoords] = useState({ x: 0, y: 0, hover: false });

  const handleMouseMove = (e: React.MouseEvent<HTMLButtonElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width - 0.5;
    const y = (e.clientY - rect.top) / rect.height - 0.5;
    setCoords({ x, y, hover: true });
  };

  const handleMouseLeave = () => {
    setCoords({ x: 0, y: 0, hover: false });
  };

  return (
    <button
      onClick={() => onSelect(c)}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      className={`group relative rounded-2xl text-left transition-all duration-300 border bg-card text-foreground overflow-hidden focus-visible:ring-2 focus-visible:ring-primary outline-none cursor-pointer card-glow-hover ${
        active
          ? "border-primary shadow-md shadow-primary/10"
          : "border-border hover:border-primary/40"
      }`}
      style={{
        minHeight: 116,
        animation: `revealCard 0.35s cubic-bezier(0.16, 1, 0.3, 1) ${Math.min(idx * 15, 300)}ms backwards`,
        transform: coords.hover
          ? `perspective(800px) rotateX(${-coords.y * 10}deg) rotateY(${coords.x * 10}deg) scale(1.02)`
          : "perspective(800px) rotateX(0deg) rotateY(0deg) scale(1)",
        boxShadow: coords.hover
          ? "0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1)"
          : "none",
      }}
    >
      {/* Light Reflection glow */}
      {coords.hover && (
        <div
          className="pointer-events-none absolute inset-0 transition-opacity duration-300"
          style={{
            background: `radial-gradient(circle 90px at ${(coords.x + 0.5) * 100}% ${(coords.y + 0.5) * 100}%, var(--color-accent, rgba(6, 182, 212, 0.15)), transparent 80%)`,
          }}
        />
      )}

      {/* Highlight accent left border */}
      <div className="absolute left-0 top-4 bottom-4 w-[3px] rounded-r bg-primary opacity-0 transition-opacity duration-200 group-hover:opacity-100" />

      <div className="flex h-full flex-col justify-between p-5 relative z-10">
        <div className="flex items-center justify-between">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-secondary/80 border border-border text-primary group-hover:scale-110 group-hover:bg-primary/15 transition-all duration-300">
            <CategoryIcon slug={c.slug} className="w-5 h-5" />
          </div>
          <span className="text-muted-foreground font-mono text-[10.5px] tracking-tight bg-secondary/60 px-2 py-0.5 rounded-full border border-border">
            /{c.slug}
          </span>
        </div>
        <div className="mt-4">
          <div className="font-bold text-foreground text-[14px] leading-snug tracking-tight group-hover:text-primary transition-colors">
            {c.name}
          </div>
          <div className="text-primary font-mono text-[11px] font-semibold mt-1">
            {c.count} APIs
          </div>
        </div>
      </div>
    </button>
  );
}

export function CategoryGrid({
  onSelect,
  activeSlug,
}: {
  onSelect: (c: Category) => void;
  activeSlug?: string;
}) {
  const [filterQuery, setFilterQuery] = useState("");

  const filteredCategories = useMemo(() => {
    const q = filterQuery.trim().toLowerCase();
    if (!q) return categories;
    return categories.filter(
      (c) => c.name.toLowerCase().includes(q) || c.slug.toLowerCase().includes(q)
    );
  }, [filterQuery]);

  return (
    <section id="categories-section" className="relative mx-auto max-w-7xl px-6 py-12">
      {/* Header with Title and Instant Search */}
      <div className="relative mb-8 flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div className="text-left">
          <div className="flex items-center gap-2 mb-2 text-primary text-xs font-mono font-semibold uppercase tracking-wider">
            <Layers size={13} />
            <span>API Directory</span>
            <span>/</span>
            <span>Browse by Category</span>
          </div>
          <h2 className="text-3xl font-extrabold tracking-tight text-foreground">
            Explore Categories
          </h2>
          <p className="text-muted-foreground mt-2 text-sm max-w-2xl">
            {categories.length} curated categories spanning APIs, developer tools, and web scrapers.
          </p>
        </div>

        {/* Inline Category Filter Input */}
        <div className="flex items-center gap-3 w-full md:w-auto">
          <div className="relative flex-1 md:w-72">
            <Search size={14} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-muted-foreground" />
            <input
              type="text"
              value={filterQuery}
              onChange={(e) => setFilterQuery(e.target.value)}
              placeholder="Filter categories (e.g. AI, weather)..."
              className="w-full pl-9 pr-8 py-2 rounded-xl text-xs bg-muted/40 border border-border text-foreground placeholder:text-muted-foreground/60 outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all font-sans"
            />
            {filterQuery && (
              <button
                onClick={() => setFilterQuery("")}
                aria-label="Clear filter"
                className="absolute right-2.5 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground p-0.5"
              >
                <X size={12} />
              </button>
            )}
          </div>
          <div className="text-muted-foreground font-mono text-xs hidden sm:block bg-secondary/60 px-3 py-2 rounded-xl border border-border shrink-0">
            {filteredCategories.length}/{categories.length}
          </div>
        </div>
      </div>

      {filteredCategories.length === 0 ? (
        <div className="rounded-2xl p-16 text-center border-2 border-dashed border-border text-muted-foreground bg-card/40">
          <p className="text-sm">
            No categories match <span className="font-semibold text-foreground">"{filterQuery}"</span>
          </p>
          <button
            onClick={() => setFilterQuery("")}
            className="mt-3 text-xs text-primary hover:underline cursor-pointer font-medium"
          >
            Clear category filter
          </button>
        </div>
      ) : (
        <div className="relative grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5">
          {filteredCategories.map((c, idx) => (
            <CategoryCard
              key={c.slug}
              c={c}
              idx={idx}
              active={c.slug === activeSlug}
              onSelect={onSelect}
            />
          ))}
        </div>
      )}
    </section>
  );
}
