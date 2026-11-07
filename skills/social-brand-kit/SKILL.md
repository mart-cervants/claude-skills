---
name: social-brand-kit
description: Use when setting up social media content work for any brand, business or page — creates and maintains the per-project "brand kit" (brand profile, voice, guardrails, pillars, visual identity, inspiration, backlog) inside the project, by reading a website, social page or description and confirming it with the user. Also the shared reference for how the other social skills (content-ideas, facebook-page-content, social-visuals) find and use the kit. Use first on any new brand, or when the kit is missing or outdated.
---

# Social Brand Kit

## Overview

The other social skills (`content-ideas`, `facebook-page-content`,
`social-visuals`) are generic: they hold method and templates, **never
brand-specific facts**. Everything specific to one brand lives in a **brand kit**
folder inside that brand's project (or a folder the user names). This skill:

1. **Locates** the kit (or creates it).
2. **Discovers** what the brand is about from a website, social page, or the
   user's description, then confirms it with the user.
3. **Maintains** the kit as things change.
4. Holds the shared **anti-slop** quality rules (all content skills use them).

## Locating the kit (all social skills follow this)

1. A line in the project's `CLAUDE.md`: `Social brand kit: <path>`.
2. Otherwise `marketing/social/` in the current project.
3. Otherwise ask the user for the folder (or offer to create one here).

If no kit exists, stop the content work and run the setup below first. Never
fall back to generic assumptions about the brand.

Read `reference/kit-structure.md` for the folder layout and what each file is for.

## Setup workflow

1. **Ask the basics**, in this order:
   - Which **language** will the content be written in (and which market/region,
     e.g. Mexican Spanish, US English)?
   - A **source to learn from**: website URL (best), Facebook/Instagram/LinkedIn
     page URL, or a written description. Any combination.
   - Where should the kit live? (default `marketing/social/` in the project)
2. **Discover** with `reference/discovery.md`: read the public sources, draft a
   brand profile, and clearly separate **Inferred** from **Confirmed**.
   Social pages are often behind a login: if a page can't be read, say so and
   ask the user to paste the About text and a few recent posts. Never bypass a
   login.
3. **Confirm** with the user: audience, offer, goals, tone, what must never be
   said (confidentiality, claims, legal), CTA and links, posting channels.
4. **Create the kit** from `templates/` (copy each template, fill from the
   confirmed answers, leave clearly marked `TODO` where information is missing).
   Add the `Social brand kit:` line to the project's `CLAUDE.md` (ask first if
   that file is committed and shared).
5. **Visual identity.** Ask for the logo, brand colors and fonts (or extract
   them from the website CSS/images, and confirm). Fill `tokens.json`.
6. **Inspiration.** Explain the `inspiration/` folder (posts the user likes and
   knows work). Offer to start collecting them now (`content-ideas` analyzes
   them).
7. **Report** what was created, what's still `TODO`, and the next step
   (`content-ideas` → `facebook-page-content`).

## Rules

- Source of truth is the kit, then the user. Don't guess brand facts.
- Mark inferred vs confirmed. Ask before writing claims, credentials, prices,
  testimonials or client names into the kit.
- Keep the kit out of any deployed/public folder (e.g. `public/`, `static/`).
- `inspiration/` holds other creators' content for analysis only: gitignored by
  default, never republished.
- Respect confidentiality rules the user gives (employer, clients, personal
  identity) — they go in `guardrails.md` and override everything else.

## Quality references used by the content skills

- `reference/anti-slop/general.md` — language-independent checks.
- `reference/anti-slop/<lang>.md` — banned phrases per language. Ships with
  `es-MX.md`. For another language, create `<lang>.md` (ask the user for
  examples of generic phrases to avoid) and add it here.
