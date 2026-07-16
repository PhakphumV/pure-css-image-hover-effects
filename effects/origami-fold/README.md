# Origami Fold

Image folds like paper along diagonal and center creases with 3D depth on hover.

**Key CSS**
```css
/* Origami Fold Effect - Paper folding 3D transforms */

.origami-fold {
  perspective: 1200px;
  transform-style: preserve-3d;
}

.origami-fold img {
  transform-style: preserve-3d;
  transition: transform 0.7s cubic-bezier(0.25, 0.46, 0.45, 0.94),
              filter 0.7s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  will-change: transform;
}

/* Four triangular fold panels */
.origami-fold::before,
.origami-fold::after,
.origami-fold .fold-tl,
.origami-fold .fold-tr,
.origami-fold .fold-bl,
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `transform-style` | Chrome 12+, FF 12+, Safari 7+ |
| `perspective` | Chrome 12+, FF 12+, Safari 7+ |
| `clip-path` | Chrome 28+, FF 28+, Safari 9+ |
| `transform-origin` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `keyframes` | Chrome 43+, FF 16+, Safari 9+ |

