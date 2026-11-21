# Metrics and thresholds

Decide with numbers set **before** spending. Everything here is a method; the
values (margin, ticket, close rate, minimum data) are written in the project's
`ads.md`, with assumptions labeled as such and replaced by real data as it comes.

## 1. Economics (from the user, or labeled assumptions)

| Input | Meaning |
|---|---|
| Ticket | Revenue per customer for the first sale (or first month) |
| Gross margin | Share of revenue left after the cost of delivering it |
| LTV | Gross profit per customer over their lifetime (not revenue). Use a conservative horizon (e.g. 12 months) |
| Funnel rates | conversation → booked call → proposal → customer, each as a rate |

Derived:

- **Max CAC (break-even)** = gross profit per customer (first sale only if
  repeat is uncertain; LTV if recurrence is proven).
- **Target CAC** = LTV ÷ target ratio. A common orientation is **LTV:CAC ≥ 3**;
  a lower ratio can be acceptable early but must be a decision, not an accident.
- **Break-even ROAS** = 1 ÷ gross margin (e.g. 40% margin → 2.5). ROAS above
  that makes money on the first sale; below it loses on the first sale.
- **ROAS** = revenue attributed ÷ ad spend. Meaningful only when sales are
  attributed reliably; for services sold by conversation it is usually unreliable
  → use cost per stage instead.

## 2. Cost per stage (the usable chain for service businesses)

```
CAC = cost per conversation
      ÷ (conversation→call rate × call→customer rate)
```

Work backwards to the **break-even cost per conversation**:

```
break_even_cost_per_conversation = max_CAC × conversation→call × call→customer
```

Example of the form only (replace with the user's numbers): if max CAC is 6,000
and 10% of conversations become a call and 25% of calls close, a conversation can
cost at most 6,000 × 0.10 × 0.25 = 150. If the real cost is above that, scaling
loses money no matter how good the CTR looks.

Early on the rates are guesses. Mark them **assumption**, and update after
every ~10–20 conversations handled.

## 3. Metrics: what each is for

| Metric | Reading | Caution |
|---|---|---|
| Cost per conversation / lead / booked call | **Success metric** (one, chosen in `ads.md`) | Quality varies; sample the actual conversations |
| Link CTR (outbound/link clicks ÷ impressions) | Message–audience fit, creative pull | Not all-clicks CTR; high on mobile/Reels can be accidental taps |
| CPM | Auction cost / audience competition | Not good or bad alone; explains cost changes |
| Frequency | Fatigue and saturation | Rising frequency + falling CTR = refresh creative |
| Cost per link click, cost per landing-page view | Diagnostic of the click→load path | Clicks ≫ landing views = slow/blocked page or in-app browser issue |
| Landing views ÷ link clicks | Loss between click and page | Low ratio → fix the page before the ad |
| Cost per result of the downstream step (call booked, proposal) | Real efficiency | Tiny samples; use with the funnel rates |
| LTV:CAC, CAC | Business outcome | Only after real customers exist |
| Delivery share per ad set/ad | **Is the test valid?** | Check first, before reading any other metric |

## 4. Minimum data before judging (framework, orientation values)

Set explicit numbers per ad set in `ads.md`. Source column matters: only the
rows marked **Meta** come from Meta's help center (checked 2026-11-20); the
rest are rules of thumb of this skill, not facts. Adjust them to the account.

| To judge… | Roughly need | Source / note |
|---|---|---|
| Delivery working | Spend near the planned daily amount, every ad set delivering | Skill. If not, fix before judging |
| CTR / CPM direction | ~1,000+ impressions and ~100 link clicks per ad set | Skill rule of thumb. Below this, differences are noise |
| Cost per conversation between two angles | ≥ ~20–30 conversations each, and a gap far bigger than the noise | Skill rule of thumb. With small budgets you often can't reach this → "inconclusive" or judge only leading indicators and say so |
| Optimization stability ("learning") | "About 50 results in the week after the ad set's last significant edit" to exit the learning phase | **Meta** ("About the learning phase"). Below it the status is "Learning limited"; expect higher, volatile cost |
| Remarketing audience | The size the interface shows for the audience; ~100 people/events is a common floor | **Not verified** in Meta's help center; the interface is the authority |

Meta also states: during learning, performance is less stable and CPA usually
higher; "avoid high ad volumes" (many ads/ad sets teach the system less about
each) — which is the real tension with one-ad-set-per-angle: keep the angle
count as low as the question allows.

If the budget cannot reach the minimum for a conclusion on the success metric,
do not pretend it can. Either: lower ambitions (rank angles on CTR + cost per
landing view only, label it directional), raise the budget, or run fewer angles.

**Time:** judge after the planned window, never on days 1–3. Whole weeks.
**Statistics:** with counts this small, two numbers 20% apart are usually not
different. Prefer "directionally better, not proven".

## 5. Pre-registered decision record (put in `ads.md` before launch)

```
Success metric: ...
Window: ... to ...
Minimum data per ad set: impressions ..., link clicks ..., conversions ...
Continue if: ...
Stop if: cost per result > ... after ... impressions/days
Scale if: cost per result ≤ ... with ≥ ... results, step size ...
Inconclusive if: minimums not met → action: ...
```

## 6. Cross-checks that prevent self-deception

- Compare platform numbers with **own analytics** (UTM on every ad link:
  `utm_source`, `utm_medium`, `utm_campaign`, `utm_content` = angle id).
- Compare landing views (platform) with sessions (own analytics): gaps mean
  tracking or load problems.
- Look at the **step after the click**: device mix, in-app browser behavior,
  scroll, CTA clicks, conversations actually started.
- Read a sample of the real conversations/leads for quality, not just count.
- Attribution windows and modeled conversions make platform conversion counts
  differ from your own; reconcile before reporting CAC.
