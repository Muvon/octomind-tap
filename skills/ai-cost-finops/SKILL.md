---
name: ai-cost-finops
title: "AI Cost & FinOps: Caching, Batching, Model Routing"
description: "Operational playbook for cutting LLM application cost in 2026. Covers provider pricing (Anthropic Claude Opus/Sonnet/Haiku, OpenAI GPT-4o/o-series, Google Gemini Pro/Flash), Anthropic prompt caching (90% discount on cached tokens, up to 85% latency cut), OpenAI automatic prompt caching (50% discount), Anthropic/OpenAI/Gemini Batch APIs (50% off), model routing patterns (Martian, NotDiamond, OpenRouter Auto vs manual rules), token economics (output 3–8× input), structured output cost wins, RAG cost stack (embeddings, rerank, vector DBs), and FinOps observability (Helicone, Langfuse, Phoenix, LangSmith, Vantage). Use when projecting LLM cost, hunting waste in an existing pipeline, picking a model, or setting up per-feature attribution. Output: cost projections with cited prices and quantified optimization levers."
license: Apache-2.0
compatibility: "Stack-agnostic. FinOps observability typically needs a proxy (Helicone) or instrumented SDK (Langfuse / Phoenix / OpenLLMetry / Vantage). All major providers expose Batch APIs and prompt caching."
domains: ai
rules:
  - session(ai)
  - content(cost)
  - content(token)
  - content(tokens)
  - content(caching)
  - content(batch)
  - content(pricing)
  - match(\b(token\s+(cost|economics|budget|usage|waste))\b)
  - match(\b(prompt\s+caching|cache\s+control)\b)
  - match(\b(batch\s+api)\b)
  - match(\b(model\s+(routing|selection|router))\b)
  - match(\b(finops|cost\s+optimization|reduce\s+(ai|llm)\s+cost)\b)
  - match(\b(Haiku|Sonnet|Opus|GPT-?4o|o1|Gemini\s+(Pro|Flash))\b)
  - match(\b(Helicone|Langfuse|Vantage|Phoenix|LangSmith|OpenLLMetry)\b)
  - semantic(reduce our LLM API spend)
  - semantic(why is our AI bill so high)
  - semantic(should we use Opus or Haiku for this)
  - semantic(set up cost tracking for our AI features)
  - semantic(what does prompt caching save)
---

## Overview

LLM cost is now a measurable engineering surface, not a line on the credit-card statement. Three levers move it most in 2026: prompt caching (Anthropic 90% / OpenAI 50% discount on cached tokens), Batch APIs (50% off across major providers), and model routing (Haiku vs Sonnet vs Opus at 5× cost spreads). This skill encodes the price book, the discount mechanics, and the optimization patterns with current numbers and primary-source citations.

Use this skill when projecting LLM cost for a new feature, hunting waste in an existing pipeline, picking a model, setting up per-feature attribution, or building a FinOps dashboard. Skip it for one-off prototypes where total spend stays under $100/month — over-optimizing tiny budgets is the engineering equivalent of premature optimization.

## Mental model

Every LLM call has a cost equation: `input_tokens × $/M_in + output_tokens × $/M_out` plus retrieval/rerank/storage if RAG. Three discounts apply: prompt caching on the input side, Batch APIs on whole calls, model routing on which model gets the call. Every optimization is a move along one of those axes. The cheapest call is the one not made; the second cheapest is the one cached; the third is the one batched; the fourth is the one routed to the smaller model.

Output tokens are 3–8× input tokens in cost across providers — the dominant lever after caching is output-length discipline (no markdown when consumer is machine, no preambles, no "let me think through this" verbosity on tasks that don't need reasoning).

## Instructions

### 1. Provider pricing (May 2026, per 1M tokens, input/output)

| Provider | Model | Input | Output | Notes |
|---|---|---|---|---|
| Anthropic | Haiku 4.5 | $1 | $5 | |
| Anthropic | Sonnet 4.6 | $3 | $15 | |
| Anthropic | Opus 4.7 | $5 | $25 | Tokenizer can emit up to 35% more tokens than 4.6 — verify per-call output budget |
| OpenAI | GPT-4o | $2.50 | $10 | |
| OpenAI | GPT-4o-mini | $0.15 | $0.60 | 16× cheaper than GPT-4o |
| OpenAI | o1 | $15 | $60 | Reasoning model |
| OpenAI | o3 | $2 | $8 | |
| OpenAI | o4-mini | $1.10 | $4.40 | |
| Google | Gemini 3.1 Pro | $2 | $12 | ≤200K context; $4 / $18 above 200K |
| Google | Gemini 3 Flash | $0.50 | $3 | |
| Google | Gemini 3.1 Flash-Lite | $0.25 | $1.50 | |

Sources: [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing), [OpenAI pricing](https://openai.com/api/pricing/), [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing). Verify against live pages — prices update. Output tokens cost ~3–5× input on most models; o1 sits at 4×; some frontier models reach 8× (verify GPT-5.2 Pro reportedly $21/$168 — claim seen in secondary sources, verify on primary).

### 2. Prompt caching

Anthropic prompt caching ([docs](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)):
- Cache writes cost 1.25× input (5-min TTL) or 2.0× input (1-hour TTL).
- Cache reads cost 0.10× input — 90% discount on cached tokens.
- Up to 85% latency reduction on cached prefixes (per Anthropic's docs).
- Mechanism: `"cache_control": {"type": "ephemeral", "ttl": "1h"}` on message blocks. Default TTL was silently changed from 1h to 5min in March 2026 — set explicitly.
- Stacks with Batch API (batch 50% off + cache 90% off ≈ 95% off the input portion).

OpenAI automatic prompt caching ([announcement](https://openai.com/index/api-prompt-caching/), [guide](https://developers.openai.com/api/docs/guides/prompt-caching)):
- Automatic 50% discount on cached prefixes — no code change.
- Kicks in at ≥1024 tokens.
- Cache evicted after 5–10 min idle, 1h max.

What to cache: system prompts, long tool/skill definitions, retrieval pre-context, few-shot examples — anything long, stable, and re-sent. The break-even on Anthropic 5-min cache writes is ~2 cache hits (you pay 1.25× write, save 0.90× × N reads); for 1-hour cache the break-even is ~3 hits.

### 3. Batch APIs (50% off everything that doesn't need real-time)

- Anthropic Message Batches — 50% discount, up to 10,000 requests per batch, 24-hour SLA, stacks with prompt caching. [docs](https://platform.claude.com/docs/en/build-with-claude/batch-processing).
- OpenAI Batch API — 50% discount on all models including embeddings; batched-on-cached gets additional 50% (so 25% of original price). [docs](https://developers.openai.com/api/docs/guides/batch).
- Gemini Batch — 50% off, inline or JSONL input, context caching applies. [docs](https://ai.google.dev/gemini-api/docs/batch-api).

Use cases: evals, bulk processing, async pipelines, embeddings backfill, dataset enrichment. If real-time isn't required, batch it — there's no reason not to take the discount.

### 4. Model routing

| Approach | Pros | Cons |
|---|---|---|
| Manual rules (classify by complexity) | Predictable; cheap; auditable | Requires upfront classification logic |
| Martian | Vendor-claimed savings up to 98% | Black-box; verify on your traffic |
| NotDiamond | Vendor-claimed up to 10× cheaper | RouterArena benchmark ranks NotDiamond #12 by cost efficiency — chooses expensive models often |
| OpenRouter Auto | Powered by NotDiamond, 33 model pool | Same caveat |

Practitioner pattern (cheaper and more predictable than commercial routers): default to the small model (Haiku, Gemini Flash, GPT-4o-mini) for typical traffic; escalate to mid-tier (Sonnet, Gemini Pro, GPT-4o) when classification confidence is low or output validation fails; reserve frontier (Opus, o1) for hard-reasoning paths only. GPT-4o-mini is 16× cheaper than GPT-4o; the typical Haiku-vs-Opus spread is 5× on input and 5× on output.

Source: [RouterArena benchmark, arXiv:2510.00202](https://arxiv.org/html/2510.00202v1) — commercial routers often gain accuracy at higher cost; manual rules with explicit fallback are competitive on cost-effectiveness.

### 5. Token economics

| Lever | Magnitude |
|---|---|
| Output is 3–5× input on most models | Cost equation dominator after caching |
| Reasoning models waste >55% of budget on filler thought | Studies on chain-of-thought wastage |
| Chain-of-Draft matches CoT accuracy at 7.6% of tokens | Latest research on compact CoT |
| Structured output (JSON over prose) | Cuts output ~60% in typical fields |
| TOON format | Vendor claim: 40–50% reduction on structured reference inputs (verify) |

Source: [codeant.ai — input vs output token cost](https://www.codeant.ai/blogs/input-vs-output-vs-reasoning-tokens-cost).

Practical implications:
- Strip markdown when the consumer is a machine — every `` and `#` is wasted tokens.
- Use structured outputs (JSON Schema / function calling) — kills preambles and apologies; constrains the output surface.
- Ban "let me think through this..." preambles via system prompt for tasks that don't benefit from reasoning.
- Use Chain-of-Draft for arithmetic / logic over full CoT.

### 6. FinOps observability and attribution

| Tool | Mode | Strength | Pricing |
|---|---|---|---|
| Helicone | Gateway (1-URL swap) | Zero markup; OSS Rust | Pro $79/mo |
| Langfuse | SDK or OTLP | OSS (MIT, 19k+ stars); per-generation cost tracking | Cloud from $29/mo |
| LangSmith | SDK | Deepest LangChain integration | $39/seat Plus |
| Phoenix (Arize) | OSS | Local-first; OTLP-native | Free / cloud paid |
| OpenLLMetry (Traceloop) | OSS | Vendor-neutral OTel instrumentation | Free / cloud paid |
| Vantage AI | FinOps platform | Cross-provider roll-up; per-team / per-customer allocation via virtual tags; MCP server; FinOps Agent | Paid, FinOps tiers |

Sources: [Langfuse cost docs](https://langfuse.com/docs/observability/features/token-and-cost-tracking), [Phoenix repo](https://github.com/Arize-ai/phoenix), [Vantage FinOps for AI](https://www.vantage.sh/blog/finops-for-ai-token-costs).

Common production pattern: Helicone as gateway for always-on cost/latency logging + Langfuse or Phoenix for trace-level analysis + Vantage for FinOps roll-up across AI providers and cloud infra in one pane.

Per-feature attribution: tag every call with `feature`, `team`, `customer_tier`, `experiment_arm` headers (Helicone) or trace attributes (Langfuse / Phoenix). Without attribution, you can't optimize what you can't measure.

### 7. Common waste patterns

| Pattern | Impact | Fix |
|---|---|---|
| Over-retrieved RAG context (10× 500-token docs = 5K tokens) | Input bloat per call | Reranker + tighter top-k |
| Uncached system prompts re-sent every request | Pay full input per turn | Prompt caching on system prompt + tool defs |
| JSON parse-retry loops | 2–3× the cost on flaky calls | Structured outputs / strict tool mode |
| Verbose CoT on tasks that don't need reasoning | Output bloat | Chain-of-Draft; ban preambles via system prompt |
| Default to Opus/o1 when Haiku/4o-mini suffices | 5–20× over-spend | Model routing with eval validation per tier |
| No streaming → no fail-fast | Pay for bad output | Stream + abort on quality signals |
| Markdown formatting when consumer is machine | Output bloat | Plain text / JSON output |

### 8. RAG cost stack

Embeddings (per 1M tokens):
- text-embedding-3-small: $0.02
- voyage-3 lite: $0.02; voyage-3: $0.06; voyage-3-large: $0.12
- Cohere Embed v3: $0.10; v4: $0.12 (text)

Reranking ([Cohere pricing](https://cohere.com/pricing)):
- Cohere Rerank 3.5: $2 per 1K searches (1 query + up to 100 docs)
- Cohere Rerank v3: was $2/M tokens

Vector DB cost at 10M vectors (approximate, May 2026):
- Pinecone Serverless: ~$70/mo ($8.25/M reads, $2/M writes, $0.33/GB)
- Weaviate Flex: ~$45/mo + $0.095/M dims
- Qdrant Cloud: ~$65/mo (1GB free)
- Turbopuffer: min $64/mo, ~$9/M reads+writes, S3-backed storage $0.02/GB

At 100M vectors: Pinecone $700+, self-hosted Qdrant/Weaviate often <$100. Source: [particula.tech vector DB comparison](https://particula.tech/blog/pinecone-vs-weaviate-vs-qdrant-vector-database). Numbers verified at time of writing; vector DB pricing changes — verify on the provider's pricing page for production budgeting.

### 9. Optimization patterns checklist

For an existing system, work top-down — biggest wins first:

- [ ] Caching — system prompts + long tool/skill defs + few-shot examples marked with cache_control or wrapped in the OpenAI auto-cache range (≥1024 tokens)
- [ ] Batching — any non-real-time path moved to Batch API
- [ ] Model routing — small model default, escalate on signal; manual rules with eval gates per tier
- [ ] Output format — structured outputs; no markdown when consumer is machine; ban CoT preambles via system prompt
- [ ] RAG over-fetch — measure context-token waste; tighten top-k; rerank; check for duplicate chunks
- [ ] Per-feature attribution — every call tagged with feature, team, customer-tier
- [ ] Streaming + abort — wired for any user-facing path
- [ ] Embedding choice — voyage-3-lite or text-embedding-3-small for typical retrieval; only upgrade when RAG eval shows lift
- [ ] Reranker is on top-50 first-stage, not top-500 — reranker cost scales with candidate count

### 10. Production case studies (with caveats)

- Klarna AI assistant — 2.3M chats in 30 days (≈700 FTE), 67% automation, reported $40M annual savings; 80% lower resolution time. [LangChain customer story](https://blog.langchain.com/customers-klarna/). Caveat: Klarna publicly walked back parts of the "AI-first" claim in 2025 and rehired human support; the cost story is real, the quality story was overstated.
- Notion — 100M+ users; reportedly 90% of AI dev time spent on evals/observability; tiered eval stack (cheap unit tests run frequently, expensive regressions gated). Verify source attribution before citing externally.
- Intercom Fin — agent resolution rates moved from ~25% to ~60% via GPT-4 + custom RAG + reranking. Verify exact figures via Intercom's own materials before publishing.

Case studies are useful for direction; production budgeting requires your own attribution data, not vendor blog numbers.

## Composition / References

Within-domain pairings:
- Pairs with the sibling AI skill on RAG patterns (RAG cost stack — embeddings, rerank, vector DB).
- Pairs with the sibling AI skill on agent design (multi-agent and tool-call cost trade-offs).
- Pairs with the sibling AI skill on evals (eval workloads belong on Batch APIs).

Primary sources:
- [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- [Anthropic prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [Anthropic Message Batches](https://platform.claude.com/docs/en/build-with-claude/batch-processing)
- [OpenAI pricing](https://openai.com/api/pricing/)
- [OpenAI prompt caching announcement](https://openai.com/index/api-prompt-caching/)
- [OpenAI Batch API guide](https://developers.openai.com/api/docs/guides/batch)
- [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Gemini Batch API](https://ai.google.dev/gemini-api/docs/batch-api)
- [Cohere pricing](https://cohere.com/pricing)
- [Langfuse token and cost tracking](https://langfuse.com/docs/observability/features/token-and-cost-tracking)
- [Helicone](https://www.helicone.ai/)
- [Phoenix (Arize)](https://github.com/Arize-ai/phoenix)
- [Vantage — FinOps for AI](https://www.vantage.sh/blog/finops-for-ai-token-costs)
- [RouterArena benchmark, arXiv:2510.00202](https://arxiv.org/html/2510.00202v1)
- [codeant.ai — input vs output token cost](https://www.codeant.ai/blogs/input-vs-output-vs-reasoning-tokens-cost)
