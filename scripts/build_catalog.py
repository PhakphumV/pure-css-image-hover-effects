#!/usr/bin/env python3
"""
scripts/build_catalog.py
========================

Generates the root index.html catalog from every effects/<slug>/meta.json.

Design read (design-taste-frontend): developer-tooling showcase for CSS
hover effects, editorial, calm. Dials: VARIANCE 5 / MOTION 3 / DENSITY 3.

Page structure:
- Hero (left-aligned, no version eyebrow)
- Featured row (3 standout effects, larger cards)
- Sticky CSS-only category filter (no JS - contract section 1)
- All effects grouped by category, each card with a category badge

Pure Python stdlib. Re-running produces byte-identical output (deterministic
per the rebuild plan, issue #8).

Usage:
    python3 scripts/build_catalog.py
"""
import json
from collections import OrderedDict
from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EFFECTS = REPO / "effects"
OUT = REPO / "index.html"

CATEGORIES = [
    "zoom", "pan", "rotate", "3d", "filter", "reveal", "fade",
    "shadow", "light", "border", "distortion", "overlay", "composite",
]

# Three visually distinctive effects that represent different categories
# and serve as the "featured" row at the top of the catalog.
FEATURED_SLUGS = ["zoom-in", "shine-sweep", "glitch-shift"]


def load_meta() -> list[dict]:
    out = []
    for d in sorted(EFFECTS.iterdir()):
        if not d.is_dir() or d.name.startswith("_"):
            continue
        meta_path = d / "meta.json"
        if not meta_path.exists():
            continue
        with meta_path.open() as f:
            meta = json.load(f)
        meta["_slug"] = d.name
        out.append(meta)
    return out


def by_slug(metas: list[dict]) -> dict[str, dict]:
    return {m["_slug"]: m for m in metas}


def group_by_category(metas: list[dict]) -> "OrderedDict[str, list[dict]]":
    grouped: "OrderedDict[str, list[dict]]" = OrderedDict((c, []) for c in CATEGORIES)
    for m in metas:
        grouped.setdefault(m["category"], []).append(m)
    for v in grouped.values():
        v.sort(key=lambda x: x["title"].lower())
    return grouped


def render_card(meta: dict, featured: bool = False) -> str:
    slug = meta["_slug"]
    title = escape(meta["title"])
    desc = escape(meta["description"])
    cat = escape(meta["category"])
    tags_html = " ".join(
        f'<span class="card__tag">{escape(t)}</span>'
        for t in meta.get("tags", [])[:4]
    )
    klass = "card card--featured" if featured else "card"
    media_klass = "card__media card__media--featured" if featured else "card__media"
    img_size = "900/600" if featured else "600/400"
    return (
        f'    <a class="{klass}" href="effects/{slug}/index.html" '
        f'data-category="{cat}">\n'
        f'      <div class="{media_klass}">\n'
        f'        <div class="hover-effect {slug}" aria-hidden="true">\n'
        f'          <img src="https://picsum.photos/seed/{slug}/{img_size}" alt="" loading="lazy">\n'
        f'        </div>\n'
        f'      </div>\n'
        f'      <div class="card__body">\n'
        f'        <span class="card__badge">{cat}</span>\n'
        f'        <h3 class="card__title">{title}</h3>\n'
        f'        <p class="card__desc">{desc}</p>\n'
        f'        <div class="card__tags">{tags_html}</div>\n'
        f'      </div>\n'
        f'    </a>'
    )


def render_filter(groups: "OrderedDict[str, list[dict]]") -> str:
    total = sum(len(v) for v in groups.values())
    pills = [f'<label class="filter__pill"><input type="radio" name="cat" value="all" checked><span>All <small>({total})</small></span></label>']
    for cat, items in groups.items():
        if not items:
            continue
        pills.append(
            f'<label class="filter__pill"><input type="radio" name="cat" value="{cat}">'
            f'<span>{cat.capitalize()} <small>({len(items)})</small></span></label>'
        )
    return "\n      ".join(pills)


def render_featured(by_sl: dict[str, dict]) -> str:
    cards = "\n".join(render_card(by_sl[s], featured=True) for s in FEATURED_SLUGS if s in by_sl)
    return f'    <section class="featured" aria-label="Featured effects">\n      <div class="featured__grid">\n{cards}\n      </div>\n    </section>'


def render_sections(groups: "OrderedDict[str, list[dict]]", featured_slugs: set[str]) -> str:
    out = []
    for cat, items in groups.items():
        if not items:
            continue
        non_featured = [m for m in items if m["_slug"] not in featured_slugs]
        if not non_featured:
            continue
        cards = "\n".join(render_card(m) for m in non_featured)
        out.append(
            f'    <section class="section" id="cat-{cat}">\n'
            f'      <header class="section__header">\n'
            f'        <h2 class="section__title">{cat.capitalize()}</h2>\n'
            f'        <p class="section__count">{len(non_featured)} effect{"s" if len(non_featured) != 1 else ""}</p>\n'
            f'      </header>\n'
            f'      <div class="grid">\n{cards}\n      </div>\n'
            f'    </section>'
        )
    return "\n\n".join(out)


def main():
    metas = load_meta()
    groups = group_by_category(metas)
    by_sl = by_slug(metas)
    total = len(metas)

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Pure CSS image hover effects</title>
  <meta name="description" content="A curated library of {total} pure-CSS image hover effects. Copy-paste ready. No JavaScript.">
  <link rel="stylesheet" href="styles/base.css">
  <link rel="stylesheet" href="styles/catalog.css">
</head>
<body>
  <header class="hero">
    <h1 class="hero__title">Pure CSS image hover effects</h1>
    <p class="hero__sub">{total} effects. One class on a div. No JavaScript.</p>
    <p class="hero__meta">
      <a href="CONTRACT.md">Contract</a>
      <span aria-hidden="true">/</span>
      <a href="META_SCHEMA.md">Schema</a>
      <span aria-hidden="true">/</span>
      <a href="BROWSER_SUPPORT.md">Browser support</a>
      <span aria-hidden="true">/</span>
      <a href="ACCESSIBILITY.md">Accessibility</a>
    </p>
  </header>

{render_featured(by_sl)}

  <nav class="filter" aria-label="Filter by category">
      {render_filter(groups)}
  </nav>

  <main>
{render_sections(groups, set(FEATURED_SLUGS))}
  </main>

  <footer class="site-footer">
    <p>Generated by <code>scripts/build_catalog.py</code>. Source of truth: <code>effects/*/meta.json</code>.</p>
  </footer>
</body>
</html>
"""
    OUT.write_text(page)
    print(f"Wrote {OUT.relative_to(REPO)} ({len(page):,} bytes, {total} effects)")


if __name__ == "__main__":
    main()
