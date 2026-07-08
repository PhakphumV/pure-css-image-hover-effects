
# Fade Colorize

Hovering fades a grayscale image back to color and slightly zooms it.

## Demo

Open the [dedicated page](index.html). Hover to see the transition.

## CSS Code

````css
.fade-colorize {
  overflow: hidden;
  display: inline-block;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  transition: box-shadow 0.2s ease;
}
.fade-colorize__img {
  display: block;
  width: 100%;
  height: auto;
  filter: grayscale(1);
  transition: filter 0.4s ease-out, transform 0.4s ease-out;
}
.fade-colorize:hover .fade-colorize__img {
  filter: grayscale(0);
  transform: scale(1.05);
}
````

## Browser Support

| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| CSS `filter` | 53+ | 35+ | 9+ | 12+ |
| CSS `transform` | 36+ | 16+ | 9+ | 12+ |

Run the demo on the dedicated page.
