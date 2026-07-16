# Horizontal Zoom & Pan

Image zooms and pans horizontally on hover.

**Key CSS**
```css
/* Horizontal Zoom & Pan Effect */

.horizontal-zoom-n-pan {
  overflow: hidden; /* Required for the pan effect to clip */
}

.horizontal-zoom-n-pan img {
  transform-origin: 0 center;
  transition: transform 0.55s ease-in-out;
  will-change: transform;
  transform: scale(1.4);
}

.horizontal-zoom-n-pan:hover img {
  transform: scale(1.5) translateX(-30%);
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `transform-origin` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |

