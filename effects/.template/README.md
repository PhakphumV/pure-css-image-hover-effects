# Effect Template

Use this template to create a new effect page.

## Files

- `index.html` - Copy to `effects/your-effect/index.html` and replace placeholders:
  - `{{EFFECT_NAME}}` - Human readable name (e.g., "Scale Reveal")
  - `{{DESCRIPTION}}` - Brief description of the effect
  - `{{EFFECT_ID}}` - CSS class name (e.g., "scale-reveal")
  - `{{CSS_CODE}}` - The CSS code for the effect
  - `{{CONTRIBUTOR_NAME}}` - Your name or GitHub handle
  - `{{CONTRIBUTOR_ROLE}}` - Your role (Creator/Contributor)
  - `{{CONTRIBUTOR_NOTES}}` - Brief notes about your contribution

- `../styles/effect-page.css` - Shared stylesheet (linked, no changes needed)
- `style.css` - Effect stylesheet

## Steps to Add New Effect

1. Copy `index.html` to `effects/your-effect-name/index.html`
2. Add entry in `scripts/gallery.js` effects array
3. Create `style.css` for standalone use
4. Commit both files

## Panel Structure

```
Preview Panel    - Shows live hover effect
HTML Panel       - Copy-pasteable HTML structure  
CSS Panel        - Copy-pasteable CSS code
Credits Panel    - Contributor information
```