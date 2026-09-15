"""Shared Google Ads client + config loading.

Every script imports from here so auth/config logic lives in exactly one place.
Credentials are never read from inside the skill folder: the config path comes
from the GOOGLE_ADS_CONFIGURATION_FILE_PATH env var, falling back to the
conventional ~/.config/google-ads/google-ads.yaml location.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

try:
    from google.ads.googleads.client import GoogleAdsClient
except ImportError:  # pragma: no cover - surfaced by doctor.py
    GoogleAdsClient = None  # type: ignore


DEFAULT_CONFIG_PATH = Path.home() / ".config" / "google-ads" / "google-ads.yaml"


def config_path() -> Path:
    """Resolve the google-ads.yaml path (env var wins, else the default)."""
    env = os.environ.get("GOOGLE_ADS_CONFIGURATION_FILE_PATH")
    return Path(env).expanduser() if env else DEFAULT_CONFIG_PATH


def _fail(msg: str) -> "None":
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(2)


def _use_public_ca_bundle() -> None:
    """Force TLS to verify against the public certifi bundle only.

    Some environments preset SSL_CERT_FILE to a single internal/corporate root
    CA, which then (a) fails to verify genuine Google certs and (b) would
    silently trust any interception using that root. Pinning requests + gRPC to
    certifi's public roots fixes verification AND fails closed: if anything ever
    tried to man-in-the-middle these calls, they error instead of being trusted.
    No-op if certifi is unavailable.
    """
    try:
        import certifi
    except ImportError:
        return
    ca = certifi.where()
    os.environ["SSL_CERT_FILE"] = ca
    os.environ["REQUESTS_CA_BUNDLE"] = ca
    os.environ["GRPC_DEFAULT_SSL_ROOTS_FILE_PATH"] = ca


def get_client() -> "GoogleAdsClient":
    """Build a GoogleAdsClient from the resolved config file.

    Exits with a clear message (rather than a traceback) if the library is
    missing or the config file cannot be found, so scripts fail readably.
    """
    if GoogleAdsClient is None:
        _fail(
            "The 'google-ads' library is not installed. "
            "Run: pip install -r requirements.txt"
        )
    _use_public_ca_bundle()
    path = config_path()
    if not path.exists():
        _fail(
            f"Config file not found at {path}. Set "
            "GOOGLE_ADS_CONFIGURATION_FILE_PATH or create the file "
            "(see config/google-ads.yaml.example and SETUP.md)."
        )
    return GoogleAdsClient.load_from_storage(str(path))


def get_customer_id(client: "GoogleAdsClient") -> str:
    """The target customer ID (digits only), taken from login_customer_id."""
    cid = getattr(client, "login_customer_id", None)
    if not cid:
        _fail(
            "login_customer_id is not set in the config file. Add it "
            "(digits only, no dashes)."
        )
    return str(cid)
