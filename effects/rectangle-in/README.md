# Rectangle In

Rectangular mask reveals image from center on hover.

**Key CSS**
```css
.rectangle-in {
  overflow: hidden;
  display: inline-block;
  border-radius: 8px;
  position: relative;
}
.rectangle-in img {
  display: block;
  width: 100%;
  height: auto;
}
.rectangle-in::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: white;
  transform: scale(1.5);
  transform-origin: center;
  transition: transform 0.6s ease;
  pointer-events: none;
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `pseudo-element` | All modern browsers |
| `clip-path` | Chrome 28+, FF 28+, Safari 9+ |
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |

