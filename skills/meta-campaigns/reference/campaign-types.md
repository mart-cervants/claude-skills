# Campaign types

Three types, used in this order. Each needs the previous one to have produced
usable data. All numbers below are orientation; the project's `ads.md` sets the
real ones.

## 1. Test (lab)

**Purpose:** learn which angle (message) gets the cheapest *qualified* response.
Not to make money yet.

**Design**
- **Number of angles = what the budget supports** (`budget-and-structure.md`; ask the budget
  first). Three or more only when budget and sourced angles allow it; 2 angles is a
  duel, not a ranking, and 1 is a calibration. Angles must differ in *message* (pain,
  proof/result, objection, offer…), not in color or crop. Take them from sourced
  ideas (`content-ideas`).
- **One variable.** Same format, same offer, same destination, same audience; only
  the angle changes.
- **One ad set per angle, equal daily budgets.** Putting several ads in one ad
  set lets delivery pile onto an early leader (a known failure: one ad took
  nearly all impressions and the test produced nothing). Alternative for very
  small budgets: **sequential** — one angle at a time, same weekdays; weaker
  because time effects mix with angle effects, so say so in the results.
- **How many angles fit:** decided by the budget, see `budget-and-structure.md`
  (ask the budget first). A quick arithmetic bound is
  `floor(test_budget / (daily_budget_per_ad_set × days))`, but it is only the
  ceiling; the table there is what to follow.
  Meta enforces a minimum budget that varies by country, objective and
  optimization, and shows an alert/recommendation in Ads Manager; read it there,
  don't assume. With a *cost per result goal* strategy, Meta says the daily
  budget should be at least 5× the goal. If it
  yields fewer than 2, either raise the budget, shorten the window, or switch to
  sequential. Don't split money thinner than the minimum data in
  `metrics-and-thresholds.md` allows.
- **Fixed before spending:** window (e.g. 7–10 days, whole weeks to cover weekday
  effects), total cap, the single success metric, minimum data per ad set,
  and the decision table (see below). Write them in `ads.md`.
- **No edits mid-test** (creative, audience, budget) — edits restart learning and
  contaminate the comparison. Exceptions: broken link, policy rejection, wrong
  account/country/budget discovered after launch (fix and note it in the results).

**Decision table (fill in `ads.md`)**

| Situation at review | Action |
|---|---|
| Delivery very uneven (an ad set <~10% of spend share) | Result for that angle = untested, not lost. Re-run it alone or in the next test. |
| Below minimum data in every ad set | **Inconclusive.** Extend only if the cap allows; otherwise record and stop. |
| One angle clearly better on the success metric and beats the break-even target | Winner → scale type. |
| Best angle still worse than break-even cost | Don't scale. Change the offer/destination or angles, or stop. Don't conclude "ads don't work" from one test. |
| Cheap clicks/conversations but no downstream result | Problem is after the click (destination, follow-up, quality); fix that before more spend. |

## 2. Scale

**Purpose:** put more budget behind what a finished test proved, without breaking
what made it work.

**Preconditions:** a winner meeting the break-even/target numbers with at least
the minimum data; downstream capacity (can you answer more conversations?).

**Rules (write the numbers in `ads.md`)**
- Raise budget in **small steps**, spaced a few days. Meta's help center says a
  budget change "may or may not be significant, depending on the magnitude"
  (its example: $100→$101 unlikely to reset learning, $100→$1000 may) and gives
  **no percentage**. Pick a step size yourself (e.g. 20%, a common practitioner
  habit, not an official figure), write it in `ads.md`, and check the Delivery
  column for "Learning" after each step.
- After each step wait for the minimum data before the next judgment; one bad day
  is not a signal.
- **Stop-loss:** if cost per result exceeds the stop threshold for the agreed
  window, step back to the previous budget or pause. Define the threshold now.
- **Pause** ads whose frequency climbs with falling CTR (fatigue) and replace the
  creative with a new execution of the winning angle, not a new angle. Note:
  per Meta, **adding a new ad to an ad set** and **pausing an ad set for 7+ days**
  are significant edits that re-enter learning; prefer a new ad set for the
  refreshed creative when the ad set is stable.
- **Duplicate to scale horizontally** (new audience or placement) only as a new,
  separate test with its own budget cap.
- Never scale on a metric the account can't see downstream (e.g. clicks alone).

## 3. Remarketing

**Purpose:** reach people who interacted or clicked and didn't convert, with a
message for their stage. Conversion = the single event in `ads.md` (booked call
or WhatsApp message).

**Preconditions**
- Enough audience: custom audiences from page/ad engagement or site visitors need
  a minimum size to be usable, and optimization needs events; with only a few
  hundred visitors or a few conversions, remarketing is not useful yet. The
  often-quoted "~100+ people/events" floor is **not confirmed** in Meta's help
  center pages checked (2026-11-20): read the audience size shown in the
  interface and treat that as the authority. Check it before building the plan.
- Tracking works for the audiences used (pixel/Conversions API for site visitors;
  engagement audiences don't need it).

**Design**
- Segments by intent: engaged with ads/Page (warm) vs visited the destination
  (hot) vs started a conversation and went silent (follow-up, mostly manual).
  Exclude people who already converted.
- Short retention windows for hot (e.g. 7–14 days), longer for warm; message
  changes by stage: objection handling, proof, simple next step.
- Frequency cap by budget and audience size; watch frequency, as small audiences
  burn out fast.
- Smallest viable budget; separate ad set per segment; same decision-table
  discipline as the test.

**If the audience is too small:** say so, keep the money in the test/scale
campaign, and revisit when the numbers grow. A "retargeting" campaign for a few
dozen people is wasted spend and misleading data.
