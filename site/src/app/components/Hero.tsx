import { useEffect, useRef, useState } from "react";
import { Search, Play, Code, Check } from "lucide-react";
import { stats } from "./data";

const statItems = [
  { value: stats.total, suffix: "+", label: "Free APIs" },
  { value: stats.categories, suffix: "", label: "Categories" },
  { value: stats.noAuth, suffix: "", label: "No Auth Required" },
  { value: stats.httpsPercent, suffix: "%", label: "HTTPS Enabled" },
];

function useCountUp(target: number, active: boolean, duration = 1400) {
  const [val, setVal] = useState(0);
  useEffect(() => {
    if (!active) return;
    const start = performance.now();
    let raf = 0;
    const tick = (t: number) => {
      const p = Math.min(1, (t - start) / duration);
      const eased = 1 - Math.pow(1 - p, 3);
      setVal(Math.round(target * eased));
      if (p < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [target, active, duration]);
  return val;
}

function StatCard({
  item,
  active,
  index,
}: {
  item: (typeof statItems)[number];
  active: boolean;
  index: number;
}) {
  const v = useCountUp(item.value, active);
  return (
    <div
      className="relative overflow-hidden rounded-2xl p-6 transition-all duration-300 border border-border bg-card/40 backdrop-blur-md shadow-sm hover:shadow-md hover:border-primary/20"
      style={{
        animation: `fadeInUp 0.6s ${index * 0.1}s both`,
      }}
    >
      <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-primary/60 to-transparent" />
      <div className="text-3xl font-extrabold tracking-tight text-foreground">
        {v.toLocaleString()}
        {item.suffix}
      </div>
      <div className="text-xs text-muted-foreground font-mono tracking-wider uppercase mt-2">
        {item.label}
      </div>
    </div>
  );
}

// 3D Particle Constellation System
function ConstellationCanvas({ theme }: { theme: "light" | "dark" }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animationFrameId: number;
    let width = canvas.width = canvas.offsetWidth;
    let height = canvas.height = canvas.offsetHeight;

    // Node tags representing API categories
    const tags = [
      "Weather API", "AI & ML", "Crypto & Web3", "IP Geolocation", 
      "Sports Tracker", "Movies & TV", "Gaming Matrix", "Dictionary", 
      "Public Finance", "Social Dev", "Open Auth", "Data Science"
    ];

    interface Particle {
      x: number;
      y: number;
      vx: number;
      vy: number;
      radius: number;
      label: string;
      color: string;
    }

    const particles: Particle[] = tags.map((tag, i) => {
      const isCyan = i % 2 === 0;
      return {
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.4,
        vy: (Math.random() - 0.5) * 0.4,
        radius: Math.random() * 3 + 2,
        label: tag,
        color: isCyan ? "#06b6d4" : "#a855f7"
      };
    });

    const mouse = { x: -1000, y: -1000, active: false };

    const handleResize = () => {
      if (!canvas) return;
      width = canvas.width = canvas.offsetWidth;
      height = canvas.height = canvas.offsetHeight;
    };

    const handleMouseMove = (e: MouseEvent) => {
      const rect = canvas.getBoundingClientRect();
      mouse.x = e.clientX - rect.left;
      mouse.y = e.clientY - rect.top;
      mouse.active = true;
    };

    const handleMouseLeave = () => {
      mouse.x = -1000;
      mouse.y = -1000;
      mouse.active = false;
    };

    window.addEventListener("resize", handleResize);
    const parent = canvas.parentElement;
    if (parent) {
      parent.addEventListener("mousemove", handleMouseMove);
      parent.addEventListener("mouseleave", handleMouseLeave);
    }

    const draw = () => {
      ctx.clearRect(0, 0, width, height);

      // Determine colors based on theme
      const lineColor = theme === "dark" ? "rgba(6, 182, 212, 0.15)" : "rgba(79, 70, 229, 0.12)";
      const labelColor = theme === "dark" ? "#9ca3af" : "#4b5563";
      const primaryDot = theme === "dark" ? "#06b6d4" : "#4f46e5";
      const secondaryDot = theme === "dark" ? "#a855f7" : "#818cf8";

      // Draw connections
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < 180) {
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.strokeStyle = lineColor;
            ctx.lineWidth = 1 - dist / 180;
            ctx.stroke();
          }
        }
      }

      // Draw and update particles
      particles.forEach((p, idx) => {
        // Apply slight attraction to cursor
        if (mouse.active) {
          const dx = mouse.x - p.x;
          const dy = mouse.y - p.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 250) {
            const force = (250 - dist) / 3000;
            p.vx += dx * force * 0.1;
            p.vy += dy * force * 0.1;

            // Cap speed
            const speed = Math.sqrt(p.vx * p.vx + p.vy * p.vy);
            if (speed > 1.2) {
              p.vx = (p.vx / speed) * 1.2;
              p.vy = (p.vy / speed) * 1.2;
            }
          }
        }

        // Float drift updating
        p.x += p.vx;
        p.y += p.vy;

        // Bounce borders
        if (p.x < 0 || p.x > width) p.vx *= -1;
        if (p.y < 0 || p.y > height) p.vy *= -1;

        // Draw particle dot
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = idx % 2 === 0 ? primaryDot : secondaryDot;
        ctx.shadowBlur = theme === "dark" ? 8 : 0;
        ctx.shadowColor = idx % 2 === 0 ? primaryDot : secondaryDot;
        ctx.fill();
        ctx.shadowBlur = 0; // Reset shadow

        // Draw text label next to dot
        ctx.fillStyle = labelColor;
        ctx.font = "500 10.5px 'JetBrains Mono', monospace";
        ctx.fillText(p.label, p.x + 8, p.y + 4);
      });

      animationFrameId = requestAnimationFrame(draw);
    };

    draw();

    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener("resize", handleResize);
      if (parent) {
        parent.removeEventListener("mousemove", handleMouseMove);
        parent.removeEventListener("mouseleave", handleMouseLeave);
      }
    };
  }, [theme]);

  return (
    <div className="absolute inset-0 z-0 pointer-events-none opacity-60 md:opacity-100">
      <canvas ref={canvasRef} className="w-full h-full" />
    </div>
  );
}

