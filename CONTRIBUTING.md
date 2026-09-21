# Contributing

This is a plain HTML/CSS site. There is no frontend framework, no bundler,
and no runtime build dependency. Node.js is only used for contributor
tooling that keeps the metadata catalog and generated catalogue sections
in sync.

## Source files (edit these)

The authoritative content lives in:

| Path | What it is |
| --- | --- |
| `catalog/effects.json` | Canonical metadata for every effect: category, name, slug, description. The single source of truth for the catalogue. |
| `effects/<cat>/<cat>.css` | CSS for every effect in the category. Each effect is a `.hover-effect.<slug>` selector block. |
| `effects/<cat>/<cat>-<slug>.html` | One demo page per effect. |
| `effects/template.html` | The shared demo-page template. |
| `effects/template.css` | Shared styles for demo pages. |
| `src/index.html` | The homepage source. The catalogue section is regenerated from `catalog/effects.json`. |
| `src/styles/`, `src/assets/` | Reserved for future shared assets and stylesheets. |
| `scripts/` | Build and verification scripts (pure Node.js stdlib). |
| `README.md` | Project documentation. The effect catalogue section is regenerated from `catalog/effects.json`. |
| `ARCHITECTURE.md` | Defines the source vs generated boundary. |
| `catalog/SCHEMA.md` | Documents the catalog JSON schema. |
| `.github/workflows/` | CI workflows. |

## Generated files (do not edit)

These are produced by `npm run build` and any manual change is overwritten
on the next build:

- `dist/` — the static site artifact uploaded to GitHub Pages.
- The catalogue sections of `index.html` and `README.md` between the
  `<!-- BEGIN GENERATED EFFECT CATALOG[UE] -->` and
  `<!-- END GENERATED EFFECT CATALOG[UE] -->` markers.

The catalog is regenerated from `catalog/effects.json`; the layout, paths,
and per-card structure are deterministic and come from the build scripts.
Do not edit these sections by hand — change the source files instead.

`index.html` and `README.md` themselves remain tracked because they are
small, convenient to browse on github.com, and editing the parts outside
the generated markers is a normal contributor action.

## Workflow

### Validate

```bash
npm run check
```

Verifies that:

- `catalog/effects.json` is well-formed and consistent with the
  implementations under `effects/` (12 checks).
- `index.html` is up to date with the source catalogue.
- `README.md` is up to date with the source catalogue.
- `dist/` matches a clean rebuild from source.

Each step exits non-zero on drift. Run this before opening a PR.

### Build

```bash
npm run build
```

Regenerates `index.html` (root), the `README.md` catalogue section, and
the full `dist/` directory. The build is idempotent: re-running it after
a clean run produces no further changes. Two consecutive builds produce
byte-identical output.

### Add a new effect

1. Add an entry to `catalog/effects.json` under the appropriate category:
   `{ slug, name, description }`. Slugs must be kebab-case and unique
   project-wide. Optional fields: `wrapperClasses` (extra CSS classes
   on the wrapper) and `tabindex` (keyboard focus).
2. Add the CSS block to `effects/<cat>/<cat>.css`, using the selector
   `.hover-effect.<slug>`.
3. Create `effects/<cat>/<cat>-<slug>.html` by cloning a sibling demo
   page and updating the slug/name.
4. Run `npm run build` to regenerate `index.html`, the README catalogue
   section, and `dist/`.
5. Run `npm run check` to confirm everything is in sync.
6. Commit with `Closes #N` and push.

## Deployment

GitHub Actions builds and deploys the site on every push to `main`.
The pipeline (`.github/workflows/pages.yml`) is:

```
checkout → npm ci → npm run check → npm run build
        → upload dist/ as a Pages artifact → deploy
```

The `npm run check` gate means the workflow fails before any deployment
if the catalog is inconsistent, the catalogue section in `index.html`
or `README.md` has drifted, or `dist/` is out of date. A broken source
tree cannot reach production.

One-time setup: in the repository's Settings → Pages, set **Source** to
**GitHub Actions**. Until that is set, GitHub Pages will continue to
serve the branch root, and the `pages.yml` workflow will appear to
succeed without effect.

A second workflow, `.github/workflows/catalog-check.yml`, runs
`npm run check` on every push and pull request so PRs get the same
verification without a deploy.

## Conventions

- **Atomic commits.** One effect per commit, with `feat(<scope>):` or
  `fix(<scope>):` prefix.
- **Conventional commit messages.** Use the scope of the affected
  category (`feat(zoom): ...`, `fix(reveal): ...`).
- **No manual edits to generated output.** If a build is wrong, fix the
  source and re-run the build.
- **No new runtime dependencies.** The project ships plain HTML and
  CSS. Build-time tooling uses only Node.js standard library.

## Local development

```bash
npm ci                 # install (no runtime deps; this is a no-op today)
npm run check          # validate everything
npm run build          # regenerate outputs
```

To preview the generated site locally:

```bash
cd dist && python3 -m http.server 8000
# then open http://localhost:8000/
```
