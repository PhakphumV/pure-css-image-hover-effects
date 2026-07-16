# Contrast Punch

Contrast increases sharply on hover for a punchy look.

**Key CSS**
```css
/* Contrast Punch Effect */

.contrast-punch img {
  filter: contrast(1);
  transition: filter 0.3s ease;
}

.contrast-punch:hover img {
  filter: contrast(1.5);
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `filter` | Chrome 53+, FF 35+, Safari 9+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |

