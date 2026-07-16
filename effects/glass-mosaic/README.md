# Glass Mosaic

Frosted-glass overlay with backdrop-filter that dims on hover.

**Key CSS**
```css
/* Glass Mosaic Effect */

.glass-mosaic::after {
  content: "";
  position: absolute;
  inset: 0;
  backdrop-filter: blur(4px) saturate(150%);
  opacity: 0.6;
  pointer-events: none;
  transition: opacity 0.3s;
}

.glass-mosaic:hover::after {
  opacity: 0.2;
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `backdrop-filter` | Chrome 76+, FF 70+, Safari 9+ |
| `pseudo-element` | All modern browsers |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `css-variables` | Chrome 49+, FF 31+, Safari 9.1+, Edge 15+ |

