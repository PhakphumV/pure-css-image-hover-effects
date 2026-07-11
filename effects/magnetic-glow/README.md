# Magnetic Glow

Glowing ring follows cursor with magnetic attraction on hover (JS-enhanced).

**Key CSS**
```css
/* Magnetic Glow Effect - Glowing ring follows cursor with magnetic attraction */

.magnetic-glow {
  position: relative;
  display: inline-block;
  overflow: hidden;
  border-radius: 12px;
}

.magnetic-glow img {
  display: block;
  width: 100%;
  height: auto;
  transition: transform 0.3s ease-out, filter 0.3s ease-out;
}

/* Magnetic glow ring */
.magnetic-glow::before {
  content: '';
  position: absolute;
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `box-shadow` | Chrome 10+, FF 4+, Safari 5.1+, Edge 12+ |
| `pseudo-element` | All modern browsers |

