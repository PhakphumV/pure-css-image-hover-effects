# Fade to Color

Grayscale image transitions to full color on hover.

**Key CSS**
```css
/* Fade Colorize Effect */

.fade-colorize img {
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

