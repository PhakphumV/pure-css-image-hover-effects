# Horizontal Zoom & Pan

Image zooms and pans horizontally on hover.

**Key CSS**
```css
.horizontal-zoom-n-pan {
  overflow: hidden;
  display: inline-block;
  border-radius: 12px;
  max-width: 100%;
}

.horizontal-zoom-n-pan img {
  display: block;
  width: 100%;
  height: auto;
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

