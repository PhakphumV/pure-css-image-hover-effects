# Contrast Soften

Contrast softens/flattens on hover for a muted look.

**Key CSS**
```css
.contrast-soften {
  overflow: hidden;
  display: inline-block;
  border-radius: 8px;
}
.contrast-soften img {
  display: block;
  width: 100%;
  height: auto;
  filter: contrast(1);
  transition: filter 0.3s ease;
}
.contrast-soften:hover img {
  filter: contrast(0.6);
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `filter` | Chrome 53+, FF 35+, Safari 9+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |

