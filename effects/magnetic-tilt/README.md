# Magnetic Tilt

3D tilt toward cursor with multi-layer parallax depth using translateZ.

**Key CSS**
```css
/* Magnetic Tilt Effect - 3D tilt toward cursor with depth parallax layers */

.magnetic-tilt {
  perspective: 1000px;
  transform-style: preserve-3d;
}

.magnetic-tilt img {
  transform-style: preserve-3d;
  transition: transform 0.1s ease-out, filter 0.3s ease-out;
  will-change: transform;
}

/* Depth layers using pseudo-elements */
.magnetic-tilt::before,
.magnetic-tilt::after {
  content: '';
  position: absolute;
  inset: -15%;
  background: inherit;
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `perspective` | Chrome 12+, FF 12+, Safari 7+ |
| `transform-style` | Chrome 12+, FF 12+, Safari 7+ |
| `translateZ` | Chrome 12+, FF 10+, Safari 4+ |
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |

