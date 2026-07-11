# Duotone Shift

Duotone filter transitions to normal color on hover.

**Key CSS**
```css
.duotone {
  overflow: hidden;
  display: inline-block;
  border-radius: 8px;
}
.duotone img {
  display: block;
  width: 100%;
  height: auto;
  filter: grayscale(1) contrast(1.2) sepia(1) hue-rotate(180deg) saturate(5);
  transition: filter 0.4s ease-out, transform 0.4s ease-out;
}
.duotone:hover img {
  filter: grayscale(0) contrast(1) sepia(0) hue-rotate(0) saturate(1);
  transform: scale(1.05);
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `filter` | Chrome 53+, FF 35+, Safari 9+ |
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |

