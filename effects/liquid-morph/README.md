# Liquid Morph

Organic blob shape morphs fluidly over image using animated border-radius on hover.

**Key CSS**
```css
/* Liquid Morph Effect - Organic shape morphing with border-radius animation */

.liquid-morph {
  position: relative;
  overflow: visible; /* Allow pseudo-elements to extend */
}

.liquid-morph img {
  transition: 
    transform 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94),
    filter 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94),
    border-radius 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

/* Liquid blob that morphs over the image */
.liquid-morph::before {
  content: '';
  position: absolute;
  inset: -30%;
  background: inherit;
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `border-radius` | Chrome 4+, FF 4+, Safari 5+, Edge 12+ |
| `animation` | Chrome 43+, FF 16+, Safari 9+ |
| `mix-blend-mode` | Chrome 41+, FF 32+, Safari 8+ |
| `keyframes` | Chrome 43+, FF 16+, Safari 9+ |
| `clip-path` | Chrome 28+, FF 28+, Safari 9+ |

