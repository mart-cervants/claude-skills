# Review Metrics — Reference (benchmark table)

| Metric | Healthy range | Below/above range means | Recommended fix |
|---|---|---|---|
| Open rate | 40-60%+ | Low → subject line isn't earning opens, or sender name/domain reputation is weak | Test new subject lines via `add_step_variant`; check `saleshandy-account-health` if consistently low across all sequences on that account |
| Reply rate | 1-3%+ for cold B2B | Low with healthy open rate → messaging/offer isn't landing, not a visibility problem | Rework the CTA/offer in the body, not the subject line; consider tightening the ICP via `saleshandy-find-leads` if reply rate is low across many sequences |
| Bounce rate | < 2% | High → list quality problem, not a copy problem | Stop sending immediately; re-verify the list via `saleshandy-verify-emails`; do not "fix" this by editing sequence content |
| Unsubscribe rate | < 0.5% | High → frequency too aggressive, or targeting is off (wrong audience receiving relevant-sounding but unwanted mail) | Increase gap between steps; re-check ICP criteria |

## Reading multiple metrics together

- High opens + low replies = targeting/offer problem, not deliverability.
- Low opens + normal replies-per-open = deliverability/subject line
  problem, not offer problem.
- Any bounce rate above 2% invalidates the other numbers — fix that first,
  because a damaged account's stats for every OTHER metric will keep
  degrading until it's addressed.
