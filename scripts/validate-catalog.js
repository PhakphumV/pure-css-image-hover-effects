#!/usr/bin/env node
/* eslint-disable no-console */
//
// Validates catalog/effects.json against the effect implementations on
// disk. Fails fast on any drift between the catalogue metadata and the
// repository structure.
//
// Usage:  node scripts/validate-catalog.js
//
// Exit code 0 on success, 1 on any validation failure. Never modifies
// repository files.
//
// Rules checked (in order, matching the issue scope):
//   - catalog/effects.json exists and parses
//   - top-level shape: { version, categories }
//   - every category has slug / name / description / effects
//   - every effect has slug / name / description
//   - every slug matches /^[a-z0-9]+(-[a-z0-9]+)*$/
//   - no duplicate category slugs
//   - no duplicate effect slugs (project-wide)
//   - every category slug maps to an existing effects/<slug>/ directory
//   - every category directory contains <slug>.css
//   - every effect slug maps to an existing effects/<cat>/<slug>.html
//   - every HTML file in effects/<cat>/ has a matching catalogue entry
//     (no orphan implementations)
//   - the informational aside folder (effects/reduced-motion-notice) is
//     not declared as a category in the catalogue
//

'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const CATALOG_PATH = path.join(ROOT, 'catalog', 'effects.json');
const EFFECTS_DIR = path.join(ROOT, 'effects');
const SLUG_RE = /^[a-z0-9]+(-[a-z0-9]+)*$/;
const ASIDE_DIRS = new Set(['reduced-motion-notice']);

let checksRun = 0;
const failures = [];

function check(label, fn) {
  checksRun += 1;
  try {
    fn();
    console.log(`\u2713 ${label}`);
  } catch (err) {
    console.log(`\u2717 ${label}`);
    failures.push({ label, message: err.message });
  }
}

function fail(message) {
  const e = new Error(message);
  // Mark so the catch site doesn't double-log.
  e.alreadyReported = true;
  throw e;
}

function assert(cond, message) {
  if (!cond) fail(message);
}

