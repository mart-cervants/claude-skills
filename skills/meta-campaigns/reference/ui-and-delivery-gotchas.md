# Interface and delivery gotchas

Lessons from running real small-budget campaigns. Interfaces change; treat each
item as "verify this field", not as a fixed fact.

## Verify after creating (compare against the plan, field by field)

- **Country/location:** the interface may default to the account's or a
  different country silently.
- **Budget and type:** default daily budget can be much higher than intended;
  campaign-level vs ad-set-level budget; lifetime vs daily.
- **Dates:** start/end; a missing end date keeps spending.
- **Optimization goal and conversion event:** may fall back to a different goal
  (e.g. link clicks instead of conversations).
- **Audience:** age, gender, interests, languages; audience expansion /
  "Advantage+ audience" toggles.
- **Placements:** automatic placements may send most spend to one placement
  (e.g. Reels), which changes the quality of clicks.
- **Destination:** the link/WhatsApp number/booking page, UTM parameters.
- **Page and identity:** the correct Page (and Instagram account) is attached.
- **Status:** everything created paused until the user approves launch.

## Recommendation buttons

"Apply now" / "Turn on Advantage+" style recommendations can revert manual
targeting (e.g. audience limits) with one click. Don't apply them without
showing the user what changes. Turning off an automated audience can raise a
modal pre-selecting "keep current settings"; read before confirming.

## Delivery

- Several ads in one ad set: delivery concentrates on an early leader; the others
  can get a handful of impressions. Compare angles with one ad set per angle,
  equal budgets, or sequentially. A starved ad is "untested", not "worse".
- Each ad set/test pays its own learning phase; very small budgets stay in
  "learning limited". Expect volatile costs; judge on whole weeks.
- Per Meta, these **significant edits** reset learning: any change to targeting,
  any change to ad creative, a change of optimization event, **adding a new ad
  to the ad set**, pausing the ad set for 7+ days (re-enters learning on
  unpause), changing bid strategy. Budget, spend limit and bid/cost goal changes
  count depending on their size (no percentage published). Don't edit mid-test.
- Budget under-delivery on day 1–2 is common; judge delivery after several days.

## Measurement

- Link CTR on mobile/Reels can be inflated by accidental taps. Cross-check with
  own analytics by `utm_content` and look at post-click engagement.
- Platform "landing page views" vs own sessions often differ (in-app browsers,
  blockers, consent banners). Reconcile before reporting.
- Few pixel events = no useful remarketing or conversion optimization. Check
  event counts and audience sizes before designing for them.
- Attribution windows and modeled conversions inflate or shift counts; for
  messaging campaigns count real conversations.
- A pixel that honors the site's cookie opt-out will under-count opted-out
  visitors; know the consent model.

## Setup traps

- Meta's own snippet pasted on top of an app-level pixel double-fires events.
- Test-events tools need a publicly reachable URL (not localhost).
- Interface language can change how interests render; switch to English to
  confirm interest names when a label looks wrong.
- Some brands/tools have no matching interest; use job titles, behaviors or
  lookalikes instead of forcing a poor match.
- A Page is required to run ads; business verification and the account currency
  are hard to change later — decide them first.
- Don't use another business's ad account, Page, pixel or creatives.

## Policy and content

- Ads are reviewed; claims about results, before/after, or guarantees can be
  rejected. Use claims the brand can prove (see `guardrails.md`).
- Don't use real third-party documents, logos or people in creatives; use
  fictional examples.
- Ads are public (Ad Library): assume competitors and customers can read them.
