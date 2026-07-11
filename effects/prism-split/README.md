# Prism Split

RGB channels separate like light through a prism on hover with spectral bands.

**Key CSS**
```css
/* Prism Split Effect - RGB channel separation like light through a prism */

.prism-split {
  position: relative;
  display: inline-block;
  overflow: hidden;
  border-radius: 8px;
}

.prism-split img {
  display: block;
  width: 100%;
  height: auto;
  transition: transform 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94),
              filter 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

/* Three RGB channels as layered elements */
.prism-split::before,
.prism-split::after,
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `mix-blend-mode` | Check caniuse.com |
| `filter` | Chrome 53+, FF 35+, Safari 9+ |
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `clip-path` | Chrome 28+, FF 28+, Safari 9+ |
| `animation` | Check caniuse.com |

