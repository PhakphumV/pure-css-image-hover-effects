
# Slide Reveal

A hover effect that slides the image to the left while scaling it up.

## Demo

Open the [dedicated page](index.html). Hover over the image to see the effect.

## CSS Code

````css
.slide-reveal {
  overflow: hidden;
  display: inline-block;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  transition: box-shadow 0.2s ease;
}
.slide-reveal__img {
  display: block;
  width: 100%;
  height: auto;
  transition: transform 0.4s ease-out;
}
.slide-reveal:hover .slide-reveal__img {
  transform: translateX(-15%) scale(1.15);
}
````

## Browser Support

| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| CSS `transform` | 36+ | 16+ | 9+ | 12+ |
| CSS `transition` | 36+ | 16+ | 9+ | 12+ |

Access the dedicated page for the demo.
