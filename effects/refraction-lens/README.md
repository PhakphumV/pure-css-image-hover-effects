# Refraction Lens

Magnifying lens effect with gradient overlay that scales on hover.

**Key CSS**
```css
/* Refraction Lens Effect */

.refraction-lens {
}

.refraction-lens::after {
  content: "";
  position: absolute;
  border-radius: 50%;
  width: 120px; height: 120px;
  background: linear-gradient(rgba(255,255,255,0.8), transparent);
  transform: translate(-50%, -50%) scale(1);
  pointer-events: none;
  transition: transform .3s;
}

.refraction-lens:hover::after {
  transform: translate(-50%, -50%) scale(1.5);
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `pseudo-element` | All modern browsers |
| `border-radius` | Chrome 4+, FF 4+, Safari 5+, Edge 12+ |
| `background-gradient` | Chrome 10+, FF 3.6+, Safari 4+, Edge 12+ |
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |

