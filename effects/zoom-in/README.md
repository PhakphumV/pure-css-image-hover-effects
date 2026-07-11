# Zoom In

Simple smooth zoom-in on hover.

**Key CSS**
```css
.zoom-in {
  overflow: hidden;
  display: inline-block;
  border-radius: 8px;
}
.zoom-in img {
  transition: transform .45s ease;
}
.zoom-in:hover img {
  transform: scale(1.18);
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |

