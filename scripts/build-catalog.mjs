#!/usr/bin/env node
//
// Generates the catalogue portion of index.html from catalog/effects.json,
// then splices it back into index.html between the generated-content
// boundary markers.
//
// Usage:
//   node scripts/build-catalog.mjs                       # catalogue HTML to stdout
//   node scripts/build-catalog.mjs --check              # exit 0 if index.html is up to date, 1 otherwise
//   node scripts/build-catalog.mjs --apply              # rewrite index.html in place
//
// Boundary markers in index.html:
//
//   <!-- BEGIN GENERATED EFFECT CATALOG -->
//   <section>...</section>
//   ...
//   <!-- END GENERATED EFFECT CATALOG -->
//
// The markers are required. Run --apply once after editing them in. The
// generator replaces ONLY the content between the markers; everything
// outside (header, aside, </main>, footer) is preserved byte-for-byte.
//
// The generator is deterministic: output depends only on
// catalog/effects.json and the strings here, with no timestamps or
// random IDs. Category and effect order are taken from array position.
//

import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, '..');
const CATALOG_PATH = resolve(ROOT, 'catalog', 'effects.json');
const INDEX_PATH = resolve(ROOT, 'index.html');

const BEGIN_MARK = '<!-- BEGIN GENERATED EFFECT CATALOG -->';
const END_MARK = '<!-- END GENERATED EFFECT CATALOG -->';

const IMAGE_BASE = 'https://picsum.photos/seed';

// Minimal HTML escaping for text inserted into HTML.
const ESCAPE_MAP = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ESCAPE_MAP[c]);
}

function renderCategory(cat) {
  const catSlug = cat.slug;
  const lines = [];
  lines.push('  <section>');
  lines.push(`    <h2>${escapeHtml(cat.name)}</h2>`);
  lines.push(`    <p>${cat.effects.length} effects</p>`);
  lines.push('    <div class="grid">');
  for (const eff of cat.effects) {
    // Default wrapper classes: ["hover-effect", <slug>]. Effects that
    // intentionally use a chained-class selector (e.g.
    // .hover-effect.high-contrast.focus) declare their full class list
    // via the optional `wrapperClasses` field.
    const classes = ['hover-effect', ...(eff.wrapperClasses ?? [eff.slug])];
    const wrapperAttrs = [`class="${classes.join(' ')}"`];
    if (eff.tabindex !== undefined) wrapperAttrs.push(`tabindex="${eff.tabindex}"`);
    lines.push('      <article class="card">');
    lines.push(`        <a href="effects/${catSlug}/${eff.slug}.html">`);
    lines.push('          <div class="demo">');
    lines.push(`            <div ${wrapperAttrs.join(' ')}>`);
    lines.push(`              <img src="${IMAGE_BASE}/${eff.slug}/600/450" alt="${escapeHtml(eff.name)}" loading="lazy">`);
    lines.push('            </div>');
    lines.push('          </div>');
    lines.push('          <div class="card-body">');
    lines.push(`            <h3>${escapeHtml(eff.name)}</h3>`);
    lines.push('          </div>');
    lines.push('        </a>');
    lines.push('      </article>');
  }
  lines.push('    </div>');
  lines.push('  </section>');
  return lines.join('\n');
}

function buildCatalogue() {
  const catalog = JSON.parse(readFileSync(CATALOG_PATH, 'utf8'));
  return catalog.categories.map(renderCategory).join('\n');
}

function applyToIndex(catalogue, indexHtml) {
  const beginIdx = indexHtml.indexOf(BEGIN_MARK);
  const endIdx = indexHtml.indexOf(END_MARK);
  if (beginIdx === -1) {
    throw new Error(`index.html is missing the BEGIN marker: ${BEGIN_MARK}`);
  }
  if (endIdx === -1) {
    throw new Error(`index.html is missing the END marker: ${END_MARK}`);
  }
  if (endIdx < beginIdx) {
    throw new Error('index.html has END marker before BEGIN marker');
  }
  const before = indexHtml.slice(0, beginIdx + BEGIN_MARK.length);
  const after = indexHtml.slice(endIdx);
  // Begin marker ends with " -->"; preserve exactly one blank line, then
  // the catalogue, then one blank line before the end marker.
  return `${before}\n${catalogue}\n${after}`;
}

function main() {
  const args = new Set(process.argv.slice(2));
  const catalogue = buildCatalogue();

  if (args.has('--check')) {
    const html = readFileSync(INDEX_PATH, 'utf8');
    const expected = applyToIndex(catalogue, html);
    if (html === expected) {
      console.log('index.html is up to date.');
      return;
    }
    console.error('index.html is OUT OF DATE. Run `node scripts/build-catalog.mjs --apply`.');
    process.exit(1);
  }

  if (args.has('--apply')) {
    const html = readFileSync(INDEX_PATH, 'utf8');
    const next = applyToIndex(catalogue, html);
    if (next !== html) writeFileSync(INDEX_PATH, next, 'utf8');
    return;
  }

  // Default: write the catalogue HTML to stdout (no markers).
  process.stdout.write(catalogue + '\n');
}

main();
