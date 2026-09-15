# Verify Emails — Reference

## Credit costs

- `reveal_phone: false` → ~1 credit/lead (email only)
- `reveal_phone: true` → ~7 credits/lead (email + phone)

For large batches, default to email-only unless the user has explicitly
asked for phone numbers — don't spend 7x the credits speculatively.

## Batching

- `enrich_contacts` and `enrich_companies` both cap at 100 records per call.
- Never split into multiple calls to work around the cap, and never loop
  calls to exceed it. If the user has more than 100 leads to verify, verify
  the first 100 (or let the user pick which 100) and tell them explicitly
  that larger batches must be done in the Saleshandy web app.

## DNC / suppression ordering

Always check DNC status BEFORE spending credits on a reveal where possible
(i.e. when an email/domain is already known). If a reveal happens first and
the resulting email matches a DNC entry, tell the user immediately — do not
add that lead to a sequence, and offer to add it via `add_dnc_items` if it
isn't already tracked under the reason it surfaced.

## Bounce risk

Emails Saleshandy could not verify as deliverable (or that come back as
role-based/catch-all addresses) increase bounce risk. A sequence's overall
bounce rate above 2% risks the health of every email account sending it
(see `saleshandy-account-health`). When in doubt, exclude rather than
include.
