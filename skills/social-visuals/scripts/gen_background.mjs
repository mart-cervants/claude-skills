#!/usr/bin/env node
// Generate text-free background candidates for social cards with Gemini (Nano Banana).
//
//   node gen_background.mjs --kit marketing/social --name p1-lanzamiento \
//     --prompt "abstract network graph converging into one glowing node" \
//     [--text-zone left|right|top|bottom|center|none] [--ratio 4:5] [--size 1K] [--n 3] [--dry]
//
// The prompt is the creative IDEA only. Brand rules (palette from tokens.json,
// "no text / no logos / no people") are appended automatically. The key is read from
// GEMINI_API_KEY (env or the nearest .env.local above the current directory) and is never printed.
// Output: <kit>/assets/backgrounds/<name>-<i>.<ext> + <same>.json (prompt, model, contrast report).
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import sharp from "sharp";

const MODEL = "gemini-nano-banana-2.1";
const ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions";
// USD per image, standard (non-batch) pricing, from the Gemini API pricing page. Verify before big batches.
const PRICE = { "1K": 0.0336, "2K": 0.0504, "4K": 0.113 };
const ZONES = ["left", "right", "top", "bottom", "center", "none"];

// ---- args ------------------------------------------------------------------------------------
const argv = process.argv.slice(2);
const flag = (n, d) => { const i = argv.indexOf(`--${n}`); if (i < 0) return d; return argv.splice(i, 2)[1]; };
const bool = (n) => { const i = argv.indexOf(`--${n}`); if (i < 0) return false; argv.splice(i, 1); return true; };
const kit = resolve(flag("kit", "marketing/social"));
const name = flag("name");
const idea = flag("prompt");
const zone = flag("text-zone", "none");
const ratio = flag("ratio", "1:1");
const size = flag("size", "1K");
const n = Math.max(1, Math.min(Number(flag("n", "3")), 6));
const dry = bool("dry");
if (!name || !idea || !ZONES.includes(zone) || !PRICE[size]) {
  console.error(`Usage: gen_background.mjs --kit <dir> --name <id> --prompt "<idea>" [--text-zone ${ZONES.join("|")}] [--ratio 1:1] [--size 1K|2K|4K] [--n 3] [--dry]`);
  process.exit(1);
}

// ---- brand tokens → prompt suffix --------------------------------------------------------------
const tokensPath = join(kit, "tokens.json");
if (!existsSync(tokensPath)) { console.error(`No tokens.json in ${kit}`); process.exit(1); }
const colors = JSON.parse(readFileSync(tokensPath, "utf8")).colors ?? {};
const { background = "#000000", accent, accent2, text = "#ffffff" } = colors;
const zoneText = zone === "none" ? "" :
  ` Composition: keep the ${zone} ${zone === "center" ? "area" : "third"} of the frame calm, dark and low-detail (open negative space for a headline); put visual interest elsewhere.`;
const rules = ` Dark background close to ${background}${accent ? `, a single ${accent} accent` : ""}${accent2 ? ` with at most a hint of ${accent2}` : ""}.` +
  " Generous empty space, soft depth, minimal, high contrast. No text, no letters, no numbers, no logos, no watermarks, no people, no robots, no laptops.";
const fullPrompt = idea.trim().replace(/\.?$/, ".") + zoneText + rules;

console.log(`Model: ${MODEL} | ${n} × ${ratio} @ ${size} | estimated cost: US$${(PRICE[size] * n).toFixed(3)}`);
console.log(`Prompt:\n  ${fullPrompt}\n`);
if (dry) { console.log("--dry: nothing sent."); process.exit(0); }

// ---- key (env or nearest .env.local upward) -------------------------------------------------------
if (!process.env.GEMINI_API_KEY) {
  for (let d = process.cwd(); ; d = dirname(d)) {
    const f = join(d, ".env.local");
    if (existsSync(f)) { try { process.loadEnvFile(f); } catch {} if (process.env.GEMINI_API_KEY) break; }
    if (dirname(d) === d) break;
  }
}
const key = process.env.GEMINI_API_KEY;
if (!key) { console.error("GEMINI_API_KEY not found (env or .env.local)."); process.exit(1); }

