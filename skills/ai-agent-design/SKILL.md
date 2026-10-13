---
name: ai-agent-design
title: "AI Agent Design: Loops, Tools, Schemas, Orchestration"
description: "Operational playbook for designing production LLM agents in 2026. Covers agent loop patterns (ReAct, Reflexion, Plan-and-Execute, native tool use), tool schema engineering (descriptions, strict mode, input examples, tool search, anti-patterns), the Agent Skills open standard, Model Context Protocol (spec 2026-07-28) integration and security, multi-agent orchestration (LangGraph, CrewAI, AutoGen, vendor agent SDKs) with cost trade-offs, error handling, loop prevention and unattended-run termination, observability via OpenTelemetry GenAI semantic conventions, OWASP LLM and Agentic Top 10 mapping, and context engineering (just-in-time retrieval, compaction, memory, sub-agent isolation, caching). Use when designing a new agent, picking an orchestration framework, debugging a misbehaving agent, or hardening tool exposure. Output: agent specs with named patterns, cost projections, observability hooks, and OWASP-mapped risk surfaces."
license: Apache-2.0
compatibility: "Stack-agnostic. Production agent stacks typically need: LLM provider SDK (Anthropic / OpenAI / Google), an orchestration framework or hand-rolled loop, a tracing backend (Langfuse / Phoenix / OpenTelemetry collector), MCP servers or REST tools."
domains: ai
rules:
  - session(ai)
  - content(agent)
  - content(agents)
  - content(tool use)
  - content(function calling)
  - content(MCP)
  - content(orchestration)
  - match(\b(agent\s+(loop|design|pattern|architecture))\b)
  - match(\b(tool[\s-]?(use|call|calling|schema))\b)
  - match(\b(function[\s-]?call(ing|s)?)\b)
  - match(\b(ReAct|Reflexion|Plan-and-Execute|Tree[\s-]?of[\s-]?Thoughts|ToT)\b)
  - match(\b(LangGraph|CrewAI|AutoGen)\b)
  - match(\b(multi[\s-]?agent)\b)
  - match(\b(Model\s+Context\s+Protocol|MCP)\b)
  - match(\b(Agent\s+Skills)\b)
  - match(\b(context\s+engineering)\b)
  - semantic(design an LLM agent with tools)
  - semantic(my agent is stuck in a loop)
  - semantic(should we use multi-agent or single agent with tools)
  - semantic(what is the best agent framework)
  - semantic(write tool schemas for my agent)
---

## Overview

A production LLM agent is a loop: model proposes an action (often a tool call), system executes it, result becomes the next observation, repeat until done. The interesting questions are: which loop pattern, what tools, what schemas, what stops infinite recursion, what's logged for debugging, what's the cost ceiling per task, and which OWASP risks are alive in this surface. This skill encodes the 2026 patterns with cited sources, and the cost / risk numbers that decide architectural choices.

Use this skill when designing a new agent, picking an orchestration framework, debugging a misbehaving agent, or hardening tool exposure. Skip it for single-shot LLM prompts that don't call tools — that's a prompt problem, not an agent problem.

## Mental model

Three forces shape every agent design:

1. Loop structure — how the model reasons across steps. ReAct (interleaved thought-action-observation) is the foundation; Reflexion adds self-critique; Plan-and-Execute splits planning from execution; native function calling (OpenAI / Anthropic tool use) is the production-grade structured variant.
2. Tool surface — what the agent can do. The schema is the API; descriptions decide behavior; the privilege scope decides blast radius. Tool design is the highest-leverage engineering surface and the most-underserved craft.
3. Failure containment — what stops the agent when things go wrong. Max iterations, action deduplication, error feedback, escalation ladders. Without these, an agent that hits an unhandled state burns money in a loop until someone notices.

The 2026 shift: "prompt engineering" → "context engineering" — curating the whole window (system prompt, tools, retrieved docs, memory, history, examples, output format) across many turns. See §9.

## Instructions

### 1. Agent loop patterns

