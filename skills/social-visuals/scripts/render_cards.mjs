#!/usr/bin/env node
// Batch-render brand cards (HTML template -> PNG) with safety checks.
//
// Usage:
//   node render_cards.mjs --kit <brand-kit dir> --cards <cards.json> --out <output dir>
//        [--scale 1] [--only id1,id2] [--approved-only] [--chrome <path to Chrome/Chromium>]
//
// cards.json:
//   { "defaults": { "w": 1080, "h": 1080 },
//     "cards": [ { "id": "01-launch", "kicker": "...", "title": "Headline with [highlight]",
//                  "body": "...", "cta": "example.com", "bg": null, "net": 1, "alt": "alt text" } ] }
//
// Checks (a card is NOT written, and the exit code is 1, if any fails):
//   - the template reports data-overflow=0 (headline fits within the safe area, <= 4 lines)
//   - the PNG is exactly w*scale x h*scale pixels
//   - no asset request failed (logo, fonts, tokens, background)
//   - no page errors
//   - (with a card "layout" from the editor) no element leaves the card and no text overlaps text
// --approved-only renders only cards whose "status" is "approved" (set it in the card editor).
// Output: <out>/<id>.png and <out>/manifest.json (sizes, headline px, alt text; merged across runs).

import { chromium } from 'playwright-core';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const opt = (name, def) => { const i = args.indexOf('--' + name); return i >= 0 ? args[i + 1] : def; };

const kit = path.resolve(opt('kit', ''));
const cardsFile = path.resolve(opt('cards', ''));
const outDir = path.resolve(opt('out', ''));
const scale = Number(opt('scale', '1')) || 1;
const only = opt('only', '') ? opt('only').split(',') : null;
const approvedOnly = args.includes('--approved-only');
if (!opt('kit') || !opt('cards') || !opt('out')) {
  console.error('Usage: node render_cards.mjs --kit <dir> --cards <cards.json> --out <dir> [--scale 1] [--only id,id] [--chrome path]');
  process.exit(2);
}

function findChrome() {
  const c = [opt('chrome'), process.env.CHROME_PATH,
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/usr/bin/chromium', '/usr/bin/chromium-browser',
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'].filter(Boolean);
  return c.find(p => fs.existsSync(p));
}

const chrome = findChrome();
if (!chrome) { console.error('No Chrome/Chromium found. Pass --chrome <path> or set CHROME_PATH.'); process.exit(2); }

// copy the template into the kit's .render folder (served together with tokens, logo and fonts)
const renderDir = path.join(kit, '.render');
fs.mkdirSync(renderDir, { recursive: true });
fs.copyFileSync(path.join(here, '..', 'templates', 'post-card.html'), path.join(renderDir, 'post-card.html'));
fs.mkdirSync(outDir, { recursive: true });

// tiny static server rooted at the kit
const types = { '.html': 'text/html', '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
  '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf', '.css': 'text/css' };
const server = http.createServer((req, res) => {
  const p = path.normalize(path.join(kit, decodeURIComponent(new URL(req.url, 'http://x').pathname)));
  if (!p.startsWith(kit) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end('not found'); }
  res.writeHead(200, { 'content-type': types[path.extname(p).toLowerCase()] || 'application/octet-stream' });
  fs.createReadStream(p).pipe(res);
});
await new Promise(r => server.listen(0, '127.0.0.1', r));
const base = `http://127.0.0.1:${server.address().port}`;

const data = JSON.parse(fs.readFileSync(cardsFile, 'utf8'));
const defaults = data.defaults || {};
const cards = (data.cards || []).filter(c => (!only || only.includes(c.id)) && (!approvedOnly || c.status === 'approved'));
if (!cards.length) { console.error(approvedOnly ? 'No approved cards to render (set status to "approved" in the card editor).' : 'No cards to render.'); server.close(); process.exit(2); }

const pngSize = b => ({ w: b.readUInt32BE(16), h: b.readUInt32BE(20) });
const browser = await chromium.launch({ executablePath: chrome, headless: true });
const manifest = []; let failures = 0;

for (const card of cards) {
  const w = card.w || defaults.w || 1080, h = card.h || defaults.h || 1080;
  const problems = [];
  const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: scale });
  const page = await ctx.newPage();
  page.on('pageerror', e => problems.push('page error: ' + e.message));
  page.on('requestfailed', r => problems.push('request failed: ' + r.url()));
  page.on('response', r => { if (r.status() >= 400) problems.push(`HTTP ${r.status()}: ${r.url()}`); });
  const params = new URLSearchParams({ w: String(w), h: String(h) });
  for (const k of ['kicker', 'title', 'body', 'cta', 'bg']) if (card[k]) params.set(k, card[k]);
  if (card.bg && card.dim != null) params.set('dim', String(card.dim));
  if (card.net === 0) params.set('net', '0');
  if (card.layout && Object.keys(card.layout).length) params.set('lay', JSON.stringify(card.layout));
  try {
    await page.goto(`${base}/.render/post-card.html?${params}`, { waitUntil: 'load' });
    await page.waitForFunction(() => document.documentElement.dataset.ready === '1', null, { timeout: 15000 });
    const info = await page.evaluate(() => ({ ...document.documentElement.dataset }));
    if (info.overflow === '1') problems.push('text overflow: ' + (info.overflowReason || 'does not fit'));
    await page.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));
    const buf = await page.locator('#stage').screenshot({ type: 'png', animations: 'disabled' });
    const got = pngSize(buf);
    if (got.w !== w * scale || got.h !== h * scale) problems.push(`wrong size: got ${got.w}x${got.h}, expected ${w * scale}x${h * scale}`);
    if (problems.length) {
      failures++;
      console.log(`FAIL  ${card.id}: ${problems.join(' | ')}`);
    } else {
      fs.writeFileSync(path.join(outDir, `${card.id}.png`), buf);
      manifest.push({ id: card.id, file: `${card.id}.png`, width: got.w, height: got.h, titlePx: Number(info.titleSize), titleLines: Number(info.titleLines), alt: card.alt || '' });
      console.log(`ok    ${card.id}  ${got.w}x${got.h}  headline ${info.titleSize}px, ${info.titleLines} line(s)`);
    }
  } catch (e) {
    failures++; console.log(`FAIL  ${card.id}: ${e.message}`);
  }
  await ctx.close();
}

await browser.close(); server.close();
const manifestPath = path.join(outDir, 'manifest.json');
let previous = [];
try { previous = JSON.parse(fs.readFileSync(manifestPath, 'utf8')).rendered || []; } catch {}
const merged = [...previous.filter(p => !manifest.some(m => m.id === p.id) && fs.existsSync(path.join(outDir, p.file))), ...manifest];
fs.writeFileSync(manifestPath, JSON.stringify({ rendered: merged }, null, 2));
console.log(failures ? `\n${failures} card(s) failed. Shorten the copy or fix the asset, then re-run.` : `\nAll ${manifest.length} card(s) rendered to ${outDir}`);
process.exit(failures ? 1 : 0);
