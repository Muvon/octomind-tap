---
name: launch-pitch-pricing
title: "Pitch Deck and Pricing Tiers: Sales Pages and Offers"
description: "Write elevator pitches, 10-12 slide pitch decks, pricing tiers, sales pages and partnership proposals. Use when turning a product into an offer."
license: Apache-2.0
compatibility: "Needs web search; slide decks need the slide-deck CLI. Any OS."
capabilities: shell slides image-view
domains: founder
rules:
  - match((?i)\b(elevator\s+pitch|pitch\s+deck|investor\s+deck)\b)
  - match((?i)\bpricing\s+(model|tiers?|page|strategy|plans?)\b)
  - match((?i)\b(sales\s+page|partnership\s+(proposal|pitch))\b)
  - semantic(how should I price my product and what tiers should I offer, 0.70)
  - semantic(write a pitch deck outline for investors with ten to twelve slides, 0.69)
  - semantic(write my elevator pitch and a sales page for this product, 0.69)
  - semantic(draft a partnership proposal and a pricing page for our plans)
---

## Overview

Turn products into offers people pay for through value perception, buyer psychology and conversion, not hype. Close the gap between what the product is and what buyers perceive. Covers elevator pitches, pitch decks (for investors, partners or the founder), pricing models and tiers, long-form sales pages, partnership proposals, objection mapping and value articulation (features into outcomes people pay for). Brand naming, positioning and voice, and paid-ad creative are separate deliverables; this skill is the persuasion layer.

## Mental model

A pitch works through specificity ("saves DevOps teams 4 hours per deploy" beats "saves time"), tension between current and desired state, proof for every claim (metric, testimonial, demo), one big idea in a sentence and a clear ask. Who writes the check matters more than who uses the product.

## Rules

### Process

1. Understand the offer: what it does, for whom, current pricing (if any), stage.
2. Research in parallel: competitor pricing and tiers, category pricing strategy (freemium versus paid), how similar products pitch, why the audience pays, category sales pages.
3. Map what triggers purchase in this category, map objections before writing, then build the assets.

Memory: before starting, remember(["pitch deck", "pricing strategy", "sales copy", "value proposition", "target audience", "competitors"]). After completing, memorize() pitch decisions, the pricing model and objection responses.

### Default pricing model by product type

- Developer tool (CLI/API): usage-based or freemium. Devs try before buying, and usage scales naturally.
- B2B SaaS: free trial then per-seat. Decision-makers must see value, and seats scale with the org.
- B2C SaaS: freemium then flat rate. Low-friction entry; simple pricing beats decision fatigue.
- Marketplace: transaction fee, aligned with user success.
- Content or community: free then premium. Build audience, monetize the most engaged.
- Open source: open core or hosted. The free core drives adoption.
- AI product or agent: hybrid platform fee plus usage credits, or outcome-based (2026 example: Intercom Fin at $0.99 per outcome, such as a resolution, on its pricing page). Each use carries real inference cost, so a flat seat price loses money on the heaviest users; price the unit the buyer values (task, resolution) and keep it above per-unit model cost.

### Pricing psychology

- Anchoring: show the expensive option first so the middle feels reasonable.
- Decoy: a slightly worse-value tier makes the target tier look great.
- Charm pricing: $29 feels meaningfully cheaper than $30 (consumer, not enterprise).
- Value framing: "less than a coffee a day" or "saves 4 hours a week = $X at your hourly rate". Frame price against the cost of inaction.
- Loss aversion: "Your free trial includes everything. Don't lose access to [feature]."
- Social proof: a "Most popular" badge on the tier you want chosen.

### Pricing mistakes

- Too low: signals low quality and is hard to raise later.
- Too many tiers: 3 ideal, 4 max, never 5 or more.
- Frustrating feature gates: the free tier must deliver real value.
- No annual discount: leaves LTV on the table.
- Unlimited AI usage on a flat plan: inference cost scales with your best customers; meter or cap it.
- Hidden pricing where the audience expects transparency: kills trust.

### Copy discipline

Literal over clever. The one-sentence description (title slide, elevator opener, sales-page hero) says what the product is and who it is for in words a listener could repeat; a coined category gets translated into the one buyers and investors already know. Comparisons name the competitor and the measured axis (price, setup time, benchmark result), compared like for like under a stated condition, or are cut: "faster and cheaper than alternatives" invites the first skeptical question. Name the members of a set ("integrates with HubSpot and Salesforce"), not "your stack". Lead with value, not features: "Save 10 hours/week", not "AI-powered automation".

### Objections to map, with response strategy

| Objection | Response strategy |
|-----------|-------------------|
| Price ("too expensive") | Value comparison, ROI |
| Trust ("never heard of you") | Social proof, risk reversal |
| Timing ("not now") | Urgency, cost of waiting |
| Switching ("we already use X") | Migration ease, unique value |
| Complexity ("looks hard") | Demo, onboarding promise |
| Need ("we don't need this") | Problem reframing, data |

### Ask or assume

- Product described: ask who is buying (end user versus decision maker), the current price and the top 2 alternatives.
- Pricing: ask competitor prices, freemium versus paid-only preference and target customer size.
- Pitch deck: ask the audience (investors, partners, customers) and the strongest proof point.
- Sales page: ask whether positioning and messaging are decided; if not, set positioning first.
- Vague request: ask one question, "Who are you trying to convince, and of what?"
- Autonomous or non-interactive brief: skip the questions, use the brief's facts, state assumptions and deliver.

### Conduct

- No hype ("revolutionary", "game-changing", "disruptive", "-grade", "-native" or "AI-powered" with no fact behind it).
- Don't skip competitive research, write generic copy, or suggest dishonest tactics (fake scarcity, misleading claims, bait-and-switch).
- Offer multiple options with reasoning, never one price point.
- Fit the solo-founder context: no enterprise sales playbooks unless asked.
- SAFE and valuation terms are reviewed by the founder's counsel. This is not legal or investment advice.

## Output format

Save every deliverable as Markdown in the working directory.

Elevator pitch, `pitch-elevator-[product].md`:

- 30 seconds (networking): what and for whom; why it is different; one proof point.
- 60 seconds: the problem that makes them nod, why today's options fail, the concrete solution, one sharp differentiator, proof, the ask.
- 2 minutes (meeting or demo intro): story hook, scale of the problem, the product in plain language, the "oh wow" demo moment, why not X, traction, vision, a specific next step.

Pitch deck (10-12 slides), `pitch-deck-[product].md`, as a Marp deck: start with `slide-deck new`, `theme: octo`, one slide per section below, speaker notes in `<!-- -->` comments. Then run `slide-deck lint` and `slide-deck render pitch-deck-[product].md --pptx --png`: a PDF to send, a PPTX for PowerPoint users (slides as images; `--pptx-editable` is experimental) and PNG previews to open and check. Fix every overflow warning. Follow the narrative arc (problem, insight, solution, proof, opportunity, ask):

1. Title: name and tagline, team, one visual capturing the product.
2. Problem: one sentence, a specific persona, quantified pain; a visual of the ugly status quo or a painful stat.
3. Insight: the non-obvious "we realized that...", not "we built an app"; it separates good pitches from forgettable ones.
4. Solution: plain language, a screenshot or demo GIF, max 3 bullets.
5. How it works: 3 steps or a visual flow; more means simplify.
6. Traction: users, revenue, growth, testimonials, waitlist; pre-launch: beta signups, LOIs, pilots, GitHub stars. Honest numbers over vanity metrics.
7. Market: bottom-up sizing first (reachable accounts times realistic ACV), top-down reports only as a cross-check, never "if we get 1%"; the trend in your favor; why now.
8. Business model: how you make money, a pricing summary, unit economics if available.
9. Competition: a 2x2 or comparison table, the quadrant you own; show differentiation, never trash competitors.
10. Team: why you, relevant experience not bios; solo founders: domain expertise and what you have shipped.
11. Ask: investors get an amount and instrument (in the US, pre-seed and seed typically run on post-money SAFEs; YC's standard deal is $125k for 7% on a post-money SAFE plus $375k on an uncapped MFN SAFE); others get a partnership or beta ask. Use of funds as milestones that earn the next round, with months of runway (commonly 18-24). Round size and valuation norms move quarterly: check current Carta or PitchBook data, never quote benchmarks from memory.
12. Contact: name, email, website, demo link.

Pricing strategy, `pricing-[product].md`:

- Model recommendation (freemium, free trial, paid only, usage-based, flat rate, per-seat) and why.
- Competitive table: competitor, model, free tier, paid start, enterprise.
- Tiers: Free or Starter at $0 for acquisition (useful but not enough to never upgrade, plus the limit that triggers paid); Pro or Growth at $X/mo as core revenue (plus the anchor that makes it feel fair); Team or Business at $X/mo for collaboration, admin, priority support and higher LTV.
- The psychology levers applied, including $29 versus $30 versus $25.
- Pricing page copy: a value-focused literal headline ("Free for one user, $12 per seat for teams", not "Our pricing" or a slogan like "Plans that grow with you"); a per-tier CTA with the reason (Free "Get started", low commitment; Pro "Start free trial" or "Upgrade"; Business "Contact us" or "Start trial", depending on the sales motion); an FAQ on plan switching (easy), hitting the limit (graceful, not punitive), refunds (trust-building) and the annual discount (framed as savings).
- Conservative revenue projections at months 3, 6 and 12 (users, conversion %, ARPU, MRR) with stated assumptions.

Sales page, `sales-page-[product].md`:

- Above the fold: an outcome headline (what they get, not what you do), a one-sentence subheadline (who and how), the primary CTA, a visual.
- Pain: 2-3 short paragraphs in their language, specific scenarios over abstract pain.
- Solution: the bridge from pain to relief, before and after.
- 3-5 feature blocks with benefit-first names: What, So what, Proof.
- The strongest social proof available: 2-3 testimonials (name, role, photo), metrics, logos, a before-and-after case snippet. Genuine only.
- Objections ("You might be wondering..."): setup effort, doesn't work for me (trial, refund, guarantee), why not [competitor] (honest differentiation).
- Final CTA: an urgency or aspiration headline, the same CTA as the hero, a risk reducer ("Free for 14 days. No credit card required.").

Partnership proposal, `partnership-[partner].md`:

- What is in it for them, first: your audience, theirs, and why the overlap wants both.
- A specific proposal, never "let's work together": a technical integration, co-marketing (joint content, cross-promotion) or a bundle or referral (revenue share).
- What we bring (audience, technology, content) and need (API access, co-marketing commitment, logo usage).
- One clear next step ("15-minute call to explore?", "Can I send a demo?").

## Checklist

- [ ] Buyer identified (who writes the check) and objections mapped before writing?
- [ ] Competitor pricing and pitches researched, and several pricing options given with reasoning?
- [ ] Deck linted and rendered, every overflow warning fixed, PDF and PNG previews checked?
- [ ] Market sized bottom-up, and funding benchmarks checked against current data rather than memory?
- [ ] Hero and one-sentence description literal; comparisons name the competitor and the measured axis?
- [ ] Deliverables saved under the file names above, with no hype and no fabricated proof?

## Composition / References

- `slide-decks` skill: Marp deck production and export.
- `launch-brand-identity` skill: positioning and voice that the pitch and sales page build on.
- `outreach-investor` skill: investor messages that carry the deck.
