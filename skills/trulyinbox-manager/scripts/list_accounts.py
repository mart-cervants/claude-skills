"""List connected TrulyInbox email accounts. Read-only.

Examples:
    python list_accounts.py
    python list_accounts.py --search example.com
    python list_accounts.py --status warming
"""

from __future__ import annotations

import argparse
import json
import sys

import _client


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--search", help="Search by email address or name")
    ap.add_argument("--status", choices=["active", "warming", "paused", "error", "auth-expired"])
    ap.add_argument("--tags", nargs="*", help="Filter by tag name(s)")
    ap.add_argument("--format", choices=["table", "json"], default="table")
    args = ap.parse_args()

    client = _client.get_client()
    params: dict = {}
    if args.search:
        params["search"] = args.search
    if args.status:
        params["status"] = args.status
    if args.tags:
        params["tags"] = args.tags

    try:
        payload = client.get("/email-accounts", params=params)
    except _client.TrulyInboxError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    items = payload.get("items", [])
    if args.format == "json":
        print(json.dumps(payload, indent=2))
        return 0

    if not items:
        print("No accounts found.")
        return 0

    print(f"{'id':>10}  {'email':<35}  {'status':<12}  {'warmupScore':>11}  {'readiness':<16}  tags")
    for it in items:
        print(f"{it['id']:>10}  {it['fromEmail']:<35}  {it['status']:<12}  "
              f"{str(it.get('warmupScore')):>11}  {str(it.get('outreachReadinessStatus')):<16}  "
              f"{','.join(it.get('tags', []))}")
    print(f"\n{payload.get('total')} total, page {payload.get('page')}/{payload.get('totalPages')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