// ---- helpers --------------------------------------------------------------------------------------
const hex = (h) => { h = h.replace("#", ""); return [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16)); };
const lin = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; };
const lum = ([r, g, b]) => 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
const textL = lum(hex(text));

// Recursively find { data: <base64>, mime_type: image/* } so we don't depend on the exact response nesting.
function findImage(o) {
  if (o && typeof o === "object") {
    const mt = o.mime_type ?? o.mimeType ?? "";
    if (typeof o.data === "string" && o.data.length > 1000 && /^image\//.test(mt)) return { data: o.data, mime: mt };
    for (const v of Object.values(o)) { const r = findImage(v); if (r) return r; }
  }
  return null;
}

// 3×3 grid: p90 luminance (worst bright pixel) per cell → contrast of the text colour against it.
async function contrastGrid(buf) {
  const S = 90;
  const { data } = await sharp(buf).resize(S, S, { fit: "fill" }).removeAlpha().raw().toBuffer({ resolveWithObject: true });
  const grid = [];
  for (let gy = 0; gy < 3; gy++) {
    const row = [];
    for (let gx = 0; gx < 3; gx++) {
      const ls = [];
      for (let y = gy * 30; y < gy * 30 + 30; y++) for (let x = gx * 30; x < gx * 30 + 30; x++) {
        const i = (y * S + x) * 3; ls.push(lum([data[i], data[i + 1], data[i + 2]]));
      }
      ls.sort((a, b) => a - b);
      const p90 = ls[Math.floor(ls.length * 0.9)];
      row.push(+((Math.max(textL, p90) + 0.05) / (Math.min(textL, p90) + 0.05)).toFixed(1));
    }
    grid.push(row);
  }
  return grid;
}
const mark = (c) => (c >= 4.5 ? "✓" : c >= 3 ? "~" : "✗");

// ---- generate -------------------------------------------------------------------------------------
const outDir = join(kit, "assets", "backgrounds");
mkdirSync(outDir, { recursive: true });
let start = 1;
while (["jpg", "png"].some((e) => existsSync(join(outDir, `${name}-${start}.${e}`)))) start++;

for (let i = start; i < start + n; i++) {
  const res = await fetch(ENDPOINT, {
    method: "POST",
    headers: { "x-goog-api-key": key, "Content-Type": "application/json", "Api-Revision": "2026-05-20" },
    body: JSON.stringify({
      model: MODEL,
      input: [{ type: "text", text: fullPrompt }],
      response_format: { type: "image", mime_type: "image/jpeg", aspect_ratio: ratio, image_size: size },
    }),
  });
  const json = await res.json().catch(() => ({}));
  if (!res.ok) { console.error(`#${i} HTTP ${res.status}:`, JSON.stringify(json.error ?? json).slice(0, 500)); process.exit(1); }
  const img = findImage(json);
  if (!img) { console.error(`#${i} no image found in response:`, JSON.stringify(json).slice(0, 300)); process.exit(1); }

  const buf = Buffer.from(img.data, "base64");
  const file = join(outDir, `${name}-${i}.${img.mime.includes("png") ? "png" : "jpg"}`);
  writeFileSync(file, buf);
  const grid = await contrastGrid(buf);
  writeFileSync(file.replace(/\.\w+$/, ".json"), JSON.stringify({
    model: MODEL, ratio, size, textZone: zone, idea, prompt: fullPrompt, date: new Date().toISOString(),
    textColor: text, contrastGrid3x3: grid, note: "Contrast of the text colour vs the brightest 10% of each cell; ✓ ≥ 4.5, ~ ≥ 3, ✗ < 3.",
  }, null, 2));

  console.log(`saved ${file}`);
  console.log("  text contrast by zone (top→bottom, left→right):");
  grid.forEach((r) => console.log("   " + r.map((c) => `${mark(c)} ${String(c).padStart(4)}`).join("   ")));
}
console.log("\nNext: upload your pick in the card editor as the background, then dim/scrim as needed.");
