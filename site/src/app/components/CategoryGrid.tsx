import { useState } from "react";
import { categories, type Category } from "./data";

function CategoryCard({
  c,
  active,
  onSelect,
}: {
  c: Category;
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
      className={`group relative rounded-2xl text-left transition-all duration-300 border bg-card text-foreground overflow-hidden ${
        active 
          ? "border-primary shadow-md shadow-primary/10" 
          : "border-border hover:border-primary/30"
      }`}
      style={{
        minHeight: 116,
        transform: coords.hover
          ? `perspective(800px) rotateX(${-coords.y * 12}deg) rotateY(${coords.x * 12}deg) scale(1.03)`
          : "perspective(800px) rotateX(0deg) rotateY(0deg) scale(1)",
        boxShadow: coords.hover ? "0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1)" : "none"
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
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-secondary/80 border border-border text-lg group-hover:scale-110 transition-transform duration-300">
            {c.emoji}
          </div>
          <span className="text-muted-foreground font-mono text-[10.5px] tracking-tight bg-secondary/60 px-2 py-0.5 rounded-full border border-border">
            /{c.slug}
          </span>
        </div>
        <div className="mt-4">
          <div className="font-bold text-foreground text-[14px] leading-snug tracking-tight">
            {c.name}
          </div>
          <div className="text-primary font-mono text-[10.5px] font-semibold mt-1">
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
  return (
    <section className="relative mx-auto max-w-7xl px-6 py-16">
      <div className="relative mb-8 flex items-end justify-between gap-6">
        <div className="text-left">
          <h2 className="text-3xl font-extrabold tracking-tight text-foreground">
            Browse by Category
          </h2>
          <p className="text-muted-foreground mt-2 text-sm">
            Explore {categories.length} curated categories spanning every developer need.
          </p>
        </div>
        <div className="text-muted-foreground font-mono text-xs hidden sm:block">
          {categories.length} Categories
        </div>
      </div>

      <div className="relative grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5">
        {categories.map((c) => (
          <CategoryCard
            key={c.slug}
            c={c}
            active={c.slug === activeSlug}
            onSelect={onSelect}
          />
        ))}
      </div>
    </section>
  );
}
