# Keyword research workflow (MANDATORY before proposing/adding keywords)

Do NOT propose or add keywords from raw search volume alone. Volume is only one
input — relevance to the actual product and to the live ad assets determines
whether a keyword earns clicks that convert. Follow these steps in order.

## 1. Understand the product FIRST (and confirm with the user)

Before any keyword work, establish and **confirm with the user**:
- What the product does, and **how** (e.g. AI-based extraction vs OCR — these
  attract different searchers).
- Its **outputs/format** (e.g. exports to Excel) — output features are valid
  keyword themes only if the ad/landing page actually claim them.
- Target audience (SMB vs enterprise; end-user vs developer).
- What the product is **NOT** (e.g. no public API, not a template gallery) — this
  drives exclusions.

Sources: the landing page (final URL), the user's description, project docs.
When unsure, ASK rather than assume. This session's lesson: excluding "OCR" and
"API" terms and confirming Excel output all came from product facts, not volume.

## 2. Pull the live campaign's assets

For the target ad group, fetch the current ad copy and landing page:
```
report.py --query "SELECT ad_group_ad.ad.responsive_search_ad.headlines,
  ad_group_ad.ad.responsive_search_ad.descriptions, ad_group_ad.ad.final_urls
  FROM ad_group_ad WHERE campaign.id = <ID>"
```
(RSA repeated assets print cleanly via a short inline script if needed.)

## 3. Alignment check — every proposed keyword must be supported

For each candidate keyword, verify it is reflected in BOTH:
- the **ad copy** (a headline/description speaks to that intent), and
- the **landing page**.

If a promising cluster is NOT supported (e.g. "invoice to excel" with no Excel
headline), you have two choices — never add it blind:
- **Exclude** the cluster, or
- **Add supporting copy first** (e.g. `update_ad.py --add-headline "Invoice PDF
  to Excel"`), truthfully, THEN add the keywords.

## 4. Intent filter → some mismatches become negatives

Separate commercial intent from noise:
- Freebie intent ("template", "free", "sample") → add as **negatives**.
- Wrong audience ("api" when there's no API; developer terms) → exclude.
- Tech mismatch ("ocr" when the product is AI) → exclude.
- Beware output words that are also relevant (e.g. do NOT broad-negate "excel"
  if the product exports Excel).

## 5. Match-type strategy

- Low-volume niche → a few **BROAD** heads for reach + **PHRASE** long-tail.
- BROAD requires solid negatives + ongoing search-term review.
- Small budget → prefer PHRASE; broad can spend fast on loose matches.

## 6. Dry-run → show plan → user confirms → apply

Always `add_keywords.py` / `update_ad.py` WITHOUT `--confirm` first, show the
user the validated plan, get explicit approval, then re-run with `--confirm`.

## 7. Follow up

After a few days, `report.py --preset search_terms` to mine real queries and add
new negatives; `report.py --preset keyword_performance` to prune non-performers.
