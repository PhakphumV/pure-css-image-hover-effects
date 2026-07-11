# Holographic Shimmer

Iridescent rainbow shimmer sweeps across image like a hologram card on hover.

**Key CSS**
```css
/* Holographic Shimmer Effect - Iridescent rainbow sweep */

.holographic-shimmer {
  position: relative;
  display: inline-block;
  overflow: hidden;
  border-radius: 12px;
}

.holographic-shimmer img {
  display: block;
  width: 100%;
  height: auto;
  transition: transform 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94),
              filter 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

/* Base holographic film layer */
.holographic-shimmer::before {
  content: '';
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `conic-gradient` | Chrome 69+, FF 83+, Safari 12.1+ |
| `animation` | Chrome 43+, FF 16+, Safari 9+ |
| `backdrop-filter` | Chrome 76+, FF 70+, Safari 9+ |
| `mix-blend-mode` | Chrome 41+, FF 32+, Safari 8+ |
| `keyframes` | Chrome 43+, FF 16+, Safari 9+ |

