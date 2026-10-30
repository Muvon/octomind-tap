---
title: "GEO Audit Report Templates"
description: "Report templates for buyer questions, AI answer captures, citation findings, source actions, and before-and-after checks in a GEO audit."
---

# GEO Audit Report Templates

Use only the records needed for the selected mode; don't expand a one-question request into a full-site assessment. Use stable IDs to connect decisions, observations, findings, source actions, and retests. Blank or unavailable data is Unknown/Unverified, never an invented zero. Examples below are synthetic, not observed engine results.

## Report shape by mode

| Mode | Required sections | File when saved |
|---|---|---|
| Question discovery | Scope and assumptions; decision/question register; priority rationale; test protocol; evidence/access requests | `geo-questions-[slug]-[YYYY-MM-DD].md` |
| Visibility audit | Scope and coverage; baseline observations; question-to-page map; prioritized findings; cited-source actions; retest conditions; unverified checks | `geo-audit-[slug]-[YYYY-MM-DD].md` |
| Experiment brief | Referenced findings; selected interventions; owners/dependencies; separate visibility/business metrics; acceptance criteria; review dates | `geo-plan-[slug]-[YYYY-MM-DD].md` |
| Retest | Matched cohort and conditions; before/after counts; change log; concurrent changes; outcome/uncertainty; next decision | `geo-retest-[slug]-[YYYY-MM-DD].md` |

Follow the host agent's save policy, but use this mode-specific shape instead of its generic SEO template for a GEO request. Don't alter site/content source files. Link supporting captures/exports by stable artifact location and capture time; retain an untouched source version, redact personal data from reports, and keep credentials out of artifacts.

## Scope header

Record product/domain and owned-domain allowlist; buyer and user (if different); market/language; decision; desired conversion and activation event/time window; selected questions and engines/surfaces; observation and comparison dates; planned/completed/error/missing counts; available access; inventory coverage and sampling exclusions. Define brand aliases to avoid counting homonyms. A provisional discovery artifact may leave the activation event Unknown.

## Question register

| ID | Buyer decision/stage | Observed need: source/date or Hypothesized | Google query | Exact AI prompt | Branded? | Evidence a useful answer needs | Existing URL/coverage | Priority rationale |
|---|---|---|---|---|---|---|---|---|
| Q01 | Client-facing consultant: shortlist without meeting bot | Hypothesized | meeting notes tool without bot client calls | Which meeting note tools work without a bot joining client calls, and what are their recording and consent limitations? | No | Supported capture methods, platform constraints, consent documentation | Unknown; inspect inventory | High fit; demand unverified |

Version the register; paraphrases receive explicit variant IDs and stay separate in comparisons. Preserve the same buyer context across the query/prompt pair without claiming equivalent Google and AI intent, results, or volume. Record excluded questions and reasons, especially branded opportunity queries unrelated to the product's actual fit.

## Observation ledger

One row per planned prompt × surface × replicate, including failures:

| Trial ID | Question/version | Engine/product, model if known | UI/API, search mode | UTC time, locale/language, session conditions | Status | Answer artifact | AI answer present? | Brand mentioned? | Brand recommended? | Owned domain cited? | Cited URLs with passage/claim mapping |
|---|---|---|---|---|---|---|---|---|---|---|---|

Status is Completed, Error, or Missing. Completed includes a rendered result with no AI answer; label refusals separately. Error/Missing boolean outcomes are Unknown, not No. Where an answer artifact omits its source list, citation outcomes remain Unknown even if mention/recommendation outcomes are scorable. Don't overwrite failed attempts with successful retries; link retries and declare which attempt is used in comparisons.

- Mention: an unambiguous brand alias appears in answer prose, including negative or neutral mentions; record sentiment/incorrect claims separately. A source-list label alone isn't a prose mention.
- Recommendation: the answer explicitly offers the brand as a suitable choice for the stated decision. A mere mention, exclusion, or quoted criticism isn't a recommendation.
- Owned-domain citation: an actual displayed source link resolves to the declared owned-domain allowlist. A third-party page mentioning the brand is a separate source-representation record, not an owned citation.
- Inspect exact cited pages, not just homepages. Store displayed URL and resolved canonical URL when verified, capture date, relevant short excerpt/section, claim supported, brand/competitor treatment, and fetch limitations. A URL appearing only in the auditor's discovery search isn't an observed engine citation.
- A refusal is a completed generated response, not a missing capture or a feature-level no-answer result. Label it separately, score mention/recommendation only from its actual prose, and retain the original answer.
- Citation quality is assessed per claim–citation mapping, not per domain reputation. Use Supported, Contradicted, Outdated, Irrelevant, or Unverified; every assessed mapping needs the claim, an inspected excerpt, and a dated evidence location. A source can support one claim and contradict another.

## Findings and source-action records

Each finding records:

```text
Finding ID / question IDs / trial IDs:
Observation (what the captures or page checks show):
Evidence locations and dates:
Existing URL and inventory coverage:
Diagnosis: missing page | weak page | retrieval barrier | source gap | incorrect claim | unknown
Confidence: High | Medium | Low, with reason
Causal explanation: hypothesis unless independently established
Severity: Critical | Moderate | Minor | Opportunity, with consequence
Scheduling priority: P0 | P1 | P2, with buyer impact, demand evidence, confidence, effort
Fix direction OR next discriminating check:
Owner / dependencies / retest criterion:
```

Critical means a demonstrated blocker or materially harmful error on an important decision; Moderate means a substantiated answer/representation weakness; Minor means local polish. Absence alone is an Opportunity, not automatically a defect. High confidence needs direct, mutually consistent evidence; a single omission supports an observation, not a high-confidence causal diagnosis.

Source actions link finding/question/trial IDs, exact URL, source type, passage, observed competitor treatment, OWN/CLAIM/EARN/CONTEST class, specific proposed action, owner, required authorization, and success check. Factual correction needs a dated primary source; unfavorable accurate reviews aren't correction targets.

Entity-consistency findings record entity/product and aliases; specific property (capability, price/plan, ownership, market availability, or policy); exact owned/cited statement; dated primary-source statement; applicable market/version; discrepancy or Unknown; linked question/trial IDs; owner; and permitted source-action class. Don't infer an error from a different legitimate product variant or missing listing, and don't promise a knowledge panel or profile correction will change recommendations.

## Metric definitions

Report numerators and denominators per surface, prompt cohort/version, branded status, and window. Zero denominator means N/A. Preserve Unknown fields and report metric-specific coverage; don't treat missing source lists as no citations.

| Metric | Explicit definition |
|---|---|
| Completion | Completed trials / planned trials; disclose errors, missing captures, retries and selection rules |
| Answer availability | Trials with an AI answer / completed trials with known answer-availability status |
| Mention rate | Trials with brand in answer prose / completed trials with scorable prose outcomes |
| Recommendation rate | Trials explicitly recommending brand / completed trials with scorable recommendation outcomes |
| Owned-domain citation rate | Trials with at least one owned-domain citation / completed trials with known citation outcomes |
| Owned-domain citation share | Deduplicated owned cited URLs / all deduplicated cited URLs, deduplicating within each trial before summing; disclose this local counting rule |
| Citation assessment coverage | Assessed claim–citation mappings / all captured mappings; Unverified mappings remain outside the assessed denominator |
| Citation support rate | Supported mappings / assessed mappings (Supported + Contradicted + Outdated + Irrelevant); report the separate failure classes and coverage |
| Activation conversion | Attributed unique users reaching the defined event within its window / eligible attributed unique users with a complete follow-up window; don't divide users by sessions |

For a completed result with no AI answer, visibility outcomes are No and it remains in applicable denominators. Report answer availability alongside these rates so feature changes aren't confused with brand gains. When prose or source lists are incomplete, metric-specific denominators differ; show that missingness rather than pooling incomparable rates. Don't equate this local citation-share formula with a vendor's similarly named metric or with third-party brand references.

Keep Google query/page performance, engine observations, Bing publisher reports, and acquisition/activation in separate tables. Label overlapping Google Web/AI coverage; vendor figures retain their stated units and sampling scope. Bing grounding queries are retrieval phrases, not necessarily verbatim customer prompts. Referral evidence can establish attributable visits, not which sampled prompt caused them.

## Retest contract

For each intervention record finding IDs, implementation evidence/date, one primary change, owner, hypothesis, comparison cohort, baseline counts, expected direction, acceptance threshold, review date, and propagation rationale. Use identical question versions, surfaces, search modes, locale/session conditions, sampling effort, and windows where practical. If a model or product changes, mark a comparability break rather than hiding it.

Example: after a verified consent section is added to an existing page, repeat Q01 on the same surface with three new independent runs and an unchanged question as a comparison. Report 0/3 → 1/3 owned-citation observations as a small-sample directional result, not significant uplift; when the baseline is zero, percent growth is undefined. Check citation correctness as well as counts. Activation impact stays Unverified without attributable user/event data.

End with a decision: retain, revise, stop, or collect more evidence, and why. Continued absence with an adequate, retrievable page does not justify endless content expansion. Never declare an intervention implemented or successful from its brief alone.

## Working format

Use the records above in Markdown, a spreadsheet, or the user's existing reporting system. Keep original captures and exports linked alongside the report; no custom schema or conversion step is required.
