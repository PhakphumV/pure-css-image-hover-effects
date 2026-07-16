# Blur to Sharp

Blurred grayscale image sharpens to full color on hover.

**Key CSS**
```css
/* Blur to Sharp Effect */

.blur-sharpen img {
  filter: blur(4px) grayscale(0.5);
  transition: filter 0.4s ease-out, transform 0.4s ease-out;
}

.blur-sharpen:hover img {
  filter: blur(0) grayscale(0);
  transform: scale(1.05);
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `filter` | Chrome 53+, FF 35+, Safari 9+ |
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |

