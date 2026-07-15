# Contrast Punch

Contrast increases sharply on hover for a punchy look.

**Key CSS**
```css
.contrast-punch {
  overflow: hidden;
  display: inline-block;
  border-radius: 8px;
}
.contrast-punch img {
  display: block;
  width: 100%;
  height: auto;
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

