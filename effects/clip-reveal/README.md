# Clip Reveal

Image reveals through animated clip-path on hover.

**Key CSS**
```css
.clip-reveal {
  overflow: hidden;
  display: inline-block;
  border-radius: 8px;
}
.clip-reveal img {
  display: block;
  width: 100%;
  height: auto;
  clip-path: inset(0 50% 0 50%);
  transition: clip-path 0.5s ease-out, transform 0.5s ease-out;
}
.clip-reveal:hover img {
  clip-path: inset(0 0 0 0);
  transform: scale(1.1);
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `clip-path` | Chrome 28+, FF 28+, Safari 9+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |

