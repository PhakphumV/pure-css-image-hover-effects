# Neon Pulse

Pulsing neon glow cycles through colors around the image border on hover.

**Key CSS**
```css
/* Neon Pulse Effect - Pulsing neon glow cycles color around border */

.neon-pulse {
  border: 1px solid var(--color-border, #e5e5e5);
  transition: border-color 0.3s ease-out;
}

.neon-pulse img {
}

.neon-pulse:hover {
  border-color: transparent;
  animation: neon-pulse-glow 1.6s ease-in-out infinite;
}

@keyframes neon-pulse-glow {
  0%, 100% { box-shadow: 0 0 8px 2px #2563eb, 0 0 20px 6px rgba(37,99,235,0.5); }
  50%      { box-shadow: 0 0 14px 4px #d946ef, 0 0 30px 10px rgba(217,70,239,0.6); }
}

```

**Browser Support**
| Feature | Support |
|---------|---------|
| `animation` | Chrome 43+, FF 16+, Safari 9+ |
| `box-shadow` | Chrome 10+, FF 4+, Safari 5.1+, Edge 12+ |
| `border` | Check caniuse.com |
| `keyframes` | Chrome 43+, FF 16+, Safari 9+ |

