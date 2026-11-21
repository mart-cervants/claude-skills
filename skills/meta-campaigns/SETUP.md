# Setup — meta-campaigns

## 1. Brand kit and `ads.md`

Needs the project's brand kit (`social-brand-kit`) and an `ads.md` next to it
(`reference/ads-template.md`). The ad account id declared there is the only
account the skill will operate on.

## 2. Meta Ads MCP (user-level, shared by all projects)

The MCP is configured once at **user scope**, so every project can use it. Because
it is global, one login may reach several businesses' ad accounts: the skill's
account check (id and name against `ads.md`) is the guard. Never rely on the
"default account" the server picks.

Meta's remote MCP for ads is an HTTP server (OAuth in the browser, no headers
or env vars needed). Check what is configured, in a terminal, from the project
where it works:

```bash
claude mcp list
claude mcp get meta-ads        # shows Scope: Local | Project | User
```

Add it at user scope:

```bash
claude mcp add --scope user --transport http meta-ads https://mcp.facebook.com/ads
```

If an old **local** (per-project) entry exists, it takes precedence in that
project and hides the user-level one. After the user-level one works, remove the
old one from that project:

```bash
cd <that-project> && claude mcp remove meta-ads -s local
```

Then restart the session, run `/mcp`, authenticate if required, and verify:
"list the ad accounts this MCP can access" — the project's account (and only
what you expect) should appear. Keep tokens out of `ads.md`, the repo and chat;
store them in the MCP's own auth or environment.

If a project must never see a given account, restrict it at the source (the
Business Manager / token permissions), not just in prompts.

## 3. Prerequisites for a new brand (Meta side)

- Business Manager / business account, ad account in the right currency, Page linked.
- Business verification is **optional to start**: Meta requires it for some features (e.g. higher spending limits, certain APIs, regulated categories) and can ask for it automatically. It needs business documents and can take up to ~14 business days. Don't make it a prerequisite for a small test; do it when Meta asks or a feature needs it. A paused or restricted account is the risk of not having it.
- Payment method and a spending limit.
- Tracking for the chosen event (pixel and/or Conversions API); consent behavior
  decided. Not needed for messaging objectives.
- A destination that works on a phone (WhatsApp link, booking page).

## 4. Machine and network

Use the machine and network the project's `guardrails.md` designates (corporate
proxies can log or block traffic; don't operate ad accounts from them).

## 5. Tool names

Names differ between MCP servers and change. At the start of a run, list the
tools actually available and map them to: read account, read campaigns/ad sets/
ads, insights, create campaign/ad set/ad, update status, update budget. If the
server has no way to create things paused, build in the interface instead.
