# Campaign spec (JSON) for `create_campaign.py`

`create_campaign.py --spec <file.json>` builds a **Search** campaign — budget,
campaign, ad groups, Responsive Search Ads, and keywords — in a single atomic
mutate. Everything succeeds together or nothing is created.

## Schema

```jsonc
{
  "budget": {
    "name": "string, required — unique budget name",
    "amount": 20.0            // required, daily amount in the ACCOUNT'S currency
  },
  "campaign": {
    "name": "string, required",
    "status": "PAUSED",       // optional; default PAUSED (safe). ENABLED to go live.
    "bidding_strategy": "MANUAL_CPC",  // optional; MANUAL_CPC (default) | MAXIMIZE_CONVERSIONS
    "enhanced_cpc": false      // optional; only used with MANUAL_CPC
  },
  "ad_groups": [               // optional, but usually you want at least one
    {
      "name": "string, required",
      "cpc_bid": 1.00,         // optional, max CPC in account currency (MANUAL_CPC)
      "ads": [
        {
          "headlines": ["3-15 headlines, <=30 chars each"],
          "descriptions": ["2-4 descriptions, <=90 chars each"],
          "final_urls": ["https://example.com/landing"]
        }
      ],
      "keywords": [
        { "text": "running shoes", "match_type": "PHRASE" },   // EXACT | PHRASE | BROAD
        { "text": "free", "match_type": "BROAD", "negative": true }
      ]
    }
  ]
}
```

## Notes & guardrails

- **Currency & micros:** amounts are entered in normal units (e.g. `20.0`); the
  script converts to micros (`× 1,000,000`) internally.
- **Status defaults to `PAUSED`** so a newly created campaign never starts
  spending before you review it. Set `"status": "ENABLED"` only when ready.
- **RSA minimums:** Google requires at least 3 headlines and 2 descriptions for
  a Responsive Search Ad. Fewer will fail validation (caught by the dry run).
- **Always dry-run first.** Run without `--confirm`, read the printed plan, then
  re-run with `--confirm`.

## Minimal example

```json
{
  "budget": { "name": "Shoes - Daily", "amount": 15 },
  "campaign": { "name": "Shoes - Search", "status": "PAUSED" },
  "ad_groups": [
    {
      "name": "Running Shoes",
      "cpc_bid": 1.20,
      "ads": [
        {
          "headlines": ["Buy Running Shoes", "Free Shipping", "Shop the Sale"],
          "descriptions": ["Top brands, low prices.", "Fast, free delivery."],
          "final_urls": ["https://example.com/running"]
        }
      ],
      "keywords": [
        { "text": "running shoes", "match_type": "PHRASE" },
        { "text": "buy running shoes", "match_type": "EXACT" }
      ]
    }
  ]
}
```
