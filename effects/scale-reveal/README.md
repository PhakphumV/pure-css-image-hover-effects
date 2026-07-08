
# Scale Reveal

A simple CSS hover effect that smoothly scales an image within a clipped container.

## Demo

Open the [dedicated page](index.html). Hover over the image to see the effect.

## CSS Code

````css
.scale-reveal {
  overflow: hidden;          /* the "window" */
  display: inline-block;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  transition: box-shadow 0.2s ease;
}
.scale-reveal__img {
  display: block;
  width: 100%;
  height: auto;
  transition: transform 0.4s ease-out;
}
.scale-reveal:hover .scale-reveal__img {
  transform: scale(1.15);        /* zoom in */
}
````

## Browser Support

| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| CSS `transform` | 36+ | 16+ | 9+ | 12+ |
| CSS `transition` | 36+ | 16+ | 9+ | 12+ |

> All code is valid in evergreen browsers.
