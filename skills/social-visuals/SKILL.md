---
name: social-visuals
description: Use when the user needs an image or visual for a social media post, cover, carousel, Reel card sequence or ad for any brand. Renders on-brand HTML templates with Playwright using the brand kit's tokens, logo and fonts, so text and logo are always exact; uses AI image models (e.g. the Higgsfield MCP) only for text-free background art, then composites. Network-agnostic — used by facebook-page-content and other posting skills.
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
| `reference/higgsfield.md` | Using AI artwork |
| `templates/post-card.html` | Default card (square / portrait / Reel frame) |
| `SETUP.md` | First run (rendering and optional MCPs) |

## Workflow

1. **Brief.** What is the single idea the visual says? Which network and size
   (from `visual-identity.md`)? Which format: card, carousel slides, Reel card
   sequence (3–6 cards)?
2. **Look at references.** Open images in the kit's `inspiration/` and its
   `notes.md` for the series style. Don't invent a new look per post —
   consistency is brand.
3. **Choose method.** Typographic card by default. Use AI artwork only if it
   adds value; check the cost first (see `reference/higgsfield.md`).
4. **Build.** Copy `templates/post-card.html` into `<kit>/.render/`, set the
   parameters (kicker, title, body, cta, size, optional `bg`), or edit a copy
   for a new layout. Keep text short: one idea, a headline of ≤ 10 words.
5. **Render.** Serve `<kit>` over HTTP (see `SETUP.md`), open the template, set
   the viewport to the exact size, wait for fonts, and screenshot as PNG. Save
   to `<kit>/designs/` as `YYYY-MM-DD-slug.png`.
6. **Verify once, in one batched round.** View the PNG: text not clipped, safe
   margins, logo sharp, contrast OK when shrunk to ~400 px wide, spelling and
   accents correct. Fix everything found in one batch, check once more, stop.
7. **Deliver.** Give the user the file path(s). If the scheduler needs public
   URLs, hosting is a separate step (see `SETUP.md`).

## Do not

- Generate or edit the logo with an AI model; always use the kit's logo file.
- Put real client/third-party data or real screenshots in visuals; demo data only.
- Use stock clichés (handshakes, laptops with glowing charts, rockets, robots).
- Ship a visual with a typo — retype the text in the template, never regenerate.
- Copy another creator's visual; take structure/style cues from `inspiration/`
  and make the content and layout your own.
