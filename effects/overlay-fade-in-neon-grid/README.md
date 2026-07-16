# Overlay Fade In Neon Grid

Neon grid overlay fades in over image on hover.

**Key CSS**
```css
.overlay-fade-in-neon-grid {
}

.overlay-fade-in-neon-grid::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    transition: opacity .5s ease, background-size .5s ease;
    background-size: 10px 10px;
    background-position: center center;
    background-image: linear-gradient(rgba(0, 255, 255, .5) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 255, 255, .5) 1px, transparent 1px);
    opacity: 0;
}

.overlay-fade-in-neon-grid img {}

.overlay-fade-in-neon-grid:hover img {}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `background` | All modern browsers |
| `pseudo-element` | All modern browsers |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `opacity` | All modern browsers |

