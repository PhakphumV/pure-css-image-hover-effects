
# Glow Border

Hovering creates a glowing border around the image.

## Demo

Open the [dedicated page](index.html).

## CSS Code

````css
.glow-border {
  overflow: hidden;
  display: inline-block;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  transition: box-shadow 0.2s ease;
}
.glow-border__img {
  display: block;
  width: 100%;
  height: auto;
  transition: box-shadow 0.4s ease-out;
}
.glow-border:hover .glow-border__img {
  box-shadow: 0 0 20px 4px var(--color-primary, #2563eb);
}
````

## Browser Support

| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| CSS `box-shadow` | 4+ | 4+ | 4+ | 12+ |
| CSS `transition` | 4+ | 4+ | 4+ | 12+ |

View on the dedicated page for the effect.
