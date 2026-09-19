# Pure CSS Image Hover Effects

A copy-paste library of pure CSS image hover effects. One class on a
`<div>` that contains an `<img>`. No JavaScript. No build step.

Open [`index.html`](./index.html) to browse the gallery. Click any
card to see a live preview and the HTML and CSS for that effect.

## Status

This is the **zoom category** only. More categories will be added
in the same shape.

## Project layout

```
.
├── index.html                # the gallery (entry point)
├── README.md                 # this file
└── effects/
    └── zoom/
        ├── zoom.css          # all zoom effect CSS (shared)
        ├── point-zoom.html   # one page per effect (preview + code)
        ├── quick-zoom.html
        ├── slide-reveal.html
        ├── zoom-in.html
        └── zoom-out.html
```

## Adding a new effect

1. **Create the HTML page** at `effects/<category>/<slug>.html`.
   Use any existing effect page (e.g. `effects/zoom/zoom-in.html`)
   as the template. Change the title, description, slug class, and
   seed.
2. **Add the CSS** to `effects/<category>/<category>.css`. The
   selectors must be scoped to `.hover-effect.<your-slug>` so they
   do not interfere with other effects.
3. **Add a card** to `index.html` inside the matching category
   `<section>`, linking to the new page.

## Adding a new category

1. Create `effects/<category>/<category>.css` with the category's
   effect CSS.
2. Create one HTML file per effect inside `effects/<category>/`,
   following the zoom template.
3. Add a `<link>` to the new category CSS in `index.html` and add a
   new `<section>` with the category's cards.

## The rule

Every effect must follow this contract:

- One class on a `<div>` (the wrapper). The class is always
  `hover-effect` plus one effect-specific class, e.g. `zoom-in`.
- One `<img>` as the only child of the wrapper.
- No JavaScript. Animation and interaction are pure CSS using
  `:hover`, `:focus-visible`, and pseudo-elements (`::before`,
  `::after`).
- No extra HTML elements inside the wrapper beyond the `<img>`.

## CSS framework

The page chrome uses [Pico.css](https://picocss.com/) v2, a
classless semantic framework loaded from a CDN. Pico handles
typography, links, headings, code blocks, and form controls. The
effects' own CSS lives in `effects/<category>/<category>.css` and
is fully self-contained.

## Browser support

Every effect works on the current versions of Chrome, Edge, Firefox,
and Safari. Desktop only.

## Accessibility

Each effect mirrors its `:hover` state onto `:focus-visible`, so
keyboard users see the same affordance. Effects respect
`prefers-reduced-motion: reduce`.
