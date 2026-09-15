"""Verify the TrulyInbox API setup end-to-end. Run this FIRST.

Prints a pass/fail checklist. Read-only: never mutates anything.
Exit code 0 = all good, 1 = something to fix.
"""

from __future__ import annotations

import sys

import _client

PASS, FAIL = "PASS", "FAIL"


def _line(status: str, label: str, detail: str = "") -> None:
    tail = f" — {detail}" if detail else ""
    print(f"[{status}] {label}{tail}")


def main() -> int:
    try:
        import requests  # noqa: F401
        _line(PASS, "requests library importable")
    except ImportError:
        _line(FAIL, "requests library importable", "run: pip install -r requirements.txt")
        return 1

    try:
        import yaml  # noqa: F401
        _line(PASS, "PyYAML importable")
    except ImportError:
        _line(FAIL, "PyYAML importable", "run: pip install -r requirements.txt")
        return 1

    path = _client.config_path()
    if not path.exists():
        _line(FAIL, "config file present", f"not found at {path} (see SETUP.md)")
        return 1
    _line(PASS, "config file present", str(path))

    try:
        client = _client.get_client()
    except SystemExit:
        return 1

    try:
        client.get("/health")
        _line(PASS, "API health check (GET /health)")
    except _client.TrulyInboxError as e:
        _line(FAIL, "API health check (GET /health)", str(e))
        return 1

    try:
        rl = client.get("/rate-limit")
        _line(PASS, "authentication (GET /rate-limit)", str(rl))
    except _client.TrulyInboxError as e:
        _line(FAIL, "authentication (GET /rate-limit)", str(e))
        print("\nCommon cause: wrong/expired api_key in the config file. "
              "Regenerate under TrulyInbox → Settings → API.")
        return 1

    print("\nDoctor finished. All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
