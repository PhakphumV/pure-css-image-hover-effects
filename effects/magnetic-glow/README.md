# Magnetic Glow

Glowing ring follows cursor with magnetic attraction on hover (JS-enhanced).

**Key CSS**
```css
/* Magnetic Glow Effect - Glowing ring follows cursor with magnetic attraction */

.magnetic-glow {
}

.magnetic-glow img {
  transition: transform 0.3s ease-out, filter 0.3s ease-out;
}

/* Magnetic glow ring */
.magnetic-glow::before {
  content: '';
  position: absolute;
  inset: -8px;
  border-radius: 16px;
  box-shadow: 
    0 0 20px 4px rgba(37, 99, 235, 0),
    0 0 40px 8px rgba(37, 99, 235, 0),
    inset 0 0 20px 4px rgba(37, 99, 235, 0);
  opacity: 0;
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `box-shadow` | Chrome 10+, FF 4+, Safari 5.1+, Edge 12+ |
| `pseudo-element` | All modern browsers |

