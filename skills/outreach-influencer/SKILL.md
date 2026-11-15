---
name: outreach-influencer
title: "Influencer Outreach Email Templates and Creator Briefs"
description: "Influencer outreach: email templates, creator vetting, collaboration briefs, rate research, FTC disclosure. Use when pitching creators or paid deals."
license: Apache-2.0
compatibility: "Needs web search for creator research. Any OS."
domains: marketing launch
rules:
  - content(influencer) content(outreach)
  - content(creator) content(pitch)
  - content(influencer) content(brief)
  - content(ambassador) content(outreach)
---

## Overview

Creator outreach turns a product into a recommendation from someone the audience already trusts. The work is mostly vetting and clarity: pick creators whose audience matches the buyer, pitch them as a collaborator, brief them without scripting them, and keep every paid or gifted relationship disclosed.

## Mental model

A creator is a small media business. They protect audience trust above any single deal, so a pitch that respects their format, their voice, and their time converts better than a pitch that tries to buy reach. Fit beats follower count.

## Rules

### Finding and vetting

Check each creator from live sources:

| Check | Evidence |
|-------|----------|
| Audience fit | Who comments, which topics get engagement, location and language |
| Engagement quality | Real conversation in comments, not only emoji; view-to-follower ratio on recent posts |
| Brand safety | Recent content, past controversies, competing sponsors |
| Disclosure habit | Past sponsored posts are labelled |
| Contact route | Business email in bio or channel About page |

Drop creators with no published contact, signs of purchased followers, or conflicts with a direct competitor. Never scrape private data or message people through automated tools.

### Tiers and rates

Rates vary by platform, niche, and format, and public benchmarks disagree by up to four times between datasets. Ask the creator for a rate card first, then check it against the planning bands below (as of 2026-11, vendor surveys, not rules). Look up current figures before proposing a budget.

| Tier | Followers (common cut) | Instagram post | TikTok video | YouTube integration |
|------|------------------------|----------------|--------------|---------------------|
| Nano | under 10,000 | USD 50 to 500 | USD 50 to 200 | USD 1,000 to 3,000 |
| Micro | 10,000 to 100,000 | USD 250 to 2,500 | USD 200 to 800 | USD 5,000 to 20,000 |
| Macro | 100,000 to 1,000,000 | USD 2,500 to 12,000 | USD 800 to 5,000 | USD 20,000 to 200,000 and up |

Tier cut-offs differ by source, so state which one you use. Engagement rate usually falls as audience grows; one vendor-reported 2026 study of 92 partnerships found medians of 6.7% for nano, 3.9% for micro and 1.4% for macro creators.

Check any quote with two numbers:

- Cost per thousand views = fee / expected views x 1,000, where expected views is the median of the creator's last 10 posts of the same format.
- Cost per engagement = fee / (expected views x engagement rate).

Usage terms are priced apart from the post. Vendor-reported planning bands: paid-ad use of the creator's handle or content (whitelisting, partnership ads) adds roughly 20% to 50% of the base fee for about 30 days, more for longer terms; exclusivity in a category adds roughly 25% to 100% depending on length. Put in writing the assets, platforms, start and end dates, and who can revoke. Do not agree to perpetual rights.

Offer formats in this order of cost: gifted product, affiliate or revenue share, flat fee for one deliverable, ongoing ambassador deal.

### First pitch

Under 120 words. Subject names the collaboration, not "Partnership opportunity". Line one cites a specific video, post, or episode and what you liked about it. Then: what the product is in one sentence, why it fits their audience, what you offer (product, fee, or both), and one question. Ask for their rate card or a call, not a yes.

### Brief

Send after interest. Include: the single message to convey, must-include facts, claims you can and cannot make, deliverables and dates, usage rights and duration, approval steps, and the disclosure requirement. Leave format and voice to the creator.

### FTC endorsement and disclosure

Any material connection between a brand and a creator must be disclosed clearly: payment, free product, discounts, affiliate commission, family or employment ties. In the US (FTC guidance, page dated 2019):

- Put the disclosure with the endorsement, not on a profile page, at the end of a post or behind a "more" link. In video, say or show it in the video itself, and repeat it periodically in live streams. In images, keep it on screen long enough to read.
- Use plain words: "ad", "sponsored", "thanks to [brand] for the free product". Do not use "sp", "collab", "thanks" or "ambassador" alone, and do not bury it in a pile of hashtags.
- Do not rely only on the platform's own label; use it in addition to words in the content.
- The creator may not make claims the brand cannot substantiate or describe a product they have not used.

US rule on fake reviews and testimonials (16 CFR Part 465, effective 2024-10-21): a brand may not write, buy or publish fake or false reviews or testimonials. A brand may not buy followers or other fake influence signals, and insider reviews (staff or agents) need a clear disclosure of the relationship. A testimonial from an AI avatar is prohibited when the experience it describes is invented. The brand is liable for what it knew or should have known was false.

United Kingdom: advertising rules (the Advertising Standards Authority and the CAP Code) require ads to be obviously identifiable; a clear "Ad" label is the common form. The ASA, CAP and CMA have published joint influencer guidance; read the current version. Since April 2025 (the CMA announced the regime in force on 2025-04-07) the Competition and Markets Authority can fine for consumer-law breaches directly, up to 10% of global turnover, including undisclosed paid posts. A platform's paid-partnership tool can satisfy the rule only if the label is clear and prominent.

The brand is responsible for briefing and monitoring creators. For any other country, state the creator's and the audience's country and send the question to counsel.

### Follow-up

One follow-up after 5 to 7 days. Silence after two touches means no.

### Shared rules

Use the `outreach-cold-copy` skill for subject and cadence craft, and the `outreach-compliance` skill for consent and opt-out rules.

## Examples

Bad: "Hey! We love your content. Want to promote our app? DM for rates."

Good: "Your 8-minute teardown of budgeting apps was the first review that tested the export feature. Our app, Ledgr, does one thing differently: it matches receipts automatically. We'd like to send you a free year and see if it fits your channel. Could you share your rate card for a dedicated video?"

Bad brief: "Say these 12 lines exactly."

Good brief: "Main point: receipts match themselves. Please mention the free export. Do not claim it replaces an accountant."

## Checklist

- [ ] Each creator vetted for audience fit, engagement quality, and brand safety?
- [ ] Rate card requested, quote checked against planning bands and the cost formulas, usage and exclusivity priced separately?
- [ ] First pitch under 120 words, citing a specific piece, one question?
- [ ] Brief lists allowed and forbidden claims, rights, dates, and approvals?
- [ ] Disclosure requirement stated in writing, in the content itself?
- [ ] Counsel pointer included for contracts, rights, and non-US creators?

## Composition / References

- Pair with `outreach-cold-copy` and `outreach-compliance` for craft and legal rules.
- Pair with a launch or content plan that defines the message the creator carries.