| Pattern | When to use | Source |
|---|---|---|
| ReAct (Thought → Action → Observation) | Default for tool-using agents | Yao et al., Princeton/Google, Oct 2022, [arXiv:2210.03629](https://arxiv.org/abs/2210.03629) |
| Reflexion | Trial-and-error tasks where self-critique helps; more expensive | Shinn et al., [arXiv:2303.11366](https://arxiv.org/abs/2303.11366) |
| Tree-of-Thoughts (ToT) | Hard search problems where ReAct gets stuck; branches reasoning paths | Yao et al., [arXiv:2305.10601](https://arxiv.org/abs/2305.10601) |
| Plan-and-Execute | Cheaper than ReAct (fewer LLM calls per step); brittle when early steps surprise | LangGraph docs; practitioner pattern |
| ReWOO (Reasoning WithOut Observation) | Reduce tokens by decoupling reasoning from tool execution | [arXiv:2305.18323](https://arxiv.org/abs/2305.18323) |
| Native tool use (OpenAI function calling / Anthropic tool use) | Production-grade structured tool invocation; default for new builds | [OpenAI function calling](https://platform.openai.com/docs/guides/function-calling); [Anthropic define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools) |

Both providers converge on JSON Schema tool inputs with a strict mode. Anthropic adds `input_examples`, tool search with deferred loading for large tool sets, and programmatic tool calling (the model orchestrates tools from code execution). The newest Claude models (Opus 5.5, Sonnet 5.5, Fable 5.1) reject forced `tool_choice` (`any` / `tool`): use `auto` with a prompt instruction, `strict: true`, or structured outputs.

### 2. Tool schema design

The most-underserved craft area in 2026. Bad tool schemas produce loops, wrong-tool calls, and ambiguous outcomes.

Best practices (per [Anthropic define-tools docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools) and [Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)):
- Descriptions are the biggest lever: what the tool does, when to use it and when not, what each parameter means, caveats. Aim for 3–4+ sentences.
- Consolidate related operations into fewer tools (an `action` parameter) and namespace by service (`github_list_prs`); no two tools should plausibly answer the same query.
- Use `input_examples` or in-description examples for nested or format-sensitive inputs; explicit JSON Schema types; strict mode where available.
- Return only high-signal fields with stable, semantic identifiers; bloated tool results waste context.
- If a parameter asks why the call is made, ask for a short explanation, not step-by-step reasoning (the newest Claude models may decline reasoning-extraction requests).

Anti-patterns: generic names (`get_data`), overlapping tools (`search_customers` vs `find_customer`), many optional fields (filled with hallucinated defaults), vague return shapes.

### 3. Agent Skills (open standard, Dec 2025)

Anthropic published Agent Skills as an open standard on Dec 18, 2025; the spec lives at [agentskills.io](https://agentskills.io/specification). A skill is a directory with `SKILL.md` (YAML frontmatter + instruction body) and optional scripts and references, loaded on demand so only the frontmatter costs context until it's needed. Use skills for portable expertise that should travel between agents and clients; verify which clients support the current spec before relying on it.

### 4. Model Context Protocol (MCP)

Open protocol launched by Anthropic in Nov 2024, governed since Dec 2025 under the Linux Foundation's Agentic AI Foundation. Current spec revision: [2026-07-28](https://modelcontextprotocol.io/specification/latest/changelog), a partly breaking release:
- Stateless: no `initialize` handshake and no `Mcp-Session-Id`; each request carries protocol version and capabilities in `_meta`; servers implement `server/discover`. Cross-call state uses server-minted handles passed as tool arguments.
- Transports: stdio and Streamable HTTP (requests carry `Mcp-Method` / `Mcp-Name` headers); HTTP+SSE is deprecated.
- Multi Round-Trip Requests replace server-initiated sampling, elicitation, and roots requests; Roots, Sampling, and Logging are deprecated. Tasks moved to an official extension.
- Auth: OAuth with Client ID Metadata Documents preferred over Dynamic Client Registration; clients validate `iss`.
- `tools/list` should be deterministic (helps prompt-cache hits) and carries cache TTL hints.

Security ([best practices](https://modelcontextprotocol.io/specification/latest/basic/security_best_practices)): servers must not accept or pass through tokens not issued to them; proxies need per-client consent; state handles are never authentication; local servers need explicit install consent and sandboxing; request minimal scopes and step up.

MCP vs REST: MCP when a tool will be reused across agents and clients (discovery, schemas, structured errors); REST when the tool is one-off or already a deployed service.

### 5. Multi-agent orchestration

| Framework | Strength | Trade-off |
|---|---|---|
| LangGraph | Stateful graph + conditional edges; most production-tested OSS option | Steeper learning curve; LangChain abstractions |
| CrewAI | Role-based crews; lowest onboarding cost | Less control over execution |
| AutoGen | Conversational group-chat patterns | Every turn re-reads the full history; expensive at volume |
| Vendor agent SDKs (Claude Agent SDK, OpenAI Agents SDK, Google ADK) | Provider-tuned harness: tools, subagents, context management | Tied to one provider's features |

Cost trade-off: multi-agent is typically 2–4× single-agent for similar tasks; a 4-agent × 5-round debate is 20+ LLM calls minimum. Use it when sub-tasks are genuinely parallel, need isolated context windows, or need different tools; otherwise single agent + better tools + better context. Current frontier models delegate to subagents readily, so state when subagents are and aren't warranted.

Orchestration patterns:
- Orchestrator-worker: one planner agent dispatches to worker agents
- Supervisor: hierarchical with a manager and specialist subordinates
- Swarm: peer-to-peer with shared state
- Sequential pipeline: agents in fixed order; cheapest multi-agent variant

### 6. Error handling and infinite-loop prevention

Hard requirements for every production agent:

- Hard max_turns / max wall-time / token budget — every agent. A stuck 50-turn run with rich context costs dollars on a frontier model; compute yours from the price book. Use provider budget controls where they exist (Anthropic task budgets, beta) on top of your own caps.
- Action deduplication — hash `(tool_name, args)` across a run; flag a repeat as a likely loop.
- Action-history comparison — detect oscillation (A → B → A → B …).
- Exponential backoff on retries — 3–5 retries general; 5–7 for rate limits.
- Error message as observation — when a tool fails, feed the error text back as the observation so the model can reason about recovery.
- Escalation ladder — reflection prompt → alternative tool suggestion → context compression + restart → graceful termination with partial results.
- Termination predicate — explicit "done" condition in the system prompt, plus a harness-side check. Unattended loops must not treat a text-only turn as completion: newer models end turns with progress reports, so keep a task checklist, nudge on open items, and stop after two or three automatic continuations ([Prompting Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5)).

Common root causes of stuck agents: missing max_turns, broken termination predicate, ambiguous tool schemas, oscillation between two near-equivalent actions.

### 7. Observability

OpenTelemetry GenAI semantic conventions — span names, tool-call attributes, agent spans, PII-safe content capture. They now live in their own repository and are still evolving, so pin the version you emit. MCP (2026-07-28) documents `traceparent` propagation in `_meta`, so traces can cross server boundaries.

| Tool | Strength |
|---|---|
| Langfuse | ClickHouse backend, native OTLP endpoint (`/api/public/otel`), strong multi-tenant; OSS |
| Arize Phoenix | Local-first, notebook-friendly, zero external deps; OSS |
| Helicone | Drop-in proxy when you cannot instrument code; OSS |
| LangSmith | Deepest LangChain integration; paid, per-seat |

Per-tool-call log — tool name, args (PII-safe), result, latency, token count, cost, error, parent span ID. Without these, debugging a multi-step failure is forensic guessing.

### 8. OWASP risks and production failures

Map every tool, retrieved-context source, memory store, and output sink to the OWASP Top 10 for LLM Applications (2026 edition; name the edition, since many reports still use 2025 IDs) and the Agentic Top 10 (ASI01 Agent Goal Hijack … ASI10 Rogue Agents, Dec 2025). Full tables and defenses live in the sibling prompt-injection-defense skill.

Agentic failures to design against: Slack AI (Aug 2024, indirect injection exfiltrating private-channel data), EchoLeak (CVE-2025-32711, zero-click via email), GitHub Copilot RCE (CVE-2025-53773), ForcedLeak in Salesforce Agentforce (Sep 2025). In each, untrusted content reached an action surface. Design rule: no session should combine untrusted input, private data access, and external communication or state change without isolation or human confirmation (the "lethal trifecta").

### 9. Context engineering (the discipline)

Popularized in June 2025 (Tobi Lütke, Andrej Karpathy) as "filling the context window with just the right information for the next step." It covers system prompt, tool definitions, retrieved docs, memory, history, examples, and output constraints; prompt engineering is a subset.

Practical implications (Anthropic, [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), Sep 2025):
- Treat context as a finite budget; recall degrades as it grows (context rot), so the goal is the smallest high-signal set.
- Retrieve just in time: give the agent lightweight identifiers (paths, queries, links) and tools to load data when needed instead of pre-loading everything.
- Long-horizon work: compaction (summarize and restart), structured note-taking or memory files outside the window, and sub-agents with clean context windows that return condensed results. Server-side compaction and context editing exist on some APIs; on Claude models that enforce preserved thinking, keep histories append-only and let the server compact.
- Keep the prefix cache-stable: deterministic tool order, static system prompt, volatile data last.
- Untrusted retrieved content goes in clearly labeled tags (see the prompt-injection skill).

Cross-reference the cost / FinOps skill for caching numbers.

## Checklist

- [ ] Loop pattern named (ReAct / Reflexion / Plan-and-Execute / native function calling) with rationale
- [ ] Tool descriptions say what, when, when not, and caveats; examples for complex inputs; strict mode where available
- [ ] No overlapping tools; related operations consolidated and namespaced; tool results high-signal
- [ ] Hard max_turns + max wall-time configured
- [ ] Action deduplication + oscillation detection in place
- [ ] Error feedback loop wired (tool errors become observations)
- [ ] Termination predicate explicit; unattended harness doesn't treat a text-only turn as done
- [ ] OpenTelemetry GenAI tracing enabled (Langfuse / Phoenix / Helicone / LangSmith)
- [ ] Per-tool-call logging with cost, latency, token count
- [ ] OWASP LLM (edition stated) + Agentic Top 10 risks mapped per tool / context source / output sink; no unguarded lethal-trifecta sessions
- [ ] Single-agent considered before multi-agent (cost rationale documented if multi-agent chosen)
- [ ] Prefix cache-stable: static system prompt, deterministic tool order, cache breakpoints set
- [ ] If using MCP: targets spec 2026-07-28, auth via Client ID Metadata Documents, no token passthrough, third-party servers pinned and reviewed

## Composition / References

Within-domain pairings:
- Pairs with the sibling AI skill on RAG patterns (most agents use retrieval as a tool).
- Pairs with the sibling AI skill on evals (every agent needs trajectory + tool-use accuracy eval).
- Pairs with the sibling AI skill on cost optimization (multi-agent and tool calls are the dominant cost drivers).
- Pairs with the sibling AI skill on prompt injection defense (every tool surface is an attack surface).

Primary sources:
- [ReAct, arXiv:2210.03629](https://arxiv.org/abs/2210.03629)
- [Anthropic — Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)
- [Anthropic — Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
- [Anthropic — Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [MCP specification 2026-07-28 changelog](https://modelcontextprotocol.io/specification/latest/changelog)
- [MCP security best practices](https://modelcontextprotocol.io/specification/latest/basic/security_best_practices)
- [Agent Skills specification](https://agentskills.io/specification)
- [Anthropic — Donating MCP and the Agentic AI Foundation](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation)
- [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
- [Langfuse OpenTelemetry integration](https://langfuse.com/integrations/native/opentelemetry)
