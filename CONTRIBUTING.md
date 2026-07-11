# Contributing to Pure CSS Image Hover Effects

Thank you for your interest in contributing! This guide will help you add new effects or improve existing ones while maintaining consistency across the gallery.

## Table of Contents

1. [Adding a New Effect](#adding-a-new-effect)
2. [Coding Standards](#coding-standards)
3. [File Structure](#file-structure)
4. [CSS Guidelines](#css-guidelines)
5. [HTML Guidelines](#html-guidelines)
6. [Documentation Standards](#documentation-standards)
6. [Testing](#testing)
7. [Pull Request Process](#pull-request-process)

---

## Adding a New Effect

### 1. Create the Effect Folder

Create a new folder under `effects/` using **kebab-case** naming:

```
effects/your-effect-name/
├── index.html      # Demo page (required)
├── style.css       # Standalone CSS (required)
└── README.md       # Documentation (required for new effects)
```

### 2. Required Files

**style.css** - Standalone CSS for the effect:
```css
/* Your Effect Name */
.your-effect-name {
  /* Container styles */
}
.your-effect-name img {
  /* Image styles */
}
.your-effect-name:hover img {
  /* Hover state */
}
```

**index.html** - Self-contained demo page:
- Must use the standard effect page layout (see [HTML Guidelines](#html-guidelines))
- Include `styles/effect-page.css` and your `style.css`
- Include preview, HTML code block, and CSS code block sections
- Use `picsum.photos` or `via.placeholder.com` for demo images

**README.md** - Documentation:
```markdown
# Effect Name

Brief description of the visual effect.

**Key CSS**
```css
/* Core CSS that makes the effect work */
```

**Browser Support**
- CSS properties used: `transform`, `transition`, `filter`, etc.
- Works in: Chrome 36+, Firefox 16+, Safari 9+, Edge 12+
```

### 3. Register the Effect

Run the manifest generator:
```bash
node scripts/generate-effects-data.js
```

This updates `effects-manifest.js` automatically.

---

## Coding Standards

### CSS Guidelines

#### Naming Conventions
- Use **kebab-case** for all class names: `.hover-effect-name`
- Use the effect name as the root class: `.glass-mosaic`, `.ink-drop`
- Avoid generic names like `.card`, `.wrapper`, `.container`
- Prefix pseudo-elements with the effect class: `.glass-mosaic::after`

#### CSS Organization
```css
/* 1. Container/Wrapper styles */
.effect-name {
  position: relative;
  overflow: hidden;
  display: inline-block;
  border-radius: 8px;
}

/* 2. Image base styles */
.effect-name img {
  display: block;
  width: 100%;
  height: auto;
  /* Transition properties */
}

/* 3. Pseudo-elements (if any) */
.effect-name::before,
.effect-name::after {
  content: "";
  position: absolute;
  /* ... */
}

/* 4. Hover states */
.effect-name:hover img { ... }
.effect-name:hover::after { ... }
```

#### Properties & Values
- Use **CSS custom properties** for configurable values:
  ```css
  .effect-name {
    --gap: 4px;
    --blur: 4px;
    --duration: 0.3s;
  }
  ```
- Prefer `transform` and `opacity` for animations (GPU-accelerated)
- Use `transition` with explicit properties, not `transition: all`
- Include vendor prefixes only when necessary (autoprefixer handles this)

#### Browser Compatibility
- Target: Chrome 36+, Firefox 16+, Safari 9+, Edge 12+
- Test `backdrop-filter`, `clip-path`, `perspective` in Safari
- Provide fallbacks where possible

#### Performance
- Avoid animating `width`, `height`, `top`, `left` — use `transform` instead
- Use `will-change` sparingly
- Keep paint areas small

---

### HTML Guidelines

#### Standard Page Structure
All effect pages MUST use this layout (see `styles/effect-page.css`):

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Effect Name — Pure CSS Image Hover Effects</title>
  <link rel="stylesheet" href="../../styles/effect-page.css">
  <link rel="stylesheet" href="./style.css">
</head>
<body>
  <header class="page-header">
    <a href="../../index.html" class="back-link">← Back to Gallery</a>
    <h1>Effect Name</h1>
    <p class="effect-description">Clear, one-sentence description of the effect.</p>
  </header>

  <main class="effect-layout">
    <div class="left-column">
      <section class="panel panel--preview">
        <h2>Preview</h2>
        <div class="preview-container">
          <div class="effect-class-name">
            <img src="https://picsum.photos/600/400?random=N" alt="Demo image">
          </div>
        </div>
        <p class="preview-hint">Hover over the image to see the effect</p>
      </section>

      <section class="panel panel--credits">
        <h2>Credits</h2>
        <div class="credit-entry">
          <strong>Your Name</strong>
          <span class="credit-role">Creator</span>
          <span class="credit-notes">Brief note about implementation</span>
        </div>
      </section>
    </div>

    <div class="right-column">
      <section class="panel panel--code">
        <h2>HTML</h2>
        <pre class="code-block"><code><div class="effect-class-name">
  <img src="your-image.jpg" alt="Description">
</div></code></pre>
      </section>

      <section class="panel panel--code">
        <h2>CSS</h2>
        <pre class="code-block"><code>/* Copy EXACTLY from style.css — must match! */</code></pre>
      </section>
    </div>
  </main>

  <footer class="page-footer">
    <p>MIT License — <a href="https://github.com/PhakphumV/pure-css-image-hover-effects" target="_blank" rel="noopener">GitHub</a></p>
  </footer>
</body>
</html>
```

#### Code Blocks
- Escape HTML entities in code blocks: `<`, `>`, `"`
- CSS in code blocks MUST match `style.css` exactly (whitespace normalized)
- Use 2-space indentation in code blocks

#### Accessibility
- Always include meaningful `alt` text on demo images
- Use semantic HTML (`<header>`, `<main>`, `<section>`, `<footer>`)
- Maintain heading hierarchy (h1 → h2 → h3)
- Include `focus-visible` styles for keyboard navigation

---

### Documentation Standards

Each effect MUST have a `README.md` with:

```markdown
# Effect Name

One-paragraph description of the visual effect and interaction.

**Key CSS**
```css
/* The essential CSS that creates the effect — copy-pasteable */
```

**Browser Support**
| Feature | Support |
|---------|---------|
| `transform` | Chrome 36+, FF 16+, Safari 9+, Edge 12+ |
| `filter` | Chrome 53+, FF 35+, Safari 9+ |
| `backdrop-filter` | Chrome 76+, FF 70+, Safari 9+ |
| etc. | |

**Performance Notes** (optional)
- Any caveats about paint cost, layout thrashing, etc.
```

---

## File Structure Reference

```
pure-css-image-hover-effects/
├── index.html                 # Gallery index (auto-generated cards)
├── effects-manifest.js        # Auto-generated effect registry
├── CONTRIBUTING.md            # This file
├── README.md                  # Project overview
├── styles/
│   ├── gallery.css            # Index page styles
│   └── effect-page.css        # Individual effect page styles (REQUIRED)
├── scripts/
│   ├── gallery.js             # Index page image switcher
│   └── generate-effects-data.js  # Manifest generator
└── effects/
    ├── effect-name/
    │   ├── index.html         # Demo page (uses effect-page.css)
    │   ├── style.css          # Standalone CSS (used in gallery + effect page)
    │   └── README.md          # Documentation
    └── ... (33 effects and counting)
```

---

## Testing

Before submitting:

1. **Visual verification**: Open `effects/your-effect/index.html` in browser
   - Hover effect works smoothly
   - No layout shift on hover
   - Works at different viewport sizes

2. **Gallery integration**: Open `index.html`
   - Effect card appears in gallery
   - Image switcher works (if applicable)
   - Click-through to effect page works

3. **Code consistency**:
   - CSS in `index.html` code block matches `style.css` exactly
   - No console errors
   - Valid HTML (run through validator if unsure)

4. **Cross-browser spot check**:
   - Chrome/Edge (Chromium)
   - Firefox
   - Safari (or iOS Safari)

---

## Pull Request Process

1. **Fork** the repository
2. **Create a branch**: `git checkout -b effect/your-effect-name`
3. **Add your effect** following the guidelines above
4. **Run the manifest generator**: `node scripts/generate-effects-data.js`
5. **Test locally**: Open `index.html` and your effect page
6. **Commit** with a clear message:
   ```
   feat: add "Effect Name" hover effect

   - Adds new pure CSS hover effect with [brief description]
   - Includes demo page, standalone CSS, and documentation
   - Updates effects manifest
   ```
7. **Open PR** with:
   - Screenshots/GIF of the effect
   - Link to live demo (if deployed)
   - Any browser compatibility notes

### PR Checklist
- [ ] Folder uses kebab-case naming
- [ ] `style.css` is standalone (no external dependencies)
- [ ] `index.html` uses standard effect-page layout
- [ ] CSS in `index.html` code block matches `style.css`
- [ ] `README.md` exists with Key CSS and Browser Support
- [ ] Manifest regenerated (`effects-manifest.js` updated)
- [ ] Effect works in gallery index
- [ ] No console errors
- [ ] Accessible markup (alt text, semantic HTML, focus styles)

---

## Code Style Reference

### CSS Property Order (Recommended)
1. Positioning: `position`, `inset`, `z-index`
2. Box model: `display`, `width`, `height`, `margin`, `padding`
3. Borders: `border`, `border-radius`, `overflow`
4. Background: `background`, `backdrop-filter`
5. Typography: `font`, `color`, `text-align`
6. Transforms: `transform`, `transform-origin`, `perspective`
7. Transitions: `transition`, `animation`
8. Misc: `opacity`, `filter`, `clip-path`, `will-change`

### CSS Formatting
```css
/* Good */
.effect-name {
  position: relative;
  overflow: hidden;
  display: inline-block;
  border-radius: 8px;
}

.effect-name img {
  display: block;
  width: 100%;
  height: auto;
  transition: transform 0.4s ease-out;
}

/* Avoid */
.effect-name{position:relative;overflow:hidden}
```

### Transition Timing Functions
- `ease-out` for entrances/reveals (natural deceleration)
- `ease-in-out` for back-and-forth movements
- `cubic-bezier(0.68, -0.55, 0.265, 1.55)` for bounce/overshoot
- Avoid `linear` unless intentional

---

## Questions?

Open an issue or start a discussion on GitHub. We're happy to help!

---

*Thank you for contributing to Pure CSS Image Hover Effects!*