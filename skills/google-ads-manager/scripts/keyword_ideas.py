"""Keyword research via the Keyword Planner (read-only, no budget consumed).

Two modes, both returning KeywordPlanHistoricalMetrics (avg monthly searches,
competition, and the top-of-page bid range you use to set bids):

  IDEAS      — GenerateKeywordIdeas: discover NEW keywords from seed terms
               and/or a URL.
  HISTORICAL — GenerateKeywordHistoricalMetrics: metrics for a list of
               keywords you already have.

Metrics refresh ~monthly and are approximate; cache results rather than
re-querying constantly. See reference/keyword-planner.md for geo/language ids.

Usage:
    # Ideas from seed keywords:
    python keyword_ideas.py --seed "running shoes" --seed "trail shoes" --geo 2840

    # Ideas from a landing page URL:
    python keyword_ideas.py --url https://example.com/shoes --geo 2840

    # Historical metrics for a specific list:
    python keyword_ideas.py --historical --keyword "running shoes" \
        --keyword "buy sneakers" --geo 2840 --format csv

    # Read keywords from a file (one per line):
    python keyword_ideas.py --historical --keywords-file kws.txt --geo 2840
"""

from __future__ import annotations

import argparse
import sys

import _client
from _common import print_rows


DEFAULT_LANGUAGE_ID = "1000"  # English. See reference/keyword-planner.md.


def _metrics_row(text: str, m) -> dict:
    """Flatten a KeywordPlanHistoricalMetrics message into a printable row."""
    comp = getattr(m, "competition", None)
    comp_name = getattr(comp, "name", str(comp)) if comp is not None else ""

    def micros(v):
        return round(int(v) / 1_000_000, 2) if v else 0.0

    return {
        "keyword": text,
        "avg_monthly_searches": int(getattr(m, "avg_monthly_searches", 0) or 0),
        "competition": comp_name,
        "competition_index": int(getattr(m, "competition_index", 0) or 0),
        "top_of_page_bid_low": micros(getattr(m, "low_top_of_page_bid_micros", 0)),
        "top_of_page_bid_high": micros(getattr(m, "high_top_of_page_bid_micros", 0)),
    }


def _network(client, partners: bool):
    e = client.enums.KeywordPlanNetworkEnum
    return e.GOOGLE_SEARCH_AND_PARTNERS if partners else e.GOOGLE_SEARCH


def _geo_names(geos):
    return [f"geoTargetConstants/{g}" for g in geos]


def run_ideas(client, customer_id, args) -> list[dict]:
    service = client.get_service("KeywordPlanIdeaService")
    request = client.get_type("GenerateKeywordIdeasRequest")
    request.customer_id = customer_id
    request.language = f"languageConstants/{args.lang}"
    request.geo_target_constants.extend(_geo_names(args.geo or []))
    request.keyword_plan_network = _network(client, args.partners)
    request.include_adult_keywords = False

    if args.seed and args.url:
        request.keyword_and_url_seed.url = args.url
        request.keyword_and_url_seed.keywords.extend(args.seed)
    elif args.seed:
        request.keyword_seed.keywords.extend(args.seed)
    elif args.url:
        request.url_seed.url = args.url
    else:
        print("Ideas mode needs --seed and/or --url.", file=sys.stderr)
        sys.exit(2)

    rows = [_metrics_row(idea.text, idea.keyword_idea_metrics)
            for idea in service.generate_keyword_ideas(request=request)]
    return rows


def run_historical(client, customer_id, args) -> list[dict]:
    keywords = list(args.keyword or [])
    if args.keywords_file:
        with open(args.keywords_file) as f:
            keywords += [ln.strip() for ln in f if ln.strip()]
    if not keywords:
        print("Historical mode needs --keyword and/or --keywords-file.",
              file=sys.stderr)
        sys.exit(2)

    service = client.get_service("KeywordPlanIdeaService")
    request = client.get_type("GenerateKeywordHistoricalMetricsRequest")
    request.customer_id = customer_id
    request.keywords.extend(keywords)
    request.language = f"languageConstants/{args.lang}"
    request.geo_target_constants.extend(_geo_names(args.geo or []))
    request.keyword_plan_network = _network(client, args.partners)

    response = service.generate_keyword_historical_metrics(request=request)
    return [_metrics_row(r.text, r.keyword_metrics) for r in response.results]


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Keyword Planner research (read-only, no spend).")
    ap.add_argument("--historical", action="store_true",
                    help="metrics for a given keyword list (default: idea discovery)")
    ap.add_argument("--seed", action="append", help="seed keyword (repeatable)")
    ap.add_argument("--url", help="seed URL (ideas mode)")
    ap.add_argument("--keyword", action="append",
                    help="keyword to look up (historical mode, repeatable)")
    ap.add_argument("--keywords-file", help="file of keywords, one per line")
    ap.add_argument("--geo", action="append",
                    help="geo target constant id, e.g. 2840=US (repeatable)")
    ap.add_argument("--lang", default=DEFAULT_LANGUAGE_ID,
                    help=f"language constant id (default {DEFAULT_LANGUAGE_ID}=English)")
    ap.add_argument("--partners", action="store_true",
                    help="use Search + Partners network (default: Search only)")
    ap.add_argument("--limit", type=int, default=50,
                    help="max rows to print (default 50; ideas mode only)")
    ap.add_argument("--format", choices=("table", "csv", "json"), default="table")
    args = ap.parse_args()

    client = _client.get_client()
    customer_id = _client.get_customer_id(client)

    from google.ads.googleads.errors import GoogleAdsException
    from _common import handle_google_ads_exception

    try:
        rows = (run_historical if args.historical else run_ideas)(
            client, customer_id, args)
    except GoogleAdsException as ex:
        handle_google_ads_exception(ex)
        return 1

    rows.sort(key=lambda r: r["avg_monthly_searches"], reverse=True)
    if not args.historical and args.limit:
        rows = rows[: args.limit]
    print_rows(rows, args.format)
    return 0


if __name__ == "__main__":
    sys.exit(main())
