#!/usr/bin/env node
//
// Generates the effect-catalogue section of README.md from
// catalog/effects.json, then splices it back into README.md between the
// generated-content boundary markers.
//
// Usage:
//   node scripts/build-readme.mjs                       # catalogue markdown to stdout
//   node scripts/build-readme.mjs --apply              # rewrite README.md in place
//   node scripts/build-readme.mjs --check              # print the regenerated README to stdout
//
// Boundary markers in README.md:
//
//   <!-- BEGIN GENERATED EFFECT CATALOGUE -->
//   ...
//   <!-- END GENERATED EFFECT CATALOGUE -->
//
// Only the content between the markers is replaced; everything outside
// (intro, project layout, contribution guidance, etc.) is preserved
// byte-for-byte.
//
// The generator is deterministic: output depends only on
// catalog/effects.json and the strings here.
//

import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, '..');
const CATALOG_PATH = resolve(ROOT, 'catalog', 'effects.json');
const README_PATH = resolve(ROOT, 'README.md');

const BEGIN_MARK = '<!-- BEGIN GENERATED EFFECT CATALOGUE -->';
const END_MARK = '<!-- END GENERATED EFFECT CATALOGUE -->';

const ESCAPE_MAP = { '&': '&amp;', '<': '&lt;', '>': '&gt;' };
function escapeMd(s) {
  // Escape pipe (table cell) and backslash, then HTML for safety.
  return String(s).replace(/[\\|]/g, (c) => '\\' + c).replace(/[&<>]/g, (c) => ESCAPE_MAP[c]);
}

function renderCategory(cat) {
  const lines = [];
  lines.push(`### ${cat.name} (${cat.effects.length} effects)`);
  lines.push('');
  lines.push(cat.description);
  lines.push('');
  for (const eff of cat.effects) {
    lines.push(`- [${eff.name}](effects/${cat.slug}/${eff.slug}.html)`);
  }
  lines.push('');
  return lines.join('\n');
}

function buildCatalogue() {
  const catalog = JSON.parse(readFileSync(CATALOG_PATH, 'utf8'));
  const totalEffects = catalog.categories.reduce((n, c) => n + c.effects.length, 0);
  const intro = `${catalog.categories.length} categories, ${totalEffects} effects total.\n`;
  return intro + '\n' + catalog.categories.map(renderCategory).join('\n');
}

function applyToReadme(catalogue, readme) {
  const beginIdx = readme.indexOf(BEGIN_MARK);
  const endIdx = readme.indexOf(END_MARK);
  if (beginIdx === -1) {
    throw new Error(`README.md is missing the BEGIN marker: ${BEGIN_MARK}`);
  }
  if (endIdx === -1) {
    throw new Error(`README.md is missing the END marker: ${END_MARK}`);
  }
  if (endIdx < beginIdx) {
    throw new Error('README.md has END marker before BEGIN marker');
  }
  const before = readme.slice(0, beginIdx + BEGIN_MARK.length);
  const after = readme.slice(endIdx);
  return `${before}\n${catalogue}\n${after}`;
}

function main() {
  const args = new Set(process.argv.slice(2));
  const catalogue = buildCatalogue();

  if (args.has('--check')) {
    const readme = readFileSync(README_PATH, 'utf8');
    process.stdout.write(applyToReadme(catalogue, readme));
    return;
  }

  if (args.has('--apply')) {
    const readme = readFileSync(README_PATH, 'utf8');
    const next = applyToReadme(catalogue, readme);
    if (next !== readme) writeFileSync(README_PATH, next, 'utf8');
    return;
  }

  process.stdout.write(catalogue + '\n');
}

main();
