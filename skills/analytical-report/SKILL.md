---
name: analytical-report
title: "Analytical Report Craft"
description: "Turn raw data into a decision-ready report a human actually reads: structured by the Minto Pyramid (answer first), every number traced to the data, the right chart for each question, and delivered as a self-contained HTML document that opens in any browser and prints to clean PDF with no dependencies. The output is format-flexible, grounded, and never fabricated."
license: Apache-2.0
compatibility: "Produces self-contained HTML by default; markdown or PDF when requested and a renderer is available."
domains: data
rules:
  - data(report)
  - data(analysis-report)
  - match(\b(generate|build|write|make)\s+(a|the|an)\s+(report|analytics report|data report)\b)
  - match(\breport\s+(from|on)\s+(this|the|my)\s+(data|csv|metrics|logs|numbers)\b)
  - match(\b(pdf|html)\s+report\b)
  - semantic(turn this data into a readable report)
  - semantic(generate a professional analytics report from these numbers)
  - semantic(make a PDF report a human can read)
---

## Overview

A report exists to help a human decide something. Most data reports fail two ways: they bury the answer under process (a chronological data dump), or they fabricate/round numbers the underlying data doesn't support. This skill encodes how to produce a report that leads with the answer, proves it with real numbers traced to the data, and is delivered in a form a person can actually read and print.

## Mental model

Two non-negotiables: the pyramid (answer first) for readability, and the grounding gate (every number computed from the data) for trust. Everything else — chart choice, layout, print CSS — serves one of those two.

## Instructions

### Structure — the Minto Pyramid (answer first)

Executives read top-down and have little time; match that. Structure every report as a pyramid:

1. Headline finding — the single most important takeaway, in one sentence, at the very top. If the reader stops here, they have the answer.
2. Executive summary — 3–5 key findings (the rule of 3–5), strongest first, each one sentence with its supporting number. This is the whole report in a glance.
3. Supporting sections — one per key finding, in the same order. Each leads with its finding (not a heading like "Data"), then shows the evidence: the chart, the table, the method in a line.
4. Recommendations / next steps — what to do about it, when the report's purpose is decision-support.
5. Appendix / method — data sources, date range, caveats, and how figures were computed, for the reader who wants to verify.

Never open with "This report analyzes…" or a methodology wall. Open with the finding.

### Grounding gate — every number traced to the data

- Compute every statistic from the actual data (load it, run the numbers — don't estimate). Report figures at the precision the data supports; don't invent decimals or round in a way that changes the story.
- No fabricated or illustrative numbers. If a figure can't be computed from the provided data, say so — never fill the gap with a plausible-looking number.
- State the data source, the date range/scope, and any filtering. Show the method in one line where a number could be questioned ("median of 1,204 sessions, bot traffic excluded").
- Flag uncertainty honestly: small samples, missing data, outliers that move the result. Give a range or interval next to any estimate that a decision hinges on. A caveat is cheaper than a wrong decision.
- Correlation is not causation — describe what the data shows, not a causal story it can't support.

### Charts — the right one, labelled, self-contained

Pick the chart by the question, not by variety:
- Trend over time -> line. Comparison across categories -> bar. Part-to-whole -> stacked bar (pie only for 2–4 slices, sparingly). Distribution -> histogram. Relationship -> scatter. A single number that matters -> a big bold stat, not a chart.
- Label directly (values on/next to marks) over forcing the eye to a legend and axis. Title each chart with its takeaway, not its variable names ("Signups fell 40% after the April change", not "Signups by month").
- One visual system: consistent colours, fonts, and sizing across every chart so the report reads as one document. Use colour to encode meaning, not decoration; keep it colour-blind-safe and readable in greyscale (it will be printed).
- Render charts as inline SVG embedded in the HTML — self-contained, styleable by the print CSS, no external image files or CDN dependencies. Plot with matplotlib and the bundled house style (`report.mplstyle`, listed under Skill Resources): `plt.style.use("<path>/report.mplstyle")`, grey the context series and color the one that carries the message, `ax.set_title(<takeaway>)`, `ax.bar_label()` or `ax.annotate()` for direct labels, then `fig.savefig(buf, format="svg")` and inline the SVG. Run it with `uv run --with matplotlib python chart.py` when matplotlib isn't installed. Hand-written SVG only for sparklines and single bars; drawn-by-hand axes and labels come out misaligned.
- Make every chart readable without sight: `role="img"` plus a `<title>` (and `<desc>` for the takeaway) inside the SVG, and the underlying numbers available as a table nearby or in the appendix. Keep marks at 3:1 contrast against the background and never rely on colour alone — add labels, patterns, or direct annotation.

### Delivery — self-contained HTML that prints to clean PDF

Default output is a single self-contained HTML file: all CSS inline in a `<style>` block, all charts inline SVG, web-safe or embedded fonts — no external requests. It opens in any browser (human-readable immediately) and prints to PDF via the browser (Print -> Save as PDF) with no tools installed.

Make it print cleanly:

```css
@media print {
  @page { size: A4; margin: 18mm; }
  .no-print { display: none; }
  h2, h3 { break-after: avoid; }
  table, figure, .card { break-inside: avoid; }
  a { color: inherit; text-decoration: none; }
}
body { font: 11pt/1.5 -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; color: #1a1a1a; }
td.num, .stat { font-variant-numeric: tabular-nums; text-align: right; }
```

Use absolute units (pt, mm) for print layout, `break-inside: avoid` on tables/figures/cards (the older `page-break-*` properties are legacy aliases), and a print-only footer (page context, source, date). Keep the on-screen version clean too — this is one document for both. Set `<html lang>` and a real `<title>`, and use semantic headings and `<table>` with `<th scope>` so the HTML and the PDF exported from it stay accessible.

Typography and layout for humans: generous line height, a readable measure (not full-width text), clear heading hierarchy, tables for enumerable facts with right-aligned numbers, a stat-tile row for the headline metrics, whitespace over density. Restraint reads as authoritative.

Format flexibility: HTML is the default and the most useful (browser + PDF in one). Produce Markdown if the request asks for it, or a rendered PDF if a renderer is available in the environment (the agent can render the HTML via a shell tool when one is present); otherwise deliver the HTML and tell the reader to open it and Print -> Save as PDF.

## Examples

Weak opening (process-first, no answer): "This report presents an analysis of user engagement data collected between January and June 2026 across all platform surfaces, using the following methodology…"

Strong opening (answer-first, pyramid): "Engagement is up 22% — but entirely from existing power users; new-user activation actually fell 15%, and that's the risk. The three findings below, then the detail."

Chart title, weak: "Sessions by Month". Chart title, strong: "Sessions doubled after launch, then plateaued in Q2 — the growth engine has stalled."

## Checklist

Before finalizing:

- [ ] The first sentence gives the answer.
- [ ] Every key finding is readable from the executive summary alone.
- [ ] Every number traces to the data, with its method, at the precision the data supports; nothing is illustrative or estimated.
- [ ] Every chart is the right type, directly labelled, titled with its takeaway, part of one visual system, and has a text alternative.
- [ ] Caveats name sample size, missing data, and anything correlational.
- [ ] The HTML renders standalone with no external requests and prints without broken tables or clipped charts.
