#!/usr/bin/env python3
"""
Script to standardize all effect pages in pure-css-image-hover-effects.
Fixes:
1. HTML structure to use standard effect-page.css layout
2. CSS code blocks to match style.css exactly
3. Creates missing README.md files
4. Updates effects-manifest.js with proper descriptions
"""

import os
import re
import json
from pathlib import Path

BASE_DIR = Path("/home/phakphumv/.hermes/profiles/freelance/home/pure-css-image-hover-effects")
EFFECTS_DIR = BASE_DIR / "effects"
STYLES_DIR = BASE_DIR / "styles"

# Effect metadata: folder_name -> {title, description, css_properties, credits_notes}
EFFECTS_META = {
    "blur-sharpen": {
        "title": "Blur to Sharp",
        "description": "Blurred grayscale image sharpens to full color on hover.",
        "css_properties": ["filter", "transform", "transition"],
        "credits": "Blur-to-sharp filter transition"
    },
    "bounce-top": {
        "title": "Bounce Top",
        "description": "Image slides from bottom to top on hover with bounce effect.",
        "css_properties": ["transform", "transition", "cubic-bezier"],
        "credits": "Bounce reveal effect"
    },
    "bounce-bottom": {
        "title": "Bounce Bottom",
        "description": "Image slides from top to bottom on hover with bounce effect.",
        "css_properties": ["transform", "transition", "cubic-bezier"],
        "credits": "Bounce reveal effect"
    },
    "bounce-left": {
        "title": "Bounce Left",
        "description": "Image slides from right to left on hover with bounce effect.",
        "css_properties": ["transform", "transition", "cubic-bezier"],
        "credits": "Bounce reveal effect"
    },
    "bounce-right": {
        "title": "Bounce Right",
        "description": "Image slides from left to right on hover with bounce effect.",
        "css_properties": ["transform", "transition", "cubic-bezier"],
        "credits": "Bounce reveal effect"
    },
    "clip-reveal": {
        "title": "Clip Reveal",
        "description": "Image reveals through animated clip-path on hover.",
        "css_properties": ["clip-path", "transition"],
        "credits": "Clip-path reveal effect"
    },
    "color-splash": {
        "title": "Color Splash",
        "description": "Circular color splash expands from center on hover.",
        "css_properties": ["pseudo-element", "border-radius", "transform", "transition"],
        "credits": "Color splash expansion effect"
    },
    "duotone": {
        "title": "Duotone Shift",
        "description": "Duotone filter transitions to normal color on hover.",
        "css_properties": ["filter", "transform", "transition"],
        "credits": "Duotone filter transition"
    },
    "fade-colorize": {
        "title": "Fade to Color",
        "description": "Grayscale image transitions to full color on hover.",
        "css_properties": ["filter", "transform", "transition"],
        "credits": "Grayscale to color transition"
    },
    "flip-horizontal": {
        "title": "Flip Horizontal",
        "description": "Image flips horizontally on hover using CSS 3D transform.",
        "css_properties": ["transform", "perspective", "transform-style", "transition"],
        "credits": "3D flip effect implementation"
    },
    "flip-vertical": {
        "title": "Flip Vertical",
        "description": "Image flips vertically on hover using CSS 3D transform.",
        "css_properties": ["transform", "perspective", "transform-style", "transition"],
        "credits": "3D flip effect implementation"
    },
    "glass-mosaic": {
        "title": "Glass Mosaic",
        "description": "Frosted-glass overlay with backdrop-filter that dims on hover.",
        "css_properties": ["backdrop-filter", "pseudo-element", "transition", "css-variables"],
        "credits": "Frosted glass overlay effect"
    },
    "glow-border": {
        "title": "Glow Border",
        "description": "Glowing border animation appears around image on hover.",
        "css_properties": ["box-shadow", "transition", "pseudo-element"],
        "credits": "Glow border animation"
    },
    "horizontal-zoom-n-pan": {
        "title": "Horizontal Zoom & Pan",
        "description": "Image zooms and pans horizontally on hover.",
        "css_properties": ["transform", "transform-origin", "transition"],
        "credits": "Horizontal pan-zoom effect"
    },
    "ink-drop": {
        "title": "Ink Drop",
        "description": "Circular \"ink\" splash expands from center on hover.",
        "css_properties": ["pseudo-element", "border-radius", "transform", "transition"],
        "credits": "Circular ink splash effect"
    },
    "overlay-fade-in-neon-grid": {
        "title": "Overlay Fade In Neon Grid",
        "description": "Neon grid overlay fades in over image on hover.",
        "css_properties": ["background", "pseudo-element", "transition", "opacity"],
        "credits": "Neon grid overlay effect"
    },
    "point-zoom": {
        "title": "Point Zoom",
        "description": "Image zooms toward cursor position on hover.",
        "css_properties": ["transform", "transform-origin", "transition"],
        "credits": "Cursor-based zoom effect"
    },
    "quick-zoom": {
        "title": "Quick Zoom",
        "description": "Fast zoom-in effect on hover with short transition.",
        "css_properties": ["transform", "transition"],
        "credits": "Quick zoom effect"
    },
    "radial-in": {
        "title": "Radial In",
        "description": "Image reveals from center outward using circular mask on hover.",
        "css_properties": ["pseudo-element", "border-radius", "transform", "transition"],
        "credits": "Radial reveal effect"
    },
    "radial-out": {
        "title": "Radial Out",
        "description": "Circular mask expands outward revealing image on hover.",
        "css_properties": ["pseudo-element", "border-radius", "transform", "transition"],
        "credits": "Radial expansion effect"
    },
    "rectangle-in": {
        "title": "Rectangle In",
        "description": "Rectangular mask reveals image from center on hover.",
        "css_properties": ["pseudo-element", "clip-path", "transform", "transition"],
        "credits": "Rectangular reveal effect"
    },
    "rectangle-out": {
        "title": "Rectangle Out",
        "description": "Rectangular mask expands outward on hover.",
        "css_properties": ["pseudo-element", "clip-path", "transform", "transition"],
        "credits": "Rectangular expansion effect"
    },
    "refraction-lens": {
        "title": "Refraction Lens",
        "description": "Magnifying lens effect with gradient overlay that scales on hover.",
        "css_properties": ["pseudo-element", "border-radius", "background-gradient", "transform", "transition"],
        "credits": "Magnifying lens effect"
    },
    "rotate-3d": {
        "title": "3D Rotate",
        "description": "Perspective-based 3D rotation with scale on hover.",
        "css_properties": ["transform", "perspective", "transform-style", "transition"],
        "credits": "3D perspective rotation effect"
    },
    "slide-reveal": {
        "title": "Slide Reveal",
        "description": "Image slides to reveal content on hover.",
        "css_properties": ["transform", "transition", "overflow"],
        "credits": "Slide reveal effect"
    },
    "slide-reveal-right": {
        "title": "Slide Reveal Right",
        "description": "Image slides right to reveal content on hover.",
        "css_properties": ["transform", "transition", "overflow"],
        "credits": "Slide reveal right effect"
    },
    "vertical-zoom-n-pan": {
        "title": "Vertical Zoom & Pan",
        "description": "Image zooms and pans vertically on hover.",
        "css_properties": ["transform", "transform-origin", "transition"],
        "credits": "Vertical pan-zoom effect"
    },
    "vignette": {
        "title": "Vignette",
        "description": "Vignette effect fades in on hover, darkening edges.",
        "css_properties": ["box-shadow", "pseudo-element", "transition"],
        "credits": "Vignette overlay effect"
    },
    "zoom-brightness": {
        "title": "Zoom Brightness",
        "description": "Image zooms and brightens from dimmed state on hover.",
        "css_properties": ["transform", "filter", "transition"],
        "credits": "Zoom with brightness transition"
    },
    "zoom-in": {
        "title": "Zoom In",
        "description": "Simple smooth zoom-in on hover.",
        "css_properties": ["transform", "transition"],
        "credits": "Basic zoom effect"
    },
    "zoom-in-slowmo": {
        "title": "Zoom In Slowmo",
        "description": "Dramatic slow-motion zoom with brightness shift on hover.",
        "css_properties": ["transform", "filter", "transition", "transform-origin"],
        "credits": "Slow-motion zoom effect"
    },
    "zoom-out": {
        "title": "Zoom Out",
        "description": "Zoomed-in image pulls back to normal on hover.",
        "css_properties": ["transform", "transition"],
        "credits": "Reverse zoom effect"
    },
    "zoom-rotate": {
        "title": "Zoom Rotate",
        "description": "Image zooms and slightly rotates on hover.",
        "css_properties": ["transform", "transition", "cubic-bezier"],
        "credits": "Zoom with rotation effect"
    },
}

