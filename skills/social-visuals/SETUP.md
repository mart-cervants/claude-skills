# Setup — social-visuals

## 1. Rendering (required)

Batch renderer: `scripts/render_cards.mjs` (Node ≥ 18, `playwright-core`, and a local
Chrome/Chromium — it does not download a browser). One-time install:

```bash
cd <this-skill>/scripts && npm install
```

Review and edit cards in the browser first (recommended before any render):

```bash
node <this-skill>/scripts/serve_editor.mjs --kit <brand kit dir> --cards calendar/2026-11.cards.json
# open the printed URL: http://127.0.0.1:8790/.render/editor.html?cards=calendar/2026-11.cards.json
```

The editor shows each card live (the exact HTML that becomes the PNG), lets you edit
kicker, headline, support line, CTA, alt text, size and status (draft/approved), warns
about overflow, saves to the cards file, and renders a PNG on demand.

Canvas controls:
- Click an element in the preview to select it; drag to move; drag the corner handle to resize.
- Guides snap to the card center, the margins and other elements (hold **Alt** to move freely;
  untick "snap" to disable).
- Arrow keys nudge 1 px (**Shift** = 10 px). **Ctrl/Cmd+Z** undo, **Shift+Ctrl/Cmd+Z** or
  **Ctrl/Cmd+Y** redo. **Delete** removes an added element. **Esc** deselects.
- The Elements list shows/hides each element (kicker, headline, bar, support line, logo,
  footer, network graphic); the properties box has X, Y, Size %, center ↔ / ↕ and reset.
- **+ Text** adds a free text box; **+ Image** adds an image from the kit's `assets/`.
- The network graphic is selected from the Elements list (not by clicking the canvas).

Images and backgrounds:
- **+ Image…** opens your file picker (several files at once are fine); you can also **drop image files
  onto the card**. New images land in the free top-right corner (several are staggered); a dropped
  image lands where you drop it. **Shift + drop** (or "Upload background…") uses the image as the
  card **background** instead, with a **Dim background** slider to keep text readable.
- Accepted: PNG, JPG, WebP, GIF, AVIF. **HEIC/HEIF is not supported by browsers**: export as JPG/PNG first.
- Images are re-encoded in the browser before upload: scaled down to at most 2400 px, PNG/WebP/GIF stay PNG
  (transparency kept), everything else becomes JPEG. This also **strips EXIF metadata such as GPS location**.
- Files are saved under `<kit>/assets/uploads/` (PNG/JPEG only; identical files are reused, never duplicated).
  They are committed with the kit unless you gitignore that folder. Only upload images you have the rights
  to use, and no real client, employer or personal photos (see `guardrails.md`).
- When elements overlap, click the same spot again to select the one underneath, or pick it in the
  Elements list. A selected element can be dragged even when another element covers it.

Layout of the page: on wide windows the editor is a fixed three-panel layout (cards list, preview,
form) where each panel scrolls on its own and the card always scales to fit (use the **zoom** menu for
50/75/100%). Below ~1100 px wide it stacks into one normally scrolling page.

Moves are saved per card as `layout` (px at a 1080 base, scaled for other sizes):

```json
"layout": { "title": {"x": 0, "y": -20, "s": 1.1},
            "logo": {"x": 700, "y": -40, "s": 1.4},
            "net": {"x": 0, "y": 0, "s": 1, "hide": true},
            "extras": [ {"type":"text","text":"New","x":88,"y":120,"size":44,"color":"accent","weight":700,"s":1},
                        {"type":"image","src":"assets/logo.png","x":600,"y":100,"w":160,"s":1} ] }
```

Guard rules (editor status bar and render script): no element may leave the card, text may
not overlap text/logo/image/bar, the headline may not exceed 4 lines or have a word wider
than the card. With a custom headline size the headline no longer auto-shrinks.
 It listens on
127.0.0.1 only and can write only `<kit>/calendar/*.cards.json`, `<kit>/designs/` and `<kit>/assets/uploads/`.
Stop it with Ctrl+C (or `pkill -f serve_editor.mjs`). Use `--port` if 8790 is taken.

Render a month of cards (all, or only the approved ones):

```bash
node <this-skill>/scripts/render_cards.mjs \
  --kit <brand kit dir> --cards <kit>/calendar/2026-11.cards.json --out <kit>/designs/2026-11
# options: --approved-only, --only id1,id2, --scale 2 (sharper, 2160 px), --chrome <path>
```

`cards.json`:

```json
{ "defaults": { "w": 1080, "h": 1080 },
  "cards": [ { "id": "p1-launch", "kicker": "Brand", "title": "Headline with [highlight]",
               "body": "One short supporting line.", "cta": "example.com",
               "alt": "Alt text for accessibility", "bg": null } ] }
```

Checks: the headline fits (shrinks to a minimum, ≤ 4 lines), the PNG is exactly the
requested size, no asset fails to load, no page error. A failing card is not written and
the exit code is 1. It also writes `manifest.json` (sizes, headline size, alt text).
It copies the template into `<kit>/.render/` (gitignored) and serves the kit on a
temporary local port.

Chrome is found at the standard macOS/Linux/Windows paths, or set `CHROME_PATH`.

Determinism: two renders of the same card can differ by a few hundred anti-aliased pixels on the
logo's edge (Chrome's image resampling), invisible to the eye. Compare with a tolerance, not md5.

Fallback (no script): copy `templates/post-card.html` to `<kit>/.render/`, serve the kit
over HTTP, open it with the Playwright MCP at the exact viewport size, wait for
`document.documentElement.dataset.ready === '1'`, check `dataset.overflow === '0'`, and
screenshot the `#stage` element.

Gotchas:
- Serve the **kit root**: the template loads `../tokens.json`, the logo and fonts relative
  to `.render/`.
- Add `?debug=1` to a template URL to see the safe margins and the fit status.
- Fonts must be WOFF2/TTF files listed in `tokens.json` (paths relative to the kit root).

## 2. AI artwork MCP (optional) — e.g. Higgsfield

Server URL: `https://mcp.higgsfield.ai/mcp` (no API key; credit-based).

```bash
claude mcp add --transport http higgsfield https://mcp.higgsfield.ai/mcp
```

Then `/mcp` → `higgsfield` → authenticate. See `reference/higgsfield.md`.
Pricing is not verified (third-party sources conflict): check the provider's
pricing page and test on the free allowance first.

Network note: a corporate proxy blocked `higgsfield.ai` on an employer-managed
machine. Use the machine and network the project's `guardrails.md` designates.

## 3. Public URLs for scheduling (needed by Metricool)

Metricool's `createScheduledPost` only accepts **public URLs** for media (and
Google Drive/Dropbox links, auto-uploaded). Options, with trade-offs:

| Option | Pros | Cons |
|---|---|---|
| **Object storage with a custom domain (recommended), e.g. Cloudflare R2** | Decoupled from the website; instant publish; automatable; cheap/free tier (R2: 10 GB, 1M writes, free egress) | One-time setup; R2 must be enabled on the account (may ask for a payment method) |
| Folder in the website repo (`public/social/`) | No new service | Git history bloat; PR + deploy per batch; content coupled to code |
| Google Drive / Dropbox links | No hosting | Must be linked in Metricool; manual sharing; hard to automate |
| Attach images by hand in the scheduler | No infrastructure | Manual step per post; error-prone |
| Separate public GitHub repo (raw links) | Free | Not a CDN; the repo/handle is public (can conflict with a low-profile rule) |

Record the chosen host and the upload command in the brand kit's
`publishing.md`. Keep the brand kit itself out of public buckets/folders: only
approved, ready-to-post images are uploaded.

Check once whether the scheduler copies the image at creation (then objects can
be removed later) or links to your URL (then keep them): compare the media URL
returned by `getScheduledPosts` with yours.

- [x] Confirmed (Metricool, 2026-11-11): the scheduler accepts the public URLs
- [x] Confirmed: Metricool **copies** the image to its own storage when the post is created, so the object can be
      removed from the host afterwards (keep it until the post is published, to be safe)
