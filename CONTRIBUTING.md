# Contributing to Pure CSS Image Hover Effects

Thank you for your interest in contributing. This guide covers the v2.0
contract-driven structure. The pre-rebuild structure (legacy `style.css`,
`gallery.js`, `effects-manifest.js`) is fully retired.

## Before you start

Read these four documents. Every contribution is measured against them:

1. **[CONTRACT.md](CONTRACT.md)** — the six non-negotiable rules every
   effect must satisfy (pure CSS, class on `<div>`, desktop-first,
   reduced-motion, `:focus-visible`, self-contained).
2. **[META_SCHEMA.md](META_SCHEMA.md)** — the 11 required fields in
   every `effects/<slug>/meta.json`.
3. **[BROWSER_SUPPORT.md](BROWSER_SUPPORT.md)** — the support baseline
   (last 2 stable versions of Chrome/Edge/Firefox/Safari, desktop only)
   and the CSS features in/out of scope.
4. **[ACCESSIBILITY.md](ACCESSIBILITY.md)** — the four media queries the
   library honors and what each does.

If your change violates any of these, CI will reject it.

## Adding a new effect

1. Copy `effects/_template/` to `effects/<your-slug>/`.
2. Edit the three files:
   - `effect.css` — replace `<effect-class>` and define the hover state.
     Use `.hover-effect.<slug>` selectors and mirror `:hover` to
     `:focus-visible`.
   - `index.html` — replace `<Title>`, `<slug>`, and the description.
   - `meta.json` — fill every field. `category` must be one of the 13
     enum values in `META_SCHEMA.md`. `js_required` and `extra_markup`
     MUST stay `false`.
3. Validate locally:
   ```bash
   python3 scripts/validate_effects.py
   python3 scripts/build_catalog.py
   ```
   Both must succeed. The validator enforces the contract and schema;
   the catalog builder proves the page is byte-deterministic.
4. Open a PR. CI will re-run the validator and the catalog
   determinism check.

## Changing the contract, schema, or browser policy

These are rare, deliberate changes. Open an issue first that explains:

1. Which rule changes.
2. Why the current rule no longer holds.
3. Which existing effects (if any) would need to change.
4. Migration path for downstream users.

Changes here ship as their own PR with an updated `CHANGELOG.md` entry.

## Pull request checklist

- [ ] `python3 scripts/validate_effects.py` passes locally
- [ ] `python3 scripts/build_catalog.py` produces a byte-identical `index.html`
      (the CI job diffs the output to enforce this)
- [ ] `meta.json` validates against `schemas/meta.schema.json`
- [ ] `effect.css` uses `.hover-effect.<slug>` selectors
- [ ] `effect.css` mirrors `:hover` to `:focus-visible`
- [ ] `index.html` contains no `<script>` or inline event handlers
- [ ] No `.js` files anywhere under `effects/<your-slug>/`
- [ ] Commit message follows Conventional Commits
      (feat / fix / docs / chore / refactor)

## Commit message style

Conventional Commits, one logical change per commit. Examples:

```
feat(effects): add depth-zoom effect
fix(base): cancel clip-path under reduced-motion
docs: clarify contract clause 4
chore(release): tag v2.1.0
```

## License

By contributing, you agree that your contributions are licensed under
the project's MIT license.
