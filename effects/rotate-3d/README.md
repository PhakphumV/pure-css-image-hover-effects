# 3D Rotate

Perspective-based 3D rotation with scale on hover.

**Key CSS**
```css
/* Rotate 3D Effect */

.rotate-3d {
  perspective: 1000px;
}

.rotate-3d img {
  transition: transform 0.5s ease-out;
  transform-style: preserve-3d;
}

.rotate-3d:hover img {
  transform: rotateY(20deg) rotateX(-20deg) scale(1.3);
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `perspective` | Chrome 12+, FF 12+, Safari 7+ |
| `transform-style` | Chrome 12+, FF 12+, Safari 7+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |

