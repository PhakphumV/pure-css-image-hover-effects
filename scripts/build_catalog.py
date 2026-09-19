#!/usr/bin/env python3
"""
scripts/build_catalog.py
========================

Generates the root index.html catalog from every effects/<slug>/meta.json.

The catalog is a single static HTML page with:
- a CSS-only category filter (no JS — contract §1)
- a responsive grid of effect cards grouped by the 13 categories
- one click per card to open the effect detail page

Pure Python stdlib. Re-running produces byte-identical output (deterministic
per the rebuild plan, issue #8).

Usage:
    python3 scripts/build_catalog.py
"""
import json
import re
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


def group_by_category(metas: list[dict]) -> "OrderedDict[str, list[dict]]":
    grouped: "OrderedDict[str, list[dict]]" = OrderedDict((c, []) for c in CATEGORIES)
    for m in metas:
        grouped.setdefault(m["category"], []).append(m)
    for v in grouped.values():
        v.sort(key=lambda x: x["title"].lower())
    return grouped


def render_card(meta: dict) -> str:
    slug = meta["_slug"]
    title = escape(meta["title"])
    desc = escape(meta["description"])
    tags = " ".join(
        f'<span class="card__tag">{escape(t)}</span>'
        for t in meta.get("tags", [])[:4]
    )
    return (
        f'    <a class="card" href="effects/{slug}/index.html" '
        f'data-category="{escape(meta["category"])}">\n'
        f'      <div class="card__media">\n'
        f'        <div class="hover-effect {slug}" aria-hidden="true">\n'
        f'          <img src="https://picsum.photos/seed/{slug}/600/400" alt="" loading="lazy">\n'
        f'        </div>\n'
        f'      </div>\n'
        f'      <div class="card__body">\n'
        f'        <h3 class="card__title">{title}</h3>\n'
        f'        <p class="card__desc">{desc}</p>\n'
        f'        <div class="card__tags">{tags}</div>\n'
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


def render_sections(groups: "OrderedDict[str, list[dict]]") -> str:
    out = []
    for cat, items in groups.items():
        if not items:
            continue
        cards = "\n".join(render_card(m) for m in items)
        out.append(
            f'    <section class="section" id="cat-{cat}">\n'
            f'      <header class="section__header">\n'
            f'        <h2 class="section__title">{cat.capitalize()}</h2>\n'
            f'        <p class="section__count">{len(items)} effect{"s" if len(items) != 1 else ""}</p>\n'
            f'      </header>\n'
            f'      <div class="grid">\n{cards}\n      </div>\n'
            f'    </section>'
        )
    return "\n\n".join(out)


def main():
    metas = load_meta()
    groups = group_by_category(metas)
    total = len(metas)

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Pure CSS Image Hover Effects</title>
  <meta name="description" content="A curated library of {total} pure-CSS image hover effects. Copy-paste ready. No JavaScript.">
  <link rel="stylesheet" href="styles/base.css">
  <link rel="stylesheet" href="styles/catalog.css">
</head>
<body>
  <header class="hero">
    <p class="hero__eyebrow">v2.0 rebuild</p>
    <h1 class="hero__title">Pure CSS image hover effects</h1>
    <p class="hero__sub">{total} effects. One class on a div. No JavaScript.</p>
    <p class="hero__meta">
      <a href="CONTRACT.md">Contract</a>
      <span aria-hidden="true">/</span>
      <a href="META_SCHEMA.md">Schema</a>
      <span aria-hidden="true">/</span>
      <a href="BROWSER_SUPPORT.md">Browser support</a>
    </p>
  </header>

  <nav class="filter" aria-label="Filter by category">
      {render_filter(groups)}
  </nav>

  <main>
{render_sections(groups)}
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