# -*- coding: utf-8 -*-
"""Wave-13 part 1 (2026-10-17): verified additions mined outside the public-apis
corpus (EBI, CORE, IMF, Wikimedia, PriceCharting). URLs verified live via
PowerShell Invoke-WebRequest: 200/308 OK; 403 = protected-but-alive (accepted).
Dedupe via catalog_utils.collect_index (exact name + norm_url)."""
import sys

sys.path.insert(0, "scripts")
from catalog_utils import APIS, ROW_TMPL, collect_index, insert_rows, norm_url

ADDITIONS = [
    ("science", "ChEMBL", "Drug discovery bioactivity database: compounds, targets, assays.", "No", "https://www.ebi.ac.uk/chembl/"),
    ("education", "CORE", "Open-access research paper aggregator: search and download API.", "🔑 ApiKey", "https://core.ac.uk/documentation/api/"),
    ("demographic-analysis", "IMF DataMapper", "Macroeconomic indicators (GDP, inflation, debt, trade).", "No", "https://www.imf.org/external/datamapper/api/"),
    ("education", "Wikimedia", "Wikimedia API portal: REST and Action APIs across wiki projects.", "No", "https://api.wikimedia.org/"),
    ("shopping", "PriceCharting", "Historical market prices for video games and trading cards.", "🔑 ApiKey", "https://www.pricecharting.com/docs/api"),
]


def main():
    names, urls = collect_index()
    per_file, added, skipped = {}, 0, 0
    for slug, name, desc, auth, url in ADDITIONS:
        if name.lower() in names or norm_url(url) in urls:
            skipped += 1
            print(f"  skip dup: {name}")
            continue
        names.add(name.lower())
        urls.add(norm_url(url))
        per_file.setdefault(APIS / f"{slug}.md", []).append(
            ROW_TMPL.format(name=name, desc=desc, auth=auth, url=url)
        )
        added += 1
    for fpath, rows in per_file.items():
        insert_rows(fpath, rows)
        print(f"  {fpath.stem}: +{len(rows)}")
    print(f"ADDED={added} SKIPPED={skipped}")


if __name__ == "__main__":
    main()
