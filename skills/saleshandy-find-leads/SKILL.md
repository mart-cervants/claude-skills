---
name: saleshandy-find-leads
description: Use when the user wants to find prospects, leads, or companies matching an ICP via Saleshandy Lead Finder — e.g. "find leads", "find my ICP", "prospect for X", "who should I target". Always asks for target criteria fresh (no stored default ICP) before calling sage_search, and hands revealed lead IDs to saleshandy-verify-emails as the next step.
---

# Saleshandy Find Leads

## Overview

Wraps `sage_search` (Saleshandy's Lead Finder AI search) with a consistent
intake and refinement loop. No default ICP is stored — always ask fresh,
since the target varies by campaign.

## Workflow

1. Ask the user for ICP criteria if not already given: role/title, industry,
   company size, geography, and anything else relevant (tech stack, funding
   stage, etc.). Don't interrogate if the request already covers most of
   this (e.g. "SaaS CTOs in Europe, 50-200 employees" needs no follow-up
   question).
2. Call `sage_search` with a natural-language query built from those
   criteria. Leave `limit` unset (defaults to 25) unless the user explicitly
   asks for more.
3. Present results along with the `agentMessage` context Sage returns — it
   often surfaces inferred filters; check these actually match what the user
   meant.
4. If the user wants to refine ("only SaaS", "remove companies in the US"),
   reuse the same `conversationId` from the previous `sage_search` call
   rather than starting a fresh search.
5. Once the user is happy with the list, tell them the next step is
   verifying emails — hand the lead IDs off to `saleshandy-verify-emails`.
   Don't reveal contacts here; that's a separate credit-consuming step the
   user should explicitly trigger.

## Example

User: "Find me VP of Sales at Series B fintech startups in the US,
50-200 employees"

→ `sage_search(query="VP of Sales at Series B fintech startups in the
United States, 50-200 employees")`
→ present results, note the lead IDs
→ "Found 25 matches. Want me to verify emails for these before adding them
to a sequence?"
