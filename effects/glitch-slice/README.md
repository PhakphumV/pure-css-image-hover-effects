# Glitch Slice

Image fractures into horizontal glitch slices with hue-shifted colors on hover.

**Key CSS**
```css
/* Glitch Slice Effect - Horizontal glitch slices with hue shifts */

.glitch-slice {
  position: relative;
  display: inline-block;
  overflow: hidden;
  border-radius: 8px;
}

.glitch-slice img {
  display: block;
  width: 100%;
  height: auto;
  transition: transform 0.3s ease-out, filter 0.3s ease-out;
}

/* Generate glitch slices using clip-path on pseudo-elements */
/* We'll use multiple layers with different clip-paths */
.glitch-slice::before,
.glitch-slice::after,
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `clip-path` | Chrome 28+, FF 28+, Safari 9+ |
| `filter` | Chrome 53+, FF 35+, Safari 9+ |
| `animation` | Check caniuse.com |
| `mix-blend-mode` | Check caniuse.com |
| `keyframes` | Check caniuse.com |

