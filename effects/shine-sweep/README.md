# Shine Sweep

Diagonal light sweep shines across image on hover like a glossy reflection.

**Key CSS**
```css
/* Shine Sweep Effect - Diagonal light sweep like glossy reflection */

.shine-sweep {
}

.shine-sweep img {
  transition: transform 0.4s ease-out, filter 0.4s ease-out;
}

/* Shine gradient sweep */
.shine-sweep::before {
  content: '';
  position: absolute;
  inset: -50%;
  background: linear-gradient(
    110deg,
    transparent 0%,
    rgba(255,255,255,0) 40%,
    rgba(255,255,255,0.4) 50%,
    rgba(255,255,255,0.6) 52%,
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `animation` | Chrome 43+, FF 16+, Safari 9+ |
| `linear-gradient` | Check caniuse.com |
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `pseudo-element` | All modern browsers |
| `mix-blend-mode` | Chrome 41+, FF 32+, Safari 8+ |

