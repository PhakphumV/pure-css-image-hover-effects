# Color Splash

Circular color splash expands from center on hover.

**Key CSS**
```css
/* Color Splash Effect */

.color-splash {
  position: relative;
  overflow: visible;
}

.color-splash::after {
  content: "";
  position: absolute;
  inset: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255,127,80,0.8);
  transform: translate(-50%, -50%);
  transition: width .3s, height .3s;
}

.color-splash:hover::after {
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `pseudo-element` | All modern browsers |
| `border-radius` | Chrome 4+, FF 4+, Safari 5+, Edge 12+ |
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |

