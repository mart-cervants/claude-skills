# Setup — social-visuals

## 1. Rendering (required)

Needs Playwright (the Playwright MCP, or `npx playwright`) and Python 3 for a
tiny local server. The template reads `../tokens.json`, the logo and the fonts
relative to its folder, so it must live **inside the brand kit**.

```bash
KIT=<path to the brand kit>                 # e.g. marketing/social
mkdir -p "$KIT/.render" "$KIT/designs"
cp <this-skill>/templates/post-card.html "$KIT/.render/post-card.html"
cd "$KIT" && python3 -m http.server 8765 &   # serve the KIT ROOT
# open http://localhost:8765/.render/post-card.html?w=1080&h=1080&kicker=...&title=...
# set the viewport to exactly w×h and take a screenshot -> PNG into $KIT/designs/
```

With the Playwright MCP: `browser_resize` to w×h, `browser_navigate` to the URL,
wait until `document.documentElement.dataset.ready === '1'` (and
`document.fonts.ready`), then `browser_take_screenshot` (type png). Stop the
server when done (`pkill -f "http.server 8765"`).

Gotchas:
- After navigating, re-check the viewport size (`innerWidth × innerHeight`) — a
  stale window size crops the render.
- `.render/` is for temporary copies; keep it gitignored (the kit's
  `.gitignore` does).
- If fonts don't load, check the paths in `tokens.json` (relative to the kit
  root) and that the server root is the kit.

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

## 3. Public URLs for scheduling (if needed)

Some schedulers want images as public URLs (confirm for the scheduler in use). A
zero-cost route: commit approved PNGs to the brand's website repo under a
public folder (e.g. `public/social/`) so they deploy to
`https://<site>/social/<file>.png`. Keep the kit itself out of public folders.

- [ ] Confirmed: the scheduler accepts image URLs
- [ ] Confirmed: the scheduler accepts uploads (then skip hosting)
