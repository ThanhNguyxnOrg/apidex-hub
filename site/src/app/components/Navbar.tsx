import { Github, Heart, Search, Shuffle, Plus, Sun, Moon } from "lucide-react";
import { stats } from "./data";
import { useFavorites } from "./favorites";

export function Navbar({
  theme,
  toggleTheme,
  onSearchClick,
  onFavoritesClick,
  onRandomClick,
  onHomeClick,
}: {
  theme: "light" | "dark";
  toggleTheme: () => void;
  onSearchClick: () => void;
  onFavoritesClick: () => void;
  onRandomClick: () => void;
  onHomeClick: () => void;
}) {
  const favs = useFavorites();
  return (
    <nav className="sticky top-0 z-40 backdrop-blur-xl bg-background/80 border-b border-border transition-colors duration-300">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-6 py-4">
        <button
          onClick={onHomeClick}
          className="flex items-center gap-2 hover:opacity-90 transition-opacity"
        >
          <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 shadow-sm" style={{ borderRadius: 8 }}>
            <defs>
              <linearGradient id="navLogo" x1="0" y1="0" x2="64" y2="64" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stopColor="#06b6d4"/>
                <stop offset="50%" stopColor="#4f46e5"/>
                <stop offset="100%" stopColor="#a855f7"/>
              </linearGradient>
            </defs>
            <rect width="64" height="64" rx="14" fill={theme === "dark" ? "#0d1117" : "#f1f5f9"}/>
            <polygon points="32,10 51,21 51,43 32,54 13,43 13,21" stroke="url(#navLogo)" strokeWidth="3" strokeLinejoin="round" strokeLinecap="round"/>
            <path d="M32,10 V32 L13,43 M32,32 L51,43" stroke="url(#navLogo)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
            <circle cx="32" cy="10" r="4" fill={theme === "dark" ? "#0d1117" : "#f1f5f9"} stroke="url(#navLogo)" strokeWidth="2"/>
            <circle cx="13" cy="43" r="4" fill={theme === "dark" ? "#0d1117" : "#f1f5f9"} stroke="url(#navLogo)" strokeWidth="2"/>
            <circle cx="51" cy="43" r="4" fill={theme === "dark" ? "#0d1117" : "#f1f5f9"} stroke="url(#navLogo)" strokeWidth="2"/>
            <circle cx="32" cy="32" r="5" fill="url(#navLogo)"/>
          </svg>
          <span className="font-semibold text-foreground tracking-tight text-base">
            Awesome APIs
          </span>
        </button>

        <button
          onClick={onSearchClick}
          className="hidden md:flex items-center gap-3 rounded-xl px-4 py-2 border border-border bg-muted/40 hover:bg-muted/70 text-muted-foreground transition-all duration-200"
          style={{ minWidth: 320, fontSize: 13.5 }}
        >
          <Search size={15} />
          <span className="flex-1 text-left">Search {stats.total}+ APIs...</span>
          <kbd className="rounded px-1.5 py-0.5 bg-muted border border-border font-mono text-[10.5px] text-muted-foreground">
            ⌘K
          </kbd>
        </button>

        <div className="flex items-center gap-2">
          <button
            onClick={onRandomClick}
            title="Random API"
            className="flex h-9 items-center gap-1.5 rounded-lg px-3 border border-border bg-card text-foreground hover:bg-secondary transition-colors duration-200"
            style={{ fontSize: 13 }}
          >
            <Shuffle size={14} />
            <span className="hidden sm:inline">Random</span>
          </button>
          <button
            onClick={onFavoritesClick}
            title="Favorites"
            className="relative flex h-9 items-center gap-1.5 rounded-lg px-3 border border-border bg-card text-foreground hover:bg-secondary transition-colors duration-200"
            style={{ fontSize: 13 }}
          >
            <Heart size={14} fill={favs.size > 0 ? "#ef4444" : "none"} color={favs.size > 0 ? "#ef4444" : undefined} />
            <span className="hidden sm:inline">Favorites</span>
            {favs.size > 0 && (
              <span className="font-mono text-[11px] text-red-500 bg-red-500/10 px-1.5 py-0.5 rounded-full border border-red-500/20">
                {favs.size}
              </span>
            )}
          </button>
          
          <button
            onClick={toggleTheme}
            title={theme === "dark" ? "Switch to Light Mode" : "Switch to Dark Mode"}
            className="flex h-9 w-9 items-center justify-center rounded-lg border border-border bg-card text-foreground hover:bg-secondary transition-colors duration-200"
          >
            {theme === "dark" ? (
              <Sun size={15} className="animate-spin-slow" />
            ) : (
              <Moon size={15} />
            )}
          </button>

          <a
            href="https://github.com/ThanhNguyxnOrg/awesome-free-apis/issues/new?template=add_api.yml"
            target="_blank"
            rel="noopener noreferrer"
            title="Submit a New API"
            className="flex h-9 items-center gap-1.5 rounded-lg px-3 text-primary bg-primary/10 border border-primary/20 hover:bg-primary hover:text-primary-foreground hover:border-primary transition-all duration-200"
            style={{ fontSize: 13, fontWeight: 500 }}
          >
            <Plus size={14} />
            <span className="hidden sm:inline">Submit API</span>
          </a>
          <a
            href="https://github.com/ThanhNguyxnOrg/awesome-free-apis"
            target="_blank"
            rel="noopener noreferrer"
            className="flex h-9 w-9 items-center justify-center rounded-lg border border-border bg-card text-foreground hover:bg-secondary transition-colors duration-200"
          >
            <Github size={16} />
          </a>
        </div>
      </div>
    </nav>
  );
}

