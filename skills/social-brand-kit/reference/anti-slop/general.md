# Anti-slop checklist (language-independent)

Run every draft through this before showing it to the user. Fix failures
silently when it's just a rewrite; report anything that changes the meaning.
Also apply the language pack (`<lang>.md` in this folder) and the brand's own
banned phrases in `voice.md`.

## 1. The specificity test (most important)

Replace the brand name with a competitor's. If the post still works, it's
generic — rewrite it around a concrete situation, a detail the user gave you, a
real tool, or a real mistake. Also check: does the post contain at least one
**concrete detail** (a tool, a situation, a step, a small number the user
provided)?

## 2. Structural tells

- "Not X, but Y" / "Not only X but also Y" used as a pattern.
- Every list has exactly three items; every paragraph ends with a punchline.
- Em-dashes more than once per post; heavy colon-and-bullet structure.
- An emoji at the start of every line or bullet. Default 0–2 emojis per post.
- Hashtag stuffing (default max 2).
- An opening line that restates the topic ("Today I want to talk about…").
- Closing with a generic engagement question that has no real question behind it.
- All sentences the same length; sentences nobody would say aloud.
- Inflated adjectives (innovative, revolutionary, cutting-edge, seamless).

## 3. Claims

- Any number, statistic or "study shows" without a source the user gave →
  remove or ask.
- Any result, client, testimonial or before/after the user hasn't confirmed
  exists → forbidden (also see `guardrails.md` in the kit).
- Superlatives ("the best", "unique", "guaranteed") → remove.

## 4. Read-aloud test

Read it as if saying it to the customer across a table. Rewrite anything you'd
feel silly saying.

## 5. Final checks

- [ ] Hook works alone in the first ~125 characters (Facebook cuts after that)
- [ ] One idea, one CTA
- [ ] Right language and register for the market (per `voice.md`)
- [ ] Nothing that breaks `guardrails.md`
- [ ] No invented numbers, clients or results
- [ ] 0–2 emojis, 1–2 hashtags unless the brand says otherwise
- [ ] Passes the specificity test
