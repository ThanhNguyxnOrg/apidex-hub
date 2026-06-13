import { useEffect, useState } from "react";
import { Navbar } from "./components/Navbar";
import { Hero } from "./components/Hero";
import { CategoryGrid } from "./components/CategoryGrid";
import { FeaturedAPIs } from "./components/FeaturedAPIs";
import { CategoryDetail } from "./components/CategoryDetail";
import { SearchModal } from "./components/SearchModal";
import { Footer } from "./components/Footer";
import { TagCloud } from "./components/TagCloud";
import { FavoritesView } from "./components/FavoritesView";
import { apis, categories, type Category } from "./components/data";

type View = "home" | "category" | "favorites";

export default function App() {
  const [view, setView] = useState<View>("home");
  const [active, setActive] = useState<Category | null>(null);
  const [searchOpen, setSearchOpen] = useState(false);
  const [theme, setTheme] = useState<"light" | "dark">(() => {
    const saved = localStorage.getItem("theme");
    if (saved === "light" || saved === "dark") return saved;
    return window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
  });

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

  // Listen for system theme changes dynamically
  useEffect(() => {
    const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
    const handler = (e: MediaQueryListEvent) => {
      // Only change if user hasn't explicitly set a preference
      if (!localStorage.getItem("theme")) {
        setTheme(e.matches ? "dark" : "light");
      }
    };
    mediaQuery.addEventListener("change", handler);
    return () => mediaQuery.removeEventListener("change", handler);
  }, []);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setSearchOpen(true);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  const toggleTheme = () => {
    setTheme((t) => (t === "dark" ? "light" : "dark"));
  };

  const goCategory = (c: Category) => {
    setActive(c);
    setView("category");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const goHome = () => {
    setView("home");
    setActive(null);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const goFavorites = () => {
    setView("favorites");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const openRandom = () => {
    const api = apis[Math.floor(Math.random() * apis.length)];
    if (api?.link) window.open(api.link, "_blank", "noopener,noreferrer");
  };

  const selectBySlug = (slug: string) => {
    const c = categories.find((c) => c.slug === slug);
    if (c) goCategory(c);
  };

  return (
    <div
      className="min-h-screen bg-background text-foreground transition-colors duration-300 font-sans"
      style={{
        fontFamily: "'Plus Jakarta Sans', system-ui, sans-serif",
      }}
    >
      <style>{`
        @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
        @keyframes fadeInUp {
          from { opacity: 0; transform: translateY(12px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .api-card { transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
        .api-card:hover {
          transform: translateY(-4px) scale(1.01);
        }
        ::selection { background: rgba(6, 182, 212, 0.25); color: #fff; }
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb {
          background: rgba(120, 120, 120, 0.15);
          border-radius: 999px;
        }
        ::-webkit-scrollbar-thumb:hover { background: rgba(120, 120, 120, 0.3); }
        @keyframes pulse {
          0%, 100% { opacity: 1; transform: scale(1); }
          50% { opacity: 0.6; transform: scale(0.85); }
        }
      `}</style>

      <Navbar
        theme={theme}
        toggleTheme={toggleTheme}
        onSearchClick={() => setSearchOpen(true)}
        onFavoritesClick={goFavorites}
        onRandomClick={openRandom}
        onHomeClick={goHome}
      />

      {view === "category" && active && (
        <CategoryDetail
          category={active}
          onBack={goHome}
          onSelectCategory={goCategory}
        />
      )}

      {view === "favorites" && <FavoritesView onBack={goHome} />}

      {view === "home" && (
        <>
          <Hero theme={theme} onSearchClick={() => setSearchOpen(true)} />
          <TagCloud onSelect={goCategory} />
          <CategoryGrid onSelect={goCategory} />
          <FeaturedAPIs />
        </>
      )}

      <Footer />

      <SearchModal
        open={searchOpen}
        onClose={() => setSearchOpen(false)}
        onSelectCategory={selectBySlug}
      />
    </div>
  );
}

