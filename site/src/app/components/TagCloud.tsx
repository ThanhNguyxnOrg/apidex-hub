import { categories, type Category } from "./data";

export function TagCloud({ onSelect }: { onSelect: (c: Category) => void }) {
  return (
    <section className="mx-auto max-w-7xl px-6 pb-2 pt-12">
      <div className="mb-5 flex items-center gap-3">
        <div className="text-muted-foreground font-mono text-xs uppercase tracking-widest font-semibold">
          Quick jump
        </div>
        <div className="h-[1px] flex-1 bg-border" />
      </div>
      <div className="flex flex-wrap gap-2 justify-start">
        {categories.map((c) => (
          <button
            key={c.slug}
            onClick={() => onSelect(c)}
            className="group inline-flex items-center gap-2 rounded-full px-3.5 py-1.5 border border-border bg-card hover:border-primary/30 text-foreground hover:bg-secondary hover:text-foreground active:scale-95 transition-all duration-200"
            style={{ fontSize: 13 }}
          >
            <span>{c.emoji}</span>
            <span className="font-medium">{c.name}</span>
            <span className="font-mono text-[10.5px] font-semibold text-primary px-1.5 py-0.5 rounded-full bg-primary/10 border border-primary/20">
              {c.count}
            </span>
          </button>
        ))}
      </div>
    </section>
  );
}