// Sandbox interactive code mock responses
const SANDBOX_DATA = {
  cats: {
    endpoint: "https://api.freeapis.org/v1/cats",
    code: `const url = "https://api.freeapis.org/v1/cats";\nconst res = await fetch(url);\nconst data = await res.json();\nconsole.log(data);`,
    response: `{
  "status": 200,
  "data": {
    "fact": "Cats can jump up to six times their height.",
    "length": 43,
    "breed_reference": "https://api.freeapis.org/v1/breeds/9"
  },
  "info": {
    "cached": false,
    "latency_ms": 42
  }
}`
  },
  weather: {
    endpoint: "https://api.freeapis.org/v1/weather?city=tokyo",
    code: `const url = "https://api.freeapis.org/v1/weather?city=tokyo";\nconst res = await fetch(url);\nconst data = await res.json();\nconsole.log(data);`,
    response: `{
  "status": 200,
  "data": {
    "city": "Tokyo",
    "temperature": "22°C",
    "condition": "Partly Cloudy",
    "humidity": "58%",
    "wind_kph": 12.5
  },
  "info": {
    "cached": true,
    "latency_ms": 15
  }
}`
  },
  ip: {
    endpoint: "https://api.freeapis.org/v1/ip-check",
    code: `const url = "https://api.freeapis.org/v1/ip-check";\nconst res = await fetch(url);\nconst data = await res.json();\nconsole.log(data);`,
    response: `{
  "status": 200,
  "data": {
    "ip": "103.82.126.90",
    "country": "Vietnam",
    "country_code": "VN",
    "timezone": "Asia/Ho_Chi_Minh",
    "isp": "FPT Telecom"
  },
  "info": {
    "cached": false,
    "latency_ms": 68
  }
}`
  }
};

type SandboxTab = "cats" | "weather" | "ip";

