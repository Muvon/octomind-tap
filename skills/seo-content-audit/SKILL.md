---
name: seo-content-audit
title: "On-Page Content SEO Audit"
description: "Operational playbook for diagnosing the on-page content layer of a page or page set: title and meta description optimization, heading structure, search-intent match, answer placement and AI-search visibility per Google's 2026 guidance, E-E-A-T proof (author byline, experience signals, named specifics), and information-gain vs the top 10 SERP results. Encodes the per-check rubric, the severity matrix, and the unverified-check escalation rule. Use when auditing the on-page content surface of one or more URLs. Output: prioritized content findings with cited evidence and fix direction."
license: Apache-2.0
compatibility: "Stack-agnostic. Requires webfetch (target page + top-10 SERP pages) and websearch (SERP for the target keyword + competitor pages)."
domains: seo
rules:
  - session(seo)
  - session(audit)
  - content(audit)
  - content(on-page)
  - content(title)
  - content(meta description)
  - content(headings)
  - content(intent)
  - content(EEAT)
  - content(E-E-A-T)
  - match(\b(audit|review|inspect)\s+.{0,40}(content|page|article|post)\b)
  - match(\b(on-?page|onpage)\s+seo\b)
  - match(\b(title\s+tag|meta\s+(description|tag)|heading\s+structure)\b)
  - match(\b(search\s+intent|intent\s+match|user\s+intent)\b)
  - match(\b(answer-?first|featured\s+snippet|extractable\s+passage|ai\s+citation)\b)
  - match(\b(e-?e-?a-?t|experience\s+signal|author\s+byline)\b)
  - match(\binformation\s+gain\b)
  - semantic(audit the on-page SEO of this article)
  - semantic(check if this page is structured for AI citation)
  - semantic(diagnose content gaps against the ranking competitors)
  - semantic(review search intent match for this page)
  - semantic(check E-E-A-T signals on this content)
---

## Overview

A page can pass every structural check, load fast, validate every schema, and still rank nowhere — because the content doesn't match search intent, the headings bury the answer, the byline says "Admin," or the top 10 already covers everything this page says. This skill diagnoses the on-page layer that the structural audit can't see: how the content is shaped against the SERP it wants to win.

The audit cross-references the target page against the actual SERP — top 10 results, "People Also Ask"-style questions, AI Overview presence where it can be observed — and returns findings where the page falls short of what's already winning. Information gain (what does this page add that the top 10 doesn't) is the priority test: Google's May 2026 AI optimization guide asks for non-commodity, first-hand content, and third-party readings of the March and May 2026 core updates saw original sources gain over aggregators.

## Mental model

On-page content audit is intent-versus-execution:

1. What is the target SERP rewarding? (intent, format, depth, structure)
2. What does the target page actually deliver? (against the same dimensions)
3. Where is the gap? (intent mismatch, structural deficit, missing experience proof, no novel signal)
4. What's the cheapest fix per unit of ranking lift?

The audit is not "compare to a checklist." It's "compare to the SERP." Generic on-page advice (keyword in title, keyword in H1) is necessary but not sufficient in 2026. Sufficient is matching the format, depth, and experience signal of the pages that already rank.

## Instructions

### Fetch protocol (parallel, ONE block)

- Read the target URL with `knowledge(command="read", source="<url>")` — title, meta, headings, body, byline, JSON-LD.
- Web search the target keyword — capture the ranking competitors and related questions.
- Read 3–5 top-ranking pages with `knowledge` — for direct comparison.
- Web search "[target keyword] site:reddit.com" — capture community phrasing and discussion.

Run all four in one block. Don't serialize. The web search tool is not Google Search: AI Overview / AI Mode presence, featured-snippet holders, and People Also Ask are Unverified unless the user supplies a screenshot or Search Console data.

### Check rubric

| # | Check | How to verify | Severity if failed |
|---|---|---|---|
| 1 | Intent match | Read the target keyword aloud — what does the searcher want? Compare to page intent. | Critical if format mismatches dominant SERP intent |
| 2 | Title tag | Describes the page accurately and concisely; distinct from sibling pages; relevant terms read naturally | Flag a specific mismatch, missing title, or confusing boilerplate; length alone isn't a failure |
| 3 | Meta description | A useful, page-specific summary consistent with the visible content; no keyword list or unsupported promise | Flag missing or misleading descriptions as appropriate; exact-match keywords and fixed lengths aren't requirements |
| 4 | H1 | Present, unique, semantically related to title (not identical), describes the page's promise | Critical if missing or duplicate |
| 5 | H2 structure | Headings describe what each section answers; question phrasing where it reads naturally | Minor if headings are vague labels that hide the content |
| 6 | Answer placement | The direct answer to the section's question appears early, before supporting detail | Moderate per key section that buries its answer |
| 7 | Self-contained sections | Each major point reads on its own without reconstructing it from several paragraphs | Minor; don't recommend splitting content into fragments — Google says chunking isn't needed |
| 8 | Data density | At least one concrete number, percentage, or statistic per major section | Minor per data-free section; Moderate if entire piece lacks specifics |
| 9 | FAQ section | Present when users genuinely ask follow-up questions (informational and commercial intent) | Minor if absent and intent is suitable; FAQ rich results ended May 7, 2026, so judge it on reader value only |
| 10 | Author byline | Real name + role + credentials + outbound link (LinkedIn / publication / org bio). "Admin" or anonymous = Critical | Critical if anonymous or generic-name attribution |
| 11 | Experience proof | Original screenshots / dashboards / photos from the field / named tools+versions / time-boxed case-study language | Critical if pure explainer with no experience signal on YMYL or expertise-required topic |
| 12 | Information gain vs top 10 | Identify the specific thing this page adds (original data, contrarian take, novel synthesis, practitioner detail) that the top 10 doesn't | Critical if the page is reconstructable from the top 10 (information-gain-zero) |
| 13 | Internal linking | 5–10 contextual links per piece; descriptive anchors (not exact-match); pillar/cluster pattern present where applicable | Moderate if under 3 internal links or all anchor text is generic |
| 14 | Schema readiness for content | Article schema present with author/datePublished/dateModified; markup matches visible text | Moderate per invalid or contradicting markup; Google states AI features need no special schema |
| 15 | Primary-source posture | Page presents primary data/experience/original synthesis OR cites primary sources where it relies on them | Critical if the page is an intermediary roundup of other rankers without added signal |

### Title and description review

- Read the page before choosing search wording; name the actual deliverable, not a broader product or service it doesn't provide.
- Review query intent and competing results when selecting a keyword. A volume lookup alone doesn't establish fit, attainable rankings, or likely traffic; mark missing evidence rather than claiming a complete SEO pass.
- Write concise, distinct titles and readable page-specific descriptions. Don't force the same phrase into every reference file or pad a description to a character target.
- Google specifies no fixed title or meta-description length limit; display truncation depends on available width. Registry field limits are a separate contribution constraint.
- Check the served HTML title, description, canonical, and applicable indexing/snippet directives when a public URL exists. Frontmatter validation isn't deployment or indexing verification.
- Use an existing authorized SEO-data connection or supplied export when numbers are needed. Don't add a custom API client just to research metadata.

### Severity matrix

- Critical — directly suppresses ranking under 2026 systems: anonymous byline on YMYL, information-gain-zero, intent format mismatch with SERP, intermediary-only positioning, missing H1.
- Moderate — degrades extraction or comprehension: buried answers, weak title/meta, invalid or contradicting schema.
- Minor — polish: data-free secondary sections, internal-link count slightly low, descriptive anchor tweaks.

Information gain is the highest-leverage content check — when in doubt, weight it Critical.

### How to score information gain

Before scoring, fetch and skim 3–5 top-ranking pages. Identify everything the SERP already says. Then score the target on:

- Original data, survey, internal benchmark, measurement, or proprietary statistic.
- First-hand case study with named specifics (time-boxed, named tools, named costs, named errors).
- Contrarian take supported by evidence (not just opinion).
- Synthesis across sources nobody else combined.
- Practitioner detail the ranking pages skip (edge cases, real failure modes, gotchas, actual cost).

If you cannot name what the target page adds that the top 10 doesn't, that is the finding: "Information-gain-zero — page reconstructable from current top 10. Highest-priority fix."

### Headings, answer placement, and AI features

Google's May 2026 AI optimization guide says AI Overviews and AI Mode need no special phrasing, chunking, llms.txt, or schema, and that a page per query variation counts as scaled content abuse. Audit structure for readers, not for a machine:

- Headings that say what the section answers ("How to set up FAQ schema" beats "Schema") help readers and passage extraction alike; don't flag a page for lacking question-form H2s.
- If an AI Overview cites competitors but not this page, look first at information gain, answer clarity, and indexability — not at formatting tricks.
- Search Console's Generative AI performance report shows impressions, not clicks, for AI Overviews and AI Mode, and Web performance totals also include them; verify live dimensions before claiming query-level presence. Use actual answer captures for prompt-level visibility, scoped vendor observations as samples, and separate attributable activation data for business outcomes.

### Unverified checks — escalation rule

- Top-10 fetch blocked or rate-limited → "Unverified: cannot fetch SERP competitors; information-gain scoring depends on this. Recommend manual SERP review or share top-3 page snapshots."
- AI Overview check impossible (search tool isn't Google) → "Unverified: AIO presence unknown; share a dated live-result capture with exact query, locale, and source links, or a documented SERP-data observation. Search Console Web aggregates don't establish query-level AIO presence."
- Author identity unclear from the page → "Unverified: author byline ambiguous; confirm author name + credentials before scoring E-E-A-T."

Never infer information gain from one source; never grade an anonymous byline before checking if there's an author bio page linked.

### Output

Use the canonical output structure from the agent that runs this skill. Every finding includes: severity, evidence (URL section, line, the missing element, the SERP comparison point), why it matters, fix direction. Save as `seo-audit-[slug]-[YYYY-MM-DD].md` in working directory.

For an explicit GEO/AEO request, retain the host's focused `geo-visibility-audit` mode and report shape. Apply only content checks justified by the selected buyer question/finding; don't expand it into a full conventional audit or propose a new page without checking existing coverage.

## Checklist

- [ ] All four fetch operations ran in parallel
- [ ] SERP fetched and top 3–5 competitors read before scoring information gain
- [ ] Every check in the rubric was evaluated or flagged as Unverified
- [ ] Intent classified before format/structure assessment
- [ ] Information-gain explicitly articulated (what does this page add) — flagged Critical if absent
- [ ] E-E-A-T scored with named author + credentials + experience signals
- [ ] AIO presence checked from user-supplied evidence or flagged Unverified; AI-visibility monitoring recommended in the hand-off
- [ ] Schema checked for validity and match with visible text (Article / Person / Organization); retired FAQ/HowTo rich results not counted as lost visibility
- [ ] No finding asks for chunking, llms.txt, or AI-specific phrasing — Google says none is needed
- [ ] Each finding cites concrete evidence (URL section, line, missing element, SERP-comparison reference)
- [ ] Report saved to disk with timestamped filename

## Composition / References

Within-domain pairings:
- Pairs with the sibling SEO skill that audits the structural / technical layer (crawlability, schema validity, CWV, indexability).
- Pairs with the sibling SEO skill that audits link profile (referring-domain quality, anchor distribution).

External authoritative sources:
- [Google Search Central — Helpful Content guidance](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- [Google Search Central — E-E-A-T and quality rater guidelines](https://developers.google.com/search/blog/2022/12/google-raters-guidelines-e-e-a-t)
- [Google Search Central — Title links](https://developers.google.com/search/docs/appearance/title-link)
- [Google Search Central — Snippets and meta descriptions](https://developers.google.com/search/docs/appearance/snippet)
- [Google Search Central — AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)
- [Google Search Central — Optimizing for generative AI features (May 2026)](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)
- [Search Engine Journal — Information gain patent analysis](https://www.searchenginejournal.com/google-information-gain-patent/)
- [Princeton/Georgia Tech — GEO research paper](https://arxiv.org/abs/2311.09735) — original framework for AI-citation optimization
