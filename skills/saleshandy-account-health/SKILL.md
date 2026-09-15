---
name: saleshandy-account-health
description: Use before building or launching a Saleshandy sequence, or when the user asks to check email account/domain health, warmup status, or sending readiness. Checks list_email_accounts and get_email_account_stats against deliverability thresholds and flags accounts that aren't ready to send.
---

# Saleshandy Account Health

## Overview

Pre-flight check run before `saleshandy-build-sequence`. Verifies that the
email accounts about to be attached to a sequence are healthy enough to send
cold outreach without hurting deliverability for every account on the domain.

## Workflow

1. Call `list_email_accounts` to get all connected accounts (filter to
   specific ones if the user named them).
2. For each account, call `get_email_account_stats`.
3. For each account's sending domain, run a DNS authentication check via
   `dig` (no Saleshandy API call needed):
   ```bash
   dig +short TXT <domain>                       # SPF — look for "v=spf1"
   dig +short TXT _dmarc.<domain>                 # DMARC — look for "v=DMARC1" and check the p= value
   dig +short TXT google._domainkey.<domain>      # DKIM (Google Workspace default selector)
   dig +short MX <domain>                         # confirms mail is actually routed where expected
   ```
   - SPF missing, or DKIM missing entirely → hard flag, this is a real
     deliverability blocker, not just hygiene.
   - DMARC missing entirely → flag (Gmail/Yahoo's bulk-sender rules require
     a DMARC record to exist at all).
   - DMARC present with `p=none` → flag as weak/monitoring-only, not a
     blocker by itself, but recommend tightening to `p=quarantine`.
   - If the DKIM selector isn't `google._domainkey` (e.g. non-Google ESP),
     note that the correct selector depends on the provider and ask the
     user rather than guessing.
   - **Clean SPF/DKIM/DMARC does NOT mean an account is deliverable** — if
     Inbox Radar/bounce data still shows poor placement despite clean DNS,
     say so explicitly and point to reputation/engagement (low
     opens/clicks/replies relative to volume) as the likely cause instead,
     rather than implying DNS is the whole story.
4. Compare against the thresholds below and produce a table: account,
   warmup status, bounce rate, DNS auth status, health verdict.
5. If any account fails a threshold, tell the user explicitly and recommend
   NOT attaching it to a new sequence yet — do not silently proceed anyway.

## Real inbox-placement testing (not just DNS)

Clean SPF/DKIM/DMARC (step 3 above) is necessary but not sufficient —
confirmed twice on this account: clean auth + low SpamAssassin content
score (0.1) still landed 100% spam at Gmail/Outlook/Hotmail/AOL and only
~30% inbox at Google Workspace, while smaller/business ESPs (Zoho, gmx,
Proton, O365, WorkMail) delivered 100% to inbox. That pattern — clean
tech, clean content, still spam-flagged specifically by the big consumer
ISPs — is the signature of a **sender-reputation/engagement problem**,
not a config problem. Two free tools give this real per-provider
placement signal (neither is a Saleshandy API call):

- **GlockApps** (glockapps.com) — free spam checker, shows inbox
  placement across Gmail/Yahoo/AOL/Outlook plus SpamAssassin score,
  50+ blocklist checks, and auth verification in one report.
- **Saleshandy's own Inbox Radar** (in the web app, not exposed via
  MCP) — same category of test, but the free tier is 1 test total, not
  recurring. Don't burn it on a test that could be done via GlockApps
  first.

**Seed-list testing hygiene** (learned the hard way — don't repeat):
- Send to seed addresses individually or in batches of ≤25, never one
  email with dozens of addresses in the `To:` field — SpamAssassin's
  `KAM_MANYTO` rule penalizes bulk-`To:` sends, which skews the score
  and isn't representative of how Saleshandy actually sends (1:1 per
  contact).
- A seed-list test only validates sequence-level settings (like
  `unsubscribe-via-email-header`) if the email is actually sent through
  Saleshandy's sending engine. A manually composed/copy-pasted test
  email bypasses that engine entirely and will show settings as "off"
  even if they're correctly configured in the sequence — that's a test
  artifact, not a real finding.

## Rebuilding reputation when placement is bad but DNS is clean

If DNS is clean (step 3) but real placement testing (above) still shows
heavy spam-folder placement at major ISPs, the fix is reputation/
engagement-based, not configuration-based. In order of effort:

1. **Check warmup status via the `trulyinbox-manager` skill, not the
   `ramp-up-*` fields.** Saleshandy's actual warm-up engine is a partnered
   third-party app, TrulyInbox — NOT the `ramp-up-status`/`ramp-up-limit`/
   `ramp-up-percent` fields inside `list_email_accounts`'s `settings`
   array. Confirmed by direct comparison: an account with
   `ramp-up-status: "0"` was still shown as "Protected — Active Warmup" in
   TrulyInbox. Don't use the Saleshandy-native fields as a warmup signal —
   run `trulyinbox-manager/scripts/check_health.py --email <address>`
   instead (it calls TrulyInbox's Open API directly: warmup status/
   settings, setup score, DNS health, and deliverability-by-ESP in one
   report). Only fall back to asking the user to check the TrulyInbox web
   dashboard by hand if that script errors (e.g. API key not set up yet —
   see that skill's `SETUP.md`).
   - **TrulyInbox's own "Deliverability %" is a warmup-network-internal
     metric** (other warmup accounts opening/replying to each other), not
     a substitute for real seed-list placement testing. Confirmed
     directly: an account showed 83% on TrulyInbox while GlockApps' real
     seed-panel test on the same account showed ~27% actual inbox
     placement at real ISPs. Warmup being active and scoring well
     internally does NOT mean real cold-send placement is fixed — still
     check GlockApps/Inbox Radar to know the real number.
   - If an account shows "At Risk"/warmup disabled in TrulyInbox,
     recommend enabling it there before using that account for any
     sequence, live or planned.
2. **Set up Google Postmaster Tools** (postmaster.google.com) now, even
   if current volume is below the ~100-200/day threshold needed for data
   to populate — free, one-time DNS verification, and it starts
   capturing data as soon as volume increases rather than losing more
   time later.
3. **Cut cold-sending volume on the affected account** while reputation
   rebuilds — don't scale up sends hoping volume fixes reputation; it's
   the opposite relationship.
4. Re-test placement (GlockApps, batched properly per the hygiene note
   above) after a reputation-rebuilding period, not immediately.

## Thresholds

- **Warmup age:** >= 14 days since the account started warmup before sending
  cold (non-warmup) email. Under 14 days → flag as "still warming up."
- **Bounce rate:** < 2%. Above 2% → flag as a list/account health risk and
  recommend pausing sends from that account until investigated.
- **Daily sending volume:** should stay within the account's configured
  daily cap (visible in `get_email_account_stats`). Never recommend raising
  the cap as a fix for low volume — raising limits on an unhealthy account
  makes deliverability worse, not better.
- **Spam complaint rate:** > 0.1% is a hard stop — recommend removing the
  account from active sequences.

## Tracking settings (open/click) gate on account health

`track-email-opens` and `track-link-clicks` (sequence settings codes 5 and
4, via `get_sequence_settings`/`update_sequence_settings`) are a known
deliverability tradeoff — Saleshandy's own UI warns that tracking can push
mail into Promotions or Spam. That tradeoff is only acceptable once the
account is healthy:

- If any attached account fails the Inbox Score / bounce-rate thresholds
  above, recommend **leaving tracking OFF** — turning it on adds a second
  variable on top of an already-failing account, and open-rate data from a
  spam-flagged account is noise, not signal, since you can't tell whether a
  bad number next week came from tracking or from the underlying
  reputation problem.
- Once an account's Inbox Score/placement is confirmed healthy (re-run the
  Inbox Radar test, don't rely on a stale result — check the test's run
  date), tracking can be turned back on. `saleshandy-review-metrics`
  depends on open-rate data for its benchmark table, so tracking needs to
  be on eventually — just not while the account is still unhealthy.

## Output

Always end with one of:

- "All N accounts are healthy — safe to proceed to sequence build/launch."
- "N of M accounts are NOT healthy: [list + reason]. Recommend [pausing /
  continuing warmup / investigating] before using them in a new sequence."

Never make the health call implicitly as part of another task — always
surface it as an explicit verdict the user sees before moving on to
`saleshandy-build-sequence`.
