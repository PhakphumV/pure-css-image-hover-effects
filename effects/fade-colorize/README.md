# Fade to Color

Grayscale image transitions to full color on hover.

**Key CSS**
```css
.fade-colorize {
  overflow: hidden;
  display: inline-block;
  border-radius: 8px;
}
.fade-colorize img {
  display: block;
  width: 100%;
  height: auto;
  filter: grayscale(1);
  transition: filter 0.4s ease-out, transform 0.4s ease-out;
}
.fade-colorize:hover img {
  filter: grayscale(0);
  transform: scale(1.05);
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `filter` | Chrome 53+, FF 35+, Safari 9+ |
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |

