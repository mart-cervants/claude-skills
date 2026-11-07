# Discovering a brand from a website, page or description

Goal: draft `brand-profile.md` (and seed voice/visuals) from public sources,
then confirm with the user. Mark every statement **Inferred** or **Confirmed**.

## Sources, in order of reliability

1. **Website (best).** Public, structured, and usually current. Read the home
   page, About, services/products, pricing (if public), contact, FAQ, and the
   page metadata (title, description). Note the language and tone of the copy,
   the headline claims, and the calls to action.
2. **Visual cues from the website.** Logo, color palette (from CSS or the
   rendered page), fonts, image style. Extract exact values when possible
   (CSS variables, theme config); otherwise describe and ask.
3. **Social page (Facebook, Instagram, LinkedIn…).** Often login-walled. Try the
   public view; if it can't be read, **don't bypass the login** — ask the user
   to paste the About text, the category, and 5–10 recent posts (with their
   reach/engagement if known).
4. **The user's description.** Always ask for it, even briefly: audience,
   offer, what makes them different, what they want from social media.

## Tools

- Use web fetching or a browser (Playwright) for public pages. If the site
  blocks automated access or is login-gated, say so and ask the user to paste
  content.
- Work from a personal machine/network if the project is personal or
  confidential (corporate proxies may log or block traffic).

## What to extract into `brand-profile.md`

| Field | Notes |
|---|---|
| Brand name, one-line description | In the brand's words |
| Language and market | Ask; never assume |
| Audience | Who buys, their situation, their words for the problem |
| Offer | Products/services, what is NOT offered, prices only if public |
| Differentiators | Evidence-backed only |
| Goals for social | Leads, bookings, awareness, community, sales |
| CTAs and links | Canonical link(s), booking/contact channels |
| Channels | Pages/accounts, handles, which are active |
| Proof available | Real clients, testimonials, numbers — **only what exists**; none is a valid answer |
| Constraints | Confidentiality, legal, regulated claims, things never to mention |
| Competitors/adjacent accounts | For format inspiration only |

## Questions to ask when information is missing

1. Who exactly is the customer, and what problem do they say out loud?
2. What are you NOT willing to say or show publicly?
3. What do you have as proof today (clients, results, certifications)? If
   nothing yet, we write without it.
4. What action should a post push: message, book, visit, buy?
5. Which 3 accounts do you admire for tone, and which 3 posts do you wish you'd written?
6. How often can you realistically publish and reply to comments?

## Output

- `brand-profile.md` filled, with Inferred/Confirmed tags and TODOs.
- A short list of open questions for the user.
- Draft `voice.md`, `visual-identity.md`, `tokens.json` (colors/fonts from the
  site when found).
