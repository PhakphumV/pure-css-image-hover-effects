# Glitch Shift

Stepped RGB channel glitch flicker with clip-path slice animation on hover.

**Key CSS**
```css
/* Glitch Shift Effect - Stepped RGB-channel glitch flicker */

.glitch-shift {
  overflow: hidden;
  display: inline-block;
  border-radius: 8px;
  position: relative;
}

.glitch-shift img {
  display: block;
  width: 100%;
  height: auto;
}

.glitch-shift::before,
.glitch-shift::after {
  content: '';
  position: absolute;
  inset: 0;
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `animation` | Check caniuse.com |
| `clip-path` | Chrome 28+, FF 28+, Safari 9+ |
| `mix-blend-mode` | Check caniuse.com |
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `keyframes` | Check caniuse.com |

