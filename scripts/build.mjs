#!/usr/bin/env node
//
// Assembles the static site into dist/.
//
// What this does:
//   1.  Wipes dist/ and recreates it.
//   2.  Copies src/index.html to dist/index.html, rewriting paths so
//       they resolve relative to the dist/ root.
//   3.  Copies every effect directory under effects/ to dist/effects/,
//       preserving directory structure.
//   4.  Copies any src/styles/ and src/assets/ content to dist/.
//   5.  Regenerates the catalogue section in dist/index.html from
//       catalog/effects.json, between the BEGIN/END GENERATED EFFECT
//       CATALOG markers.
//
// What this does NOT do:
//   - Touch the repository-root index.html or README.md (those are
//     maintained by build-site.mjs and build-readme.mjs, which are
//     still needed until GH Pages switches to dist/).
//   - Run any frontend bundler, minifier, or transpiler.
//   - Touch effects/ source -- it is copied verbatim.
//
// Usage:
//   node scripts/build.mjs                       # writes dist/
//   node scripts/build.mjs --check               # exit 0 if dist/ is up to date
//

import { rmSync, mkdirSync, copyFileSync, readdirSync, readFileSync, writeFileSync, existsSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, '..');
const CATALOG_PATH = join(ROOT, 'catalog', 'effects.json');
const DIST = join(ROOT, 'dist');
const EFFECTS = join(ROOT, 'effects');
const SRC = join(ROOT, 'src');
const IMAGE_BASE = 'https://picsum.photos/seed';

const BEGIN_MARK = '<!-- BEGIN GENERATED EFFECT CATALOG -->';
const END_MARK = '<!-- END GENERATED EFFECT CATALOG -->';

const ESCAPE_MAP = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ESCAPE_MAP[c]);
}

// -- catalogue rendering (mirror of build-catalog.mjs) -------------------

function renderCategory(cat) {
  const catSlug = cat.slug;
  const lines = [];
  lines.push('  <section>');
  lines.push(`    <h2>${escapeHtml(cat.name)}</h2>`);
  lines.push(`    <p>${cat.effects.length} effects</p>`);
  lines.push('    <div class="grid">');
  for (const eff of cat.effects) {
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

function buildCatalogue(catalog) {
  return catalog.categories.map(renderCategory).join('\n');
}

function applyCatalogue(html, catalogue) {
  const beginIdx = html.indexOf(BEGIN_MARK);
  const endIdx = html.indexOf(END_MARK);
  if (beginIdx === -1) throw new Error(`dist/index.html is missing ${BEGIN_MARK}`);
  if (endIdx === -1) throw new Error(`dist/index.html is missing ${END_MARK}`);
  if (endIdx < beginIdx) throw new Error('dist/index.html has END marker before BEGIN marker');
  const before = html.slice(0, beginIdx + BEGIN_MARK.length);
  const after = html.slice(endIdx);
  return `${before}\n${catalogue}\n${after}`;
}

// -- filesystem helpers ---------------------------------------------------

function rimraf(p) {
  if (!existsSync(p)) return;
  rmSync(p, { recursive: true, force: true });
}

function copyRecursive(srcDir, destDir) {
  if (!existsSync(srcDir)) return;
  mkdirSync(destDir, { recursive: true });
  for (const entry of readdirSync(srcDir, { withFileTypes: true })) {
    const srcPath = join(srcDir, entry.name);
    const destPath = join(destDir, entry.name);
    if (entry.isDirectory()) {
      copyRecursive(srcPath, destPath);
    } else if (entry.isFile()) {
      // Skip dotfiles (.gitkeep etc.); they are placeholders, not real
      // assets that belong in the served site.
      if (entry.name.startsWith('.')) continue;
      copyFileSync(srcPath, destPath);
    }
  }
}

function rewritePaths(html) {
  // src/ sits one level above effects/. dist/index.html lives at the
  // dist/ root, so paths become plain "effects/..." and "assets/...".
  return html.replace(
    /((?:href|src)=")\.\.\/(effects\/|assets\/)/g,
    '$1$2'
  );
}

// -- main -----------------------------------------------------------------

function assemble() {
  rimraf(DIST);
  mkdirSync(DIST, { recursive: true });

  // src/index.html -> dist/index.html, paths un-prefixed.
  const srcHtml = readFileSync(join(SRC, 'index.html'), 'utf8');
  const rewritten = rewritePaths(srcHtml);
  writeFileSync(join(DIST, 'index.html'), rewritten, 'utf8');

  // effects/ -> dist/effects/ (verbatim).
  copyRecursive(EFFECTS, join(DIST, 'effects'));

  // src/styles and src/assets -> dist/ (if they have content).
  copyRecursive(join(SRC, 'styles'), join(DIST, 'styles'));
  copyRecursive(join(SRC, 'assets'), join(DIST, 'assets'));

  // Regenerate the catalogue section in place.
  const catalog = JSON.parse(readFileSync(CATALOG_PATH, 'utf8'));
  const catalogue = buildCatalogue(catalog);
  const currentHtml = readFileSync(join(DIST, 'index.html'), 'utf8');
  const nextHtml = applyCatalogue(currentHtml, catalogue);
  writeFileSync(join(DIST, 'index.html'), nextHtml, 'utf8');
}

function check() {
  if (!existsSync(join(DIST, 'index.html'))) {
    console.error('dist/ does not exist. Run `node scripts/build.mjs`.');
    process.exit(1);
  }
  const catalog = JSON.parse(readFileSync(CATALOG_PATH, 'utf8'));
  const catalogue = buildCatalogue(catalog);
  const expectedSrcHtml = readFileSync(join(SRC, 'index.html'), 'utf8');
  const expected = applyCatalogue(rewritePaths(expectedSrcHtml), catalogue);
  const current = readFileSync(join(DIST, 'index.html'), 'utf8');
  if (current === expected) {
    console.log('dist/ is up to date.');
    return;
  }
  console.error('dist/ is OUT OF DATE. Run `node scripts/build.mjs`.');
  process.exit(1);
}

function main() {
  const args = new Set(process.argv.slice(2));
  if (args.has('--check')) check();
  else assemble();
}

main();