function ApiPlayground({ theme }: { theme: "light" | "dark" }) {
  const [activeTab, setActiveTab] = useState<SandboxTab>("cats");
  const [viewState, setViewState] = useState<"request" | "response">("request");
  const [loading, setLoading] = useState(false);

  const triggerRun = () => {
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setViewState("response");
    }, 600);
  };

  const current = SANDBOX_DATA[activeTab];

  return (
    <div className="relative w-full rounded-2xl border border-border bg-card text-left font-mono shadow-xl overflow-hidden transition-all duration-300">
      {/* Header bar */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-border bg-muted/40">
        <div className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-full bg-red-500/70" />
          <span className="w-2.5 h-2.5 rounded-full bg-yellow-500/70" />
          <span className="w-2.5 h-2.5 rounded-full bg-green-500/70" />
          <span className="text-[11px] text-muted-foreground ml-2 font-sans font-medium">playground.js</span>
        </div>
        
        {/* Sandbox tabs */}
        <div className="flex gap-1.5">
          {(["cats", "weather", "ip"] as SandboxTab[]).map((tab) => (
            <button
              key={tab}
              onClick={() => {
                setActiveTab(tab);
                setViewState("request");
              }}
              className={`px-2.5 py-0.5 text-[10.5px] rounded-md font-sans transition-colors ${
                activeTab === tab
                  ? "bg-primary text-primary-foreground font-semibold"
                  : "text-muted-foreground hover:text-foreground hover:bg-secondary/80"
              }`}
            >
              /{tab}
            </button>
          ))}
        </div>
      </div>

      {/* Editor/Response display */}
      <div className="p-5 text-[13px] leading-relaxed min-h-[190px] flex flex-col justify-between select-text">
        <div>
          {viewState === "request" ? (
            <div className="whitespace-pre text-foreground">
              <span className="text-purple-500 dark:text-purple-400">const</span> url = <span className="text-green-600 dark:text-green-400">"{current.endpoint}"</span>;<br />
              <span className="text-purple-500 dark:text-purple-400">const</span> res = <span className="text-purple-500 dark:text-purple-400">await</span> <span className="text-blue-600 dark:text-blue-400">fetch</span>(url);<br />
              <span className="text-purple-500 dark:text-purple-400">const</span> data = <span className="text-purple-500 dark:text-purple-400">await</span> res.<span className="text-blue-600 dark:text-blue-400">json</span>();<br />
              <span className="text-blue-600 dark:text-blue-400">console</span>.<span className="text-blue-600 dark:text-blue-400">log</span>(data);
            </div>
          ) : (
            <pre className="text-muted-foreground text-[11px] leading-normal whitespace-pre font-mono max-h-[170px] overflow-y-auto">
              {current.response}
            </pre>
          )}
        </div>

        {/* Footer controls inside console */}
        <div className="mt-5 flex items-center justify-between border-t border-border pt-4">
          <div className="flex gap-2 bg-muted/60 p-0.5 rounded-lg border border-border">
            <button
              onClick={() => setViewState("request")}
              className={`px-2.5 py-1 text-[10.5px] rounded-md font-sans transition-all ${
                viewState === "request"
                  ? "bg-card text-foreground font-medium shadow-sm"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              Request
            </button>
            <button
              onClick={() => setViewState("response")}
              className={`px-2.5 py-1 text-[10.5px] rounded-md font-sans transition-all ${
                viewState === "response"
                  ? "bg-card text-foreground font-medium shadow-sm"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              Response
            </button>
          </div>

          <button
            onClick={triggerRun}
            disabled={loading}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg bg-primary text-primary-foreground hover:opacity-90 active:scale-[0.97] transition-all disabled:opacity-60 cursor-pointer"
          >
            {loading ? (
              <span className="w-2.5 h-2.5 border-2 border-primary-foreground border-t-transparent rounded-full animate-spin" />
            ) : viewState === "response" ? (
              <Check size={11} />
            ) : (
              <Play size={11} fill="currentColor" />
            )}
            {loading ? "Calling..." : viewState === "response" ? "Success" : "Test Query"}
          </button>
        </div>
      </div>
    </div>
  );
}

export function Hero({
  theme,
  onSearchClick,
}: {
  theme: "light" | "dark";
  onSearchClick: () => void;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (!ref.current) return;
    const obs = new IntersectionObserver(
      (entries) => entries.forEach((e) => e.isIntersecting && setVisible(true)),
      { threshold: 0.1 }
    );
    obs.observe(ref.current);
    return () => obs.disconnect();
  }, []);

  return (
    <section
      ref={ref}
      className="relative overflow-hidden border-b border-border bg-background transition-colors duration-300"
    >
      {/* 3D Particle Constellation background canvas */}
      <ConstellationCanvas theme={theme} />

      {/* Radial lighting spots */}
      <div
        aria-hidden
        className="pointer-events-none absolute top-[-10%] left-1/2 -translate-x-1/2 h-[350px] w-[500px] rounded-full opacity-60 dark:opacity-100"
        style={{
          background: "radial-gradient(circle, rgba(79, 70, 229, 0.15) 0%, transparent 70%)",
          filter: "blur(60px)",
        }}
      />
      <div
        aria-hidden
        className="pointer-events-none absolute bottom-0 right-[10%] h-[300px] w-[300px] rounded-full opacity-20 dark:opacity-40"
        style={{
          background: "radial-gradient(circle, rgba(6, 182, 212, 0.15) 0%, transparent 70%)",
          filter: "blur(50px)",
        }}
      />

      <div className="relative mx-auto max-w-7xl px-6 pb-20 pt-24 z-10">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          {/* Left Column: Headline copy */}
          <div className="lg:col-span-7 text-left">
            <div
              className="mb-6 inline-flex items-center gap-2 rounded-full bg-accent/40 border border-accent px-3 py-1 text-[11px]"
              style={{
                color: "var(--primary)",
                fontFamily: "JetBrains Mono, monospace",
              }}
            >
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
              Auto-synced from README.md
            </div>

            <h1
              style={{
                fontSize: "clamp(38px, 5.5vw, 64px)",
                lineHeight: 1.08,
                letterSpacing: "-0.03em",
                fontWeight: 800,
              }}
              className="mb-6 text-foreground"
            >
              Discover, Test, and <br />
              <span className="bg-gradient-to-r from-cyan-500 via-indigo-500 to-purple-500 bg-clip-text text-transparent">
                Integrate Free APIs
              </span>
            </h1>

            <p className="mb-8 font-sans text-muted-foreground text-lg leading-relaxed max-w-[560px]">
              A clean, structured developer hub featuring over <span className="text-foreground font-semibold">{stats.total}+ free public APIs</span>. 
              Totally free, HTTPS-enabled, CORS-vetted, and continuously tested.
            </p>

            {/* Interactive Search Bar Trigger */}
            <div className="max-w-[480px]">
              <button
                onClick={onSearchClick}
                className="group flex w-full items-center gap-3.5 rounded-2xl px-5 border border-border bg-card hover:border-primary/40 hover:shadow-lg transition-all duration-300"
                style={{ height: 56 }}
              >
                <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-primary/10 border border-primary/20 text-primary group-hover:scale-105 transition-transform duration-200">
                  <Search size={15} />
                </div>
                <span className="text-[14px] flex-1 text-left text-muted-foreground">
                  Search {stats.total}+ free APIs...
                </span>
                <div className="flex items-center gap-1 text-[10px] font-mono text-muted-foreground opacity-60">
                  <kbd className="rounded bg-muted border border-border px-1.5 py-0.5">⌘</kbd>
                  <kbd className="rounded bg-muted border border-border px-1.5 py-0.5">K</kbd>
                </div>
              </button>
            </div>
          </div>

          {/* Right Column: Code Playground Widget */}
          <div className="lg:col-span-5 relative">
            <ApiPlayground theme={theme} />
          </div>
        </div>

        {/* Stats Grid */}
        <div className="mt-20 grid grid-cols-2 gap-4 md:grid-cols-4 border-t border-border pt-12">
          {statItems.map((s, i) => (
            <StatCard key={s.label} item={s} active={visible} index={i} />
          ))}
        </div>
      </div>
    </section>
  );
}
