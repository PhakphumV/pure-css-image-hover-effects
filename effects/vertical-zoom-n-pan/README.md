# Vertical Zoom & Pan

Image zooms and pans vertically on hover.

**Key CSS**
```css
.vertical-zoom-n-pan {
  max-width: 100%;
}

.vertical-zoom-n-pan img {
  transform-origin: center 0;
  transition: transform 0.55s ease-in-out;
  will-change: transform;
  transform: scale(1.4);
}

.vertical-zoom-n-pan:hover img {
  transform: scale(1.5) translateY(-30%);
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `transform-origin` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |

