import { ArrowLeft, Heart } from "lucide-react";
import { apis } from "./data";
import { ApiCard } from "./ApiCard";
import { useFavorites } from "./favorites";

export function FavoritesView({ onBack }: { onBack: () => void }) {
  const favs = useFavorites();
  const items = apis.filter((a) => favs.has(a.name));

  return (
    <div className="mx-auto max-w-7xl px-6 py-12 text-left">
      <button
        onClick={onBack}
        className="mb-6 flex items-center gap-2 text-muted-foreground hover:text-foreground text-xs font-semibold uppercase tracking-wider transition-colors"
      >
        <ArrowLeft size={14} /> Home
      </button>

      <div className="mb-8 flex items-center gap-4">
        <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-red-500/10 border border-red-500/20 shadow-sm">
          <Heart size={24} className="text-red-500 fill-current" />
        </div>
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-foreground">
            Your Favorites
          </h1>
          <p className="text-muted-foreground mt-2 text-sm">
            {items.length === 0
              ? "Heart any API to save it here. Stored in your browser only."
              : `${items.length} API${items.length === 1 ? "" : "s"} saved locally.`}
          </p>
        </div>
      </div>

      {items.length === 0 ? (
        <div className="rounded-2xl p-16 text-center border-2 border-dashed border-border text-muted-foreground bg-card/50">
          <Heart size={40} className="mx-auto mb-4 text-muted-foreground/40" />
          <div className="text-sm">
            No favorites yet. Click the heart on any API to save it.
          </div>
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {items.map((api) => (
            <ApiCard key={api.name} api={api} />
          ))}
        </div>
      )}
    </div>
  );
}
