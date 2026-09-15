"""Account-wide warmup dashboard summary (all connected accounts). Read-only.

Usage: python dashboard.py
"""

from __future__ import annotations

import sys

import _client


def main() -> int:
    client = _client.get_client()
    try:
        d = client.get("/dashboard")
    except _client.TrulyInboxError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    print(f"Total accounts:      {d['totalAccounts']}")
    print(f"Active warmups:      {d['activeWarmups']}")
    print(f"Paused warmups:      {d['pausedWarmups']}")
    print(f"Accounts w/ errors:  {d['accountsWithErrors']}")
    print(f"Avg setup score:     {d['avgSetupScore']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
