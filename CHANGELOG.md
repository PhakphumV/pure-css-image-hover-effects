# Changelog

All notable changes to this project are documented here. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and
the project adheres to [Semantic Versioning](https://semver.org/).

## [2.0.0] — 2026-09-19

The v2.0 rebuild. The repo was rewritten from scratch against a new
canonical contract. Every effect, every doc, every script is new or
substantially revised. The pre-rebuild gallery, manifest, and per-effect
README layout are fully retired.

### Added

- **CONTRACT.md** — six non-negotiable rules every effect must satisfy
  (pure CSS, class on `<div>`, desktop-first, reduced-motion,
  `:focus-visible`, self-contained).
- **META_SCHEMA.md** + **schemas/meta.schema.json** — 11 required
  metadata fields with a JSON Schema (Draft 2020-12) for validation.
- **BROWSER_SUPPORT.md** — baseline (last 2 stable versions of
  Chrome/Edge/Firefox/Safari, desktop only) and the CSS feature
  matrix (what we use, what we explicitly do not).
- **ACCESSIBILITY.md** — the four media queries the library honors
  (`prefers-reduced-motion`, `prefers-contrast`,
  `prefers-reduced-transparency`, `:focus-visible`).
- **styles/base.css** — shared rules owned by the library: the
  `.hover-effect` wrapper, the reduced-motion reset (which also
  cancels `clip-path`, `filter`, and `opacity`), the
  `:focus-visible` outline ring, the prefers-contrast thickening,
  and the prefers-reduced-transparency fallback.
- **styles/catalog.css** — the catalog page's visual layer with a
  3-card featured row, category badges on every card, and a sticky
  CSS-only category filter.
- **scripts/build_catalog.py** — deterministic, stdlib-only generator
  that reads `effects/*/meta.json` and writes a byte-stable `index.html`.
- **scripts/validate_effects.py** — contract + schema validator used
  by CI. Exit 1 on any violation.
- **.github/workflows/validate.yml** — CI job that runs the validator
  and verifies the catalog is byte-deterministic.
- **effects/_template/** — canonical template every real effect is
  copied from.
- 54 effects migrated to the contract-driven shape
  (`effect.css` + `index.html` + `meta.json`), classified into the
  13 categories (zoom, pan, rotate, 3d, filter, reveal, fade, shadow,
  light, border, distortion, overlay, composite).
- **reports/** — verification snapshots for the simple bucket (28),
  advanced bucket (26), and full audit (54/54 pass).

### Changed

- Every effect directory now contains exactly three files
  (`effect.css`, `index.html`, `meta.json`) instead of the legacy
  (`style.css`, `index.html`, `README.md`).
- Selectors are scoped to `.hover-effect.<slug>` so two effects can
  coexist on the same page without bleed.
- Every `:hover` state is mirrored to `:focus-visible` for keyboard
  users.
- `README.md` rewritten from a project overview into a copy-paste
  usage guide with a 3-step workflow and a 4-step contributor workflow.

### Removed

- `effects-manifest.js` — manual list of effects.
- `standardize_effects.py` — one-off normalization script.
- `scripts/` (old) — `effect-page.js`, `gallery.js`,
  `generate-effects-data.js`.
- `styles/effect-page.css`, `styles/gallery.css` — superseded by
  `styles/base.css` + `styles/catalog.css` + per-effect `effect.css`.
- Per-effect `README.md` files — folded into `meta.json` and the
  generated catalog.
- `effects/.template/` — dot-prefixed duplicate of the new canonical
  `effects/_template/`.
- `PROPOSED_EFFECTS.md` — stale ideas list from the pre-rebuild era.

### Fixed

- `glitch-shift` and other effects with pre-existing JS-like scanline
  pseudo-element dependencies were rewritten so the core effect works
  without any extra wrapper markup.
- The reduced-motion reset now also cancels `clip-path`, `filter`,
  and `opacity` so reveal and filter effects show the full image
  instead of leaving it half-clipped or blurred.

## [1.x] — pre-rebuild

The pre-rebuild gallery shipped ad-hoc effects with a manifest-driven
JS gallery. v1.x releases are not documented here; consult git history.
