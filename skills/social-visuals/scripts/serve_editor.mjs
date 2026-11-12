#!/usr/bin/env node
// Local card editor + preview server (no dependencies beyond Node >= 18).
//
// Usage:
//   node serve_editor.mjs --kit <brand-kit dir> [--port 8790] [--cards calendar/2026-11.cards.json]
//
// Opens a review page at http://127.0.0.1:<port>/.render/editor.html where you can:
//   - see every card's live preview (the exact HTML that gets rendered to PNG)
//   - edit kicker, title, body, CTA, alt text, size, status (draft / approved)
//   - see overflow / fit warnings
//   - save to the cards.json, and render a PNG on demand
// Nothing leaves your machine: the server listens on 127.0.0.1 only and writes only
// <kit>/calendar/*.cards.json, <kit>/designs/** and <kit>/assets/uploads/** (PNG/JPEG only).

import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const opt = (n, d) => { const i = args.indexOf('--' + n); return i >= 0 ? args[i + 1] : d; };
const kitArg = opt('kit');
if (!kitArg) { console.error('Usage: node serve_editor.mjs --kit <brand-kit dir> [--port 8790] [--cards calendar/YYYY-MM.cards.json]'); process.exit(2); }
const kit = path.resolve(kitArg);
const port = Number(opt('port', '8790'));
const defaultCards = opt('cards', '');

if (!fs.existsSync(path.join(kit, 'tokens.json'))) { console.error(`No tokens.json in ${kit}. Is this a brand kit folder?`); process.exit(2); }

// put the current templates next to the kit's tokens/assets
const renderDir = path.join(kit, '.render');
fs.mkdirSync(renderDir, { recursive: true });
for (const f of ['post-card.html', 'editor.html']) fs.copyFileSync(path.join(here, '..', 'templates', f), path.join(renderDir, f));

const types = { '.html': 'text/html; charset=utf-8', '.json': 'application/json; charset=utf-8', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
  '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf', '.css': 'text/css', '.md': 'text/plain; charset=utf-8' };

const send = (res, code, body, type = 'application/json; charset=utf-8') => {
  res.writeHead(code, { 'content-type': type, 'cache-control': 'no-store' });
  res.end(typeof body === 'string' || Buffer.isBuffer(body) ? body : JSON.stringify(body));
};
const readBody = req => new Promise((resolve, reject) => {
  let b = ''; req.on('data', c => { b += c; if (b.length > 1e6) { reject(new Error('body too large')); req.destroy(); } });
  req.on('end', () => resolve(b)); req.on('error', reject);
});

// only <kit>/calendar/*.cards.json may be read/written through the API
function cardsPath(rel) {
  if (!rel || !/^calendar\/[A-Za-z0-9._-]+\.cards\.json$/.test(rel)) return null;
  return path.join(kit, rel);
}
const ID_RE = /^[A-Za-z0-9][A-Za-z0-9_-]{0,60}$/;
const STR_KEYS = ['id', 'kicker', 'title', 'body', 'cta', 'alt', 'bg', 'status'];
function validate(data) {
  if (!data || !Array.isArray(data.cards)) return 'cards must be an array';
  const seen = new Set();
  for (const c of data.cards) {
    if (!ID_RE.test(c.id || '')) return `invalid id: ${c.id}`;
    if (seen.has(c.id)) return `duplicate id: ${c.id}`;
    seen.add(c.id);
    for (const k of STR_KEYS) if (c[k] != null && (typeof c[k] !== 'string' || c[k].length > 600)) return `invalid ${k} in ${c.id}`;
    if (c.status && !['draft', 'approved'].includes(c.status)) return `invalid status in ${c.id}`;
    if (c.bg && !(/^https:\/\/[^\s]+$/.test(c.bg) || (/^[A-Za-z0-9._\/-]{1,200}$/.test(c.bg) && !c.bg.includes('..') && !c.bg.startsWith('/')))) return `invalid bg in ${c.id}`;
    if (c.layout != null) { const e = validateLayout(c.layout); if (e) return `${e} in ${c.id}`; }
    if (c.dim != null && !num(c.dim, 0, 1)) return `invalid dim in ${c.id}`;
    for (const k of ['w', 'h']) if (c[k] != null && !(Number.isInteger(c[k]) && c[k] >= 200 && c[k] <= 4000)) return `invalid ${k} in ${c.id}`;
  }
  return null;
}

