
# Rotate 3D

Hovering applies a 3D rotation with perspective, creating a subtle depth effect.

## Demo

Open the [dedicated page](index.html).

## CSS Code

````css
.rotate-3d {
  overflow: hidden;
  display: inline-block;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  transition: box-shadow 0.2s ease;
  perspective: 1000px;
}
.rotate-3d__img {
  display: block;
  width: 100%;
  height: auto;
  transition: transform 0.5s ease-out;
  transform-style: preserve-3d;
}
.rotate-3d:hover .rotate-3d__img {
  transform: rotateY(15deg) rotateX(-5deg) scale(1.1);
}
````

## Browser Support

| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| CSS `perspective` | 12+ | 12+ | 7+ | 12+ |
| CSS `transform-style` | 12+ | 12+ | 7+ | 12+ |
| CSS `transform` | 12+ | 12+ | 7+ | 12+ |

Check the effect on the dedicated page.
