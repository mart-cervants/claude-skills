---
name: social-visuals
description: Use when the user needs an image or visual for a social media post, cover, carousel, Reel card sequence or ad for any brand. Renders on-brand HTML templates with Playwright using the brand kit's tokens, logo and fonts, so text and logo are always exact; uses AI image models (the Gemini API script, or an image MCP such as Higgsfield) only for text-free background art, then composites. Network-agnostic — used by facebook-page-content and other posting skills.
---

# Social Visuals

## Overview

Produces on-brand PNGs for posts, covers, carousels and Reel cards, for any
brand. Brand specifics (colors, fonts, logo, style) come from the **brand kit**
(`social-brand-kit`): `tokens.json`, `visual-identity.md`, `assets/`,
`inspiration/`. Two methods, used together:

1. **Brand card (default).** An HTML template rendered to PNG with Playwright.
   Text, logo and layout are exact (no garbled letters).
2. **AI artwork (optional).** An image MCP (e.g. Higgsfield) generates
   **text-free** background art; the template then overlays the real logo and
   text on top.

**Core principle — never trust an image model with text or the logo.** Models
misspell words and distort logos. Anything with letters or the logo is
composited by the template.

## Prerequisites

Locate the kit (`social-brand-kit`: `Social brand kit:` line in `CLAUDE.md`,
else `marketing/social/`, else ask). Read `tokens.json`, `visual-identity.md`,
`guardrails.md`, `inspiration/notes.md`. If the kit has no logo or fonts, ask
the user for them or use the defaults in `tokens.json` and say so.

## Reference files

| File | Read when |
|---|---|
| `reference/visual-principles.md` | Always, before designing (generic craft rules) |
| `reference/higgsfield.md` | Using AI artwork through an image MCP |
| `reference/gemini.md` + `scripts/gen_background.mjs` | Using AI artwork through the Gemini API (key only; 3 candidates with a text-contrast report) |
| `templates/post-card.html` | The default card template (square / portrait / Reel frame) |
| `scripts/serve_editor.mjs` + `templates/editor.html` | Local review/edit canvas: live preview, drag/resize/snap, layers, fit warnings, approve, save, render |
| `scripts/render_cards.mjs` | Batch rendering with safety checks (see `SETUP.md`) |
| `SETUP.md` | First run (renderer and optional MCPs) |

## Workflow

1. **Brief.** What is the single idea the visual says? Which network and size (from
   `visual-identity.md`)? Which format: card, carousel slides, Reel card sequence
   (3–6 cards)?
2. **Look at references.** Open images in the kit's `inspiration/` and its `notes.md`
   for the series style. Don't invent a new look per post — consistency is brand.
3. **New series only: copy first, then layouts.** If there is no template for this kind
   of post yet: (a) get the approved copy and its hierarchy (kicker, headline, support
   line); (b) propose 2–3 layout concepts in plain words and let the user pick one;
   (c) only then build or adapt the template, with explicit tokens (hex colors, exact
   fonts) and a negative list. Existing series skip this step.
4. **Choose method.** Typographic card by default. Use AI artwork only if it adds
   value, as a text-free full-bleed background; check the cost first (see
   `reference/gemini.md` or `reference/higgsfield.md`). Don't composite cut-out product images or complex
   photos: stay with text, layout and vector shapes.
5. **Write the card data** (`<kit>/calendar/YYYY-MM.cards.json`, see `SETUP.md`): one
   entry per card with `id`, `kicker`, `title` (wrap the highlight in `[brackets]`),
   `body`, `cta`, `alt` (alt text for accessibility; Metricool accepts `mediaAltText`)
   and `status: "draft"`.
6. **Open the review editor and give the user the link — before rendering any PNG.**
   Start `scripts/serve_editor.mjs --kit <kit> --cards calendar/YYYY-MM.cards.json`
   (leave it running in the background) and hand over the printed URL, e.g.
   `http://127.0.0.1:8790/.render/editor.html?cards=calendar/2026-11.cards.json`.
   There the user sees every card live (the exact HTML that becomes the PNG), edits
   the text, **drags and resizes elements on the canvas** (snapping guides, layers with
   show/hide, X/Y/size fields, added text and images — uploaded from the computer or dropped on
   the card — a dimmable background image, undo/redo), sees fit/overflow
   warnings, sets `status` to `approved`, and saves. Moves are stored per card as
   `layout` offsets in the cards file, so the PNG always matches the preview.
   Wait for their approval. If they ask for layout/style changes (not just wording),
   edit `templates/post-card.html` and tell them to refresh.
7. **Longest-copy test.** Before a template joins a series, render it with the longest
   realistic headline and support line, not just the example text.
8. **Render approved cards** with `scripts/render_cards.mjs --approved-only` (or the
   editor's "Save + Render PNG" button). A card is written only if the headline fits
   (shrinks from 80 px to a 56 px minimum, ≤ 4 lines), the PNG is exactly the
   requested size, and no asset failed to load. A failure means: shorten the copy or
   fix the asset, then re-run (`--only <id>` re-renders one card).
9. **Verify once, in one batched look.** View the PNGs: contrast OK when shrunk to
   ~400 px wide, spacing, accents and spelling. Fix everything found in one batch,
   check once more, then stop polishing.
10. **Deliver.** Give the user the file paths. Upload only approved images to the
   brand's media host (see `SETUP.md` and the kit's `publishing.md`).

## Do not

- Generate or edit the logo with an AI model; always use the kit's logo file.
- Put real client/third-party data or real screenshots in visuals; demo data only.
- Use stock clichés (handshakes, laptops with glowing charts, rockets, robots).
- Ship a visual with a typo — fix the text in the card data and re-render; never regenerate with AI.
- Skip the overflow checks or edit the PNG by hand to hide a text overflow; shorten the copy.
- Render, upload or schedule cards the user hasn't reviewed and approved in the editor.
- Upload images the brand doesn't have the rights to, or real client, employer or personal photos.
- Copy another creator's visual; take structure/style cues from `inspiration/`
  and make the content and layout your own.
