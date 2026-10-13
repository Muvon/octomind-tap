---
name: ai-cost-finops
title: "AI Cost & FinOps: Caching, Batching, Model Routing"
description: "Operational playbook for cutting LLM application cost in 2026. Covers the current price book (Anthropic Claude Fable/Opus/Sonnet/Haiku, OpenAI GPT-6 Astra/Sol/Luna, Google Gemini Pro/Flash/Flash-Lite), prompt caching mechanics (Anthropic write/read multipliers and TTLs, OpenAI and Gemini automatic caching), Batch and Flex tiers (50% off), effort and reasoning-depth controls, model routing vs effort tuning, output-length discipline, the RAG cost stack (embeddings, rerank, vector DBs), and FinOps attribution (provider usage APIs, Helicone, Langfuse, Phoenix, Vantage). Use when projecting LLM cost, hunting waste in an existing pipeline, picking a model or effort level, or setting up per-feature attribution. Output: cost-per-task projections with cited, dated prices and quantified optimization levers."
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
  - match(\b(Fable|Haiku|Sonnet|Opus|GPT-?6|Astra|Gemini\s+(Pro|Flash))\b)
  - match(\b(Helicone|Langfuse|Vantage|Phoenix|LangSmith|OpenLLMetry)\b)
  - semantic(reduce our LLM API spend)
  - semantic(why is our AI bill so high)
  - semantic(should we use Opus or Haiku for this)
  - semantic(set up cost tracking for our AI features)
  - semantic(what does prompt caching save)
---

## Overview

LLM cost is an engineering surface, not a line on the card statement. The levers that move it most in 2026, in order: prompt caching (cache reads cost a tenth of input or less), Batch/Flex tiers (50% off), effort or reasoning-depth tuning, then model routing. This skill holds the dated price book, the discount mechanics, and the optimization order with primary-source citations.

Use it when projecting cost for a new feature, hunting waste in an existing pipeline, picking a model or effort level, or setting up per-feature attribution. Skip it for prototypes spending under ~$100/month.

## Mental model

Every call costs `uncached_input × $in + cache_writes × $write + cache_reads × $read + output × $out` (thinking tokens bill as output), plus retrieval, rerank, and storage for RAG. Judge cost per completed task, not per request: a cheaper call that needs more turns or retries is not cheaper.

Work the levers in order. Free wins first, because they don't trade quality: caching, input hygiene, output hygiene, batch. Then quality trades, measured against an eval: effort level, then model choice. The cheapest call is the one not made; then the cached one; then the batched one; then the one at lower effort or on a smaller model.

Output tokens cost 5× input on most current models, so output-length discipline (no markdown for machine consumers, no preambles) is the next lever after caching.

## Rules

### 1. Price book (2026: verified 2026-10-12, per 1M tokens, standard tier, input/output)

Prices change quarterly. Re-check the pricing pages before any budget.

| Provider | Model | Input | Output | Notes |
|---|---|---|---|---|
| Anthropic | Claude Fable 5.1 | $10 | $50 | Most capable widely released Claude; thinking always on |
| Anthropic | Claude Opus 5.5 | $4 | $20 | Default effort `medium` |
| Anthropic | Claude Sonnet 5.5 | $2 | $10 | |
| Anthropic | Claude Haiku 5.5 | $0.10 | $0.50 | Prompts ≤100K tokens; $0.50 / $2.50 above |
| OpenAI | gpt-6-astra | $10 | $50 | Cached input $1; >272K input billed at a higher tier |
| OpenAI | gpt-6.1-sol | $2 | $10 | Cached input $0.10 |
| OpenAI | gpt-6-luna | $0.10 | $0.50 | Cached input $0.01 |
| Google | Gemini 3.1 Pro (preview) | $2 | $12 | ≤200K prompt; $4 / $18 above |
| Google | Gemini 3.8 Flash | $0.75 | $3.75 | Promotional to 31 Dec 2026, then $1.50 / $7.50 |
| Google | Gemini 3.5 Flash-Lite | $0.30 | $2.50 | |

Sources: [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing), [OpenAI pricing](https://developers.openai.com/api/docs/pricing), [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing). Older generations stay listed at their own prices; Claude Opus 4.7 and later use a tokenizer that emits ~1–1.35× the tokens of older Claude models, so re-baseline with token counting when migrating. Regional data-residency endpoints carry uplifts on some providers (OpenAI: +10%).

### 2. Prompt caching

Anthropic ([docs](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)):
- Writes cost 1.25× input (5-minute TTL, the default) or 2× (1-hour TTL, set `"ttl": "1h"`). Reads cost ~0.1× input; 0.05× on Opus 5.5 and 0.025× on Fable 5.1.
- Break-even: two requests on the 5-minute TTL, three on the 1-hour. A cache read refreshes the TTL, so traffic that arrives less than 5 minutes apart never needs the 1-hour TTL.
- Prefix match in render order tools → system → messages; any byte change invalidates everything after it. Max 4 breakpoints; minimum cacheable prefix is model-dependent (512–4096 tokens) and shorter prefixes silently don't cache.
- Top-level automatic caching moves the breakpoint forward as a conversation grows; add an explicit breakpoint on the static system prefix for agent loops.
- Caches are model-scoped, and changing top-level effort mid-conversation invalidates the message cache.
- Verify with `usage.cache_read_input_tokens`; zero across repeated requests means a silent invalidator (timestamps in the system prompt, unsorted JSON, a varying tool list).

OpenAI: automatic prefix caching, no code change; cached input is billed at 5–10% of input on the GPT-6 family (pricing page). Gemini: implicit caching plus explicit context caches billed at ~10% of input plus hourly storage.

Cache system prompts, tool and skill definitions, few-shot examples, and long static documents — anything long, stable, and re-sent.

### 3. Batch and Flex (50% off anything nobody waits on)

- Anthropic Message Batches — 50% off every token, including cache reads and writes; results within 24 hours, in any order (key by `custom_id`). No mid-batch tool loop. [docs](https://platform.claude.com/docs/en/build-with-claude/batch-processing)
- OpenAI Batch and Flex — both 50% below standard on current models. [pricing](https://developers.openai.com/api/docs/pricing)
- Gemini Batch and Flex — 50% off; Priority costs ~1.8×. [pricing](https://ai.google.dev/gemini-api/docs/pricing)

Use for evals, backfills, embeddings, dataset enrichment, and scheduled jobs.

### 4. Effort before routing

Current frontier models expose a reasoning-depth control: Claude `output_config.effort` (`low` → `max`, with adaptive thinking), OpenAI reasoning effort, Gemini thinking level. Effort is the first quality-trading lever: it trades thoroughness for tokens inside one model and keeps one cache namespace.

- Effort names don't mean the same thinking budget across models; re-run the sweep per model. Anthropic reports Opus 5.5 at `medium` matching or beating Opus 5 at `high` on coding and knowledge work ([prompting guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5)).
- Chat, classification, and high-volume routes often hold quality at `low`; coding and long-horizon agents repay `high`/`xhigh`. Tune per route, not globally.
- Before building a multi-model cascade, measure the strongest model at lower effort on the same tasks.

### 5. Model routing

| Approach | Pros | Cons |
|---|---|---|
| Manual rules (classify by complexity, escalate on validation failure) | Predictable, auditable | Needs upfront classification logic |
| Commercial routers (Martian, NotDiamond, OpenRouter Auto) | Zero setup | Vendor-claimed savings; often pick expensive models ([RouterArena, arXiv:2510.00202](https://arxiv.org/abs/2510.00202)) |

Pattern: small model by default (Haiku, Flash-Lite, Luna), escalate to mid-tier on low confidence or failed validation, reserve the top tier for hard-reasoning paths — with an eval gate per tier. Every model switch forfeits cache reuse.

### 6. Output and input hygiene

- Structured outputs (Anthropic `output_config.format` and strict tools, OpenAI Structured Outputs) kill preambles and parse-retry loops.
- No markdown when the consumer is a machine; ban preambles in the system prompt.
- Don't ask current reasoning models to write their reasoning into the answer: it costs output tokens, and on the newest Claude models it can be declined (`reasoning_extraction`). Lower effort instead.
- Trim tool results to high-signal fields; cap or compact long histories.
- Set `max_tokens` with room for thinking — a truncated answer you retry costs twice.

### 7. FinOps observability and attribution

| Tool | Mode | Strength |
|---|---|---|
| Provider usage/cost APIs (Anthropic Usage & Cost Admin API, OpenAI usage) | Org-level | Ground truth for spend by model, key, workspace |
| Helicone | Gateway (URL swap) | Always-on cost/latency logging; OSS |
| Langfuse | SDK or OTLP | Per-generation cost tracking; OSS |
| Phoenix (Arize) | OSS, OTLP-native | Local-first trace analysis |
| LangSmith | SDK | Deepest LangChain integration |
| Vantage | FinOps platform | Cross-provider and cloud roll-up, per-team allocation |

Check current plan pricing on each vendor's site. Tag every call with `feature`, `team`, `customer_tier`, `experiment_arm`; use per-project API keys or workspaces so usage reports are attributable. Without attribution you can't optimize.

### 8. Waste patterns

| Pattern | Impact | Fix |
|---|---|---|
| Uncached system prompt and tools re-sent every turn | Full input price per turn | Stable prefix + breakpoints; verify hit rate |
| Timestamp or request ID in the system prompt | Cache never hits | Move volatile content after the last breakpoint |
| Over-retrieved RAG context | Input bloat | Rerank + tighter top-k |
| JSON parse-retry loops | 2–3× cost on flaky calls | Structured outputs / strict tools |
| Top tier at top effort for routine traffic | Several-fold over-spend | Effort sweep, then routing, gated by evals |
| No streaming abort | Pay for bad output | Stream and stop on quality signals |

### 9. RAG cost stack

- Embeddings are usually a rounding error next to generation; upgrade the embedding model only when retrieval evals show lift.
- Rerankers bill per search (Cohere: one query + up to 100 documents; Rerank 4 shipped Apr 2026) — cost scales with candidates, so rerank the top 50, not the top 500.
- Managed vector DBs (Pinecone, Weaviate, Qdrant, Turbopuffer) price on storage, reads, and writes; self-hosting wins at very large scale. Price your own volume on the vendor pages.
- A stable corpus under ~200K tokens can skip RAG entirely: put it in the prompt and cache it ([Anthropic Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)).

## Examples

Bad: "Use Opus for everything; it's the best." No per-task cost, no eval, no effort setting.

Good: "Support triage runs 40K requests/day with a 6K-token static prefix. Caching the prefix cuts that input to ~0.1× after the first write; the nightly re-classification moves to Batch at 50% off; an effort sweep shows `low` holds the 94% routing accuracy of `high`. Projected per-ticket cost drops from $X to $Y (prices from the pricing page, 2026-10-12)."

Case studies (Klarna, Intercom Fin) are useful for direction only; budget from your own attribution data, not vendor blog numbers.

## Checklist

- [ ] Prices quoted with the date checked and the source URL
- [ ] Cache hit rate measured from usage fields; static prefix byte-stable; TTL chosen from request gaps
- [ ] Every non-real-time path on Batch or Flex
- [ ] Effort swept per route against an eval before any model routing
- [ ] Routing tiers each gated by an eval; cache-scope loss accounted for
- [ ] Structured outputs on machine-consumed paths; no preambles; `max_tokens` leaves room for thinking
- [ ] RAG: rerank depth bounded; long-context-with-cache considered for small corpora
- [ ] Every call tagged for per-feature attribution; per-project keys or workspaces
- [ ] Cost reported per completed task, not per request

## Composition / References

Within-domain pairings:
- Pairs with the sibling AI skill on RAG patterns (embeddings, rerank, vector DB costs).
- Pairs with the sibling AI skill on agent design (multi-agent and tool-loop cost).
- Pairs with the sibling AI skill on evals (every effort or routing change needs an eval gate; eval runs belong on Batch).

Primary sources:
- [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- [Anthropic prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [Anthropic batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing)
- [Anthropic effort](https://platform.claude.com/docs/en/build-with-claude/effort)
- [OpenAI pricing](https://developers.openai.com/api/docs/pricing)
- [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Langfuse token and cost tracking](https://langfuse.com/docs/observability/features/token-and-cost-tracking)
- [RouterArena, arXiv:2510.00202](https://arxiv.org/abs/2510.00202)