function readJson(p) {
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

function listDirs(parent) {
  return fs.readdirSync(parent, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => d.name)
    .filter((n) => !n.startsWith('.'));
}

function listFiles(parent, ext) {
  return fs.readdirSync(parent, { withFileTypes: true })
    .filter((d) => d.isFile() && d.name.endsWith(ext))
    .map((d) => d.name);
}

// -- 1. parse + shape ----------------------------------------------------

check('catalog/effects.json parses', () => {
  if (!fs.existsSync(CATALOG_PATH)) fail(`missing ${CATALOG_PATH}`);
  let data;
  try { data = readJson(CATALOG_PATH); }
  catch (err) { fail(`catalog/effects.json is not valid JSON: ${err.message}`); }
  check.shape = data;
});

check('top-level shape (version + categories array)', () => {
  const data = check.shape;
  assert(typeof data === 'object' && data !== null, 'root must be an object');
  assert(typeof data.version === 'number', 'version must be a number');
  assert(Array.isArray(data.categories), 'categories must be an array');
});

// -- 2. category / effect fields -----------------------------------------

check('categories', () => {
  for (const cat of check.shape.categories) {
    assert(typeof cat === 'object' && cat !== null, 'category must be an object');
    assert(typeof cat.slug === 'string' && cat.slug.length > 0, `category missing slug: ${JSON.stringify(cat)}`);
    assert(typeof cat.name === 'string' && cat.name.length > 0, `category ${cat.slug} missing name`);
    assert(typeof cat.description === 'string' && cat.description.length > 0, `category ${cat.slug} missing description`);
    assert(Array.isArray(cat.effects), `category ${cat.slug} effects must be an array`);
  }
});

check('effects', () => {
  for (const cat of check.shape.categories) {
    for (const eff of cat.effects) {
      assert(typeof eff === 'object' && eff !== null, `effect in ${cat.slug} must be an object`);
      assert(typeof eff.slug === 'string' && eff.slug.length > 0, `effect in ${cat.slug} missing slug: ${JSON.stringify(eff)}`);
      assert(typeof eff.name === 'string' && eff.name.length > 0, `effect ${cat.slug}/${eff.slug} missing name`);
      assert(typeof eff.description === 'string' && eff.description.length > 0, `effect ${cat.slug}/${eff.slug} missing description`);
    }
  }
});

// -- 3. slug pattern -----------------------------------------------------

check('slug pattern (lowercase, hyphen-separated)', () => {
  for (const cat of check.shape.categories) {
    assert(SLUG_RE.test(cat.slug), `category slug "${cat.slug}" does not match ${SLUG_RE}`);
    for (const eff of cat.effects) {
      assert(SLUG_RE.test(eff.slug), `effect slug "${eff.slug}" in ${cat.slug} does not match ${SLUG_RE}`);
    }
  }
});

// -- 4. uniqueness --------------------------------------------------------

check('unique category slugs', () => {
  const seen = new Map();
  for (const cat of check.shape.categories) {
    if (seen.has(cat.slug)) fail(`duplicate category slug "${cat.slug}"`);
    seen.set(cat.slug, true);
  }
});

check('unique effect slugs (project-wide)', () => {
  const seen = new Map();
  for (const cat of check.shape.categories) {
    for (const eff of cat.effects) {
      if (seen.has(eff.slug)) fail(`duplicate effect slug "${eff.slug}" (also in category "${seen.get(eff.slug)}")`);
      seen.set(eff.slug, cat.slug);
    }
  }
});

// -- 5. catalog -> disk paths -------------------------------------------

check('every category slug maps to effects/<slug>/', () => {
  for (const cat of check.shape.categories) {
    const dir = path.join(EFFECTS_DIR, cat.slug);
    if (!fs.existsSync(dir) || !fs.statSync(dir).isDirectory()) {
      fail(`category "${cat.slug}" has no directory at ${path.relative(ROOT, dir)}`);
    }
  }
});

check('every category directory contains <slug>.css', () => {
  for (const cat of check.shape.categories) {
    const css = path.join(EFFECTS_DIR, cat.slug, `${cat.slug}.css`);
    if (!fs.existsSync(css)) fail(`category "${cat.slug}" missing ${path.relative(ROOT, css)}`);
  }
});

check('every effect slug maps to effects/<cat>/<slug>.html', () => {
  for (const cat of check.shape.categories) {
    for (const eff of cat.effects) {
      const html = path.join(EFFECTS_DIR, cat.slug, `${eff.slug}.html`);
      if (!fs.existsSync(html)) fail(`effect "${cat.slug}/${eff.slug}" missing ${path.relative(ROOT, html)}`);
    }
  }
});

check('no orphan implementations (every HTML file is in the catalog)', () => {
  // Build the set of (cat, eff) declared in the catalog.
  const declared = new Set();
  for (const cat of check.shape.categories) {
    for (const eff of cat.effects) declared.add(`${cat.slug}/${eff.slug}`);
  }
  // Walk every category directory on disk.
  for (const cat of check.shape.categories) {
    const dir = path.join(EFFECTS_DIR, cat.slug);
    for (const file of listFiles(dir, '.html')) {
      const slug = file.replace(/\.html$/, '');
      if (!declared.has(`${cat.slug}/${slug}`)) {
        fail(`orphan implementation: ${path.relative(ROOT, path.join(dir, file))} has no catalog entry`);
      }
    }
  }
});

check('informational aside folders are not declared as categories', () => {
  for (const cat of check.shape.categories) {
    if (ASIDE_DIRS.has(cat.slug)) fail(`"${cat.slug}" is an informational aside, not a hover-effect category`);
  }
});

// -- summary --------------------------------------------------------------

console.log('');
if (failures.length === 0) {
  console.log(`Catalogue validation passed (${checksRun} checks).`);
  process.exit(0);
} else {
  console.error(`Catalogue validation failed (${failures.length} of ${checksRun} checks):`);
  for (const f of failures) console.error(`  - ${f.label}: ${f.message}`);
  process.exit(1);
}
