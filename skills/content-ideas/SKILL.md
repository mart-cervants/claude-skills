---
name: content-ideas
description: Use when the user wants ideas for what to post on social media (posts, carousels, Reels), has few or no raw ideas, or wants to refill the idea backlog. Works from the brand kit: the user's real inputs, guided research, and analyzed inspiration (posts the user likes or knows performed well), and produces a sourced, scored, format-aware backlog. Borrows patterns, never content. Never invents ideas without a source. Brand-agnostic; hands approved ideas to a posting skill such as facebook-page-content.
---

# Content Ideas

## Overview

Produces a **sourced, scored, format-aware backlog** of post ideas for any
brand. Every idea carries its source, so nothing comes from the model's general
memory (the origin of generic "AI slop" ideas).

Three input modes, best first:

- **Mode A — the user's raw inputs.** Notes, voice-note transcripts, problems the
  user solved, questions customers asked, conversations with real customers.
- **Mode B — research feed.** A guided pass over public sources
  (`reference/research-sources.md`) to *produce* raw inputs when there are none.
- **Mode C — inspiration.** Posts/Reels the user likes or knows performed well
  (`inspiration/` in the brand kit). Claude extracts the **pattern** (hook,
  structure, format, style, why it likely worked), then rebuilds it around the
  brand's own information (`reference/inspiration-analysis.md`).

Ideas are **format-agnostic cores** (`reference/idea-formats.md`): each idea lists
format candidates (card, carousel, Reel, text) and the format is chosen at
planning time, because the evidence on which format wins is mixed.

This skill doesn't write posts or schedule them. Approved ideas go to a posting
skill (e.g. `facebook-page-content`). The monthly review lives in that skill's
`results.md`; this skill only reads it.

## Prerequisites

Locate the brand kit (see `social-brand-kit`: `Social brand kit:` line in the
project's `CLAUDE.md`, else `marketing/social/`, else ask). If there's no kit,
run `social-brand-kit` first. Ask which **language** the content is in if the
kit doesn't say.

Read from the kit: `brand-profile.md`, `guardrails.md`, `pillars.md`,
`voice.md` (vocabulary), `idea-backlog.md`, `results.md`, `inspiration/notes.md`.

## Reference files

| File | Read when |
|---|---|
| `reference/inspiration-analysis.md` | Mode C: analyzing viral/liked references (and the originality rule) |
| `reference/idea-formats.md` | Choosing formats: post vs Reel vs carousel |
| `reference/research-sources.md` | Mode B research pass |
| `reference/interview-guide.md` | Talking to real customers (best raw input) |
| `reference/scoring.md` | Scoring and vetting every idea |

## Workflow

1. **Guardrails first.** Read the kit's `guardrails.md`. Reject or reshape ideas
   that would break it (confidentiality, invented claims, real third-party data).
2. **Check the backlog.** Read `idea-backlog.md`. If there are ≥ 12 `approved`
   ideas, stop — no need to generate more.
3. **Choose input mode(s).** Ask what the user has:
   - raw inputs → Mode A;
   - references they like or know went viral → Mode C (start here if they have
     them; references also teach style and format);
   - nothing → offer, in order: (a) 2–3 short customer conversations
     (`interview-guide.md`), (b) a ~45-minute research pass (Mode B), (c) the
     idea interview in the kit's `pillars.md`. Never fall back to generic topics.
4. **Extract ideas.** Turn each input into post-sized ideas (one question
   answered, one mistake and its fix, one myth, one step), phrased the way the
   audience speaks, in the brand's language and register (`voice.md`).
5. **Record provenance** for each idea: `source` type and where exactly (real
   question, conversation, search, other Page's comments, inspiration ID,
   own experience). No source → discard.
6. **Add format candidates** per `idea-formats.md` (a single idea can have
   several), and the pillar.
7. **Vet and score** per `scoring.md`. Mark social/search-derived ideas
   `needs validation`; mark inspiration-derived ideas with the adaptation test
   result.
8. **Show the shortlist** (score, pillar, formats, source, one-line angle). The
   user approves, edits or drops. Update `idea-backlog.md`.
9. **Hand off.** Approved ideas are the input to the posting skill's planning.

## Rules

- No ideas without a source. No statistics unless the user supplies a source.
- **Borrow patterns, not content.** Never copy another creator's text, script or
  creative; the new post must carry the brand's own information or experience.
  Platforms deprioritize unoriginal reposts (see `inspiration-analysis.md`).
- Don't scrape platforms, bypass logins, or use third-party ad-spy tools. Use
  public pages and the user's own accounts; the user does logged-in steps and
  pastes or screenshots the findings.
- Treat comments/DMs as private: record the pattern of a question, never names.
- Viral ≠ transferable: reference metrics come from other audiences and show
  survivorship bias. Treat them as hypotheses to test on the brand's Page.
- Prefer 12–20 good ideas over 100 mediocre ones.
- Use a personal machine/network when the project is personal or confidential.

## Example

User: "No tengo ideas para el próximo mes, pero tengo 4 Reels que me gustan"

→ locate the kit, read guardrails, backlog (3 ideas)
→ Mode C: analyze the 4 references (screenshots + transcripts) into patterns
→ combine with the user's raw notes; Mode A for anything they remember
→ 14 ideas with sources, format candidates and scores; show the top 10
→ user approves 8 → backlog updated → handed to the posting skill
