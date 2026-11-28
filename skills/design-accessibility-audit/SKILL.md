---
name: design-accessibility-audit
title: "Accessibility Audit: WCAG 2.2, EAA, ADA Reports"
description: "Audit sites, apps, and PDFs against WCAG 2.2 AA, EAA, and ADA; rate barriers by user impact; write audit reports, statements, and remediation roadmaps."
license: Apache-2.0
compatibility: "A browser to inspect rendered pages and web access to verify current law; a human screen-reader pass is needed for any public conformance claim."
capabilities: browser webfetch
domains: designer
rules:
  - match((?i)\b(accessibility|a11y|WCAG(\s*2\.\d)?(\s*(A|AA|A/AA))?)\s+(audit|report|statement|roadmap|conformance|compliance|remediation)\b|\baudit\b.{0,40}\bWCAG\b)
  - match((?i)\b(remediation|fix\s+guidance|roadmap)\b.{0,60}\b(accessibility|WCAG|a11y|audit|barriers?|contrast|focus|ARIA|findings)\b|\b(accessibility|a11y|audit)\b.{0,40}\b(roadmap|remediation|findings)\b)
  - match((?i)\b(screen[\s-]?reader|NVDA|JAWS|VoiceOver|keyboard[\s-]only|focus\s+(management|indicators?)|ARIA)\b)
  - match((?i)\b(EAA|European\s+Accessibility\s+Act|ADA\s+(title|compliance|website)|Section\s+508|EN\s*301\s*549|VPAT)\b|\baccessibility\b.{0,40}\b(questionnaire|procurement)\b|\bprocurement\b.{0,60}\baccessibility\b)
  - semantic(is our website accessible and compliant with the European Accessibility Act, 0.72)
  - semantic(check this page against WCAG and rank the barriers, 0.72)
  - semantic(write an accessibility statement and remediation roadmap, 0.72)
  - semantic(test whether our app works with a screen reader and keyboard, 0.72)
  - semantic(is this PDF accessible to people with disabilities, 0.72)
---

## Overview

This skill audits digital products against WCAG 2.2 AA (and the WCAG 2.1 AA baseline that most laws still cite), the European Accessibility Act (EAA), and US ADA Title II and Section 508. It rates barriers by user impact and produces what buyers and regulators ask for: audit reports, accessibility statements, VPAT or ACR-style conformance summaries, and remediation roadmaps. It speaks in user impact first and success criteria second: "a keyboard user cannot check out" lands harder than "2.1.1 failure".

It covers full WCAG 2.2 A and AA audits with severity ratings; EAA applicability triage; ADA Title II and III, Section 508, UK Equality Act, and AODA applicability; audits of PDFs and mobile apps; EN 301 549 mapping; procurement questionnaire answers; and design and code-level fix guidance (ARIA, focus management, contrast, semantics). It produces audit evidence; accredited auditors certify. It does not give legal rulings on exposure or enforcement.

## Mental model

Automated scanning finds only part of the problem (estimates run from about a third to just over half of issues, depending on how they are counted), so the method is always automated checks plus manual keyboard, structure, and screen-reader reasoning. Alt text existing is automatable; alt text being useful is not. Every audit states which findings are automated, which are manual, and which need assistive-technology testing with real users.

Severity follows user impact, not criterion number: anything blocking task completion for a user group (checkout, login, form submit) is a blocker regardless of how small the code fix is.

## Rules

Method:

1. Ingest: target URLs or code, markets served, and deadline pressure. A procurement ask versus a regulator letter changes tone, not findings. Recall earlier audits of the product.
2. Triage applicability: EAA (enforced since 28 June 2025: e-commerce, banking, transport, telecom, e-books, consumer devices and their services; which member states; whether the micro-enterprise exemption applies), ADA Title II for US state and local government, ADA Title III for US private businesses, Section 508 for US federal procurement, the UK Equality Act, AODA for Ontario.
3. Audit: inspect rendered pages in the browser. Check the six dominant failure classes first, then keyboard-only flow (tab order, focus visibility, traps), semantic structure (headings, landmarks, labels), dynamic content (ARIA states, live regions), and media alternatives. Flag what needs a human screen-reader pass.
4. Rate: per finding, the WCAG criterion (and WCAG version), user impact, severity (blocker, serious, moderate, minor), affected user groups, and fix guidance.
5. Deliver the report, statement draft, and roadmap, then record findings and conformance status.

The six failure classes: 96% of detected web accessibility errors fall into six classes (WebAIM Million 2026, shares of top homepages): low-contrast text 83.9%, missing alt text 53.1%, missing form labels 51%, empty links 46.3%, empty buttons 30.6%, missing document language 13.5%. They are cheap to find and fix, and 95.9% of homepages fail at least one.

Legal baselines, as of 2026-11 (verify before quoting):

- EAA: presumption of conformity comes from the harmonised EN 301 549 v3.2.1 (WCAG 2.1 AA). EN 301 549 v4.1.1 (WCAG 2.2 AA, plus real-time communication changes) was published on 2 September 2026 but is not yet cited in the Official Journal; citation is expected on 16 December 2026 (Ireland's National Disability Authority). Until it is cited, v3.2.1 stays the baseline; audit to 2.2 AA now. The micro-enterprise exemption (under 10 staff and at most 2M euro turnover or balance sheet) covers services only, not products.
- ADA Title II (US state and local government): WCAG 2.1 AA. A DOJ interim final rule (April 2026) moved compliance dates to 26 April 2027 for entities serving 50,000 or more people and 26 April 2028 for smaller ones and special districts.
- ADA Title III (US private businesses open to the public): DOJ's position is that the ADA covers goods and services offered on the web, but it has no web regulation and requires no technical standard. It names WCAG and the Section 508 standards as helpful guidance and says a clean automated report does not guarantee accessibility. Treat WCAG 2.1 AA (2.2 AA going forward) as the working benchmark and send litigation exposure to counsel.
- UK Equality Act 2010: service providers owe disabled people reasonable adjustments. The Act names neither websites nor WCAG, so WCAG 2.2 AA is the benchmark used in practice. Public sector bodies have separate accessibility regulations.
- AODA (Ontario): public websites of designated public sector organisations and of businesses or non-profits with 50 or more employees must meet WCAG 2.0 AA, except 1.2.4 live captions and 1.2.5 audio description, since 1 January 2021; intranets are exempt.
- Section 508: WCAG 2.0 AA via the revised 508 standards; meeting 2.2 AA covers it.
- PDFs and mobile apps: audit them to the same WCAG criteria. EN 301 549 puts web content in clause 9, non-web documents such as PDFs in clause 10, and software including mobile apps in clause 11. For a PDF check tags and reading order, headings, alt text, language, document title, and form-field labels. For an app check screen-reader labels, focus order, target size, and text scaling on a real device.

WCAG 2.2 adds at AA: 2.4.11 Focus Not Obscured (Minimum), 2.5.7 Dragging Movements, 2.5.8 Target Size (Minimum, 24 by 24 CSS px), 3.2.6 Consistent Help, 3.3.7 Redundant Entry, 3.3.8 Accessible Authentication (Minimum). 4.1.1 Parsing is removed. Focus Appearance (2.4.13) is AAA. Note the WCAG version per finding.

WCAG 3 is a Working Draft and years from a standard. APCA contrast is not a conformance measure; base contrast findings on the WCAG 2.x ratios (4.5:1 text, 3:1 large text and UI components).

More ARIA usually means more broken: pages with ARIA average significantly more errors. Prefer native HTML semantics, and recommend removing ARIA before adding it.

An accessibility statement states conformance status honestly (full, partial, or not conformant), lists known exceptions, gives a feedback channel, and names the enforcement contact. An aspirational statement contradicted by the product is a legal liability, not a shield.

Don't declare conformance from automated scans alone, don't let a statement overclaim, and don't rank severity by count of issues instead of user impact. Recommend a human assistive-technology pass before any public conformance claim.

## Examples

- "Are we EAA compliant?": triage applicability first, then audit. Never answer yes or no without evidence.
- "Fix our accessibility": audit before fixes; deliver a prioritized roadmap with code guidance per finding.
- A procurement questionnaire arrives: answer from the latest audit and flag claims the product can't back.
- A single component or design review: run a targeted criteria check, not a full audit.
- An overlay widget is proposed: explain that overlays don't confer conformance and often add barriers (the FTC's 2025 order made accessiBe pay 1M dollars for claiming its AI tool made sites WCAG-compliant), and recommend fixing the source.
- A non-interactive brief: state the assumed markets and scope in the report and proceed.

## Output format

Save as `a11y-audit-[product].md`:

```markdown
# Accessibility Audit: [Product]

## Summary
[Conformance verdict, blocker count, EAA exposure, top 3 risks in plain language]

## Applicability
[EAA coverage, markets, exemptions, deadline context]

## Findings
| # | Severity | WCAG | Location | User impact | Fix guidance | Method |
[Method per finding: auto / manual / needs-AT-testing]

## Remediation Roadmap
[Phased: blockers, serious, rest; owner and effort per phase]

## Statement Draft
[Honest conformance status, exceptions, feedback channel]
```

## Checklist

- [ ] Applicability triaged and legal baselines verified on this run
- [ ] The six dominant failure classes checked first
- [ ] Every finding has a WCAG criterion and version, a user impact, a severity, and a method
- [ ] Automated, manual, and needs-assistive-technology findings are separated
- [ ] The statement draft claims no more than the evidence supports
- [ ] A human assistive-technology pass is recommended before any public claim

## Composition / References

- The `design-ux-review` skill covers quick heuristic reviews and microcopy.
- Sources: WCAG 2.2, EN 301 549, WebAIM Million 2026, DOJ ADA web guidance.
