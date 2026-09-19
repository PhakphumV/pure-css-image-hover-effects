# Accessibility baseline

Every effect in this library honors four accessibility media queries,
enforced globally in `styles/base.css`:

## `prefers-reduced-motion: reduce` (CONTRACT.md §4)

When the user has requested reduced motion (OS-level setting), all
hover effects collapse to static. Specifically, on `.hover-effect` and
its child `<img>`, the following are forcibly set to their resting
values:

- `transition: none`
- `animation: none`
- `transform: none`
- `clip-path: none` (so reveal effects show the full image, not a half-clipped one)
- `filter: none` (so blur/sepia/grayscale defaults are removed)
- `opacity: 1` (so any fade-to-lower-opacity default is reset)

The reset is global — individual effects MUST NOT override it.

## `prefers-contrast: more`

When the user requests higher contrast (Windows High Contrast, forced
colors mode), the `:focus-visible` outline thickens from 3px to 4px
so keyboard focus remains visible against busy backgrounds.

## `prefers-reduced-transparency: reduce`

The catalog page (`styles/catalog.css`) uses `backdrop-filter: blur()`
on its sticky category filter bar. Users who request reduced
transparency get a solid `var(--color-bg)` fill instead, with no
blur — the bar is still legible, just opaque.

## `:focus-visible` (CONTRACT.md §5)

Every hover state is mirrored on `:focus-visible` so keyboard users
get the same affordance. The focus ring is `outline: 3px solid
var(--color-primary)` with `outline-offset: 2px`. Under
`prefers-contrast: more`, this thickens to 4px.

The default browser focus ring is preserved where present; we never
use `outline: none` without a replacement.

## What this does NOT cover

- Screen reader announcements — the library does not add ARIA because
  hover effects are decorative. Images should always carry meaningful
  `alt` text in the host page.
- Keyboard activation order — the host page is responsible for tab
  order. We add `tabindex="0"` to each demo wrapper so the focus
  state is reachable, but we do not rearrange the page.

Refs #14
