# Pure CSS Image Hover Effects

A copy-paste library of pure CSS image hover effects. One class on a
`<div>` that contains an `<img>`. No JavaScript. No build step.

Open [`index.html`](./index.html) to browse the gallery. Click any
card to see a live preview and the HTML and CSS for that effect.

## Status

Zoom category only. More categories will follow the same shape.

## Project layout

    .
    ├── index.html                 # the gallery
    ├── README.md
    └── effects/
        ├── template.html          # canonical effect page template
        ├── template.css           # shared styles for every effect page
        └── zoom/
            ├── zoom.css           # all zoom effect CSS (shared)
            ├── point-zoom.html    # one page per effect
            ├── quick-zoom.html
            ├── zoom-in.html
            └── zoom-out.html

## Adding a new effect

The canonical template is [`effects/template.html`](./effects/template.html).
Every effect page must follow it; the placeholders documented in its
header comment are the only things that change between effects.

1. Copy `effects/template.html` to `effects/<category>/<slug>.html`
   and fill in every `{{...}}` placeholder.
2. Add the effect's CSS to `effects/<category>/<category>.css`,
   scoped to `.hover-effect.<your-slug>` so it does not interfere
   with other effects.
3. Add a card to the matching `<section>` in `index.html`, linking
   to the new page.

## Adding a new category

1. Create `effects/<category>/<category>.css` with the effect CSS.
2. Copy `effects/template.html` once per effect into
   `effects/<category>/` and fill in the placeholders.
3. Link the new category CSS from `index.html` and add a new
   `<section>` with its cards.

## The rule

Every effect must follow this contract:

- One class on a `<div>` (the wrapper). The class is always
  `hover-effect` plus one effect-specific class, e.g. `zoom-in`.
- One `<img>` as the only child of the wrapper.
- No JavaScript.
- No extra HTML elements inside the wrapper beyond the `<img>`.

## CSS framework

The page chrome uses [Pico.css](https://picocss.com/) v2, loaded
from a CDN. Pico provides the semantic styling for `<header>`,
`<main>`, `<footer>`, `<nav>`, `<hgroup>`, and the basic typography
defaults. The effect-specific CSS in `effects/<category>/<category>.css`
is fully self-contained and never overrides Pico's defaults.

The two-column effect page layout is `<div class="grid detail">`:
Pico's `.grid` provides `display: grid`, and the `.detail` modifier
in `effects/template.css` fixes the column count to 2.

## Browser support

Every effect works on the current versions of Chrome, Edge, Firefox,
and Safari. Desktop only.

## Accessibility

Each effect mirrors its `:hover` state onto `:focus-visible`, so
keyboard users see the same affordance. Effects respect
`prefers-reduced-motion: reduce`.
