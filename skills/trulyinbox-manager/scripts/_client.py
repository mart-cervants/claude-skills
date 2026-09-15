"""Shared TrulyInbox API client + config loading.

Every script imports from here so auth/config/error-handling logic lives in
exactly one place. The API key is never read from inside the skill folder:
its path comes from the TRULYINBOX_CONFIG_FILE_PATH env var, falling back to
the conventional ~/.config/trulyinbox/config.yaml location.

API docs: https://developer.trulyinbox.com/api-reference/introduction
Auth: X-Api-Key header. Base URL: https://lupus-edge.trulyinbox.com/v1
Rate limit: 20 requests/min per key (see X-RateLimit-* response headers).
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from typing import Any

try:
    import requests
except ImportError:  # pragma: no cover - surfaced by doctor.py
    requests = None  # type: ignore

try:
    import yaml
except ImportError:  # pragma: no cover - surfaced by doctor.py
    yaml = None  # type: ignore


BASE_URL = "https://lupus-edge.trulyinbox.com/v1"
DEFAULT_CONFIG_PATH = Path.home() / ".config" / "trulyinbox" / "config.yaml"


def config_path() -> Path:
    """Resolve the config.yaml path (env var wins, else the default)."""
    env = os.environ.get("TRULYINBOX_CONFIG_FILE_PATH")
    return Path(env).expanduser() if env else DEFAULT_CONFIG_PATH


def _fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(2)


def _use_public_ca_bundle() -> None:
    """Force TLS to verify against the public certifi bundle only.

    Some environments preset SSL_CERT_FILE to a single internal/corporate root
    CA, which then fails to verify genuine TrulyInbox/API certs. Pinning
    requests to certifi's public roots fixes verification and fails closed
    (no silent trust of an interception cert). Same fix as google-ads-manager
    hit on this machine. No-op if certifi is unavailable.
    """
    try:
        import certifi
    except ImportError:
        return
    ca = certifi.where()
    os.environ["SSL_CERT_FILE"] = ca
    os.environ["REQUESTS_CA_BUNDLE"] = ca


def _load_api_key() -> str:
    if yaml is None:
        _fail("PyYAML is not installed. Run: pip install -r requirements.txt")
    path = config_path()
    if not path.exists():
        _fail(
            f"Config file not found at {path}. Set TRULYINBOX_CONFIG_FILE_PATH "
            "or create it (see config/config.yaml.example and SETUP.md)."
        )
    cfg = yaml.safe_load(path.read_text()) or {}
    key = cfg.get("api_key")
    if not key or key == "YOUR_TRULYINBOX_API_KEY":
        _fail(f"api_key missing/unfilled in {path}. See SETUP.md.")
    return str(key)


class TrulyInboxError(RuntimeError):
    """Raised for any non-2xx response. Carries the parsed error body."""

    def __init__(self, status: int, error_code: str, message: str, details: Any):
        self.status = status
        self.error_code = error_code
        self.details = details
        super().__init__(f"[{status}] {error_code}: {message}")


class Client:
    """Thin requests wrapper: auth header, base URL, JSON errors, 429 backoff."""

    def __init__(self) -> None:
        if requests is None:
            _fail("The 'requests' library is not installed. Run: pip install -r requirements.txt")
        _use_public_ca_bundle()
        self._session = requests.Session()
        self._session.headers.update({"X-Api-Key": _load_api_key()})

    def request(self, method: str, path: str, *, params: dict | None = None,
                json_body: dict | None = None, max_retries: int = 3) -> Any:
        url = f"{BASE_URL}{path}"
        for attempt in range(max_retries + 1):
            resp = self._session.request(method, url, params=params, json=json_body, timeout=30)
            if resp.status_code == 429 and attempt < max_retries:
                reset = resp.headers.get("X-RateLimit-Reset")
                wait = max(1.0, float(reset) - time.time()) if reset else 2.0 * (attempt + 1)
                print(f"Rate limited (429) — waiting {wait:.0f}s before retry "
                      f"({attempt + 1}/{max_retries})...", file=sys.stderr)
                time.sleep(wait)
                continue
            break

        if 200 <= resp.status_code < 300:
            if not resp.content:
                return None
            body = resp.json()
            # Every success response is wrapped in {"payload": {...}} at
            # runtime — not reflected in the published OpenAPI schema, which
            # documents the unwrapped shape directly. Unwrap here once so
            # every script can use the documented field names as-is.
            if isinstance(body, dict) and set(body.keys()) == {"payload"}:
                return body["payload"]
            return body

        try:
            body = resp.json()
        except ValueError:
            body = {}
        raise TrulyInboxError(
            resp.status_code,
            body.get("error_code", "unknown_error"),
            body.get("message", resp.text[:300]),
            body.get("details", {}),
        )

    def get(self, path: str, **kw) -> Any:
        return self.request("GET", path, **kw)

    def post(self, path: str, json_body: dict | None = None, **kw) -> Any:
        return self.request("POST", path, json_body=json_body, **kw)


def get_client() -> Client:
    return Client()


def resolve_account_id(client: Client, email_or_id: str) -> int:
    """Accept either a numeric emailAccountId or an email address and return the id.

    Exits with a clear message if an email address matches zero or multiple
    accounts, rather than guessing.
    """
    if email_or_id.isdigit():
        return int(email_or_id)

    payload = client.get("/email-accounts", params={"search": email_or_id})
    items = payload.get("items", [])
    matches = [i for i in items if i.get("fromEmail", "").lower() == email_or_id.lower()]
    if not matches:
        matches = items  # fall back to whatever the search loosely matched
    if len(matches) == 0:
        _fail(f"No email account found matching '{email_or_id}'.")
    if len(matches) > 1:
        names = ", ".join(f"{m['fromEmail']} (id={m['id']})" for m in matches)
        _fail(f"'{email_or_id}' matched multiple accounts: {names}. Pass the numeric id instead.")
    return int(matches[0]["id"])
