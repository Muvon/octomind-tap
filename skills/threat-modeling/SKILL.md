---
name: threat-modeling
title: "Threat Modeling: STRIDE and Data Flow Diagrams"
description: "Threat modeling steps: data flow diagram, trust boundaries, STRIDE per element, rated threat table, mitigations. Use when designing or reviewing."
license: Apache-2.0
compatibility: "Stack-agnostic. Text diagrams (Mermaid) are enough; no modeling tool required."
domains: security-analyst
rules:
  - match((?i)\bthreat[\s-]?model(l)?(ing|s|ed)?\b)
  - match(\bSTRIDE\b)
  - match((?i)\b(attack\s+trees?|trust\s+boundar(y|ies)|data[\s-]?flow\s+diagrams?|abuse\s+cases?)\b)
  - match((?i)\bwhat\s+(could|can)\s+go\s+wrong\b.{0,40}\b(design|architecture|feature|system|integration)\b)
  - match((?i)\bsecurity\s+(review|assessment)\b.{0,30}\b(design|architecture)\b)
---

## Overview

Threat modeling finds design flaws before code exists, when a fix costs a diagram edit instead of a rewrite. This skill gives a repeatable procedure that ends in a written threat table: each threat has an element it hits, a rating, a response and an owner. Use it for a new feature, a new integration, or a review of an existing design. Code-level bugs belong to a code review, not to this procedure.

## Mental model

The OWASP Threat Modeling Cheat Sheet organizes the work as four questions ([OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html)):

1. What are we working on? Draw the system.
2. What can go wrong? List threats against each part.
3. What are we going to do about it? Pick a response for each threat.
4. Did we do a good enough job? Check the model and the mitigations.

A threat belongs to a design element, not to a vague "the system". Walking each element against a fixed list of threat types is how gaps get found.

## Rules

### Step 1: model the system

- Draw a data flow diagram with four element types: external entity (user, third-party service), process (code that runs), data store (database, queue, file, cache), data flow (any movement between them).
- Draw trust boundaries where the level of trust changes: internet to server, server to database, tenant to tenant, your code to a third-party API, the user's browser to your backend, an LLM to the tools it can call.
- Name the data on every flow and mark the sensitive ones (credentials, personal data, payment data).
- Cloud systems: add IAM roles, managed services, tenant separation and data residency as elements or boundaries.
- Stop when every flow that crosses a boundary is on the page. A larger diagram is not a better one.

### Step 2: find threats with STRIDE per element

STRIDE names six threats, each breaking one property ([Microsoft threat categories](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats)). Not every threat applies to every element type. This mapping comes from the STRIDE-per-element method in [Microsoft's threat modeling write-up](https://learn.microsoft.com/en-us/archive/blogs/larryosterman/threat-modeling-again-what-does-stride-have-to-do-with-threat-modeling):

| Element | S Spoofing (authentication) | T Tampering (integrity) | R Repudiation (accountability) | I Information disclosure (confidentiality) | D Denial of service (availability) | E Elevation of privilege (authorization) |
|---|---|---|---|---|---|---|
| External entity | yes | | yes | | | |
| Process | yes | yes | yes | yes | yes | yes |
| Data store | | yes | yes (logs) | yes | yes | |
| Data flow | | yes | | yes | yes | |

Walk every element and every boundary crossing against its applicable letters. Write one row per concrete threat, not one per letter.

Per-letter prompts:

| Letter | Ask |
|---|---|
| S | Can a caller pretend to be someone else? How does this process know who is calling? |
| T | Who can change this data at rest or in transit, and would anyone notice? |
| R | Could a user deny an action, and could we prove it from the logs? Can the logs themselves be altered? |
| I | Who can read this data at rest, in transit, in logs, in error messages, in backups? |
| D | What exhausts this element (requests, storage, CPU, third-party quota)? What happens when it is down? |
| E | Can a low-privilege caller reach a high-privilege action? Is authorization checked on the server for each request? |

Other methods are better in some cases: attack trees for one high-value goal, abuse cases for business-logic flaws, LINDDUN for privacy. The cheat sheet advises stating why a method fits and what it misses, and not stacking methods for show.

### Step 3: rate and respond

The cheat sheet notes that likelihood times impact is the usual ranking and is hard to estimate. Use a coarse scale so the team spends time on responses, not on scores. This scale is a working convention of this skill, not a standard:

| Score | Likelihood | Impact |
|---|---|---|
| 1 | Needs insider access or a rare condition | Minor, recoverable inside a day |
| 2 | Needs a skilled attacker or one prior flaw | Limited data or service loss |
| 3 | Any internet user can try it | Sensitive data exposed, money lost, or full service loss |

Risk = likelihood x impact. 6 or 9: fix before release. 3 or 4: fix on a dated plan. 1 or 2: may accept, in writing.

Each threat gets one response ([OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html)): mitigate, eliminate (remove the feature or flow), transfer (insurance, a provider's control; this does not reduce the risk by itself), or accept (with a named owner and a reason).

Map each mitigation to a testable requirement, for example "all object reads check the caller's tenant ID on the server", not "improve access control". Where a mitigation maps to an OWASP Top 10 category or an ASVS requirement, cite the ID so it becomes a review item.

### Step 4: validate

- The diagram matches the real system (check against code, deployment config, or the team).
- Every boundary crossing has at least one threat row or an explicit "none found".
- Every row has a response; every mitigation has a test or a measurable check.
- Store the model with access limited to people who need it, and update it when a flow, a data type, or a boundary changes.

### Output format

A single document: the diagram, then this table.

| ID | Element or boundary | STRIDE | Threat (attacker does X to get Y) | L | I | Risk | Response | Mitigation requirement | Owner |
|---|---|---|---|---|---|---|---|---|---|

Add a short list of assumptions (what you took as given) and open questions.

## Examples

Bad: "Threat: hackers. Mitigation: add security." No element, no rating, no testable requirement.

Good: "T-07, flow browser to API (crosses the internet boundary), T: a user edits the `account_id` field in the request to read another account (L3 x I3 = 9). Mitigate: the API derives the account from the session and rejects mismatches; integration test uses two accounts. Owner: backend lead."

## Checklist

- [ ] Diagram has all four element types and every trust boundary
- [ ] Sensitive data marked on the flows that carry it
- [ ] Each element walked against only its applicable STRIDE letters
- [ ] Each threat names an element, an attacker action and a gain
- [ ] Each threat rated with likelihood, impact and risk on the stated scale
- [ ] Each threat has one response; accepted risks have an owner and reason
- [ ] Each mitigation is a testable requirement
- [ ] Assumptions and open questions listed; model stored with limited access

## Composition / References

- [OWASP Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html) (read 2026-11-15)
- [Microsoft: STRIDE threat categories](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats)
- [Microsoft (Osterman, 2007): STRIDE per element](https://learn.microsoft.com/en-us/archive/blogs/larryosterman/threat-modeling-again-what-does-stride-have-to-do-with-threat-modeling)
