# Zoom Out

Zoomed-in image pulls back to normal on hover.

**Key CSS**
```css
.zoom-out {
}
.zoom-out img {
  transition: transform .45s ease;
  transform: scale(1.2);
}
.zoom-out:hover img {
  transform: scale(1);
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |

