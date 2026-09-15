"""Add headlines / descriptions to an existing Responsive Search Ad.

Editing an RSA replaces the WHOLE repeated field, so this script fetches the
current assets, APPENDS the new ones (preserving text and any pinning), and
writes the full list back with a precise field mask — it never overwrites your
existing copy. Routes through _common.apply_mutate (validate -> plan -> confirm).

RSA limits: up to 15 headlines and 4 descriptions. Headlines <= 30 chars,
descriptions <= 90 chars (enforced by the API; caught in the dry run).

Find the --ad-id with:
  report.py --query "SELECT ad_group_ad.ad.id FROM ad_group_ad WHERE campaign.id = <id>"

Usage (dry-run unless --confirm):
    python update_ad.py --ad-id 821568783800 \
        --add-headline "Invoice PDF to Excel" \
        --add-headline "Export Invoices to Excel" --confirm
"""

from __future__ import annotations

import argparse
import sys

import _client
from _common import apply_mutate

MAX_HEADLINES = 15
MAX_DESCRIPTIONS = 4


def _fetch_rsa(client, customer_id, ad_id):
    svc = client.get_service("GoogleAdsService")
    q = f"""
        SELECT ad_group_ad.ad.id,
               ad_group_ad.ad.responsive_search_ad.headlines,
               ad_group_ad.ad.responsive_search_ad.descriptions
        FROM ad_group_ad
        WHERE ad_group_ad.ad.id = {ad_id}
    """
    for batch in svc.search_stream(customer_id=customer_id, query=q):
        for row in batch.results:
            return row.ad_group_ad.ad.responsive_search_ad
    print(f"Ad id {ad_id} not found (or not a Responsive Search Ad).",
          file=sys.stderr)
    sys.exit(2)


def build(client, customer_id, args) -> tuple[list, list[str]]:
    from google.protobuf import field_mask_pb2

    ad_id = args.ad_id
    rsa_current = _fetch_rsa(client, customer_id, ad_id)
    new_h = args.add_headline or []
    new_d = args.add_description or []
    if not new_h and not new_d:
        print("Nothing to add. Use --add-headline and/or --add-description.",
              file=sys.stderr)
        sys.exit(2)

    # capacity checks (fail fast with a clear message before the API does)
    if len(rsa_current.headlines) + len(new_h) > MAX_HEADLINES:
        print(f"Would exceed {MAX_HEADLINES} headlines "
              f"({len(rsa_current.headlines)} existing + {len(new_h)} new).",
              file=sys.stderr)
        sys.exit(2)
    if len(rsa_current.descriptions) + len(new_d) > MAX_DESCRIPTIONS:
        print(f"Would exceed {MAX_DESCRIPTIONS} descriptions "
              f"({len(rsa_current.descriptions)} existing + {len(new_d)} new). "
              "Descriptions are full — replacing one isn't supported here; edit "
              "in the UI if you need to swap a description.", file=sys.stderr)
        sys.exit(2)

    op = client.get_type("MutateOperation")
    ad = op.ad_operation.update
    ad.resource_name = f"customers/{customer_id}/ads/{ad_id}"
    rsa = ad.responsive_search_ad
    plan: list[str] = []
    mask_paths: list[str] = []

    if new_h:
        for h in rsa_current.headlines:  # preserve existing (text + pinning)
            a = client.get_type("AdTextAsset")
            a.text = h.text
            if h.pinned_field:
                a.pinned_field = h.pinned_field
            rsa.headlines.append(a)
        for text in new_h:
            a = client.get_type("AdTextAsset")
            a.text = text
            rsa.headlines.append(a)
            plan.append(f"Ad {ad_id}: add headline '{text}' ({len(text)} chars)")
        mask_paths.append("responsive_search_ad.headlines")

    if new_d:
        for d in rsa_current.descriptions:
            a = client.get_type("AdTextAsset")
            a.text = d.text
            if d.pinned_field:
                a.pinned_field = d.pinned_field
            rsa.descriptions.append(a)
        for text in new_d:
            a = client.get_type("AdTextAsset")
            a.text = text
            rsa.descriptions.append(a)
            plan.append(f"Ad {ad_id}: add description '{text}' ({len(text)} chars)")
        mask_paths.append("responsive_search_ad.descriptions")

    client.copy_from(op.ad_operation.update_mask,
                     field_mask_pb2.FieldMask(paths=mask_paths))
    plan.append(f"(existing copy preserved: {len(rsa_current.headlines)} "
                f"headlines, {len(rsa_current.descriptions)} descriptions)")
    return [op], plan


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Add headlines/descriptions to an existing RSA.")
    ap.add_argument("--ad-id", required=True)
    ap.add_argument("--add-headline", action="append", help="new headline (repeatable, <=30 chars)")
    ap.add_argument("--add-description", action="append", help="new description (repeatable, <=90 chars)")
    ap.add_argument("--confirm", action="store_true")
    args = ap.parse_args()

    client = _client.get_client()
    customer_id = _client.get_customer_id(client)
    ops, plan = build(client, customer_id, args)
    apply_mutate(client, customer_id, ops, confirm=args.confirm, plan_lines=plan)
    return 0


if __name__ == "__main__":
    sys.exit(main())
