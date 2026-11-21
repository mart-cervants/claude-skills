# Budget first, then structure

The budget decides how many angles (ad sets) a test can support — not the other
way round. **Ask for the budget before proposing any structure**, then run the
table below and explain the result to the user in plain words.

## Ask (in this order)

1. Maximum the user is willing to spend in total, and per month. This is a cap,
   not a target.
2. Test window they can wait (default: 7 days, whole weeks).
3. What a conversion (the single result) is worth: expected cost per result, if
   they have one. If not, the best available estimate, labeled **assumption**:
   from the account's own history, a peer benchmark the MCP exposes, or a first
   cheap calibration round. Never invent it silently.
4. How many different angles they actually have, with a source each
   (`content-ideas`). Fewer real angles than the budget allows → run fewer.

## What Meta says (help center, checked 2026-11-20)

- An ad set usually exits the learning phase after **about 50 results in the week
  after its last significant edit**; before that, performance is less stable and
  CPA usually higher ("About the learning phase"). Status "Learning limited" means
  it isn't getting enough results.
- "**Avoid high ad volumes.** When you create many ads and ad sets, the delivery
  system learns less about each." Combining similar ad sets combines learnings.
- "**Use realistic budgets.** If you set a small or inflated budget, the delivery
  system has an inaccurate indicator…" and avoid frequent budget changes.
- Minimum budgets vary by country, objective and optimization; Ads Manager shows
  an alert or recommendation. If the budget is a problem, "you can try optimizing
  for an event that may be easier and cheaper to achieve" ("Best practices for
  minimum budgets"). With a cost-per-result goal strategy, daily budget should
  be at least 5× the goal.

These are the sources for the table; anything not in them below is this skill's
reasoning and is marked.

## Compute

```
weekly_test_budget      = total_test_budget ÷ weeks_in_window   (cap-aware)
budget_to_exit_learning = 50 × expected_cost_per_result          (per ad set, per week)
ad_sets_that_fit        = floor(weekly_test_budget ÷ budget_to_exit_learning)
```

Also require each ad set's daily budget ≥ the platform minimum shown in the
account (read it from the MCP/Ads Manager).

## Decision table

| `ad_sets_that_fit` | What to propose | How to read results |
|---|---|---|
| ≥ 3 and ≥ 3 sourced angles | One ad set per angle (up to 3), equal budgets | Cost per result is judgeable if each reaches the minimum data |
| 2 | Two angles, one ad set each | Same, with a duel instead of a ranking |
| 1 | One ad set. Compare angles **sequentially** (one after another, same weekdays) or run the best angle alone; say that sequence effects mix in | Cost per result for that ad set; angle comparison is weak |
| 0 (budget can't reach ~50 results even for one ad set) | **Learning-limited regime.** Offer, in this order: (a) raise the budget or lengthen the window, (b) optimize for an easier, cheaper event upstream (Meta's own suggestion), (c) run at most 2 angles at the largest budget each can get and call the result **directional** | Never state a CAC or a winner with confidence. Rank on link CTR, cost per result relative between ad sets, and the quality of the actual conversations; say "inconclusive" when gaps are within noise |

Rules that always apply:
- Fewer ad sets with more budget each beats more ad sets with less (Meta: avoid
  high ad volumes). Never split money below the minimum a conclusion needs.
- Never put several angles in one ad set to "let Meta pick" when the goal is to
  compare angles; delivery piles onto an early leader.
- Keep total spend inside the user's cap; leave a reserve (a third or so is a
  sensible default, a skill rule of thumb) for a second round on the best result.
- State the choice and the reason to the user before building: "With X per
  month and an expected Y per result, N ad set(s) fit, so …". Offer the
  alternatives that change the answer (more budget, longer window, cheaper
  event). The user decides.

## Calibration round (when the cost per result is unknown)

If there's no estimate at all, a short first round exists to measure it, not to
rank angles: one ad set, one angle, the cheapest defensible budget for a few
days, then recompute `ad_sets_that_fit` with the real cost. Say so explicitly.