def read_style_css(effect_dir):
    """Read and return the content of style.css"""
    css_path = effect_dir / "style.css"
    if css_path.exists():
        return css_path.read_text()
    return None

def format_css_for_html(css_content):
    """Format CSS content for HTML code block display"""
    if not css_content:
        return ""
    # Ensure consistent formatting - keep as-is but escape for HTML
    return css_content.replace("&", "&").replace("<", "<").replace(">", ">")

def generate_html_page(effect_name, meta):
    """Generate standardized HTML page for an effect"""
    effect_dir = EFFECTS_DIR / effect_name
    css_content = read_style_css(effect_dir)
    
    if not css_content:
        print(f"WARNING: No style.css found for {effect_name}")
        return None
    
    css_formatted = format_css_for_html(css_content)
    
    # Random image number for variety
    import hashlib
    img_num = int(hashlib.md5(effect_name.encode()).hexdigest(), 16) % 50 + 1
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{meta["title"]} — Pure CSS Image Hover Effects</title>
  <link rel="stylesheet" href="../../styles/effect-page.css">
  <link rel="stylesheet" href="./style.css">
</head>
<body>
  <header class="page-header">
    <a href="../../index.html" class="back-link">← Back to Gallery</a>
    <h1>{meta["title"]}</h1>
    <p class="effect-description">{meta["description"]}</p>
  </header>

  <main class="effect-layout">
    <div class="left-column">
      <section class="panel panel--preview">
        <h2>Preview</h2>
        <div class="preview-container">
          <div class="{effect_name}">
            <img src="https://picsum.photos/600/400?random={img_num}" alt="Demo image">
          </div>
        </div>
        <p class="preview-hint">Hover over the image to see the effect</p>
      </section>

      <section class="panel panel--credits">
        <h2>Credits</h2>
        <div class="credit-entry">
          <strong>PhakphumV</strong>
          <span class="credit-role">Creator</span>
          <span class="credit-notes">{meta["credits"]}</span>
        </div>
      </section>
    </div>

    <div class="right-column">
      <section class="panel panel--code">
        <h2>HTML</h2>
        <pre class="code-block"><code><div class="{effect_name}">
  <img src="your-image.jpg" alt="Description">
