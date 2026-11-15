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
  designs/             brand designs: one-off files at the top level are committed (cover, profile picture);
                       per-post renders go in subfolders (designs/YYYY-MM/) and are NOT committed
  inspiration/         references the user likes (images) + notes.md (patterns)
    viral/             analyzed viral/high-performing references (private)
  calendar/            YYYY-MM.md calendars and YYYY-MM.cards.json card data (local working files, NOT committed)
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
- Commit only the **stable** part of the kit (profile, voice, guardrails, pillars, visual identity,
  tokens, logo, fonts, brand designs). Copy `templates/kit.gitignore` to `<kit>/.gitignore`.
- **Per-post files are local only:** `calendar/*` (calendars + cards JSON), `designs/<month>/`
  (renders), `assets/uploads/`, `assets/backgrounds/` (AI candidates). They change with every post;
  committing them would mean a branch, PR and merge for each post. The source of truth after
  scheduling is the scheduler (text, date) and the media host (final images).
- Living docs that change often (`idea-backlog.md`, `results.md`) are committed by default; the
  user may gitignore them too. Local-only files have no backup: say so once, and suggest copying
  the month's `*.cards.json` somewhere safe if they care.
- If the kit contains sensitive information, keep it outside git or gitignore those files.
- `inspiration/` is gitignored by default (others' content; copyright).
