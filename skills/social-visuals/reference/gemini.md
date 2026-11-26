# AI backgrounds with the Gemini API (Nano Banana)

Alternative to an image MCP (Higgsfield etc.) — works with just an API key, so it also works on
networks where MCP image services are blocked. Script: `scripts/gen_background.mjs`.

## Setup (once per machine/brand)

1. Create a key in Google AI Studio (use the brand owner's own Google account/project).
2. Image models have **no free API tier**; Google may require **prepaid credits** — load the
   smallest amount allowed (≈ US$0.034 per 1K image, so US$5 ≈ 150 images). The AI Studio web UI is free
   for manual generation if you prefer to skip the API.
3. Put `GEMINI_API_KEY=...` in the project's git-ignored `.env.local` (or export it). Never commit,
   print or paste the key. Restrict it to the Generative Language API in Google Cloud.
4. `cd <skills>/social-visuals/scripts && npm install` (adds `sharp` for the contrast check).

## Use

```
node <skills>/social-visuals/scripts/gen_background.mjs --kit marketing/social \
  --name p1-lanzamiento --prompt "<creative idea>" --text-zone left --ratio 4:5
```

**One candidate by default (`--n 1`) to save money** (~US$0.03 each). Ask for `--n 2` or `--n 3` only when exploring a new style
or a cover that sets the look of a series. A single candidate is easy to adjust afterwards: move/scale/dim it in the card editor, or
regenerate just that one (`--edit` for small tweaks, `--ref` for a fresh take).

- `--prompt` is **the creative idea only**. The script appends the brand rules from `tokens.json`
  (background and accent colours) and "no text / logos / people". Fold motifs from
  `visual-identity.md` into the idea yourself.
- `--text-zone` asks the model to keep that area calm and dark for the headline.
- `--dry` prints the final prompt and estimated cost without calling the API. Always dry-run first.
- `--edit <image>`: `--prompt` becomes a change instruction ("darken the left third"); output is
  `<name>-edit-<i>`. Good for small tweaks. **Not reliable for big style changes** (the same instruction kept
  the old style in one run and worked in another).
- `--ref <image>` (repeatable): use an image as a composition/palette guide for a **fresh** generation.
  Better than `--edit` when the style must change; expect faint leftovers of the reference.
- Output: `<kit>/assets/backgrounds/<name>-<i>.jpg` and a sidecar `.json` (prompt, model, date,
  contrast grid). Files are numbered, never overwritten. The folder writes its own `.gitignore`
  (`*`, which also hides that file): candidates are never committed. Keep a local `log.md` of the
  chosen ones (file, prompt, model, date, R2 URL) — it is local too, so the media host is where
  the final background lives.
- Then upload the pick in the card editor as the card background and dim/scrim as needed.

## Using the pick on a card

Set the card's `bg` to a kit-relative path the editor serves (`assets/uploads/<file>`) or an `https` URL
(e.g. R2). Set `"net": 0` so the template's decorative node network doesn't draw over the art. `dim`
controls the left-to-right scrim. Note: a remote `bg` can fail behind a corporate web proxy that
redirects or blocks the request; the renderer now fails the card with "background image failed to
load" instead of silently rendering without it. Don't bypass the proxy; render from a personal network
or use a local file.

## Contrast report

Each candidate is scored on a 3×3 grid: contrast of the kit's text colour against the **brightest 10%**
of each cell. `✓` ≥ 4.5, `~` ≥ 3 (large headlines only), `✗` < 3. Choose the candidate whose text
zone is `✓`. This is a pre-selection aid; the rendered card is still the final check.

## Facts (verified against Google's docs, Nov 2026 — re-check before relying on them)

- Model `gemini-nano-banana-2.1`: 1K $0.0336, 2K $0.0504, 4K $0.113 per image (batch ≈ half).
- `gemini-2.5-flash-image` is deprecated (shuts down 2027-03-15). Don't build on it.
- Outputs carry an invisible SynthID watermark.
- Aspect ratios `1:1` and `4:5` (returns 928×1152) were tested and work; 5:4 and 16:9 are in Google's
  examples. If a ratio is rejected the script prints the API error — crop in the editor instead.
- First real run (3 candidates, ~US$0.10): the response nests the image under `steps[].content[]`; the
  script finds it by searching for an `image/*` block, so it survives layout changes.
- Image-to-image editing and reference images are supported by the API but not wired into the
  script yet.

## Rules

Same as `higgsfield.md`: text-free only, composite text and logo with the template, 1 candidate by default (2–3 only to explore a style),
no people unless the kit's `guardrails.md` allows them, log what you keep in `inspiration/notes.md`.

## Series of representative illustrations (any brand)

Use it when the owner wants each card to *show* its topic (a document, a chat, shelves, a map...) instead of an abstract
background. It is still text-free artwork: the template puts the text and logo on top.

**The look belongs to the brand, not to this skill.** Read it from the kit: the "Illustration series" section of
`visual-identity.md` (style sentence, anchor image, allowed and forbidden subjects, logo policy) and the series table in
`inspiration/notes.md`. If the kit has none yet, propose one with the user (steps 1–2 below), then **write it into the kit** so
the next batch, another machine or another session reuses it. Colours already come from `tokens.json`.

1. **Concept list first (no cost).** One line per card: the concrete subject and why it explains the topic. The user approves
   or changes the list before anything is generated.
2. **First card = style anchor.** Generate it (`--n 2` or `3` while the look isn't set), pick one, approve it in the editor and
   store the file in the kit as the series anchor (a stable brand asset, not a throwaway candidate).
3. **Every next card uses the anchor as reference:** `--ref <anchor>` plus the sentence "same visual style as the reference
   image". This keeps dozens of images in one consistent series. Use `--n 1` for the rest.
4. **Prompt recipe** (the script appends the palette from `tokens.json`, "no text/logos/people" and the calm text zone):
   - Style: the kit's style sentence (flat vs. isometric vs. line art, stroke, glow, background), ending with "same visual
     style as the reference image".
   - Position: "The subject sits in the right 40 percent of the frame, vertically centered, clearly visible and not too small."
     Without it, subjects sprawl under the headline and get muted by the scrim; with `--text-zone left` the headline stays free.
   - Blank shapes: "Shapes are blank: no numbers, no letters, no brand logos, no people."
   - One sentence "Subject: ..." that names the concrete objects and their arrangement.
5. **Subjects that explain without clichés.** Map each topic to concrete, recognizable objects from the brand's own industry.
   Pattern (examples only, adapt to the brand): a late report → pages with blank grids + a clock; mismatched figures → two bar
   charts + a not-equal sign; a process in steps → three connected icons; a checklist → card with ticked and empty boxes; stock
   → shelves with boxes + an alert dot in the accent colour. Respect the kit's `guardrails.md` and "Don't" list (stock cliché
   objects, fake dashboards that look like real data, people).
6. **Third-party logos** (messaging apps, office suites...): only if the brand allows it, and then composite the official file
   with the template; never ask the model to draw them (it deforms them).
7. **Review in one look.** Put the candidates side by side (any image tool, or the editor) instead of opening one by one,
   pick, copy the pick to `assets/uploads/` and set the card's `bg` and `"net": 0`.
8. **Cost:** about US$0.034 per 1K image (see the facts above); `--n 1` for almost every card.
9. **Carousel inner slides** need a simple icon each: `--n 1` is enough; fix size/position in the editor.
