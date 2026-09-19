# Manual QA Checklist

This checklist covers accessibility and behavior checks that
CI cannot automate. Run it on representative effects after any
contract change. See `ACCESSIBILITY.md` for the full policy.

## Keyboard

- [ ] The wrapper is reachable via Tab when the consumer marks it
      interactive (e.g. `tabindex="0"`, `<button>`, `<a>`).
- [ ] `:focus-visible` produces the same visual transformation
      as `:hover`.
- [ ] The focus outline is visible against busy backgrounds.
- [ ] Focus is not trapped; Tab moves away cleanly.
- [ ] Keyboard users are not dependent on pointer-only behavior.

## Reduced motion (`prefers-reduced-motion: reduce`)

- [ ] The effect shows the resting image under reduced motion.
- [ ] No animation continues; the effect is static.
- [ ] `clip-path` reveal effects show the full image, not a
      clipped portion.
- [ ] `filter` effects (blur, sepia, grayscale) are removed.
- [ ] Opacity defaults are reset to fully visible.

## Touch (`hover: none`)

- [ ] On touch devices, the wrapper shows the resting image
      regardless of tap or focus.
- [ ] The focus outline is preserved for keyboard users on
      hybrid devices.
- [ ] No sticky or lingering hover state on tap.

## Visual and contrast

- [ ] The effect does not obscure essential image content.
- [ ] Color/brightness changes under reduced motion remain
      visible (the effect is still distinct, just non-animated).
- [ ] Heavy overlays (backdrop-filter, blur) do not hide the
      image entirely.

## Reduced transparency (`prefers-reduced-transparency: reduce`)

- [ ] On the catalog page, the sticky filter bar becomes opaque
      (no backdrop-filter).

## Contrast preference (`prefers-contrast: more`)

- [ ] The `:focus-visible` outline thickens to 4px.

## Per-effect spot checks

For each effect being shipped or changed:

- [ ] `:focus-visible` mirror exists in `effect.css`.
- [ ] `alt` attribute is present on the canonical `<img>`.
- [ ] No effect-local `@media (prefers-reduced-motion)` with
      `!important` (would defeat the global reset).
- [ ] No descendant CSS selectors implying extra HTML.
- [ ] No JS state classes (`.is-*`, `.has-*`, `.js-*`).
- [ ] No `@import` or cross-effect CSS references.
- [ ] `meta.json` `css_features` matches what the CSS actually
      uses.

Refs #35
