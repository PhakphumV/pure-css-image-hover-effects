#!/usr/bin/env python3
"""
tests/standalone/generate.py
============================

Generates tests/standalone/index.html — a single-page standalone test
for every retained effect. Loads only styles/base.css and each
effect's effect.css. No gallery CSS. No JavaScript. Used by the
visual/browser QA pass (issue #36) to verify that every effect
works with the canonical markup in isolation.

Run from the repo root:
    python3 tests/standalone/generate.py

Open tests/standalone/index.html in a browser to inspect every
effect at four aspect ratios (landscape, portrait, square, wide).
"""
import json
from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
EFFECTS = REPO / "effects"
OUT = REPO / "tests" / "standalone" / "index.html"

ASPECTS = [
    ("landscape", 600, 400),
    ("portrait", 400, 600),
    ("square", 500, 500),
    ("wide", 1200, 300),
]


def load_meta() -> list[dict]:
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


def render_effect_section(meta: dict) -> str:
    slug = meta["_slug"]
    title = escape(meta["title"])
    category = escape(meta["category"])
    desc = escape(meta["description"])
    cases = []
    for label, w, h in ASPECTS:
        cases.append(
            f'      <div class="case">\n'
            f'        <p class="case__label">{label} {w}x{h}</p>\n'
            f'        <div class="hover-effect {slug}" tabindex="0">\n'
            f'          <img src="https://picsum.photos/seed/{slug}-{label}/{w}/{h}" alt="{title} demo">\n'
            f'        </div>\n'
            f'      </div>'
        )
    return (
        f'  <section class="effect" id="{slug}">\n'
        f'    <header class="effect__header">\n'
        f'      <h2 class="effect__title">{title}</h2>\n'
        f'      <p class="effect__meta">category: <code>{category}</code> &middot; slug: <code>{slug}</code></p>\n'
        f'      <p class="effect__desc">{desc}</p>\n'
        f'    </header>\n'
        f'    <div class="cases">\n'
        + "\n".join(cases) +
        f'\n    </div>\n'
        f'  </section>'
    )


def main():
    metas = load_meta()
    sections = "\n\n".join(render_effect_section(m) for m in metas)

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Standalone test — Pure CSS Image Hover Effects</title>
  <link rel="stylesheet" href="../../styles/base.css">
  <style>
    body {{ padding: 2rem; max-width: 1400px; margin: 0 auto; background: #fafafa; }}
    .intro {{ margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 1px solid #e5e5e5; }}
    .intro h1 {{ margin: 0 0 0.5rem; font-size: 1.5rem; }}
    .intro p {{ margin: 0.25rem 0; color: #666; font-size: 0.9rem; }}
    .effect {{ margin-bottom: 3rem; padding-bottom: 1.5rem; border-bottom: 1px solid #f0f0f0; }}
    .effect__header {{ margin-bottom: 1rem; }}
    .effect__title {{ margin: 0 0 0.25rem; font-size: 1.125rem; font-weight: 600; }}
    .effect__meta {{ margin: 0 0 0.25rem; font-size: 0.8125rem; color: #666; }}
    .effect__desc {{ margin: 0; font-size: 0.875rem; color: #444; }}
    .cases {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; }}
    .case {{ background: #fff; border: 1px solid #e5e5e5; border-radius: 6px; padding: 0.75rem; }}
    .case__label {{ margin: 0 0 0.5rem; font-size: 0.75rem; color: #666; font-family: ui-monospace, monospace; }}
    .case img {{ display: block; width: 100%; height: auto; }}
  </style>
</head>
<body>
  <header class="intro">
    <h1>Standalone test — every effect at four aspect ratios</h1>
    <p>Loads only <code>styles/base.css</code> and each effect's <code>effect.css</code>. No gallery CSS. No JavaScript.</p>
    <p>Manual QA: open this file in a browser, hover/focus each effect, enable <code>prefers-reduced-motion</code>, and inspect for layout overflow, clipping, or rendering artifacts.</p>
    <p>Total effects tested: <strong>{len(metas)}</strong></p>
  </header>

{sections}

</body>
</html>
"""
    OUT.write_text(page)
    print(f"Wrote {OUT.relative_to(REPO)} ({len(page):,} bytes, {len(metas)} effects)")


if __name__ == "__main__":
    main()
