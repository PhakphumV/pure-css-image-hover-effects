# Corner Frame

Animated corner brackets draw in from edges to frame the image on hover.

**Key CSS**
```css
/* Corner Frame Effect - Camera-style corner brackets snap into place */

.corner-frame {
  position: relative;
  overflow: visible;
  padding: 10px;
}

.corner-frame img {
  transition: transform 0.35s ease-out;
}

.corner-frame::before,
.corner-frame::after {
  content: '';
  position: absolute;
  width: 22px;
  height: 22px;
  border-color: var(--color-primary, #2563eb);
  border-style: solid;
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `pseudo-element` | All modern browsers |
| `clip-path` | Chrome 28+, FF 28+, Safari 9+ |

