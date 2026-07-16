# Bounce Right

Image slides from left to right on hover with bounce effect.

**Key CSS**
```css
/* Bounce Right Effect */

.bounce-right img {
  position: relative;
  left: 0;
  transition: left 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.bounce-right:hover img {
  left: 100%;
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `left` | Check caniuse.com |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `cubic-bezier` | Chrome 4+, FF 4+, Safari 3.1+, Edge 12+ |

