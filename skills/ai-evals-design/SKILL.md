---
name: ai-evals-design
title: "AI Evals Design: Golden Sets, Metrics, Significance, CI"
description: "Operational playbook for designing production LLM evaluation in 2026. Covers eval framework selection (Promptfoo, DeepEval, Maxim, LangSmith, Braintrust, Phoenix, Galileo, Patronus), golden dataset construction (size, stratification, versioning), synthetic data generation, LLM-as-judge design with G-Eval methodology (Liu et al., EMNLP 2023), preference-leakage mitigation (Wong et al. 2025), statistical significance testing (McNemar's, paired t, Bayesian pairwise, bootstrap), RAG metrics (RAGAS, TruLens RAG Triad), agent trajectory evaluation, drift detection, eval-driven development (Red Hat, March 2026), CI/CD prompt-regression gates, and benchmark literacy (GAIA, BFCL, SWE-Bench Verified, MMLU-Pro, GPQA Diamond, HELM, τ-Bench). Use when designing an eval suite, validating a prompt change, gating a deploy, or diagnosing production quality drift. Output: eval verdicts with statistical evidence, not vibe judgments."
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

In 2026, eval engineering is a discipline with its own job title, its own salary band, and its own framework ecosystem. "Evals are the new code review" — Red Hat's "Eval-Driven Development" (EDD) article (March 23, 2026) made the framing explicit; ~75% of AI engineer interview questions now focus on evaluation. The reason: every prompt and model change is a stochastic intervention into a behavior surface, and "looks better" is not a verdict. This skill encodes the methodology that turns LLM evaluation from anecdote into evidence.

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

### 1. Framework landscape (May 2026)

