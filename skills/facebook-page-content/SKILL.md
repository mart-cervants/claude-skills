---
name: facebook-page-content
description: Use when the user wants to plan, write, review, or schedule Facebook Page posts for any brand — monthly content calendars, post copy, format choice (card, carousel, Reel, text), and scheduling through the Metricool MCP. Works from the brand kit and approved ideas, applies the brand voice and the anti-slop checklist, generates visuals via social-visuals, and never schedules or publishes anything the user hasn't approved. Facebook-specific; other networks add notes under reference/network-notes/.
---

# Facebook Page Content

## Overview

Turns approved ideas into a month of Facebook Page posts that are ready to
publish: a calendar, copy in the brand's voice and language, a visual per post,
and scheduled posts waiting in Metricool for the user's approval.

**Core principle — Claude shapes real ideas, it doesn't invent them.** Posts
start from approved, sourced ideas (`content-ideas`) or raw inputs the user
provides. **Second principle — nothing goes out unseen.** Posts are created as
drafts / for review and the user approves them.

Brand-agnostic: every brand-specific fact (voice, guardrails, pillars, links,
visuals) comes from the **brand kit** (see `social-brand-kit`). If the kit is
missing, run `social-brand-kit` first; don't assume anything about the brand.

## Prerequisites

1. Locate the kit: `Social brand kit:` line in the project's `CLAUDE.md`, else
   `marketing/social/`, else ask.
2. Confirm the **language and market** from `brand-profile.md` (ask if absent).
3. Read from the kit: `guardrails.md` (always first), `voice.md`,
   `brand-profile.md`, `pillars.md`, `results.md`, `idea-backlog.md`.

## Reference files

| File | Read when |
|---|---|
| `reference/facebook-best-practices.md` | Choosing format, cadence, timing, hooks |
| `reference/calendar-template.md` | Producing the calendar |
| `reference/network-notes/README.md` | Adding another network |
| `SETUP.md` | First run, or if scheduling tools are missing |
| (`social-brand-kit`) `reference/anti-slop/general.md` + `<lang>.md` | After drafting, as the quality gate |

## Workflow

1. **Guardrails.** Read the kit's `guardrails.md`. If the request would break it
   (confidentiality, invented claims), say so and offer a compliant version.
2. **Inputs.** Use `approved` ideas in the kit's `idea-backlog.md`. If there are
   none or too few, run the `content-ideas` skill (inputs, research, or
   inspiration) — don't invent ideas.
3. **Plan the month.** Choose pillars and the mix from `pillars.md` (default 80/20
   educate vs promote), format per idea from its format candidates, and cadence
   (default 2–3 posts/week; adjust to what the user can reply to). Produce the
   calendar table from `reference/calendar-template.md`. Show it and get OK
   before drafting full copy. Save it as `<kit>/calendar/YYYY-MM.md`.
4. **Draft.** One idea per post, in the kit's voice and language. The first
   ~125 characters must work alone (hook). Mark hypotheticals as such.
5. **Anti-slop gate.** Run every draft through the `social-brand-kit` anti-slop
   checklist (general + the language pack + the brand's own banned phrases).
   Fix failures before showing the user; report meaning changes.
6. **Visuals.** For each post, use the `social-visuals` skill with the kit's
   tokens. For Reels from cards, produce the card sequence there.
7. **Review round.** Show the full month as one table (date, pillar, format,
   hook, full text, visual, CTA). Let the user edit, drop or reorder. Don't
   schedule yet.
8. **Schedule (Metricool MCP).** After explicit approval, create the posts as
   drafts / for review, one per date, in the time zone from `brand-profile.md`.
   Test with ONE post first and confirm it appears in the Metricool planner with
   the right text, date and image before creating the rest. Mind the plan's
   monthly scheduling cap (Free: 20 posts/month).
9. **Close the loop.** Monthly, pull Facebook post/Reel analytics and write
   `<kit>/results.md` (what worked, what to stop, experiments). `content-ideas`
   reads it.

## Gotchas

- Metricool tool names seen in its docs: `post_schedule_post`,
  `update_schedule_post`, `get_best_time_to_post`, `get_facebook_posts`,
  `get_facebook_reels`, `get_facebook_stories`. The list changes — check the
  tools actually available in the session.
- Unconfirmed until tested: whether media must be a public URL, how "for review"
  posts behave. Record what you learn in `SETUP.md`.
- Use only the canonical link(s) from `brand-profile.md` in posts.
- Respect `guardrails.md` identity rules (names, photos, employer mentions).
- Repurposing others' content is penalized by Meta; inspiration gives patterns,
  not text (see `content-ideas`).

## Example

User: "Prepárame el contenido del próximo mes"

→ locate the kit; read guardrails, voice, backlog; confirm language
→ pick 12–14 approved ideas (or run `content-ideas`), assign formats and dates,
  show the calendar, wait for OK
→ draft, run the anti-slop gate, build visuals with `social-visuals`
→ show the full month table, apply edits
→ on approval, schedule 1 test post, verify in Metricool, then the rest
