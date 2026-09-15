"""Manage campaign-level targeting/exclusions: negative keywords and geo targets.

Routes through _common.apply_mutate (validate -> plan -> --confirm). This
covers the two most common asset/targeting jobs; the same pattern (build a
MutateOperation with a campaign_criterion_operation) extends to audiences,
proximity, ad-schedule, and language criteria — add cases as needed.

Usage (dry-run unless --confirm):
    # Add campaign-level negative keywords:
    python manage_assets.py --campaign-id 222 \
        --add-negative "free" --add-negative "cheap" --match BROAD --confirm

    # Add geo targets by location constant id (e.g. 2840 = United States):
    python manage_assets.py --campaign-id 222 --add-geo 2840 --confirm
"""

from __future__ import annotations

import argparse
import sys

import _client
from _common import apply_mutate


def build(client, customer_id, args) -> tuple[list, list[str]]:
    svc = client.get_service("GoogleAdsService")
    geo_svc = client.get_service("GeoTargetConstantService")
    enums = client.enums
    campaign_rn = svc.campaign_path(customer_id, args.campaign_id)
    ops: list = []
    plan: list[str] = []

    for text in args.add_negative or []:
        op = client.get_type("MutateOperation")
        c = op.campaign_criterion_operation.create
        c.campaign = campaign_rn
        c.negative = True
        c.keyword.text = text
        c.keyword.match_type = getattr(enums.KeywordMatchTypeEnum, args.match.upper())
        ops.append(op)
        plan.append(f"Campaign {args.campaign_id}: NEGATIVE keyword "
                    f"[{args.match.upper()}] '{text}'")

    for geo_id in args.add_geo or []:
        op = client.get_type("MutateOperation")
        c = op.campaign_criterion_operation.create
        c.campaign = campaign_rn
        c.location.geo_target_constant = geo_svc.geo_target_constant_path(geo_id)
        ops.append(op)
        plan.append(f"Campaign {args.campaign_id}: add geo target {geo_id}")

    if not ops:
        print("Nothing to do. Provide --add-negative and/or --add-geo.",
              file=sys.stderr)
        sys.exit(2)
    return ops, plan


def main() -> int:
    ap = argparse.ArgumentParser(description="Manage campaign negatives & geo targeting.")
    ap.add_argument("--campaign-id", required=True)
    ap.add_argument("--add-negative", action="append",
                    help="negative keyword text (repeatable)")
    ap.add_argument("--match", default="BROAD", help="EXACT | PHRASE | BROAD")
    ap.add_argument("--add-geo", action="append",
                    help="geo target constant id (repeatable)")
    ap.add_argument("--confirm", action="store_true")
    args = ap.parse_args()

    client = _client.get_client()
    customer_id = _client.get_customer_id(client)
    ops, plan = build(client, customer_id, args)
    apply_mutate(client, customer_id, ops, confirm=args.confirm, plan_lines=plan)
    return 0


if __name__ == "__main__":
    sys.exit(main())
