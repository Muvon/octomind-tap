---
name: shopping-gifts
title: "Gift Idea Generator – Shortlist Within Your Budget"
description: "Gift idea generator for a person the user describes: recipient intake, a few distinct directions, live price, delivery and return checks, and a shortlist of up to three gift ideas with honest weaknesses. Use when the user asks for gift ideas, a gift finder, a present for someone, or what to give for an occasion."
license: Apache-2.0
compatibility: "Requires: web search and web page fetching."
domains: shopping
rules:
  - content(gift)
  - content(gifts)
  - content(gifting)
  - match((?i)\bpresents? for\b)
  - match((?i)\bwhat (should|can|do) (i|we) (get|give) (my|our|him|her|them)\b)
  - content(birthday)
  - content(anniversary)
---

## Overview

Gift requests start from a person, not a product category. This skill turns what the user says about one named recipient into a small, personal shortlist grounded in current web research instead of generic gift-guide rankings. The outcome is up to three ideas, each tied to something the user said about the person, with a stated weakness, a checked price and a delivery and return caveat. The user keeps the purchase.

## Mental model

A modest gift that feels right beats an expensive one that creates work for the recipient. Every idea must connect to a fact the user supplied, and "they already have the useful version" is a valid reason to skip an idea. Three distinct ideas beat thirty vaguely suitable products. Budget is a ceiling, not a spending target.

## Rules

### Workflow

1. Intake: identify the recipient by the name or nickname the user gives, plus relationship, occasion, interests, dislikes, things they already own, budget ceiling, country, currency and delivery deadline. Ask one focused question for a material gap.
2. Frame: turn only the supplied details into a few gift criteria. Separate confirmed preferences from assumptions. Note allergies, sizing, accessibility or household constraints when the user gave them.
3. Explore: use web search to research several genuinely different directions, including a low-cost or non-purchase option when it fits. Don't start from sponsored gift lists.
4. Verify: read retailer pages with `knowledge(command="read", source="<url>")` to check the exact item or experience, current price, availability, delivery estimate, personalization lead time and return restrictions. Cite only what you confirmed.
5. Shortlist: present at most three ideas, each tied to the recipient brief, with its honest weakness and a total-cost check against the budget.
6. Recommend: name the strongest fit and the one remaining uncertainty that could change it. Leave purchase and every outward action to the user.

### Evidence

- Every price, spec and availability claim needs a live source from this session. Give the retailer link, check date, country and currency, and separate the listing price from the delivered cost.
- Check shipping, tax where shown, consumables and subscriptions. Mark unknown costs as unknown instead of pretending the item fits the ceiling.
- A delivery estimate is not a guarantee. Flag tight deadlines, and suggest locally obtainable or printable alternatives when verified shipping cannot meet the occasion.
- Link current official sources for any legal or safety claim.
- If pages are blocked or prices are unavailable, say what remains unverified and offer search terms or a clearly labeled concept, not an invented live deal.

### Recipient privacy

- Use only what the user shares about the person. Don't search for private profiles and don't infer sensitive traits from a name, age or relationship.
- Confirmed durable recipient facts (sizes, dislikes, past gifts) may be stored with `memorize`, but only after the user confirms. Never store them in autonomous runs.

### Gift fit rules

- Personalization can remove return options. Verify the seller's actual policy before calling a gift return-friendly, and don't invent legal rights or blanket cancellation rules.
- Experiences need recipient interest, location and accessibility fit. Verify validity dates, booking requirements and exclusions before recommending a voucher.
- Avoid gifts that impose ongoing fees, maintenance or an obligation on the recipient unless the burden is stated explicitly.
- Don't repeat health promises and don't treat popularity as proof of safety.
- For children's items, food or safety-sensitive gifts, check relevant official guidance and recalls. Don't diagnose, prescribe or recommend regulated medical devices.
- Investment gifts and affordability questions belong with a qualified professional, not a gift shortlist.

### Output shape

- Recipient and occasion: confirmed details, assumptions, budget and deadline.
- Up to three ideas: the gift, why it fits this person, price with currency, retailer link and check date, delivery and returns caveat, honest weakness.
- Best fit: one recommendation tied to the brief, with any unknown delivered cost or unconfirmed recipient preference made explicit.

Keep verified details, inferences and unknowns visibly separate. Never invent prices, specs, laws, sources or recipient preferences, and never exceed the budget silently.

### Running without a human

- Chatting directly: ask one focused question for a material gap, then proceed.
- Brief marked AUTONOMOUS or non-interactive: ask nothing. List assumptions at the top (occasion, budget, country, recipient traits), deliver the shortlist, avoid private profiling, and label every region-dependent fact you could not verify. Don't write to memory.

## Examples

Recipient-led intake:

- Bad: "Gift for Maya, who loves gardening" answered with a list of top gardening products.
- Good: Ask for occasion, budget and country in one question, then research listings that match what the user said about Maya.

Recipient who has everything:

- Bad: "They have everything" answered with a more expensive gadget.
- Good: Offer a verified experience, a consumable or a thoughtful non-purchase gesture, with its booking terms and validity checked.

Autonomous run:

- Bad: Stopping to ask for the budget when the brief is non-interactive.
- Good: State "Assumed: birthday, mid-range budget, delivery to the buyer's home country" at the top, deliver three ideas, and label any region-dependent detail as unverified.

## Checklist

- [ ] Each idea links to something the user said about the recipient.
- [ ] At most three ideas, each with a stated weakness.
- [ ] Every price has retailer link, check date, country and currency.
- [ ] Delivered cost and the budget ceiling compared; unknown costs labeled.
- [ ] Delivery against the deadline and return rules checked, personalization noted.
- [ ] Unverified items labeled, with no invented prices, laws or preferences.
- [ ] No private profiling and no sensitive traits inferred.
- [ ] Nothing stored in memory without user confirmation, and nothing in autonomous runs.
- [ ] Purchase left with the user.

## Composition / References

- `shopping-reviews` analyzes customer reviews of one chosen product once a candidate gift is picked.
- Official safety and recall sources for children's items and food: link the current regulator page for the buyer's country.
