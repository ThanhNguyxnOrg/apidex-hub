import { useEffect, useState } from "react";
import { Routes, Route, useNavigate, useParams, useLocation } from "react-router";
import { Navbar } from "./components/Navbar";
import { Hero } from "./components/Hero";
import { CategoryGrid } from "./components/CategoryGrid";
import { FeaturedAPIs } from "./components/FeaturedAPIs";
import { CategoryDetail } from "./components/CategoryDetail";
import { SearchModal } from "./components/SearchModal";
import { Footer } from "./components/Footer";
import { FavoritesView } from "./components/FavoritesView";
import { ApiDetailDrawer } from "./components/ApiDetailDrawer";
import { ToastProvider } from "./components/Toast";
import { apis, categories, type Api, type Category } from "./components/data";
import { X, Command } from "lucide-react";

/* ── Route Components ── */
function HomePage({
  theme,
  openSearch,
  onOpenDetail,
}: {
  theme: "light" | "dark";
  openSearch: (filter?: "all" | "no-auth" | "https") => void;
  onOpenDetail: (api: Api) => void;
}) {
  const navigate = useNavigate();

  const handleSelectCategory = (c: Category) => {
    navigate(`/category/${c.slug}`);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <>
      <Hero theme={theme} onSearchClick={openSearch} />
      <CategoryGrid onSelect={handleSelectCategory} />
      <FeaturedAPIs onOpenDetail={onOpenDetail} />
    </>
  );
}

function CategoryPageRoute({ onOpenDetail }: { onOpenDetail: (api: Api) => void }) {
  const { slug } = useParams<{ slug: string }>();
  const navigate = useNavigate();

  const category = categories.find((c) => c.slug === slug);

  if (!category) {
    return (
      <div className="mx-auto max-w-7xl px-6 py-24 text-center">
        <h1 className="text-3xl font-extrabold text-foreground mb-4">Category Not Found</h1>
        <p className="text-muted-foreground mb-6">
          The requested category <span className="font-mono text-primary font-semibold">"{slug}"</span> does not exist or has no active APIs.
        </p>
        <button
          onClick={() => navigate("/")}
          className="px-5 py-2.5 rounded-xl bg-primary text-primary-foreground font-semibold text-sm hover:opacity-90 transition-opacity cursor-pointer"
        >
          Return to All Categories
        </button>
      </div>
    );
  }

  return (
    <CategoryDetail
      category={category}
      onBack={() => {
        navigate("/");
        window.scrollTo({ top: 0, behavior: "smooth" });
      }}
      onSelectCategory={(c) => {
        navigate(`/category/${c.slug}`);
        window.scrollTo({ top: 0, behavior: "smooth" });
      }}
      onOpenDetail={onOpenDetail}
    />
  );
}

function FavoritesPageRoute({ onOpenDetail }: { onOpenDetail: (api: Api) => void }) {
  const navigate = useNavigate();
  return (
    <FavoritesView
      onBack={() => {
        navigate("/");
        window.scrollTo({ top: 0, behavior: "smooth" });
      }}
      onOpenDetail={onOpenDetail}
    />
  );
}

/* ── Main App Root ── */
export default function App() {
  const navigate = useNavigate();
  const location = useLocation();

  const [searchOpen, setSearchOpen] = useState(false);
  const [searchFilter, setSearchFilter] = useState<"all" | "no-auth" | "https">("all");
  const [selectedApi, setSelectedApi] = useState<Api | null>(null);
  const [shortcutsOpen, setShortcutsOpen] = useState(false);
  const [scrollProgress, setScrollProgress] = useState(0);

  const [theme, setTheme] = useState<"light" | "dark">(() => {
    const saved = localStorage.getItem("theme");
    if (saved === "light" || saved === "dark") return saved;
    return window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
  });

  // Track theme changes on root html element
  useEffect(() => {
    const root = document.documentElement;
    if (theme === "dark") {
      root.classList.add("dark");
      root.classList.remove("light");
      root.style.colorScheme = "dark";
    } else {
      root.classList.add("light");
      root.classList.remove("dark");
      root.style.colorScheme = "light";
    }
    localStorage.setItem("theme", theme);
  }, [theme]);

  // System theme changes
  useEffect(() => {
    const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
    const handler = (e: MediaQueryListEvent) => {
      if (!localStorage.getItem("theme")) {
        setTheme(e.matches ? "dark" : "light");
      }
    };
    mediaQuery.addEventListener("change", handler);
    return () => mediaQuery.removeEventListener("change", handler);
  }, []);

  // Track scroll progress
  useEffect(() => {
    const handleScroll = () => {
      const totalScroll = document.documentElement.scrollHeight - window.innerHeight;
      if (totalScroll > 0) {
        setScrollProgress((window.scrollY / totalScroll) * 100);
      }
    };
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  // Scroll to top on route change
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [location.pathname]);

  const openSearch = (filter: "all" | "no-auth" | "https" = "all") => {
    setSearchFilter(filter);
    setSearchOpen(true);
  };

  const toggleTheme = () => {
    setTheme((t) => (t === "dark" ? "light" : "dark"));
  };

  const openRandom = () => {
    const api = apis[Math.floor(Math.random() * apis.length)];
    if (api) {
      setSelectedApi(api);
    }
  };

  // Keyboard shortcut listener
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      // Ignore if typing inside input/textarea
      const target = e.target as HTMLElement;
      if (target?.tagName === "INPUT" || target?.tagName === "TEXTAREA") return;

      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        openSearch("all");
      } else if (e.key === "?" && !e.metaKey && !e.ctrlKey) {
        e.preventDefault();
        setShortcutsOpen((prev) => !prev);
      } else if (e.key.toLowerCase() === "t" && !e.metaKey && !e.ctrlKey) {
        e.preventDefault();
        toggleTheme();
      } else if (e.key.toLowerCase() === "r" && !e.metaKey && !e.ctrlKey) {
        e.preventDefault();
        openRandom();
      } else if (e.key.toLowerCase() === "f" && !e.metaKey && !e.ctrlKey) {
        e.preventDefault();
        navigate("/favorites");
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [navigate]);

  return (
    <ToastProvider>
      <div
        className="min-h-screen bg-background text-foreground transition-colors duration-300 font-sans relative"
        style={{
          fontFamily: "'Plus Jakarta Sans', system-ui, sans-serif",
        }}
      >
      {/* Accessibility Skip Link */}
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2.5 focus:rounded-xl focus:bg-primary focus:text-primary-foreground focus:shadow-2xl focus:font-semibold focus:outline-none focus:ring-2 focus:ring-ring"
      >
        Skip to main content
      </a>

      {/* Top Scroll Progress Indicator */}
      <div
        aria-hidden
        className="fixed top-0 left-0 right-0 h-[2.5px] z-50 pointer-events-none"
        style={{
          background: `linear-gradient(90deg, #06b6d4, #4f46e5, #a855f7)`,
          width: `${scrollProgress}%`,
          transition: "width 0.1s ease-out",
        }}
      />

      <Navbar
        theme={theme}
        toggleTheme={toggleTheme}
        onSearchClick={() => openSearch("all")}
        onFavoritesClick={() => navigate("/favorites")}
        onRandomClick={openRandom}
        onHomeClick={() => navigate("/")}
      />

      <main id="main-content">
        <Routes>
          <Route
            path="/"
            element={
              <HomePage
                theme={theme}
                openSearch={openSearch}
                onOpenDetail={(api) => setSelectedApi(api)}
              />
            }
          />
          <Route
            path="/category/:slug"
            element={
              <CategoryPageRoute
                onOpenDetail={(api) => setSelectedApi(api)}
              />
            }
          />
          <Route
            path="/favorites"
            element={
              <FavoritesPageRoute
                onOpenDetail={(api) => setSelectedApi(api)}
              />
            }
          />
          <Route
            path="*"
            element={
              <div className="mx-auto max-w-7xl px-6 py-24 text-center">
                <h1 className="text-3xl font-extrabold text-foreground mb-4">404 — Page Not Found</h1>
                <p className="text-muted-foreground mb-6">
                  The page you're looking for does not exist.
                </p>
                <button
                  onClick={() => navigate("/")}
                  className="px-5 py-2.5 rounded-xl bg-primary text-primary-foreground font-semibold text-sm hover:opacity-90 transition-opacity cursor-pointer"
                >
                  Return to Home
                </button>
              </div>
            }
          />
        </Routes>
      </main>

      <Footer />

      {/* Modals & Overlays */}
      <SearchModal
        open={searchOpen}
        initialFilter={searchFilter}
        onClose={() => setSearchOpen(false)}
        onSelectCategory={(slug) => {
          navigate(`/category/${slug}`);
          window.scrollTo({ top: 0, behavior: "smooth" });
        }}
      />

      <ApiDetailDrawer
        api={selectedApi}
        onClose={() => setSelectedApi(null)}
        onSelectCategory={(slug) => {
          navigate(`/category/${slug}`);
          window.scrollTo({ top: 0, behavior: "smooth" });
        }}
      />

      {/* Keyboard Shortcuts Dialog */}
      {shortcutsOpen && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs"
          onClick={() => setShortcutsOpen(false)}
          role="dialog"
          aria-modal="true"
          aria-label="Keyboard Shortcuts"
        >
          <div
            className="w-full max-w-md rounded-2xl border border-border bg-card p-6 shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between pb-4 border-b border-border">
              <div className="flex items-center gap-2 text-foreground font-bold">
                <Command size={18} className="text-primary" />
                <span>Keyboard Shortcuts</span>
              </div>
              <button
                onClick={() => setShortcutsOpen(false)}
                aria-label="Close shortcuts modal"
                className="p-1 rounded-lg text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors"
              >
                <X size={16} />
              </button>
            </div>
            <div className="mt-4 space-y-3 font-mono text-xs">
              <div className="flex items-center justify-between py-1">
                <span className="text-muted-foreground font-sans">Global Search</span>
                <kbd className="px-2 py-1 rounded bg-muted border border-border text-foreground">⌘K / Ctrl+K</kbd>
              </div>
              <div className="flex items-center justify-between py-1">
                <span className="text-muted-foreground font-sans">Toggle Dark / Light Theme</span>
                <kbd className="px-2 py-1 rounded bg-muted border border-border text-foreground">T</kbd>
              </div>
              <div className="flex items-center justify-between py-1">
                <span className="text-muted-foreground font-sans">Explore Random API</span>
                <kbd className="px-2 py-1 rounded bg-muted border border-border text-foreground">R</kbd>
              </div>
              <div className="flex items-center justify-between py-1">
                <span className="text-muted-foreground font-sans">Open Bookmarked Favorites</span>
                <kbd className="px-2 py-1 rounded bg-muted border border-border text-foreground">F</kbd>
              </div>
              <div className="flex items-center justify-between py-1">
                <span className="text-muted-foreground font-sans">Show / Hide Shortcuts</span>
                <kbd className="px-2 py-1 rounded bg-muted border border-border text-foreground">?</kbd>
              </div>
              <div className="flex items-center justify-between py-1">
                <span className="text-muted-foreground font-sans">Close Modal / Drawer</span>
                <kbd className="px-2 py-1 rounded bg-muted border border-border text-foreground">ESC</kbd>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  </ToastProvider>
  );
}
