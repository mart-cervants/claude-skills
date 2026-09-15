# Keyword Planner (`keyword_ideas.py`)

Read-only keyword research via `KeywordPlanIdeaService`. No budget is consumed.
Use it to research demand and cost **before** writing a campaign spec, then feed
the winners into `reference/campaign-spec.md`.

## Two modes

| Mode | API call | Use when |
|------|----------|----------|
| Ideas (default) | `GenerateKeywordIdeas` | Discover NEW keywords from seed terms and/or a URL |
| `--historical` | `GenerateKeywordHistoricalMetrics` | Get metrics for a specific list you already have |

## Columns returned (per keyword)

- **avg_monthly_searches** — 12-month average; approximate/bucketed.
- **competition** — LOW / MEDIUM / HIGH (advertiser density).
- **competition_index** — 0–100 numeric version of competition.
- **top_of_page_bid_low / _high** — 20th / 80th percentile top-of-page bids in
  account currency (converted from micros). Your primary bidding signal.

Rows are sorted by `avg_monthly_searches` descending. Ideas mode is capped by
`--limit` (default 50).

## Required-ish inputs

- **`--geo`** — geo target constant id(s), repeatable. Strongly recommended;
  omit only for a global view. Common ids:
  | id | location |
  |----|----------|
  | 2840 | United States |
  | 2826 | United Kingdom |
  | 2124 | Canada |
  | 2036 | Australia |
  | 2484 | Mexico |
  | 2724 | Spain |
  Full list: https://developers.google.com/google-ads/api/data/geotargets
- **`--lang`** — language constant id, default `1000` (English). Others:
  Spanish `1003`, French `1002`, German `1001`, Portuguese `1014`.
  Reference: https://developers.google.com/google-ads/api/data/codes-formats#languages
- **`--partners`** — include Search partners (default: Google Search only).

## Examples

```bash
# Discover ideas from seeds, US, English:
python keyword_ideas.py --seed "running shoes" --seed "trail shoes" --geo 2840

# Ideas from a landing page:
python keyword_ideas.py --url https://example.com/shoes --geo 2840 --limit 100

# Historical metrics for a specific list, as CSV:
python keyword_ideas.py --historical --keyword "running shoes" \
    --keyword "buy sneakers" --geo 2840 --format csv

# From a file (one keyword per line):
python keyword_ideas.py --historical --keywords-file kws.txt --geo 2840
```

## Notes

- Metrics refresh ~monthly and change slowly — **cache** results (e.g. save the
  CSV) instead of re-querying repeatedly.
- Bid ranges are estimates, not guarantees. Very low-spend accounts may see
  coarser data.
- To discover geo/language ids programmatically, query `geo_target_constant`
  and `language_constant` via `report.py --query "..."`.
