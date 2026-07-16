# Tilt Shadow

Perspective tilt with directional drop shadow creating 3D depth on hover.

**Key CSS**
```css
/* Tilt Shadow Effect - Perspective tilt with directional drop shadow */

.tilt-shadow {
  perspective: 800px;
  transition: box-shadow 0.35s ease-out;
}

.tilt-shadow img {
  transition: transform 0.35s ease-out;
  transform-style: preserve-3d;
}

.tilt-shadow:hover {
  box-shadow: -18px 24px 28px -12px rgba(0,0,0,0.35);
}

.tilt-shadow:hover img {
  transform: rotateX(8deg) rotateY(-12deg) translateZ(10px) scale(1.03);
}

```

**Browser Support**
| Feature | Support |
|---------|---------|
| `perspective` | Chrome 12+, FF 12+, Safari 7+ |
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `box-shadow` | Chrome 10+, FF 4+, Safari 5.1+, Edge 12+ |
| `transform-style` | Chrome 12+, FF 12+, Safari 7+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |

