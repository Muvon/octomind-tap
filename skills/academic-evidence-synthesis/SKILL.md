---
name: academic-evidence-synthesis
title: "Systematic Review: Review Types, Searches, PRISMA"
description: "Pick a review type, frame the question (PICO, PEO), write per-database searches, log screening, report PRISMA 2020 counts, pick a bias tool and checklist."
license: Apache-2.0
compatibility: "Any Octomind session with web search. Database access varies by user; state which databases were actually searched."
domains: academic
rules:
  - session(literature)
  - content(prisma)
  - content(systematic) content(review)
  - content(scoping) content(review)
  - content(rapid) content(review)
  - content(pico)
  - content(risk) content(bias)
  - content(consort) content(strobe)
  - match((?i)\b(search\s+strategy|search\s+string|boolean\s+search|mesh\s+terms?)\b)
  - content(pubmed)
  - semantic(help me plan a systematic review and report the screening counts)
---

## Overview

A literature review is only as defensible as its method. This skill gives the method steps that review readers and journal editors check: which review type the question needs, how to frame the question, how to search each database, how to log screening, which counts the PRISMA 2020 flow diagram needs, and which risk-of-bias tool or reporting checklist fits the study design. Use it for literature searches, thesis literature chapters, systematic and scoping reviews, and the reporting-checklist check before submitting an empirical paper.

## Mental model

- The review type is chosen from the question and the resources, not from the topic. A review that calls itself systematic must have a written protocol, a reproducible search in at least two databases, screening against stated criteria, and a bias assessment. Anything less is a narrative or rapid review and says so.
- Every number in the report comes from the screening log. Counts are recorded as they happen; they are never reconstructed afterwards.
- A search that used one free web surface is a literature search, not a systematic search. State the surfaces and dates.
- An AI assistant can draft strings, deduplicate, and tabulate. It cannot replace a second human screener, database access, or the author's judgement about inclusion.

## Rules

### Review type decision table

| Question the user has | Review type | Protocol and registration | Screening | Bias assessment |
|---|---|---|---|---|
| "What do we know about X?" for background or a thesis chapter | Narrative review | None needed; state the search used | One screener | Optional; note limits of the sources |
| "What has been studied, with what methods, and where are the gaps?" | Scoping review (PRISMA-ScR; JBI method) | Register on OSF Registries; PROSPERO does not currently accept scoping reviews (check its eligibility page) | Two screeners preferred | Not required; say it was not done |
| "Does intervention A work better than B?" or another focused answerable question | Systematic review, with meta-analysis only if studies are similar enough | Register on PROSPERO (health outcomes) or OSF before screening; PROSPERO does not register reviews already past data extraction | Two independent screeners, conflicts resolved by a third | Required, by design (table below) |
| Decision needed in weeks | Rapid review | Protocol and a stated list of shortcuts | Cochrane Rapid Reviews Methods Group interim guidance (2020, since updated; look up the current Cochrane recommendations before relying on these figures): dual-screen at least 20% of abstracts, resolve conflicts; a single reviewer may rate risk of bias if a second reviewer verifies every judgement | Required |
| "Summarize all reviews on X" | Umbrella review | Protocol | Two screeners | Appraise the reviews with AMSTAR 2 or ROBIS |

### Question frames

| Frame | Elements | Use for |
|---|---|---|
| PICO | Population, Intervention, Comparison, Outcome | Effect of an intervention |
| PEO | Population, Exposure, Outcome | Risk factors and exposures where no intervention is assigned |
| PCC | Population, Concept, Context | Scoping reviews |
| SPIDER | Sample, Phenomenon of Interest, Design, Evaluation, Research type | Qualitative and mixed-methods evidence. Cooke, Smith and Booth (2012) built it for qualitative synthesis; a later test found it more specific but likely to miss relevant papers, so run a broader check search beside it |

Write the frame first, then one concept block per element, then synonyms and controlled vocabulary per block. Do not put the Outcome block in the search for a systematic review unless the outcome is reliably indexed; outcome terms in titles and abstracts miss studies that measure the outcome but do not name it.

### Per-database search syntax

Syntax below was read on each vendor or API page. Re-check the database's help page for the interface the user has, because interfaces change.

| Source | Field and operators | Notes |
|---|---|---|
| PubMed | Operators `AND`, `OR`, `NOT` in uppercase. `[tiab]` title and abstract, `[mh]` MeSH heading. `*` truncation needs at least four characters before it. Phrase in quotes. Proximity: `"term1 term2"[tiab:~3]` | A field tag or quoted phrase switches off automatic term mapping, so combine a `[mh]` set with a `[tiab]` set joined by `OR` |
| Scopus | `TITLE-ABS-KEY(...)`. `AND`, `OR`, `AND NOT` (place last). Proximity `W/n` and `PRE/n`. `*` and `?` wildcards, one per term | Double quotes find a loose phrase; braces `{...}` find an exact phrase |
| Web of Science | Use the Advanced Search field tags and the proximity operator in the Clarivate help | Copy the tag list from the current Clarivate help page; do not write tags from memory |
| OpenAlex (API) | `search.title_and_abstract=` with uppercase `AND`, `OR`, `NOT` and quoted phrases. Stemming is on by default; wildcards `*` and `?` only work with `search.exact`, need at least 3 characters before the wildcard, and cannot lead a term | A minus sign does not exclude terms. Old filter `title_and_abstract.search` is deprecated |
| arXiv (API) | `search_query=` with prefixes `ti:`, `abs:`, `au:`, `cat:`, `all:`; operators `AND`, `OR`, `ANDNOT` | Preprints: record the version and whether a published version exists |
| Semantic Scholar | Use for citation chasing and related-paper discovery | Read the API documentation for query operators before stating a string |
| Google Scholar | Discovery and citation chasing only | No reproducible export, no field tags, results are ranked; a systematic review cannot rest on it alone |

Report each search as: database, interface, date run, exact string, filters, number of records. Run the same concept blocks in every database; do not claim a database was searched unless the string ran and returned a count. Search-reporting rules are in PRISMA-S (Rethlefsen et al., 2021).

### Screening log

One row per record, kept as a file the user can audit:

`id | source database | title | year | duplicate of | title-abstract decision | reason | full text obtained | full-text decision | exclusion reason code`

- Fix exclusion reason codes before screening (wrong population, wrong intervention or exposure, wrong comparator, wrong outcome, wrong design, not peer-reviewed or not a primary report, not in scope language, duplicate report). Use one reason per excluded report.
- Pilot the criteria on a sample of about 50 records, adjust once, then freeze them.
- A second screener's decisions go in their own columns; record agreement. If no second human screened, write that in the limitations.

### PRISMA 2020 flow counts

Source: Page et al., BMJ 2021;372:n71. Count at each stage and check that the arithmetic closes.

| Stage | Count to record |
|---|---|
| Identification | Records from each database and register, each listed; records from other methods (citation chasing, websites) separately |
| Removed before screening | Duplicates; records marked ineligible by automation tools; records removed for other reasons |
| Screening | Records screened; records excluded; reports sought for retrieval; reports not retrieved |
| Eligibility | Reports assessed; reports excluded, each with reason and count |
| Included | Studies included; reports of included studies (one study can have several reports) |

Checks: identified minus removed equals screened; screened minus excluded equals sought; sought minus not retrieved equals assessed; assessed minus excluded equals included reports. If automation tools excluded records, say how many a human excluded and how many a tool did. The 2020 statement has separate flow templates for new reviews, updates, and searches that include other methods. PRISMA extensions proposed for AI-assisted reviews are not endorsed standards; do not cite them as the standard.

### Risk-of-bias tool by study design

| Study design | Tool | Note |
|---|---|---|
| Randomized trial | Cochrane RoB 2 | Judge per outcome and result |
| Non-randomized study of an intervention | ROBINS-I | Version 2 was released in 2025; check the ROBINS-I site for the current version |
| Cohort and case-control | Newcastle-Ottawa Scale, or the JBI checklist for the design | State which and why |
| Cross-sectional, case series, qualitative | JBI checklist for the design, or CASP for qualitative | |
| Diagnostic accuracy | QUADAS-2 | |
| Systematic review used as evidence | AMSTAR 2 (16 items) or ROBIS | The 2025 comparison of 200 reviews found the two tools give complementary, not interchangeable, results |
| Scoping review | None required | Say the appraisal was not done |

Report bias judgements per study in a table and say how they affected the synthesis. Never state an effect size from a title or abstract you did not open.

### Reporting guideline by design (for papers the author is writing)

| Design | Guideline | Note |
|---|---|---|
| Randomized trial | CONSORT 2025 (BMJ, 14 April 2025; 30-item checklist plus flow diagram; replaces CONSORT 2010) | Add the trial registration number |
| Observational (cohort, case-control, cross-sectional) | STROBE | Choose the design-specific checklist |
| Systematic review or meta-analysis | PRISMA 2020 | Add PRISMA-S for the search |
| Scoping review | PRISMA-ScR | |
| Qualitative interviews or focus groups | COREQ | |
| Qualitative, general | SRQR | |

Find the current checklist on the EQUATOR Network site before the author fills it in. The editor will ask for it, so supply it with the submission.

### AI-use disclosure line

When an AI assistant helped with strings, deduplication or tabulation, add one line to the methods: tool and version, the tasks it did, and that every inclusion decision and every extracted value was checked by a named human. Follow the venue's own AI policy where it differs.

## Examples

Weak: "I searched Google for studies on school phones and found 20 papers; this systematic review shows phones lower grades."

Better: "Scoping review (PRISMA-ScR). Frame: PCC. Databases: PubMed and Scopus, run 2026-11-10, strings in Appendix A. 412 records identified, 96 duplicates removed, 316 screened, 41 reports assessed, 12 included. Bias not assessed (scoping). Protocol registered on OSF."

## Checklist

- [ ] The review type is stated and matches the question and the resources.
- [ ] A question frame is written and each concept has synonyms and controlled vocabulary.
- [ ] Each database has its exact string, run date and record count.
- [ ] Exclusion reason codes were fixed before screening; the log has one row per record.
- [ ] The flow counts close at every stage.
- [ ] A bias tool or checklist matches each study design, or its absence is stated.
- [ ] The second-screener situation and any AI use are disclosed.
- [ ] No review is called systematic unless it has a protocol, two databases, and a bias assessment.

## Composition / References

- [PRISMA 2020 statement (Page et al., BMJ 2021;372:n71)](https://www.bmj.com/content/372/bmj.n71)
- [PRISMA flow diagram templates](https://www.prisma-statement.org/prisma-2020-flow-diagram)
- [CONSORT 2025 statement (BMJ, 2025)](https://doi.org/10.1136/bmj-2024-081123)
- [Cooke, Smith and Booth, Beyond PICO: the SPIDER tool (2012)](https://pubmed.ncbi.nlm.nih.gov/22829486/)
- [Cochrane Rapid Reviews Methods Group interim guidance (2020; check for the updated recommendations)](https://methods.cochrane.org/rapidreviews/sites/methods.cochrane.org.rapidreviews/files/public/uploads/cochrane_rr_-_guidance-23mar2020-v1.pdf)
- [PubMed User Guide](https://pubmed.ncbi.nlm.nih.gov/help/)
- [Scopus search tips](https://schema.elsevier.com/dtds/document/bkapi/search/SCOPUSSearchTips.htm)
- [OpenAlex search documentation](https://help.openalex.org/how-to-use-the-api/get-lists-of-entities/search-entities)
- [arXiv API user manual](https://info.arxiv.org/help/api/user-manual.html)
- [EQUATOR Network reporting guidelines](https://www.equator-network.org/)
- For thesis question fit and defense preparation, see the thesis specialist; for the venue's own AI-use policy, check the venue site.
