# Build Sequence — Reference (cold-email best practices)

## Cadence

- Default to 4-5 follow-up steps (5 total touches including the first
  email) — sequences under 3 touches meaningfully underperform on replies.
- Gap 2-4 days between steps. Faster reads as spammy/aggressive; slower
  loses momentum and top-of-mind presence.
- Don't front-load all steps at once — stagger via
  `update_sequence_schedule` so sends land during business hours in the
  recipient's timezone where that data is available.

## Formatting & deliverability

- Default new steps to text-only (no heavy HTML/images) — plain-text
  formatted emails land in inboxes more reliably than heavily designed
  ones.
- Every sequence must have an unsubscribe mechanism configured before going
  live — check `get_sequence_settings` / `update_sequence_settings` for the
  unsubscribe link setting and make sure it's on.
- Also enable `unsubscribe-via-email-header` (setting code 13) on every new
  sequence by default — a reply-based opt-out ("Reply 'Stop'...") is not
  the same as the formal `List-Unsubscribe` email header mailbox providers
  use for one-click unsubscribe. Confirmed via a real mail-tester.com test
  (2026-09-06) that a sequence without it scored 10/10 everywhere else but
  was flagged specifically for missing this header — free, safe fix, no
  downside, so just turn it on rather than asking.
- Keep subject lines short, specific, and non-salesy — avoid ALL CAPS,
  excessive punctuation, or spam-trigger words ("free", "guarantee", "act
  now").

## Personalization

- Use merge fields (first name, company, role) rather than generic
  greetings — pull the exact field labels from `list_fields` so tokens
  actually resolve instead of showing literal placeholder text.
- The first line of the first email should reference something specific to
  the lead/company, not just the merge tokens — generic personalization
  (just inserting a name token) doesn't move reply rates much on its own.

## Copywriting tone (validated against real Reddit threads, 2026-09-06)

Sources: [56% positive-reply-rate breakdown](https://www.reddit.com/r/Coldemailing/comments/1u8ftw4/the_exact_cold_email_setup_that_got_me_56/) (36 comments), [what actually gets replies, not just opens](https://www.reddit.com/r/b2bemailing/comments/1vjjkz9/ive_sent_thousands_of_cold_emails_heres_what/) (50 comments), and pushback found in [Brutally rate my cold email template](https://www.reddit.com/r/FinancialCareers/comments/1vvshr1/brutally_rate_my_cold_email_template/).

- Don't open with "My name is X and I work at Y, we help companies do Z" —
  the top delete-trigger. Open with something about *them*: a role/pain
  point, an observation, a trigger event.
- State what you do in one sentence, max. No mission paragraph, no feature
  bullets.
- Keep the ask tiny, not "30 minutes for a demo." Lines like "worth a
  quick chat?" or "is this even relevant to what you're working on?"
  outperform hard CTAs — the second gets replies even on a "no," which is
  still useful signal.
- Length: fully readable on a phone screen without scrolling. If it takes
  more than 3 short paragraphs, that's a positioning problem, not a copy
  problem. Short sentences, plain words — aim for roughly 8th-grade
  reading level (Hemingway-editor style: short sentences, active voice, no
  filler adverbs).
- No links or attachments in the first email — strong spam-trigger. Add
  them from step 2 onward, once there's been an open or reply.
- Most replies come from follow-up 2 or 3, not the first email — this is
  the argument for the 4-5 step cadence above, not just a nice-to-have.

**Caveat found in pushback comments — don't over-apply the above:** on the
`r/FinancialCareers` thread, the top-voted criticism of a short, casual,
copy-pasted template was "Snore. Literally same copy and paste... Research
the person, draft up something made by YOU and not ChatGPT or Claude."
That thread is 1:1 networking asks (a stranger doing you a personal
favor), a much higher personalization bar than B2B outbound offering a
concrete product/value (the two other threads' context). The lesson that
generalizes: spintax variation and a tiny-ask structure are not a
substitute for the email being relevant to the specific recipient — they
just avoid literal duplicate-content spam triggers. If the same {{Company}}
value could be swapped into every send with the sentence still making
sense, the email is too generic regardless of how good the sentence-level
copy is.

## Spintax

Saleshandy supports spintax for both subject line and body, to generate
variation across sends and avoid identical-content spam triggers. Syntax
is `{spin} option one | option two | option three {endspin}` (pipe-
separated options between `{spin}` and `{endspin}` — NOT the `{a|b}`
bracket shorthand used by some other tools, which Saleshandy does not
parse). Use it where a phrase has multiple natural equivalent phrasings
(openers, sign-offs, CTA phrasing) — never spin the specific/factual
content (names, numbers, the actual value proposition), since that's
what needs to stay true, not just varied. Preview rendering per-prospect
and send a test email to confirm before activating a sequence with new
spintax.

## Filtering leads before enrollment

There's no MCP tool equivalent of the app UI's "tag → move to CRM/Prospects
→ create a filtered saved view → send to sequence" flow. `add_leads_to_sequence`
collapses tagging + prospect creation + enrollment into one call
(`leadIds` + `sequenceId` + `stepId`, with `newTags`/`tagIds` for tagging),
but there's no server-side "filter" step — any filtering (e.g. "only leads
with a non-empty Company Industry, since the sequence copy uses
`{{Company Industry}}`") has to happen on the lead list *before* calling
the tool:

1. Get the lead data with the field to filter on (a Lead Finder CSV export,
   or the `sage_search` results if still in-session).
2. Drop/set aside rows where the required field is blank. Confirm with the
   user whether to backfill those rows some other way or just exclude them
   from this enrollment — don't silently drop leads without saying so, since
   it changes the addressable list size (e.g. ~5-10% of an 800-lead list).
3. Call `add_leads_to_sequence` with only the filtered `leadIds`.

This produces the same end state as the manual tag/view workflow (tagged,
filtered, enrolled) without needing the CRM/saved-view UI at all.

## Account attachment

- Never attach an account that failed `saleshandy-account-health`
  thresholds to a live sequence.
- Spread sending across multiple warmed accounts rather than loading one
  account with the full volume — this is what `add_email_accounts_to_sequence`
  and `update_sequence_priority_distribution` are for.
