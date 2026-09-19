# Pure CSS Image Hover Effects

A copy-paste library of **54 pure CSS image hover effects**.
One class on a `<div>` that contains an `<img>`.
No JavaScript. No build step. No dependencies.

Open [`index.html`](./index.html) in any modern desktop browser to browse
the gallery. Click any effect card to reveal the HTML and CSS, then
select the code and copy with `Ctrl+C` (or `Cmd+C` on Mac).

## How to use

1. Open `index.html` and pick an effect from the gallery.
2. Click the card to expand it.
3. Copy the HTML into your page and the CSS into your stylesheet.

That is it. Each effect is self-contained: one CSS class added to a
wrapper `<div>`, one `<img>` inside it, and a small block of CSS rules.

### Minimal example

```html
<div class="hover-effect zoom-in">
  <img src="your-image.jpg" alt="description">
</div>
```

```css
.hover-effect.zoom-in > img {
  transition: transform 0.3s ease;
}

.hover-effect.zoom-in:hover > img {
  transform: scale(1.1);
}
```

## The rule

Every effect in this library follows the same contract:

- **One class** on a `<div>` (the wrapper). The class is always
  `hover-effect` plus one effect-specific class, e.g. `zoom-in`.
- **One `<img>`** as the only child of the wrapper.
- **No JavaScript.** All animation and interaction is pure CSS using
  `:hover`, `:focus-visible`, and pseudo-elements (`::before`,
  `::after`).
- **No extra HTML elements.** No inner `<div>`s, `<span>`s, or other
  wrappers beyond the `<img>`.

## Categories

| Category | Count | What it does |
|----------|------:|--------------|
| 3D | 7 | perspective, flips, tilts |
| Composite | 3 | combinations of multiple techniques |
| Distortion | 1 | morphing shapes |
| Fade | 1 | opacity transitions |
| Filter | 7 | blur, contrast, grayscale, hue, saturate |
| Light | 5 | shine sweeps, glows, holographic shimmer |
| Overlay | 10 | reveals, masks, wipes |
| Pan | 5 | directional motion |
| Reveal | 6 | clip-path, glitch, slice |
| Shadow | 4 | drop, lift, glow |
| Zoom | 5 | scale, dolly, magnify |

## Browser support

Every effect works on the current versions of:

- Chrome and Edge (Chromium)
- Firefox
- Safari

Desktop only. Mobile and tablet are not in scope because most effects
rely on hover, which is not reliably available on touch devices.
Effects may still display on touch screens, but the interactive state
will not trigger.

## Accessibility

Each effect mirrors its `:hover` state onto `:focus-visible`, so
keyboard users get the same affordance as mouse users. Effects also
respect `prefers-reduced-motion: reduce` by disabling transitions
and transforms.

## For learners

If you are new to CSS, this library is meant to be read. Pick an
effect that looks interesting, copy its CSS into your project, then
tweak one property at a time to see what it does. Hover effects are
a great way to learn:

- `transform` (translate, scale, rotate, skew)
- `filter` (blur, contrast, hue-rotate, saturate)
- `clip-path` (inset, polygon, circle)
- `transition` and `animation`
- pseudo-elements `::before` and `::after`
