# Accessibility baseline

This document is the authoritative accessibility model for the
v2 library. It reconciles `CONTRACT.md`, `styles/base.css`, the
metadata schema, and the validator. Issues #32, #33, and #34
established the contract; #35 establishes how that contract is
honored for users with diverse needs and devices.

## 01. Accessibility goals

The library aims to be:

- **Usable with a keyboard** for any consumer who makes the wrapper
  focusable.
- **Usable with reduced motion** without losing essential visual
  information.
- **Usable on touch devices** without sticky or confusing states.
- **Transparent** about which claims the library can make and which
  are the consumer's responsibility.
- **Not exploitative** of transient visual changes to communicate
  essential information that should be available without hover.

The library does **not** claim universal WCAG compliance for the
consumer's page; it claims a defined baseline for the effect itself.

## 02. Canonical HTML

Every effect is consumed as:

```html
<div class="hover-effect EFFECT-SLUG">
  <img src="image.jpg" alt="Description">
</div>
```

The wrapper is a plain `<div>`. It has no `tabindex`, no `role`, no
ARIA. The `<img>` carries meaningful `alt` text supplied by the
consumer.

## 03. Focus and `:focus-visible` policy

The library uses `:focus-visible` (not `:focus`) so that mouse
clicks do not leave a focus ring, while keyboard tabbing does.

Every effect's `effect.css` MUST mirror its `:hover` state to
`:focus-visible`:

```css
.hover-effect.<slug>:hover > img,
.hover-effect.<slug>:focus-visible > img {
  /* the visual transformation */
}
```

This is enforced by `scripts/validate_effects.py` (see §11).

The `:focus-visible` outline ring is provided globally in
`styles/base.css`:

- Default: `outline: 3px solid var(--color-primary)` with
  `outline-offset: 2px`.
- Under `prefers-contrast: more`: thickened to 4px.

The library never uses `outline: none` without a replacement.

## 04. Consumer responsibility for focusability

Whether the wrapper is focusable is the **consumer's** decision, not
the library's. The consumer chooses between:

- **Decorative**: no `tabindex`; the wrapper is presentational and
  not in the tab order.
- **Interactive**: the consumer adds `tabindex="0"` (or wraps the
  effect in a `<button>` or `<a>`) so keyboard users can reach it.

The per-effect demo pages in this repository intentionally omit
`tabindex="0"` from the canonical example. The demo's preview panel
keeps `tabindex="0"` as a convenience for keyboard users testing
the effect in isolation.

If the consumer wraps the effect in a `<button>` or `<a>`, the
`:focus-visible` ring naturally appears on that wrapper instead of
the `.hover-effect` div. The library's ring still applies to the
inner `.hover-effect` when it itself receives focus.

## 05. Hover versus keyboard behavior

When the wrapper is focusable, `:focus-visible` produces the same
visual transformation as `:hover`. Keyboard users therefore see
the full effect, not a degraded version.

When the wrapper is decorative (no focus), the visual effect is
hover-only. This is acceptable for purely decorative effects. The
library does not require every effect to be focusable.

## 06. Reduced-motion policy

The library uses one repository-wide rule, enforced globally in
`styles/base.css` under `@media (prefers-reduced-motion: reduce)`:

When the user has requested reduced motion, the following are
forcibly set on `.hover-effect`, `.hover-effect > img`, and the
hover/focus-visible states:

- `transition: none`
- `animation: none`
- `transform: none`
- `clip-path: none` (so reveal effects show the full image)
- `filter: none` (so blur/sepia defaults are removed)
- `opacity: 1` (so fade-to-lower defaults are reset)

Color and brightness changes that do not create motion are NOT
suppressed — the effect is still visually distinct, it simply does
not animate.

**Effects MUST NOT redefine this media query with `!important`**.
The validator (`check_reduced_motion` in
`scripts/validate_effects.py`) flags any effect that does.

## 07. Touch and coarse-pointer behavior

Hover has no universal equivalent on touch devices. The library
treats touch devices as a separate interaction model:

- Under `@media (hover: none)`, `styles/base.css` suppresses the
  hover and focus-visible visual effects so the resting state is
  always shown.
- The `:focus-visible` outline is preserved so keyboard users on
  hybrid devices still see focus indication.
- The catalog page (which has its own filter bar) gets the same
  treatment for its backdrop-filter under
  `prefers-reduced-transparency: reduce`.

Coarse pointers (`@media (pointer: coarse)`) are not given
special treatment: the same `@media (hover: none)` guard already
covers tablets and phones. The consumer can add pointer-specific
overrides if their use case requires them.

## 08. Contrast and overlay considerations

Some effects substantially alter brightness, contrast, color,
opacity, or overlays. The library does **not** claim that every
visual effect guarantees WCAG contrast compliance because the
underlying image and background are consumer-controlled.

Guidelines for consumers using high-contrast effects:

- Do not rely on a transient hover state to communicate essential
  information that must be available without hover.
- Where an effect obscures the image (heavy `filter: blur`,
  heavy `backdrop-filter`, low-opacity overlays), provide a
  non-hover means to access the same information.
- The `:focus-visible` state is the keyboard user's equivalent to
  hover; do not make it visually weaker than `:hover`.

## 09. Other user-preference media queries

| Feature | Status |
|---------|--------|
| `prefers-reduced-motion: reduce` | Supported globally (§6) |
| `prefers-contrast: more` | Supported globally (thicker outline) |
| `prefers-reduced-transparency: reduce` | Supported globally on catalog (§7) |
| `@media (hover: none)` | Supported globally (§7) |
| `forced-colors` (Windows High Contrast) | Consumer responsibility. The default browser focus ring works. |
| `pointer: coarse` | Consumer responsibility. The hover:none guard already covers touch. |

The library intentionally does not add speculative CSS for
preference features that are not needed.

## 10. Gallery and demo behavior

The catalog page (`index.html`) may add interactive navigation
(filtering, code display, demo controls). These are gallery concerns,
not effect concerns. The catalog must not become a hidden
prerequisite for any effect's accessibility behavior.

The per-effect `index.html` demo page mirrors the wrapper in a
`.preview-container`. The demo's preview panel may include
`tabindex="0"` as a testing convenience. Real consumers should
follow §04.

## 11. Automated validation

`scripts/validate_effects.py` enforces the machine-checkable parts
of this document:

- `:focus-visible` mirror exists in every `effect.css`.
- `alt` attribute is present on the canonical `<img>`.
- No effect redefines `@media (prefers-reduced-motion: reduce)`
  with `!important`.
- `meta.json` does not claim CSS features the CSS does not use.

`scripts/validate_effects.py --check-fixtures` runs the validator
against `tests/fixtures/{positive,negative}/*` to prevent silent
regression.

`styles/base.css` itself is checked to contain the
`@media (hover: none)` guard (a repo-level invariant).

## 12. Manual QA checklist

See `QA_CHECKLIST.md` for the full keyboard, reduced-motion,
touch, and visual checklist that CI cannot automate.

## 13. Known limitations

- The library does not add ARIA. Effects are decorative by default;
  consumers add ARIA when the effect conveys semantic meaning.
- The library does not manage keyboard activation order. Consumers
  control tab order on their page.
- The library does not enforce image alt-text quality; the
  validator only checks that `alt` is present.
- The library does not test visual aesthetics. Manual review is
  required for effects that significantly alter the image's
  appearance.

Refs #35
