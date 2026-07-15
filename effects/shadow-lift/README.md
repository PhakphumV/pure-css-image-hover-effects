# Shadow Lift

A soft shadow appears beneath the image on hover, creating lift.

**Key CSS**
```css
.shadow-lift {
  overflow: hidden;
  display: inline-block;
  border-radius: 8px;
}
.shadow-lift img {
  display: block;
  width: 100%;
  height: auto;
  box-shadow: none;
  transition: box-shadow 0.4s ease;
}
.shadow-lift:hover img {
  box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.4);
}
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `box-shadow` | Chrome 10+, FF 4+, Safari 5.1+, Edge 12+ |
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `transition` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |

