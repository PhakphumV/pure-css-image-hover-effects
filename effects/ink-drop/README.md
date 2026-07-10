# Ink Drop

A circular “ink” splash that expands when hovered.

**Key CSS**
```
.hover-card.ink-drop::after {
  content: "";
  position: absolute;
  inset: 50%;
  width: 0; height: 0;
  border-radius: 50%;
  background: rgba(0,0,0,.1);
  transition: width .3s, height .3s;
}
.hover-card.ink-drop:hover::after { width: 200%; height: 200%; }
```
