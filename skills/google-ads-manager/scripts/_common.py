"""Shared helpers: the safety-gated mutate, error parsing, output formatting.

The single most important thing in this skill lives here: apply_mutate() runs
every change through validate_only first, prints a plan, and refuses to touch
the account unless confirm=True. All mutating scripts route through it.
"""

from __future__ import annotations

import csv
import io
import json
import sys
from typing import Iterable, Sequence


# --------------------------------------------------------------------------- #
# Error handling
# --------------------------------------------------------------------------- #
def handle_google_ads_exception(ex) -> "None":
    """Print a GoogleAdsException as per-operation, actionable failures."""
    request_id = getattr(ex, "request_id", "unknown")
    print(f"\nRequest FAILED (request_id={request_id}):", file=sys.stderr)
    failure = getattr(ex, "failure", None)
    if failure is None:
        print(f"  {ex}", file=sys.stderr)
        sys.exit(1)
    for error in failure.errors:
        loc = ""
        if error.location and error.location.field_path_elements:
            loc = " @ " + ".".join(
                e.field_name for e in error.location.field_path_elements
            )
        code = _error_code_name(error)
        print(f"  [{code}]{loc}: {error.message}", file=sys.stderr)
        hint = _hint_for(code, error.message)
        if hint:
            print(f"      hint: {hint}", file=sys.stderr)
    sys.exit(1)


def _error_code_name(error) -> str:
    try:
        which = error.error_code._pb.WhichOneof("error_code")
        return f"{which}={getattr(error.error_code, which)}" if which else "error"
    except Exception:
        return "error"


def _hint_for(code: str, message: str) -> str:
    low = (code + " " + message).lower()
    if "developer_token_not_approved" in low or "not approved" in low:
        return (
            "Your developer token only has test-account access. Apply for "
            "Basic access in the Ads API Center, or target a TEST account."
        )
    if "authentication" in low or "authorization" in low or "permission" in low:
        return (
            "Auth/delegation issue. Confirm the impersonated_email is a "
            "Workspace user with access to this Ads account and that "
            "domain-wide delegation is enabled. Run doctor.py."
        )
    if "customer_not_enabled" in low or "not_found" in low:
        return "Check login_customer_id (digits only, no dashes) is correct and accessible."
    if "quota" in low or "rate" in low or "resource_exhausted" in low:
        return "Rate/quota limit hit. Retry with backoff or reduce batch size."
    return ""


# --------------------------------------------------------------------------- #
# The safety-gated mutate
# --------------------------------------------------------------------------- #
def apply_mutate(
    client,
    customer_id: str,
    mutate_operations: Sequence,
    *,
    confirm: bool,
    plan_lines: Iterable[str],
) -> "object | None":
    """Run mutate_operations with a validate -> plan -> confirm gate.

    1. Always runs validate_only=True first (catches errors, changes nothing).
    2. Prints the human-readable plan (plan_lines).
    3. If confirm is False, stops here (dry run) and returns None.
    4. If confirm is True, runs the real mutate and returns the response.
    """
    from google.ads.googleads.errors import GoogleAdsException

    ga_service = client.get_service("GoogleAdsService")

    def _build_request(validate_only: bool):
        req = client.get_type("MutateGoogleAdsRequest")
        req.customer_id = customer_id
        req.mutate_operations.extend(mutate_operations)
        req.validate_only = validate_only
        req.response_content_type = (
            client.enums.ResponseContentTypeEnum.MUTABLE_RESOURCE
        )
        return req

    # Step 1: validate_only — verifies the whole batch without applying it.
    try:
        ga_service.mutate(request=_build_request(validate_only=True))
    except GoogleAdsException as ex:
        print("Validation failed — nothing was changed.", file=sys.stderr)
        handle_google_ads_exception(ex)

    # Step 2: show the plan.
    print("\n" + "=" * 70)
    print("PLANNED CHANGES (validated OK, NOT yet applied):")
    print("=" * 70)
    for line in plan_lines:
        print(f"  {line}")
    print(f"  Target account: {customer_id}")
    print("=" * 70)

    # Step 3: dry-run stop.
    if not confirm:
        print(
            "\nDRY RUN. No changes applied. Re-run with --confirm to apply "
            "the plan above."
        )
        return None

    # Step 4: apply for real.
    try:
        response = ga_service.mutate(request=_build_request(validate_only=False))
    except GoogleAdsException as ex:
        handle_google_ads_exception(ex)
        return None  # unreachable; handle_* exits

    print("\nAPPLIED. Affected resources:")
    for result in response.mutate_operation_responses:
        which = result._pb.WhichOneof("response")
        if which:
            res = getattr(result, which)
            print(f"  {getattr(res, 'resource_name', which)}")
    return response


# --------------------------------------------------------------------------- #
# Output formatting for reports
# --------------------------------------------------------------------------- #
def print_rows(rows: list[dict], fmt: str) -> "None":
    """Print report rows as table | csv | json."""
    if fmt == "json":
        print(json.dumps(rows, indent=2, default=str))
        return
    if not rows:
        print("(no rows)")
        return
    headers = list(rows[0].keys())
    if fmt == "csv":
        out = io.StringIO()
        writer = csv.DictWriter(out, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
        print(out.getvalue().rstrip())
        return
    # table (default)
    widths = {h: max(len(h), *(len(str(r.get(h, ""))) for r in rows)) for h in headers}
    line = " | ".join(h.ljust(widths[h]) for h in headers)
    print(line)
    print("-+-".join("-" * widths[h] for h in headers))
    for r in rows:
        print(" | ".join(str(r.get(h, "")).ljust(widths[h]) for h in headers))
