"""Run a GAQL query (raw or a named preset) and print the results.

Read-only. Never consumes budget. Presets live in reference/gaql-cookbook.md
and are mirrored in the PRESETS dict below.

Usage:
    python report.py --preset campaign_spend --format table
    python report.py --query "SELECT campaign.id, campaign.name FROM campaign" --format csv
    python report.py --list-presets
"""

from __future__ import annotations

import argparse
import sys

import _client
from _common import print_rows


# Keep in sync with reference/gaql-cookbook.md.
PRESETS: dict[str, str] = {
    "campaign_spend": """
        SELECT campaign.id, campaign.name, campaign.status,
               metrics.cost_micros, metrics.impressions, metrics.clicks,
               metrics.conversions, metrics.conversions_value
        FROM campaign
        WHERE segments.date DURING LAST_30_DAYS
        ORDER BY metrics.cost_micros DESC
    """,
    "ad_group_performance": """
        SELECT campaign.name, ad_group.id, ad_group.name, ad_group.status,
               metrics.cost_micros, metrics.clicks, metrics.conversions
        FROM ad_group
        WHERE segments.date DURING LAST_30_DAYS
        ORDER BY metrics.cost_micros DESC
    """,
    "keyword_performance": """
        SELECT campaign.name, ad_group.name,
               ad_group_criterion.keyword.text,
               ad_group_criterion.keyword.match_type,
               metrics.cost_micros, metrics.clicks, metrics.conversions,
               metrics.average_cpc
        FROM keyword_view
        WHERE segments.date DURING LAST_30_DAYS
        ORDER BY metrics.cost_micros DESC
    """,
    "search_terms": """
        SELECT search_term_view.search_term, campaign.name,
               metrics.clicks, metrics.cost_micros, metrics.conversions
        FROM search_term_view
        WHERE segments.date DURING LAST_30_DAYS
        ORDER BY metrics.cost_micros DESC
    """,
    "budget_utilization": """
        SELECT campaign.name, campaign_budget.amount_micros,
               metrics.cost_micros
        FROM campaign
        WHERE segments.date DURING LAST_7_DAYS
        ORDER BY metrics.cost_micros DESC
    """,
}

def _flatten(row) -> dict:
    """Turn a GoogleAdsRow into a flat {dotted.field: value} dict for printing.

    Uses MessageToDict so it works for any GAQL query (only fields present in
    the response appear). Values in micros (keys ending _micros) are converted
    to currency units and the suffix dropped.
    """
    from google.protobuf.json_format import MessageToDict

    d = MessageToDict(row._pb, preserving_proto_field_name=True)
    out: dict = {}
    _walk(d, "", out)
    return out


def _walk(obj, prefix: str, out: dict) -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            _walk(v, f"{prefix}.{k}" if prefix else k, out)
    elif isinstance(obj, list):
        out[prefix] = ", ".join(str(x) for x in obj)
    else:
        if prefix.endswith("_micros"):
            try:
                out[prefix[: -len("_micros")]] = round(int(obj) / 1_000_000, 2)
                return
            except (TypeError, ValueError):
                pass
        out[prefix] = obj


def main() -> int:
    ap = argparse.ArgumentParser(description="Run a GAQL report (read-only).")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--preset", choices=sorted(PRESETS), help="named query preset")
    g.add_argument("--query", help="raw GAQL query string")
    ap.add_argument("--format", choices=("table", "csv", "json"), default="table")
    ap.add_argument("--list-presets", action="store_true")
    args = ap.parse_args()

    if args.list_presets:
        for name in sorted(PRESETS):
            print(name)
        return 0

    query = args.query or (PRESETS[args.preset] if args.preset else None)
    if not query:
        ap.error("provide --preset or --query (or --list-presets)")

    client = _client.get_client()
    customer_id = _client.get_customer_id(client)
    ga_service = client.get_service("GoogleAdsService")

    from google.ads.googleads.errors import GoogleAdsException
    from _common import handle_google_ads_exception

    rows: list[dict] = []
    try:
        stream = ga_service.search_stream(customer_id=customer_id, query=query)
        for batch in stream:
            for row in batch.results:
                rows.append(_flatten(row))
    except GoogleAdsException as ex:
        handle_google_ads_exception(ex)

    print_rows(rows, args.format)
    return 0


if __name__ == "__main__":
    sys.exit(main())
