# Sepia In

Image starts sepia-toned, turns to full color on hover.

**Key CSS**
```css
.sepia-in {
}
.sepia-in img {
  filter: sepia(1);
  transition: filter 0.5s ease;
}
.sepia-in:hover img {
  filter: sepia(0);
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `filter` | Chrome 53+, FF 35+, Safari 9+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |

