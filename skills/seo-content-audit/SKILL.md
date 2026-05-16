---
name: seo-content-audit
title: "On-Page Content SEO Audit"
description: "Operational playbook for diagnosing the on-page content layer of a page or page set: title and meta description optimization, heading structure and voice-search phrasing, search-intent match, AI-citability (answer-first sections, featured snippet blocks, extractable passages, FAQ structure), E-E-A-T proof (author byline, experience signals, named specifics), and information-gain vs the top 10 SERP results. Encodes the per-check rubric, the severity matrix, and the unverified-check escalation rule. Use when auditing the on-page content surface of one or more URLs. Output: prioritized content findings with cited evidence and fix direction."
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

The audit cross-references the target page against the actual SERP — top 10 results, AI Overview presence, "People Also Ask" coverage, voice-search phrasing — and returns findings where the page falls short of what's already winning. Information-gain (what does this page add that the top 10 doesn't) is the 2026 ranking gate; an information-gain-zero page is now actively suppressed as AI-derivable filler.

## Mental model

On-page content audit is intent-versus-execution:

1. What is the target SERP rewarding? (intent, format, depth, structure)
2. What does the target page actually deliver? (against the same dimensions)
3. Where is the gap? (intent mismatch, structural deficit, missing experience proof, no novel signal)
4. What's the cheapest fix per unit of ranking lift?

The audit is not "compare to a checklist." It's "compare to the SERP." Generic on-page advice (keyword in title, keyword in H1) is necessary but not sufficient in 2026. Sufficient is matching the format, depth, and experience signal of the pages that already rank.

## Instructions

### Fetch protocol (parallel, ONE block)

- `webfetch` the target URL — capture title, meta, headings, body, byline, any visible schema-rendered elements.
- `websearch` the target keyword — capture top 10 organic, AIO presence, "People Also Ask", "Related searches", featured snippet holder.
- `webfetch` 3–5 top-ranking pages from the SERP — for direct comparison.
- `websearch` "[target keyword] site:reddit.com" — capture community discussion (load-bearing for AI citation in 2026).

Run all four in one block. Don't serialize.

### Check rubric

| # | Check | How to verify | Severity if failed |
|---|---|---|---|
| 1 | Intent match | Read the target keyword aloud — what does the searcher want? Compare to page intent. | Critical if format mismatches dominant SERP intent |
| 2 | Title tag | 50–60 chars, primary keyword front-loaded, compelling (clear value, not generic) | Moderate per failed dimension |
| 3 | Meta description | 150–160 chars, keyword present, answers "why click this result" | Moderate per failed dimension |
| 4 | H1 | Present, unique, semantically related to title (not identical), describes the page's promise | Critical if missing or duplicate |
| 5 | H2 structure | Voice-search phrasing where natural ("What is X?", "How to Y", "Why Z") — voice/AI assistants match conversational queries | Moderate if all headings are noun-phrase labels |
| 6 | Answer-first per section | 40–50 word direct answer immediately after each H2, before longer body | Moderate per H2 that buries the answer |
| 7 | Extractable passages | Each major point is a self-contained ~150-word unit that works as a standalone answer | Moderate if key answers require reading multiple paragraphs to reconstruct |
| 8 | Data density | At least one concrete number, percentage, or statistic per major section | Minor per data-free section; Moderate if entire piece lacks specifics |
| 9 | FAQ section | Present and recommended for the intent class (informational and commercial benefit most; 2.8x AI-citation lift with FAQ schema) | Minor if absent and intent is suitable |
| 10 | Author byline | Real name + role + credentials + outbound link (LinkedIn / publication / org bio). "Admin" or anonymous = Critical | Critical if anonymous or generic-name attribution |
| 11 | Experience proof | Original screenshots / dashboards / photos from the field / named tools+versions / time-boxed case-study language | Critical if pure explainer with no experience signal on YMYL or expertise-required topic |
| 12 | Information gain vs top 10 | Identify the specific thing this page adds (original data, contrarian take, novel synthesis, practitioner detail) that the top 10 doesn't | Critical if the page is reconstructable from the top 10 (information-gain-zero) |
| 13 | Internal linking | 5–10 contextual links per piece; descriptive anchors (not exact-match); pillar/cluster pattern present where applicable | Moderate if under 3 internal links or all anchor text is generic |
| 14 | Schema readiness for content | Article schema present with author/datePublished/dateModified; FAQ schema if FAQ section exists; HowTo if procedural | Moderate per missing schema on eligible content |
| 15 | Primary-source posture | Page presents primary data/experience/original synthesis OR cites primary sources where it relies on them | Critical if the page is an intermediary roundup of other rankers without added signal (March 2026 update demoted intermediary pages — 80% of top-3 shifted) |

### Severity matrix

- Critical — directly suppresses ranking under 2026 systems: anonymous byline on YMYL, information-gain-zero, intent format mismatch with SERP, intermediary-only positioning, missing H1.
- Moderate — degrades extraction or comprehension: missing answer-first block, weak title/meta, no FAQ where intent supports one, schema gaps on eligible content.
- Minor — polish: data-free secondary sections, internal-link count slightly low, descriptive anchor tweaks.

Information-gain is the most ranking-relevant 2026 signal — when in doubt, weight it Critical.

### How to score information gain

Before scoring, fetch and skim 3–5 top-ranking pages. Identify everything the SERP already says. Then score the target on:

- Original data, survey, internal benchmark, measurement, or proprietary statistic.
- First-hand case study with named specifics (time-boxed, named tools, named costs, named errors).
- Contrarian take supported by evidence (not just opinion).
- Synthesis across sources nobody else combined.
- Practitioner detail the ranking pages skip (edge cases, real failure modes, gotchas, actual cost).

If you cannot name what the target page adds that the top 10 doesn't, that is the finding: "Information-gain-zero — page reconstructable from current top 10. Highest-priority fix."

### Voice-search and AI-citation phrasing

Voice and AI assistants match conversational queries verbatim. H2s should sound like the spoken query, not the SEO-token version:

- "What is topical authority?" beats "Topical Authority"
- "How to set up FAQ schema" beats "FAQ Schema Setup"
- "Why does my INP score keep dropping?" beats "INP Score Troubleshooting"

When auditing H2s, count the number phrased as spoken queries vs noun-phrase labels. Flag if fewer than half are conversational.

### AI Overview interaction

When auditing a page targeting a keyword that triggers AI Overviews:

- Check whether the page's snippet block (the 40–50 word direct answer after H2) is self-contained — AI Overviews quote these verbatim.
- Check whether the page is being cited in the AI Overview (manual search with the keyword in incognito; capture citation list).
- If the AIO cites competitors but not this page, the gap is extractability: the competitors structured their answer for extraction; this page didn't.
- Citation share is now a measurable KPI alongside rank. Tools: Otterly.ai, Semrush AI Toolkit, Ahrefs Brand Radar, Profound. Recommend monitoring setup as part of the audit hand-off.

### Unverified checks — escalation rule

- Top-10 fetch blocked or rate-limited → "Unverified: cannot fetch SERP competitors; information-gain scoring depends on this. Recommend manual SERP review or share top-3 page snapshots."
- AI Overview check impossible (no manual search done) → "Unverified: AIO presence unknown; rerun the audit with a manual incognito search captured."
- Author identity unclear from the page → "Unverified: author byline ambiguous; confirm author name + credentials before scoring E-E-A-T."

Never infer information gain from one source; never grade an anonymous byline before checking if there's an author bio page linked.

### Output

Use the canonical output structure from the agent that runs this skill. Every finding includes: severity, evidence (URL section, line, the missing element, the SERP comparison point), why it matters, fix direction. Save as `seo-audit-[slug]-[YYYY-MM-DD].md` in working directory.

## Checklist

- [ ] All four fetch operations ran in parallel
- [ ] SERP fetched and top 3–5 competitors read before scoring information gain
- [ ] Every check in the rubric was evaluated or flagged as Unverified
- [ ] Intent classified before format/structure assessment
- [ ] Information-gain explicitly articulated (what does this page add) — flagged Critical if absent
- [ ] E-E-A-T scored with named author + credentials + experience signals
- [ ] AIO presence checked and citation-share recommendation included if triggered
- [ ] Schema readiness checked per content type (Article / FAQ / HowTo / Person)
- [ ] Voice-search H2 phrasing counted; flagged if under half
- [ ] Each finding cites concrete evidence (URL section, line, missing element, SERP-comparison reference)
- [ ] Report saved to disk with timestamped filename

## Composition / References

Within-domain pairings:
- Pairs with the sibling SEO skill that audits the structural / technical layer (crawlability, schema validity, CWV, indexability).
- Pairs with the sibling SEO skill that audits link profile (referring-domain quality, anchor distribution).

External authoritative sources:
- [Google Search Central — Helpful Content guidance](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- [Google Search Central — E-E-A-T and quality rater guidelines](https://developers.google.com/search/blog/2022/12/google-raters-guidelines-e-e-a-t)
- [Google Search Central — Generative AI in Search optimization](https://developers.google.com/search/docs/appearance/ai-features)
- [Search Engine Journal — Information gain patent analysis](https://www.searchenginejournal.com/google-information-gain-patent/)
- [Princeton/Georgia Tech — GEO research paper](https://arxiv.org/abs/2311.09735) — original framework for AI-citation optimization
