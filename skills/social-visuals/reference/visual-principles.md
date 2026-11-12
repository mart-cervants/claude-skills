# Visual principles (generic)

Brand-specific palette, type and motifs are in the kit's `visual-identity.md`
and `tokens.json`. These rules apply to any brand.

## Craft

- **One idea per visual.** One focal point, large type, generous space.
- **One accent color.** Use the brand accent for the key word, a bar, or one
  icon — never to fill large areas.
- **Hierarchy:** label (kicker) → headline → one supporting line → footer
  (logo + CTA). Headline ≤ 10 words; supporting line ≤ 25 words.
- **Legibility at phone size.** On a 1080 px card: headline ≥ 64 px, body ≥ 34 px,
  label ≥ 26 px. If you must shrink text to fit, the idea is too big — cut it.
- **Contrast.** Meet at least 4.5:1 for body text; put a dark/light scrim under
  text over artwork.
- **Margins.** ≥ 64 px safe margin; nothing important in platform overlay zones
  (top/bottom ~250 px on Stories/Reels; bottom-left of a Page cover).
- **Consistency.** Reuse the same template per series so the feed reads as one
  brand. Define 2–3 series in `inspiration/notes.md`.

## Sizes (defaults; the kit may override)

| Use | Size (px) |
|---|---|
| Feed, square | 1080×1080 |
| Feed, portrait | 1080×1350 |
| Link preview | 1200×630 |
| Facebook Page cover | 1640×624 (central ~1,110 px survives the mobile crop) |
| Profile picture | 1024×1024 (circle-safe: keep content in the central ~70%) |
| Story / Reel | 1080×1920 |

## Text fit and testing

- Shrink-to-fit needs a **minimum size** (56 px on a 1080 card) and a **maximum number of
  lines** (4). If the copy still doesn't fit, shorten it; never go below the minimum.
- Test every template with the **longest realistic copy**, not the example text.
- Stay with text, layout and vector shapes. Photos only as text-free full-bleed
  backgrounds; no composited cut-outs.
- Write alt text for every published image.

## Carousels and Reel card sequences

- 3–6 cards. Card 1 = hook; last card = CTA. One step or point per card.
- Same template, same position for the headline on every card.
- For Reels from cards: ≤ 30 s, ~3–5 s per card, text readable in that time.

## Don't

- Stock-photo clichés, fake dashboards that resemble real client data, text
  inside AI-generated art, more than two font weights, decorative extra fonts,
  low-contrast text over busy art.

## Quality gate

- [ ] Right pixel size, sharp logo
- [ ] Readable at ~400 px wide
- [ ] Margins respected; nothing clipped
- [ ] Spelling and accents correct for the language
- [ ] One accent, matches the brand and the series
- [ ] No claims or data the guardrails forbid
