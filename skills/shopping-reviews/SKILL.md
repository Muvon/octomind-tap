---
name: shopping-reviews
title: "Amazon Review Analyzer – Cross-Retailer Review Summary"
description: "Amazon review analyzer for one exact product across Amazon and other retailers: samples positive, middling and negative reviews, separates variants and seller issues, finds recurring praise and failures, and weighs fake-review signals without accusations. Use when the user asks what owners say, whether reviews are fake, to check reviews, or for a review summary of a product."
license: Apache-2.0
compatibility: "Requires: web search and web page fetching."
domains: shopping
rules:
  - content(reviews)
  - match((?i)\b(fake|customer|owner|amazon|user|verified) reviews?\b)
  - match((?i)\bwhat (do )?(owners|buyers|people) say\b)
---

## Overview

Star ratings hide what owners actually experience. This skill reads customer reviews of one identified product across Amazon and at least one other retailer, separates recurring praise and failures from isolated stories, variant confusion and questionable review patterns, and ends with who the product suits. The result is an honest account of what the accessible evidence supports. It is not a star-rating paraphrase and not a certificate of review authenticity.

## Mental model

Reviews are a sample, not a population. Every statement is limited to what was actually read, at which retailer, on which date, for which variant. Plain and fair beats dramatic: "several owners report a loose hinge" is useful, "everyone hates it" is not. Themes matter through their consequences for the buyer's real use case.

## Rules

### Workflow

1. Identify: confirm the exact product, model, generation, variant and country from the user's link or name. Ask one focused question if a mismatch would change the analysis.
2. Locate: use web search to find customer-review pages at two or more retailers, then read them with `knowledge(command="read", source="<url>")`. Search snippets and editorial roundups are not a review corpus.
3. Sample: read accessible positive, middling and negative reviews across dates. Record retailer, source URL, retrieval date, visible sample size and any sorting or access limits.
4. Separate: exclude unrelated variants. Distinguish product faults from delivery, seller-service, setup or compatibility complaints. Keep older versions and later revisions apart.
5. Synthesize: identify repeated strengths, repeated failures and conflicting experiences. Check whether apparently independent reports are duplicated or syndicated across sites.
6. Assess: explain credibility signals cautiously, then connect the supported themes to who the product suits, who should avoid it and what the evidence cannot settle.

### Evidence

- Cite the live review page for each material theme, with review dates where visible. Never fabricate quotations, counts, ratings, references or access to reviews you could not read.
- Seek independent reports across retailers. Duplicated or syndicated text counts as one report, and a retailer's displayed total is not the number you examined.
- Describe patterns within the observed sample, not population defect rates. Give denominators for any computed fraction, and don't combine incompatible rating scales into a new score.
- Treat a single severe complaint as an isolated report unless corroborated. "Not seen in this sample" does not mean "does not happen".
- Weight recent, detailed use reports and long-term follow-ups over vague star ratings. Sorting, self-selection and small samples can distort the picture.
- Reviews pooled across sizes, generations or accessories can mislead. Attribute each theme to the verified variant or mark the variant unknown.
- Keep owner experiences apart from verified specs, marketing and editorial tests. If a spec or current price is needed, check it live and cite the manufacturer or retailer with date and currency.
- If only one retailer is accessible or pages require a login, say so. Don't bypass access controls and don't present partial coverage as a cross-retailer consensus.

### Credibility signals

- Possible fake-review signals: unusual timing bursts, repeated wording, generic praise, irrelevant product references and disclosed incentives. Show the evidence and the plausible innocent explanations.
- Verified-purchase labels, incentives and reviewer history are context, not proof of authenticity or fraud.
- Don't assign an invented fake-review percentage. Don't accuse a reviewer or seller without substantiation. Report observable signals and their limits, with no authenticity verdict.

### Safety and limits

- Reviews cannot establish medical efficacy, legal rights or product safety. Verify recalls and safety issues with current official sources, flag unresolved risks, and point to qualified professionals when appropriate.
- Don't offer financial advice or recommend regulated medical devices. Affordability, investment and clinical suitability are outside a review summary.
- Don't equate star ratings with quality, authenticity or safety.
- Contacting reviewers or sellers and publishing reviews stay with the user.

### Output shape

- Product and coverage: exact variant, retailers and URLs, retrieval dates, visible samples and gaps.
- Recurring praise: theme, supporting sources and practical benefit.
- Recurring failures: theme, supporting sources, severity and variant or date caveats.
- Credibility signals: observable evidence, uncertainty and alternative explanations.
- Who it suits and who should avoid it: grounded in the themes and the user's use case.
- Bottom line: strongest supported conclusion, confidence rationale and unresolved questions.

Keep observed patterns, tentative interpretations and unknowns visibly separate. Conflicting owner reports get a check of variant, dates and use conditions, and the disagreement stays in the brief if it cannot be resolved.

### Running without a human

- Chatting directly: ask one focused question when the product identity is unclear, then proceed.
- Brief marked AUTONOMOUS or non-interactive: ask nothing. Proceed with the best-supported model identity, list assumptions and coverage limits at the top, deliver the brief, and keep every unverified item labeled.

## Examples

Review request on one listing:

- Bad: Summarizing the star distribution on the Amazon page the user pasted.
- Good: Identify the exact listing, then read reviews at one or more other retailers before describing any broader pattern.

Fake-review question:

- Bad: "Yes, these reviews are fake, most are paid."
- Good: "Several of the reviews I read share near-identical wording and were posted within days of each other. That is a timing and wording signal, but a launch promotion could explain it. The sample cannot support a verdict."

Conflicting reports:

- Bad: Averaging a loud failure story with praise and calling the product mixed.
- Good: Check variant, dates and use conditions; if the split remains, report it as unresolved with the sources on each side.

## Checklist

- [ ] Exact product, variant and country confirmed, or assumed and stated.
- [ ] Two or more retailers read, or the single-retailer limit stated.
- [ ] Positive, middling and negative reviews sampled, with dates and sample size recorded.
- [ ] Variant, seller and delivery complaints separated from product faults.
- [ ] Duplicated or syndicated text counted once.
- [ ] Every theme cited to a live review page, with no invented quotes or counts.
- [ ] Credibility signals shown with innocent explanations and no accusation.
- [ ] Output covers coverage, praise, failures, credibility, fit and bottom line.
- [ ] Unverified items labeled.

## Composition / References

- `shopping-gifts` handles recipient-led gift ideas; use it before analyzing reviews of a chosen gift.
- Recalls and safety notices: link the current regulator page for the buyer's country.
