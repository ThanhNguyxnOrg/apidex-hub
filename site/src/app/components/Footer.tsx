import { Github } from "lucide-react";
import { stats } from "./data";
import apiData from "../../data/apis.json";

export function Footer() {
  return (
    <footer className="border-t border-border bg-card transition-colors duration-300">
      <div className="mx-auto max-w-7xl px-6 py-12">
        <div className="flex flex-col items-start justify-between gap-6 md:flex-row md:items-center">
          <div className="text-left">
            <div className="text-foreground font-bold tracking-tight text-base">
              Awesome Free APIs
            </div>
            <p className="text-muted-foreground text-sm mt-2 max-w-[480px]">
              Auto-generated from README.md via GitHub Actions. Edit the README,
              push to main — the site rebuilds itself.
            </p>
          </div>
          <div className="flex items-center gap-3">
            <a
              href="https://github.com/ThanhNguyxnOrg/awesome-free-apis"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 rounded-lg px-4 py-2 border border-border bg-card text-foreground hover:bg-secondary transition-colors duration-200"
              style={{ fontSize: 13 }}
            >
              <Github size={14} /> Star on GitHub
            </a>
          </div>
        </div>
        <div className="mt-10 flex flex-wrap items-center justify-between gap-3 border-t border-border/60 pt-6 font-mono text-[11px] text-muted-foreground">
          <span>MIT License · {stats.total} APIs · Built with React + Tailwind</span>
          <span>Last synced: {apiData.meta.generated_at?.slice(0, 10) ?? new Date().toISOString().slice(0, 10)}</span>
        </div>
      </div>
    </footer>
  );
}
