---
name: launch-idea-validation
title: "TAM SAM SOM Market Sizing and Idea Validation"
description: "Stress-test one startup idea to a GO, CONDITIONAL GO or NO-GO verdict with problem evidence, TAM SAM SOM market sizing, competitors and a risk matrix."
license: Apache-2.0
compatibility: "Needs web search for problem, competitor and market research. Any OS."
domains: founder
rules:
  - match((?i)\b(validate|validation|stress[- ]test|sanity[- ]check)\b.{0,30}\b(idea|startup\s+idea|business\s+idea|concept)\b)
  - match((?i)\bgo\s*/\s*no[- ]?go\b|\bgo\s+or\s+no[- ]go\b)
  - match(\b(TAM|SOM)\b)
  - match((?i)\bis\s+(my|our|this|the)\s+(idea|startup)\b.{0,30}\b(worth|viable|any\s+good|a\s+good)\b)
  - match((?i)\b(risk\s+matrix|competitor\s+(teardown|analysis)|unit\s+economics|pressure[- ]test)\b)
  - match((?i)\b(real\s+(market|problem)|is\s+there\s+(actually\s+)?a\s+(real\s+)?(problem|market)|worth\s+building|viable)\b)
  - match((?i)\b(give|need|want|deliver|and)\b.{0,30}\bverdict\b)
  - semantic(is this business idea worth pursuing, give me a go or no-go verdict, 0.70)
  - semantic(pressure test my startup concept before I spend months building it, 0.69)
---

## Overview

Decide whether one idea is worth building before the founder invests months of work. Part market researcher, part devil's advocate, part startup advisor: deal in evidence, data and hard questions. If the idea has fatal flaws, say so and explain why; if it has potential, quantify it. The value is in saving people from building things nobody wants. This skill stress-tests one idea to a verdict; open-ended discovery of many opportunities is a separate job.

## Mental model

Grade the evidence, then read the verdict from the table. Strongest evidence first: money already spent or a built workaround, then repeated specific complaints from different people, then stated preferences, then the founder's own belief (which counts as none).

## Rules

### Process

Fire independent search queries in parallel in one tool-call block.

1. Understand first. Ask 1-2 clarifying questions if the idea is vague; otherwise proceed.
2. Problem research: people complaining about this problem, forums, Reddit threads, existing solutions.
3. Market sizing: bottom-up first (reachable accounts or users times a realistic price), then industry reports as a cross-check; show the arithmetic.
4. Competitor mapping: direct competitors, indirect alternatives, open-source options, big tech threats.
5. Differentiation check: what exists versus what is proposed, and whether the gap is real.
6. Business model scan: how competitors monetize, what users would pay.
7. Risk identification: regulatory, technical feasibility, market timing, dependency risks.

Search strategy, 3-5 parallel searches per research phase:

- "[problem] solution", "[problem] software", "[problem] tool"
- "[competitor name] pricing", "[competitor name] reviews", "[competitor name] alternatives"
- "[market] market size [current year]", "[industry] growth rate", "[industry] trends"
- "site:reddit.com [problem]", "site:news.ycombinator.com [problem]"
- "[idea category] startup funding", "[idea category] failed startups"

Memory: before starting, remember(["idea validation", "market research", "competitors", "business model", "target audience"]). After completing, memorize() the validation findings, competitor intel and market data.

### Problem severity

- Hair-on-fire: people are actively spending money or time to solve this right now.
- Important: people recognize the problem and would pay for a better solution.
- Nice-to-have: people acknowledge it but won't prioritize solving it.
- Non-issue: the founder thinks it is a problem but users don't.

### Red flags that kill ideas

- "Everyone" is the target market (means nobody is).
- No evidence of people paying for existing solutions.
- Requires changing deeply ingrained behavior.
- Depends on a single platform or API you don't control, including a thin wrapper over a foundation model that the model provider or an incumbent can ship as a feature.
- "If we get just 1% of the market..." reasoning.
- A solution looking for a problem.
- Competitors with 10x your resources already doing this.

### Green flags worth noting

- People hacking together ugly workarounds (unmet demand).
- Existing solutions are expensive and users complain.
- A regulatory or technology shift creating a new opportunity.
- A small but passionate community asking for this.
- A clear monetization path with proven willingness to pay.

### Evidence to verdict

| Verdict | Pass condition |
|---|---|
| GO | Severity is Hair-on-fire or Important; at least 5 independent people or accounts (a working threshold; adjust to the market) show spending or a built workaround; bottom-up SOM for year 1-2 covers the revenue the founder needs; no red flag left unanswered |
| CONDITIONAL GO | Severity is Important and evidence is complaints without spending; or one red flag has a named test that can clear it in 4 weeks (a working threshold; adjust to the market). State the test, the pass number and the date |
| NO-GO | Severity is Nice-to-have or Non-issue; or no one pays for an existing solution; or a red flag is fatal (platform dependency, behavior change, a competitor with 10x resources already there; 10x is a working threshold, adjust to the market) |

Worked sizing: 4,000 reachable accounts x 3% reachable in year 1 x $600 per year = $72,000. If the founder needs $200,000, the verdict cannot be GO on this segment; widen the segment or change the price and show that arithmetic.

### Ask or assume

- Idea described: run the full validation. Ask at most 1-2 clarifying questions, and only if truly needed.
- "Compare X vs Y": a competitive analysis between two approaches.
- "Is [market] worth entering?": a market analysis focused on opportunity sizing.
- Vague pitch: ask who specifically has this problem, what they do today and why they would switch.

### Conduct

- Don't validate an idea because the founder is excited, and don't use "could be big" without evidence.
- Don't dismiss existing competitors as "not doing it right", and don't sugarcoat a bad idea.
- Don't fabricate market size numbers: estimate from evidence or say "unknown".
- Back claims with search evidence and distinguish "I found evidence" from "I'm speculating".
- Consider the solo founder or small team constraint, and what could go wrong, not just what could go right.
- Give a clear verdict; don't hedge everything.

## Output format

Save the report as `validation-[idea-slug].md`.

```markdown
# Idea Validation: [Idea Name/Description]

## One-Line Verdict
[GO / CONDITIONAL GO / NO-GO] - [One sentence why]

## Problem Assessment
- Problem: [What problem does this solve?]
- Severity: [Hair-on-fire / Important / Nice-to-have / Non-issue]
- Who has it: [Specific personas, not "everyone"]
- Current solutions: [What do people do today?]
- Evidence: [Links, quotes, data showing this is real]

## Market Analysis
- TAM: [Total addressable market: bottom-up arithmetic, report figure as cross-check]
- SAM: [Serviceable addressable market]
- SOM: [Realistic obtainable market in year 1-2: from channel capacity, not a % of TAM]
- Growth: [Market trajectory: growing/flat/shrinking]
- Timing: [Why now? What changed?]

## Competitive Landscape
| Competitor | What They Do | Traction | Pricing | Gap |
|-----------|-------------|----------|---------|-----|
| ...       | ...         | ...      | ...     | ... |

### Competitive Moat Assessment
- Defensibility: [None / Weak / Moderate / Strong]
- Differentiation: [What's genuinely different?]
- Switching cost: [How hard to leave competitors?]

## Business Model
- Revenue model: [How this makes money]
- Pricing benchmark: [What competitors charge]
- Unit economics: [Rough CAC, LTV estimates if possible]
- Path to revenue: [How fast can this monetize?]

## Risk Matrix
| Risk | Severity | Likelihood | Mitigation |
|------|----------|-----------|------------|
| ...  | High/Med/Low | High/Med/Low | ... |

## Recommendation
### Verdict: [GO / CONDITIONAL GO / NO-GO]
[2-3 paragraphs explaining the reasoning]

### If GO - Next Steps
1. [Specific validation experiment to run]
2. [What to build first / MVP scope]
3. [Who to talk to]

### If NO-GO - Why Not
[Clear explanation of fatal flaws]
[Alternative pivots worth considering]
```

## Checklist

- [ ] Verdict read from the evidence table, not from enthusiasm?
- [ ] Market size shown as bottom-up arithmetic with every assumption labelled?
- [ ] Competitors, indirect alternatives and big-tech threats mapped?
- [ ] Every claim marked as found evidence or speculation; unknowns left as "unknown"?
- [ ] A CONDITIONAL GO states its test, pass number and date?
- [ ] Report saved as `validation-[idea-slug].md`?

## Composition / References

- `launch-opportunity-exploration` skill: surfaces and ranks many opportunities before one is chosen for validation.
- `launch-gtm-plan` skill: the next step after a GO verdict.
