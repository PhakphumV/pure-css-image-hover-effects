# Refraction Lens

A magnifying‑lens look‑ahead effect that enlarges slightly on hover.

**Key CSS**
```
.hover-card.refraction-lens::after {
  content: "";
  position: absolute;
  border-radius: 50%;
  width: 120px; height: 120px;
  background: linear-gradient(rgba(255,255,255,0.8), transparent);
  transform: translate(-50%, -50%) scale(1);
  transition: transform .3s;
}
.hover-card.refraction-lens:hover::after { transform: translate(-50%, -50%) scale(1.5); }
```
