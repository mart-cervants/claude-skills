---
name: saleshandy-build-sequence
description: Use when the user wants to create, set up, or configure a Saleshandy outreach sequence/campaign. Applies cold-email best practices (step cadence, timing, deliverability formatting) by default and always confirms sequence/step/account choices explicitly with the user before creating anything.
---

# Saleshandy Build Sequence

## Overview

Builds a new sequence using `create_sequence`, `add_sequence_step`,
`add_step_variant`, and `update_sequence_schedule`, defaulting to the
cadence and deliverability practices in `reference.md` unless the user
specifies otherwise.

## Workflow

1. Confirm account health has been checked — run `saleshandy-account-health`
   first if it hasn't already happened in this conversation. Don't attach
   an unhealthy/unwarmed account to a new sequence.
2. Ask the user for the sequence goal/audience if not already clear (this
   frames subject lines and messaging — the ICP search itself is
   `saleshandy-find-leads`' job, not this skill's).
3. Propose a step plan using the cadence defaults in `reference.md` (4-5
   steps, 2-4 day gaps) — show it to the user before creating anything, and
   let them adjust step count/timing.
4. Call `create_sequence`, then `add_sequence_step` for each step in the
   agreed plan, then `update_sequence_schedule` for timing/send windows.
5. If the user wants A/B testing, use `add_step_variant` per step rather
   than creating parallel sequences.
6. Apply the deliverability defaults from `reference.md` (text-only
   formatting, unsubscribe link, personalization tokens) unless the user
   overrides them.
7. Before enrolling any leads (`add_leads_to_sequence` or
   `import_prospects_to_sequence_step`), explicitly ask which sequence and
   which step — even if this is the only sequence that exists and even if
   it was just created in this same conversation. Never default to step 1
   or infer the target from context.
   - **Tag + filter + enroll, without the manual UI's tag → move-to-CRM →
     saved-view steps.** `add_leads_to_sequence` takes `leadIds` +
     `sequenceId` + `stepId` and does the tagging (`newTags`/`tagIds`) and
     prospect creation itself — there's no MCP tool for "create a saved
     view," but the net result is the same. If the sequence copy depends on
     a field being non-empty (e.g. `{{Company Industry}}` merge tokens),
     filter the lead list down to rows where that field is populated
     *before* calling the tool, rather than trying to filter server-side.
     See `reference.md`'s "Filtering leads before enrollment" section.
   - Reminder: only leads already revealed via `enrich_contacts` actually
     get added — unrevealed leads are silently skipped server-side.
8. Leave the sequence paused/inactive until the user explicitly confirms
   they want it live.

## Example

User: "Set up a sequence for the fintech VP of Sales leads we just
verified"

→ confirm account health checked
→ propose: Step 1 (day 0, email) → Step 2 (day 3, email) → Step 3 (day 6,
email) → Step 4 (day 10, email) — 4 steps, 3-4 day gaps
→ user approves or adjusts
→ `create_sequence` → `add_sequence_step` x4 → `update_sequence_schedule`
→ ask which step to enroll the verified leads into (don't assume step 1)
