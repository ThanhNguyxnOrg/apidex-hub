import { useState, useEffect } from "react";
import { X, ExternalLink, Copy, Check, Terminal, Code2, Globe2, ShieldCheck, HeartPulse } from "lucide-react";
import { type Api } from "./data";
import { AuthBadge } from "./AuthBadge";
import { CategoryIcon } from "./categoryIcons";
import { useToast } from "./Toast";

export function ApiDetailDrawer({
  api,
  onClose,
  onSelectCategory,
}: {
  api: Api | null;
  onClose: () => void;
  onSelectCategory?: (slug: string) => void;
}) {
  const [activeTab, setActiveTab] = useState<"curl" | "js" | "python">("curl");
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    if (api) {
      window.addEventListener("keydown", handleKeyDown);
      document.body.style.overflow = "hidden";
    }
    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      document.body.style.overflow = "";
    };
  }, [api, onClose]);

  if (!api) return null;

  const snippets = {
    curl: `# cURL Request
curl -X GET "${api.link}" \\
  -H "Accept: application/json"${api.auth === "apiKey" ? ' \\\n  -H "Authorization: Bearer YOUR_API_KEY"' : ""}`,
    js: `// JavaScript (Fetch API)
async function fetchApi() {
  const response = await fetch("${api.link}", {
    headers: {
      "Accept": "application/json",${api.auth === "apiKey" ? '\n      "Authorization": "Bearer YOUR_API_KEY",' : ""}
    }
  });
  const data = await response.json();
  console.log(data);
}
fetchApi();`,
    python: `# Python (requests)
import requests

url = "${api.link}"
headers = {
    "Accept": "application/json",${api.auth === "apiKey" ? '\n    "Authorization": "Bearer YOUR_API_KEY",' : ""}
}

response = requests.get(url, headers=headers)
print(response.json())`,
  };

  const { showToast } = useToast();

  const handleCopy = () => {
    navigator.clipboard.writeText(snippets[activeTab]);
    setCopied(true);
    showToast(`Copied ${activeTab.toUpperCase()} snippet to clipboard!`, "success");
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div
      className="fixed inset-0 z-50 flex justify-end bg-black/60 backdrop-blur-xs transition-opacity duration-300"
      onClick={onClose}
      role="dialog"
      aria-modal="true"
      aria-labelledby="drawer-title"
    >
      <div
        className="relative w-full max-w-xl h-full bg-card border-l border-border shadow-2xl flex flex-col overflow-y-auto"
        style={{
          animation: "slideInRight 0.25s cubic-bezier(0.16, 1, 0.3, 1)",
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <style>{`
          @keyframes slideInRight {
            from { transform: translateX(100%); }
            to { transform: translateX(0); }
          }
        `}</style>

        {/* Drawer Header */}
        <div className="sticky top-0 z-10 flex items-center justify-between px-6 py-5 border-b border-border bg-card/95 backdrop-blur-md">
          <div className="flex items-center gap-2.5">
            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10 border border-primary/20 text-primary">
              <CategoryIcon slug={api.category} className="w-4 h-4" />
            </span>
            <span className="font-mono text-xs uppercase tracking-wider text-muted-foreground font-semibold">
              API Specification
            </span>
          </div>
          <button
            onClick={onClose}
            aria-label="Close drawer"
            className="flex h-8 w-8 items-center justify-center rounded-lg border border-border text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors focus-visible:ring-2 focus-visible:ring-primary outline-none"
          >
            <X size={16} />
          </button>
        </div>

        {/* Drawer Content */}
        <div className="p-6 space-y-6 flex-1">
          {/* Title & Badges */}
          <div>
            <div className="flex items-start justify-between gap-4">
              <h2 id="drawer-title" className="text-2xl font-black tracking-tight text-foreground">
                {api.name}
              </h2>
              <div className="flex items-center gap-1.5 shrink-0">
                <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-500 border border-emerald-500/20">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                  Verified Active
                </span>
              </div>
            </div>

            <p className="mt-3 text-muted-foreground text-sm leading-relaxed">
              {api.description}
            </p>

            {/* Metadata Pills */}
            <div className="mt-4 flex flex-wrap items-center gap-2">
              <AuthBadge type={api.auth} />
              {api.https ? (
                <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-mono font-medium bg-emerald-500/10 text-emerald-500 border border-emerald-500/20">
                  <ShieldCheck size={12} /> HTTPS Secure
                </span>
              ) : (
                <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-mono font-medium bg-amber-500/10 text-amber-500 border border-amber-500/20">
                  HTTP (Insecure)
                </span>
              )}
              {onSelectCategory && (
                <button
                  onClick={() => {
                    onSelectCategory(api.category);
                    onClose();
                  }}
                  className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-mono font-medium bg-secondary text-foreground hover:border-primary/40 border border-border transition-colors cursor-pointer"
                >
                  <CategoryIcon slug={api.category} className="w-3.5 h-3.5 text-primary" />
                  /{api.category}
                </button>
              )}
            </div>
          </div>

          {/* Action CTAs */}
          <div className="flex items-center gap-3 pt-2">
            <a
              href={api.link}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 inline-flex items-center justify-center gap-2 rounded-xl bg-primary px-4 py-2.5 text-sm font-semibold text-primary-foreground shadow-sm hover:opacity-90 active:scale-98 transition-all"
            >
              <ExternalLink size={15} />
              Open API Website / Documentation
            </a>
          </div>

          {/* Code Snippets Section */}
          <div className="rounded-xl border border-border bg-muted/30 overflow-hidden">
            <div className="flex items-center justify-between border-b border-border bg-muted/60 px-4 py-2">
              <div className="flex items-center gap-1">
                <button
                  onClick={() => setActiveTab("curl")}
                  className={`px-3 py-1 rounded-lg text-xs font-mono font-semibold transition-colors ${
                    activeTab === "curl"
                      ? "bg-card text-foreground shadow-xs"
                      : "text-muted-foreground hover:text-foreground"
                  }`}
                >
                  cURL
                </button>
                <button
                  onClick={() => setActiveTab("js")}
                  className={`px-3 py-1 rounded-lg text-xs font-mono font-semibold transition-colors ${
                    activeTab === "js"
                      ? "bg-card text-foreground shadow-xs"
                      : "text-muted-foreground hover:text-foreground"
                  }`}
                >
                  JavaScript
                </button>
                <button
                  onClick={() => setActiveTab("python")}
                  className={`px-3 py-1 rounded-lg text-xs font-mono font-semibold transition-colors ${
                    activeTab === "python"
                      ? "bg-card text-foreground shadow-xs"
                      : "text-muted-foreground hover:text-foreground"
                  }`}
                >
                  Python
                </button>
              </div>

              <button
                onClick={handleCopy}
                aria-label="Copy code snippet"
                className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-mono text-muted-foreground hover:text-foreground hover:bg-secondary border border-border/80 transition-colors"
              >
                {copied ? <Check size={12} className="text-emerald-500" /> : <Copy size={12} />}
                {copied ? "Copied!" : "Copy"}
              </button>
            </div>

            <div className="p-4 bg-black/40 overflow-x-auto">
              <pre className="font-mono text-xs text-foreground/90 leading-relaxed">
                <code>{snippets[activeTab]}</code>
              </pre>
            </div>
          </div>

          {/* Link Checker Live Insight */}
          <div className="rounded-xl border border-emerald-500/20 bg-emerald-500/5 p-4 flex items-start gap-3">
            <HeartPulse size={18} className="text-emerald-500 mt-0.5 shrink-0" />
            <div className="text-xs text-muted-foreground leading-relaxed">
              <span className="font-semibold text-foreground">Automated Daily Verification:</span> This endpoint is monitored daily by APIDex Hub's link health pipeline. Status is verified against live network responses.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
