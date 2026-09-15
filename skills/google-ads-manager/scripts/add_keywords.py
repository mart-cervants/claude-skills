"""Add keywords (positive or negative) to an EXISTING ad group.

Creates one AdGroupCriterionOperation per keyword and routes through
_common.apply_mutate, so it validates and prints a plan first and only applies
with --confirm. Use report.py to find the --ad-group-id first
(see reference/gaql-cookbook.md).

Usage (dry-run unless --confirm):
    # Add positive phrase-match keywords:
    python add_keywords.py --ad-group-id 200138775740 \
        --keyword "invoice processing" --keyword "ocr receipt scanning" \
        --match PHRASE --confirm

    # Add ad-group negative keywords:
    python add_keywords.py --ad-group-id 200138775740 --negative \
        --keyword "free" --keyword "template" --match BROAD --confirm

    # From a file (each line: `text` or `text,MATCH`):
    python add_keywords.py --ad-group-id 200138775740 --keywords-file kws.txt
"""

from __future__ import annotations

import argparse
import sys

import _client
from _common import apply_mutate


def _parse_keywords(args) -> list[tuple[str, str]]:
    """Return [(text, match_type), ...] from --keyword and/or --keywords-file."""
    default_match = args.match.upper()
    out: list[tuple[str, str]] = []
    for kw in args.keyword or []:
        out.append((kw.strip(), default_match))
    if args.keywords_file:
        with open(args.keywords_file) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if "," in line:
                    text, match = line.rsplit(",", 1)
                    out.append((text.strip(), match.strip().upper()))
                else:
                    out.append((line, default_match))
    if not out:
        print("No keywords given. Use --keyword and/or --keywords-file.",
              file=sys.stderr)
        sys.exit(2)
    return out


def build(client, customer_id, args) -> tuple[list, list[str]]:
    svc = client.get_service("GoogleAdsService")
    enums = client.enums
    ad_group_rn = svc.ad_group_path(customer_id, args.ad_group_id)
    ops: list = []
    plan: list[str] = []

    for text, match in _parse_keywords(args):
        op = client.get_type("MutateOperation")
        c = op.ad_group_criterion_operation.create
        c.ad_group = ad_group_rn
        c.status = enums.AdGroupCriterionStatusEnum.ENABLED
        c.negative = args.negative
        c.keyword.text = text
        try:
            c.keyword.match_type = getattr(enums.KeywordMatchTypeEnum, match)
        except AttributeError:
            print(f"Invalid match type '{match}' (use EXACT|PHRASE|BROAD).",
                  file=sys.stderr)
            sys.exit(2)
        if args.cpc is not None and not args.negative:
            c.cpc_bid_micros = int(round(args.cpc * 1_000_000))
        ops.append(op)
        neg = "NEGATIVE " if args.negative else ""
        bid = f" @ {args.cpc} CPC" if (args.cpc is not None and not args.negative) else ""
        plan.append(f"Ad group {args.ad_group_id}: add {neg}[{match}] '{text}'{bid}")

    return ops, plan


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Add positive or negative keywords to an existing ad group.")
    ap.add_argument("--ad-group-id", required=True)
    ap.add_argument("--keyword", action="append", help="keyword text (repeatable)")
    ap.add_argument("--keywords-file",
                    help="file of keywords; each line 'text' or 'text,MATCH'")
    ap.add_argument("--match", default="PHRASE",
                    help="default match type: EXACT | PHRASE | BROAD (default PHRASE)")
    ap.add_argument("--negative", action="store_true",
                    help="add as negative keywords instead of positive")
    ap.add_argument("--cpc", type=float,
                    help="optional max CPC bid for the added keywords (account currency)")
    ap.add_argument("--confirm", action="store_true",
                    help="apply the change (omit for a dry run)")
    args = ap.parse_args()

    client = _client.get_client()
    customer_id = _client.get_customer_id(client)
    ops, plan = build(client, customer_id, args)
    apply_mutate(client, customer_id, ops, confirm=args.confirm, plan_lines=plan)
    return 0


if __name__ == "__main__":
    sys.exit(main())
