---
name: sales-proposals
title: "Proposal Writing: RFP Response and Bid Decision"
description: "RFP and proposal writing: bid/no-bid scoring, compliance matrices, win themes with proof, evaluator-focused drafts, color-team review. Use for any RFP."
license: Apache-2.0
compatibility: "Requires the document-export tooling (pandoc, typst, poppler-utils) for DOCX and PDF output. macOS/Linux."
capabilities: shell documents
rules:
  - match((?i)\b(respond to|answer|shred|pull out|extract|go through)\b.{0,40}\b(rfp|rfq|rfi|tender|solicitation)\b)
  - match((?i)\b(bid[/ -]?no[- ]?bid|go or no-go|should we (even )?bid|compliance matrix|win themes?|color[- ]team|(pink|red|gold)[- ]team|pwin)\b)
  - match((?i)\bsecurity questionnaire\b|\b(sig lite|caiq|hecvat)\b)
  - match((?i)\b(past[- ]performance|section [lm]\b|evaluation (factors|criteria)|evaluators?)\b)
  - match((?i)\b(write|draft|improve|review|outline)\b.{0,25}\b(proposal (outline|section|volume|response)|executive summary|technical (approach|volume)|management volume)\b)
  - match((?i)\b(rfp|rfq|solicitation)\b.{0,40}\b(draft|response|requirements?|bid)\b)
  - semantic(should we bid on this rfp)
  - semantic(build a compliance matrix and win themes for this tender, 0.71)
  - semantic(draft the executive summary and technical approach for our bid, 0.75)
---

## Overview

This skill turns solicitations into compliant, evaluator-friendly proposals, using disciplined capture methodology (Shipley-style). It decides whether a bid is worth chasing, extracts every requirement into a compliance matrix, builds win themes from real discriminators, and drafts sections the way evaluators score them. Compliance comes first: a brilliant proposal that misses a mandatory requirement scores zero.

## Mental model

- Evaluators score, they don't read. Findable beats eloquent.
- A theme without proof is a slogan.
- Chasing every bid is how win rates die.

## Rules

### Scope

Covered: bid/no-bid analysis with PWin scoring, RFP shredding into a compliance matrix, win-theme development, proposal outlines mapped to evaluation criteria, section drafting, executive summaries, past-performance write-ups, security-questionnaire answers, color-team-style review passes (compliance check, then scoring simulation), and reusable content library curation.

Instructions versus criteria: in US federal work these are Section L (instructions) and Section M (criteria). Since the 2025-26 Revolutionary FAR Overhaul, agencies issue Part 15 class deviations, so follow the solicitation's own instructions and provisions over legacy FAR 15 citations. For UK, EU and commercial RFPs, use the solicitation's own instructions and scoring rubric.

Not covered: pricing strategy and rates (a human decision: structure the pricing volume, never set numbers), startup pitch decks and investor materials, contract negotiation and legal terms, and certifications or registrations the organization doesn't hold, which are never claimed.

### Workflow

1. Ingest the RFP document (convert Word or PDF to text with `pandoc <file.docx> -t gfm` or `pdftotext -layout <file.pdf> -`), the deadline, the incumbent situation and the organization's real capabilities. Remember "proposals", "win themes", "past performance" and "content library".
2. Bid/no-bid: score before writing anything: customer relationship, requirement fit, incumbent strength, price competitiveness, capacity to deliver. Low PWin means recommend no-bid with reasoning.
3. Shred: extract every "shall", "must", "will provide" and submission instruction into the compliance matrix, including the format rules (font, size, spacing, margins, paper, page limits and what counts toward them, file type, file naming). Instructions and evaluation criteria often disagree: flag conflicts for a clarifying question before the question deadline.
4. Strategize: win themes are strength, then benefit to this buyer, then proof. Research the buyer's mission, pain and hot buttons with web search; ghost competitor weaknesses without naming them.
5. Draft: the outline mirrors the instructions' required structure; each section answers its evaluation criterion, leads with the benefit and embeds the win theme.
6. Review in two passes: compliance (every matrix row addressed, page and format limits honored), then scoring simulation (read as a tired evaluator with the criteria open). Then memorize themes and reusable content.
7. Produce the submission files per the `document-export` skill: `doc-export docx` and `doc-export pdf` from the draft with the RFP's font, size, spacing, margins and paper, `--max-pages` set to the volume's limit, file names as instructed. Fix every page-limit or font problem in the report before handing over; final submission stays with the user.

### Craft rules

- Compliance matrix anatomy: requirement ID, RFP reference, requirement text, proposal section, status (compliant, partial, exception), owner. Every row closed before submission; an exception is declared, never hidden.
- Lead every section with the answer, mirror the RFP's own terminology, use the criterion's language in headings, and make scoring easy.
- Win themes need proof: a metric, past performance or a named capability. Three strong themes repeated beat ten asserted once.
- Past performance formula: what we did, for whom, how it is relevant here, measured result. Unverifiable claims get cut.
- Customer-centric ratio: the buyer's name and mission should appear more often than yours. A proposal about yourself loses.
- Answer only what is asked at the page count given. Over-length gets rejected unread in strict shops; unrequested extras dilute scoring.
- The question period is a weapon: ambiguities, conflicts between instructions and criteria, and scope gaps become submitted questions. Silence converts assumptions into risk.

### Outside US federal work

As of 2026-11; look up the current rule before relying on it.

- UK public sector: the Procurement Act 2023 governs procurements started on or after 2025-02-24. Suppliers enter their core supplier information once on the central digital platform, an upgrade of Find a Tender, and reuse it across bids.
- EU public sector: Directive 2014/24/EU awards on the most economically advantageous tender (Art. 67) and requires the documents to state each criterion's weighting, so write to the weights. The European Single Procurement Document (ESPD) is a self-declaration that no exclusion ground applies and the selection criteria are met; the authority may ask for the supporting documents at any time, so keep them current. Serious misrepresentation in it is itself a ground for exclusion.
- US federal registration: an active SAM.gov registration with a Unique Entity ID (UEI, which replaced the DUNS number on 2022-04-04) is required to receive awards. The registration expires every year; a lapsed one makes the entity ineligible for new awards.
- Defense work: the CMMC level a solicitation requires comes from its DFARS clause. As of 2026-11 the Department of War announced on 2026-07-13 the immediate suspension of CMMC Phase II requirements (due 2026-11-10; war.gov release "Department of War Suspends CMMC Phase II Requirements"); Phase I self-assessments stay in place, and in the interim it enforces NIST SP 800-171 Rev 2 through self-assessments and select government-led assessments. Verify the current phase on the DoD CIO CMMC page (dodcio.defense.gov/CMMC/) and in the solicitation before stating any CMMC status.
- Cloud services sold to federal agencies need FedRAMP authorization. The programme's rules changed in 2026 (Consolidated Rules for 2026, launched 2026-06-25 and mandatory for all stakeholders from 2027-01-01, with new certification classes); check fedramp.gov for the path and the product's listed status. Claim only the status the marketplace lists.
- Commercial RFPs have no Section L or M: shred the questions and any stated scoring weights into the same compliance matrix, and treat the weights as the evaluation criteria.
- Security questionnaires (SIG, CAIQ, HECVAT or a buyer's own): answer from one maintained answer library; cite the evidence for each answer (report, policy, date); never answer yes to a control that is not in place; route unknown answers to the security owner; keep answers consistent across questionnaires.

### Guards

- Don't fabricate past performance, certifications or capabilities.
- Don't hide a non-compliance as creative wording.
- Don't blow page or format limits.
- Don't skip the bid/no-bid because the team is excited.
- Do close every compliance-matrix row, tie every theme to proof, write for the evaluator's scoring sheet, and recommend no-bid when the numbers say so.

## Examples

- RFP shared: bid/no-bid first, always; ask for capability facts you can't verify.
- "Just write the response": still shred first. Drafting without a matrix is how mandatory requirements get missed.
- "Improve our draft": compliance pass, then scoring simulation, findings ranked by score impact.
- Recurring bids: build the content library of boilerplate answers, past-performance blocks and current bios.
- No RFP yet ("we heard about an opportunity"): capture prep covering buyer research, discriminators and teaming gaps.

## Output format

Working files as Markdown in the working directory, submission files as instructed (DOCX and/or PDF):

- Bid decision: `bid-decision-[opportunity].md` with scored factors, PWin and recommendation.
- Compliance matrix: `compliance-matrix-[opportunity].md` with the full shred table.
- Strategy: `win-themes-[opportunity].md` with themes and proof points, ghosting angles and questions to submit.
- Draft: `proposal-[opportunity].md` with the outline per instructions, drafted sections and executive summary; exported to the required DOCX/PDF with the page count and font check result.
- Review: `review-[opportunity].md` with compliance findings and simulated evaluator scoring with fixes.

## Checklist

- [ ] Bid/no-bid scored before any drafting?
- [ ] Every shall, must and submission instruction is a matrix row, each closed or declared as an exception?
- [ ] Every win theme has proof?
- [ ] Page, font and file-name rules verified in the export report?
- [ ] No claim of a certification, registration or past performance the organization lacks?
- [ ] Conflicts and ambiguities submitted as questions before the deadline?

## Composition / References

- `document-export` skill: DOCX and PDF output with page and font checks.
- `sales-qualification` skill: capture-stage qualification of the opportunity.
