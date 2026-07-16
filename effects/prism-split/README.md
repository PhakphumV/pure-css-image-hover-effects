# Prism Split

RGB channels separate like light through a prism on hover with spectral bands.

**Key CSS**
```css
/* Prism Split Effect - RGB channel separation like light through a prism */

.prism-split {
}

.prism-split img {
  transition: transform 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94),
              filter 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

/* Three RGB channels as layered elements */
.prism-split::before,
.prism-split::after,
.prism-split .channel {
  content: '';
  position: absolute;
  inset: 0;
  background: inherit;
  background-size: cover;
  background-position: center;
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `mix-blend-mode` | Chrome 41+, FF 32+, Safari 8+ |
| `filter` | Chrome 53+, FF 35+, Safari 9+ |
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `clip-path` | Chrome 28+, FF 28+, Safari 9+ |
| `animation` | Chrome 43+, FF 16+, Safari 9+ |

