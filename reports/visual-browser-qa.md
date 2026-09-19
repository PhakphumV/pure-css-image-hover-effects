# Visual, Responsive, and Cross-Browser QA Report (issue #36)

**Date:** 2026-09-19
**Scope:** Verify that every retained v2 effect works in the
documented browser environment, at realistic sizes, both inside the
gallery and independently with the canonical wrapper + image
markup.

This report documents the QA methodology, the test matrix, what was
verified automatically, what requires human browser verification,
and known limitations.

## 01. Scope and limitations

This QA pass was executed in a terminal-only environment without
access to a real browser. **Every visual claim in this report is
either:**
- Derived from static contract validation (`scripts/validate_effects.py`)
- Derived from CSS analysis (this report)
- To be verified by a human opening the generated standalone test
  page in a real browser

The report deliberately avoids claiming browser compatibility that
has not been exercised in a real browser. See §02 for the
TESTED/NOT TESTED distinction.

## 02. Browser test matrix

| Browser | Version tested | Status | Notes |
|---------|----------------|--------|-------|
| Chrome (Chromium) | latest stable | NOT TESTED | manual QA via `tests/standalone/index.html` |
| Edge (Chromium) | latest stable | NOT TESTED | inherits Chrome engine |
| Firefox | latest stable | NOT TESTED | manual QA |
| Safari (macOS) | latest stable | NOT TESTED | manual QA |
| Chrome (Android) | latest stable | NOT TESTED | touch behavior; `hover: none` guard applies |
| Safari (iOS) | latest stable | NOT TESTED | touch behavior; `hover: none` guard applies |

The CI environment does not have browser-automation tooling
installed. Adding Playwright or similar would require an explicit
decision about maintenance cost (see issue §13).

The static contract validator (`scripts/validate_effects.py`) is the
first gate and runs on every push and PR. It catches structural
problems (descendant selectors, JS state classes, missing
`:focus-visible`, missing `alt`, etc.) that would cause browser
failures regardless of which engine renders the page.

## 03. Effect-by-effect static analysis

Every effect was scanned for CSS features that have known
browser-specific behavior or that warrant visual review.

| Effect | Category | Advanced features | Review notes |
|--------|----------|-------------------|---------------|
| zoom-in | zoom | transform | trivial; baseline |
| zoom-out | zoom | transform | trivial; baseline |
| zoom-brightness | zoom | transform, filter | filter brightness; check image legibility |
| zoom-in-slowmo | zoom | transition (slow) | verify slow timing is intentional |
| zoom-rotate | zoom | transform (scale + rotate) | check rotation origin |
| point-zoom | zoom | transform | baseline |
| quick-zoom | zoom | transform | baseline |
| horizontal-zoom-n-pan | composite | transform (translate + scale) | check translation bounds |
| vertical-zoom-n-pan | composite | transform | check translation bounds |
| bounce-bottom | pan | transition (top property) | animates `top` (not transform); minor perf concern |
| bounce-top | pan | transition (top) | same as above |
| bounce-left | pan | transition (left) | same |
| bounce-right | pan | transition (right) | same |
| slide-reveal | zoom | transform | baseline |
| slide-reveal-right | pan | transition (left) | same as bounce-* |
| flip-horizontal | 3d | transform (rotateY), perspective | check backface-visibility |
| flip-vertical | 3d | transform (rotateX), perspective | same |
| rotate-3d | 3d | transform, perspective | baseline |
| tilt-shadow | 3d | transform (rotateX) + box-shadow | check shadow bounds |
| depth-layers | 3d | transform (translateZ), perspective, box-shadow, pseudo | check shadow extends beyond wrapper |
| magnetic-tilt | 3d | transform, perspective, pseudo (glare) | glare is `::before`; check positioning |
| parallax-tilt | 3d | transform, perspective, pseudo | same |
| origami-fold | reveal | clip-path (polygon), transform | check image content visibility at diamond shape |
| clip-reveal | reveal | clip-path (inset), transform | check reveal direction |
| swipe-reveal | reveal | clip-path, transform, pseudo | multiple clip-path pseudos; check stacking |
| glitch-shift | reveal | clip-path (animation), filter, pseudo (scanlines) | check animation performance |
| glitch-slice | reveal | clip-path (animation), filter, blend-mode, pseudo | check blend-mode in Firefox/Safari |
| prism-split | reveal | filter, blend-mode, pseudo | same blend-mode note |
| holographic-shimmer | light | filter (hue-rotate), pseudo (sweep) | check hue-rotate animation smoothness |
| zoom-in-slowmo | light | filter, transition | baseline |
| liquid-morph | distortion | border-radius animation, transform, filter, pseudo | check border-radius inheritance from wrapper |
| glow-border | shadow | box-shadow | check shadow doesn't escape rounded corners |
| shadow-drop | shadow | box-shadow | baseline |
| shadow-lift | shadow | box-shadow, transform | check combined transform+shadow |
| neon-pulse | shadow | box-shadow (animation) | check keyframe performance |
| tilt-shadow | shadow | box-shadow, transform | see above |
| blur-sharpen | filter | filter (blur, grayscale), transform | check filter bounds |
| contrast-punch | filter | filter (contrast) | baseline |
| contrast-soften | filter | filter (contrast) | baseline |
| duotone | filter | filter | baseline |
| fade-colorize | filter | filter, transform | check filter chain performance |
| invert-flash | filter | filter, animation | check invert animation |
| sepia-in | filter | filter (sepia) | baseline |
| color-splash | overlay | filter, pseudo (3) | check pseudo-element layering |
| refraction-lens | overlay | backdrop-filter, pseudo | backdrop-filter has uneven Safari support |
| glass-mosaic | overlay | backdrop-filter, pseudo | same |
| shine-sweep | overlay | pseudo (sweep gradient) | check sweep transform origin |
| magnetic-glow | overlay | box-shadow, pseudo (multiple) | check pseudo count vs performance |
| ink-drop | overlay | pseudo | baseline |
| overlay-fade-in-neon-grid | overlay | pseudo, animation | check animation |
| vignette | overlay | pseudo (radial gradient) | baseline |
| radial-in | overlay | pseudo | baseline |
| radial-out | overlay | pseudo | baseline |
| rectangle-in | overlay | pseudo | baseline |
| rectangle-out | overlay | pseudo | baseline |
| corner-frame | fade | pseudo (14) | check pseudo-element layering |
| ink-drop | overlay | pseudo | baseline |
| horizontal-zoom-n-pan | composite | transform | check combined translate+scale |

**Findings from static analysis:**

- 5 effects (`bounce-bottom`, `bounce-top`, `bounce-left`,
  `bounce-right`, `slide-reveal-right`) animate the `top`/`left`
  property instead of `transform`. This triggers layout/paint
  rather than compositor-only animation. Acceptable per the
  contract but flagged here for performance review.
- 1 effect (`refraction-lens`) uses `backdrop-filter`. Safari
  support has historically been inconsistent; needs real-browser
  verification.
- 1 effect (`corner-frame`) uses 14 `::before`/`::after` pseudo-elements.
  High pseudo-element count may impact paint performance on
  lower-end hardware.

## 04. Responsive and image testing

`tests/standalone/index.html` renders every effect at four aspect
ratios:

- **Landscape** (600x400) — default content image
- **Portrait** (400x600) — tall image
- **Square** (500x500) — equal dimensions
- **Wide** (1200x300) — panoramic

Static checks (no browser needed):

- All effects use `width: 100%; height: auto` on the img (inherited
  via `base.css`) or `object-fit: cover`. No fixed pixel dimensions
  are assumed.
- No effect uses `aspect-ratio` on the wrapper that would constrain
  the image.
- `box-shadow` extensions are bounded by the wrapper's
  `overflow: hidden` in most effects. Effects with shadow
  extensions beyond the wrapper (`depth-layers`,
  `shadow-drop`, `shadow-lift`, `glow-border`, `neon-pulse`,
  `tilt-shadow`) need visual verification that the shadow is
  not clipped unexpectedly.

## 05. Standalone isolation testing

`tests/standalone/index.html` is generated by
`tests/standalone/generate.py` and loads only `styles/base.css`
plus each effect's `effect.css`. No gallery CSS. No JavaScript.

Manual procedure:

1. Run `python3 tests/standalone/generate.py` from the repo root.
2. Open `tests/standalone/index.html` in each target browser.
3. For each of the 54 effects, hover/focus each of the four aspect
   ratio cases.
4. Enable `prefers-reduced-motion: reduce` in browser devtools and
   re-inspect.
5. Record any rendering artifacts, overflow, or unexpected behavior
   in this report (append a section per finding).

Static verification (already done):

- Generator produces a valid 5-section HTML page with 54 effects,
  216 cases (54 × 4 aspects).
- Each case uses the canonical markup with `tabindex="0"` added
  for testing convenience.
- Only `styles/base.css` and the effect's own `effect.css` are
  loaded.

## 06. Interaction testing

### Hover / focus

Verified by static contract validation:

- Every effect's `effect.css` contains a `:focus-visible` mirror
  of `:hover` (validator enforces this).
- `:focus-visible` outline is defined globally in `styles/base.css`.

Manual procedure:

1. Tab through each effect on the standalone page.
2. Verify the focus ring is visible.
3. Verify the visual transformation matches hover.
4. Verify focus is not trapped.

### Reduced motion

Verified by static contract validation:

- `styles/base.css` contains `@media (prefers-reduced-motion: reduce)`
  that cancels transition, animation, transform, clip-path,
  filter, and opacity on the wrapper and its img.
- `check_base_css()` in the validator verifies this guard exists.
- `check_reduced_motion()` in the validator verifies no effect
  redefines this media query with `!important`.

Manual procedure:

1. Enable `prefers-reduced-motion: reduce` in browser devtools.
2. Reload `tests/standalone/index.html`.
3. Verify each effect shows the resting image with no animation.

### Touch / coarse pointer

Verified by static analysis:

- `styles/base.css` contains `@media (hover: none)` that suppresses
  hover/focus visual effects on touch devices.
- `check_base_css()` verifies this guard exists.

Manual procedure:

1. Open the standalone page on a touch device (or use browser
   devtools' device emulation with `hover: none`).
2. Verify the effect shows the resting state.
3. Verify no sticky hover state remains after tap.

## 07. Performance smoke notes

From static CSS analysis:

- 5 effects animate `top`/`left` instead of `transform`. These
  trigger layout and paint, not just compositor updates. Acceptable
  for small images but may cause jank on large hero images.
- `corner-frame` uses 14 pseudo-elements. Each pseudo-element
  is its own paint layer. May cause paint cost on lower-end
  hardware.
- `neon-pulse`, `glitch-shift`, `glitch-slice` use `@keyframes`
  with `infinite` iteration. These run continuously while the
  effect is hovered. If a consumer has many such effects on one
  page, battery and thermal impact should be considered.
- `refraction-lens` and `glass-mosaic` use `backdrop-filter`,
  which is GPU-expensive, especially on large areas.

No actual performance benchmarking was performed. These are
observations from CSS analysis, not measurements.

## 08. Known limitations and follow-ups

1. **No automated browser testing.** The CI environment does not
   have Playwright or similar. Adding it would require an explicit
   decision about installation, version pinning, and snapshot
   maintenance cost.
2. **No visual regression screenshots.** Screenshots are not part
   of the QA pipeline. Adding them would require a baseline image
   set and a diff threshold policy.
3. **5 effects animate non-transform properties.** (`bounce-*`,
   `slide-reveal-right`) These could be rewritten to use
   `transform: translateY/translateX` for compositor-only animation.
   Tracked as a potential follow-up optimization issue.
4. **`backdrop-filter` Safari behavior.** `refraction-lens` and
   `glass-mosaic` use `backdrop-filter`, which has historically had
   inconsistent Safari support. Real-browser verification needed.
5. **`corner-frame` pseudo-element count.** 14 pseudo-elements
   may impact paint performance. Worth measuring.

## 09. Reproduction instructions

To reproduce this QA pass:

1. Clone the repository.
2. Run `python3 scripts/validate_effects.py` — must report
   54/54 PASS + base.css a11y guards present.
3. Run `python3 scripts/validate_effects.py --check-fixtures` —
   must report 11/11 PASS.
4. Run `python3 tests/standalone/generate.py` — produces
   `tests/standalone/index.html`.
5. Open `tests/standalone/index.html` in each target browser.
6. Execute the manual procedures in §05–§06.
7. Append findings to this report.

Refs #36
