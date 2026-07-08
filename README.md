# Pure CSS Image Hover Effects

A curated gallery of pure CSS hover effects designed for simple `<img>` tags wrapped in `<div>` containers. No JavaScript required for the visual effects — just hover to see them in action.

## Overview

This repository showcases interesting CSS techniques that add visual appeal to ordinary image elements. Each effect is self-contained, lightweight, and works without any JavaScript dependencies for the animation itself.

**Live Demo:** Open `index.html` in your browser to explore all effects.

## Effects Gallery

| Effect | Description | CSS Features |
|--------|-------------|--------------|
| Scale Reveal | Image scales up within a clipped container | `transform: scale()`, `overflow: hidden` |
| Slide Reveal | Image slides sideways while zooming | `transform: translateX() scale()` |
| Fade Colorize | Grayscale to full color transition | `filter: grayscale()`, smooth transitions |
| Glow Border | Radial glow expands around the image | `box-shadow` animation |
| 3D Rotate | Perspective-based 3D rotation | `perspective`, `transform-style: preserve-3d` |
| Clip Reveal | Center-expanding clip path reveal | `clip-path: inset()` |
| Zoom & Rotate | Combined zoom with subtle rotation | `transform: scale() rotate()` |
| Blur Sharpen | Blurred grayscale sharpens on hover | `filter: blur() grayscale()` |
| Vignette | Dark vignette overlay fades in | `::after` pseudo-element, gradient |
| Duotone Shift | Duotone filter transitions to normal | `filter: sepia() hue-rotate() saturate()` |

## Structure

```
pure-css-image-hover-effects/
├── index.html              # Main gallery page
├── styles/
│   └── gallery.css         # Shared gallery styles + effect classes
├── scripts/
│   └── gallery.js          # Handles image switching (no effect logic)
├── effects/
│   ├── effect-name/
│   │   ├── index.html      # Dedicated demo page
│   │   ├── style.css       # Standalone CSS for the effect
│   │   └── README.md       # Documentation for each effect
│   └── ... (10 total)
└── assets/
    └── previews/           # Preview screenshots
```

## Usage

### Quick Start

1. Copy the desired effect's HTML structure:

```html
<div class="scale-reveal">
  <img src="your-image.jpg" alt="Description">
</div>
```

2. Include the CSS (either from `styles/gallery.css` or a standalone `style.css`):

```html
<link rel="stylesheet" href="styles/gallery.css">
```

### As a Module

Each effect folder contains standalone files you can drop into any project:

```html
<!-- Include in your page -->
<link rel="stylesheet" href="effects/scale-reveal/style.css">

<div class="scale-reveal">
  <img src="photo.jpg" alt="Your image">
</div>
```

## Features

- **Pure CSS**: All animations use only CSS transitions and transforms
- **No JS for Effects**: JavaScript is only used for gallery navigation, not the animations themselves
- **Responsive**: Grid adapts to screen size
- **Accessible**: Keyboard navigation support, reduced motion respect
- **Lightweight**: Minimal CSS, no external dependencies

## Browser Support

All effects work in evergreen browsers. Specific feature support varies:

| Feature | Support |
|---------|---------|
| CSS `transform` | Chrome 36+, Firefox 16+, Safari 9+, Edge 12+ |
| CSS `transition` | Chrome 36+, Firefox 16+, Safari 9+, Edge 12+ |
| CSS `filter` | Chrome 53+, Firefox 35+, Safari 9+ |
| CSS `clip-path` | Chrome 28+, Firefox 28+, Safari 9+ |
| CSS `perspective` | Chrome 12+, Firefox 12+, Safari 7+ |

## Customization

All effects use CSS custom properties (CSS variables) for easy theming:

```css
:root {
  --color-primary: #2563eb;  /* Change accent color */
  --transition: 0.3s ease;   /* Adjust timing */
}
```

## Running Locally

```bash
# Clone or navigate to the directory
cd pure-css-image-hover-effects

# Serve with any static server (optional but recommended)
npx serve .
# or
python -m http.server 8000
```

Open `http://localhost:8000` in your browser.

## Contributing

Each new effect should include:

1. Folder under `effects/` with kebab-case naming
2. `index.html` - Self-contained demo
3. `style.css` - Standalone CSS
4. `README.md` - Description and browser support table
5. Update `scripts/gallery.js` to register the new effect

## License

MIT License — [GitHub](https://github.com/PhakphumV/pure-css-image-hover-effects) • [Technolista](https://technolista.com)