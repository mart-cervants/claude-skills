"""Diagnose why a campaign has no / low metrics. Read-only, no spend.

Runs the decision tree in reference/diagnostics.md automatically:
account currency + billing, campaign serving/primary status, ad-group status,
ad approval, keyword eligibility, targeting, recent impressions, and real
search demand (Keyword Planner) for the campaign's keywords. Prints per-check
findings and a heuristic verdict.

Usage:
    python diagnose_campaign.py --campaign-id 24156377666
"""

from __future__ import annotations

import argparse
import sys

import _client


def _rows(svc, cid, query):
    out = []
    for batch in svc.search_stream(customer_id=cid, query=query):
        out.extend(batch.results)
    return out


def _flag(label, ok, detail=""):
    mark = "PASS" if ok is True else ("WARN" if ok is None else "FAIL")
    print(f"[{mark}] {label}" + (f" — {detail}" if detail else ""))


def main() -> int:
    ap = argparse.ArgumentParser(description="Diagnose a campaign's serving/metrics.")
    ap.add_argument("--campaign-id", required=True)
    args = ap.parse_args()
    cin = args.campaign_id

    client = _client.get_client()
    cid = _client.get_customer_id(client)
    svc = client.get_service("GoogleAdsService")

    from google.ads.googleads.errors import GoogleAdsException
    from _common import handle_google_ads_exception

    findings = {"blockers": [], "notes": []}
    currency = "?"

    try:
        # 0. Account + currency
        for r in _rows(svc, cid, "SELECT customer.currency_code, customer.time_zone, "
                       "customer.status, customer.test_account FROM customer"):
            currency = r.customer.currency_code
            _flag("Account", r.customer.status.name == "ENABLED",
                  f"status={r.customer.status.name}, "
                  f"currency={currency}, tz={r.customer.time_zone}, "
                  f"test_account={r.customer.test_account}")
            if r.customer.status.name != "ENABLED":
                findings["blockers"].append("account not ENABLED")

        # 1. Billing
        billing = _rows(svc, cid, "SELECT billing_setup.status FROM billing_setup")
        approved = any(b.billing_setup.status.name == "APPROVED" for b in billing)
        _flag("Billing setup", approved if billing else False,
              ", ".join(b.billing_setup.status.name for b in billing) or "none found")
        if not approved:
            findings["blockers"].append("no APPROVED billing setup")

        # 2. Campaign
        camp = _rows(svc, cid, "SELECT campaign.name, campaign.status, "
                     "campaign.serving_status, campaign.primary_status, "
                     "campaign.primary_status_reasons, campaign.bidding_strategy_type, "
                     "campaign_budget.amount_micros "
                     f"FROM campaign WHERE campaign.id = {cin}")
        if not camp:
            print(f"Campaign {cin} not found.", file=sys.stderr)
            return 2
        c = camp[0].campaign
        budget = camp[0].campaign_budget.amount_micros / 1_000_000
        reasons = ", ".join(x.name for x in c.primary_status_reasons)
        serving_ok = c.status.name == "ENABLED" and c.serving_status.name == "SERVING"
        _flag("Campaign serving", serving_ok if serving_ok else None,
              f"status={c.status.name}, serving={c.serving_status.name}, "
              f"primary={c.primary_status.name} ({reasons}), "
              f"bidding={c.bidding_strategy_type.name}, budget={budget} {currency}/day")
        if c.status.name != "ENABLED":
            findings["blockers"].append(f"campaign status {c.status.name}")
        if "LEARNING" in c.primary_status.name or "LEARNING" in reasons:
            findings["notes"].append("bid strategy still LEARNING (normal when new)")

        # 3. Ad groups
        ags = _rows(svc, cid, "SELECT ad_group.status, ad_group.primary_status "
                    f"FROM ad_group WHERE campaign.id = {cin}")
        bad_ag = [a for a in ags if a.ad_group.status.name != "ENABLED"]
        _flag("Ad groups", not bad_ag if ags else False,
              f"{len(ags)} ad group(s), "
              + ", ".join(f"{a.ad_group.primary_status.name}" for a in ags))

        # 4. Ads
        ads = _rows(svc, cid, "SELECT ad_group_ad.status, "
                    "ad_group_ad.policy_summary.approval_status, "
                    "ad_group_ad.policy_summary.review_status, ad_group_ad.ad_strength "
                    f"FROM ad_group_ad WHERE campaign.id = {cin}")
        disapproved = [a for a in ads
                       if a.ad_group_ad.policy_summary.approval_status.name == "DISAPPROVED"]
        under_review = [a for a in ads
                        if a.ad_group_ad.policy_summary.review_status.name in
                        ("UNDER_REVIEW", "REVIEW_IN_PROGRESS")]
        _flag("Ads approved", not disapproved if ads else False,
              f"{len(ads)} ad(s), "
              + ", ".join(f"{a.ad_group_ad.policy_summary.approval_status.name}"
                          f"/{a.ad_group_ad.ad_strength.name}" for a in ads))
        if disapproved:
            findings["blockers"].append(f"{len(disapproved)} ad(s) DISAPPROVED")
        if under_review:
            findings["notes"].append(f"{len(under_review)} ad(s) still under review")

        # 5. Keywords
        kws = _rows(svc, cid, "SELECT ad_group_criterion.keyword.text, "
                    "ad_group_criterion.status "
                    f"FROM ad_group_criterion WHERE campaign.id = {cin} "
                    "AND ad_group_criterion.type = 'KEYWORD' "
                    "AND ad_group_criterion.negative = false")
        kw_texts = [k.ad_group_criterion.keyword.text for k in kws]
        _flag("Keywords", bool(kws), f"{len(kws)} positive keyword(s)")
        if not kws:
            findings["blockers"].append("no positive keywords")

        # 6. Targeting (geo + language + network)
        crit = _rows(svc, cid, "SELECT campaign_criterion.type, "
                     "campaign_criterion.negative, "
                     "campaign_criterion.location.geo_target_constant, "
                     "campaign_criterion.language.language_constant "
                     f"FROM campaign_criterion WHERE campaign.id = {cin}")
        geos = [x.campaign_criterion.location.geo_target_constant.split("/")[-1]
                for x in crit if x.campaign_criterion.type_.name == "LOCATION"
                and not x.campaign_criterion.negative]
        langs = [x.campaign_criterion.language.language_constant.split("/")[-1]
                 for x in crit if x.campaign_criterion.type_.name == "LANGUAGE"]
        net = _rows(svc, cid, "SELECT campaign.network_settings.target_google_search, "
                    "campaign.network_settings.target_search_network, "
                    "campaign.network_settings.target_content_network "
                    f"FROM campaign WHERE campaign.id = {cin}")[0].campaign.network_settings
        _flag("Targeting", bool(geos) or None,
              f"geo={geos or 'ALL'}, lang={langs or 'ALL'}, "
              f"google_search={net.target_google_search}")

        # 7. Recent impressions
        m = _rows(svc, cid, "SELECT metrics.impressions, metrics.clicks, "
                  "metrics.cost_micros FROM campaign "
                  f"WHERE campaign.id = {cin} AND segments.date DURING LAST_30_DAYS")
        impr = sum(int(x.metrics.impressions) for x in m)
        clicks = sum(int(x.metrics.clicks) for x in m)
        _flag("Impressions (30d)", impr > 0 if impr else None,
              f"impressions={impr}, clicks={clicks}")

        # 8. Demand (only worth checking if config looks healthy but impressions ~0)
        demand_total = None
        if kw_texts and impr == 0 and not findings["blockers"]:
            try:
                idea_svc = client.get_service("KeywordPlanIdeaService")
                req = client.get_type("GenerateKeywordHistoricalMetricsRequest")
                req.customer_id = cid
                req.keywords.extend(kw_texts[:50])
                if geos:
                    req.geo_target_constants.extend(f"geoTargetConstants/{g}" for g in geos)
                if langs:
                    req.language = f"languageConstants/{langs[0]}"
                req.keyword_plan_network = client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH
                resp = idea_svc.generate_keyword_historical_metrics(request=req)
                demand_total = sum(int(getattr(r.keyword_metrics, "avg_monthly_searches", 0) or 0)
                                   for r in resp.results)
                _flag("Search demand", demand_total > 500 if demand_total else None,
                      f"~{demand_total} total avg monthly searches across "
                      f"{len(kw_texts)} keyword(s) in geo {geos or 'ALL'}")
            except GoogleAdsException:
                pass

    except GoogleAdsException as ex:
        handle_google_ads_exception(ex)
        return 1

    # Verdict
    print("\n" + "=" * 70)
    print("VERDICT")
    print("=" * 70)
    if findings["blockers"]:
        print("CONFIG BLOCKERS (fix these — they stop serving):")
        for b in findings["blockers"]:
            print(f"  - {b}")
    elif impr == 0 and demand_total is not None and demand_total < 500:
        print("DEMAND-LIMITED: setup is healthy, but the keywords have very little")
        print(f"  search volume (~{demand_total}/mo in geo {geos or 'ALL'}). Expected to")
        print("  see ~0 impressions. Broaden to higher-volume, on-product terms")
        print("  (see reference/keyword-research-workflow.md). Raising budget won't help.")
    elif impr == 0 and findings["notes"]:
        print("LIKELY RAMPING: no blockers found. " + "; ".join(findings["notes"]))
        print("  Give it a few days; ensure the keywords have real demand.")
    else:
        print("No hard blockers found. See per-check notes above.")
    for n in findings["notes"]:
        print(f"  note: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
