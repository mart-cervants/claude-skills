---
name: meta-campaigns
description: Use when the user wants to plan, launch, review, scale or retarget paid Meta (Facebook/Instagram) ad campaigns for any brand or Page — a test/lab campaign comparing angles, scaling what works, or remarketing to people who engaged or clicked. Decides with numbers (CAC, LTV:CAC, break-even ROAS, cost per conversation/lead/booked call, link CTR, CPM, frequency) fixed before spending, reuses the brand kit and the content/visual skills for creatives, and operates through the Meta Ads MCP only after confirming the ad account and getting explicit approval of every spend-affecting change. Brand-agnostic; offer, audiences, budget and targets live in the project's ads.md.
---

# Meta Campaigns

## Overview

Turns "let's run ads" into a small, decided-in-advance experiment: what is being
tested, how much it may cost, what result means continue / scale / stop, and how
the winner gets retargeted. Then (optionally) builds and operates it through the
Meta Ads MCP with a confirmation gate on every change that can spend money.

**Principle 1 — decide before you spend.** Budget, objective, test structure,
minimum data and decision rules are written down in the project's `ads.md`
*before* anything is created. Judging after the fact, by feel, is how small
budgets get wasted.

**Principle 2 — inconclusive is a valid result.** With small budgets, "not enough
data to decide" is the honest outcome; never promote a winner from noise.

**Principle 3 — never touch the wrong account or spend unseen.** Confirm the ad
account on every session; show the exact change and wait for approval.

Brand-agnostic: this skill holds method only. Every brand fact (offer, audiences,
budget, margins, targets, account id) comes from the project's `ads.md` and
brand kit. If `ads.md` is missing, create it from `reference/ads-template.md`
with the user before anything else.

## Prerequisites

1. Locate the brand kit (`Social brand kit:` line in the project's `CLAUDE.md`,
   else `marketing/social/`). Read `guardrails.md` first (identity,
   confidentiality, claims), then `brand-profile.md` and `voice.md`.
2. Locate `ads.md` (same folder as the kit by default). Missing or incomplete →
   build it (workflow step 2). Incomplete = any of: declared ad account,
   conversion event, budget cap, economics, decision rules.
3. Read-only work (planning, reviewing numbers) needs no MCP. Operating needs the
   Meta Ads MCP (`SETUP.md`). Check which tools the session actually exposes;
   tool names vary by server and change over time.

## Reference files

| File | Read when |
|---|---|
| `reference/ads-template.md` | Creating or completing the project's `ads.md` |
| `reference/budget-and-structure.md` | First: turning the user's budget into how many ad sets/angles to run |
| `reference/campaign-types.md` | Designing a test, scale or remarketing campaign |
| `reference/metrics-and-thresholds.md` | Choosing the objective, computing targets, deciding on results |
| `reference/ui-and-delivery-gotchas.md` | Building in Ads Manager or via MCP; before any launch |
| `SETUP.md` | First run, or the MCP is missing or points to the wrong account |
| `social-brand-kit`, `content-ideas`, `social-visuals` | Voice/guardrails, sourced angles, creatives |

## Hard rules

1. **Account check first, every session and before any write.** Read the active
   ad account (id and name) from the MCP and compare it with the account
   declared in `ads.md`. Mismatch, or `ads.md` has none → stop and tell the
   user. Never "fix" it by switching accounts on your own. If the MCP is global
   and serves several businesses, this check is the only guard.
2. **Spend gate.** Anything that can start, raise or redirect spend (create
   active, unpause, raise budget, change audience/placement/bid, duplicate) is
   shown as the exact payload ("dry run") and needs the user's explicit OK for
   that payload. Approval of a plan is not approval of each change. Create
   campaigns, ad sets and ads **paused**; the user (or an explicit OK) activates.
3. **Respect the caps in `ads.md`** (total test budget, daily cap). If a step
   would exceed them, stop and ask.
4. **Read before write.** Before editing an existing campaign, read its current
   state and show what will change. Updates can't be undone in spend already made.
5. **No invented numbers.** Margins, ticket, conversion rates are the user's, or
   labeled assumptions. Benchmarks from this skill are orientation, not targets.
6. **Guardrails and low profile.** Ad copy and creatives follow the kit's
   `guardrails.md` (names, photos, employer, claims). Ads count as public content.
7. **Nothing from another business** — names, audiences, figures, creatives —
   crosses into this brand's ads.

## Workflow

1. **Budget first (`reference/budget-and-structure.md`).** Before proposing any
   structure, ask the user for the spending cap (total and per month), the
   window, the expected cost per result (or mark it an assumption) and the
   real, sourced angles available. Compute how many ad sets the budget
   supports and tell the user the result and the reason, with the alternatives
   that would change it (more budget, longer window, cheaper event). The user
   decides; never assume "3 angles".
2. **Frame (`ads.md`).** With the user, fill `reference/ads-template.md`: goal and
   single conversion event, ad account, the budget decision from step 1, offer
   and landing/destination, economics (ticket, margin, close rate, LTV) with
   assumptions marked, audiences, and the decision rules. Compute break-even
   and target numbers (`reference/metrics-and-thresholds.md`). Show and get OK.
3. **Readiness check.** Account active and in the right currency; Page linked;
   destination works (WhatsApp link/booking opens on a phone); tracking in
   place for the chosen event, or the plan uses an objective that doesn't need it
   (see "Objective selection"); payment method and spending limit set. List gaps
   as tasks; do not launch with gaps that make the result unreadable.
4. **Pick the campaign type** (`reference/campaign-types.md`): test, scale or
   remarketing. Default for a first campaign is a test. Don't scale without a
   finished test; don't remarket without enough audience.
5. **Angles and creatives.** Angles come from `content-ideas` (sourced), not
   invention; copy in the brand voice through the anti-slop gate
   (`social-brand-kit`); visuals via `social-visuals` with its mandatory editor
   review. One variable per ad: change the angle, keep format and offer.
6. **Build the plan.** Write the structure (campaign → ad sets → ads), budgets,
   dates, tracking tags (UTM), and the decision table: metric, minimum data,
   thresholds, action. Save into `ads.md` (or a dated campaign section).
   Show it; wait for approval.
7. **Create (MCP or Ads Manager).** Account check, then create everything
   **paused** with the dry-run/approval gate. Re-read what was created and
   compare with the plan field by field (country, budget, optimization goal,
   placements, audience, start/end dates, tracking). Fix differences before
   activating. Hidden defaults are the usual culprit (`reference/ui-and-delivery-gotchas.md`).
8. **Launch** only on explicit user OK. Record ids and the start date in `ads.md`.
9. **Review on schedule, not on impulse.** Do not judge before the minimum data
   in the plan is met. At the review: pull the numbers, check delivery
   distribution first (did every ad set/ad get its share?), then the decision
   table. Outcome is one of: continue, stop, scale, retest, **inconclusive**.
   Cross-check with your own analytics (UTM) and the step after the click.
10. **Close the loop.** Append results (what ran, spend, numbers, decision, why)
   to the kit's `results.md`; feed learnings to `content-ideas`. Update `ads.md`
   assumptions with real numbers.

## Objective selection

Choose the objective by what the account can actually optimize and measure:

- Little or no conversion history and a messaging CTA → conversations
  (Click-to-WhatsApp/Messenger). Commonly said not to need a pixel (not
  re-verified against Meta's docs; confirm in Ads Manager when building); judge
  conversation quality by hand early.
- Booked call / form → needs the event tracked (pixel or Conversions API); with
  few events, optimization is weak. Start upstream (conversations or landing
  views) and move down as events accumulate.
- Traffic/clicks → cheap, fast data, but the easiest to fool (accidental taps,
  low-intent visits). Use only as a diagnostic, not as the success metric.

## Gotchas

- Several ads in one ad set are **not** delivered evenly; the system favors an
  early leader and can starve the rest. To compare angles, use one ad set per
  angle with equal budgets, or test sequentially.
- A very high link CTR on mobile/Reels can be accidental taps. Verify with
  own analytics and what happens after the click.
- Small events volume = no useful remarketing audience and weak optimization.
- The interface applies defaults silently (country, budget, placements, audience
  expansion) and "apply recommendation" buttons can undo targeting. Verify every
  field after creation.

## Example

User: "Quiero probar anuncios de Meta para mi servicio con ~$3,000 MXN"

→ account check; locate kit and `ads.md` (missing → build with the user)
→ frame: objective = WhatsApp conversations, budget cap, economics (assumptions
  marked), break-even cost per conversation, decision rules
→ test design: N angles from `content-ideas` (N limited by what the budget
  supports at equal budgets), one ad set per angle, creatives via `social-visuals`
→ show plan + decision table → approval → create paused (dry run each step)
→ verify created fields against the plan → launch on OK
→ review at the preset date: delivery check, then decision table; may say "inconclusive"
