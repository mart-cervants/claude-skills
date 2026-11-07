# Adding another network

This skill is Facebook-first. To add a network (Instagram, LinkedIn, TikTok…):

1. Create `reference/network-notes/<network>.md` with:
   - format and size rules (text limits, image sizes, hashtags, link behavior)
   - best practices and benchmarks (with sources and evidence quality)
   - network-specific tone differences from `brand-voice.md`
   - Metricool notes (supported formats, per-network scheduling quirks)
2. In `SKILL.md`, add a line under "Reference files" and in step 4 (Draft):
   "If the target network is X, also read `network-notes/x.md`."
3. Reuse, don't duplicate: voice, anti-slop, guardrails and pillars stay shared.
4. If the network's workflow differs a lot (e.g. video-first), create a sibling
   skill `<network>-page-content` that points to the shared references.

Metricool can post different text per network ("a different caption for each
network"), so one raw idea can become one post per network.
