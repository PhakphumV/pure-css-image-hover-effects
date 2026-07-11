# Radial In

Image reveals from center outward using circular mask on hover.

**Key CSS**
```css
.radial-in {
  overflow: hidden;
  display: inline-block;
  border-radius: 8px;
  position: relative;
}
.radial-in img {
  display: block;
  width: 100%;
  height: auto;
}
.radial-in::before {
  content: '';
  position: absolute;
  top: 50%; left: 50%;
  width: 100%; height: 100%;
  background: white;
  border-radius: 50%;
  transform: translate(-50%, -50%) scale(1.5);
  transform-origin: center;
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `pseudo-element` | All modern browsers |
| `border-radius` | Chrome 4+, FF 4+, Safari 5+, Edge 12+ |
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |

