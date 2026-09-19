#!/usr/bin/env python3
"""
scripts/inventory.py
====================

One-shot inventory script for issue #37. Walks every effect,
checks metadata accuracy, identifies potential duplicates, and
validates catalog consistency. Not committed as a long-term tool;
kept because the reconciliation report references it.
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EFFECTS = REPO / "effects"
CATALOG = REPO / "index.html"
FEATURED = ["zoom-in", "shine-sweep", "glitch-shift"]


def load_all() -> list[dict]:
    out = []
    for d in sorted(EFFECTS.iterdir()):
        if not d.is_dir() or d.name.startswith("_"):
            continue
        meta_p = d / "meta.json"
        if not meta_p.exists():
            continue
        with meta_p.open() as f:
            meta = json.load(f)
        meta["_slug"] = d.name
        out.append(meta)
    return out


def main():
    metas = load_all()
    print(f"Total effects: {len(metas)}")

    # Category distribution
    cats = Counter(m["category"] for m in metas)
    print("\nCategory distribution:")
    for c in sorted(cats):
        present = "PRESENT" if cats[c] > 0 else "EMPTY"
        print(f"  {c:<14} {cats[c]:>3}  {present}")

    # Duplicate / variant analysis (heuristic: similar names or descriptions)
    print("\nPotential variants/duplicates (heuristic):")
    by_cat = defaultdict(list)
    for m in metas:
        by_cat[m["category"]].append(m["slug"])
    for cat, slugs in sorted(by_cat.items()):
        if len(slugs) <= 1:
            continue
        # Group by base name (strip -in/-out/-horizontal/-vertical etc.)
        variants = defaultdict(list)
        for s in slugs:
            base = s
            for suffix in ("-in-slowmo", "-horizontal", "-vertical", "-in", "-out", "-right", "-bottom", "-top", "-left", "-n-pan"):
                if base.endswith(suffix):
                    base = base[: -len(suffix)]
                    break
            variants[base].append(s)
        for base, members in sorted(variants.items()):
            if len(members) > 1:
                print(f"  [{cat}] {base}: {', '.join(sorted(members))}")

    # Featured slugs validity
    print("\nFeatured slugs:")
    by_slug = {m["_slug"]: m for m in metas}
    for f in FEATURED:
        if f in by_slug:
            m = by_slug[f]
            print(f"  {f:<20} OK ({m['category']}, {m['complexity']})")
        else:
            print(f"  {f:<20} MISSING")

    # Catalog consistency
    print("\nCatalog consistency:")
    if CATALOG.exists():
        catalog_text = CATALOG.read_text()
        catalog_count = catalog_text.count('class="card"') + catalog_text.count('card--featured')
        print(f"  Catalog cards (excluding template): {catalog_count}")
        print(f"  Tree effects: {len(metas)}")
        print(f"  Featured cards in catalog: {catalog_text.count('card--featured')}")
        # Check featured slugs appear in catalog
        for f in FEATURED:
            if f in catalog_text:
                print(f"  Featured '{f}' appears in catalog: YES")
            else:
                print(f"  Featured '{f}' appears in catalog: NO")
        # Check no retired slugs
        retired_in_catalog = []
        for m in metas:
            slug = m["_slug"]
            # Check if any known-retired patterns
            if any(p in slug for p in ["legacy", "old", "v1-"]):
                if slug in catalog_text:
                    retired_in_catalog.append(slug)
        if retired_in_catalog:
            print(f"  Retired patterns in catalog: {retired_in_catalog}")
        else:
            print(f"  No retired patterns in catalog: OK")
    else:
        print("  index.html not found (run scripts/build_catalog.py first)")

    # Slug uniqueness
    slugs = [m["_slug"] for m in metas]
    dupes = [s for s, n in Counter(slugs).items() if n > 1]
    print(f"\nDuplicate slugs: {dupes if dupes else 'none'}")

    # meta.id vs meta.slug vs directory name
    print("\nSlug consistency (id == slug == dir name):")
    for m in metas:
        if m.get("id") != m["_slug"] or m.get("slug") != m["_slug"]:
            print(f"  {m['_slug']}: id={m.get('id')!r} slug={m.get('slug')!r} MISMATCH")

    # Display name uniqueness
    titles = Counter(m["title"] for m in metas)
    title_dupes = [t for t, n in titles.items() if n > 1]
    print(f"\nDuplicate titles: {title_dupes if title_dupes else 'none'}")


if __name__ == "__main__":
    main()
