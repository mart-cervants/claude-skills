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
  --name p1-lanzamiento --prompt "<creative idea>" --text-zone left --ratio 4:5 --n 3
```

- `--prompt` is **the creative idea only**. The script appends the brand rules from `tokens.json`
  (background and accent colours) and "no text / logos / people". Fold motifs from
  `visual-identity.md` into the idea yourself.
- `--text-zone` asks the model to keep that area calm and dark for the headline.
- `--dry` prints the final prompt and estimated cost without calling the API. Always dry-run first.
- Output: `<kit>/assets/backgrounds/<name>-<i>.jpg` and a sidecar `.json` (prompt, model, date,
  contrast grid). Files are numbered, never overwritten.
- Then upload the pick in the card editor as the card background and dim/scrim as needed.

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

Same as `higgsfield.md`: text-free only, composite text and logo with the template, 2–4 candidates,
no people unless the kit's `guardrails.md` allows them, log what you keep in `inspiration/notes.md`.
