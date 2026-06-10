import { categories, type Category } from "./data";

export function CategoryGrid({
  onSelect,
  activeSlug,
}: {
  onSelect: (c: Category) => void;
  activeSlug?: string;
}) {
  return (
    <section className="relative mx-auto max-w-7xl px-6 py-20">
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0"
        style={{
          backgroundImage:
            "radial-gradient(rgba(255,255,255,0.04) 1px, transparent 1px)",
          backgroundSize: "28px 28px",
          maskImage:
            "radial-gradient(ellipse at top, black 20%, transparent 70%)",
          WebkitMaskImage:
            "radial-gradient(ellipse at top, black 20%, transparent 70%)",
        }}
      />
      <div className="relative mb-10 flex items-end justify-between gap-6">
        <div>
          <h2
            style={{
              fontSize: 36,
              lineHeight: 1.15,
              letterSpacing: "-0.025em",
              fontWeight: 700,
            }}
          >
            <span
              style={{
                background: "linear-gradient(180deg, #ffffff 0%, #cbd5e1 100%)",
                WebkitBackgroundClip: "text",
                backgroundClip: "text",
                WebkitTextFillColor: "transparent",
              }}
            >
              Browse by{" "}
            </span>
            <span
              style={{
                background: "linear-gradient(135deg, #06b6d4, #8b5cf6)",
                WebkitBackgroundClip: "text",
                backgroundClip: "text",
                WebkitTextFillColor: "transparent",
              }}
            >
              Category
            </span>
          </h2>
          <p style={{ color: "#8b949e", marginTop: 10, fontSize: 15 }}>
            {categories.length} curated categories spanning every developer need.
          </p>
        </div>
        <div
          style={{
            color: "#8b949e",
            fontFamily: "JetBrains Mono, monospace",
            fontSize: 12,
          }}
        >
          {categories.length} Total
        </div>
      </div>

      <div className="relative grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5">
        {categories.map((c) => {
          const active = c.slug === activeSlug;
          return (
            <button
              key={c.slug}
              onClick={() => onSelect(c)}
              className="category-tile group relative rounded-2xl p-[1px] text-left"
              style={{
                background: active
                  ? "linear-gradient(135deg, rgba(6,182,212,0.6), rgba(139,92,246,0.5))"
                  : "linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.04))",
                minHeight: 128,
              }}
            >
              <div
                className="tile-inner relative flex h-full flex-col overflow-hidden rounded-[15px] p-5"
                style={{
                  background:
                    "linear-gradient(135deg, rgba(139,92,246,0.05), rgba(59,130,246,0.03)), #0d1117",
                  minHeight: 126,
                }}
              >
                <div
                  aria-hidden
                  className="tile-glow pointer-events-none absolute -inset-px opacity-0 transition-opacity duration-200"
                  style={{
                    background:
                      "radial-gradient(circle at 30% 0%, rgba(6,182,212,0.35), transparent 60%)",
                  }}
                />
                <div className="relative flex h-full flex-col">
                  <div style={{ fontSize: 28 }}>{c.emoji}</div>
                  <div
                    style={{
                      color: "#e6edf3",
                      fontSize: 14.5,
                      fontWeight: 500,
                      marginTop: 12,
                      lineHeight: 1.3,
                    }}
                  >
                    {c.name}
                  </div>
                  <div
                    className="mt-auto pt-3"
                    style={{
                      color: "#06b6d4",
                      fontFamily: "JetBrains Mono, monospace",
                      fontSize: 12,
                      fontWeight: 500,
                    }}
                  >
                    {c.count} APIs
                  </div>
                </div>
              </div>
            </button>
          );
        })}
      </div>
    </section>
  );
}
