---
name: saleshandy-check-inbox
description: Use when the user wants to check the Saleshandy unified inbox, see unread prospect replies, or respond to a prospect message — e.g. "check inbox", "any replies", "unread messages". Triages unread threads and drafts or sends replies with explicit user confirmation before anything is sent.
---

# Saleshandy Check Inbox

## Overview

Simple triage loop over the unified inbox: how many unread, what they're
about, and help draft/send replies.

## Workflow

1. Call `get_unread_email_threads_count` first — a quick "you have N
   unread" beats immediately dumping a full thread list.
2. If N > 0, call `get_email_list` (or `get_email_thread` for a specific
   thread the user names) to see who replied and a snippet/summary.
3. Summarize each unread thread in one line: sender, sequence context if
   available, and what they're asking/saying (interested, objection,
   out-of-office, unsubscribe request, etc.).
4. Flag anything that looks like an unsubscribe/opt-out request explicitly
   — recommend adding that contact to a DNC list (via
   `saleshandy-verify-emails`' DNC tooling) rather than just replying.
5. If the user wants to respond, draft the reply text and show it to them
   before calling `reply_to_email` — never send a reply without the user
   seeing and approving the exact text first, even for a short one-liner.
6. After sending, mark progress conversationally — don't call
   `complete_task`/`skip_task` unless the user is also using Saleshandy's
   Tasks feature and explicitly asks; that's out of scope for this skill.

## Example

User: "Check my inbox"

→ `get_unread_email_threads_count` → "3 unread"
→ `get_email_list` → summarize: "1) Jane at Acme asked for pricing, 2) Tom
unsubscribed, 3) auto-reply OOO from Priya"
→ "Want me to draft a reply to Jane, and should I add Tom to the DNC
list?"
