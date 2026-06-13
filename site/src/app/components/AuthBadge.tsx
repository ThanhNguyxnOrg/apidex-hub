import type { AuthType } from "./data";

const badgeConfig: Record<
  AuthType,
  { label: string; dotColor: string; bgClass: string; borderClass: string; textClass: string }
> = {
  none: {
    label: "No Auth",
    dotColor: "bg-emerald-500",
    bgClass: "bg-emerald-500/10 dark:bg-emerald-500/5",
    borderClass: "border-emerald-500/20 dark:border-emerald-500/10",
    textClass: "text-emerald-600 dark:text-emerald-400",
  },
  apiKey: {
    label: "API Key",
    dotColor: "bg-amber-500",
    bgClass: "bg-amber-500/10 dark:bg-amber-500/5",
    borderClass: "border-amber-500/20 dark:border-amber-500/10",
    textClass: "text-amber-600 dark:text-amber-400",
  },
  oauth: {
    label: "OAuth",
    dotColor: "bg-rose-500",
    bgClass: "bg-rose-500/10 dark:bg-rose-500/5",
    borderClass: "border-rose-500/20 dark:border-rose-500/10",
    textClass: "text-rose-600 dark:text-rose-400",
  },
};

export function AuthBadge({ type }: { type: AuthType }) {
  const config = badgeConfig[type];
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 border ${config.bgClass} ${config.borderClass} ${config.textClass} uppercase font-mono tracking-wider`}
      style={{
        fontSize: "10px",
        fontWeight: 600,
        lineHeight: 1.5,
      }}
    >
      <span className={`w-1.5 h-1.5 rounded-full ${config.dotColor}`} />
      {config.label}
    </span>
  );
}

export function HttpsBadge({ https }: { https: boolean }) {
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 border uppercase font-mono tracking-wider ${
        https
          ? "bg-sky-500/10 border-sky-500/20 text-sky-600 dark:bg-sky-500/5 dark:border-sky-500/10 dark:text-sky-400"
          : "bg-slate-500/10 border-slate-500/20 text-slate-600 dark:bg-slate-500/5 dark:border-slate-500/10 dark:text-slate-400"
      }`}
      style={{
        fontSize: "10px",
        fontWeight: 600,
        lineHeight: 1.5,
      }}
    >
      <span className={`w-1.5 h-1.5 rounded-full ${https ? "bg-sky-500" : "bg-slate-400"}`} />
      HTTPS
    </span>
  );
}
