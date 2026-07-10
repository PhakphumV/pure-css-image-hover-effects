# Color Splash

A circular splash that expands from the center on hover.

**Key CSS**
```
.hover-card.color-splash::after {
  content: "";
  position: absolute;
  inset: 50%;
  width: 0; height: 0;
  border-radius: 50%;
  background: rgba(255,127,80,0.8);
  transition: width .3s, height .3s;
}
.hover-card.color-splash:hover::after { width: 300%; height: 300%; }
```
