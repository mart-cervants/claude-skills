# AI artwork with an image MCP (e.g. Higgsfield)

Status: **not tested yet.** Facts come from Higgsfield's MCP page and
third-party write-ups; update this file after the first real run.

## What it is

Official MCP server, URL `https://mcp.higgsfield.ai/mcp`, no API key, 30+
image/video models (Nano Banana Pro, Flux, Seedream, Soul, Kling, Veo, …),
credit-based billing, plus prebuilt workflows (ads, resizing, localization).

## Rules (any brand)

1. **Text-free only.** Never ask for text, logos, UI labels or numbers in the
   image. Prompt "no text, no letters, no logos". The template adds all text.
2. **Preflight cost.** Pass `get_cost: true` (returns credit cost without
   generating) before any batch.
3. **Small batches.** 2–4 variations, pick one.
4. **Keep the brand palette in the prompt** — use the colors from `tokens.json`
   and the motifs from `visual-identity.md`.
5. **Composite, don't ship raw.** Place the art as the `bg` of the card template
   (a scrim keeps text legible).
6. **No people** unless the kit's `guardrails.md` allows them.
7. **Log what you keep**: model, prompt, file, where used → `inspiration/notes.md`
   ("AI artwork log").

## Prompt starter (fill from the kit)

```
{{subject / abstract scene}} on a {{background color}} background, with
{{accent color}} and {{secondary color}} highlights, {{motif from visual-identity.md}},
soft depth, minimal, premium, high contrast, lots of empty space on the left for
text. No text, no letters, no logos, no people.
```

Match the aspect ratio to the target (1:1, 4:5, 9:16, 16:9). Ask for 2K and
downscale.

## Cost and plan notes (unverified)

Sources conflict: a small free daily allowance with limits/watermark, paid plans
from roughly $5–15/month, about 2 credits per Nano Banana Pro image. Confirm on
the provider's pricing page, and test on the free allowance first (check for
watermarks).

## When NOT to use it

- A tip, list, checklist or steps → the typographic card is better.
- Anything that needs exact text, logo or diagram labels.
- When you generate only a handful of images a month.
