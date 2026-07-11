# Flip Horizontal

Image flips horizontally on hover using CSS 3D transform.

**Key CSS**
```css
.flip-horizontal {
  overflow: hidden;
  display: inline-block;
  border-radius: 8px;
  perspective: 1000px;
}
.flip-horizontal img {
  display: block;
  width: 100%;
  height: auto;
  transition: transform 0.6s ease;
  transform-style: preserve-3d;
}
.flip-horizontal:hover img {
  transform: scaleX(-1);
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `perspective` | Chrome 12+, FF 12+, Safari 7+ |
| `transform-style` | Chrome 12+, FF 12+, Safari 7+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |

