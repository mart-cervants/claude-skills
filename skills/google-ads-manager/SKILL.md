---
name: google-ads-manager
description: Use when the user wants to create, update, report on, or manage Google Ads campaigns, ad groups, keywords, budgets, bids, or targeting via the Google Ads API. Runs Python scripts that call the official google-ads client library, with a mandatory dry-run-before-spend safety gate.
---

# Google Ads Manager

## Overview

Manage Google Ads campaigns through small Python scripts that call the official
`google-ads` API client (v25). Covers the full lifecycle: reporting, creating
campaigns, updating budgets/bids/status/targeting, and managing negatives & geo.

**Core principle — never spend money by accident.** Every mutating operation is
validated (`validate_only=True`) and printed as a plain-language plan BEFORE
anything is applied. Nothing touches the account until the user has seen the
plan and explicitly approved it.

All scripts live in `scripts/` and share auth via `_client.py` and the safety
gate via `_common.py`. Config/credentials live **outside** this folder (see
`SETUP.md`) — never read or write credentials inside the skill.

## Prerequisite gate — always run first

The library is installed in a dedicated venv. Run every script with that
interpreter (not the system `python3`):

```bash
~/.config/google-ads/venv/bin/python scripts/doctor.py
```

Tip: `alias gads-py="$HOME/.config/google-ads/venv/bin/python"` then `gads-py scripts/<name>.py …`.

Before any operation, confirm setup works with `doctor.py` (above).

If it reports any `FAIL`, STOP and walk the user through `SETUP.md`. Do not try
to run other scripts against a broken config — you'll just get opaque auth
errors. Two gotchas `doctor.py` flags:
- Service-account delegation needs the `impersonated_email` to be a Workspace
  user with Ads access, with domain-wide delegation enabled.
- A fresh developer token has **test-account access only** until Google approves
  Basic access — production accounts will error until then.

## Intent → script routing

| User wants to… | Run | Mutating? |
|----------------|-----|-----------|
| Diagnose why a campaign has no/low metrics | `diagnose_campaign.py --campaign-id N` | No |
| Research keywords: search volume, competition, bid ranges | `keyword_ideas.py …` (see `reference/keyword-planner.md`) | No |
| See spend / performance / keywords / search terms | `report.py --preset <name>` or `--query "<GAQL>"` | No |
| Look up ids (budget id, criterion id, campaign id) | `report.py --query "…"` (see `reference/gaql-cookbook.md`) | No |
| Create a new campaign (budget+ad groups+ads+keywords) | `create_campaign.py --spec <file.json>` | Yes |
| Add keywords (positive/negative) to an existing ad group | `add_keywords.py --ad-group-id N …` | Yes |
| Add headlines/descriptions to an existing RSA | `update_ad.py --ad-id N …` | Yes |
| Change a budget / bid / pause / enable | `update_entity.py …` | Yes |
| Add negative keywords or geo targeting | `manage_assets.py …` | Yes |

Details:
- **Keyword research** — `keyword_ideas.py` (Keyword Planner). Read-only, no
  spend. Ideas mode discovers keywords from `--seed`/`--url`; `--historical`
  gets metrics for a keyword list. Returns avg monthly searches, competition,
  and top-of-page bid ranges — use these to pick keywords and set bids before
  building a campaign spec. See `reference/keyword-planner.md`.
- **Reporting** — `report.py --list-presets` to see presets. Read-only, safe to
  run freely. Formats: `--format table|csv|json`.
- **Create** — write a JSON spec per `reference/campaign-spec.md`, then run
  `create_campaign.py`. Campaigns default to `PAUSED`.
- **Update / assets** — see each script's `--help`; ids usually come from a
  `report.py` query first.

## MANDATORY safety workflow for every mutating script

`create_campaign.py`, `update_entity.py`, and `manage_assets.py` all take a
`--confirm` flag. Without it they run `validate_only` and print the plan only.

Follow this sequence EVERY time — no exceptions:

1. Run the script **without `--confirm`** (dry run).
2. Show the printed plan to the user in chat.
3. Wait for the user to explicitly approve.
4. Only then re-run the **same command with `--confirm`**.

**You MUST NOT pass `--confirm` in the same step you first build a command.**
The user has to see the validated plan first.

### Red-flag rationalizations — STOP if you think any of these

| Thought | Reality |
|---------|---------|
| "The change is small, I'll just apply it." | Small budget typos spend real money. Dry-run first. |
| "The user already said what they want." | They approved the intent, not the validated plan. Show it. |
| "Re-running the dry-run wastes a step." | The dry-run IS the safety check. It's not optional. |
| "It's paused, so it's safe to apply directly." | Still show the plan. Habits transfer to unpaused changes. |
| "I'll pass --confirm to save a round trip." | Never. Confirm comes only after the user sees the plan. |

## MANDATORY before proposing or adding keywords

Never propose keywords from search volume alone. Volume without relevance buys
irrelevant clicks. Before suggesting or adding ANY keyword you MUST:

1. **Understand the product and confirm with the user** — what it does and *how*
   (e.g. AI vs OCR), its outputs (e.g. Excel), audience, and what it is NOT
   (e.g. no API). Inspect the landing page; when unsure, ASK.
2. **Pull the live ad's assets** (RSA headlines/descriptions + final URL) and
   check every candidate keyword is supported by the ad copy AND landing page.
3. If a cluster isn't supported, **exclude it or add supporting copy first**
   (`update_ad.py`) — never add unsupported keywords blind.
4. **Filter by intent** — freebie terms → negatives; wrong audience/tech
   mismatch → exclude.
5. **Dry-run → show plan → user confirms → apply.**

Full procedure: `reference/keyword-research-workflow.md`. This is a hard rule —
the "propose keywords blind" shortcut is exactly what it prevents.

### Red-flag rationalizations — STOP (keyword edition)

| Thought | Reality |
|---------|---------|
| "High volume, so add it." | Volume ≠ relevance. Check the product + ad copy first. |
| "It's roughly related." | If no headline/landing-page supports it, it won't convert. Exclude or add copy. |
| "I know what the product does." | Confirm with the user — assumptions here cost money. |

## Known gotchas (Google Ads API v25)

- **Check `customer.currency_code` FIRST.** All budgets/bids/metrics are in the
  account currency, not USD. (This account is MXN — a "131" bid = 131 pesos.)
- **`campaign.contains_eu_political_advertising` is REQUIRED on create**
  (`create_campaign.py` defaults it to DOES_NOT_CONTAIN). Enum name:
  `EuPoliticalAdvertisingStatusEnum`.
- **`campaign.start_date` / `campaign.end_date` are NOT valid GAQL field names.**
- Amounts are in **micros** (× 1,000,000); scripts convert automatically.
- Run scripts with the venv python (`~/.config/google-ads/venv/bin/python`); it
  forces the public certifi CA bundle (fixes corporate-network TLS, fails closed).

## Reference (load only when needed)

- `SETUP.md` — one-time credential/delegation setup.
- `reference/gaql-cookbook.md` — GAQL presets and ad-hoc queries.
- `reference/campaign-spec.md` — JSON schema for `create_campaign.py`.
- `reference/keyword-research-workflow.md` — MANDATORY keyword process (above).
- `reference/diagnostics.md` — "why zero/low metrics?" decision tree; automated
  by `diagnose_campaign.py`.

## Notes

- Amounts are entered in normal currency units; scripts convert to micros.
- Single-account setup: `login_customer_id` in the config is the target account.
- Errors surface as per-operation messages with field paths and actionable
  hints (see `_common.handle_google_ads_exception`).
