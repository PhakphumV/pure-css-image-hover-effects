# Bounce Bottom

Image slides from top to bottom on hover with bounce effect.

**Key CSS**
```css
/* Bounce Bottom Effect */

.bounce-bottom img {
  position: relative;
  top: 0;
  transition: top 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.bounce-bottom:hover img {
  top: 100%;
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `top` | Check caniuse.com |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `cubic-bezier` | Chrome 4+, FF 4+, Safari 3.1+, Edge 12+ |

