---
name: saleshandy-verify-emails
description: Use when the user wants to verify, reveal, or check emails for a list of leads before outreach — e.g. "verify these emails", "reveal contacts", "check bounces", "get emails for these leads". Reveals contact info via enrich_contacts and checks DNC suppression before/after reveal to avoid wasting credits and protect deliverability.
---

# Saleshandy Verify Emails

## Overview

Converts a lead list (from `saleshandy-find-leads` or supplied directly)
into verified, sendable contacts — checking DNC suppression and respecting
credit costs along the way. See `reference.md` for credit-cost and batching
details.

## Workflow

1. Get the lead list: `lead_id[]` from a prior `sage_search`, or
   `linkedin_url[]` / `full_name_with_company[]` if supplied directly.
2. Ask the user: email only, or email + phone? Map "email" / no preference
   → `reveal_phone: false`; "phone" / "email and phone" → `true`. If
   ambiguous AND the batch is large, confirm before burning phone credits
   (7x more expensive — see `reference.md`).
3. If the user already has known emails/domains (not going through a
   reveal), check them against DNC first via `search_dnc_item(type="email")`
   before doing anything else — no point verifying or enrolling a suppressed
   contact.
4. Call `enrich_contacts` with up to 100 IDs per call (hard cap — see
   `reference.md` for how to handle more).
5. Poll `get_enrichment_status` until `completed`, then call
   `get_enrichment_result`.
6. Report: how many revealed successfully, how many failed/had no email
   found, and flag any that matched a DNC list.
7. If a revealed contact looks like a hard bounce risk (Saleshandy reports
   it as unverifiable), recommend excluding it rather than enrolling it,
   since bounces hurt account health (see `saleshandy-account-health`
   thresholds).

## Handoff

End by asking whether to proceed to `saleshandy-build-sequence` (or
`add_leads_to_sequence` into an existing one) with the verified list —
restate the mandatory gate: always ask the user which sequence AND which
step; never default or infer either, even if only one active sequence
exists.
