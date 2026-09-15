---
name: trulyinbox-manager
description: Use when the user wants to check TrulyInbox warmup status, deliverability score, setup/DNS health, or the account-wide warmup dashboard for a Saleshandy email account via the TrulyInbox Open API. Read-only in this version — no warmup start/stop/settings changes.
---

# TrulyInbox Manager

## Overview

Programmatic access to TrulyInbox's warmup/deliverability data via small
Python scripts calling the official Open API (`X-Api-Key` header, plain
REST, no SDK). Built to replace manually checking the TrulyInbox web
dashboard — this is the tool `saleshandy-account-health` calls for the "real
warmup signal" it can't get from Saleshandy's own `ramp-up-*` fields (see
that skill's docs for why those native fields aren't trustworthy).

**v1 scope is read-only by design.** Warmup start/stop, settings updates,
account connect/disconnect/delete, and workspace bulk-connect exist in the
API but are deliberately not built here yet — no current use case needed
them, and mutating endpoints deserve the same dry-run→confirm safety gate
`google-ads-manager` uses before they're added. If a task needs one of
those, say so explicitly rather than improvising a raw API call.

All scripts live in `scripts/`, share auth via `_client.py`. The API key
lives **outside** this folder (see `SETUP.md`) — never read or write it
inside the skill.

## Prerequisite gate — always run first

```bash
python scripts/doctor.py
```

If it reports any `FAIL`, walk the user through `SETUP.md`. Don't run other
scripts against a broken config — you'll just get opaque 401/403s.

## Intent → script routing

| User wants to… | Run |
|----------------|-----|
| Full health check on one account (warmup + setup score + DNS + deliverability) | `check_health.py --email <address>` |
| List/search connected accounts | `list_accounts.py [--search <term>] [--status <status>]` |
| Quick portfolio-wide summary (all accounts) | `dashboard.py` |

`check_health.py` is the one to reach for from `saleshandy-account-health` —
it's the single-command combined report (see "Real warmup signal" in that
skill). Resolve by `--email` (looks up the id via `/email-accounts?search=`)
or `--account-id` if already known.

## Known gotchas

- **Responses are wrapped in `{"payload": {...}}` at runtime** — the
  published OpenAPI schema documents the unwrapped shape directly (e.g.
  `DashboardResponseDto`'s fields at the top level), but the real API
  nests everything one level under `payload`, same convention as
  Saleshandy's own MCP tools. `_client.py`'s `request()` unwraps this
  automatically so every script can use the documented field names as-is
  — don't re-introduce a raw `.json()` call elsewhere without the same
  unwrap.
- **Corporate TLS**: if this machine has an ambient `SSL_CERT_FILE` pointing
  at a single corporate root (e.g. `CorpRoot.pem` — the same class of issue
  as any skill calling external HTTPS APIs from a corporate network), it
  breaks both `pip install` and live API calls
  against genuine TLS certs. `_client.py` forces the public certifi bundle
  before any request; if `pip install -r requirements.txt` itself fails with
  a cert error, prefix it too:
  `SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())") pip install -r requirements.txt`.

- **Base URL**: `https://lupus-edge.trulyinbox.com/v1` — not in the API
  key/account settings anywhere, hardcoded in `_client.py`.
- **Rate limit: 20 requests/min per key.** `_client.py` auto-retries once on
  a 429 using the `X-RateLimit-Reset` header. Don't loop `check_health.py`
  over many accounts back-to-back without expecting some waiting — it makes
  5 calls per account.
- **404 means "not_found", often "no score computed yet"** — not necessarily
  a broken account. A brand-new account can legitimately have no
  `warmupScore`/`setup-score` row yet. `check_health.py` prints `unavailable`
  per-section rather than failing the whole report.
- **`deliverability-score` needs an explicit date range** (`startDate`/
  `endDate`, max window enforced server-side) — `check_health.py` defaults
  to the last 30 days via `--days`.
- **TrulyInbox's own score is a warmup-network-internal metric** — other
  warmup accounts engaging with each other — NOT the same as real ISP
  inbox placement. `check_health.py` prints a reminder of this every run;
  don't strip it out, it's the exact confusion `saleshandy-account-health`
  corrected once already (an account scored 83% here while GlockApps showed
  ~27% real placement on the same account).

## Reference

- `SETUP.md` — one-time API key setup.
- Full API reference: https://developer.trulyinbox.com/api-reference/introduction
