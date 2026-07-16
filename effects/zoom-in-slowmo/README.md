# Zoom In Slowmo

Dramatic slow-motion zoom with brightness shift on hover.

**Key CSS**
```css
.zoom-in-slowmo {
}
.zoom-in-slowmo img {
  transform-origin: 50% 65%;
  transition: transform 5s, filter 3s ease-in-out;
  filter: brightness(150%);
}
.zoom-in-slowmo:hover img {
  filter: brightness(100%);
  transform: scale(3);
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `filter` | Chrome 53+, FF 35+, Safari 9+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `transform-origin` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |

