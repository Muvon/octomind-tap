---
name: launch-brand-identity
title: "Brand Identity: Naming, Positioning and Landing Copy"
description: "Craft an early-stage brand: names, positioning, messaging hierarchy, voice and landing page copy. Use when naming a product or writing its positioning."
license: Apache-2.0
compatibility: "Needs web search for competitor and trademark knockout research. Any OS."
rules:
  - match((?i)\b(name|names|naming|rename)\b.{0,25}\b(my|our|the|a)\s+(new\s+)?(product|startup|app|tool|company|brand|project|saas)\b)
  - match((?i)\bpositioning\s+(statement|framework|strategy)\b|\bbrand\s+(identity|voice|guidelines?|messaging)\b)
  - match((?i)\b(taglines?|messaging\s+(framework|hierarchy)|value\s+proposition)\b)
  - match((?i)\blanding\s+page\s+(copy|headline|hero)\b)
  - semantic(position my product against its competitors and write the messaging)
  - semantic(write the brand voice and messaging hierarchy for our product)
  - semantic(draft landing page headline and hero copy that states our value proposition, 0.72)
---

## Overview

Produce concrete, usable brand assets for early-stage products such as indie projects, startups, open-source tools and SaaS: names, taglines, positioning statements, messaging frameworks, voice guidelines and landing page copy that converts. Think like a copywriter who understands strategy; every word earns its place. The skill covers identity, positioning and voice. Sales-page conversion copy, pricing models, pitch decks and paid-ad creative sit on top of the identity and are separate deliverables.

## Mental model

A brand owns one word in the customer's mind. Specific beats general ("for solo founders" beats "for startups"), and the audience's own language beats marketing language. Competitive research comes first: you need to know what is already claimed.

## Rules

### Process

Fire independent search queries in parallel.

1. Understand the product: what it does, for whom, why it matters.
2. Research the space: how competitors position themselves, what language the audience uses.
3. Find the gap: which positioning angle is unclaimed or underserved.
4. Craft the identity: name, position, message, voice.

Research searches:

- "[competitor] tagline", "[competitor] homepage", "[competitor] about page"
- "[audience] language", "[audience] pain points reddit", "[audience] what they call [problem]"
- "[category] positioning", "[category] messaging examples"
- "[product type] landing page examples"

Memory: before starting, remember(["brand identity", "product positioning", "target audience", "competitors", "messaging"]). After completing, memorize() brand decisions, positioning and voice guidelines.

### Positioning

- Own a word. The best brands own one word in the customer's mind.
- Be specific. "For developers" beats "for everyone"; "for solo founders" beats "for startups".
- Frame the category. Prefer a category buyers already search for and understand. Creating a new one means first convincing the market that the category should exist, the costliest of the three positioning styles (head-to-head, a subcategory you can lead, a new category), so reserve it for products no existing category describes (April Dunford, Obviously Awesome). A coined label never stands alone: pair it with the known category it belongs to.
- Against, not negative. Position against the status quo, not against competitors by name, and name it concretely (the spreadsheet, the weekly manual export, the approval queue), not "legacy tools" or "outdated solutions".

### Naming

- Say it out loud. If you can't say it in conversation, it fails.
- Spell test: can someone type it after hearing it once?
- Search test: is it googleable? Does it clash with something big?
- Knockout check (a risk screen, not legal clearance): search the exact name and sound-alikes in the user's markets and Nice classes (software: 9 and 42). Use USPTO Trademark Search (tmsearch.uspto.gov, which replaced TESS), EUIPO eSearch or TMview for the EU, and the WIPO Global Brand Database elsewhere; then domains, app stores, GitHub, npm, PyPI and social handles. Shortlisted names go to a trademark attorney for a full clearance search before money is spent.
- Global test: does it mean something unfortunate in other languages?
- Short beats clever: 2 syllables beat 4.
- Test names and taglines against the "say it in conversation" rule.

### Copy

- Benefits over features: "Save 4 hours a week" beats "AI-powered automation".
- Specific over vague: "Used by 2,000 developers" beats "Trusted by many".
- Literal over clever in heroes. A headline a stranger can't decode without context fails; wordplay and slogans live in tagline options, each paired with a literal subheadline (what it is and for whom).
- Named comparisons or none: "half the price of X at 10 seats" works; "better than the alternatives" proves nothing.
- Name the set: "Works with Stripe, Paddle, and Lemon Squeezy", not "works with your payment tools".
- Effects over abstractions: "Replies land in Slack within a minute" beats "seamless communication".
- Active over passive: "Ship faster" beats "Faster shipping is enabled".
- Their words over your words: use the language your audience actually uses.
- One idea per sentence.
- No buzzwords without substance ("revolutionary", "cutting-edge", "next-gen", "-grade", "-native" and "-powered" compounds); replace each with the fact it stands for.
- Write for the solo founder or small team: no enterprise-scale brand playbooks.

### Technical products

- Don't hide the tech. Developers respect honesty about what is under the hood.
- Show, don't describe: code snippets, CLI output and screenshots beat adjectives.
- Respect intelligence: no "revolutionary" or "game-changing".
- Acknowledge tradeoffs: "Fast but opinionated" is more trustworthy than "best at everything".

### Ask or assume

- Product described: ask who the target audience is, the top 2-3 alternatives, and the one thing that makes this different.
- "Name my product": ask what it does, who it is for and what feeling the name should evoke.
- "Write landing page copy": ask whether positioning and messaging are decided; if not, do that first.
- Existing brand and a refinement: ask to see the current copy and positioning first.
- Autonomous or non-interactive brief: no questions. Research the alternatives yourself, state the assumed audience and differentiator, and deliver 2-3 options.

## Examples

Always give 2-3 alternatives with the reasoning ("I chose X because..."), never a single option.

Bad tagline: "Revolutionary AI-powered workflow platform."

Good tagline option: "Invoices matched to bank lines in one click", paired with the literal subheadline "Bookkeeping software for accounting firms with 5-50 clients."

## Output format

Brand identity, saved as `brand-identity-[product].md`:

```markdown
# Brand Identity: [Product Name]

## Positioning Statement
For [target audience] who [need/pain point],
[Product] is the [category] that [key differentiator].
Unlike [alternatives], [Product] [unique value].

## Core Value Proposition
[One sentence that answers: why should anyone care?]

## Messaging Hierarchy

### Primary Message (Hero)
[The #1 thing to communicate: what + for whom + why it matters]

### Supporting Messages
1. [Benefit 1]: [Proof point / how it works]
2. [Benefit 2]: [Proof point / how it works]
3. [Benefit 3]: [Proof point / how it works]

### Objection Handling
| Objection | Response |
|-----------|----------|
| "Why not just use [competitor]?" | ... |
| "Is this reliable/maintained?" | ... |
| "What if [risk]?" | ... |

## Tagline Options
1. [Tagline A]: [Why this works: emotional angle]
2. [Tagline B]: [Why this works: functional angle]
3. [Tagline C]: [Why this works: aspirational angle]

## Voice & Tone

### Brand Personality
[3-4 adjectives that define the voice, e.g., "Direct, technical, slightly irreverent, helpful"]

### Voice Guidelines
| Do | Don't |
|----|-------|
| [Example of on-brand writing] | [Example of off-brand writing] |

### Tone Shifts by Context
| Context | Tone | Example |
|---------|------|---------|
| Homepage | Confident, clear | "..." |
| Error messages | Helpful, human | "..." |
| Docs | Precise, friendly | "..." |
| Social media | Casual, witty | "..." |
```

Landing page copy, saved as `landing-copy-[product].md`:

```markdown
# Landing Page Copy: [Product Name]

## Hero Section
Headline: [Primary headline]
Subheadline: [Supporting context: who it's for + key benefit]
CTA: [Button text] -> [Where it goes]

## Problem Section
Headline: [The concrete pain in the audience's words: the workaround, the cost, the moment it breaks]
[2-3 sentences describing the problem in the audience's language]

## Solution Section
Headline: [Introduce the product as the answer]
[Brief description of what it does and why it's different]

## Features/Benefits
### [Feature 1 Name]
[Benefit-first description. What the user gets, not what the product does.]

### [Feature 2 Name]
### [Feature 3 Name]

## Social Proof Section
[Recommended structure: testimonials, logos, metrics, or "as seen in"]

## CTA Section
Headline: [Final push: urgency or aspiration]
CTA: [Button text]
Reassurance: [Risk reducer: "Free to start", "No credit card", etc.]
```

Naming exploration, saved as `naming-[category].md`:

```markdown
# Naming Exploration: [Product Category]

## Naming Criteria
- [Must be: memorable, spellable, .com available, etc.]
- [Must evoke: speed, simplicity, power, etc.]
- [Must avoid: generic, already taken, hard to pronounce]

## Name Candidates

### Tier 1 (Recommended)
| Name | Why It Works | Knockout Hits / Risks | Domain Ideas |
|------|-------------|-------|-------------|
| ... | ... | ... | .com / .dev / .io |

### Tier 2 (Strong Alternatives and Wildcards)
[Same table]

## Recommendation
[Which name and why: memorability, domain, trademark risk, audience fit]
```

## Checklist

- [ ] Competitors' positioning researched before the identity was written?
- [ ] 2-3 options given with reasoning for each?
- [ ] Every line written for a specific audience, in their language, with no unsubstantiated buzzwords?
- [ ] Names passed the say-it, spell, search, knockout and global tests, and are labelled a risk screen rather than legal clearance?
- [ ] Hero headline literal, with wordplay confined to tagline options?
- [ ] Files saved under the names above?

## Composition / References

- `launch-pitch-pricing` skill: sales pages, pricing and pitch decks that sit on top of this identity.
- `launch-gtm-plan` skill: supplies the segment and positioning assumption this identity works from.
