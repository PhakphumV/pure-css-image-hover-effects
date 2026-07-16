# Glow Border

Glowing border animation appears around image on hover.

**Key CSS**
```css
/* Glow Border Effect */

.glow-border {
  overflow: visible; /* Allow box-shadow to extend beyond container */
  transition: box-shadow 0.3s ease-in-out;
}

.glow-border img {
  /* Image styling handled by base.css */
}

.glow-border:hover {
  box-shadow: 0 0 20px 4px #2563eb;
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `box-shadow` | Chrome 10+, FF 4+, Safari 5.1+, Edge 12+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `pseudo-element` | All modern browsers |

