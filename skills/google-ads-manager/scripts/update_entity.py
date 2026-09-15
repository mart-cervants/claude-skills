"""Update existing campaigns / ad groups: budget, bid, status.

Routes through _common.apply_mutate, so it validates and prints a plan first
and only applies with --confirm. Uses field masks so only the named field is
changed.

Usage (all dry-run unless --confirm):
    # Change a campaign's daily budget (by budget resource id):
    python update_entity.py --set-budget --budget-id 111 --amount 25 --confirm

    # Pause / enable a campaign:
    python update_entity.py --campaign-status --campaign-id 222 --status PAUSED

    # Change an ad group's max CPC:
    python update_entity.py --set-cpc --ad-group-id 333 --cpc 1.50 --confirm

    # Pause / enable a keyword criterion:
    python update_entity.py --criterion-status --ad-group-id 333 \
        --criterion-id 444 --status PAUSED
"""

from __future__ import annotations

import argparse
import sys

import _client
from _common import apply_mutate


def _apply_mask(client, sub_operation, update_obj):
    """Set sub_operation.update_mask to cover exactly the fields set on update_obj.

    This is Google's documented idiom: build the update object (resource_name +
    the field being changed), then derive the field mask from what's set.
    """
    from google.api_core import protobuf_helpers

    client.copy_from(
        sub_operation.update_mask,
        protobuf_helpers.field_mask(None, update_obj._pb),
    )


def build(client, customer_id, args) -> tuple[list, list[str]]:
    svc = client.get_service("GoogleAdsService")
    enums = client.enums
    ops: list = []
    plan: list[str] = []

    if args.set_budget:
        op = client.get_type("MutateOperation")
        b = op.campaign_budget_operation.update
        b.resource_name = svc.campaign_budget_path(customer_id, args.budget_id)
        b.amount_micros = int(round(args.amount * 1_000_000))
        _apply_mask(client, op.campaign_budget_operation, b)
        ops.append(op)
        plan.append(f"Budget {args.budget_id}: set daily amount -> {args.amount}")

    if args.campaign_status:
        op = client.get_type("MutateOperation")
        c = op.campaign_operation.update
        c.resource_name = svc.campaign_path(customer_id, args.campaign_id)
        c.status = getattr(enums.CampaignStatusEnum, args.status.upper())
        _apply_mask(client, op.campaign_operation, c)
        ops.append(op)
        plan.append(f"Campaign {args.campaign_id}: status -> {args.status.upper()}")

    if args.set_cpc:
        op = client.get_type("MutateOperation")
        g = op.ad_group_operation.update
        g.resource_name = svc.ad_group_path(customer_id, args.ad_group_id)
        g.cpc_bid_micros = int(round(args.cpc * 1_000_000))
        _apply_mask(client, op.ad_group_operation, g)
        ops.append(op)
        plan.append(f"Ad group {args.ad_group_id}: max CPC -> {args.cpc}")

    if args.criterion_status:
        op = client.get_type("MutateOperation")
        k = op.ad_group_criterion_operation.update
        k.resource_name = svc.ad_group_criterion_path(
            customer_id, args.ad_group_id, args.criterion_id)
        k.status = getattr(enums.AdGroupCriterionStatusEnum, args.status.upper())
        _apply_mask(client, op.ad_group_criterion_operation, k)
        ops.append(op)
        plan.append(f"Criterion {args.criterion_id} (ad group {args.ad_group_id}): "
                    f"status -> {args.status.upper()}")

    if not ops:
        print("No operation selected. See --help for the available actions.",
              file=sys.stderr)
        sys.exit(2)
    return ops, plan


def main() -> int:
    ap = argparse.ArgumentParser(description="Update campaign/ad-group entities.")
    ap.add_argument("--set-budget", action="store_true")
    ap.add_argument("--campaign-status", action="store_true")
    ap.add_argument("--set-cpc", action="store_true")
    ap.add_argument("--criterion-status", action="store_true")

    ap.add_argument("--budget-id")
    ap.add_argument("--campaign-id")
    ap.add_argument("--ad-group-id")
    ap.add_argument("--criterion-id")
    ap.add_argument("--amount", type=float, help="daily budget amount (account currency)")
    ap.add_argument("--cpc", type=float, help="max CPC bid (account currency)")
    ap.add_argument("--status", help="ENABLED | PAUSED | REMOVED")
    ap.add_argument("--confirm", action="store_true")
    args = ap.parse_args()

    client = _client.get_client()
    customer_id = _client.get_customer_id(client)
    ops, plan = build(client, customer_id, args)
    apply_mutate(client, customer_id, ops, confirm=args.confirm, plan_lines=plan)
    return 0


if __name__ == "__main__":
    sys.exit(main())
