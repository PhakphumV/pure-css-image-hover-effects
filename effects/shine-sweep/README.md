# Shine Sweep

Diagonal light sweep shines across image on hover like a glossy reflection.

**Key CSS**
```css
/* Shine Sweep Effect - Diagonal light sweep like glossy reflection */

.shine-sweep {
  position: relative;
  display: inline-block;
  overflow: hidden;
  border-radius: 8px;
}

.shine-sweep img {
  display: block;
  width: 100%;
  height: auto;
  transition: transform 0.4s ease-out, filter 0.4s ease-out;
}

/* Shine gradient sweep */
.shine-sweep::before {
  content: '';
  position: absolute;
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `animation` | Check caniuse.com |
| `linear-gradient` | Check caniuse.com |
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `pseudo-element` | All modern browsers |
| `mix-blend-mode` | Check caniuse.com |

