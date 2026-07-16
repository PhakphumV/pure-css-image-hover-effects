# Swipe Reveal

Split swipe reveals alternate color layer on hover using clip-path animation.

**Key CSS**
```css
/* Swipe Reveal Effect - Split swipe reveals alternate color layer */

.swipe-reveal {
}

.swipe-reveal img {
  transition: transform 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

/* Reveal layer - slides in from left */
.swipe-reveal::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  clip-path: inset(0 100% 0 0);
  transition: clip-path 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  z-index: 1;
}

```

**Browser Support**
| Feature | Support |
|---------|---------|
| `clip-path` | Chrome 28+, FF 28+, Safari 9+ |
| `animation` | Chrome 43+, FF 16+, Safari 9+ |
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `pseudo-element` | All modern browsers |
| `keyframes` | Chrome 43+, FF 16+, Safari 9+ |

