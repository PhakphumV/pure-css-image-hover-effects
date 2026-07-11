# Bounce Bottom

Image slides from top to bottom on hover with bounce effect.

**Key CSS**
```css
.bounce-bottom {
  overflow: hidden;
  display: inline-block;
  border-radius: 8px;
  position: relative;
}
.bounce-bottom img {
  display: block;
  width: 100%;
  height: auto;
}
.bounce-bottom::before {
  content: '';
  position: absolute;
  top: 100%; left: 0;
  width: 100%; height: 100%;
  background: white;
  transition: top 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  z-index: 1;
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `cubic-bezier` | Chrome 4+, FF 4+, Safari 3.1+, Edge 12+ |

