# Setup — facebook-page-content

## 1. Brand kit

Needs a brand kit for the project (`social-brand-kit` creates it). The skill
finds it via a `Social brand kit: <path>` line in the project's `CLAUDE.md`, or
`marketing/social/` by default.

## 2. Connect the Metricool MCP

Metricool's official MCP works on **any plan, including Free** (Free: 1 brand,
20 scheduled posts/month, 30 days of analytics, Facebook included).

Endpoint (from Metricool's docs): `https://ai.metricool.com/mcp`

```bash
claude mcp add --transport http metricool https://ai.metricool.com/mcp
```

Then run `/mcp` inside Claude Code, pick `metricool`, and authenticate (OAuth in
the browser) with the Metricool account that owns the brand's Page. A token
connection also exists via `METRICOOL_USER_TOKEN` and `METRICOOL_USER_ID`
(Account settings); that path may require a paid plan.

Verify: ask Claude to "list my Metricool brands" and "show scheduled posts".

## 3. Link the Facebook Page in Metricool

Create a brand in Metricool and connect the Page. Posts can only be scheduled
to networks connected there.

## 4. Machine and network

Use the machine and network the project's `guardrails.md` designates (corporate
proxies can log or block traffic).

## 5. Confirm on first use (then write the answers here)

- [ ] Does the MCP accept images as public URLs only, or can it upload files?
- [ ] How do "for review" posts behave — do they stay unpublished until approved?
- [ ] Does scheduling beyond 30 days work for Facebook through Metricool?
- [ ] Time zone handling: do posts land at the intended local time?

## Sources

- https://help.metricool.com/mcp-limits-and-plan-requirements-h72jg
- https://help.metricool.com/more-scheduling-options-with-metricools-mcp-ylkdd
- https://metricool.com/metricool-mcp-claude/
