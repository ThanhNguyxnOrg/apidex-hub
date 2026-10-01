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
          aria-label="APIDex Hub Home"
          className="flex items-center gap-2.5 hover:opacity-90 transition-opacity cursor-pointer focus-visible:ring-2 focus-visible:ring-primary outline-none rounded-lg"
        >
          {/* Borderless transparent logo */}
          <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg" className="h-8 w-8">
            <defs>
              <linearGradient id="navLogo" x1="0" y1="0" x2="64" y2="64" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stopColor="#06b6d4" />
                <stop offset="50%" stopColor="#4f46e5" />
                <stop offset="100%" stopColor="#a855f7" />
              </linearGradient>
            </defs>
            <polygon points="32,8 52,19.5 52,44.5 32,56 12,44.5 12,19.5" stroke="url(#navLogo)" strokeWidth="3.5" strokeLinejoin="round" strokeLinecap="round" />
            <path d="M32,8 V32 L12,44.5 M32,32 L52,44.5" stroke="url(#navLogo)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
            <circle cx="32" cy="8" r="4" fill={theme === "dark" ? "#06080f" : "#ffffff"} stroke="url(#navLogo)" strokeWidth="2.5" />
            <circle cx="12" cy="44.5" r="4" fill={theme === "dark" ? "#06080f" : "#ffffff"} stroke="url(#navLogo)" strokeWidth="2.5" />
            <circle cx="52" cy="44.5" r="4" fill={theme === "dark" ? "#06080f" : "#ffffff"} stroke="url(#navLogo)" strokeWidth="2.5" />
            <circle cx="32" cy="32" r="5.5" fill="url(#navLogo)" />
          </svg>
          <span className="font-bold text-foreground tracking-tight text-base font-sans">
            APIDex Hub
          </span>
        </button>

        <button
          onClick={onSearchClick}
          aria-label="Search APIs by name, category, or keyword (Press Command+K)"
          className="hidden md:flex items-center gap-3 rounded-xl px-4 py-2 border border-border bg-muted/40 hover:bg-muted/70 text-muted-foreground transition-all duration-200 cursor-pointer focus-visible:ring-2 focus-visible:ring-primary outline-none"
          style={{ minWidth: 320, fontSize: 13.5 }}
        >
          <Search size={15} className="text-primary" />
          <span className="flex-1 text-left">Search {stats.total.toLocaleString()} APIs...</span>
          <kbd className="rounded px-1.5 py-0.5 bg-muted border border-border font-mono text-[10.5px] text-muted-foreground">
            ⌘K
          </kbd>
        </button>

        <div className="flex items-center gap-2">
          <button
            onClick={onRandomClick}
            aria-label="Open a random API"
            title="Random API"
            className="flex h-9 items-center gap-1.5 rounded-lg px-3 border border-border bg-card text-foreground hover:bg-secondary transition-colors duration-200 cursor-pointer focus-visible:ring-2 focus-visible:ring-primary outline-none"
            style={{ fontSize: 13 }}
          >
            <Shuffle size={14} />
            <span className="hidden sm:inline">Random</span>
          </button>

          <button
            onClick={onFavoritesClick}
            aria-label={`View your ${favs.size} favorite APIs`}
            title="Favorites"
            className="relative flex h-9 items-center gap-1.5 rounded-lg px-3 border border-border bg-card text-foreground hover:bg-secondary transition-colors duration-200 cursor-pointer focus-visible:ring-2 focus-visible:ring-primary outline-none"
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
            aria-label={theme === "dark" ? "Switch to Light Mode" : "Switch to Dark Mode"}
            title={theme === "dark" ? "Switch to Light Mode" : "Switch to Dark Mode"}
            className="flex h-9 w-9 items-center justify-center rounded-lg border border-border bg-card text-foreground hover:bg-secondary transition-colors duration-200 cursor-pointer focus-visible:ring-2 focus-visible:ring-primary outline-none"
          >
            {theme === "dark" ? (
              <Sun size={15} />
            ) : (
              <Moon size={15} />
            )}
          </button>

          <a
            href="https://github.com/ThanhNguyxnOrg/apidex-hub/issues/new?template=add_api.yml"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Submit a new API via GitHub issue"
            title="Submit a New API"
            className="flex h-9 items-center gap-1.5 rounded-lg px-3 text-primary bg-primary/10 border border-primary/20 hover:bg-primary hover:text-primary-foreground hover:border-primary transition-all duration-200 focus-visible:ring-2 focus-visible:ring-primary outline-none"
            style={{ fontSize: 13, fontWeight: 500 }}
          >
            <Plus size={14} />
            <span className="hidden sm:inline">Submit API</span>
          </a>

          <a
            href="https://github.com/ThanhNguyxnOrg/apidex-hub"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="View APIDex Hub GitHub Repository"
            title="GitHub Repository"
            className="flex h-9 w-9 items-center justify-center rounded-lg border border-border bg-card text-foreground hover:bg-secondary transition-colors duration-200 focus-visible:ring-2 focus-visible:ring-primary outline-none"
          >
            <Github size={16} />
          </a>
        </div>
      </div>
    </nav>
  );
}
