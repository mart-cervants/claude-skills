# Analyzing inspiration (Mode C)

The user collects posts they like or know performed well, into the kit's
`inspiration/` (and `inspiration/viral/` for high performers). Claude turns each
into a **pattern**, not a copy.

## What Claude can and can't read

- **Can:** images (screenshots of posts, covers, carousels, Reels frames),
  pasted captions, transcripts, comments, and metrics the user notes.
- **Can't:** watch video or hear audio. For Reels, ask for 3–6 frame
  screenshots (hook, middle, end), the caption, the on-screen text, and the
  spoken text/transcript. Claude can sample frames from a local video only if
  a tool like ffmpeg is available; confirm before relying on it.

## Intake (ask the user for each reference)

1. The screenshot(s) or file, and the link if there is one.
2. The format (single image, carousel, Reel, text).
3. Metrics seen and the date (views/likes/comments/shares; account size if known).
4. Why they think it worked, in their own words.
5. Is it from the same niche/audience as the brand, or a different one?

## Pattern analysis (fill one row per reference in `inspiration/notes.md`)

| Element | Question |
|---|---|
| **Hook** | What's in the first line / first 3 seconds? What type: question, bold claim, number, story, "mistake", visual surprise? |
| **Structure** | How is it organized? (problem → cause → fix, list of N, before/after, myth vs fact, step by step, story) |
| **Format and length** | Image card, carousel (N slides), Reel (seconds), text length |
| **Visual style** | Layout, type size, colors, pace of cuts, text on screen, faces/no faces |
| **Emotional trigger** | Curiosity, recognition, relief, controversy, usefulness |
| **CTA** | Comment keyword, save, share, link, DM |
| **Why it probably worked** | Hypothesis only; note survivorship bias and audience differences |
| **Transferability** | Does the brand's audience share the context? High / medium / low |

## Adaptation test (must pass before an idea is approved)

1. **Own information:** does the new post contain the brand's own knowledge,
   example, experience, data or demo that the reference does not?
2. **Different wording and creative:** would a side-by-side comparison show
   only a shared *structure*, not shared sentences or visuals?
3. **Audience fit:** does it make sense for this brand's audience and offer
   (not just "it got views elsewhere")?
4. **Guardrails:** does it pass the kit's `guardrails.md`?

If any answer is no, rework the idea or drop it.

## Why originality matters (Meta, 2025–2026)

Meta says it reduces distribution of unoriginal content and penalizes repeated
reposting of others' videos, photos or text without meaningful enhancement;
adding captions, borders, a watermark or simple stitching doesn't count. Content
you film or produce yourself is original, and remix-style content counts only
when it adds new information, analysis or substantial improvement. Details
change; check the current Meta guidance before relying on this.

- https://about.fb.com/news/2026/03/rewarding-original-creators-on-facebook/
- https://creators.facebook.com/blog/combating-unoriginal-content

## Output

For each reference: one row of pattern notes + 1–3 ideas (in `idea-backlog.md`)
with source `inspiration <ID>` and the adaptation-test result. Reusable
patterns (e.g. "mistake → fix → check" carousel) go into the kit's
`inspiration/notes.md` series styles so the visuals stay consistent.
