# Bounce Right

Image slides from left to right on hover with bounce effect.

**Key CSS**
```css
.bounce-right {
  overflow: hidden;
  display: inline-block;
  border-radius: 8px;
  position: relative;
}
.bounce-right img {
  display: block;
  width: 100%;
  height: auto;
}
.bounce-right::before {
  content: '';
  position: absolute;
  top: 0; left: -100%;
  width: 100%; height: 100%;
  background: white;
  transition: left 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  z-index: 1;
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `cubic-bezier` | Chrome 4+, FF 4+, Safari 3.1+, Edge 12+ |

