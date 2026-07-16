# Rectangle Out

Rectangular mask expands outward on hover.

**Key CSS**
```css
.rectangle-out {
}
.rectangle-out img {
}
.rectangle-out::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: white;
  transform: scale(0);
  transform-origin: center;
  transition: transform 0.6s ease;
  pointer-events: none;
  z-index: 1;
}
.rectangle-out:hover::before {
  transform: scale(1.5);
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `pseudo-element` | All modern browsers |
| `clip-path` | Chrome 28+, FF 28+, Safari 9+ |
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |

