# Slide Reveal

Image slides to reveal content on hover.

**Key CSS**
```css
/* placeholder */
.slide-reveal {
  overflow: hidden;
  display: inline-block;
  border-radius: 8px;
}
.slide-reveal img {
  display: block;
  width: 0;
  height: 100%;
  transition: width 0.4s ease-out;
}
.slide-reveal:hover img {
  width: 100%;
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `overflow` | All modern browsers |

