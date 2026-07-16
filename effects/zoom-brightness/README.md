# Zoom Brightness

Image zooms and brightens from dimmed state on hover.

**Key CSS**
```css
.zoom-brightness {
}
.zoom-brightness img {
  transition: transform 2s, filter 1.5s ease-in-out;
  transform-origin: center center;
  filter: brightness(50%);
}
.zoom-brightness:hover img {
  filter: brightness(100%);
  transform: scale(1.3);
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `filter` | Chrome 53+, FF 35+, Safari 9+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |

