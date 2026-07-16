# Holographic Shimmer

Iridescent rainbow shimmer sweeps across image like a hologram card on hover.

**Key CSS**
```css
/* Holographic Shimmer Effect - Iridescent rainbow sweep */

.holographic-shimmer {
  position: relative;
  overflow: visible; /* Allow pseudo-elements to extend */
}

/* Base holographic film layer */
.holographic-shimmer::before {
  content: '';
  position: absolute;
  inset: -20%;
  background: 
    conic-gradient(
      from 0deg,
      #ff0080, #ff8c00, #ffd700, #00ff80, #00ffff, #0080ff, #8000ff, #ff0080
    );
  opacity: 0;
  pointer-events: none;
  mix-blend-mode: screen;
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `conic-gradient` | Chrome 69+, FF 83+, Safari 12.1+ |
| `animation` | Chrome 43+, FF 16+, Safari 9+ |
| `backdrop-filter` | Chrome 76+, FF 70+, Safari 9+ |
| `mix-blend-mode` | Chrome 41+, FF 32+, Safari 8+ |
| `keyframes` | Chrome 43+, FF 16+, Safari 9+ |

