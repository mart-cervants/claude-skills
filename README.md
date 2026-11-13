# claude-skills

Personal collection of [Claude Code](https://docs.claude.com/en/docs/claude-code) skills, packaged as a plugin.

## Install

```
/plugin marketplace add <this-repo-url>
/plugin install claude-skills
```

Or, for local development without publishing anywhere, symlink individual skills into `~/.claude/skills/`:

```
ln -s "$(pwd)/skills/<skill-name>" ~/.claude/skills/<skill-name>
```

## Skills

| Skill | What it does |
|---|---|
| `social-brand-kit` | Set up and locate the per-project brand kit (brand profile, voice, guardrails, pillars, visual tokens, inspiration) by reading a website, social page or description; shared anti-slop quality rules (general + per-language packs). |
| `content-ideas` | Build a sourced, scored, format-aware backlog of post ideas for any brand from the user's raw inputs, conversations, guided research and analyzed inspiration (no ideas without a source; patterns, never copied content). |
| `facebook-page-content` | Plan, write, review and schedule Facebook Page posts for any brand (monthly calendar, copy in the brand voice and language, anti-slop gate) via the Metricool MCP; nothing goes out unapproved. |
| `social-visuals` | On-brand social images for any brand from its kit tokens: Playwright-rendered HTML cards (exact text and logo) plus optional text-free AI artwork via an image MCP such as Higgsfield. |
| `google-ads-manager` | Create, update, report on, and manage Google Ads campaigns/ad groups/keywords/budgets via the official API client, with a mandatory dry-run-before-spend safety gate. |
| `saleshandy-account-health` | Check Saleshandy email account/domain warmup status and deliverability readiness before sending. |
| `saleshandy-build-sequence` | Create and configure Saleshandy outreach sequences with cold-email best practices baked in. |
| `saleshandy-check-inbox` | Triage the Saleshandy unified inbox and draft/send replies with explicit confirmation. |
| `saleshandy-find-leads` | Find prospects/companies matching an ICP via Saleshandy Lead Finder. |
| `saleshandy-review-metrics` | Diagnose underperforming sequences from stats and recommend a concrete fix. |
| `saleshandy-verify-emails` | Verify/reveal lead emails and check DNC suppression before outreach. |
| `trulyinbox-manager` | Read-only warmup/deliverability/DNS health reporting for TrulyInbox-managed email accounts. |

Each skill's `SKILL.md` documents its own setup (API keys, config file locations, etc.) — none of that lives in this README to avoid duplication drift.
