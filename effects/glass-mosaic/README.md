# Glass Mosaic

A frosted‑glass grid overlay that dims when hovered.

**Key CSS**
```
.hover-card.glass-mosaic {
  position: relative;
  overflow: hidden;
}
.hover-card.glass-mosaic::after {
  content: "";
  position: absolute;
  inset: 0;
  backdrop-filter: blur(4px) saturate(150%);
  opacity: 0.6;
  transition: opacity .3s;
}
.hover-card.glass-mosaic:hover::after { opacity: .2; }
```
