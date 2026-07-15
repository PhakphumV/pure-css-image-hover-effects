# Invert Flash

A quick full color-invert flash on hover.

**Key CSS**
```css
.invert-flash {
  overflow: hidden;
  display: inline-block;
  border-radius: 8px;
}
.invert-flash img {
  display: block;
  width: 100%;
  height: auto;
  filter: invert(0);
  transition: filter 0.1s ease;
}
.invert-flash:hover img {
  animation: invert-flash 0.15s ease;
}

@keyframes invert-flash {
  0%   { filter: invert(0); }
  50%  { filter: invert(1); }
  100% { filter: invert(0); }
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `filter` | Chrome 53+, FF 35+, Safari 9+ |
| `animation` | Chrome 43+, FF 16+, Safari 9+ |
| `keyframes` | Chrome 43+, FF 16+, Safari 9+ |

