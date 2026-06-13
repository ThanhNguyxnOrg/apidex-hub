import { apis } from "./data";
import { ApiCard } from "./ApiCard";
import { Star } from "lucide-react";

export function FeaturedAPIs() {
  const featured = apis.filter((a) => a.featured);
  return (
    <section className="border-t border-border bg-background transition-colors duration-300">
      <div className="mx-auto max-w-7xl px-6 py-20">
        <div className="mb-10 text-left">
          <div className="mb-3 inline-flex items-center gap-1.5 rounded-full px-3 py-0.5 bg-amber-500/10 border border-amber-500/20 text-amber-600 dark:text-amber-400 font-mono text-[10.5px] uppercase tracking-wider font-semibold">
            <Star size={11} className="fill-current" />
            Featured
          </div>
          <h2 className="text-3xl font-extrabold tracking-tight text-foreground">
            Most Popular APIs
          </h2>
          <p className="text-muted-foreground mt-2 text-sm">
            Hand-picked APIs developers love and use every day.
          </p>
        </div>

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {featured.map((api) => (
            <ApiCard key={api.name} api={api} />
          ))}
        </div>
      </div>
    </section>
  );
}
