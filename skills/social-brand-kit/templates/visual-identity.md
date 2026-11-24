# Visual identity — {{BRAND NAME}}

> Machine-readable values live in `tokens.json`. Keep both in sync. If the
> brand has a website design system (e.g. `DESIGN.md`), link it here and treat
> it as the source of truth.

## Palette
| Token | Hex | Use |
|---|---|---|
| background | TODO | |
| surface | TODO | |
| text | TODO | |
| muted text | TODO | |
| accent | TODO | One accent per visual |

Rules: TODO (e.g. one accent, dark/light background, forbidden colors).

## Typography
- **Headings:** TODO
- **Body:** TODO
- Minimum sizes on a 1080 px card: headline 64 px, body 34 px, label 26 px.

## Motifs and layout
- TODO — grid, shapes, illustration style, logo placement and safe margins.

## Illustration series (optional)
Fill this in when cards should *show* their topic with text-free AI artwork (`social-visuals`, `reference/gemini.md`).
- **Style sentence** (goes into the prompt): TODO — e.g. flat vs. line art, stroke weight, glow, background.
- **Anchor image:** TODO — path of the first approved card/illustration; every next one uses it as `--ref`.
- **Subject position:** TODO — e.g. subject in the right 40% so the headline stays free.
- **Subjects that fit the brand's industry:** TODO — concrete, recognizable objects.
- **Not allowed:** TODO — stock clichés, fake data that looks real, people, text inside the art.
- **Third-party logos:** TODO — allowed or not; if allowed, composite the official file, never AI-drawn.
- **Candidates per image:** 1 by default (money); more only to explore a style.

## Sizes
| Use | Size (px) | Notes |
|---|---|---|
| Feed, square | 1080×1080 | Default |
| Feed, portrait | 1080×1350 | |
| Link preview | 1200×630 | |
| Facebook Page cover | 1640×624 | Keep content in the central ~1,110 px (mobile crop); keep bottom-left clear (profile picture) |
| Profile picture | 1024×1024 | Circle-safe: keep the logo in the central ~70% |
| Story / Reel | 1080×1920 | Keep text out of the top/bottom ~250 px |

## Do
- One idea per visual, large type, plenty of empty space.

## Don't
- Stock clichés, fake dashboards that look like real data, text inside AI-generated art.

## Quality gate
- [ ] Right pixel size, sharp logo
- [ ] Readable at ~400 px wide
- [ ] Margins ≥ 64 px; nothing clipped
- [ ] Spelling and accents correct
- [ ] Matches the series in `inspiration/`