const ELEMENTS = ['kicker', 'title', 'bar', 'body', 'logo', 'cta', 'net'];
const num = (x, lo, hi) => typeof x === 'number' && Number.isFinite(x) && x >= lo && x <= hi;
function validateLayout(L) {
  if (typeof L !== 'object' || Array.isArray(L)) return 'layout must be an object';
  for (const [k, o] of Object.entries(L)) {
    if (k === 'extras') {
      if (!Array.isArray(o) || o.length > 12) return 'extras must be an array (max 12)';
      for (const e of o) {
        if (!e || !['text', 'image'].includes(e.type)) return 'invalid extra type';
        if (!num(e.x ?? 0, -3000, 3000) || !num(e.y ?? 0, -3000, 3000) || !num(e.s ?? 1, 0.2, 6)) return 'invalid extra position/scale';
        if (e.type === 'text') {
          if (typeof (e.text ?? '') !== 'string' || (e.text ?? '').length > 300) return 'invalid extra text';
          if (e.size != null && !num(e.size, 8, 400)) return 'invalid extra size';
          if (e.color != null && !['accent', 'text', 'muted'].includes(e.color)) return 'invalid extra color';
          if (e.weight != null && ![400, 700].includes(e.weight)) return 'invalid extra weight';
        } else {
          if (typeof e.src !== 'string' || !/^[A-Za-z0-9._\/-]{1,200}$/.test(e.src) || e.src.includes('..') || e.src.startsWith('/')) return 'invalid extra image path';
          if (e.w != null && !num(e.w, 20, 2000)) return 'invalid extra width';
        }
      }
      continue;
    }
    if (!ELEMENTS.includes(k)) return `unknown layout element: ${k}`;
    if (typeof o !== 'object' || o === null) return `invalid layout for ${k}`;
    if (!num(o.x ?? 0, -3000, 3000) || !num(o.y ?? 0, -3000, 3000) || !num(o.s ?? 1, 0.2, 6)) return `invalid layout values for ${k}`;
    if (o.hide != null && typeof o.hide !== 'boolean') return `invalid hide for ${k}`;
  }
  return null;
}
const outDirFor = rel => path.join('designs', path.basename(rel).replace(/\.cards\.json$/, ''));

