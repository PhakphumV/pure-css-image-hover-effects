# Effect Catalog Schema

This directory holds the canonical metadata for the project's hover-effect
catalogue. The file `effects.json` is the single source of truth for
category and effect names, slugs, and descriptions; everything else in
the project (the gallery HTML, the README effect list, the individual
demo pages) is derived from this file.

## File: `effects.json`

### Top-level shape

```json
{
  "version": 1,
  "categories": [
    { "slug": "...", "name": "...", "description": "...", "effects": [ ... ] }
  ]
}
```

| Field | Type | Notes |
| --- | --- | --- |
| `version` | integer | Schema version. Bump on breaking changes. |
| `categories` | array | Ordered list. Array position is display order. |

### Category object

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `slug` | string | yes | Lowercase, hyphen-separated. Canonical identity. |
| `name` | string | yes | Display name (e.g. `"Rotate & Tilt"`). |
| `description` | string | yes | One-line category description. |
| `effects` | array | yes | Ordered list of effects in this category. |

### Effect object

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `slug` | string | yes | Lowercase, hyphen-separated. Canonical identity. Must be unique project-wide. |
| `name` | string | yes | Display name shown on cards. |
| `description` | string | yes | One-line effect description. |
| `wrapperClasses` | array of strings | no | Extra CSS classes for the wrapper, in addition to `hover-effect`. Defaults to `[<slug>]` when omitted. Use this for effects whose CSS selector is a chained-class selector (e.g. `["high-contrast", "focus"]`). |
| `tabindex` | integer | no | When set, the generated wrapper carries `tabindex="<value>"`. Use this for effects that intentionally take focus (keyboard accessibility). |

## Slug conventions

- Lowercase ASCII only.
- Hyphens (`-`) separate words. No underscores, spaces, or other punctuation.
- Match the directory and file names on disk:
  - category slug -> `effects/<slug>/<slug>.css`
  - effect slug -> `effects/<category-slug>/<slug>.html`
- Display names may use spaces, capitalization, ampersands, or hyphens
  (e.g. `"Rotate & Tilt"`, `"Counter-Clockwise"`); slugs are the
  strict form.
- Slugs are the canonical identity. Renaming a slug is a breaking change.

## What is NOT stored here

These are derived values and must never be duplicated in the catalog:

- **Display order** beyond array position — order is implied by index.
- **Category or effect counts** — derived from `effects.length`.
- **HTML paths** (e.g. `effects/zoom/zoom-in.html`) — derived from slugs.
- **CSS selectors** (e.g. `.hover-effect.zoom-in`) — derived from slugs.
- **Image URLs** — generated from a stable seed + the slug.

## Ownership

The catalog is the canonical source of catalogue metadata. Adding a new
effect, renaming one, or reordering the gallery all start with editing
`effects.json`. Build tooling (added in later issues) will consume this
file to regenerate `index.html`, the README catalogue section, and the
demo pages.

The catalog is human-edited for now (no machine populates it). Future
issues add validation and a generator pipeline.
