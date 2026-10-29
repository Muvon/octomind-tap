---
name: outreach-influencer
title: "Influencer Outreach Email Templates and Creator Briefs"
description: "Influencer outreach email templates, creator vetting, collaboration briefs, rate research, and FTC disclosure checks. Use when pitching influencers, creators, or ambassadors and planning paid, gifted, or affiliate partnerships."
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

Rates vary by platform, niche, and format and shift constantly. Do not quote benchmarks from memory. Ask the creator for their rate card, or research current figures before proposing a budget. Offer formats in this order of cost: gifted product, affiliate or revenue share, flat fee for one deliverable, ongoing ambassador deal.

### First pitch

Under 120 words. Subject names the collaboration, not "Partnership opportunity". Line one cites a specific video, post, or episode and what you liked about it. Then: what the product is in one sentence, why it fits their audience, what you offer (product, fee, or both), and one question. Ask for their rate card or a call, not a yes.

### Brief

Send after interest. Include: the single message to convey, must-include facts, claims you can and cannot make, deliverables and dates, usage rights and duration, approval steps, and the disclosure requirement. Leave format and voice to the creator.

### FTC endorsement and disclosure

Any material connection between a brand and a creator must be disclosed clearly: payment, free product, affiliate commission, or employment. Disclosure goes where the audience sees it without clicking, in the content itself, in plain words such as "ad", "sponsored", or "paid partnership". Hashtags buried in a pile do not count, and platform tools alone may not suffice. The creator may not make claims about the product that the brand cannot substantiate. The brand is responsible for guiding and monitoring creators. Rules differ outside the US, so state the recipient's country and send questions to counsel.

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
- [ ] Rates asked for or researched live, none quoted from memory?
- [ ] First pitch under 120 words, citing a specific piece, one question?
- [ ] Brief lists allowed and forbidden claims, rights, dates, and approvals?
- [ ] Disclosure requirement stated in writing, in the content itself?
- [ ] Counsel pointer included for contracts, rights, and non-US creators?

## Composition / References

- Pair with `outreach-cold-copy` and `outreach-compliance` for craft and legal rules.
- Pair with a launch or content plan that defines the message the creator carries.
