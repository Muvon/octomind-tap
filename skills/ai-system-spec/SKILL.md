---
name: ai-system-spec
title: "AI System Spec: Architecture, Cost Model, Hand-Off"
description: "Architect an LLM application: pattern, model and effort, context and caching, tracing, cost model, written spec. Use for new RAG or agent builds."
license: Apache-2.0
compatibility: "Stack-agnostic. Needs web access to read current provider docs and pricing pages."
domains: ai-engineer
rules:
  - match((?i)\b(build|implement|add|wire|migrate|refactor|rework|package|set\s+up|write|design)\b.{0,50}\b(prompt\s+caching|model\s+routing|token[\s-]accounting|batch\s+api|MCP\s+server|tool\s+schemas?|agent\s+loop|agent\s+skill|message\s+history|(production\s+)?tracing|hybrid\s+retrieval|retrieval\s+pipeline|chunking|query\s+rewriting|contextual\s+retrieval)\b)
  - match((?i)\b(cut|reduce|lower|bring\s+down)\b.{0,30}\b(LLM|API|token|OpenAI)\s+(spend|costs?|bill)\b|\b(LLM|OpenAI|Anthropic|API)\s+bill\b|\btokens\s+are\s+(being\s+)?wasted\b)
  - match((?i)\b(model\s+selection|routing\s+(recommendation|config)|cost\s+model|system\s+spec|architecture\s+spec)\b)
  - match((?i)\b(build|implement|ship)\b.{0,30}\b(LLM\s+app\w*|AI\s+(app|feature)|chatbot|voice\s+agent|multi-agent\s+pipeline)\b)
  - match((?i)\b(architect|design|spec|plan)\b.{0,40}\b(LLM|RAG|AI|agent)\s+(system|app|application|pipeline|feature|architecture)\b)
  - semantic(architect an LLM application under a budget and latency target, 0.72)
  - semantic(choose a model and caching strategy for our new RAG product, 0.72)
  - semantic(write a design spec for an agent with tools and tracing, 0.72)
  - semantic(cut our language model spend without hurting answer quality, 0.72)
---

## Overview

Building an LLM application well means choosing the simplest pattern that meets the accuracy, latency, and cost targets, then instrumenting it so it can be evaluated and attacked. This skill gives the build sequence, the decision rules that set the architecture, and a written spec that records the choices and the hand-off checks. Use it when starting a RAG, agent, multi-agent, voice, or hybrid build, or when reviewing an architecture. Skip it for a single prompt with no tools or retrieval.

## Mental model

Every architectural choice is priced, and every choice names its typical failure: retrieval miss, hallucination, tool loop, context pollution, cost spike, P99 latency. Production means concurrency, partial failures, observability, and a cost ceiling. Notebook-only ideas are labelled as such.

## Rules

Working method:

1. Collect the use case and constraints: budget, latency target, accuracy target, scale. Ask once when they are missing; a non-interactive brief applies defaults and lists the assumptions in the spec.
2. Architect: RAG, agent, hybrid, or pipeline; models, effort, and routing; context and caching; observability; the evaluation surface.
3. Build incrementally: the cheapest version that could work, with tracing and a cache-stable prefix from the first request. Add reranking, fallbacks, and routing only when the evaluation surface shows they are needed.
4. Instrument for hand-off: trace every prompt, completion, and tool call; tag spans so evaluations can consume them; attribute cost per task.
5. Hand off: name what evaluation and red-team work should test, and the failure modes already known.

Decision rules:

- Cheap before clever: start with the simplest model and the smallest context. Add complexity when a measured shortfall justifies it.
- Effort before model swaps. Frontier models expose a reasoning-depth control (Claude effort with adaptive thinking; OpenAI reasoning effort). Measure the strongest model at lower effort before building a multi-model cascade: caches are model-scoped and cost is per completed task, not per request.
- Long context versus RAG is a cost and accuracy trade. Effective context degrades well before the window limit (RULER; Chroma "Context Rot", Jul 2025). A stable corpus under about 200K tokens usually belongs in the prompt with caching (Anthropic Contextual Retrieval post). Large, fast-changing, or citation-audited corpora belong in RAG.
- Cache by design. Keep the prefix byte-stable, with timestamps and request IDs after the last breakpoint, and verify hits from usage fields, not code review. Anthropic cache writes cost 1.25x (5-minute TTL) or 2x (1-hour TTL) and reads about 0.1x input or less; OpenAI and Gemini cache prefixes automatically. Take current multipliers from the pricing pages.
- Batch anything nobody waits on. Anthropic Message Batches, OpenAI Batch and Flex, and Gemini Batch run at 50% off; Anthropic's batch discount stacks with caching. Evals, backfills, and async pipelines belong there.
- Hybrid retrieval plus rerank is the production default: BM25, dense, and fusion, then a reranker (Cohere Rerank 4, cross-encoders, BGE) over the top 50 to 100 candidates.
- Tool schemas decide agent behavior: detailed descriptions (what, when, when not, caveats), namespaced and consolidated tools, high-signal responses, `strict: true`, and tool search for large tool sets. The newest Claude models reject forced `tool_choice`; use `auto` with prompt steering, strict tools, or structured outputs.
- Treat all LLM output as untrusted input. Output that flows into tools, SQL, shells, or other prompts is validated and constrained (structured outputs, schemas, output guards); list these sinks in the red-team hand-off.
- Multi-agent costs 2 to 4 times a single agent. Use it only when one agent with rich tools cannot solve the problem.
- Observability is day-1 work. Use the OpenTelemetry GenAI semantic conventions as the span schema.
- Output format is a cost lever. Structured outputs (Anthropic `output_config.format`, OpenAI Structured Outputs) replace prefill; assistant prefill returns 400 on Claude 4.6 and later. No markdown when no one reads it.
- MCP: target the current spec (2026-07-28: stateless Streamable HTTP, no session header, Client ID Metadata Documents for registration). Servers never pass client tokens through to downstream APIs.
- Verify model names, prices, and API parameters against primary docs before stating them; they change quarterly. Cite the source for any number. Don't pick the top tier or top effort when a cheaper tier or lower effort shows no evaluation degradation.

## Examples

- Build me a RAG: ask for corpus size, refresh rate, latency target, budget, and accuracy target, then architect.
- Build me an agent: ask for the tools needed, the iteration cap, which tools write, and the budget, then design.
- Optimize cost: ask for the current cost breakdown by feature, then propose caching, batch, effort, routing, and format changes, each quantified.
- Why is this slow: read the traces first; don't speculate.

## Output format

Save specs as `ai-system-spec-[slug].md` in the working directory. Implementation diffs add a cost estimate per task, a trace example, and an evaluation hook example.

```markdown
# AI System Spec: [Name]

## Use case
- What the system does: [...]
- Inputs: [...]
- Outputs: [...]
- Users and scale: [QPS, daily volume]
- Constraints: latency P50 [...] / P99 [...], cost ceiling [...], accuracy target [...]

## Architecture
- Pattern: RAG / agent / hybrid / pipeline
- Model(s): [primary and effort, fallback, router rules]
- Retrieval (if RAG): [chunking, retrieval, reranking, evaluation]
- Tools (if agent): [list with descriptions]
- Context strategy: [system prompt, caching, history, retrieval]
- Observability: [tracing stack, logged spans]

## Cost model
- Per task: uncached input x $X + cache writes and reads + output (including thinking) x $Y + retrieval $Z
- Daily projection: [...]
- Optimization levers: [caching, batch, effort, routing, output format]

## Hand-off to evaluation
- What to evaluate: [list]
- Suggested metrics: [...]
- Suggested golden set size: [...]

## Hand-off to red-team review
- Attack surface: [tools exposed, user input paths, retrieved content sources]
- Defense layers already in: [structured outputs, content filters, instruction and data separation]
- Suggested red-team scope: [...]
```

## Checklist

- [ ] Constraints (budget, latency, accuracy, scale) stated or defaulted with the assumption listed
- [ ] Pattern chosen with the simpler alternative named and rejected for a measured reason
- [ ] Every price and parameter cites a current source
- [ ] Tracing on from the first request; prefix cache-stable
- [ ] Output sinks that consume model output listed and validated
- [ ] Retries, fallbacks, iteration caps, and output validation designed in
- [ ] Hand-off to evaluation and red-team review written

## Composition / References

- The `ai-agent-design` skill holds loop patterns, tool schemas, MCP, and context engineering.
- The `ai-rag-patterns` skill holds chunking, retrieval, and reranking detail.
- The `ai-cost-finops` skill holds the price book and cost levers.
- The `ai-evals-design` skill and the `ai-prompt-injection-defense` skill cover the two hand-offs.
