# -*- coding: utf-8 -*-
"""Wave-12 (2026-10-17): thin-category additions, verified live via HTTP (200/308/401-protected/418-alive).
Deduped: skips present, dead dropped (bgpview ERR both methods, lyft ERR, kaggle 404-variant)."""
import re
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from add_wave2 import norm_url, APIS, ROW_RE

ADDITIONS = [
    ("reviews", "Trustpilot", "Official APIs for business units, reviews and consumer profiles.", "🔑 ApiKey", "https://developers.trustpilot.com/"),
    ("networking-dns", "PeeringDB", "Global network/IXP peering data Exchange API.", "No", "https://peeringdb.com/apidocs/"),
    ("fitness-wellness", "Polar Accesslink", "Polar device activity, sleep and training data.", "🔐 OAuth", "https://www.polaraccesslink.com/v3-docs/"),
    ("fitness-wellness", "Google Fit", "Fitness session, steps and health-data store REST APIs.", "🔐 OAuth", "https://developers.google.com/fit/rest/"),
    ("museums-art", "DigitalNZ", "30M+ digitized items from New Zealand galleries and archives.", "🔑 ApiKey", "https://api.digitalnz.org/"),
    ("finance", "FinancialModelingPrep", "Company fundamentals, ratios and historical stock data.", "🔑 ApiKey", "https://financialmodelingprep.com/api/"),
    ("finance", "SimFin", "Standardized company fundamentals and financial statements.", "🔑 ApiKey", "https://www.simfin.com/"),
    ("security-validation", "StopForumSpam", "Spam registry of IP/email/username from forum spam.", "No", "https://www.stopforumspam.com/"),
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