</div></code></pre>
      </section>

      <section class="panel panel--code">
        <h2>CSS</h2>
        <pre class="code-block"><code>{css_formatted}</code></pre>
      </section>
    </div>
  </main>

  <footer class="page-footer">
    <p>MIT License — <a href="https://github.com/PhakphumV/pure-css-image-hover-effects" target="_blank" rel="noopener">GitHub</a></p>
  </footer>
</body>
</html>'''
    return html

def generate_readme(effect_name, meta):
    """Generate README.md for an effect"""
    effect_dir = EFFECTS_DIR / effect_name
    css_content = read_style_css(effect_dir)
    
    if not css_content:
        return None
    
    # Extract key CSS for the "Key CSS" section
    css_lines = css_content.strip().split('\n')
    key_css = '\n'.join(css_lines[:20])  # First 20 lines
    
    readme = f'''# {meta["title"]}

{meta["description"]}

**Key CSS**
```css
{key_css}
```

**Browser Support**
| Feature | Support |
|---------|---------|
'''
    for prop in meta["css_properties"]:
        support = get_browser_support(prop)
        readme += f"| `{prop}` | {support} |\n"
    
    readme += '\n'
    return readme

def get_browser_support(prop):
    """Get browser support string for a CSS property"""
    supports = {
        "transform": "Chrome 36+, FF 16+, Safari 9+, Edge 12+",
        "transition": "Chrome 36+, FF 16+, Safari 9+, Edge 12+",
        "filter": "Chrome 53+, FF 35+, Safari 9+",
        "backdrop-filter": "Chrome 76+, FF 70+, Safari 9+",
        "clip-path": "Chrome 28+, FF 28+, Safari 9+",
        "perspective": "Chrome 12+, FF 12+, Safari 7+",
        "transform-style": "Chrome 12+, FF 12+, Safari 7+",
        "pseudo-element": "All modern browsers",
        "border-radius": "Chrome 4+, FF 4+, Safari 5+, Edge 12+",
        "cubic-bezier": "Chrome 4+, FF 4+, Safari 3.1+, Edge 12+",
        "background-gradient": "Chrome 10+, FF 3.6+, Safari 4+, Edge 12+",
        "css-variables": "Chrome 49+, FF 31+, Safari 9.1+, Edge 15+",
        "box-shadow": "Chrome 10+, FF 4+, Safari 5.1+, Edge 12+",
        "transform-origin": "Chrome 36+, FF 16+, Safari 9+, Edge 12+",
        "opacity": "All modern browsers",
        "overflow": "All modern browsers",
    }
    return supports.get(prop, "Check caniuse.com")

def update_manifest():
    """Update effects-manifest.js with proper descriptions"""
    effects_list = []
    for folder_name in sorted(EFFECTS_META.keys()):
        meta = EFFECTS_META[folder_name]
        effects_list.append({
            "id": folder_name,
            "title": meta["title"],
            "desc": meta["description"],
            "folder": folder_name
        })
    
    manifest_content = f'''window.__EFFECTS_MANIFEST__ = {{
  "effects": {json.dumps(effects_list, indent=2)}
}};
'''
    manifest_path = BASE_DIR / "effects-manifest.js"
    manifest_path.write_text(manifest_content)
    print(f"Updated {manifest_path}")

def main():
    print("Starting standardization of effect pages...")
    
    # Process each effect
    for effect_name, meta in EFFECTS_META.items():
        effect_dir = EFFECTS_DIR / effect_name
        if not effect_dir.exists():
            print(f"WARNING: Effect directory not found: {effect_name}")
            continue
        
        # 1. Generate and write HTML page
        html_content = generate_html_page(effect_name, meta)
        if html_content:
            html_path = effect_dir / "index.html"
            html_path.write_text(html_content)
            print(f"  ✓ Updated {effect_name}/index.html")
        
        # 2. Generate and write README.md
        readme_content = generate_readme(effect_name, meta)
        if readme_content:
            readme_path = effect_dir / "README.md"
            readme_path.write_text(readme_content)
            print(f"  ✓ Created {effect_name}/README.md")
    
    # 3. Update manifest
    update_manifest()
    print("\nDone! All effects standardized.")

if __name__ == "__main__":
    main()