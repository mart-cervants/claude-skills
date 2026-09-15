# GAQL cookbook

Reference queries for `report.py`. The named presets below are built into the
script (`report.py --preset <name>`); the rest are copy-paste starters for
`report.py --query "<gaql>"`.

GAQL reference: https://developers.google.com/google-ads/api/docs/query/overview
Field reference: https://developers.google.com/google-ads/api/fields/v25/overview

## Conventions
- `metrics.cost_micros` / `average_cpc` are in **micros** (÷ 1,000,000 for
  currency). `report.py` converts these automatically for display.
- Date ranges: `DURING LAST_7_DAYS | LAST_30_DAYS | THIS_MONTH`, or explicit
  `segments.date BETWEEN '2026-01-01' AND '2026-01-31'`.

## Built-in presets

### `campaign_spend` — spend & conversions per campaign (last 30 days)
```sql
SELECT campaign.id, campaign.name, campaign.status,
       metrics.cost_micros, metrics.impressions, metrics.clicks,
       metrics.conversions, metrics.conversions_value
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
ORDER BY metrics.cost_micros DESC
```

### `ad_group_performance`
```sql
SELECT campaign.name, ad_group.id, ad_group.name, ad_group.status,
       metrics.cost_micros, metrics.clicks, metrics.conversions
FROM ad_group
WHERE segments.date DURING LAST_30_DAYS
ORDER BY metrics.cost_micros DESC
```

### `keyword_performance`
```sql
SELECT campaign.name, ad_group.name,
       ad_group_criterion.keyword.text,
       ad_group_criterion.keyword.match_type,
       metrics.cost_micros, metrics.clicks, metrics.conversions,
       metrics.average_cpc
FROM keyword_view
WHERE segments.date DURING LAST_30_DAYS
ORDER BY metrics.cost_micros DESC
```

### `search_terms` — actual queries that triggered ads
```sql
SELECT search_term_view.search_term, campaign.name,
       metrics.clicks, metrics.cost_micros, metrics.conversions
FROM search_term_view
WHERE segments.date DURING LAST_30_DAYS
ORDER BY metrics.cost_micros DESC
```

### `budget_utilization`
```sql
SELECT campaign.name, campaign_budget.amount_micros, metrics.cost_micros
FROM campaign
WHERE segments.date DURING LAST_7_DAYS
ORDER BY metrics.cost_micros DESC
```

## Handy ad-hoc queries

### List all campaigns with their budget resource id (needed for update_entity.py)
```sql
SELECT campaign.id, campaign.name, campaign.status,
       campaign_budget.id, campaign_budget.amount_micros
FROM campaign
```

### Find ad group + criterion ids for a keyword (needed to pause a keyword)
```sql
SELECT ad_group.id, ad_group_criterion.criterion_id,
       ad_group_criterion.keyword.text, ad_group_criterion.status
FROM ad_group_criterion
WHERE ad_group_criterion.type = 'KEYWORD'
```

### Daily trend for one campaign
```sql
SELECT segments.date, metrics.cost_micros, metrics.conversions
FROM campaign
WHERE campaign.id = CAMPAIGN_ID AND segments.date DURING LAST_30_DAYS
ORDER BY segments.date
```
