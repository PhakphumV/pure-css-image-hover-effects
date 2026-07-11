# Liquid Morph

Organic blob shape morphs fluidly over image using animated border-radius on hover.

**Key CSS**
```css
/* Liquid Morph Effect - Organic shape morphing with border-radius animation */

.liquid-morph {
  position: relative;
  display: inline-block;
  overflow: hidden;
  border-radius: 16px;
}

.liquid-morph img {
  display: block;
  width: 100%;
  height: auto;
  transition: transform 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94),
              filter 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94),
              border-radius 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

/* Liquid blob that morphs over the image */
.liquid-morph::before {
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `border-radius` | Chrome 4+, FF 4+, Safari 5+, Edge 12+ |
| `animation` | Check caniuse.com |
| `mix-blend-mode` | Check caniuse.com |
| `keyframes` | Check caniuse.com |
| `clip-path` | Chrome 28+, FF 28+, Safari 9+ |

