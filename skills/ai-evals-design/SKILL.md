---
name: ai-evals-design
title: "AI Evals Design: Golden Sets, Metrics, Significance, CI"
description: "Operational playbook for designing production LLM evaluation in 2026. Covers eval framework selection (Promptfoo, DeepEval, Inspect, LangSmith, Braintrust, Phoenix, Galileo), golden dataset construction (size, stratification, versioning, contamination), synthetic data generation, LLM-as-judge design and calibration (G-Eval, human agreement, position/length bias, preference leakage), statistical significance (standard errors, clustering, paired differences, power analysis), RAG metrics (RAGAS, TruLens RAG Triad), agent evaluation (outcome grading, pass@k vs pass^k, transcripts), drift detection, eval-driven development and CI regression gates, and benchmark literacy (saturation and contamination of MMLU, GPQA, SWE-bench Verified; SWE-bench Pro, HLE, tau2-bench, BFCL, GAIA). Use when designing an eval suite, validating a prompt or model change, gating a deploy, or diagnosing production quality drift. Output: eval verdicts with statistical evidence, not vibe judgments."
license: Apache-2.0
compatibility: "Stack-agnostic. Production eval stacks typically need: an LLM provider SDK, a framework (Promptfoo / DeepEval / Braintrust / LangSmith), and a tracing backend for production drift monitoring (Phoenix / Langfuse / Helicone / Galileo)."
domains: ai
rules:
  - session(ai)
  - content(eval)
  - content(evals)
  - content(evaluation)
  - content(golden)
  - match(\b(eval|evaluation)\s+(suite|harness|framework|design|driven)\b)
  - match(\b(golden\s+(set|dataset|examples))\b)
  - match(\b(LLM[\s-]?as[\s-]?judge|G-Eval)\b)
  - match(\b(RAGAS|TruLens|DeepEval|Promptfoo|Braintrust|Maxim|LangSmith)\b)
  - match(\b(prompt\s+(regression|drift)|model\s+drift)\b)
  - match(\b(statistical\s+significance|McNemar|paired\s+t-?test)\b)
  - match(\b(MMLU|GPQA|GAIA|SWE-?Bench|BFCL|HELM|τ-?Bench)\b)
  - match(\b(eval[\s-]?driven\s+development|EDD)\b)
  - semantic(design an evaluation suite for our LLM app)
  - semantic(did this prompt change actually improve anything)
  - semantic(how to know if our agent regressed in production)
  - semantic(set up a golden dataset for testing)
  - semantic(prevent prompt regression in CI)
---

## Overview

Every prompt, model, or effort change is a stochastic intervention into a behavior surface, and "looks better" is not a verdict. Eval-driven development (Red Hat, March 2026) makes the suite the merge gate. This skill encodes the methodology that turns LLM evaluation from anecdote into evidence.

Use this skill when designing a new eval suite, validating a prompt or model change, gating a deploy, debugging production quality drift, or building CI regression tests. Skip it when the change is purely structural (config, framework version) with no behavioral surface area.

## Mental model

A real eval has five parts:

1. Behavior spec — a precise, falsifiable description of what the system should do. "Be helpful" is not a spec. "Answer the user's question using only the retrieved context, with factual claims grounded in cited passages" is.
2. Golden dataset — stratified examples covering happy paths and edge cases. Version-controlled. Sized for the smallest effect you care about detecting.
3. Metric — one per behavior. Composite scores hide regressions; report components.
4. Judge — for non-binary metrics, an LLM-as-judge with explicit rubric. Picked from a different model family than the generator to mitigate preference leakage.
5. Statistical test — paired sample test with effect size and significance, not point estimates.

Everything else (framework choice, CI integration, drift monitoring) is plumbing around these five. Get the methodology right; the tools follow.

## Instructions

### 1. Framework landscape (2026)

| Framework | OSS / paid | Best for | Source |
|---|---|---|---|
| Promptfoo | OSS CLI + YAML (OpenAI-owned since Mar 2026) | Local dev loop, CI gates, red-team mode with OWASP / NIST presets | [promptfoo.dev](https://www.promptfoo.dev) |
| DeepEval (Confident AI) | OSS Python + paid cloud | G-Eval, hallucination, faithfulness, contextual metrics; synthetic data | [deepeval.com](https://deepeval.com/docs/getting-started) |
| Inspect (UK AI Security Institute) | OSS Python | Agentic and capability evals with sandboxes; used for frontier-model testing | [inspect.aisi.org.uk](https://inspect.aisi.org.uk/) |
| LangSmith | Paid (per-seat) | LangChain / LangGraph integration; trajectory evals | [docs](https://docs.langchain.com/langsmith/) |
| Braintrust | Paid | Dataset → scoring → monitoring → CI gating | [braintrust.dev](https://www.braintrust.dev) |
| Phoenix (Arize) | OSS | Tracing + embedding-drift clustering | [arize.com/phoenix](https://arize.com/phoenix/) |
| Galileo | Paid | Failure-mode mining; small-model evaluators | [galileo.ai](https://galileo.ai/) |

Common production pattern: tracing (Langfuse or Phoenix) for production samples + DeepEval, Promptfoo, or Inspect for the suites in CI.

### 2. Golden dataset construction

| Property | Guidance |
|---|---|
| Size | 50–500 examples typical for prompt-level evals; agent-level evals can need 200–1000 due to multi-step variance |
| Stratification | Cover intents, edge cases, hard negatives, multilingual variants, length extremes — not just happy paths |
| Source | Production traffic samples (with PII redaction) + handcrafted edge cases + synthetic adversarial examples |
| Version control | Stored alongside prompts in git; versioned; tagged with the prompt/model commit they were created against |
| Refresh cadence | Every quarter or when behavior shifts; add examples for newly observed failure modes |
| Labels | Ground truth where possible (gold answers); for open-ended outputs, judge-rubric criteria suffice |

Start small where effects are large: 20–50 tasks drawn from real failures is enough to see early agent changes (Anthropic, Jan 2026). Then size for the smallest effect you care about. For paired pass/fail at 80% power and α=0.05, detecting a 5-point gain needs roughly 300 items when ~10% of pairs disagree and ~600 at 20%; an unpaired comparison near 50% accuracy needs ~1,500 per arm. Don't report a "result" from n=20.

### 3. Synthetic data generation

- DeepEval Synthesizer — input → evolve → score on self-containment and clarity; multi-turn supported ([DeepEval Synthesizer docs](https://deepeval.com/docs/synthesizer-introduction)).
- OpenAI Evals registry — YAML grader patterns; broad community-contributed eval set.
- Adversarial example mining — for safety and robustness, pull relevant patterns from PyRIT and garak datasets.
- Contamination hygiene — keep the golden set private, embed canary strings, and refresh it from production failures; synthetic items generated by the model under test inherit its blind spots.

Synthetic data complements, never replaces, real production traffic. Use it to fill stratification gaps (rare intents, edge cases) — not to substitute for the messy reality of real users.

### 4. LLM-as-judge — G-Eval methodology

[G-Eval](https://arxiv.org/abs/2303.16634) — Liu et al., EMNLP 2023: the judge reasons about a narrow criterion, then fills a score form with anchored levels; 0.514 Spearman with human ratings on SummEval. DeepEval's `GEval` implements it. Use it when a deterministic metric doesn't fit; prefer binary pass/fail criteria when the behavior allows, and average multiple judge runs when variance is high.

### 5. Preference leakage and self-bias mitigation

[Preference leakage](https://arxiv.org/abs/2502.01534) — Li et al., ICLR 2026. Judges favor students trained on data from the same model, an inheriting model, or the same family; the paper's SFT setting averaged a 23.6% leakage score. Judges also carry position bias, length bias, and self-preference.

Mitigations:
- Use a judge from a different model family than the generator and its data generator.
- Calibrate against human labels before trusting the judge: report TPR/TNR or Cohen's kappa on a labelled sample sized like any other eval; the paper's most effective fix was contextual calibration on a held-out labelled set.
- Prefer binary pass/fail on narrow criteria over Likert scales; give the judge an "unknown" option; use one judge per dimension (Anthropic, Jan 2026).
- For pairwise comparisons, run both orderings and count only consistent verdicts.
- Strip formatting and style cues the judge might key on.

### 6. Statistical significance

Per Anthropic's statistical guidance (Miller, [arXiv:2411.00640](https://arxiv.org/abs/2411.00640), Nov 2024):

- Report the mean with its standard error and 95% CI; an eval score is a sample estimate.
- Cluster standard errors when items share a source (several questions per document); naive errors can be far too small.
- Compare variants as paired differences on the same items (McNemar's for paired pass/fail), reporting the mean difference, its CI, and the correlation.
- Reduce within-item variance by resampling stochastic outputs and averaging.
- Run a power analysis before the eval, not after.
- Correct for multiple comparisons (Holm, Benjamini–Hochberg) when testing many variants; bootstrap or Bayesian methods when n is small ([evalstats](https://github.com/ianarawjo/evalstats)).

Mandatory output for any "we improved X" claim: effect size + CI + sample size + test used.

### 7. Eval categories and metric selection

| Category | Metric examples | Framework fit |
|---|---|---|
| Quality / correctness | Exact match, ROUGE/BLEU (for translation), G-Eval correctness | DeepEval, RAGAS, custom |
| Faithfulness / hallucination | DeepEval HallucinationMetric, RAGAS faithfulness | DeepEval, RAGAS |
| RAG retrieval quality | RAGAS context precision, recall, entity recall; TruLens context relevance | RAGAS, TruLens |
| Safety / toxicity / bias | Promptfoo red-team, Patronus, HELM bias metrics | Promptfoo, Patronus |
| Robustness | Adversarial probes, paraphrase invariance | HELM, garak |
| Latency / cost | Trace-level cost and P50/P99 latency | Helicone, LangSmith, Langfuse |
| Agent trajectory | Trajectory match, tool-use accuracy, task completion | LangSmith trajectory evals, OSS `agentevals` |

### 8. RAG-specific evaluation

[RAGAS](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/) — Es et al., EACL 2024, [arXiv:2309.15217](https://arxiv.org/abs/2309.15217). Metrics:
- Faithfulness — generator's claims grounded in retrieved context
- Answer relevancy — answer addresses the question
- Context precision — retrieved chunks ranked correctly by relevance
- Context recall — required information was retrieved
- Context entity recall — named entities in the answer appear in the context

Production threshold: faithfulness > 0.8 and context precision > 0.8 are strong; domain-dependent.

[TruLens RAG Triad](https://www.trulens.org/getting_started/core_concepts/rag_triad/):
- Context relevance (retriever quality)
- Groundedness (generator stays in context)
- Answer relevance (final answer addresses question)

All three are LLM-as-judge. Failure at any vertex names the failure mode.

### 9. Agent-specific evaluation

Anthropic, ["Demystifying evals for AI agents"](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) (Jan 2026):
- Grade outcomes, not exact tool sequences; rigid trajectory checks penalize valid paths. Give partial credit on multi-part tasks.
- pass@k (at least one of k trials succeeds) fits tasks where one good answer is enough; pass^k (all k succeed) fits customer-facing reliability. They diverge sharply as k grows.
- Start each trial from a clean, isolated environment; shared state inflates scores and correlates failures.
- Read transcripts to validate graders; a task at 0% across many trials usually means a broken task or grader.
- Balance sets: include cases where the behavior should and shouldn't happen.
- Capability evals start low and give room to climb; graduate saturated ones into regression suites that should stay near 100%.

Standard agent metrics: task completion rate, tool-use accuracy (right tool, right arguments), trajectory length (flag outliers as loops), tool-error recovery, cost per completed task.

### 10. Eval-driven development (EDD)

[Red Hat — "Eval-Driven Development", March 23, 2026](https://developers.redhat.com/articles/2026/03/23/eval-driven-development-build-evaluate-ai-agents). Framing: evals are the new code review. Define the behavior spec, build the golden set, record a baseline, run every prompt / model / RAG change through the suite, gate merges on significance, fail the build on regression, and monitor drift in production. The suite is versioned alongside the prompt.

### 11. Drift detection and production monitoring

- Phoenix / Arize — embedding-centroid distance across time windows for semantic drift in inputs or outputs.
- Galileo — failure-mode mining across production traces.
- Helicone / Langfuse — cost, latency, and error-rate drift.

Set alert thresholds during the eval baseline and alert on crossings; dashboards alone don't catch drift.

### 12. Benchmark literacy

| Benchmark | Status in 2026 | Source |
|---|---|---|
| MMLU / MMLU-Pro, GPQA Diamond, MATH, HumanEval | Near-saturated at the frontier; triage only | Standard |
| SWE-bench Verified | Contaminated: OpenAI stopped reporting it in Feb 2026 and points to SWE-bench Pro | [OpenAI](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/) |
| SWE-bench Pro, Terminal-Bench | Harder coding / terminal-agent successors | Project sites |
| Humanity's Last Exam | Expert-level closed-ended questions | Project site |
| GAIA | General assistant with tools | [arXiv:2311.12983](https://arxiv.org/abs/2311.12983); [HAL leaderboard](https://hal.cs.princeton.edu/gaia) |
| BFCL v4 | Function calling, multi-turn and agentic | [Berkeley leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html) |
| τ²-bench | Tool-agent reliability over reruns (pass^k) | Project repo |
| HELM | Reproducible multi-metric benchmarking | [Stanford CRFM HELM](https://crfm.stanford.edu/helm/) |

Caution: published benchmarks leak into training data and reward hacking on tool-use benchmarks is documented. Use them for capability triage; use your own private held-out set for production decisions. Verify saturation status live — it changes with every model generation.

## Checklist

- [ ] Behavior spec is precise and falsifiable
- [ ] Golden set n is power-analyzed against the smallest effect size that matters
- [ ] Stratification covers happy paths and named edge cases
- [ ] Golden set is version-controlled alongside prompts
- [ ] Metric is per-behavior, not composite
- [ ] Judge is from a different family than the generator and has measured agreement with human labels
- [ ] Narrow binary criteria (or G-Eval with anchored rubric) for non-deterministic metrics
- [ ] Paired comparison with standard errors (clustered where needed), CI, and effect size
- [ ] Agent evals grade outcomes, report pass@k or pass^k to match the use case, and run in isolated environments
- [ ] CI integration gates merges on regression (Promptfoo / DeepEval / Braintrust)
- [ ] Production drift monitoring in place with alert thresholds
- [ ] Eval suite refresh cadence defined

## Composition / References

Within-domain pairings:
- Pairs with the sibling AI skill on RAG patterns (RAGAS / RAG Triad scoring lives here).
- Pairs with the sibling AI skill on agent design (agent trajectory evals).
- Pairs with the sibling AI skill on cost optimization (latency / cost metrics are first-class eval categories).
- Pairs with the sibling AI skill on prompt injection defense (safety / red-team evals).

Primary sources:
- [G-Eval, arXiv:2303.16634](https://arxiv.org/abs/2303.16634), Liu et al., EMNLP 2023
- [Preference Leakage, arXiv:2502.01534](https://arxiv.org/abs/2502.01534), Li et al., ICLR 2026
- [A statistical approach to model evaluations (Miller), arXiv:2411.00640](https://arxiv.org/abs/2411.00640)
- [Anthropic — Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- [RAGAS, arXiv:2309.15217](https://arxiv.org/abs/2309.15217)
- [TruLens RAG Triad](https://www.trulens.org/getting_started/core_concepts/rag_triad/)
- [DeepEval LLM evals](https://deepeval.com/docs/metrics-llm-evals)
- [Red Hat — Eval-Driven Development, March 2026](https://developers.redhat.com/articles/2026/03/23/eval-driven-development-build-evaluate-ai-agents)
- [evalstats reference repo](https://github.com/ianarawjo/evalstats)
- [GAIA, arXiv:2311.12983](https://arxiv.org/abs/2311.12983)
- [Princeton HAL leaderboard](https://hal.cs.princeton.edu/gaia)
- [BFCL leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html)
- [HELM, arXiv:2211.09110](https://arxiv.org/abs/2211.09110)
- [OpenAI — Why we no longer evaluate SWE-bench Verified](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/)
- [Inspect (UK AISI)](https://inspect.aisi.org.uk/)
- [Galileo drift monitoring platforms](https://galileo.ai/blog/best-llm-output-drift-monitoring-platforms)
- [Promptfoo](https://www.promptfoo.dev)
