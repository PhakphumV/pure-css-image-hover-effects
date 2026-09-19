# Effect Metadata Schema

Every effect directory contains a `meta.json` that drives the catalog
generator (#8) and the contract validator (#13). This document is the
authoritative spec; `schemas/meta.schema.json` is the machine‑readable
version (Draft 2020‑12).

## Required fields

| Field | Type | Notes |
|-------|------|-------|
| `id` | string | Stable identifier (e.g. `"zoom-in"`). Lowercase, hyphenated. Must match the directory slug. |
| `slug` | string | Same as `id`. Kept separate so consumers can use it as a URL segment without depending on `id`. |
| `title` | string | Human‑readable name (e.g. `"Zoom In"`). |
| `category` | enum | One of the 13 categories below. |
| `description` | string | One sentence explaining what the effect does. ≤ 120 chars. |
| `tags` | string[] | Free‑form tags for search/filter (e.g. `["scale", "simple"]`). |
| `complexity` | enum | `"simple"` or `"advanced"`. Drives the catalog grouping. |
| `css_features` | string[] | CSS features used (e.g. `["transform", "transition"]`). For documentation, not validation. |
| `js_required` | boolean | **Always `false`**. Enforced by the schema. |
| `extra_markup` | boolean | **Always `false`**. Enforced by the schema. |
| `reduced_motion` | string | How the effect behaves under `prefers-reduced-motion: reduce`. One of: `"disabled"`, `"instant"`, `"no-change"`. |

## Categories (enum, closed)

The 13 categories from issue #5:

`zoom`, `pan`, `rotate`, `3d`, `filter`, `reveal`, `fade`, `shadow`,
`light`, `border`, `distortion`, `overlay`, `composite`.

Adding a new category requires a schema version bump.

## Example

```json
{
  "id": "zoom-in",
  "slug": "zoom-in",
  "title": "Zoom In",
  "category": "zoom",
  "description": "Smooth scale-up of the image on hover.",
  "tags": ["scale", "simple", "transform"],
  "complexity": "simple",
  "css_features": ["transform", "transition"],
  "js_required": false,
  "extra_markup": false,
  "reduced_motion": "disabled"
}
```

## Why `js_required` and `extra_markup` are in the schema

These two fields exist to make the contract (§1 and §2 of `CONTRACT.md`)
machine‑enforceable. The schema's `const: false` on both means a `meta.json`
claiming `js_required: true` will fail validation before any code runs.
