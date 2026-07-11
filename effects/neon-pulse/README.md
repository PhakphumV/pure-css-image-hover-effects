# Neon Pulse

Pulsing neon glow cycles through colors around the image border on hover.

**Key CSS**
```css
/* Neon Pulse Effect - Pulsing neon glow cycles color around border */

.neon-pulse {
  display: inline-block;
  border-radius: 8px;
  border: 1px solid var(--color-border, #e5e5e5);
  transition: border-color 0.3s ease-out;
}

.neon-pulse img {
  display: block;
  width: 100%;
  height: auto;
  border-radius: 7px;
}

.neon-pulse:hover {
  border-color: transparent;
  animation: neon-pulse-glow 1.6s ease-in-out infinite;
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `animation` | Check caniuse.com |
| `box-shadow` | Chrome 10+, FF 4+, Safari 5.1+, Edge 12+ |
| `border` | Check caniuse.com |
| `keyframes` | Check caniuse.com |

