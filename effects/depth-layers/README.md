# Depth Layers

Multi-layer parallax depth with translateZ separates foreground/mid/background on hover.

**Key CSS**
```css
/* Depth Layers Effect - Multi-layer parallax depth with translateZ */

.depth-layers {
  position: relative;
  display: inline-block;
  overflow: hidden;
  border-radius: 12px;
  perspective: 1000px;
  transform-style: preserve-3d;
}

.depth-layers img {
  display: block;
  width: 100%;
  height: auto;
  transform-style: preserve-3d;
  transition: transform 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94),
              filter 0.3s ease-out;
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
| `will-change` | Check caniuse.com |

