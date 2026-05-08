# Marketing guest-posting — extended stages 5–8 + edge cases

Detailed reference for stages 5–8 of the workflow, decision-guide edge cases, Google's position, and tool inventory. SKILL.md keeps the workflow outline and stages 1–4 detail; load this file when executing stages 5–8 or hitting an edge case.

## Stage 5 — Pitch architecture (the 80–150-word email)

Pitch performance data:
- Personalized pitch = 18% reply vs 6% generic (3× difference)
- Length: 80–150 words, no longer
- Subject line: specific, references their content, not generic
- Body structure (in order): personalization hook → credibility line → 3 topic offers → soft CTA

Architecture:

```
SUBJECT: [Specific reference to a recent post + 4–6 word topic suggestion]
   GOOD: "Loved your CI piece — pitch on monorepo trade-offs?"
   BAD: "Guest post pitch for [publication]"
   BAD: "Quick question"

OPENING (1–2 lines) — Personalization hook tied to a SPECIFIC article they published.
   Reference the title or a specific point. Not "love your blog" — "your piece on X
   made me rethink Y."

CREDIBILITY (1 line) — One sentence on who you are, why you can write on this.
   Name 1–2 prior placements (with link), or your specific expertise/data.

TOPIC OFFER (the meat — 3–5 lines) — 3 specific topic ideas, each one sentence,
   each addressing a content gap on their site. Title + value prop.

CTA (1 line) — Soft. "Happy to send a draft outline if any of these fit."
   NEVER "let me know what you think" or "if interested, please reply."

SIGN-OFF — Name. One link. Done.
```

Length math: subject ~10 words; opening ~25 words; credibility ~25 words; topic offers ~50 words; CTA ~10 words; signature ~5 words = ~125 words. Stay in this range.

Pitch template (brief — not a finished email):

```
Subject: [Reference to specific post they wrote] — [topic suggestion in 4-6 words]

Hi [Editor first name],

Your [post title or specific point] last [time-frame] got me thinking about [related angle]. Specifically, the part where you mentioned [specific quote/idea] — I think there's a follow-up that would resonate with [audience descriptor].

I'm [credibility — role + 1 prior tier-comparable placement OR specific original asset]. A few topics I could write that I think would fit:

  • [Topic 1 title] — [one-sentence value prop tied to their audience]
  • [Topic 2 title] — [one-sentence value prop]
  • [Topic 3 title] — [one-sentence value prop]

Happy to send a detailed outline if any of these fit your editorial calendar.

— [Name]
[One link, branded]
```

Pre-pitch relationship-building (multiplier):

For T1/T2 (acceptance <20%), do this BEFORE the pitch over 2–4 weeks:
- Share their content 2–3× on social with your own thoughtful comment
- Leave 1–2 substantive comments on their recent posts (not "great article!")
- Send one appreciation email — no pitch, just thank them for a specific piece
- Reference all of this implicitly in the eventual pitch

This moves T1/T2 acceptance rates from 5% to 20%+.

## Stage 6 — Writing standards by tier

Match the tier:

Tier-1 standard:
- "As good or better than what you post on your own blog"
- 2,500–4,000 words; longer is fine if substantive
- Actionable system, not summary — step-by-step process the reader can apply
- Custom screenshots, charts, original data
- Search-intent match — readers should find it via target queries
- Original quotes (not just citations) where possible
- Internal linking to host site's own relevant content (3–5 internal links)

Tier-2 standard:
- 1,500–2,500 words
- Case study or process post format works well
- Visuals required but can be lighter
- Internal linking to host site (2–3 links)

Tier-3 standard:
- 1,000–1,500 words
- Substantive but doesn't need T1 production polish
- 1–2 internal links to host site

Tier-4 standard:
- 800–1,200 words
- Solid contribution, simpler structure

Universal rules across all tiers:
- Original — never duplicate published-elsewhere content
- Human-written — AI-content farms are a tagged violation category (Oct 2025 update)
- Match the publication's voice (read 5 of their posts before writing)
- Lead with the value, not the setup
- No promotional content for your own product/service in the body

Output of Stage 6: an outline + post-writing brief (target word count, format, voice notes, internal-link list). Actual prose generation is out of scope for this skill.

## Stage 7 — Link strategy (placement + anchors)

This is where penalty risk is highest.

Link placement:

| Link type | Count | Placement | Notes |
|---|---|---|---|
| Body link (preferred) | 1–2 | Inside the article body, contextually relevant | 387% more referral traffic than bio-only |
| Author bio link | 1 | In bio top or bottom | Standard; usually nofollow |
| In-content related link | 0–1 | Linking to host's other content | Signals editorial care |

Body link rules:
- Must genuinely help the reader at that exact point in the post
- Place near (within 1–2 paragraphs of) a topic the linked page covers
- Don't force a link if the post doesn't naturally call for one — bio-only is fine

Anchor text distribution (track across all posts):

| Anchor type | Target mix | Examples |
|---|---|---|
| Branded | 40–50% | "Acme", "Acme Tools", "Acme's documentation" |
| Partial-match | 20–30% | "Acme's CI/CD platform", "see Acme's monorepo guide" |
| Semantic / long-tail | 15–25% | "this benchmark on deploy time", "the team's analysis of cold-start latency" |
| Generic | 5–10% | "here", "this article", "see this case study", URL-only |
| Exact-match keyword | <10% | "monorepo CI tool", "best CI/CD platform" — used SPARINGLY |

Why this matters: diversification reduces manual-action risk by 68%. Sites that use exact-match on every guest post get flagged within months. Track anchor distribution across last 20 placements; if exact-match exceeds 10%, stop using until ratio rebalances.

Author bio rules:
- ONE link only
- Anchor: branded or URL — never exact-match keyword
- 1–2 sentence bio — not a sales pitch
- Link to homepage or specific resource (not a sales page)

Forbidden in any guest post:
- Self-promotional CTAs ("buy our X", "sign up for our Y")
- Stuffed exact-match anchors
- Affiliate links unless explicitly approved by host (and then with `rel="sponsored"`)
- Linking to the same destination URL across multiple posts (sitewide pattern)

## Stage 8 — Follow-up and relationship

| Action | Timing | Purpose |
|---|---|---|
| First follow-up | 7 days after pitch (no reply) | Polite bump, re-state one topic, ask if a different angle would fit |
| Second follow-up | 14 days after pitch (no reply after first) | One sentence; do not pitch a third time |
| Thank-you note | After post is published | One paragraph, no ask, mention a specific reader response if any |
| Share + amplify | Day of and week after publication | Post on social; tag the publication and editor; comment-engage |
| Re-pitch trigger | 90 days after publication | Pitch a follow-up topic referencing the prior post's reception |

Goal: convert a one-off placement into a 3–4 post relationship over 12 months. Each subsequent post has higher acceptance, compounds your association, and builds tier-up portfolio.

## Decision guide — edge cases

| Situation | Action |
|---|---|
| Site lists "guest post fee: $200" with no `rel="sponsored"` | Strike — paid placement passing ranking signal = penalty |
| "Vetted network" agency offers 10 placements/month for $2k | Strike — guest-post farm; Oct 2025 update target |
| Niche-edit / link-insertion service offers placement on existing article for $300 | Strike — same penalty class as paid guest posts |
| Site clearly editorial but "write for us" page is 2 years old | Email the editor directly anyway — page outdated, not policy |
| Editor responds: "We charge $150 per published post, fully edited" | Skip unless `rel="sponsored"` is explicitly applied |
| User wants one ghostwriter for 10 posts under different bylines | Refuse — same-author footprint = PBN-detection trigger |
| User wants to syndicate the same post to 5 sites | Refuse — duplicate content; rewrite per publication |
| Pitch reply: "We need it within 48 hours and 3,500 words" | Decline if not realistic — better to pass than ship sub-standard |
| User has zero portfolio; wants to pitch tier-1 | Refuse and ladder — start tier-3/4, build 3–5 placements, then ladder up |
| Same topic accepted by two publications independently | Write two original versions — different angles, examples, conclusions |
| Pitch accepted but editor wants you to remove the body link | Negotiate once, accept gracefully — bio-link-only is still valid |
| Pitch accepted but editor wants exact-match anchor on body link | Push back for branded/partial; if they insist on exact, walk away |
| Tier-1 engaged 3 months, no acceptance | Stop. Drop tier. Re-pitch T1 in 6 months from a stronger position |

## Google's position on guest posting

Allowed:
- Editorial guest contributions on topically aligned sites
- Posts written for genuine readership, not just for the link
- Properly attributed sponsored content with `rel="sponsored"`
- Niche-relevant outreach that builds real relationships

Violations (per Google's spam policy):
- "Advertorials or native advertising where payment is received for articles that include links that pass ranking credit" (paid guest posts without `rel="sponsored"`)
- "Using automated programs or services to create links" (mass guest-post farms)
- "Excessive reciprocal link exchanges" (scaled "you write for me, I write for you")
- Guest post networks (closed networks publishing for SEO)
- AI-generated guest post farms (Oct 2025 update — distinct violation category)
- Repetitive exact-match anchor patterns across multiple guest posts (algorithmic flag)

The intent test: would this guest post exist if SEO didn't exist? If yes → editorial. If no → violation in waiting.

## Tools — free vs paid

| Tool | Tier | Use for |
|---|---|---|
| Google Search (operators) | Free | Discovery |
| Ahrefs Free Backlink Checker | Free (limited) | Top 100 backlinks of competitor → guest opportunities |
| Wayback Machine | Free | Confirming a site's longevity / topical history |
| Hunter.io free tier | Free (limited) | Editor email discovery |
| Apollo / RocketReach free tier | Free (limited) | Editor LinkedIn / email discovery |
| Featured.com newsletter | Free | Editor calls for sources (HARO replacement) |
| Source of Sources (SOS) | Free | Editor calls for sources |
| Qwoted | Freemium | Journalist matching |
| Similarweb (free tier) | Free | Traffic estimate sanity-check |
| Ahrefs / Semrush full | Paid | Network graph, full backlink profile |
