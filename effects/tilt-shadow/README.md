# Tilt Shadow

Perspective tilt with directional drop shadow creating 3D depth on hover.

**Key CSS**
```css
/* Tilt Shadow Effect - Perspective tilt with directional drop shadow */

.tilt-shadow {
  display: inline-block;
  border-radius: 8px;
  perspective: 800px;
  transition: box-shadow 0.35s ease-out;
}

.tilt-shadow img {
  display: block;
  width: 100%;
  height: auto;
  border-radius: 8px;
  transition: transform 0.35s ease-out;
  transform-style: preserve-3d;
}

.tilt-shadow:hover {
  box-shadow: -18px 24px 28px -12px rgba(0,0,0,0.35);
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `perspective` | Chrome 12+, FF 12+, Safari 7+ |
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `box-shadow` | Chrome 10+, FF 4+, Safari 5.1+, Edge 12+ |
| `transform-style` | Chrome 12+, FF 12+, Safari 7+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |

