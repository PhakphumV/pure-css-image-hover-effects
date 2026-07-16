# Glitch Shift

Stepped RGB channel glitch flicker with clip-path slice animation on hover.

**Key CSS**
```css
/* Glitch Shift Effect - Stepped RGB-channel glitch flicker */

.glitch-shift {
  position: relative;
  overflow: visible; /* Allow pseudo-elements to be visible */
}

.glitch-shift::before,
.glitch-shift::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: inherit;
  background-size: cover;
  background-position: center;
  opacity: 0;
  mix-blend-mode: screen;
  pointer-events: none;
  z-index: 1;
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `animation` | Chrome 43+, FF 16+, Safari 9+ |
| `clip-path` | Chrome 28+, FF 28+, Safari 9+ |
| `mix-blend-mode` | Chrome 41+, FF 32+, Safari 8+ |
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `keyframes` | Chrome 43+, FF 16+, Safari 9+ |

