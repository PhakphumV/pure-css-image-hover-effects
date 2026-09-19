# v2.0 contract audit (issue #32)

**Date:** 2026-09-19
**Scope:** Repository-wide audit of the v2.0 effect contract. No code
or schema changes; this document is the authoritative basis for the
follow-up issues (#33–#37).

## 01. Executive summary

The v2.0 contract is **internally consistent at the document level**
but has **two structural enforcement gaps** that allow violations to
ship undetected:

1. **Descendant-selector loophole.** 9 advanced effects use CSS
   selectors of the form `.hover-effect.<slug> .<child>` (e.g.
   `.hover-effect.depth-layers .l`), which implies extra HTML
   markup that the canonical contract forbids. The `meta.json` for
   each of these declares `extra_markup: false`, contradicting the
   CSS. The validator only checks that *some* `.hover-effect.<slug>`
   selector exists; it does not verify that the effect works with
   the canonical one-wrapper-one-img markup.

2. **`pointer-events: none` mis-flag.** 9 overlay/light effects use
   `pointer-events: none` legitimately on pseudo-elements (so they
   do not block hover/focus on the underlying image). The audit
   script initially flagged these as "cursor-tracking", which is a
   false positive. No action needed; this is noted to keep the
   follow-up validator (#33) from over-flagging.

All 54 effects satisfy the **pure-CSS, no-JS** requirement and the
**`:focus-visible` mirror** requirement. The a11y baseline
(reduced-motion + prefers-contrast + prefers-reduced-transparency)
is enforced globally in `styles/base.css` and does not need per-effect
overrides.

The validator currently passes 54/54 effects, but it is **insufficient**:
it does not detect the descendant-selector class of violation
described above, and it does not detect CSS-level gallery-class
pollution.

## 02. Current canonical contract

The intended consumer-facing HTML for every effect:

```html
<div class="hover-effect EFFECT-SLUG" tabindex="0">
  <img src="image.jpg" alt="Description">
</div>
```

Every effect must:

1. Use exactly one `<div>` wrapper containing exactly one `<img>`.
2. Put the effect slug as a class on the wrapper (not on the `<img>`).
3. Work without JavaScript.
4. Require no effect-specific extra HTML (no extra `<span>`, `<div>`,
   `<figure>`, etc. inside the wrapper).
5. Allow CSS pseudo-elements on the wrapper (`::before`, `::after`).
6. Have independently copyable CSS (one `effect.css` per effect).
7. Not depend on gallery JS, DOM, or catalog implementation.
8. Provide appropriate keyboard focus behavior (`:focus-visible`
   mirrors `:hover`).
9. Follow the repository reduced-motion policy (handled globally).
10. Work with arbitrary image URLs and responsive sizing.
11. Not depend on demo filenames or gallery-only classes.
12. Declare browser/CSS feature requirements consistently in
    `meta.json` (`css_features`).
13. Require no framework or external CSS dependency.

JavaScript is permitted for gallery/navigation UI but not for the
visual effect itself.

## 03. Document consistency matrix

| Topic | CONTRACT.md | META_SCHEMA.md | BROWSER_SUPPORT.md | ACCESSIBILITY.md | CONTRIBUTING.md | README.md | Implementation | Authoritative |
|-------|-------------|---------------|--------------------|-----------------|-----------------|-----------|----------------|----------------|
| Wrapper structure | §2: "exactly one class onto a `<div>` wrapper" | n/a (enforced via validator) | n/a | n/a | "Use `.hover-effect.<slug>` selectors" | "Copy this markup into your HTML" with one `<div>` + one `<img>` | Template and 45/54 effects match | **CONTRACT.md §2 + the one-wrapper-one-img rule** |
| Extra markup | §2: "no extra wrapper elements (`<span>`, `<figure>`) may be required" | `extra_markup: false` const | n/a | n/a | "no `.js` files anywhere under `effects/<your-slug>/`" | "Copy the markup" with exactly one `<div>` + one `<img>` | 9 effects use descendant CSS selectors that imply extra markup | **CONTRACT.md §2 + `meta.json` `extra_markup: false`** — needs validator coverage |
| JavaScript | §1: "Pure CSS only — zero JavaScript" | `js_required: false` const | n/a | n/a | "no `.js` files anywhere" | "No JavaScript" | All 54 effects pass; catalog uses CSS-only filter | **CONTRACT.md §1** |
| Focus-visible | §5: "The hover state must be mirrored on `:focus-visible`" | n/a | n/a | "Every hover state is mirrored on `:focus-visible`" | "every effect must satisfy CONTRACT.md §5" | "The effect activates on `:hover` and on `:focus-visible`" | All 54 effects have `:focus-visible` mirror | **CONTRACT.md §5** |
| Reduced motion | §4: "All transitions and transforms must be suppressed when `@media (prefers-reduced-motion: reduce)` matches" | `reduced_motion` field | n/a | "transition: none, animation: none, transform: none, clip-path: none, filter: none, opacity: 1" | "reduced-motion policy" | n/a | Enforced globally in `styles/base.css` (clip-path/filter/opacity all reset) | **CONTRACT.md §4** + global base.css reset |
| Mobile / touch | §3: "Mobile and tablet hover are out of scope" | n/a | "Mobile / tablet: hover effects are out of scope" | n/a | n/a | "Mobile and tablet: Hover effects are intentionally desktop-only" | No `@media (hover: none)` guard in base.css | **CONTRACT.md §3** — guard should be added to base.css for explicitness |
| Browser support | §3: "majority of desktop browsers" | n/a | Last 2 stable Chrome/Edge/Firefox/Safari | n/a | n/a | "Works on every modern desktop browser" | Catalog filter uses `body:has()` (Chrome 105+, FF 121+, Safari 15.4+) | **BROWSER_SUPPORT.md** |
| External dependencies | §6: "self-contained per-effect directories" | n/a | "no framework/external CSS dependency" | n/a | "no external dependencies" | "No JavaScript. Works on every modern desktop browser." | No external deps in any effect | **CONTRACT.md §6** |
| Gallery vs effect | (silent) | n/a | n/a | n/a | (silent) | (silent) | Catalog page uses `body:has()` and CSS Grid for filter; effects do not reference catalog classes | **The contract is silent; needs explicit wording** (see §13) |

**Contradictions / gaps found:**

- **Extra markup (high):** CONTRACT.md §2 mentions `<span>` and
  `<figure>` but does not mention child `<div>` elements. The 9
  effects with descendant selectors use single-letter child classes
  (`.l`, `.s`, `.g`, `.f`, `.r`, `.c`) that imply a child `<div>`
  with that class. **Authoritative rule:** "no child elements of any
  kind inside the wrapper except `<img>`". CONTRACT.md §2 needs to
  be tightened; see §12.

- **Mobile / touch (low):** The contract says mobile/tablet is out of
  scope, but `styles/base.css` does not contain an explicit
  `@media (hover: none)` guard. The current behavior is correct
  (CSS pseudo-classes just don't match on touch) but the intent
  should be documented in CSS.

- **Gallery isolation (high):** The contract is silent on what
  gallery behavior is allowed. The current implementation correctly
  separates gallery (catalog page) from effect (per-effect page),
  but the contract must say this explicitly so a future contributor
  does not couple them.

## 04. Effect-by-effect compliance matrix

Status legend:

- **COMPLIANT** — passes every contract clause with the canonical
  one-wrapper-one-img markup.
- **PARTIAL** — passes the validator and basic checks but references
  descendant CSS selectors that imply extra HTML, contradicting
  `meta.json: extra_markup: false`.
- **UNCLEAR** — needs human review (effect is large, has many
  pseudo-elements, or uses advanced CSS that may have subtle
  contract implications).
- **DUPLICATE/OVERLAP** — visually near-identical to another effect
  and could be merged.

The "Flags" column lists specific issues. A dash (—) means no
specific issue beyond the status itself.

| Effect | Status | Flags | Action |
|--------|--------|-------|--------|
| zoom-in | COMPLIANT | — | Keep |
| zoom-out | COMPLIANT | — | Keep |
| zoom-brightness | COMPLIANT | — | Keep |
| zoom-in-slowmo | COMPLIANT | — | Keep |
| zoom-rotate | COMPLIANT | — | Keep |
| point-zoom | COMPLIANT | — | Keep |
| quick-zoom | COMPLIANT | — | Keep |
| horizontal-zoom-n-pan | COMPLIANT | — | Keep |
| vertical-zoom-n-pan | COMPLIANT | — | Keep |
| bounce-bottom | COMPLIANT | — | Keep |
| bounce-top | COMPLIANT | — | Keep |
| bounce-left | COMPLIANT | — | Keep |
| bounce-right | COMPLIANT | — | Keep |
| slide-reveal | COMPLIANT | — | Keep |
| slide-reveal-right | COMPLIANT | — | Keep |
| flip-horizontal | COMPLIANT | — | Keep |
| flip-vertical | COMPLIANT | — | Keep |
| rotate-3d | COMPLIANT | — | Keep |
| tilt-shadow | COMPLIANT | — | Keep |
| blur-sharpen | COMPLIANT | — | Keep |
| contrast-punch | COMPLIANT | — | Keep |
| contrast-soften | COMPLIANT | — | Keep |
| duotone | COMPLIANT | — | Keep |
| fade-colorize | COMPLIANT | — | Keep |
| invert-flash | COMPLIANT | — | Keep |
| sepia-in | COMPLIANT | — | Keep |
| clip-reveal | COMPLIANT | — | Keep |
| glow-border | COMPLIANT | — | Keep |
| shadow-drop | COMPLIANT | — | Keep |
| shadow-lift | COMPLIANT | — | Keep |
| neon-pulse | COMPLIANT | — | Keep |
| corner-frame | COMPLIANT | — | Keep (largest simple effect: 14 pseudo-elements, but all on the wrapper) |
| overlay-fade-in-neon-grid | COMPLIANT | — | Keep |
| ink-drop | COMPLIANT | — | Keep (pseudo-elements only on wrapper) |
| color-splash | COMPLIANT | — | Keep (pseudo-elements only on wrapper) |
| refraction-lens | COMPLIANT | — | Keep (uses `pointer-events: none` on pseudo, legitimate) |
| glass-mosaic | COMPLIANT | — | Keep (uses `pointer-events: none` on pseudo, legitimate; class is one letter but it is on the wrapper) |
| magnetic-glow | COMPLIANT | — | Keep (uses `pointer-events: none` on pseudo, legitimate) |
| shine-sweep | COMPLIANT | — | Keep (uses `pointer-events: none` on pseudo, legitimate) |
| vignette | COMPLIANT | — | Keep (uses `pointer-events: none` on pseudo, legitimate) |
| radial-in | COMPLIANT | — | Keep (uses `pointer-events: none` on pseudo, legitimate) |
| radial-out | COMPLIANT | — | Keep (uses `pointer-events: none` on pseudo, legitimate) |
| rectangle-in | COMPLIANT | — | Keep (uses `pointer-events: none` on pseudo, legitimate) |
| rectangle-out | COMPLIANT | — | Keep (uses `pointer-events: none` on pseudo, legitimate) |
| depth-layers | **PARTIAL** | descendant selector `.hover-effect.depth-layers .l` | **Rewrite** (issue #34) |
| glitch-shift | **PARTIAL** | descendant selector `.hover-effect.glitch-shift .s` | **Rewrite** (issue #34) |
| glitch-slice | **PARTIAL** | descendant selector `.hover-effect.glitch-slice .s` | **Rewrite** (issue #34) |
| holographic-shimmer | **PARTIAL** | descendant selector `.hover-effect.holographic-shimmer .s` | **Rewrite** (issue #34) |
| liquid-morph | **PARTIAL** | descendant selector `.hover-effect.liquid-morph .r` | **Rewrite** (issue #34) |
| magnetic-tilt | **PARTIAL** | descendant selector `.hover-effect.magnetic-tilt .g` | **Rewrite** (issue #34) |
| origami-fold | **PARTIAL** | descendant selector `.hover-effect.origami-fold .f` | **Rewrite** (issue #34) |
| parallax-tilt | **PARTIAL** | descendant selector `.hover-effect.parallax-tilt .g` | **Rewrite** (issue #34) |
| prism-split | **PARTIAL** | descendant selector `.hover-effect.prism-split .c` | **Rewrite** (issue #34) |
| swipe-reveal | **UNCLEAR** | 14 pseudo-elements, large CSS (1959 bytes) | **Human review** (issue #34) |

**Totals:** 44 COMPLIANT, 9 PARTIAL, 1 UNCLEAR, 0 NON-COMPLIANT,
0 DUPLICATE/OVERLAP.

## 05. Known violations with exact file/class references

The 9 PARTIAL effects all share the same pattern: they use
descendant CSS selectors that imply a child `<div>` inside the
wrapper, contradicting `meta.json: extra_markup: false`. The
canonical contract (§2) requires the wrapper to contain only an
`<img>`. The validator does not detect this.

| Effect | File | Selector | Implied markup |
|--------|------|----------|----------------|
| depth-layers | `effects/depth-layers/effect.css` | `.hover-effect.depth-layers .l` | `<div class="l">` |
| glitch-shift | `effects/glitch-shift/effect.css` | `.hover-effect.glitch-shift .s` | `<div class="s">` |
| glitch-slice | `effects/glitch-slice/effect.css` | `.hover-effect.glitch-slice .s` | `<div class="s">` |
| holographic-shimmer | `effects/holographic-shimmer/effect.css` | `.hover-effect.holographic-shimmer .s` | `<div class="s">` |
| liquid-morph | `effects/liquid-morph/effect.css` | `.hover-effect.liquid-morph .r` | `<div class="r">` |
| magnetic-tilt | `effects/magnetic-tilt/effect.css` | `.hover-effect.magnetic-tilt .g` | `<div class="g">` |
| origami-fold | `effects/origami-fold/effect.css` | `.hover-effect.origami-fold .f` | `<div class="f">` |
| parallax-tilt | `effects/parallax-tilt/effect.css` | `.hover-effect.parallax-tilt .g` | `<div class="g">` |
| prism-split | `effects/prism-split/effect.css` | `.hover-effect.prism-split .c` | `<div class="c">` |

**Root cause:** during the v2 migration (issue #7), the CSS was
mechanically rewritten to scope selectors to `.hover-effect.<slug>`,
but descendant selectors from the pre-rebuild markup survived
because the migration script did not strip them. The `meta.json`
fields were generated from heuristics and declared
`extra_markup: false` without verifying the CSS against the
canonical markup.

**Why these passed validation:** `scripts/validate_effects.py`
checks only that *some* `.hover-effect.<slug>` selector exists. It
does not check that the effect is self-contained with the canonical
markup.

**Resolution path (issue #34):** each of these effects must be
rewritten so the layered/glitch/morph effect is achieved using only
the wrapper and its child `<img>` plus pseudo-elements. If a
visually equivalent result cannot be achieved without extra markup,
the effect should be retired and replaced (not silently weakened).

## 06. Validator coverage gap analysis

| Contract rule | Documented? | Validator checks it? | Current effects comply? | Follow-up needed |
|---------------|-------------|----------------------|------------------------|------------------|
| §1 Pure CSS, zero JS | Yes (CONTRACT.md §1) | Yes: `js_required: false` const, `<script>` scan, inline handler scan (with the `(?<=[\s<])on[a-z]+\s*=` regex), `.js` file scan | Yes (54/54) | None |
| §2 Class on `<div>` wrapper | Yes (CONTRACT.md §2) | Partially: checks `meta.json` `id`/`slug` match dir name; checks that *some* `.hover-effect.<slug>` selector exists | **No (9 effects violate)** | **Yes** — add a check that no descendant selector of the form `.hover-effect.<slug> .<x>` exists (or, if it does, that `meta.extra_markup` is `true` and the HTML in `index.html` actually contains the required child element) |
| §2 No extra markup | Yes (CONTRACT.md §2, `meta.extra_markup: false`) | Partially: schema enforces `false`, but does not cross-check against CSS descendant selectors | **No (9 effects declare `false` but CSS implies children)** | **Yes** — same as above |
| §3 Works on majority of desktop browsers | Yes (CONTRACT.md §3, BROWSER_SUPPORT.md) | No | Yes (manual claim) | Yes — feature detection could be added (e.g., reject effects whose `css_features` include `backdrop-filter` without a `fallback` field, once the schema is extended) |
| §4 Reduced-motion | Yes (CONTRACT.md §4, ACCESSIBILITY.md) | No (relies on global `styles/base.css` reset) | Yes (verified by reading base.css) | Optional: add a check that the effect does not override `@media (prefers-reduced-motion: reduce)` with `!important` that would defeat the global reset |
| §5 `:focus-visible` mirror | Yes (CONTRACT.md §5) | Yes: regex `:focus-visible` in effect.css | Yes (54/54) | None |
| §6 Self-contained | Yes (CONTRACT.md §6) | Partially: checks no `.js` files; does not check no `@import`, no cross-effect CSS reference | Yes (manual claim) | Yes — add `@import` ban and a check that no effect references another effect's CSS file |
| Gallery isolation | No (contract is silent) | No | Yes (manual claim) | Yes — see §08 |
| Browser-feature graceful degradation | Partial (BROWSER_SUPPORT.md) | No | Unknown (no tests) | Yes — for `backdrop-filter`, `clip-path`, `body:has()`, define explicit fallback behavior and check effects don't assume support |

**False positives the validator does NOT produce (good):**

- The earlier `JS_RE` regex (`on\w+\s*=`) matched `content=`,
  `controls=`, and other HTML attributes starting with `on`. Fixed
  in commit `5729ac5` (rebuild/13-validation) by requiring `on` to
  be a standalone attribute via `(?<=[\s<])on[a-z]+\s*=`. The
  validator now correctly distinguishes event handlers from
  legitimate attributes.

## 07. Template and README findings

**Template (`effects/_template/`):**

- ✅ `effect.css` template correctly shows `.hover-effect.<effect-class>`
  selectors with both `:hover` and `:focus-visible` mirrors.
- ✅ `index.html` template shows the canonical one-wrapper-one-img
  markup.
- ✅ `meta.json` template shows all required fields.
- ⚠ The template does not explicitly state that **child elements
  inside the wrapper are forbidden** beyond the `<img>`. The
  README and CONTRIBUTING should make this unambiguous.
- ⚠ The template's `effect.css` does not include a comment about
  the global `prefers-reduced-motion` reset living in `base.css`.
  Contributors should know not to duplicate it.

**README.md:**

- ✅ Usage section shows the correct canonical markup.
- ✅ Repository layout diagram correctly shows `effect.css` /
  `index.html` / `meta.json` per effect.
- ⚠ The "Adding a new effect" section does not warn against the
  descendant-selector anti-pattern. A future contributor could
  copy a PARTIAL effect's CSS and reintroduce the violation.

**Recommended additions** (not implemented in this issue):

1. In `effects/_template/effect.css`, add a comment block at the top:
   ```css
   /*
    * Rules:
    * - selectors target `.hover-effect.<slug>` (wrapper) and
    *   `.hover-effect.<slug> > img` (child image) ONLY
    * - pseudo-elements `::before` / `::after` on the wrapper are allowed
    * - NO descendant selectors like `.hover-effect.<slug> .<child>`
    *   (those would require extra HTML and violate CONTRACT.md §2)
    * - NO `@import` (self-contained per CONTRACT.md §6)
    * - mirror `:hover` to `:focus-visible` (CONTRACT.md §5)
    */
   ```
2. In README.md "Adding a new effect", add a paragraph:
   > Do not add child elements inside the wrapper beyond the
   > `<img>`. If you need layered effects, use `::before` /
   > `::after` pseudo-elements or rewrite using transforms on the
   > `<img>` itself.

## 08. Gallery isolation findings

The catalog page (`index.html`, generated by `scripts/build_catalog.py`,
styled by `styles/catalog.css`) is **cleanly separated** from the
per-effect pages. Specifically:

- ✅ No effect's `effect.css` references any class from
  `styles/catalog.css` (`.card`, `.card__media`, `.filter__pill`,
  `.section__title`, etc.).
- ✅ No effect's `index.html` references any catalog-only class or
  element.
- ✅ The catalog filter is CSS-only via `body:has(input[name="cat"][value="X"]:checked)`
  — no JS.
- ✅ Each catalog card is a real `<a>` linking to the effect's
  `index.html`, so the gallery is a navigable catalog, not a
  required runtime dependency.
- ⚠ The catalog uses `body:has(...)`, which is a relatively new
  selector (Chrome 105+, Firefox 121+, Safari 15.4+). This is
  documented in `BROWSER_SUPPORT.md` but should also be called out
  in `CONTRACT.md` as an acceptable modern CSS feature.

**Contract gap:** the contract is currently silent on what gallery
behavior is allowed. The implementation is correct, but the contract
must explicitly state:

> Gallery behavior (catalog page, filtering, navigation, code
> display, demo image switching) is OUT OF SCOPE for the effect
> contract. An effect must not depend on any gallery-only class,
> attribute, DOM element, or behavior. The catalog may use modern
> CSS (including `body:has()`, CSS Grid, `color-mix()`) without
> this imposing any requirement on individual effects.

## 09. Accessibility findings

`styles/base.css` correctly implements all four media queries
documented in `ACCESSIBILITY.md`:

- `prefers-reduced-motion: reduce` cancels `transition`, `animation`,
  `transform`, `clip-path`, `filter`, `opacity` on `.hover-effect`
  and its `<img>`. ✅
- `prefers-contrast: more` thickens `:focus-visible` from 3px to
  4px. ✅
- `prefers-reduced-transparency: reduce` replaces the catalog's
  sticky filter bar's `backdrop-filter` with a solid fill. ✅
- `:focus-visible` ring is `outline: 3px solid var(--color-primary)`
  with `outline-offset: 2px`. ✅

**Reconciliation with CONTRACT.md §3 and §4:**

- The contract says mobile/tablet is out of scope. The current
  implementation relies on the natural cascade (hover doesn't match
  on touch) but does not contain an explicit `@media (hover: none)`
  guard. **Recommended:** add the guard to `base.css` for
  explicitness and to match the contract's intent.

- The contract §5 requires `:focus-visible` mirroring `:hover`. All
  54 effects comply. **No action.**

- `tabindex="0"` is set on the wrapper in every `index.html` demo
  template. The contract is silent on whether `tabindex` belongs to
  the library or the consumer. **Recommended:** the library should
  document in `README.md` that the consumer is responsible for
  `tabindex` (the effect itself does not force the wrapper to be
  focusable, because some consumers may want a different focus
  strategy). The current per-effect demo pages should drop the
  `tabindex="0"` from the canonical example, or keep it but
  document it as a demo-only convenience.

## 10. Browser-support findings

`BROWSER_SUPPORT.md` correctly enumerates the CSS features the
library uses. The actual usage in the codebase matches the
documented matrix:

| Feature | In docs? | Actually used? | Where |
|---------|----------|-----------------|-------|
| `transform` | Yes | Yes | Most effects |
| `transition` | Yes | Yes | All effects |
| `filter` | Yes | Yes | blur-sharpen, duotone, sepia-in, etc. |
| `backdrop-filter` | Yes | Yes | glass-mosaic (used on `::before`) |
| `clip-path` | Yes | Yes | clip-reveal, swipe-reveal |
| `perspective` / 3d transforms | Yes | Yes | depth-layers, flip-horizontal, rotate-3d, etc. |
| `@keyframes` / `animation` | Yes | Yes | invert-flash, neon-pulse, glitch-shift, etc. |
| `::before` / `::after` | Yes | Yes | shine-sweep, glass-mosaic, etc. |
| `@media (hover: hover)` / `(hover: none)` | Partial | Implicit (no explicit guard in base.css) | Should be added |
| `@media (prefers-reduced-motion)` | Yes | Yes | `styles/base.css` |
| `@media (prefers-contrast)` | Yes | Yes | `styles/base.css` |
| `@media (prefers-reduced-transparency)` | Yes | Yes | `styles/catalog.css` |
| `:focus-visible` | Yes | Yes | `styles/base.css` and all effects |
| `body:has(...)` | Yes | Yes | `styles/catalog.css` |
| `@supports` | Documented as NOT used | Not used | n/a |
| Vendor prefixes | Documented as NOT used | Not used | n/a |
| Houdini (`@property`, paint worklets) | Documented as NOT used | Not used | n/a |
| Scroll-driven animations | Documented as NOT used | Not used | n/a |

**Recommendation:** `BROWSER_SUPPORT.md` should add a paragraph
on **graceful degradation** for `backdrop-filter` and `body:has()`.
The current implementation degrades gracefully (the catalog bar
becomes opaque; the catalog filter falls back to "all effects"),
but this should be explicit.

## 11. Decisions that must be made

The following decisions block the follow-up issues. They should be
made by the repo owner, not by the auditor:

1. **Descendant-selector policy:** when an effect's CSS uses a
   descendant selector that implies extra markup, should the
   effect be (a) rewritten to use pseudo-elements only, (b)
   retired if no equivalent rewrite exists, or (c) grandfathered
   with `extra_markup: true`? **Recommendation: (a) or (b), never
   (c)** — grandfathering contradicts the contract and invites
   future drift.

2. **`pointer-events: none` on pseudo-elements:** confirm that
   this is allowed (it is — pseudo-elements do not receive pointer
   events anyway in most cases, but the explicit declaration is
   defensive). **Recommendation: explicitly allow.**

3. **`tabindex` policy:** should the library force `tabindex="0"`
   on the wrapper, or leave it to the consumer? **Recommendation:
   leave to consumer.** The demo pages may keep `tabindex="0"` as
   a convenience, but the contract should not require it.

4. **`@media (hover: none)` guard:** should the guard be added
   to `styles/base.css` to make the mobile-out-of-scope rule
   explicit? **Recommendation: yes, for documentation as much as
   behavior.**

5. **Schema extension:** should `meta.json` gain a
   `browser_fallbacks` field listing each advanced CSS feature
   and its graceful-degradation behavior? **Recommendation: yes,
   optional field.**

6. **`swipe-reveal` review:** the effect is flagged UNCLEAR (14
   pseudo-elements, 1959 bytes of CSS). Decide whether it stays or
   is simplified.

## 12. Recommended contract wording

For `CONTRACT.md §2` (replace the existing "no extra wrapper
elements" sentence):

> The consumer-facing markup is exactly one `<div>` wrapper
> containing exactly one `<img>`:
>
> ```html
> <div class="hover-effect EFFECT-SLUG" tabindex="0">
>   <img src="image.jpg" alt="Description">
> </div>
> ```
>
> The effect's CSS may target only:
> - `.hover-effect.EFFECT-SLUG` (the wrapper)
> - `.hover-effect.EFFECT-SLUG > img` (the child image)
> - `.hover-effect.EFFECT-SLUG::before` and `::after` (pseudo-elements
>   on the wrapper)
>
> The effect's CSS **must not** target any other descendant
> selector (e.g. `.hover-effect.EFFECT-SLUG .<child>`). Such
> selectors would require extra HTML inside the wrapper, which is
> forbidden.
>
> The wrapper may carry a `tabindex` attribute if the consumer wants
> keyboard focus, but the library does not require it.

Add a new clause (between current §6 and end):

> §7. Gallery isolation. The catalog page, filtering, navigation,
> code display, and demo image switching are out of scope for the
> effect contract. An effect must not depend on any gallery-only
> class, attribute, DOM element, or behavior. The catalog may use
> modern CSS (including `body:has()`, CSS Grid, `color-mix()`)
> without imposing any requirement on individual effects.

## 13. Follow-up implementation issues

1. **Issue #33 — Strengthen automated contract validation.** Add
   checks for: (a) no descendant selectors of the form
   `.hover-effect.<slug> .<x>`, (b) no `@import`, (c) no cross-effect
   CSS reference, (d) optional `browser_fallbacks` field validation.
2. **Issue #34 — Rewrite/replace the 9 PARTIAL effects.** Each of
   depth-layers, glitch-shift, glitch-slice, holographic-shimmer,
   liquid-morph, magnetic-tilt, origami-fold, parallax-tilt,
   prism-split must be rewritten to use only the wrapper + `<img>`
   + pseudo-elements, or retired.
3. **Issue #35 — Reconcile accessibility and reduced-motion
   baseline.** Add the `@media (hover: none)` guard to
   `styles/base.css`. Document the `tabindex` policy.
4. **Issue #36 — Perform visual, responsive, and cross-browser QA.**
   Manual testing across the BROWSER_SUPPORT matrix, especially
   for `backdrop-filter` (glass-mosaic) and `body:has()` (catalog
   filter).
5. **Issue #37 — Reconcile metadata, taxonomy, duplicates, and
   catalog.** Review `swipe-reveal` (UNCLEAR). Decide whether any
   effects are visually duplicates (e.g. `slide-reveal` vs
   `slide-reveal-right`).

## 14. Explicit list of effects to rewrite, replace, merge, or retire

**Rewrite (9, all PARTIAL):**

| Effect | Action | Reason |
|--------|--------|--------|
| depth-layers | Rewrite without `.l` child | Descendant selector violates §2 |
| glitch-shift | Rewrite without `.s` child | Descendant selector violates §2 |
| glitch-slice | Rewrite without `.s` child | Descendant selector violates §2 |
| holographic-shimmer | Rewrite without `.s` child | Descendant selector violates §2 |
| liquid-morph | Rewrite without `.r` child | Descendant selector violates §2 |
| magnetic-tilt | Rewrite without `.g` child | Descendant selector violates §2 |
| origami-fold | Rewrite without `.f` child | Descendant selector violates §2 |
| parallax-tilt | Rewrite without `.g` child | Descendant selector violates §2 |
| prism-split | Rewrite without `.c` child | Descendant selector violates §2 |

**Human review (1, UNCLEAR):**

| Effect | Action | Reason |
|--------|--------|--------|
| swipe-reveal | Review | 14 pseudo-elements, 1959 bytes — may be overscoped |

**Retire / replace (0):** no effect is so broken that it must be
removed rather than rewritten.

**Merge candidates (2, possible visual overlap):**

| Effects | Action | Reason |
|---------|--------|--------|
| slide-reveal / slide-reveal-right | Review | Possibly identical except for transform direction |
| horizontal-zoom-n-pan / vertical-zoom-n-pan | Keep separate | Different transform axes are intentional |

## 15. Final definition of contract compliant

An effect is **CONTRACT COMPLIANT** if and only if all of the following hold:

1. `effects/<slug>/` contains exactly three files: `effect.css`,
   `index.html`, `meta.json`.
2. `meta.json` validates against `schemas/meta.schema.json` with
   `js_required: false` and `extra_markup: false`.
3. `effect.css` contains a selector targeting `.hover-effect.<slug>`
   and (if it animates the image) `.hover-effect.<slug> > img`.
4. `effect.css` contains NO descendant selector of the form
   `.hover-effect.<slug> .<child>`.
5. `effect.css` mirrors `:hover` to `:focus-visible`.
6. `effect.css` contains no `@import` and does not reference any
   other effect's CSS file.
7. `index.html` contains exactly one `<div class="hover-effect <slug>">`
   wrapper and exactly one `<img>` inside it, plus the page chrome
   (header, preview panel, code panel). No `<script>`, no inline
   event handlers.
8. `index.html` validates as HTML5.
9. The effect renders correctly with `prefers-reduced-motion: reduce`
   set (verified by the global reset in `styles/base.css`).
10. The effect renders correctly in every browser in
    `BROWSER_SUPPORT.md`'s baseline, or degrades gracefully for any
    advanced feature used.

This definition is enforceable by a strengthened validator
(issue #33). The current validator enforces clauses 1, 2, 5, and 7
only.

---

**End of audit.**
