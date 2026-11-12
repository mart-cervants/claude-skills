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

## 5. Confirmed on first connection (2026-11-11, Free plan)

Tools exposed by the Metricool MCP: `getBrandSettings`, `getScheduledPosts`,
`getBestTimeToPostByNetwork`, `createScheduledPost`, `createScheduledPostForReview`,
`sendScheduledPostForReview`, `updateScheduledPost`, `getAnalyticsAvailableMetrics`,
`getAnalyticsDataByMetrics`.

- **Media must be public URLs** (`info.media`). External Google Drive/Dropbox links
  are auto-uploaded; there is no local file upload. Host images publicly first
  (see `social-visuals/SETUP.md`, "Public URLs for scheduling").
- **Drafts:** `createScheduledPost` takes `info.draft = true`. Use this for the
  approval step on the Free plan.
- **"For review" needs a plan with team management** (`createScheduledPostForReview`,
  `sendScheduledPostForReview`; reviewers are emails). Don't rely on it on Free.
- **`updateScheduledPost` overwrites immediately** and changes the post `id` (the
  `uuid` is stable). Resend the full original content, changing only what's needed.
- **First comment:** `info.firstCommentText` exists (useful to test link in the
  first comment).
- **Facebook post type:** `info.facebookData.type` = `POST`, `REEL` or `STORY`
  (Reels need a video; Stories need image or video). Always include
  `facebookData` for Facebook posts.
- **Time zone:** use the brand's IANA zone from `getBrandSettings`
  (DataNode's brand is `America/Monterrey`, same offset as Mexico City).
- **Best times** (`getBestTimeToPostByNetwork`, network `facebook`) returned data
  on a brand with no posts yet, so treat it as a general benchmark until the Page
  has its own history. In the first check it peaked around 10:00 and 12:00 on weekdays.

## 6. Still to confirm (then write the answer here)

- [ ] Draft posts: do they appear in the Metricool planner as drafts and stay
      unpublished until approved/scheduled by hand?
- [ ] Does a public image URL attach correctly (try a card hosted on the brand's site)?
- [ ] Does scheduling beyond 30 days work for Facebook through Metricool?
- [ ] Does `autoPublish: true` publish at the scheduled time (watch the first one)?

## Sources

- https://help.metricool.com/mcp-limits-and-plan-requirements-h72jg
- https://help.metricool.com/more-scheduling-options-with-metricools-mcp-ylkdd
- https://help.metricool.com/how-to-connect-metricools-mcp-with-claude-0l84v
- https://metricool.com/metricool-mcp-claude/
