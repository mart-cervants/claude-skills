# Diagnostics: "why zero / low metrics?"

When a campaign shows no (or very few) impressions, work this decision tree
top-down. Each step has a read-only GAQL query. `diagnose_campaign.py` automates
the whole tree — use it first, then drill in with these queries as needed.

Golden rule learned this session: **most "no metrics" cases are NOT broken setup
— they're demand or relevance.** Rule out config quickly, then check demand.

## 0. Account currency (always do this first)
Interpret every amount in the account's currency, not USD.
```
SELECT customer.currency_code, customer.time_zone, customer.status,
       customer.test_account FROM customer
```
This account is MXN — a "131" bid is 131 pesos (~$7), not $131.

## 1. Is the account able to serve? (billing)
```
SELECT billing_setup.id, billing_setup.status FROM billing_setup
```
No `APPROVED` billing setup → nothing serves. Common on brand-new accounts.

## 2. Campaign serving status
```
SELECT campaign.status, campaign.serving_status, campaign.primary_status,
       campaign.primary_status_reasons, campaign.bidding_strategy_type,
       campaign_budget.amount_micros FROM campaign WHERE campaign.id = <ID>
```
- `status` must be ENABLED, `serving_status` SERVING.
- `primary_status` / `primary_status_reasons` usually name the exact blocker
  (e.g. CAMPAIGN_PAUSED, BUDGET, BIDDING_STRATEGY_LEARNING, NO_ELIGIBLE_ADS).
- `LEARNING` / `BIDDING_STRATEGY_LEARNING` is normal for a new campaign.

## 3. Ad group status
```
SELECT ad_group.status, ad_group.primary_status, ad_group.primary_status_reasons
FROM ad_group WHERE campaign.id = <ID>
```
Want ENABLED + ELIGIBLE.

## 4. Ads — approved and eligible?
```
SELECT ad_group_ad.status, ad_group_ad.primary_status,
       ad_group_ad.policy_summary.approval_status,
       ad_group_ad.policy_summary.review_status, ad_group_ad.ad_strength
FROM ad_group_ad WHERE campaign.id = <ID>
```
Watch for UNDER_REVIEW (common first days) or DISAPPROVED (policy) → no serving.

## 5. Keywords — eligible and approved?
```
SELECT ad_group_criterion.keyword.text, ad_group_criterion.status,
       ad_group_criterion.system_serving_status,
       ad_group_criterion.approval_status
FROM ad_group_criterion
WHERE campaign.id = <ID> AND ad_group_criterion.type = 'KEYWORD'
```

## 6. Targeting — not too narrow / mismatched?
```
SELECT campaign_criterion.type, campaign_criterion.status,
       campaign_criterion.negative,
       campaign_criterion.location.geo_target_constant,
       campaign_criterion.language.language_constant
FROM campaign_criterion WHERE campaign.id = <ID>
```
Also network:
```
SELECT campaign.network_settings.target_google_search,
       campaign.network_settings.target_search_network,
       campaign.network_settings.target_content_network
FROM campaign WHERE campaign.id = <ID>
```
Classic trap: geo + language don't match the keywords' language/market.

## 7. Is there any impression at all?
```
SELECT metrics.impressions, metrics.clicks, metrics.cost_micros,
       metrics.search_impression_share
FROM campaign WHERE campaign.id = <ID> AND segments.date DURING LAST_7_DAYS
```

## 8. Is there real search DEMAND? (the usual culprit)
If everything above is healthy but impressions are ~0, check whether the
keywords have meaningful volume in the targeted geo:
```
keyword_ideas.py --historical --keyword "<kw1>" --keyword "<kw2>" ... --geo <geo>
```
Sum the avg monthly searches. This session: 7 keywords summed to ~170/month
across the entire US → ~0 impressions was expected, not a bug.

## Verdict patterns
- Billing not approved / campaign paused / ads disapproved → **fix config**.
- All eligible, `LEARNING`, only a few days old → **wait + ensure demand**.
- All eligible but total demand tiny → **demand-limited**: broaden to higher-
  volume, on-product terms (run keyword-research-workflow.md), or accept low
  volume. Do NOT just raise budget — budget isn't the constraint.
