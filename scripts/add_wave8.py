# -*- coding: utf-8 -*-
"""Wave-8 (2026-10-17): additions verified live (HTTP 200/308 via Invoke-WebRequest; 403=accepted as protected-but-alive only where noted). None duplicate by URL or name."""
import re
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from add_wave2 import norm_url, APIS, ROW_RE

ADDITIONS = [
    ("government-civic", "OpenStates", "State legislation, legislators and committee data across US states.", "🔑 ApiKey", "https://openstates.org/"),
    ("jobs-career", "Greenhouse", "Official job board API for company openings and postings.", "No", "https://developers.greenhouse.io/"),
    ("development", "Pipedream", "Integration platform with 2,500+ APIs and event-driven workflows.", "🔑 ApiKey", "https://pipedream.com/docs/"),
    ("development", "LaunchDarkly", "Feature flag management, experimentation and toggles.", "🔑 ApiKey", "https://apidocs.launchdarkly.com/"),
    ("science", "DataCite", "DOI metadata API for research datasets and outputs.", "🔑 ApiKey", "https://support.datacite.org/docs/api"),
    ("text-analysis-nlp", "DBpedia", "Structured knowledge base and semantic search over Wikipedia data.", "No", "https://www.dbpedia.org/"),
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
