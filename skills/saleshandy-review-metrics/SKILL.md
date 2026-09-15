---
name: saleshandy-review-metrics
description: Use when the user asks how a sequence is performing, wants to review sequence metrics, or wants to optimize an underperforming sequence. Pulls get_sequence_stats/get_consolidated_stats and diagnoses the single most likely cause of underperformance using benchmark ranges, then recommends one concrete fix rather than a generic list.
---

# Saleshandy Review Metrics

## Overview

Turns raw sequence stats into a diagnosis and a single recommended next
action, using the benchmark table in `reference.md`.

## Workflow

1. Get the sequence(s) — call `list_sequences` if the user hasn't given an
   ID, and ask which sequence(s) if more than one is active and it isn't
   obvious from context.
2. Call `get_sequence_stats` for a single sequence, or
   `get_consolidated_stats` for multiple sequences over a time period.
3. Compute the key ratios: open rate, reply rate, bounce rate, click rate
   (if links are used).
4. Compare each against the benchmark table in `reference.md` and identify
   the WORST outlier — the metric furthest below (or above, for bounce) the
   healthy range. That's today's diagnosis.
5. Map that outlier to its likely cause and ONE concrete fix from
   `reference.md` — don't dump the whole reference table on the user, just
   the relevant row(s).
6. If bounce rate is the outlier, treat it as urgent: recommend pausing the
   sequence and re-running `saleshandy-verify-emails` on the list before
   anything else, since continuing to send makes account health worse.
7. If the user wants to act on the recommendation (e.g. edit a step, adjust
   timing), hand off to `saleshandy-build-sequence` for the actual edit
   rather than mutating steps directly from this skill.

## Example

User: "How's my fintech sequence doing?"

→ `get_sequence_stats`
→ open rate 58% (healthy), reply rate 0.8% (below 1-3% healthy range),
bounce rate 0.9% (healthy)
→ Diagnosis: opens are fine, so subject lines/deliverability aren't the
problem — replies are low, which points to messaging/offer relevance, not
visibility.
→ Recommendation: "Reply rate is the weak point, not opens. Worth testing a
step variant with a more specific/relevant offer or a clearer single ask —
want me to draft one via saleshandy-build-sequence?"
