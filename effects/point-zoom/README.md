# Point Zoom

Image zooms toward cursor position on hover.

**Key CSS**
```css
.point-zoom {
}
.point-zoom img {
  transform-origin: 65% 75%;
  transition: transform 1s, filter 0.5s ease-out;
}
.point-zoom:hover img {
  transform: scale(5);
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `transform-origin` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |

