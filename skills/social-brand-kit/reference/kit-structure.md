# Brand kit structure

One folder per brand, inside its project (default `marketing/social/`), found
via `Social brand kit: <path>` in the project's `CLAUDE.md`.

```
<kit>/
  brand-profile.md     what the brand is, audience, offer, goals, language, links, channels
  voice.md             tone, vocabulary, formats, CTAs, REAL writing samples, good-vs-bad
  guardrails.md        what must never be said/shown (confidentiality, claims, legal)
  pillars.md           content pillars, mix, idea sources, idea interview, "what worked"
  visual-identity.md   colors, type, motifs, sizes, do/don't
  tokens.json          machine-readable colors, fonts, logo path (used by social-visuals)
  idea-backlog.md      sourced, scored ideas (owned by content-ideas)
  results.md           monthly review of what worked (owned by the posting skills)
  assets/              logo, fonts, reusable images
  designs/             finished brand designs (covers, profile picture, templates)
  inspiration/         references the user likes (images) + notes.md (patterns)
    viral/             analyzed viral/high-performing references (private)
  calendar/            YYYY-MM.md monthly calendars (planned and approved posts)
  .render/             temporary folder for rendering (gitignored)
```

## Who reads/writes what

| File | Read by | Written by |
|---|---|---|
| brand-profile, voice, guardrails, pillars | all content skills | social-brand-kit (setup), user |
| visual-identity, tokens.json, assets | social-visuals | social-brand-kit, user |
| inspiration/, notes.md | content-ideas, social-visuals | user, content-ideas |
| idea-backlog.md | content-ideas, posting skills | content-ideas |
| calendar/, results.md | posting skills, content-ideas | posting skills |

## Rules

- Skills never store brand facts inside the skills repo; only generic method.
- Don't place the kit inside deployed folders (`public/`, `static/`, `dist/`).
- Commit the kit with the project unless it contains sensitive information; in
  that case keep the kit outside git or gitignore the sensitive files.
- `inspiration/` is gitignored by default (others' content; copyright).
