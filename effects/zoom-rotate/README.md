# Zoom Rotate

Image zooms and slightly rotates on hover.

**Key CSS**
```css
/* Zoom Rotate Effect */

.zoom-rotate img {
  transition: transform 0.5s cubic-bezier(0.22, 1, 0.36, 1);
}

.zoom-rotate:hover img {
  transform: scale(1.2) rotate(3deg);
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `cubic-bezier` | Chrome 4+, FF 4+, Safari 3.1+, Edge 12+ |