| Framework | OSS / paid | Best for | Source |
|---|---|---|---|
| Promptfoo | OSS CLI + YAML | Local dev loop, red-team mode (157 plugins, OWASP-LLM + NIST AI RMF presets) | [promptfoo.dev](https://www.promptfoo.dev) |
| DeepEval (Confident AI) | OSS Python + paid cloud | 50+ metrics (G-Eval, hallucination, faithfulness, contextual precision/recall/relevancy); synthetic dataset generation | [deepeval.com](https://deepeval.com/docs/getting-started) |
| Maxim AI | Paid | Simulation + eval + observability + gateway in one stack | [getmaxim.ai](https://www.getmaxim.ai/) |
| LangSmith | Paid (per-seat) | Deepest LangChain / LangGraph integration; trajectory evals for agents | [docs.smith.langchain.com](https://docs.langchain.com/langsmith/) |
| Braintrust | Paid | Dataset → scoring → monitoring → CI gating | [braintrust.dev](https://www.braintrust.dev) |
| Helicone | OSS Rust gateway | Lightweight proxy logging | [helicone.ai](https://www.helicone.ai/) |
| Phoenix (Arize) | OSS | Observability + embedding-drift clustering | [arize.com/phoenix](https://arize.com/phoenix/) |
| Galileo | Paid | Galileo Signals (failure-mode mining); Luna-2 small-model evaluators | [galileo.ai](https://galileo.ai/) |
| Patronus AI | Paid | Eval-first; hallucination + safety detectors | [patronus.ai](https://www.patronus.ai/) |

Common production pattern: Helicone as gateway (always-on cost/latency logging) + Langfuse or Phoenix for trace storage + DeepEval or Promptfoo for the actual eval suites in CI.

### 2. Golden dataset construction

| Property | Guidance |
|---|---|
| Size | 50–500 examples typical for prompt-level evals; agent-level evals can need 200–1000 due to multi-step variance |
| Stratification | Cover intents, edge cases, hard negatives, multilingual variants, length extremes — not just happy paths |
| Source | Production traffic samples (with PII redaction) + handcrafted edge cases + synthetic adversarial examples |
| Version control | Stored alongside prompts in git; versioned; tagged with the prompt/model commit they were created against |
| Refresh cadence | Every quarter or when behavior shifts; add examples for newly observed failure modes |
| Labels | Ground truth where possible (gold answers); for open-ended outputs, judge-rubric criteria suffice |

Power analysis — when you want to detect an effect size of ~5 percentage points with 80% power and α=0.05, n ≈ 200 paired examples (rough rule-of-thumb for proportions). Smaller effects need larger n. Don't run an n=20 eval and report a "result."

### 3. Synthetic data generation

- DeepEval Synthesizer — input → evolve → score on self-containment and clarity; multi-turn supported ([DeepEval Synthesizer docs](https://deepeval.com/docs/synthesizer-introduction)).
- OpenAI Evals registry — YAML grader patterns; broad community-contributed eval set.
- Adversarial example mining — for safety / robustness, mine known jailbreak datasets (PyRIT 53+ datasets, garak 37+ probes) for relevant patterns.

Synthetic data complements, never replaces, real production traffic. Use it to fill stratification gaps (rare intents, edge cases) — not to substitute for the messy reality of real users.

### 4. LLM-as-judge — G-Eval methodology

[G-Eval](https://arxiv.org/abs/2303.16634) — Liu et al., EMNLP 2023. Chain-of-thought prompting + form-filling paradigm. Reports 0.514 Spearman correlation with human ratings on summarization tasks — the strongest open methodology for LLM-as-judge at the time of publication.

G-Eval workflow:
1. Define the evaluation criterion in narrow, explicit terms (broad criteria collapse to noise).
2. Have the judge model generate a chain of thought reasoning about the criterion.
3. Have the judge fill a structured score form (e.g., 1–5 scale with anchor descriptions per score).
4. Use multiple judge runs or multiple judge models if score variance is high.

DeepEval's `GEval` metric implements this directly. Use it when human-aligned scoring is needed and a deterministic metric doesn't fit.

### 5. Preference leakage and self-bias mitigation

[Preference leakage](https://arxiv.org/abs/2502.01534) — Wong et al., 2025. When the judge model is from the same family as the generator (or trained on similar data), evaluation scores inflate. Reports ~23.6% leakage on SFT-aligned data. GPT-4o and Claude 3.5 prefer their own-family outputs in measurable ways ([self-bias paper](https://arxiv.org/html/2508.06709v1) — verify exact models cited).

Mitigations:
- Use a judge from a different model family than the generator (e.g., Claude judges OpenAI outputs and vice versa).
- Run a small human-validation set (n=20–50) against the judge; calibrate.
- Use multiple judges from different families; report disagreement as a confidence signal.
- For pairwise comparisons, randomize positions and run both orderings.

### 6. Statistical significance

| Test | When | Source |
|---|---|---|
| McNemar's test | Paired binary outcomes (pass/fail) | Cameron Wolfe — [Stats for LLM evals](https://cameronrwolfe.substack.com/p/stats-llm-evals) |
| Paired t-test (modified for k-fold) | Paired continuous scores; k-fold cross-validation | [evalstats repo](https://github.com/ianarawjo/evalstats) |
| Bayesian pairwise | Small N (<50); preferred over bootstrap | Same source |
| Bootstrap | When parametric assumptions fail; medium N | Standard |

Mandatory output for any "we improved X" claim: effect size + significance level + sample size + confidence interval. Point estimates without uncertainty are not eval results.

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

LangSmith multi-turn evals ([docs](https://docs.langchain.com/langsmith/trajectory-evals)) — score semantic intent + final outcome + trajectory (tool-call sequence and arguments).

OSS `agentevals` package — trajectory match (exact or fuzzy) or LLM-judge for trajectories.

Standard agent metrics:
- Task completion rate — fraction of golden tasks the agent finished correctly
- Tool-use accuracy — fraction of tool calls that picked the right tool with right arguments
- Trajectory length — average number of steps; flag outliers as potential loops
- Tool-error recovery — fraction of error-encountered runs that completed anyway
- Cost per task — total tokens × $/token, including all turns

### 10. Eval-driven development (EDD)

[Red Hat — "Eval-Driven Development", March 23, 2026](https://developers.redhat.com/articles/2026/03/23/eval-driven-development-build-evaluate-ai-agents). Eight-stage framework with DeepEval + multi-turn + CI/CD for Red Hat AI agents. Framing: "evals are the new code review."

EDD workflow:
1. Define behavior spec.
2. Build golden set.
3. Implement first version.
4. Run eval suite; record baseline.
5. Iterate: every change runs through the suite.
6. Statistical significance gate before merge.
7. CI fail-the-build on regression.
8. Production drift monitoring.

Every prompt / model / RAG change runs through the suite before merge. The suite is versioned alongside the prompt. The suite fails the build on regression.

### 11. Drift detection and production monitoring

- Arize / Phoenix — embedding-centroid distance across time windows for semantic drift in inputs or outputs ([Arize blog on agent observability](https://arize.com/blog/best-ai-observability-tools-for-autonomous-agents-in-2026/)).
- Galileo — Galileo Signals; failure-mode mining across production traces ([Galileo blog](https://galileo.ai/blog/best-llm-output-drift-monitoring-platforms)).
- Helicone — proxy-level cost / latency / error rate drift.

Drift alerting — set thresholds during eval baseline; alert on threshold crossings; do not just review dashboards.

### 12. Benchmark literacy

| Benchmark | What it measures | Source |
|---|---|---|
| MMLU / MMLU-Pro | General knowledge, 14 subjects, 10-choice | [Artificial Analysis MMLU-Pro](https://artificialanalysis.ai/evaluations/mmlu-pro) |
| GPQA Diamond | "Google-proof" PhD-level questions; 198 examples; PhDs ~65% | [GPQA Diamond](https://artificialanalysis.ai/evaluations/gpqa-diamond) |
| MATH, HumanEval | Math and code basics; both largely saturated | Standard |
| SWE-Bench Verified | Real GitHub issues; production code-agent benchmark | Standard |
| GAIA | General assistant with tools | Meta / HF, [arXiv:2311.12983](https://arxiv.org/abs/2311.12983); Princeton [HAL leaderboard](https://hal.cs.princeton.edu/gaia) |
| AgentBench | Multi-environment agent benchmark | Standard |
| BFCL v4 | Function-calling evaluation; AST-based scoring, 2000+ Q/F/A pairs; serial + parallel + multi-turn | [Berkeley leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html); ICML 2025 paper |
| τ-Bench | Reliability over reruns; how consistent is the model | Standard |
| HELM | 7 metrics × 16 scenarios; reproducible benchmarking | [Stanford CRFM HELM](https://crfm.stanford.edu/helm/); [arXiv:2211.09110](https://arxiv.org/abs/2211.09110) |

Caution: published benchmarks have known training-set contamination; reward-hacking on tool-use benchmarks has been documented. Use them for capability triage; use your own held-out golden set for production decisions. Anthropic publishes detailed system cards with capability + safety eval methodology (e.g., Claude Opus 4.6, Feb 2026 — see [Claude system card](https://www.anthropic.com/claude-opus-4-6-system-card)).

### 13. Common pitfalls

- Small golden sets that overfit to whichever examples were handy when the prompt was tuned.
- Single-metric eval — one number hides regressions in the components.
- Same model family for generator and judge — preference leakage inflates scores.
- No statistical significance — point estimates reported as "improvements."
- Eval suite not in CI — devs forget to run it.
- Eval suite never refreshed — production drift moves past the golden set's relevance.

## Checklist

- [ ] Behavior spec is precise and falsifiable
- [ ] Golden set n is power-analyzed against the smallest effect size that matters
- [ ] Stratification covers happy paths and named edge cases
- [ ] Golden set is version-controlled alongside prompts
- [ ] Metric is per-behavior, not composite
- [ ] Judge model is from a different family than generator (or human-validated rubric)
- [ ] G-Eval method used for non-binary criteria
- [ ] Statistical significance test selected to match data shape
- [ ] Effect size + CI reported alongside p-value
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
- [Preference Leakage, arXiv:2502.01534](https://arxiv.org/abs/2502.01534), Wong et al., 2025
- [RAGAS, arXiv:2309.15217](https://arxiv.org/abs/2309.15217)
- [TruLens RAG Triad](https://www.trulens.org/getting_started/core_concepts/rag_triad/)
- [DeepEval LLM evals](https://deepeval.com/docs/metrics-llm-evals)
- [Red Hat — Eval-Driven Development, March 2026](https://developers.redhat.com/articles/2026/03/23/eval-driven-development-build-evaluate-ai-agents)
- [Cameron Wolfe — Stats for LLM evals](https://cameronrwolfe.substack.com/p/stats-llm-evals)
- [evalstats reference repo](https://github.com/ianarawjo/evalstats)
- [GAIA, arXiv:2311.12983](https://arxiv.org/abs/2311.12983)
- [Princeton HAL leaderboard](https://hal.cs.princeton.edu/gaia)
- [BFCL leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html)
- [HELM, arXiv:2211.09110](https://arxiv.org/abs/2211.09110)
- [Anthropic Claude Opus 4.6 system card](https://www.anthropic.com/claude-opus-4-6-system-card)
- [OpenAI–Anthropic joint safety evaluation pilot](https://openai.com/index/openai-anthropic-safety-evaluation/)
- [Galileo drift monitoring platforms](https://galileo.ai/blog/best-llm-output-drift-monitoring-platforms)
- [Promptfoo](https://www.promptfoo.dev)
