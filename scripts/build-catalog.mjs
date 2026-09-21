#!/usr/bin/env node
//
// Generates the catalogue portion of index.html from catalog/effects.json.
// The output is a sequence of <section> blocks, one per category, with
// effect cards derived from each effect's slug.
//
// Usage:
//   node scripts/build-catalog.mjs                 # writes to stdout
//   node scripts/build-catalog.mjs > out.html      # capture to file
//
// The generator is deterministic: output depends only on catalog/effects.json
// and the strings here, with no timestamps or random IDs. Category order and
// effect order are taken from array position in the catalog.
//

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, '..');
const CATALOG_PATH = resolve(ROOT, 'catalog', 'effects.json');

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

function main() {
  const catalog = JSON.parse(readFileSync(CATALOG_PATH, 'utf8'));
  const sections = catalog.categories.map(renderCategory);
  process.stdout.write(sections.join('\n') + '\n');
}

main();
