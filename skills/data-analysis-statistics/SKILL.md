---
name: data-analysis-statistics
title: "Statistical Significance and A/B Tests: Data Analysis"
description: "Turn messy data into a plain answer: exploratory analysis, honest statistics, A/B test reading and chart choice. Use for analysis and significance."
license: Apache-2.0
compatibility: "Needs Python with pandas, or uv to fetch packages; Polars or DuckDB for data larger than memory."
domains: analyst
capabilities: image-view
rules:
  - match((?i)\b(analy[sz]e|explore|profile|clean\s+up|clean)\s+(this|the|my|our)\s+(\w+\s+){0,2}(data|dataset|csv|survey|results|export)\b)
  - match((?i)\b(a/b\s+tests?|ab\s+tests?|split\s+tests?|statistically\s+(significant|meaningful)|p[\s-]?values?|confidence\s+intervals?|simpson'?s\s+paradox|effect\s+size|just\s+noise|real\s+(conversion\s+)?difference)\b)
  - match((?i)\b(test|experiment)\b.{0,60}\b(visitors?|arms?|variants?|clicks?|conversions?)\b.{0,100}\b(better|difference|noise|real|significan\w+)\b)
  - match((?i)\b(cause\s+and\s+effect|causal\w*|confound\w*)\b)
  - match((?i)\b(best|right)\s+(chart|graph|plot)\b|\b(choose|pick)\b.{0,30}\b(chart|graph|plot)\b)
  - match((?i)\bclean\w*\b.{0,100}\b(tell\s+me|answer|whether|why)\b)
  - match((?i)\b(investigate|explain|find)\b.{0,40}\b(drop|dropped|decline|fall|rise|increase)\w*\b.{0,100}\b(segment|cohort|csv|dump|dataset|data)\b)
  - match((?i)\b(skewed|outliers?|long[\s-]tail)\b|\b(relationship|difference)s?\s+between\b.{0,100}\b(strong\s+enough|meaningful|mislead\w*)\b)
  - semantic(explore this dataset and tell me what stands out, 0.72)
  - semantic(is the difference between these two groups statistically significant, 0.72)
  - semantic(read the results of our A/B test and tell me what to ship, 0.72)
  - semantic(which chart type should I use to show this comparison, 0.72)
---

## Overview

Use this skill to turn raw, messy data into a trustworthy, plainly stated answer to the actual business question. Do the statistics correctly, say when a number is causal versus merely correlated, and show it in the chart that fits the question. The deliverable is a decision, not a table.

## Mental model

Lead with the answer (bottom line up front), then the evidence and caveats. Use plain language for non-experts and define a term the first time you use it. Be honest about uncertainty and push back on cherry-picking: a conclusion the data doesn't support is worse than "we don't know yet".

## Rules

### Method

Follow a CRISP-DM-style loop. Use Python and the shell to inspect and compute: pandas for ordinary files, Polars or DuckDB when the data is larger than memory or easier to query in SQL.

1. Frame: restate the business question, the decision it feeds, and what each possible answer would change. Refuse a vague "just pull me a number" until the decision behind it is clear.
2. Inspect and clean: check coverage, missingness, duplicates and definition mismatches. Reshape toward tidy data (one variable per column, one observation per row).
3. EDA first: profile each key variable with distributions, the five-number summary, box plots, and outlier and missingness checks before computing any headline metric.
4. Analyze: choose descriptive versus inferential deliberately. Attach a confidence interval to any population claim (bootstrap when the metric is skewed or a ratio). For comparisons, interpret a properly powered test and report effect size. Check key segments for Simpson's paradox.
5. Communicate: answer and recommended action in plain language, the single right chart, the assumptions, and what would change the conclusion. Plot with matplotlib and the `report.mplstyle` file from the `analytical-report` skill (takeaway as the title, the message series in the accent color, context in grey, direct labels), saved as PNG and SVG. Use `uv run --with matplotlib` when it isn't installed. Open the saved PNG and look at it before using it.

### Frameworks

| Framework | Originator | Use it for |
|---|---|---|
| Exploratory Data Analysis | Tukey, 1977 | Five-number summary, box plots, resistant stats (median, IQR); let data suggest hypotheses before modeling |
| Descriptive vs inferential | Statistics canon | Say "in this sample" versus "we estimate for all users"; attach uncertainty to population claims |
| Correlation is not causation | Pearl; Bradford Hill | Default to association; name confounders and reverse causation; causal claims need randomization or a credible quasi-experiment (difference-in-differences, regression discontinuity) with its assumptions stated |
| Simpson's paradox | Simpson 1951; Blyth 1972 | Check the aggregate holds within key segments before stating a direction; weight correctly |
| Trustworthy A/B testing | Kohavi, Tang and Xu, 2020 | Power up front (alpha, power, baseline, MDE gives n); check sample ratio mismatch before reading any metric; no unplanned peeking, monitor only with a sequential (always-valid) design; CUPED-style variance reduction when pre-period data exists; report effect size and CI, not just p < 0.05 |
| Multiple comparisons | Benjamini and Hochberg, 1995 | Many metrics or segments: control the false discovery rate (or Holm), or label the cut exploratory |
| Chart by question | Cleveland-McGill; Abela | Comparison as bar, trend as line, distribution as histogram, relationship as scatter; favor position and length over pie and area |
| Tidy data | Wickham, 2014 | One variable per column, one observation per row; makes analysis and plotting reliable |

Statistical significance is not practical significance: a 0.1% lift can be "significant" and still not worth doing. Report the effect size.

### Common requests

| Request | Response |
|---|---|
| "Just pull me this number" | Clarify the decision behind it first, or you will deliver the wrong number confidently. |
| "Does X cause Y?" | Default to "this is correlation"; name plausible confounders; say what design would establish causation. |
| "Is it significant?" | Report the effect size and confidence interval, not just the p-value. |
| Ambiguous | Ask one clarifying question, then proceed. |

In an autonomous, non-interactive brief, don't ask. State the decision you assume the number feeds, proceed, and list the assumptions with the answer.

### Guards

- Don't claim "the data shows X causes Y" from observational correlation.
- Don't p-hack: no running many cuts until something hits p < 0.05, no optional stopping or peeking, no dropping inconvenient outliers.
- Don't report "statistically significant" while ignoring effect size and practical importance.
- Don't use pie charts for more than 2 or 3 slices, dual-axis charts to imply correlation, or truncated y-axes that exaggerate differences.
- Do EDA before headline metrics, state uncertainty on every population claim, and check segments before stating a direction.
- This is general analytical guidance, not medical, legal or financial advice. Conclusions are estimates from a sample and assume the underlying data is reasonably complete and unbiased: verify that, don't assume it.

### Scope limits

Writing and optimizing the SQL itself, spreadsheet formula help, building and validating predictive models, production ML pipelines and model deployment, and professional judgment in medical, legal or financial matters are separate jobs.

## Output format

Deliver an analysis, not a data dump:

- Answer: the bottom line and the recommended action, up front
- How: method, sample, key assumptions
- Evidence: the one chart that fits the question, plus the headline numbers with uncertainty
- Caveats: biases, what is correlation versus causation, and what data would make this more trustworthy

Save to `analysis-[topic-slug].md` (and any chart or script) in the working directory when asked.

## Checklist

- [ ] The decision behind the question is stated.
- [ ] EDA came before any headline metric.
- [ ] Every population claim carries an interval, and effect size is reported next to significance.
- [ ] Key segments were checked before a direction was stated.
- [ ] Causal language is absent unless a design supports it.
- [ ] The chart type fits the question, and the saved image was opened and checked.

## Composition / References

- `analytical-report` covers turning the result into a formatted report.
- `data-predictive-modeling` covers predictive and forecasting models.
