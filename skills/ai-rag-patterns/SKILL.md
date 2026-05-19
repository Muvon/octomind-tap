---
name: ai-rag-patterns
title: "RAG Patterns: Chunking, Retrieval, Reranking, Evaluation"
description: "Operational playbook for designing and tuning production RAG (Retrieval-Augmented Generation) systems in 2026. Covers chunking strategies (fixed/recursive, semantic, late chunking, Anthropic Contextual Retrieval), retrieval (BM25, dense, hybrid with reciprocal rank fusion, ColBERT late-interaction), query rewriting (HyDE, multi-query, decomposition), reranking (Cohere Rerank, cross-encoders, BGE-Reranker), evaluation (RAGAS metrics, TruLens RAG Triad, DeepEval), the seven failure modes (Barnett et al.), agentic RAG patterns, multi-modal RAG (ColPali), and the long-context-vs-RAG trade-off. Use when designing a new RAG pipeline, diagnosing why an existing one underperforms, or evaluating retrieval quality. Output: architecture decisions with cited numbers, not vibes."
license: Apache-2.0
compatibility: "Stack-agnostic. Requires webfetch (for accessing docs and APIs) and a vector store. Many sub-techniques (Cohere Rerank, voyage embeddings, Anthropic Contextual Retrieval) require external API keys."
domains: ai
rules:
  - session(ai)
  - content(rag)
  - content(retrieval)
  - content(chunking)
  - content(embedding)
  - content(embeddings)
  - content(reranker)
  - content(reranking)
  - match(\b(retrieval[\s-]?augmented|RAG)\b)
  - match(\b(vector\s+(db|database|store|search))\b)
  - match(\b(chunking|chunk\s+(size|strategy))\b)
  - match(\b(hybrid\s+(retrieval|search))\b)
  - match(\b(rerank(er|ing)?)\b)
  - match(\b(BM25|dense\s+retrieval|ColBERT|HyDE)\b)
  - match(\b(RAGAS|TruLens|DeepEval)\b)
  - semantic(design a RAG pipeline for my documents)
  - semantic(why is my retrieval missing relevant chunks)
  - semantic(should we use long context or RAG)
  - semantic(evaluate retrieval quality for our agent)
  - semantic(rerank results to improve RAG accuracy)
---

## Overview

Production RAG in 2026 is no longer "embed, retrieve top-5, generate." Three measurable shifts changed the playbook: hybrid retrieval beating either BM25 or dense alone, reranking moving from optional to default, and Anthropic's Contextual Retrieval (September 2024) collapsing retrieval-failure rates dramatically. This skill encodes the patterns that actually move the metrics, with cited numbers and the failure modes they address.

Use this skill when designing a new RAG pipeline, diagnosing why an existing one underperforms, or evaluating retrieval quality before generation. Skip it for simple in-context document Q&A on a small static corpus where long-context generation (1M Sonnet / 2M Gemini) is the cheaper answer — see §6.

## Mental model

A RAG pipeline is a chain of probabilistic filters: chunking decides what units the system can return, indexing decides what's searchable, retrieval ranks candidates, reranking re-orders them, and generation consumes the result. The output is bounded by the weakest link. The seven failure modes (Barnett et al., arXiv:2401.05856) map cleanly: missing content, top-ranked-missed, not-in-context, not-extracted, wrong format, incorrect specificity, incomplete. Diagnose at the layer that owns the failure; tuning generation when retrieval is the bottleneck is wasted effort.

Two compounding levers move 2026 production RAG most: contextual chunking (adding LLM-generated chunk context before indexing) and hybrid retrieval with reranking. The numbers in §1–§3 below are from Anthropic's Contextual Retrieval write-up and the Elastic / TOIS hybrid-retrieval studies.

## Instructions

### 1. Chunking strategies

| Strategy | When to use | Source |
|---|---|---|
| Fixed-size / recursive (LangChain `RecursiveCharacterTextSplitter`) | Baseline; works for prose with stable structure | Practitioner default; no canonical paper |
| Semantic (LlamaIndex `SemanticSplitterNodeParser`) | Mixed-topic documents where boundaries matter | Practitioner pattern; Greg Kamradt "5 levels of chunking" |
| Late Chunking (Jina AI, Sep 2024) | Long documents with rich context; uses 8192-token embedding model, mean-pools after the transformer at chunk boundaries | [arXiv:2409.04701](https://arxiv.org/abs/2409.04701) |
| Anthropic Contextual Retrieval | Production RAG where retrieval quality matters and cost permits ~$1.02 per million doc tokens to pre-process | [Anthropic blog, Sep 2024](https://www.anthropic.com/news/contextual-retrieval) |
| Parent-document / small-to-big | Index small for precision, return parent for context | LangChain `ParentDocumentRetriever`, LlamaIndex `AutoMergingRetriever` |

Anthropic Contextual Retrieval numbers (from a baseline top-20 retrieval-failure rate of 5.7%):
- Contextual Embeddings alone: −35% failure-rate reduction (5.7 → 3.7%)
- Contextual Embeddings + Contextual BM25: −49% (5.7 → 2.9%)
- Contextual Embeddings + Contextual BM25 + Reranking: −67% (5.7 → 1.9%)

The headline 67% requires reranking on top — it is not the chunking technique alone.

### 2. Retrieval — BM25, dense, hybrid

| Method | Strength | Weakness |
|---|---|---|
| BM25 (lexical) | Exact term match, no embedding cost, captures rare terms | Misses paraphrase, synonyms, semantic relationships |
| Dense vector (any modern embedder) | Captures paraphrase and semantic similarity | Weak on rare terms, exact codes, proper nouns |
| Hybrid (BM25 + dense, reciprocal rank fusion) | Combines both signals; outperforms either alone on most production corpora | More moving parts, two indices to maintain |
| ColBERT / late interaction | Token-level matching; strong for queries needing exact-phrase grounding | More expensive than dense |

Hybrid numbers — Elastic Search Labs reports reciprocal rank fusion at +18% NDCG@10 over BM25 alone and +1.4% over ELSER alone on the BEIR benchmark ([Elastic — hybrid retrieval](https://www.elastic.co/search-labs/blog/improving-information-retrieval-elastic-stack-hybrid)). ACM TOIS (Bruch et al., 2023, doi:10.1145/3596512) shows convex combination at α≈0.5 reaches Recall@5 = 0.726 vs RRF k=60 at 0.695 — tuned weighting beats RRF given ~40 labeled query-result pairs to fit α.

Reciprocal Rank Fusion — Cormack, Clarke, Büttcher, SIGIR 2009 (canonical paper). The formula combines ranks across retrievers: `RRF_score(d) = Σ 1 / (k + rank_i(d))`, default `k=60`.

ColBERTv2 — Santhanam et al., NAACL 2022. `jina-colbert-v2` reports +6.5% nDCG@10 over ColBERTv2; `jina-reranker-v3` reports 61.85 nDCG@10 on BEIR, +4.79% over v2 ([arXiv:2509.25085](https://arxiv.org/html/2509.25085v3)).

### 3. Query rewriting / expansion

| Technique | What it does | Source |
|---|---|---|
| HyDE | LLM generates a hypothetical answer document, embeds that for retrieval | [arXiv:2212.10496](https://arxiv.org/abs/2212.10496), Gao et al. Dec 2022 |
| Multi-query | LLM rewrites the query into N variations; retrieve for each; merge | LangChain `MultiQueryRetriever` |
| Decomposition / least-to-most | Break a complex question into sub-questions; retrieve and answer each | [arXiv:2205.10625](https://arxiv.org/abs/2205.10625), Zhou et al. May 2022 |
| Query routing | LLM picks which retriever / index / corpus to use | LlamaIndex `RouterQueryEngine`; agentic-RAG survey [arXiv:2501.09136](https://arxiv.org/abs/2501.09136) |

Query rewriting is most impactful when user queries are short or ambiguous (chat agents, voice agents). For well-formed search queries, the lift is marginal.

### 4. Reranking

Reranking is the second filter: take 50–100 candidates from first-stage retrieval, score with a more expensive model, return top 3–10.

| Reranker | Source |
|---|---|
| Cohere Rerank 3.5 / 4 | [Cohere Rerank docs](https://docs.cohere.com/docs/rerank) — pricing $2 per 1K searches (1 query + up to 100 docs) |
| Cross-encoders (`sentence-transformers/ms-marco-MiniLM-L-6-v2`) | Reimers & Gurevych, EMNLP 2019 |
| BGE-Reranker (`bge-reranker-v2-m3`) | Xiao et al., BAAI, [arXiv:2309.07597](https://arxiv.org/abs/2309.07597) |
| ColBERT as reranker | Late-interaction over first-stage top-k |

Anthropic's Contextual Retrieval write-up reports reranking adds ~18% relative failure-rate reduction on top of hybrid Contextual Retrieval. No single canonical "typical lift" exists — it depends on first-stage noise level. Vendor blogs cite "20–35% RAG accuracy lift" and "NDCG@5 +18 points" — these are vendor-reported, not peer-reviewed, so treat as ballpark.

### 5. Evaluation

Three frameworks dominate; use one as primary, cross-check with another.

| Framework | Metrics | Source |
|---|---|---|
| RAGAS | Faithfulness, answer relevancy, context precision, context recall, context entity recall | Es et al., EACL 2024, [arXiv:2309.15217](https://arxiv.org/abs/2309.15217); [RAGAS metrics docs](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/) |
| TruLens RAG Triad | Context relevance, groundedness, answer relevance | [trulens.org RAG Triad](https://www.trulens.org/getting_started/core_concepts/rag_triad/) |
| DeepEval | G-Eval, HallucinationMetric, ContextualPrecision/Recall/Relevancy | [DeepEval LLM evals](https://deepeval.com/docs/metrics-llm-evals); G-Eval based on Liu et al., EMNLP 2023, [arXiv:2303.16634](https://arxiv.org/abs/2303.16634) |

RAGAS scores — original paper reports human-agreement 95% / 78% / 70% on faithfulness / answer relevance / context relevance. Production threshold: >0.8 on faithfulness and context precision is strong; depends on domain.

Recommended flow (practitioner consensus, not a single citation):
1. Offline golden-set: tune retriever with RAGAS context precision/recall.
2. Tune generator: faithfulness + answer relevancy.
3. Online tracing: Phoenix or LangSmith with LLM-as-judge sampling on production traffic.

Cross-check with the eval-design skill in the same domain for statistical-significance methodology and judge selection.

### 6. Long context vs RAG (the 2025–2026 question)

Anthropic Sonnet/Opus 1M context (Aug 2025); Gemini 1.5/2.0 Pro 2M context. The question: does long-context generation replace RAG?

Databricks "Long Context RAG Performance of LLMs" ([blog](https://www.databricks.com/blog/long-context-rag-performance-llms)) finds long-context QA beats chunk-RAG on stable, single-doc tasks but Gemini 1.5 underperforms o1 / GPT-4o / Sonnet 3.5 on DocsQA and FinanceBench. The RULER benchmark (Hsieh et al., [arXiv:2404.06654](https://arxiv.org/abs/2404.06654)) shows advertised context degrades early — effective context is shorter than the stated window.

Practitioner consensus (no single citation): use hybrid — retrieve a wider top-50 to top-100K-token shortlist, then long-context generate over the shortlist. Pure long-context loses on cost, citation auditability, and corpus freshness; pure short-RAG loses on multi-step reasoning across distant context. Pick by corpus size, refresh rate, citation requirements, and budget.

### 7. Multi-modal RAG

| Technique | Use case | Source |
|---|---|---|
| ColPali | Document images, PDFs with charts/tables, slides | Faysse et al., [arXiv:2407.01449](https://arxiv.org/abs/2407.01449), Jun 2024; introduces ViDoRe benchmark |
| ColQwen2, ColSmol | Smaller / multi-language variants | [illuin-tech/colpali](https://github.com/illuin-tech/colpali) |

ColPali beats text-extraction-then-embed pipelines on document-image benchmarks. Use it when the corpus is visually rich (scans, slides, layouts that don't OCR cleanly).

### 8. Agentic RAG

Singh et al., "Agentic Retrieval-Augmented Generation: A Survey" ([arXiv:2501.09136](https://arxiv.org/abs/2501.09136), Jan 2025). Patterns: reflection (re-query if confidence low), planning (decompose then retrieve per sub-question), tool use (route between corpora and tools), multi-agent (specialist sub-agents per corpus).

Use agentic RAG when queries are heterogeneous (some need code search, some need docs, some need web), or when single-pass retrieval has known failure modes the agent can detect and recover from. Cost: 2–4× a single-pass RAG; justify with evidence the simpler design failed.

### 9. The seven failure modes (Barnett et al.)

[arXiv:2401.05856](https://arxiv.org/abs/2401.05856), Jan 2024 — canonical failure taxonomy:
1. Missing content — answer isn't in the corpus
2. Top-ranked missed — relevant chunk exists but wasn't retrieved
3. Not in context — retrieved but didn't make the generator's prompt window
4. Not extracted — in the prompt but generator missed it (often context pollution)
5. Wrong format — extracted correctly but presented incorrectly
6. Incorrect specificity — too general or too specific for the question
7. Incomplete — partial answer

Diagnose at the failing layer; map fix to the right intervention (corpus curation, retrieval tuning, reranking, chunk-size, generator prompting).

### 10. Production patterns checklist

- [ ] Chunking strategy chosen with rationale tied to corpus structure
- [ ] Retrieval is hybrid (BM25 + dense + RRF or convex combination)
- [ ] Reranking on top-50 to top-100 first-stage results
- [ ] Query rewriting where queries are short / ambiguous
- [ ] Eval suite using RAGAS or TruLens RAG Triad with a versioned golden set
- [ ] Production tracing via Phoenix / LangSmith / Langfuse
- [ ] Drift monitoring on retrieval (embedding centroid distance over time)
- [ ] Long-context vs RAG decision documented with rationale
- [ ] Multi-modal corpus uses ColPali-family when documents are visually rich
- [ ] Agentic patterns only when single-pass has documented failure modes

## Composition / References

Within-domain pairings:
- Pairs with the sibling AI skill on agent design (RAG often lives inside an agent loop with retrieval as a tool).
- Pairs with the sibling AI skill on evals (every RAG decision is gated by RAGAS / RAG Triad measurement).
- Pairs with the sibling AI skill on cost optimization (embedding + rerank + vector DB costs are the RAG-specific FinOps lever).

Primary sources:
- [Anthropic — Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)
- [Late Chunking, arXiv:2409.04701](https://arxiv.org/abs/2409.04701)
- [RAGAS, arXiv:2309.15217](https://arxiv.org/abs/2309.15217)
- [TruLens RAG Triad](https://www.trulens.org/getting_started/core_concepts/rag_triad/)
- [Seven Failure Points of RAG, arXiv:2401.05856](https://arxiv.org/abs/2401.05856)
- [Cormack et al. RRF, SIGIR 2009](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)
- [HyDE, arXiv:2212.10496](https://arxiv.org/abs/2212.10496)
- [Elastic Search Labs — hybrid retrieval](https://www.elastic.co/search-labs/blog/improving-information-retrieval-elastic-stack-hybrid)
- [Hybrid Fusion ACM TOIS](https://dl.acm.org/doi/full/10.1145/3596512)
- [ColPali, arXiv:2407.01449](https://arxiv.org/abs/2407.01449)
- [Agentic RAG Survey, arXiv:2501.09136](https://arxiv.org/abs/2501.09136)
- [RULER, arXiv:2404.06654](https://arxiv.org/abs/2404.06654)
- [Databricks long-context RAG performance](https://www.databricks.com/blog/long-context-rag-performance-llms)
- [Cohere Rerank docs](https://docs.cohere.com/docs/rerank)
- [DeepEval LLM evals](https://deepeval.com/docs/metrics-llm-evals)
