# Pure CSS Image Hover Effects

<img width="890" height="484" alt="image" src="https://github.com/user-attachments/assets/9ca9f515-30c0-49ce-a6de-6dfe8d03f3ab" />

A curated gallery of pure CSS hover effects designed for simple `<img>` tags wrapped in `<div>` containers. No JavaScript required for the visual effects — just hover to see them in action.

## Overview

This repository showcases interesting CSS techniques that add visual appeal to ordinary image elements. Each effect is self-contained, lightweight, and works without any JavaScript dependencies for the animation itself.

**Live Demo:** Open `index.html` in your browser to explore all effects.

## Structure

```
pure-css-image-hover-effects/
├── index.html              # Main gallery page
├── styles/
│   └── gallery.css         # Shared gallery styles + effect classes
├── scripts/
│   └── gallery.js          # Handles image switching (no effect logic)
└── effects/
    ├── effect-name/
    │   ├── index.html      # Dedicated demo page
    │   ├── style.css       # Standalone CSS for the effect
    │   └── README.md       # Documentation for each effect
    └── ... (10 total)
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

## TODO

- [x] Publish as Github page
- [ ] Dynamically build JSON file from directory structure for collection of effects
- [ ] Dynamically display style.css code in the single effect page
- [ ] Copy css code button
- [ ] CSS code preview with css styling format
- [ ] Dark mode switcher
- [ ] A11Y: Font resizer
- [ ] A11Y: Keyboard navigation
- [ ] Curate 100 hover effects
- [ ] Categorize effects
- [ ] Add tags to each effects, to mention which css properties used for the effect.
- [ ] Filter by tags
- [ ] Pagination and sorting
- [ ] OR Random cards
- [ ] Probably have to reorganize so it's easier to navigate and avoid duplicates.
- [ ] Curate 500 hover effects
- [ ] Curate 1k hover effects
- [ ] Curate 2k hover effects
- [ ] Curate 5k hover effects
- [ ] Curate 10k hover effects, is it possible?
- [ ] Curate 20k hover effects, is the sky limit?
- [ ] Curate 50k hover effects, or are we going to the moon?
- [ ] Curate 100k hover effects, anyone really believe this?


## Contributing

Each new effect should include:

1. Folder under `effects/` with kebab-case naming
2. `index.html` - Self-contained demo
3. `style.css` - Standalone CSS
4. `README.md` - Description and browser support table
5. Update `scripts/gallery.js` to register the new effect

## License

MIT License — [GitHub](https://github.com/PhakphumV/pure-css-image-hover-effects) • [Technolista](https://technolista.com)
