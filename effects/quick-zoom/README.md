# Quick Zoom

Fast zoom-in effect on hover with short transition.

**Key CSS**
```css
.quick-zoom {
  overflow: hidden;
  display: inline-block;
  border-radius: 8px;
}
.quick-zoom img {
  transform-origin: 0 0;
  transition: transform 0.25s, visibility 0.25s ease-in;
}
.quick-zoom:hover img {
  transform: scale(2);
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |

