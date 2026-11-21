# ads.md template (copy into the project's brand kit, e.g. `marketing/social/ads.md`)

Fill with the user. Mark every guess `(assumption)`. Replace assumptions with real
numbers as data arrives. Keep this file free of secrets (no tokens).

```markdown
# Ads — <brand>

## Account (checked by the skill before any write)
- Ad account id: <act_...>        # the ONLY account this project may use
- Ad account name: <...>
- Currency / time zone: <MXN> / <IANA>
- Page: <name>   Instagram: <handle or none>
- Business verification: <pending | done>
- Payment method and spending limit set: <yes/no>

## Goal
- Single conversion event: <WhatsApp conversation | booked call | form>
- Objective used in Meta: <...>
- Destination: <wa.me link | booking URL>  (opens correctly on a phone: yes/no)
- Tracking: <pixel / Conversions API / none> — events available: <...>

## Offer
- What is advertised: <...>
- Claims allowed (provable): <...>
- Claims never to make: <see guardrails.md>

## Budget
- Total test cap: <amount>
- Daily cap (all campaigns): <amount>
- Per-ad-set daily budget: <amount>   Window: <dates / weeks>
- Angles that fit: floor(total ÷ (per-ad-set daily × days)) = <n>

## Economics (assumption unless marked real)
- Ticket: <...>   Gross margin: <...>   LTV (12 mo): <...>
- conversation → call: <rate>   call → customer: <rate>
- Max CAC (break-even): <...>   Target CAC: <...>   Target LTV:CAC: <3>
- Break-even ROAS: <1 ÷ margin>
- Break-even cost per conversation: <...>

## Audiences
- Cold: <location, age, language, interests/job titles, exclusions>
- Warm / hot (remarketing): <sources, retention, minimum size, exclusions>

## Campaigns
### <YYYY-MM test-1>
- Type: test | scale | remarketing
- Structure: one ad set per angle, equal budget
- Angles (sourced): <angle id — idea id/source — one-line message>
- Creatives: <paths / R2 URLs; alt text; approved in editor: yes/no>
- UTM: source=facebook, medium=paid, campaign=<id>, content=<angle id>
- Pre-registered decision record:
  - Success metric: ...
  - Minimum data per ad set: impressions ..., link clicks ..., conversions ...
  - Continue if / Stop if / Scale if / Inconclusive if: ...
- Ids (after creation): campaign ..., ad sets ..., ads ...
- Launch date / planned review date: ...
- Results: (copy summary to results.md after the review)
```
