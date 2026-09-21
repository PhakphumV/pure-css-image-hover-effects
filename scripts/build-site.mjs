#!/usr/bin/env node
//
// Copies src/index.html to ./index.html, rewriting paths so the file
// works at the repository root.
//
// Path adjustments:
//   href/src "../effects/"  ->  "effects/"
//   href/src "../assets/"   ->  "assets/"   (forward refs from src)
//
// The build leaves BEGIN/END GENERATED EFFECT CATALOG markers intact;
// the actual catalogue content is filled in later by build-catalog.mjs.
//
// Usage:
//   node scripts/build-site.mjs                # writes ./index.html in place (idempotent)
//   node scripts/build-site.mjs --check        # exit 0 if up to date, 1 otherwise
//

import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, '..');
const SRC_INDEX = resolve(ROOT, 'src', 'index.html');
const OUT_INDEX = resolve(ROOT, 'index.html');

function render() {
  const html = readFileSync(SRC_INDEX, 'utf8');
  // Strip the "../" prefix only from href/src values that point at one of
  // the top-level source directories. Conservative on purpose: only known
  // prefixes get rewritten, everything else passes through untouched.
  return html.replace(
    /((?:href|src)=")\.\.\/(effects\/|assets\/)/g,
    '$1$2'
  );
}

function readOrEmpty(path) {
  try { return readFileSync(path, 'utf8'); } catch { return ''; }
}

function main() {
  const args = new Set(process.argv.slice(2));
  const next = render();
  const current = readOrEmpty(OUT_INDEX);

  if (args.has('--check')) {
    if (current === next) {
      console.log('index.html is up to date.');
      return;
    }
    console.error('index.html is OUT OF DATE. Run `node scripts/build-site.mjs`.');
    process.exit(1);
  }

  if (next !== current) writeFileSync(OUT_INDEX, next, 'utf8');
}

main();
