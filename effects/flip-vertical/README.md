# Flip Vertical

Image flips vertically on hover using CSS 3D transform.

**Key CSS**
```css
/* Flip Vertical Effect */

.flip-vertical {
  perspective: 1000px;
}

.flip-vertical img {
  transition: transform 0.6s ease;
  transform-style: preserve-3d;
}

.flip-vertical:hover img {
  transform: scaleY(-1);
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `perspective` | Chrome 12+, FF 12+, Safari 7+ |
| `transform-style` | Chrome 12+, FF 12+, Safari 7+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |

