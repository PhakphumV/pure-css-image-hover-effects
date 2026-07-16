# Effect Template

Use this template to create a new effect page.

## Files

- `index.html` - Copy to `effects/your-effect/index.html` and replace placeholders:
  - `{{EFFECT_NAME}}` - Human readable name (e.g., "Scale Reveal")
  - `{{DESCRIPTION}}` - Brief description of the effect
  - `{{EFFECT_ID}}` - CSS class name (e.g., "scale-reveal")
  - `{{CONTRIBUTOR_NAME}}` - Your name or GitHub handle
  - `{{CONTRIBUTOR_ROLE}}` - Your role (Creator/Contributor)
  - `{{CONTRIBUTOR_NOTES}}` - Brief notes about your contribution

- `../styles/base.css` - Shared base styles (loaded first)
- `../styles/effect-page.css` - Effect page layout styles
- `style.css` - Effect stylesheet (contains ONLY hover behavior, no layout)
- `../../scripts/effect-page.js` - Auto-generates HTML/CSS code panels from live DOM

## Steps to Add New Effect

1. Copy `index.html` to `effects/your-effect-name/index.html`
2. Replace all `{{PLACEHOLDERS}}` in the HTML
3. Create `style.css` with **only the hover behavior** (transforms, filters, animations, etc.)
   - Do NOT include layout properties: `overflow`, `display`, `width`, `height`, `border-radius`, `position: relative`, `margin`, `padding` on the base selector
   - The gallery and effect pages provide normalized layout via `.card__media` / `.preview-container`
   - Keep `overflow: visible` if your effect needs it (e.g., box-shadow glow, pseudo-elements extending beyond container)
4. Add entry in `effects-manifest.js` (run `node scripts/generate-manifest.js`)
5. Commit both files

## Panel Structure

```
Preview Panel    - Shows live hover effect
HTML Panel       - Auto-generated from live preview DOM
CSS Panel        - Auto-fetched from ./style.css
Credits Panel    - Contributor information
```

## CSS Guidelines

**Keep in style.css (hover behavior):**
- `transform`, `filter`, `clip-path`, `opacity`
- `transition` / `animation` on hover properties
- `@keyframes` definitions
- `box-shadow` (when it's the effect itself, e.g., glow-border)
- `background` on `::before`/`::after` (overlay effects)
- `mix-blend-mode`, `backdrop-filter`
- Custom properties (`--gap`, `--blur`, etc.)

**Remove from style.css (handled by base.css):**
- `.effect-id { overflow, display, border-radius, position, width, height, margin, padding }`
- `.effect-id img { display, width, height, border-radius }`
- Base `transition` on non-hover properties

**Exception:** Keep `overflow: visible` if pseudo-elements/box-shadow need to escape container.
Keep `position: relative` if you use absolute-positioned pseudo-elements.
Keep specific `border-radius` ONLY if the effect morphs it (e.g., `radius-square-to-circle`).

## Example style.css

```css
/* Scale Reveal Effect */

.scale-reveal img {
  clip-path: inset(0 50% 0 50%);
  transition: clip-path 0.5s ease-out, transform 0.5s ease-out;
}

.scale-reveal:hover img {
  clip-path: inset(0 0 0 0);
  transform: scale(1.1);
}
```

## Template Placeholders Reference

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{EFFECT_NAME}}` | Display name | "Scale Reveal" |
| `{{DESCRIPTION}}` | One-line description | "Image reveals through animated clip-path on hover." |
| `{{EFFECT_ID}}` | CSS class (kebab-case) | "scale-reveal" |
| `{{CONTRIBUTOR_NAME}}` | Your name/handle | "JaneDev" |
| `{{CONTRIBUTOR_ROLE}}` | Role | "Creator" |
| `{{CONTRIBUTOR_NOTES}}` | Brief notes | "Clip-path reveal with scale" |