# Flip Horizontal

Image flips horizontally on hover using CSS 3D transform.

**Key CSS**
```css
/* Flip Horizontal Effect */

.flip-horizontal {
  perspective: 1000px;
}

.flip-horizontal img {
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

