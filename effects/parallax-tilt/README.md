# Parallax Tilt

Multi-layer 3D parallax tilt toward cursor with depth separation (JS-enhanced).

**Key CSS**
```css
/* Parallax Tilt Effect - Multi-layer 3D parallax tilt toward cursor with depth separation */

.parallax-tilt {
  position: relative;
  display: inline-block;
  overflow: hidden;
  border-radius: 12px;
  perspective: 1000px;
  transform-style: preserve-3d;
}

.parallax-tilt img {
  display: block;
  width: 100%;
  height: auto;
  transform-style: preserve-3d;
  transition: transform 0.1s ease-out, filter 0.3s ease-out;
  will-change: transform;
}

```

**Browser Support**
| Feature | Support |
|---------|---------|
| `perspective` | Chrome 12+, FF 12+, Safari 7+ |
| `transform-style` | Chrome 12+, FF 12+, Safari 7+ |
| `translateZ` | Check caniuse.com |
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |

