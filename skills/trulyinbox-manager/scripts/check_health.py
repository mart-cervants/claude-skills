"""One-shot warmup/deliverability health report for a single TrulyInbox account.

Pulls warmup status, warmup settings, setup score, DNS health, and deliverability
score in one call each and prints a combined report — the direct MCP-tool-free
replacement for eyeballing the TrulyInbox web dashboard. Read-only.

Examples:
    python check_health.py --email user@example.com
    python check_health.py --account-id 12345 --days 30
    python check_health.py --email user@example.com --refresh-setup-score
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys

import _client


def _section(title: str) -> None:
    print(f"\n-- {title} " + "-" * max(0, 60 - len(title)))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    target = ap.add_mutually_exclusive_group(required=True)
    target.add_argument("--email", help="Account email address")
    target.add_argument("--account-id", help="Numeric emailAccountId")
    ap.add_argument("--days", type=int, default=30,
                     help="Deliverability lookback window in days (default 30)")
    ap.add_argument("--refresh-setup-score", action="store_true",
                     help="Force a synchronous refresh of the setup score before reading it")
    args = ap.parse_args()

    client = _client.get_client()
    account_id = _client.resolve_account_id(client, args.email or args.account_id)
    print(f"Account: {args.email or args.account_id}  (id={account_id})")

    # Warmup status (today's activity + outreach readiness)
    _section("Warmup status (today)")
    try:
        ws = client.get(f"/warmup-status/{account_id}")
        print(f"current={ws['current']}  strategy={ws['strategy']}  "
              f"dailySendingLimit={ws.get('dailySendingLimit')}")
        print(f"sent={ws['sent']}  received={ws['received']}  replied={ws['replied']}  "
              f"spam={ws['spam']}  undelivered={ws['undelivered']}")
        print(f"warmupScore={ws.get('warmupScore')}  "
              f"outreachReadinessStatus={ws.get('outreachReadinessStatus')}")
        if ws.get("warmupScore") is None:
            print("NOTE: no warmup score computed yet — too new or warmup not running.")
    except _client.TrulyInboxError as e:
        print(f"unavailable: {e}")

    # Warmup settings (strategy/volume config)
    _section("Warmup settings")
    try:
        wset = client.get(f"/warmup-settings/{account_id}")
        print(f"warmupStatus={wset['warmupStatus']}  strategy={wset['strategy']}  "
              f"timeZone={wset['timeZone']}")
        print(f"maxSendingLimit={wset.get('maxSendingLimit')}  "
              f"warmUpInitialSendingLimit={wset.get('warmUpInitialSendingLimit')}  "
              f"increaseEmailsByNumber={wset.get('increaseEmailsByNumber')}")
        print(f"volume split — google={wset['googleVolumePercentage']}%  "
              f"microsoft={wset['microsoftVolumePercentage']}%  "
              f"others={wset['othersVolumePercentage']}%")
        if wset["warmupStatus"] != "active":
            print(f"NOTE: warmup is '{wset['warmupStatus']}', not actively running.")
    except _client.TrulyInboxError as e:
        print(f"unavailable: {e}")

    # Setup score (SPF/DKIM/DMARC/MX/blacklist composite)
    _section("Setup score")
    try:
        if args.refresh_setup_score:
            score = client.post(f"/setup-score/{account_id}/refresh")
        else:
            score = client.get(f"/setup-score/{account_id}")
        print(f"emailAccountScore={score['emailAccountScore']}/100  "
              f"(updatedAt={score.get('updatedAt')})")
        for k in ("dmarcScore", "spfScore", "dkimScore", "mxRecordScore",
                  "ipBlacklistScore", "domainBlacklistScore"):
            if k in score:
                print(f"  {k}={score[k]}")
    except _client.TrulyInboxError as e:
        print(f"unavailable: {e}")

    # Live DNS health
    _section("DNS health (live lookup)")
    try:
        dns = client.get(f"/dns-health/{account_id}")
        print(f"spf={dns['spf']}  dkim={dns['dkim']}  dmarc={dns['dmarc']}  mx={dns['mx']}")
        failing = [k for k in ("spf", "dkim", "dmarc", "mx") if dns[k] != "pass"]
        if failing:
            print(f"NOTE: failing/unknown: {', '.join(failing)}")
    except _client.TrulyInboxError as e:
        print(f"unavailable: {e}")

    # Real inbox-vs-spam deliverability by ESP
    _section(f"Deliverability score (last {args.days} days)")
    end = dt.date.today()
    start = end - dt.timedelta(days=args.days)
    try:
        d = client.post(f"/deliverability-score/{account_id}", json_body={
            "startDate": start.isoformat(),
            "endDate": end.isoformat(),
        })
        print(f"totalDeliverabilityRate={d['totalDeliverabilityRate']}%  "
              f"(sent={d['totalSentCount']}, inbox={d['totalInboxCount']}, "
              f"spam={d['totalSpamInboxCount']})")
        for esp in ("gmail", "outlook", "other"):
            if d.get(esp):
                e = d[esp]
                print(f"  {esp}: {e}")
        if d["totalSentCount"] == 0:
            print("NOTE: zero sends in this window — score is not meaningful yet.")
    except _client.TrulyInboxError as e:
        print(f"unavailable: {e}")

    print("\nReminder: this is TrulyInbox's own warmup-network score, not a "
          "substitute for a real seed-list placement test (GlockApps/Inbox Radar) "
          "— see saleshandy-account-health's caveat on that distinction.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
