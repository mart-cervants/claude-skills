"""Verify the Google Ads API setup end-to-end. Run this FIRST.

Prints a pass/fail checklist and, on failure, exactly what to fix. Read-only:
it never mutates the account. Exit code 0 = all good, 1 = something to fix.
"""

from __future__ import annotations

import sys
from pathlib import Path

import _client


PASS = "PASS"
FAIL = "FAIL"
WARN = "WARN"


def _line(status: str, label: str, detail: str = "") -> None:
    tail = f" — {detail}" if detail else ""
    print(f"[{status}] {label}{tail}")


def main() -> int:
    ok = True

    # 1. Library present.
    try:
        from google.ads.googleads.client import GoogleAdsClient  # noqa: F401
        import google.ads.googleads as pkg

        _line(PASS, "google-ads library importable", f"v{getattr(pkg, '__version__', '?')}")
    except ImportError:
        _line(FAIL, "google-ads library importable",
              "run: pip install -r requirements.txt")
        return 1  # nothing else can run

    # 2. Config file found + parseable.
    path = _client.config_path()
    if not path.exists():
        _line(FAIL, "config file present", f"not found at {path} (see SETUP.md)")
        return 1
    try:
        import yaml

        cfg = yaml.safe_load(Path(path).read_text()) or {}
        _line(PASS, "config file present", str(path))
    except Exception as e:  # noqa: BLE001
        _line(FAIL, "config file parseable", str(e))
        return 1

    # 3. Required fields.
    for field in ("developer_token", "login_customer_id"):
        if not cfg.get(field):
            _line(FAIL, f"config has {field}", "missing")
            ok = False
        else:
            _line(PASS, f"config has {field}")
    if cfg.get("json_key_file_path"):
        key_exists = Path(str(cfg["json_key_file_path"])).expanduser().exists()
        _line(PASS if key_exists else FAIL, "service-account key file present",
              cfg["json_key_file_path"] if key_exists else "path does not exist")
        ok = ok and key_exists
        if not cfg.get("impersonated_email"):
            _line(WARN, "impersonated_email set",
                  "required for service-account domain-wide delegation")
    else:
        _line(WARN, "auth method", "no json_key_file_path — expecting OAuth refresh token")

    if not ok:
        print("\nFix the FAIL items above, then re-run doctor.py.")
        return 1

    # 4. Live auth check: list accessible customers (read-only).
    try:
        client = _client.get_client()
        customer_service = client.get_service("CustomerService")
        accessible = customer_service.list_accessible_customers()
        ids = [rn.split("/")[-1] for rn in accessible.resource_names]
        _line(PASS, "authentication (list_accessible_customers)",
              f"{len(ids)} account(s) reachable")
    except Exception as e:  # noqa: BLE001
        _line(FAIL, "authentication (list_accessible_customers)", str(e)[:200])
        print(
            "\nCommon causes:\n"
            "  - Domain-wide delegation not enabled for the service account,\n"
            "    or impersonated_email is not a Workspace user with Ads access.\n"
            "  - Developer token still pending / test-only.\n"
            "See SETUP.md."
        )
        return 1

    # 5. Target account reachable.
    target = str(cfg["login_customer_id"])
    if target in ids:
        _line(PASS, "target login_customer_id accessible", target)
    else:
        _line(WARN, "target login_customer_id accessible",
              f"{target} not in accessible list {ids} "
              "(ok if it's a client account under a manager)")

    print("\nDoctor finished. Reminder: a fresh developer token only reaches TEST "
          "accounts until Google approves Basic/Standard access.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
