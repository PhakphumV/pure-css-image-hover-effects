#!/usr/bin/env node
//
// Verifies that the committed dist/ matches a clean rebuild from the
// current source tree.
//
// Builds dist/ into a fresh temporary directory (under the OS temp dir)
// using the same logic as build.mjs, then compares every file and
// directory entry against the committed dist/. Any difference is
// reported and causes a non-zero exit.
//
// The comparison is content-only (sha256 of file bytes). mtime is
// deliberately ignored; the goal is to detect stale or incorrect
// generated output, not filesystem-level noise.
//
// Usage:
//   node scripts/verify-dist.mjs
//
// Exit code:
//   0   dist/ is a clean build from current source.
//   1   dist/ differs from a clean build (with details on stderr).
//   2   the build itself failed (details on stderr).
//

import { rmSync, mkdirSync, readdirSync, readFileSync, writeFileSync, copyFileSync, existsSync, mkdtempSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { dirname, join, resolve, relative } from 'node:path';
import { fileURLToPath } from 'node:url';
import { tmpdir } from 'node:os';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, '..');
const CATALOG_PATH = join(ROOT, 'catalog', 'effects.json');
const DIST = join(ROOT, 'dist');
const SRC = join(ROOT, 'src');
const EFFECTS = join(ROOT, 'effects');
const IMAGE_BASE = 'https://picsum.photos/seed';

const BEGIN_MARK = '<!-- BEGIN GENERATED EFFECT CATALOG -->';
const END_MARK = '<!-- END GENERATED EFFECT CATALOG -->';

const ESCAPE_MAP = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
function escapeHtml(s) { return String(s).replace(/[&<>"']/g, (c) => ESCAPE_MAP[c]); }

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

function buildCatalogue(catalog) { return catalog.categories.map(renderCategory).join('\n'); }

function applyCatalogue(html, catalogue) {
  const beginIdx = html.indexOf(BEGIN_MARK);
  const endIdx = html.indexOf(END_MARK);
  const before = html.slice(0, beginIdx + BEGIN_MARK.length);
  const after = html.slice(endIdx);
  return `${before}\n${catalogue}\n${after}`;
}

function copyRecursive(srcDir, destDir) {
  if (!existsSync(srcDir)) return;
  mkdirSync(destDir, { recursive: true });
  const entries = readdirSync(srcDir, { withFileTypes: true })
    .slice()
    .sort((a, b) => a.name.localeCompare(b.name));
  for (const entry of entries) {
    const srcPath = join(srcDir, entry.name);
    const destPath = join(destDir, entry.name);
    if (entry.isDirectory()) copyRecursive(srcPath, destPath);
    else if (entry.isFile()) {
      if (entry.name.startsWith('.')) continue;
      copyFileSync(srcPath, destPath);
    }
  }
}

function rewritePaths(html) {
  return html.replace(/((?:href|src)=")\.\.\/(effects\/|assets\/)/g, '$1$2');
}

function assembleTo(outDir) {
  if (existsSync(outDir)) rmSync(outDir, { recursive: true, force: true });
  mkdirSync(outDir, { recursive: true });
  writeFileSync(join(outDir, 'index.html'),
                rewritePaths(readFileSync(join(SRC, 'index.html'), 'utf8')),
                'utf8');
  copyRecursive(EFFECTS, join(outDir, 'effects'));
  copyRecursive(join(SRC, 'styles'), join(outDir, 'styles'));
  copyRecursive(join(SRC, 'assets'), join(outDir, 'assets'));
  const catalog = JSON.parse(readFileSync(CATALOG_PATH, 'utf8'));
  const catalogue = buildCatalogue(catalog);
  writeFileSync(join(outDir, 'index.html'),
                applyCatalogue(readFileSync(join(outDir, 'index.html'), 'utf8'), catalogue),
                'utf8');
}

function sha256(p) {
  return createHash('sha256').update(readFileSync(p)).digest('hex');
}

function indexDir(root) {
  // Return { relative-path -> sha256 } for every file under root.
  const out = new Map();
  function walk(dir, prefix) {
    for (const e of readdirSync(dir, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
      const full = join(dir, e.name);
      const rel = prefix ? `${prefix}/${e.name}` : e.name;
      if (e.isDirectory()) walk(full, rel);
      else if (e.isFile()) out.set(rel, sha256(full));
    }
  }
  walk(root, '');
  return out;
}

function diffMaps(a, b) {
  const added = [];     // in b, not in a
  const removed = [];   // in a, not in b
  const changed = [];   // in both, different sha
  for (const [k, v] of a) if (!b.has(k)) removed.push(k);
  for (const [k, v] of b) if (!a.has(k)) added.push(k);
                   else if (a.get(k) !== v) changed.push(k);
  return { added, removed, changed };
}

function main() {
  let cleanRoot;
  try {
    cleanRoot = mkdtempSync(join(tmpdir(), 'verify-dist-'));
  } catch (err) {
    console.error('verify-dist: failed to create temp dir:', err.message);
    process.exit(2);
  }
  const cleanDist = join(cleanRoot, 'dist');

  try {
    assembleTo(cleanDist);
  } catch (err) {
    console.error('verify-dist: clean build failed:', err.message);
    process.exit(2);
  }

  if (!existsSync(DIST)) {
    console.error('verify-dist: dist/ does not exist. Run `npm run build`.');
    rmSync(cleanRoot, { recursive: true, force: true });
    process.exit(1);
  }

  const expected = indexDir(cleanDist);
  const actual = indexDir(DIST);
  const { added, removed, changed } = diffMaps(actual, expected);

  if (added.length === 0 && removed.length === 0 && changed.length === 0) {
    console.log(`dist/ matches a clean build (${expected.size} files).`);
    rmSync(cleanRoot, { recursive: true, force: true });
    return;
  }

  console.error('dist/ is OUT OF DATE relative to source.');
  // added: present in expected (clean build) but missing from dist/ → "missing in dist/"
  // removed: present in dist/ but absent from expected → "unexpected in dist/"
  if (removed.length) console.error(`  ${removed.length} unexpected in dist/: ${removed.slice(0, 5).join(', ')}${removed.length > 5 ? ', ...' : ''}`);
  if (added.length)   console.error(`  ${added.length} missing in dist/: ${added.slice(0, 5).join(', ')}${added.length > 5 ? ', ...' : ''}`);
  if (changed.length) console.error(`  ${changed.length} stale in dist/: ${changed.slice(0, 5).join(', ')}${changed.length > 5 ? ', ...' : ''}`);
  console.error('  Run `npm run build` to refresh.');
  rmSync(cleanRoot, { recursive: true, force: true });
  process.exit(1);
}

main();
