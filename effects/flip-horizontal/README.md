# Flip Horizontal

A CSS hover effect that flips the image horizontally using `transform: scaleX(-1)`, creating a mirror effect across the vertical axis.

## How It Works

The effect uses CSS 3D transforms with `scaleX(-1)` to flip the image along its horizontal axis. The `perspective` property on the container adds depth, and `transform-style: preserve-3d` ensures the image maintains its 3D context during the flip.

## Browser Support

| Feature | Support |
|---------|---------|
| CSS `transform` | Chrome 36+, Firefox 16+, Safari 9+, Edge 12+ |
| CSS `transition` | Chrome 36+, Firefox 16+, Safari 9+, Edge 12+ |
| CSS `scaleX` | Chrome 36+, Firefox 16+, Safari 9+, Edge 12+ |

## Usage

```html
<div class="flip-horizontal">
  <img src="your-image.jpg" alt="Description">
</div>
```