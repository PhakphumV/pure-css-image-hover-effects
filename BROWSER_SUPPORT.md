# Browser and CSS feature support policy

## Baseline

Per `CONTRACT.md §3`, every effect in this library targets:

| Browser | Versions supported |
|---------|--------------------|
| Chrome   | last 2 stable (current and previous) |
| Edge     | last 2 stable (Chromium-based; legacy Edge is not supported) |
| Firefox  | last 2 stable |
| Safari   | last 2 stable |

Anything outside this matrix is unsupported. In particular:

- Internet Explorer: not supported (no evergreen).
- Legacy Edge (EdgeHTML, pre-Chromium): not supported.
- Mobile / tablet: hover effects are out of scope per `CONTRACT.md §3`. The
  `@media (hover: none)` guard in `styles/base.css` intentionally suppresses
  all hover/focus states on touch-only devices.
- Embedded WebViews older than the matrix above: not supported.

## Tested vs claimed

The CI pipeline enforces the **structural** contract via
`scripts/validate_effects.py` (every push and PR). That covers
descendant-selector detection, `:focus-visible` mirror, `alt`
attribute, schema validation, reduced-motion override detection,
and the repo-level a11y guards in `styles/base.css`.

**Visual / cross-browser testing is currently NOT automated.**
`reports/visual-browser-qa.md` documents what was checked
statically, what requires a real browser, and the reproduction
procedure (`tests/standalone/generate.py` produces a standalone
test page that exercises every effect at four aspect ratios with
only `styles/base.css` + the effect's own `effect.css`).

Until browser automation is added, the matrix above describes the
**claimed** support baseline. Real-browser verification status for
each effect is recorded in `reports/visual-browser-qa.md`.

## CSS features used

Every effect MAY use the following CSS features. None of them require a
prefix in any browser in the matrix above; older prefixes are not shipped.

| Feature | Notes |
|---------|-------|
| `transform` | `scale`, `translate`, `rotate`, individual axis forms. |
| `transition` | timing functions and delays as needed per effect. |
| `filter` | `blur`, `grayscale`, `sepia`, `contrast`, `brightness`, `hue-rotate`, `saturate`, `drop-shadow`. |
| `backdrop-filter` | used by a small number of overlay effects. Falls back gracefully on browsers without support (the element becomes opaque). |
| `clip-path` | `inset()` form, used by reveal effects. |
| `perspective`, `transform-style`, individual 3d transform functions | used by 3d category effects. |
| `@keyframes`, `animation` | used by advanced effects with stepped motion. |
| `::before`, `::after` | used by overlay and composite effects for gradient sweeps and scanlines. |
| `@media (hover: hover)` / `(hover: none)` | desktop-only guard. |
| `@media (prefers-reduced-motion: reduce)` | motion suppression. |
| `@media (prefers-contrast: more)` | focus-ring thickening. |
| `@media (prefers-reduced-transparency: reduce)` | backdrop-filter fallback. |
| `:focus-visible` | keyboard-accessibility mirror of `:hover`. |
| `body:has(...)` | used only by the catalog page's category filter. Supported in Chrome 105+, Edge 105+, Firefox 121+, Safari 15.4+. The catalog page degrades to "all effects" if `:has` is unavailable. |

## What we explicitly do NOT use

| Feature | Why |
|---------|-----|
| `@supports` queries | the contract says one shape, no progressive enhancement. |
| Vendor prefixes (`-webkit-`, `-moz-`, `-ms-`) | the baseline has no need for them. |
| JavaScript of any kind | `CONTRACT.md §1`. |
| CSS Houdini (`@property`, registered custom properties, paint worklets) | not yet in the baseline. |
| Scroll-driven animations (`animation-timeline: view()`) | not yet in the baseline. |

## Reporting a compatibility issue

If an effect breaks in a browser in the matrix above, open an issue with:

1. Browser name and exact version.
2. OS.
3. The effect slug (e.g. `glitch-shift`).
4. A description or screenshot of what's broken.

CI runs the contract validator on every PR; visual regressions need a
human report.

Refs #15
