import { useState } from "react";
import { ArrowUpRight, Check, Copy, Heart } from "lucide-react";
import type { Api } from "./data";
import { AuthBadge, HttpsBadge } from "./AuthBadge";
import { toggleFavorite, useFavorites } from "./favorites";
import { useToast } from "./Toast";

export function ApiCard({
  api,
  onOpenDetail,
}: {
  api: Api;
  onOpenDetail?: (api: Api) => void;
}) {
  const favs = useFavorites();
  const isFav = favs.has(api.name);
  const [copied, setCopied] = useState(false);
  const [coords, setCoords] = useState({ x: 0, y: 0, hover: false });
  const { showToast } = useToast();

  const onCopy = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    navigator.clipboard?.writeText(api.link);
    setCopied(true);
    showToast(`Copied ${api.name} endpoint URL`, "success");
    setTimeout(() => setCopied(false), 1400);
  };

  const onFav = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    toggleFavorite(api.name);
    if (!isFav) {
      showToast(`Added ${api.name} to Favorites`, "heart");
    } else {
      showToast(`Removed ${api.name} from Favorites`, "info");
    }
  };

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width - 0.5;
    const y = (e.clientY - rect.top) / rect.height - 0.5;
    setCoords({ x, y, hover: true });
  };

  const handleMouseLeave = () => {
    setCoords({ x: 0, y: 0, hover: false });
  };

  const handleCardClick = () => {
    if (onOpenDetail) {
      onOpenDetail(api);
    } else {
      window.open(api.link, "_blank", "noopener,noreferrer");
    }
  };

  return (
    <div
      onClick={handleCardClick}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          handleCardClick();
        }
      }}
      className="group relative block overflow-hidden rounded-2xl p-6 border border-border bg-card text-foreground transition-all duration-300 cursor-pointer text-left focus-visible:ring-2 focus-visible:ring-primary outline-none card-glow-hover"
      style={{
        transform: coords.hover
          ? `perspective(800px) rotateX(${-coords.y * 10}deg) rotateY(${coords.x * 10}deg) scale(1.02)`
          : "perspective(800px) rotateX(0deg) rotateY(0deg) scale(1)",
        boxShadow: coords.hover
          ? "0 12px 30px -10px rgba(0, 0, 0, 0.15), 0 8px 16px -8px rgba(0, 0, 0, 0.15)"
          : "none",
      }}
    >
      {/* Light Reflection glow */}
      {coords.hover && (
        <div
          className="pointer-events-none absolute inset-0 transition-opacity duration-300"
          style={{
            background: `radial-gradient(circle 120px at ${(coords.x + 0.5) * 100}% ${(coords.y + 0.5) * 100}%, var(--color-accent, rgba(6, 182, 212, 0.15)), transparent 80%)`,
          }}
        />
      )}

      <div className="flex items-start justify-between gap-3 mb-3 relative z-10">
        <div className="flex items-center gap-2 min-w-0">
          <span
            className="w-2 h-2 rounded-full bg-emerald-500 shrink-0"
            title="Verified Active: Link checked by daily pipeline"
          />
          <h3 className="text-[17px] font-bold text-foreground leading-snug tracking-tight truncate group-hover:text-primary transition-colors">
            {api.name}
          </h3>
        </div>
        <div className="flex shrink-0 items-center gap-1">
          <button
            onClick={onCopy}
            aria-label={`Copy link for ${api.name}`}
            title="Copy link"
            className="flex h-7 w-7 items-center justify-center rounded-lg border border-transparent hover:border-border hover:bg-secondary text-muted-foreground hover:text-foreground transition-all duration-200"
            style={{ color: copied ? "#10b981" : undefined }}
          >
            {copied ? <Check size={13} /> : <Copy size={13} />}
          </button>
          <button
            onClick={onFav}
            aria-label={isFav ? `Remove ${api.name} from favorites` : `Add ${api.name} to favorites`}
            title={isFav ? "Remove favorite" : "Add favorite"}
            className="flex h-7 w-7 items-center justify-center rounded-lg border border-transparent hover:border-border hover:bg-secondary text-muted-foreground hover:text-foreground transition-all duration-200"
            style={{ color: isFav ? "#ef4444" : undefined }}
          >
            <Heart size={13} fill={isFav ? "#ef4444" : "none"} />
          </button>
          <a
            href={api.link}
            target="_blank"
            rel="noopener noreferrer"
            onClick={(e) => e.stopPropagation()}
            aria-label={`Open ${api.name} website directly`}
            title="Open website in new tab"
            className="flex h-7 w-7 items-center justify-center rounded-lg border border-transparent hover:border-border hover:bg-secondary text-muted-foreground hover:text-foreground transition-all duration-200"
          >
            <ArrowUpRight
              size={15}
              className="transition-transform group-hover:translate-x-0.5 group-hover:-translate-y-0.5"
            />
          </a>
        </div>
      </div>

      <p className="text-muted-foreground text-[13.5px] leading-relaxed mb-5 relative z-10 min-h-[40px] line-clamp-2">
        {api.description}
      </p>

      <div className="flex flex-wrap items-center gap-1.5 relative z-10">
        <AuthBadge type={api.auth} />
        <HttpsBadge https={api.https} />
      </div>
    </div>
  );
}
