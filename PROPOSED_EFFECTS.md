# Proposed 7 New Effects for pure-css-image-hover-effects

This document proposes 7 new pure-CSS hover effects to add to the gallery. Each effect is designed to be unique, visually distinct from the existing 33 effects, and implementable with pure CSS (no JS).

---

## Current Effects Summary (33 total)

**Filter/Color Effects (6):** blur-sharpen, duotone, fade-colorize, zoom-brightness, vignette, color-splash  
**Reveal/Mask Effects (8):** clip-reveal, radial-in, radial-out, rectangle-in, rectangle-out, slide-reveal, slide-reveal-right, overlay-fade-in-neon-grid  
**Transform/Zoom Effects (10):** zoom-in, zoom-out, zoom-in-slowmo, quick-zoom, zoom-rotate, point-zoom, horizontal-zoom-n-pan, vertical-zoom-n-pan, rotate-3d, bounce-top/bottom/left/right  
**3D/Flip Effects (2):** flip-horizontal, flip-vertical  
**Overlay/Decorative (5):** glass-mosaic, glow-border, ink-drop, refraction-lens, vignette  

**Gaps Identified:** No pixelation effects, no light/shine sweeps, no split reveals, no cursor-following 3D tilt, no glitch/RGB-shift effects, no mosaic/tile explosions, no color-channel separation.

---

## Proposed 7 New Effects

### 1. **pixelate-sharpen** — *Pixelate to Sharp*
**Category:** Filter/Color Effect  
**Concept:** Image starts heavily pixelated (using `filter: blur() + contrast()` trick or SVG filter), transitions to razor-sharp on hover. Complements `blur-sharpen` with a distinct "retro/digital" aesthetic.  
**Key CSS:** `filter: blur() contrast()`, `transition`, `@keyframes` for stepped pixelation  
**Browser Support:** Chrome 53+, FF 35+, Safari 9+, Edge 12+  
**Unique Value:** Retro/gaming aesthetic; distinct from Gaussian blur

---

### 2. **light-sweep** — *Light Sweep / Shine*
**Category:** Overlay/Decorative Effect  
**Concept:** A diagonal light/shine sweeps across the image on hover — like a glare passing over a glossy photo. Pure CSS using animated gradient on pseudo-element.  
**Key CSS:** `::before` with `linear-gradient`, `transform: translateX(-150%) → translateX(150%)`, `transition`, `mix-blend-mode: screen`  
**Browser Support:** All modern browsers  
**Unique Value:** First "light/shine" effect in collection; adds premium/glossy feel

---

### 3. **split-reveal-diagonal** — *Split Diagonal Reveal*
**Category:** Reveal/Mask Effect  
**Concept:** Image splits diagonally (or horizontally/vertically) into two halves that slide apart to reveal the image (or alternate content). Uses `clip-path: polygon()` with animated points.  
**Key CSS:** `clip-path: polygon()`, `transform: translate()`, `transition`, `overflow: hidden`  
**Browser Support:** Chrome 28+, FF 28+, Safari 9+, Edge 12+  
**Unique Value:** Dynamic geometric reveal; distinct from radial/rectangular masks

---

### 4. **tilt-3d** — *3D Tilt / Perspective Follow*
**Category:** 3D/Transform Effect  
**Concept:** Subtle 3D tilt effect — image rotates slightly on X/Y axes following cursor position. **Pure CSS approximation** using `:hover` with `transform: perspective() rotateX() rotateY()` (true cursor-follow needs minimal JS, but hover-state tilt works pure CSS).  
**Key CSS:** `transform: perspective(1000px) rotateX(var(--rx)) rotateY(var(--ry))`, `transform-style: preserve-3d`, `transition`  
**Browser Support:** Chrome 12+, FF 12+, Safari 7+, Edge 12+  
**Unique Value:** Interactive 3D depth; distinct from `rotate-3d` (which is fixed rotation)

---

### 5. **glitch-rgb-shift** — *RGB Channel Shift / Glitch*
**Category:** Filter/Color Effect (Experimental)  
**Concept:** On hover, RGB channels separate/shift creating a digital glitch effect. Uses multiple pseudo-elements with `mix-blend-mode` (screen for R, multiply for B, etc.) and slight `transform: translate()` offsets animated via `@keyframes`.  
**Key CSS:** `::before`, `::after` with `mix-blend-mode`, `filter: hue-rotate()`, `animation` with `clip-path` for scanlines  
**Browser Support:** Chrome 58+, FF 52+, Safari 13.1+ (mix-blend-mode support)  
**Unique Value:** First "glitch/digital artifact" effect; trendy cyberpunk aesthetic

---

### 6. **mosaic-explode** — *Mosaic Tile Explode*
**Category:** Reveal/Mask Effect (Advanced)  
**Concept:** Image breaks into a grid of tiles (CSS Grid) that scale/rotate/fade out in sequence on hover, revealing the image (or alternate content) underneath. Uses `grid-template-columns`, `nth-child` delays, `transform: scale(0) rotate()`.  
**Key CSS:** `display: grid`, `grid-template-columns: repeat(N, 1fr)`, `@keyframes tile-explode`, `animation-delay` via `nth-child`  
**Browser Support:** Chrome 57+, FF 52+, Safari 10.1+, Edge 16+ (CSS Grid)  
**Unique Value:** Particle-like explosion; most complex/impressive reveal in collection

---

### 7. **color-channel-split** — *RGB Channel Separation*
**Category:** Filter/Color Effect  
**Concept:** On hover, the image splits into three offset layers (Red, Green, Blue) that separate slightly — creating a chromatic aberration / RGB split effect. Three pseudo-elements (or nested spans) with `filter: hue-rotate()` + `mix-blend-mode: screen` + `transform: translate()`.  
**Key CSS:** 3 layers with `mix-blend-mode: screen`, `filter: hue-rotate(0deg) / hue-rotate(120deg) / hue-rotate(240deg)`, `transform: translateX()`, `transition`  
**Browser Support:** Chrome 58+, FF 52+, Safari 13.1+  
**Unique Value:** Optical/photographic artifact effect; distinct from duotone/color-splash

---

## Implementation Notes

| Effect | Est. CSS Lines | Complexity | New CSS Features Introduced |
|--------|---------------|------------|----------------------------|
| pixelate-sharpen | ~30 | Low | `filter: contrast()` trick |
| light-sweep | ~25 | Low | Animated gradient + `mix-blend-mode` |
| split-reveal-diagonal | ~40 | Medium | Animated `clip-path: polygon()` |
| tilt-3d | ~35 | Medium | `transform-style: preserve-3d` |
| glitch-rgb-shift | ~60 | High | Multi-layer `mix-blend-mode` + `@keyframes` |
| mosaic-explode | ~80 | High | CSS Grid + staggered `nth-child` animations |
| color-channel-split | ~50 | Medium | Triple-layer `mix-blend-mode: screen` |

---

## Next Steps

If approved, I would:
1. Add 7 entries to `EFFECTS_META` in `standardize_effects.py`
2. Create 7 effect folders under `effects/` with `style.css` and placeholder `index.html`
3. Run `standardize_effects.py` to generate standardized pages, READMEs, and manifest
4. Add thumbnails to `index.html` gallery (or regenerate if automated)

---

**Ready to implement when you give the go-ahead.** Which effects interest you most? Want to adjust any concepts?