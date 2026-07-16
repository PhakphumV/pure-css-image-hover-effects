# Glitch Slice

Image fractures into horizontal glitch slices with hue-shifted colors on hover.

**Key CSS**
```css
/* Glitch Slice Effect - Horizontal glitch slices with hue shifts */

.glitch-slice {
  position: relative;
  overflow: visible; /* Allow slices to show */
}

/* Base image transition */
.glitch-slice img {
  transition: transform 0.3s ease-out, filter 0.3s ease-out;
}

/* Generate glitch slices using clip-path on pseudo-elements and child elements */
.glitch-slice::before,
.glitch-slice::after,
.glitch-slice .slice-1,
.glitch-slice .slice-2,
.glitch-slice .slice-3,
.glitch-slice .slice-4,
.glitch-slice .slice-5 {
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `clip-path` | Chrome 28+, FF 28+, Safari 9+ |
| `filter` | Chrome 53+, FF 35+, Safari 9+ |
| `animation` | Chrome 43+, FF 16+, Safari 9+ |
| `mix-blend-mode` | Chrome 41+, FF 32+, Safari 8+ |
| `keyframes` | Chrome 43+, FF 16+, Safari 9+ |

