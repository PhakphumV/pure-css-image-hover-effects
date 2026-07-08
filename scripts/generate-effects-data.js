#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');

const repoRoot = path.resolve(__dirname, '..');
const effectsDir = path.join(repoRoot, 'effects');
const outputPath = path.join(repoRoot, 'effects.json');
const clientManifestPath = path.join(repoRoot, 'effects-manifest.js');

function toTitle(slug) {
  return slug
    .split('-')
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(' ');
}

function escapeForJs(value) {
  return JSON.stringify(value);
}

function getReadmeSummary(folderPath, folderName) {
  const readmePath = path.join(folderPath, 'README.md');
  if (!fs.existsSync(readmePath)) {
    return `Pure CSS hover effect for ${toTitle(folderName)}.`;
  }

  const content = fs.readFileSync(readmePath, 'utf8');
  const headingMatch = content.split(/\r?\n/).find((line) => line.startsWith('# '));
  if (headingMatch) {
    return headingMatch.slice(2).trim();
  }

  const paragraphMatch = content.match(/^[^#\n]+$/m);
  if (paragraphMatch) {
    return paragraphMatch[0].trim();
  }

  return `Pure CSS hover effect for ${toTitle(folderName)}.`;
}

function buildEffectsData() {
  const folders = fs
    .readdirSync(effectsDir, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && !entry.name.startsWith('.'))
    .map((entry) => entry.name)
    .filter((folderName) => {
      const folderPath = path.join(effectsDir, folderName);
      return fs.existsSync(path.join(folderPath, 'index.html')) && fs.existsSync(path.join(folderPath, 'style.css'));
    })
    .sort();

  return folders.map((folderName) => {
    const folderPath = path.join(effectsDir, folderName);
    const title = toTitle(folderName);

    return {
      id: folderName,
      title,
      desc: getReadmeSummary(folderPath, folderName),
      folder: folderName
    };
  });
}

function writeEffectsData() {
  const effects = buildEffectsData();
  const payload = JSON.stringify({ effects }, null, 2) + '\n';
  const clientPayload = `window.__EFFECTS_MANIFEST__ = ${escapeForJs({ effects })};\n`;
  fs.writeFileSync(outputPath, payload, 'utf8');
  fs.writeFileSync(clientManifestPath, clientPayload, 'utf8');
  console.log(`Generated ${path.relative(repoRoot, outputPath)} with ${effects.length} effects.`);
}

writeEffectsData();
