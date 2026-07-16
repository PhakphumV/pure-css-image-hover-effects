# Shadow Drop

A shadow is present by default and settles flat on hover.

**Key CSS**
```css
.shadow-drop {
}
.shadow-drop img {
  box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.4);
  transition: box-shadow 0.4s ease;
}
.shadow-drop:hover img {
  box-shadow: none;
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `box-shadow` | Chrome 10+, FF 4+, Safari 5.1+, Edge 12+ |
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |

