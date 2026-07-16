# Ink Drop

Circular "ink" splash expands from center on hover.

**Key CSS**
```css
/* Ink Drop Effect */

.ink-drop::after {
  content: "";
  position: absolute;
  inset: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.1);
  transform: translate(-50%, -50%);
  transition: width 0.3s, height 0.3s;
}

.ink-drop:hover::after {
  width: 200%;
  height: 200%;
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `pseudo-element` | All modern browsers |
| `border-radius` | Chrome 4+, FF 4+, Safari 5+, Edge 12+ |
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |

