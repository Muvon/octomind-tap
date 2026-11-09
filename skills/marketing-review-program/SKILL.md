---
name: marketing-review-program
title: "Ask Customers for Reviews: Program Plan"
description: "Plans how to ask real customers for honest public reviews: site choice, invitation copy, incentive and disclosure rules. Use to start a review program."
license: Apache-2.0
compatibility: "Needs web search or page fetching to check current platform policies. Any OS. Plans only; sends nothing."
capabilities: webfetch
domains: marketing
rules:
  - match(\b(customer|user|product)\s+reviews?\b)
  - match(\b(ask|collect|get|generate|request)\w*\s+(more\s+|honest\s+|positive\s+|\d+\s+)?(public\s+)?reviews\b)
  - match(\b(ask|request)\w*\b.*\b(customers|users|clients)\b.*\breviews?\b)
  - match(\b(g2|capterra|trustpilot)\b.*\breviews?\b)
  - match(\breview\s+(program|campaign|incentive|request|site)s?\b)
  - content(testimonials)
  - match(\b(ugc|user[- ]generated\s+content)\b)
  - match(\bcustomer\s+advocacy\b)
---

## Overview

Reviews and customer posts are claims from third parties, so their value depends on being honest and verifiably unpaid for sentiment. This skill produces a program plan: when to ask, where, whom, with what wording, what incentives each platform allows, and how to measure it. It sends no invitations and changes no profile. Platform and legal positions below were read on 2026-11-09 and change; recheck before launch.

## Mental model

Moment of success, then neutral invitation to every eligible customer, then honest review on a chosen site, then disclosed and permitted reuse. Each step has one failure: asking too early, asking selectively, rewarding sentiment, hiding the connection. The plan removes those four.

## Rules

### Sequence

- Ask after the activation milestone or another measured success moment, never at signup. A review from someone who has not yet used the product is not a review of the experience.
- If activation is not defined, the first deliverable is a definition: the events and time window that mark a customer who got value. Don't invite until it exists.

### Choose sites

- Start from where this buyer compares products. Ask the team, check sales calls and search results for the category.
- When captured AI answers exist, note which review sites they cite. Label this an observation, not a ranking cause.
- Pick one to three sites. Spread thin reviews across many sites help none.

### Eligibility and frequency

- Invite real customers with actual use. Exclude employees, relatives, investors and agents, or require clear disclosure of the relationship.
- Cap invitations per person, for example one per product per 12 months. This is a convention, not a platform rule.
- Contact basis follows the `outreach-compliance` skill: record the source, honor opt-outs, respect the recipient's jurisdiction.

### Invitation

- Neutral wording that asks for an honest review, states any incentive, and goes to every eligible customer the same way.
- No sentiment gating: don't send satisfied customers to the public site and unhappy ones to a private form. Trustpilot and G2 name selective solicitation as a violation; the FTC says it can violate the FTC Act.
- A private feedback channel may exist, offered to everyone alongside the public link.

### Incentives by destination

Read on 2026-11-09; recheck each page before launch. Conditional means allowed under limits. The Capterra and Amazon rows come from search extracts of the official pages, because direct fetches failed.

| Destination | Status | Source and rule |
|---|---|---|
| G2 | Conditional | [Guidelines](https://legal.g2.com/community-guidelines): incentives may not depend on sentiment; vendors may not incentivize independently without disclosing to G2; G2 labels incentivized reviews |
| Capterra / Gartner Digital Markets | Conditional | [Guidelines](https://www.capterra.com/legal/community-guidelines/): nominal incentives only, offered regardless of rating and never contingent on a positive review; insiders and direct competitors can't receive them; use the Vendor Portal link; incentivized reviews are labelled |
| Trustpilot | Forbidden | [Guidelines for businesses](https://legal.trustpilot.com/for-reviewers/guidelines-for-businesses): no incentives for writing or editing reviews; invite everyone the same way; no selective invitations |
| Google Business Profile | Forbidden | [Policy](https://support.google.com/business/answer/2622994): no incentives; no discouraging negative reviews or selectively soliciting positive ones |
| Apple App Store | Forbidden | [Guidelines](https://developer.apple.com/app-store/review/guidelines/): paid or incentivized feedback is manipulation; apps must not force a rating or review for access |
| Google Play | Forbidden | [Policy](https://support.google.com/googleplay/android-developer/answer/9898684): do not offer rewards for ratings or reviews |
| Amazon | Forbidden | [Review policy summary](https://trustworthyshopping.aboutamazon.com/how-amazon-maintains-a-trusted-review-experience): selling partners can't offer compensation for a positive or negative review, or ask customers to edit or remove one. Amazon Vine is run by Amazon and isn't a seller incentive |

Where a platform allows incentives, disclose them in the invitation and keep the offer independent of the rating.

### Legal floor

Not legal advice. Read at [eCFR](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-D/part-465) and the [FTC Q&A](https://www.ftc.gov/business-guidance/resources/consumer-reviews-testimonials-rule-questions-answers).

- 16 CFR 465.4: no paying or rewarding reviews where the reward depends on a particular sentiment, stated or implied.
- 16 CFR 465.5: reviews by officers, managers, employees, agents or their immediate relatives need clear disclosure; managers must not solicit them without it. The FTC says generalized solicitations to all customers are exempt.
- 16 CFR 465.7: no unfounded legal threats, intimidation or knowingly false accusations to block or remove a review; no claiming displayed reviews are all reviews when some are hidden by rating.
- 16 CFR 255.5: a material connection that the audience would not expect, including free product, discounts or other benefits, must be disclosed clearly. Incentives are not banned by the rule.
- UK: Digital Markets, Competition and Consumers Act 2024, Schedule 20 paragraph 13 covers fake reviews, concealed incentives and selective publication; in force 6 April 2025.
- EU: not verified here; flag for local review.

Recommend legal review before launch.

### Social posts

- Anyone paid, rewarded or given product to post must disclose the connection clearly in the post itself, in plain words, not only on a profile (16 CFR 255.5).
- Use the platform label where one exists. TikTok: commercial content disclosure setting, shown as Paid partnership ([help](https://ads.tiktok.com/help/article/about-the-content-disclosure-setting-for-creators)). LinkedIn: brand partnership label for content shared in exchange for value ([help](https://www.linkedin.com/help/linkedin/answer/a1627083)). Instagram: paid partnership label for content made for an exchange of value, including free products and gifts ([help](https://help.instagram.com/1109894795810258)). X: Paid Partnership setting for compensated, gifted, or affiliate promotions ([policy](https://help.x.com/en/rules-and-policies/paid-partnerships-policy), reviewed 2026-09).
- Get written permission before reusing a customer's post, quote or name. A reposting brand makes its own disclosures. For creators, see `outreach-influencer`.

### Negative reviews

Don't suppress, threaten or offer payment to remove. Route the problem to support, then let the review stand. Writing public replies is owned elsewhere.

### Measurement

Report counts with denominators: eligible customers, invitations sent, reviews per site, rating distribution for incentivized versus non-incentivized reviews, review recency, and how many reviewers reached activation. Rating drift upward after an incentive starts is a warning sign. Treat AI-answer changes as a separate observation with no causal claim.

## Examples

Wrong invitation: "Love our product? Leave us 5 stars on Trustpilot for a $20 gift card!"
Right: "You have used Acme for 30 days. If you are willing, tell others what it was like, good or bad: [link]. We do not reward reviews."

Wrong routing: score 9-10 goes to the public site, score 0-8 goes to a private form.
Right: everyone receives the same message with the public link and a separate support link.

Wrong post brief: "Post a glowing video and get a free year."
Right: "Free year offered for any honest post. Turn on the paid partnership label and say you received it."

## Checklist

- [ ] Activation trigger defined before any invitation timing?
- [ ] One to three sites chosen with the buyer-comparison evidence?
- [ ] Insiders excluded or disclosed; frequency cap set and labelled a convention?
- [ ] One invitation per site, neutral, same for every eligible customer, incentive stated?
- [ ] Every incentive checked against the table and the platform's live page?
- [ ] Social posts carry in-post disclosure and the platform label where verified?
- [ ] Written permission step for reuse?
- [ ] Negative-review routing avoids suppression?
- [ ] Metrics have denominators; legal review items listed?

## Composition / References

Save as `review-program-[product].md` with: activation trigger, sites and policy check, eligibility, invitation copy per site, incentive and disclosure, social program, negative-review routing, metrics, legal review items.

- `outreach-compliance` for contact basis and opt-out; `outreach-influencer` for creator disclosure.
- [16 CFR part 465](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-D/part-465), [16 CFR part 255](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255), [DMCC Act Schedule 20](https://www.legislation.gov.uk/ukpga/2024/13/schedule/20).

Sources accessed 2026-11-09. The frequency cap and one-to-three site limit are practitioner conventions.