const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, 'http://x');
    const p = url.pathname;
    if (p === '/favicon.ico') { res.writeHead(204); return res.end(); }
    if (p === '/' ) { res.writeHead(302, { location: '/.render/editor.html' + (defaultCards ? `?cards=${encodeURIComponent(defaultCards)}` : '') }); return res.end(); }

    if (p === '/api/files' && req.method === 'GET') {
      const dir = path.join(kit, 'calendar');
      const files = fs.existsSync(dir) ? fs.readdirSync(dir).filter(f => f.endsWith('.cards.json')).map(f => 'calendar/' + f) : [];
      return send(res, 200, { files, default: defaultCards || files[files.length - 1] || null });
    }
    if (p === '/api/upload' && req.method === 'POST') {
      const chunks = []; let size = 0;
      for await (const ch of req) { size += ch.length; if (size > 15 * 1024 * 1024) return send(res, 413, { error: 'File too large (max 15 MB)' }); chunks.push(ch); }
      const buf = Buffer.concat(chunks);
      const kind = buf.slice(0, 8).equals(Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a])) ? 'png'
        : (buf[0] === 0xff && buf[1] === 0xd8 && buf[2] === 0xff) ? 'jpg' : null;
      if (!kind) return send(res, 400, { error: 'Only PNG or JPEG images are accepted (the editor converts other formats first).' });
      // identical bytes already uploaded -> reuse that file
      const sha = createHash('sha1').update(buf).digest('hex');
      const upDir = path.join(kit, 'assets', 'uploads');
      if (fs.existsSync(upDir)) for (const f of fs.readdirSync(upDir)) { const fp = path.join(upDir, f); if (fs.statSync(fp).size === buf.length && createHash('sha1').update(fs.readFileSync(fp)).digest('hex') === sha) return send(res, 200, { ok: true, path: `assets/uploads/${f}`, bytes: buf.length, reused: true }); }
      let base = (url.searchParams.get('name') || 'image').replace(/\.[^.]*$/, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40) || 'image';
      const dir = path.join(kit, 'assets', 'uploads'); fs.mkdirSync(dir, { recursive: true });
      let name = `${base}.${kind}`, n = 2; while (fs.existsSync(path.join(dir, name))) name = `${base}-${n++}.${kind}`;
      fs.writeFileSync(path.join(dir, name), buf);
      return send(res, 200, { ok: true, path: `assets/uploads/${name}`, bytes: buf.length });
    }
    if (p === '/api/assets' && req.method === 'GET') {
      const out = [];
      const walk = (dir, rel) => { for (const f of fs.readdirSync(dir)) { const full = path.join(dir, f), r = rel ? rel + '/' + f : f;
        if (fs.statSync(full).isDirectory()) { if (f !== 'fonts') walk(full, r); } else if (/\.(png|jpe?g|svg|webp)$/i.test(f)) out.push(r); } };
      const root = path.join(kit, 'assets'); if (fs.existsSync(root)) walk(root, 'assets');
      return send(res, 200, { assets: out });
    }
    if (p === '/api/cards' && req.method === 'GET') {
      const file = cardsPath(url.searchParams.get('file'));
      if (!file || !fs.existsSync(file)) return send(res, 404, { error: 'cards file not found' });
      return send(res, 200, fs.readFileSync(file, 'utf8'));
    }
    if (p === '/api/cards' && req.method === 'POST') {
      const file = cardsPath(url.searchParams.get('file'));
      if (!file) return send(res, 400, { error: 'invalid file' });
      const data = JSON.parse(await readBody(req));
      const err = validate(data);
      if (err) return send(res, 400, { error: err });
      fs.writeFileSync(file, JSON.stringify(data, null, 2) + '\n');
      return send(res, 200, { ok: true });
    }
    if (p === '/api/render' && req.method === 'POST') {
      const rel = url.searchParams.get('file'); const id = url.searchParams.get('id') || '';
      const file = cardsPath(rel);
      if (!file || !fs.existsSync(file) || !ID_RE.test(id)) return send(res, 400, { error: 'invalid request' });
      const out = outDirFor(rel);
      const child = spawn(process.execPath, [path.join(here, 'render_cards.mjs'), '--kit', kit, '--cards', file, '--out', path.join(kit, out), '--only', id],
        { cwd: here });
      let log = ''; child.stdout.on('data', d => log += d); child.stderr.on('data', d => log += d);
      child.on('close', code => send(res, 200, { ok: code === 0, output: log.trim(), png: code === 0 ? `/${out.split(path.sep).join('/')}/${id}.png?t=${Date.now()}` : null }));
      return;
    }

    // static files from the kit root
    const target = path.normalize(path.join(kit, decodeURIComponent(p)));
    if (!target.startsWith(kit) || !fs.existsSync(target) || fs.statSync(target).isDirectory()) return send(res, 404, 'not found', 'text/plain');
    return send(res, 200, fs.readFileSync(target), types[path.extname(target).toLowerCase()] || 'application/octet-stream');
  } catch (e) {
    return send(res, 500, { error: String(e.message || e) });
  }
});

server.listen(port, '127.0.0.1', () => {
  const base = `http://127.0.0.1:${port}`;
  console.log(`Card editor running for ${kit}`);
  console.log(`  Review & edit:  ${base}/.render/editor.html${defaultCards ? '?cards=' + encodeURIComponent(defaultCards) : ''}`);
  console.log('  Stop with Ctrl+C.');
});
server.on('error', e => { console.error(e.code === 'EADDRINUSE' ? `Port ${port} is in use. Try --port ${port + 1}` : e.message); process.exit(1); });
