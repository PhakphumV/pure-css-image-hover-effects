# Vignette

Vignette effect fades in on hover, darkening edges.

**Key CSS**
```css
.vignette {
  overflow: hidden;
  display: inline-block;
  border-radius: 8px;
  position: relative;
}
.vignette img {
  display: block;
  width: 100%;
  height: auto;
  transition: transform 0.4s ease-out;
}
.vignette::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,0.6) 100%);
  opacity: 0;
  transition: opacity 0.4s ease-out;
  pointer-events: none;
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `box-shadow` | Chrome 10+, FF 4+, Safari 5.1+, Edge 12+ |
| `pseudo-element` | All modern browsers |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |

