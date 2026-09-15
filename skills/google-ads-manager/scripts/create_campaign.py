"""Create a Search campaign atomically from a declarative JSON spec.

Builds the budget, campaign, ad groups, ads, and keywords as a SINGLE mutate
using temporary (negative) resource names, so the whole thing succeeds or fails
together — no orphaned entities. Routes through _common.apply_mutate, so it is
validate_only by default and only applies with --confirm.

Spec schema is documented in reference/campaign-spec.md.

Usage:
    python create_campaign.py --spec campaign.json              # dry run
    python create_campaign.py --spec campaign.json --confirm    # apply
"""

from __future__ import annotations

import argparse
import json
import sys

import _client
from _common import apply_mutate


# Temporary resource IDs (negative) — replaced with real IDs within the request.
BUDGET_TMP = -1
CAMPAIGN_TMP = -2


def _res(client, customer_id, kind, tmp_id):
    service = client.get_service("GoogleAdsService")
    path_fn = {
        "campaign_budget": service.campaign_budget_path,
        "campaign": service.campaign_path,
        "ad_group": service.ad_group_path,
    }[kind]
    return path_fn(customer_id, tmp_id)


def build_operations(client, customer_id: str, spec: dict) -> tuple[list, list[str]]:
    ops: list = []
    plan: list[str] = []
    enums = client.enums

    # --- Budget ---
    budget = spec["budget"]
    op = client.get_type("MutateOperation")
    b = op.campaign_budget_operation.create
    b.resource_name = _res(client, customer_id, "campaign_budget", BUDGET_TMP)
    b.name = budget["name"]
    b.amount_micros = int(round(float(budget["amount"]) * 1_000_000))
    b.delivery_method = enums.BudgetDeliveryMethodEnum.STANDARD
    b.explicitly_shared = False
    ops.append(op)
    plan.append(f"Budget '{budget['name']}': {budget['amount']}/day")

    # --- Campaign ---
    camp = spec["campaign"]
    op = client.get_type("MutateOperation")
    c = op.campaign_operation.create
    c.resource_name = _res(client, customer_id, "campaign", CAMPAIGN_TMP)
    c.name = camp["name"]
    c.campaign_budget = _res(client, customer_id, "campaign_budget", BUDGET_TMP)
    c.advertising_channel_type = enums.AdvertisingChannelTypeEnum.SEARCH
    # Start paused by default unless the spec explicitly enables it.
    status = camp.get("status", "PAUSED").upper()
    c.status = getattr(enums.CampaignStatusEnum, status)
    # Required in v25: declare EU political advertising status. A data-extraction
    # product is not political advertising; override in the spec if that changes.
    c.contains_eu_political_advertising = (
        enums.EuPoliticalAdvertisingStatusEnum
        .DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING
    )
    # Bidding: default to Manual CPC unless a strategy is given.
    strategy = camp.get("bidding_strategy", "MANUAL_CPC").upper()
    if strategy == "MAXIMIZE_CONVERSIONS":
        c.maximize_conversions.CopyFrom(client.get_type("MaximizeConversions"))
    else:
        c.manual_cpc.enhanced_cpc_enabled = camp.get("enhanced_cpc", False)
    ops.append(op)
    plan.append(f"Campaign '{camp['name']}': SEARCH, status={status}, bidding={strategy}")

    # --- Ad groups + ads + keywords ---
    ag_tmp = CAMPAIGN_TMP  # walk further negative for each child
    for gi, ag in enumerate(spec.get("ad_groups", []), start=1):
        ag_tmp -= 1
        ag_id = ag_tmp
        op = client.get_type("MutateOperation")
        g = op.ad_group_operation.create
        g.resource_name = _res(client, customer_id, "ad_group", ag_id)
        g.name = ag["name"]
        g.campaign = _res(client, customer_id, "campaign", CAMPAIGN_TMP)
        g.type_ = enums.AdGroupTypeEnum.SEARCH_STANDARD
        g.status = enums.AdGroupStatusEnum.ENABLED
        if ag.get("cpc_bid") is not None:
            g.cpc_bid_micros = int(round(float(ag["cpc_bid"]) * 1_000_000))
        ops.append(op)
        plan.append(f"  Ad group '{ag['name']}'"
                    + (f" @ {ag['cpc_bid']} CPC" if ag.get("cpc_bid") else ""))

        # Responsive Search Ad(s)
        for ad in ag.get("ads", []):
            op = client.get_type("MutateOperation")
            a = op.ad_group_ad_operation.create
            a.ad_group = _res(client, customer_id, "ad_group", ag_id)
            a.status = enums.AdGroupAdStatusEnum.ENABLED
            rsa = a.ad.responsive_search_ad
            for h in ad["headlines"]:
                asset = client.get_type("AdTextAsset")
                asset.text = h
                rsa.headlines.append(asset)
            for d in ad["descriptions"]:
                asset = client.get_type("AdTextAsset")
                asset.text = d
                rsa.descriptions.append(asset)
            for url in ad.get("final_urls", []):
                a.ad.final_urls.append(url)
            ops.append(op)
            plan.append(f"    RSA: {len(ad['headlines'])} headlines, "
                        f"{len(ad['descriptions'])} descriptions")

        # Keywords
        for kw in ag.get("keywords", []):
            op = client.get_type("MutateOperation")
            k = op.ad_group_criterion_operation.create
            k.ad_group = _res(client, customer_id, "ad_group", ag_id)
            k.status = enums.AdGroupCriterionStatusEnum.ENABLED
            k.keyword.text = kw["text"]
            match = kw.get("match_type", "BROAD").upper()
            k.keyword.match_type = getattr(enums.KeywordMatchTypeEnum, match)
            k.negative = kw.get("negative", False)
            ops.append(op)
            neg = "NEGATIVE " if kw.get("negative") else ""
            plan.append(f"    {neg}keyword [{match}] '{kw['text']}'")

    return ops, plan


def main() -> int:
    ap = argparse.ArgumentParser(description="Create a Search campaign from a JSON spec.")
    ap.add_argument("--spec", required=True, help="path to the campaign JSON spec")
    ap.add_argument("--confirm", action="store_true",
                    help="apply the change (omit for a dry run)")
    args = ap.parse_args()

    with open(args.spec) as f:
        spec = json.load(f)

    client = _client.get_client()
    customer_id = _client.get_customer_id(client)
    ops, plan = build_operations(client, customer_id, spec)

    apply_mutate(client, customer_id, ops, confirm=args.confirm, plan_lines=plan)
    return 0


if __name__ == "__main__":
    sys.exit(main())
