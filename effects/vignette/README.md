# Vignette

Vignette effect fades in on hover, darkening edges.

**Key CSS**
```css
/* Vignette Effect */

.vignette {
  position: relative;
}

.vignette img {
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
  border-radius: var(--radius);
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `box-shadow` | Chrome 10+, FF 4+, Safari 5.1+, Edge 12+ |
| `pseudo-element` | All modern browsers |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |

