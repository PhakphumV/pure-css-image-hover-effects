# Effect Contract

Every effect in this library **must** satisfy every clause below. The
automated validator (`scripts/validate_effects.py`) enforces these rules in
CI. An effect that breaks the contract is removed or rewritten, not
grandfathered.

## 1. Pure CSS only — zero JavaScript

- No `<script>` tags, no inline event handlers (`onclick`, `onmouseover`, …),
  no `javascript:` URLs.
- No JavaScript files loaded by the effect's `index.html`.
- No CSS `url(...)` pointing to `.js` files.
- Interactive state (hover, focus) is driven by CSS pseudo‑classes only
  (`:hover`, `:focus-visible`).

## 2. Class applied to a `<div>` container

- The user copies exactly one class onto a `<div>` wrapper:
  ```html
  <div class="hover-effect zoom-in">
    <img src="photo.jpg" alt="">
  </div>
  ```
- The effect's own `effect.css` targets `.zoom-in` (the wrapper) and
  `.zoom-in img` (the child image).
- No class may be required on the `<img>` itself; no extra wrapper elements
  (`<span>`, `<figure>`) may be required.

## 3. Works on the majority of desktop browsers

Target baseline (see `BROWSER_SUPPORT.md` for the full matrix):

- Chrome / Edge (last 2 stable versions)
- Firefox (last 2 stable versions)
- Safari (last 2 stable versions)

Mobile and tablet hover are **out of scope**: the `@media (hover: hover)`
guard in `styles/base.css` intentionally suppresses hover effects on
touch‑only devices. This is not a contract violation — it is the contract.

## 4. Respects user motion preferences

- All transitions and transforms must be suppressed when
  `@media (prefers-reduced-motion: reduce)` matches.
- The suppression lives in `styles/base.css` and applies globally; individual
  effects do **not** opt out.

## 5. Keyboard accessible

- The hover state must be mirrored on `:focus-visible` so keyboard users see
  the same affordance when the wrapper is focusable.
- Focus rings must be visible (the default browser ring is acceptable; do not
  suppress it with `outline: none` without a replacement).
- Whether the wrapper is focusable is the consumer's decision
  (see `ACCESSIBILITY.md` §04). The library does not force
  `tabindex="0"`. The `:focus-visible` mirror works whenever the
  consumer makes the wrapper reachable via keyboard.

## 6. Self‑contained

- Each effect directory contains exactly three files: `effect.css`,
  `index.html`, `meta.json`.
- No effect may depend on another effect's CSS or HTML.
- The only shared stylesheet is `styles/base.css`, which is owned by the
  library, not by any individual effect.

## 7. Touch devices

On devices that cannot hover (`@media (hover: none)`),
`styles/base.css` suppresses the visual hover and focus-visible
effects. The wrapper is still keyboard-focusable if the consumer
adds a focus mechanism.


## What the contract forbids (cheat sheet)

| Forbidden | Why |
|-----------|-----|
| `<script>` in `index.html` | Violates §1 |
| Class on `<img>` instead of `<div>` | Violates §2 |
| Extra `<span>` wrapper required | Violates §2 |
| Effect breaks in Firefox | Violates §3 |
| Effect animates under reduced‑motion | Violates §4 |
| `outline: none` without replacement | Violates §5 |
| Importing another effect's CSS | Violates §6 |
