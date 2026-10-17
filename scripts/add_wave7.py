# -*- coding: utf-8 -*-
"""Wave-7 (2026-10-17): additions verified live (HTTP 200/308 via Invoke-WebRequest). None duplicate by URL or name."""
import re
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from add_wave2 import norm_url, APIS, ROW_RE

ADDITIONS = [
    ("monitoring-observability", "Healthchecks.io", "Health monitoring with pings, cron checks and down-alerting.", "🔑 ApiKey", "https://healthchecks.io/docs/api/"),
    ("monitoring-observability", "Cronitor", "Cron job and data pipeline monitoring with instant alerts.", "🔑 ApiKey", "https://cronitor.io/docs"),
    ("education", "WaniKani", "Japanese kanji, radicals and spaced-repetition learning data.", "🔑 ApiKey", "https://docs.api.wanikani.com/"),
    ("education", "KanjiAPI", "Open Japanese kanji and kana character reference.", "No", "https://kanjiapi.dev/"),
    ("utilities-tools", "cron-job.org", "Free scheduled HTTP jobs with uptime checks and notifications.", "🔑 ApiKey", "https://cron-job.org/en/"),
    ("phone-telephony", "SimpleTexting", "SMS campaigns, contacts and two-way messaging.", "🔑 ApiKey", "https://simpletexting.com/api/"),
    ("business", "Toast", "Restaurant POS platform: menus, orders, guests and payments.", "🔑 ApiKey", "https://dev.toasttab.com/"),
    ("weather", "Foreca", "Global weather forecasts, current conditions and comparisons.", "🔑 ApiKey", "https://developer.foreca.com/"),
]

ROW_TMPL = "| **{name}** | {desc} | {auth} | ✅ | [Link]({url}) |"


def insert_rows(fpath, rows):
    lines = fpath.read_text(encoding="utf-8").splitlines()
    idx = [i for i, l in enumerate(lines) if l.startswith("| **")]
    first, last = idx[0], idx[-1]
    new = sorted(lines[first:last + 1] + rows, key=lambda l: ROW_RE.match(l).group(1).lower())
    fpath.write_text("\n".join(lines[:first] + new + lines[last + 1:]) + "\n", encoding="utf-8")
    return len(new)


def main():
    names, urls = set(), set()
    for f in APIS.glob("*.md"):
        for line in f.read_text(encoding="utf-8").splitlines():
            m = ROW_RE.match(line)
            if m:
                names.add(m.group(1).strip().lower())
                for u in re.findall(r"\((https?://[^)]+)\)", line):
                    urls.add(norm_url(u))

    per_file, added, skipped = {}, 0, 0
    for slug, name, desc, auth, url in ADDITIONS:
        if name.lower() in names or norm_url(url) in urls:
            skipped += 1
            print(f"  skip dup: {name}")
            continue
        names.add(name.lower()); urls.add(norm_url(url))
        per_file.setdefault(APIS / f"{slug}.md", []).append(ROW_TMPL.format(name=name, desc=desc, auth=auth, url=url))
        added += 1

    for fpath, rows in per_file.items():
        insert_rows(fpath, rows)
        print(f"  {fpath.stem}: +{len(rows)}")
    print(f"ADDED={added} SKIPPED={skipped}")


if __name__ == "__main__":
    main()
