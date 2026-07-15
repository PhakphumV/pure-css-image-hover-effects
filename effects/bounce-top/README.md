# Bounce Top

Image slides from bottom to top on hover with bounce effect.

**Key CSS**
```css
.bounce-top {
  overflow: hidden;
  display: inline-block;
  border-radius: 8px;
  position: relative;
}
.bounce-top img {
  display: block;
  width: 100%;
  height: auto;
  position: relative;
  top: 0;
  transition: top 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}
.bounce-top:hover img {
  top: -100%;
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `cubic-bezier` | Chrome 4+, FF 4+, Safari 3.1+, Edge 12+ |

